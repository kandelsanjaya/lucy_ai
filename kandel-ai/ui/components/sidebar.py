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
        avatar_name = (user.get('name') or 'User').strip()
        initial = avatar_name[0].upper() if avatar_name else 'U'

        # ChatGPT-like avatar (always SVG; no external images needed)
        avatar_svg = f"""
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="g" x1="4" y1="2" x2="26" y2="28" gradientUnits="userSpaceOnUse">
              <stop stop-color="#60a5fa"/>
              <stop offset="1" stop-color="#a78bfa"/>
            </linearGradient>
          </defs>
          <circle cx="14" cy="14" r="13" fill="url(#g)"/>
          <circle cx="14" cy="14" r="13" fill="white" fill-opacity="0.10"/>
          <text x="14" y="18" text-anchor="middle" font-family="ui-sans-serif, system-ui" font-size="12" font-weight="800" fill="white">{initial}</text>
          <path d="M7 17c2.2-3.2 11.8-3.2 14 0" stroke="white" stroke-opacity="0.35" stroke-width="1.2" stroke-linecap="round"/>
        </svg>
        """

        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:.6rem;opacity:.9;padding:.35rem .2rem .2rem .2rem;">
              <div style="width:40px;height:40px;border-radius:14px;background:color-mix(in srgb, var(--surface) 60%, transparent);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;">
                {avatar_svg}
              </div>
              <div>
                <div style="font-weight:800;font-size:.95rem;line-height:1.1;">{user.get('name','User')}</div>
                <div class="kai-muted" style="font-size:.7rem;">{user.get('role','user').title()}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Logout", use_container_width=True, key="btn_logout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
