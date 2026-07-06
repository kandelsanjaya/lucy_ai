"""
Lucy AI Agent — All-in-One RAG AI Platform
===========================================
Main Streamlit entry point.

Run with:
    streamlit run app.py

Author layout inspired by the "Lucy AI Agent" product mockup:
RAG + Web Search + Memory + Multi-language + Image Gen + OCR + Voice + Code + More.
"""

import os
import time
import streamlit as st
from utils.icons import icon
from utils.loader import SPLASH_HTML

from pages_content import (
    dashboard, chat, documents, image_gen, code_assistant,
    web_search, ocr, voice, memory, tools, settings, profile, help as help_page,
)

st.set_page_config(
    page_title="Lucy AI Agent — All-in-One RAG AI Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------------------------------
# Bridge st.secrets -> os.environ so utils/helpers.py (os.environ based)
# picks up keys whether they come from secrets.toml or real env vars.
# --------------------------------------------------------------------------
for _key in ("OPENAI_API_KEY", "TAVILY_API_KEY"):
    try:
        if _key in st.secrets and st.secrets[_key]:
            os.environ.setdefault(_key, st.secrets[_key])
    except Exception:
        pass


# --------------------------------------------------------------------------
# Load theme CSS
# --------------------------------------------------------------------------
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles", "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# --------------------------------------------------------------------------
# Session state defaults
# --------------------------------------------------------------------------
DEFAULTS = {
    "logged_in": False,
    "splash_shown": False,
    "page": "dashboard",
    "user": {"name": "Kandel Sanjaya", "email": "kandelsanjaya7@example.com", "plan": "Pro Plan"},
}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# (key, label, svg-icon-name, emoji-for-button)
NAV_ITEMS = [
    ("dashboard", "Dashboard", "dashboard", "📊"),
    ("chat", "Chat", "chat", "💬"),
    ("documents", "Documents", "documents", "📄"),
    ("image_gen", "Image Generation", "image", "🎨"),
    ("code_assistant", "Code Assistant", "code", "💻"),
    ("web_search", "Web Search", "websearch", "🔍"),
    ("ocr", "OCR", "ocr", "🔠"),
    ("voice", "Voice Assistant", "voice", "🎙️"),
    ("memory", "Memory", "memory", "🧠"),
    ("tools", "Tools", "tools", "🛠️"),
    ("profile", "Profile", "user", "👤"),
    ("settings", "Settings", "settings", "⚙️"),
    ("help", "Help & Support", "help", "❓"),
]

PAGE_MODULES = {
    "dashboard": dashboard, "chat": chat, "documents": documents,
    "image_gen": image_gen, "code_assistant": code_assistant, "web_search": web_search,
    "ocr": ocr, "voice": voice, "memory": memory, "tools": tools,
    "profile": profile, "settings": settings, "help": help_page,
}


# --------------------------------------------------------------------------
# Splash screen — shown once per session, using the electron loader
# --------------------------------------------------------------------------
def render_splash():
    placeholder = st.empty()
    placeholder.markdown(SPLASH_HTML, unsafe_allow_html=True)
    time.sleep(1.1)
    placeholder.empty()
    st.session_state.splash_shown = True


# --------------------------------------------------------------------------
# Login screen
# --------------------------------------------------------------------------
def render_login():
    st.markdown('<div class="login-wrap glass-card">', unsafe_allow_html=True)
    st.markdown(f"""<div style="text-align:center;margin-bottom:10px;">
        <div style="width:64px;height:64px;margin:0 auto 12px;">{icon('logo', 64)}</div>
        <div class="login-title">Welcome Back</div>
        <div class="login-sub">Sign in to continue to Lucy AI</div>
    </div>""", unsafe_allow_html=True)

    email = st.text_input("Email", value="kandel.sanjaya@example.com")
    password = st.text_input("Password", type="password", value="••••••••••••")
    c1, c2 = st.columns(2)
    c1.checkbox("Remember me")
    c2.markdown("<div style='text-align:right;padding-top:6px;'><a href='#' "
                "style='color:#a78bfa;font-size:0.85rem;'>Forgot password?</a></div>", unsafe_allow_html=True)

    if st.button("Sign In", type="primary", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.user["email"] = email or st.session_state.user["email"]
        st.rerun()

    st.markdown("<div style='text-align:center;color:var(--text-3);margin:14px 0;font-size:0.82rem;'>"
                "Or continue with</div>", unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    g1.button("Google", use_container_width=True)
    g2.button("GitHub", use_container_width=True)
    g3.button("Microsoft", use_container_width=True)

    st.markdown("<div class='lucy-footer'>Designed by <span class='credit'>Kandel Sanjaya</span> ✨</div>",
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""<div class="lucy-brand">{icon('logo', 30)} Lucy AI</div>""", unsafe_allow_html=True)

        for key, label, icon_name, emoji in NAV_ITEMS:
            active = st.session_state.page == key
            wrapper_class = "nav-active" if active else ""
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            if st.button(f"{label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
        user = st.session_state.user
        st.markdown(
            f"""<div class="flex-between" style="padding:6px 4px;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <div style="width:34px;height:34px;border-radius:50%;background:var(--grad-primary);
                             display:flex;align-items:center;justify-content:center;color:white;font-weight:700;">
                             {user['name'][0]}
                        </div>
                        <div>
                            <div style="font-size:0.85rem;font-weight:700;">{user['name']}</div>
                            <div class="small muted">{user['plan']}</div>
                        </div>
                    </div>
                </div>""",
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------
# Top bar
# --------------------------------------------------------------------------
def render_topbar():
    label = dict((k, l) for k, l, _, _ in NAV_ITEMS)[st.session_state.page]
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"<div style='font-size:1.05rem;font-weight:700;color:var(--text-2);'>{label}</div>",
                    unsafe_allow_html=True)
    with c2:
        b1, b2, b3 = st.columns(3)
        if b1.button("＋ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.page = "chat"
            st.rerun()
        b2.markdown(f"<div style='text-align:center;padding-top:6px;'>{icon('bell', 20, '#a9a9bc')}</div>",
                    unsafe_allow_html=True)
        b3.markdown(f"<div style='text-align:center;padding-top:6px;'>{icon('settings', 20, '#a9a9bc')}</div>",
                    unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Main router
# --------------------------------------------------------------------------
if not st.session_state.logged_in:
    render_login()
else:
    render_sidebar()
    render_topbar()
    st.write("")
    PAGE_MODULES[st.session_state.page].render(st.session_state.user)