"""
KANDEL AI - Sidebar Navigation
Designed by Kandel Sanjaya
"""
import streamlit as st
from ui.components.icons import icon

NAV_ITEMS = [
    ("dashboard", "dashboard", "Dashboard"),
    ("chat", "chat", "Chat"),
    ("documents", "documents", "Documents"),
    ("image", "image", "Image Generation"),
    ("code", "code", "Code Assistant"),
    ("search", "search", "Web Search"),
    ("ocr", "ocr", "OCR"),
    ("voice", "voice", "Voice Assistant"),
    ("translate", "translate", "Translation"),
    ("memory", "memory", "Memory"),
    ("analytics", "analytics", "Analytics"),
    ("tools", "tools", "Tools"),
    ("settings", "settings", "Settings"),
    ("help", "help", "Help & Support"),
]


def render_sidebar(user: dict):
    with st.sidebar:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:.5rem;padding:.5rem 0 1rem 0;">
                <div style="width:34px;height:34px;border-radius:10px;background:var(--gradient);"></div>
                <div>
                    <div style="font-weight:800;font-size:1.05rem;">KANDEL AI</div>
                    <div class="kai-muted" style="font-size:.65rem;">Designed by Kandel Sanjaya</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(f"➕  New Chat", use_container_width=True, key="btn_new_chat"):
            st.session_state.active_chat_messages = []
            st.session_state.page = "chat"
            st.rerun()

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        current_page = st.session_state.get("page", "dashboard")
        for page_key, icon_key, label in NAV_ITEMS:
            active = current_page == page_key
            cls = "kai-nav-item active" if active else "kai-nav-item"
            clicked = st.button(label, key=f"nav_{page_key}", use_container_width=True)
            if clicked:
                st.session_state.page = page_key
                st.rerun()

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="kai-nav-item" style="opacity:.85;">
                {icon('user', 18)} <span>{user.get('name','User')} · {user.get('role','user').title()}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Logout", use_container_width=True, key="btn_logout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
