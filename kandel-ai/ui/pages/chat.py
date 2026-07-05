"""
KANDEL AI - Chat Page (Cortex AI style with session panel)
Designed by Kandel Sanjaya
"""
import streamlit as st
import json
import time
from core.supervisor import answer_query, is_greeting, detect_language
from ui.components.widgets import chat_bubble_user, chat_bubble_ai, message_meta, electron_loader
from database.db import get_conn
from memory.memory_store import get_all_memory


def _has_documents(user_id: int) -> bool:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM documents WHERE user_id=?", (user_id,))
        return c.fetchone()[0] > 0


def _session_files(user_id: int):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT filename, chunks, created_at FROM documents WHERE user_id=? ORDER BY created_at DESC LIMIT 6", (user_id,))
        return [dict(r) for r in c.fetchall()]


def _export_chat_text(messages: list) -> str:
    lines = []
    for m in messages:
        who = "You" if m["role"] == "user" else "KANDEL AI"
        lines.append(f"{who}: {m['content']}\n")
    return "\n".join(lines)


def _render_session_panel(user: dict, last_model: str, last_latency: float):
    st.markdown('<div class="kai-card">', unsafe_allow_html=True)
    st.markdown("#### 📁 Session Files")
    files = _session_files(user["id"])
    if not files:
        st.caption("No files uploaded yet. Upload documents from the Documents page to enable RAG.")
    for f in files:
        size_kb = f["chunks"] * 1  # rough placeholder proxy for display only
        st.markdown(
            f"""<div style="display:flex;align-items:center;gap:.5rem;padding:.4rem 0;border-bottom:1px solid var(--border);">
            <span>📄</span>
            <div><div style="font-size:.85rem;">{f['filename']}</div>
            <div class="kai-muted" style="font-size:.7rem;">{f['chunks']} chunks</div></div>
            </div>""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="kai-card">', unsafe_allow_html=True)
    st.markdown("#### 🧠 Agent Memory")
    mems = get_all_memory(user["id"])[:3]
    if not mems:
        st.caption("KANDEL AI hasn't learned anything about you yet — start chatting.")
    for m in mems:
        st.markdown(
            f'<div style="font-size:.8rem;padding:.3rem 0;">• {m["summary"] or m["answer"][:60]}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="kai-card">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Model Stats")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Model", last_model.split("-")[0] if last_model else "—")
    with c2:
        st.metric("Latency", f"{last_latency}s" if last_latency else "—")
    st.markdown("</div>", unsafe_allow_html=True)


def render_chat(user: dict):
    if "active_chat_messages" not in st.session_state:
        st.session_state.active_chat_messages = []

    chat_col, panel_col = st.columns([2.6, 1], gap="large")

    with chat_col:
        top_l, top_r = st.columns([4, 2])
        with top_l:
            st.markdown("### Chat with KANDEL AI")
            st.caption("Ask in any language — I'll detect it, remember our conversation, and search when needed.")
        with top_r:
            if st.session_state.active_chat_messages:
                export_text = _export_chat_text(st.session_state.active_chat_messages)
                dc1, dc2 = st.columns(2)
                with dc1:
                    st.download_button(
                        "⬇ Chat", data=export_text,
                        file_name=f"kandel_ai_chat_{int(time.time())}.txt",
                        mime="text/plain", use_container_width=True, key="download_chat_btn",
                    )
                with dc2:
                    st.download_button(
                        "⬇ JSON", data=json.dumps(st.session_state.active_chat_messages, indent=2, default=str),
                        file_name=f"kandel_ai_chat_{int(time.time())}.json",
                        mime="application/json", use_container_width=True, key="download_chat_json_btn",
                    )

        last_model, last_latency = "", 0.0
        for i, msg in enumerate(st.session_state.active_chat_messages):
            if msg["role"] == "user":
                chat_bubble_user(msg["content"])
            else:
                chat_bubble_ai(msg["content"])
                if msg.get("meta"):
                    message_meta(**msg["meta"])
                    last_model = msg["meta"].get("model", "")
                    last_latency = msg["meta"].get("response_time", 0.0)
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
        query = st.chat_input("Ask me anything or paste a document link...")
        query = pending or query

        if query:
            st.session_state.active_chat_messages.append({"role": "user", "content": query})
            chat_bubble_user(query)

            if is_greeting(query):
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

    with panel_col:
        last_model, last_latency = "", 0.0
        for m in reversed(st.session_state.active_chat_messages):
            if m["role"] == "assistant" and m.get("meta"):
                last_model = m["meta"].get("model", "")
                last_latency = m["meta"].get("response_time", 0.0)
                break
        _render_session_panel(user, last_model, last_latency)
