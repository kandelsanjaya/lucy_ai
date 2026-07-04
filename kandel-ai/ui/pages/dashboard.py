"""
KANDEL AI - Dashboard Home
Designed by Kandel Sanjaya
"""
import streamlit as st
from ui.components.widgets import stat_card, progress_bar
from memory.memory_store import memory_stats, get_all_memory
from database.db import get_conn


def _counts(user_id: int):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chats WHERE user_id=?", (user_id,))
        chats = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM documents WHERE user_id=?", (user_id,))
        docs = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM images WHERE user_id=?", (user_id,))
        imgs = c.fetchone()[0]
    return chats, docs, imgs


def render_dashboard(user: dict):
    st.markdown(f"## Hello, {user['name']}! 👋")
    st.caption("How can I help you today?")

    chats, docs, imgs = _counts(user["id"])
    mem = memory_stats(user["id"])["total"]

    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("Total Chats", str(chats), "")
    with c2: stat_card("Documents", str(docs), "")
    with c3: stat_card("Images Generated", str(imgs), "")
    with c4: stat_card("Memory Items", str(mem), "")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    left, right = st.columns([2, 1])
    with left:
        st.markdown('<div class="kai-card">', unsafe_allow_html=True)
        st.markdown('<div class="kai-orb-hero" style="width:120px;height:120px;"></div>', unsafe_allow_html=True)
        st.markdown("#### Ask me anything")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.selectbox("Mode", ["Auto", "RAG (Documents)", "Web Search"], label_visibility="collapsed", key="dash_mode")
        with m2:
            st.selectbox("Model", ["Groq · llama-3.3-70b-versatile", "Groq · llama-3.1-8b-instant"], label_visibility="collapsed", key="dash_model")
        with m3:
            st.selectbox("Language", ["Auto Detect", "English", "Nepali", "Hindi"], label_visibility="collapsed", key="dash_lang")

        q = st.text_input("Quick ask", placeholder="Ask KANDEL AI anything...", label_visibility="collapsed", key="quick_ask")
        if st.button("Send to Chat", key="quick_ask_send"):
            if q.strip():
                st.session_state.pending_query = q
                st.session_state.page = "chat"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown("#### Quick Actions")
        qa1, qa2, qa3, qa4, qa5 = st.columns(5)
        actions = [
            ("Summarize PDF", "documents"), ("Generate Image", "image"),
            ("Write Code", "code"), ("Translate Text", "translate"), ("Analyze Data", "analytics"),
        ]
        for col, (label, target) in zip([qa1, qa2, qa3, qa4, qa5], actions):
            with col:
                if st.button(label, key=f"qa_{target}", use_container_width=True):
                    st.session_state.page = target
                    st.rerun()

    with right:
        st.markdown('<div class="kai-card">', unsafe_allow_html=True)
        st.markdown("#### Memory Status")
        pct = min(int((mem / max(mem + 50, 1)) * 100) + 40, 98)
        st.markdown(f"**{pct}%** — Good")
        progress_bar(pct)
        st.caption(f"{mem} memory items stored")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="kai-card">', unsafe_allow_html=True)
        st.markdown("#### Recent Chats")
        recent = get_all_memory(user["id"])[:4]
        if not recent:
            st.caption("No conversations yet — start chatting!")
        for r in recent:
            st.markdown(
                f"""<div style="padding:.3rem 0;border-bottom:1px solid var(--border);">
                <span style="font-size:.85rem;">{r['question'][:36]}{'...' if len(r['question'])>36 else ''}</span><br>
                <span class="kai-muted" style="font-size:.7rem;">{r['created_at']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="kai-card">', unsafe_allow_html=True)
        st.markdown("#### Model")
        st.write(f"`{user.get('model') or 'Groq · llama-3.3-70b-versatile'}`")
        st.markdown("</div>", unsafe_allow_html=True)
