"""
KANDEL AI - Chat Page
Designed by Kandel Sanjaya
"""
import streamlit as st
import json
import time
from core.supervisor import answer_query, is_greeting, detect_language
from ui.components.widgets import chat_bubble_user, chat_bubble_ai, message_meta, electron_loader
from database.db import get_conn


def _has_documents(user_id: int) -> bool:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM documents WHERE user_id=?", (user_id,))
        return c.fetchone()[0] > 0


def _export_chat_text(messages: list) -> str:
    lines = []
    for m in messages:
        who = "You" if m["role"] == "user" else "KANDEL AI"
        lines.append(f"{who}: {m['content']}\n")
    return "\n".join(lines)


def render_chat(user: dict):
    top_l, top_r = st.columns([4, 1])
    with top_l:
        st.markdown("### Chat with KANDEL AI")
        st.caption("Ask in any language — I'll detect it, remember our conversation, and search when needed.")
    with top_r:
        if st.session_state.get("active_chat_messages"):
            export_text = _export_chat_text(st.session_state.active_chat_messages)
            st.download_button(
                "⬇ Download Chat",
                data=export_text,
                file_name=f"kandel_ai_chat_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_chat_btn",
            )
            st.download_button(
                "⬇ Export JSON",
                data=json.dumps(st.session_state.active_chat_messages, indent=2, default=str),
                file_name=f"kandel_ai_chat_{int(time.time())}.json",
                mime="application/json",
                use_container_width=True,
                key="download_chat_json_btn",
            )

    if "active_chat_messages" not in st.session_state:
        st.session_state.active_chat_messages = []

    # render history
    for i, msg in enumerate(st.session_state.active_chat_messages):
        if msg["role"] == "user":
            chat_bubble_user(msg["content"])
        else:
            chat_bubble_ai(msg["content"])
            if msg.get("meta"):
                message_meta(**msg["meta"])
            ac1, ac2, ac3 = st.columns([1, 1, 6])
            with ac1:
                st.download_button(
                    "⬇", data=msg["content"], file_name=f"kandel_ai_reply_{i}.txt",
                    key=f"dl_msg_{i}", use_container_width=True,
                )
            with ac2:
                if st.button("🔁", key=f"regen_msg_{i}", help="Regenerate this response"):
                    st.session_state.pending_query = st.session_state.active_chat_messages[i - 1]["content"]
                    st.session_state.active_chat_messages = st.session_state.active_chat_messages[: i - 1]
                    st.rerun()

    pending = st.session_state.pop("pending_query", None)

    query = st.chat_input("Type your message...")
    query = pending or query

    if query:
        st.session_state.active_chat_messages.append({"role": "user", "content": query})
        chat_bubble_user(query)

        if is_greeting(query):
            lang = detect_language(query)
            greeting_reply = f"Hey {user['name']}! Great to see you. What would you like to work on today?"
            chat_bubble_ai(greeting_reply)
            st.session_state.active_chat_messages.append({"role": "assistant", "content": greeting_reply})
        else:
            placeholder = st.empty()
            with placeholder.container():
                electron_loader("Thinking & routing to the right agent...")

            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.active_chat_messages[:-1]
            ]
            has_docs = _has_documents(user["id"])

            try:
                result = answer_query(user["id"], query, history, has_documents=has_docs, stream=False)
                placeholder.empty()
                chat_bubble_ai(result["answer"])
                meta = {
                    "agent": result["agent"],
                    "model": result["model"],
                    "confidence": result["confidence"],
                    "response_time": result["response_time"],
                    "sources": result["sources"],
                }
                message_meta(**meta)
                st.session_state.active_chat_messages.append(
                    {"role": "assistant", "content": result["answer"], "meta": meta}
                )
            except Exception as e:
                placeholder.empty()
                st.error(f"Something went wrong talking to Groq: {e}")

        st.rerun()
