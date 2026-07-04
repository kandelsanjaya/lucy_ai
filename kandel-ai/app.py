"""
KANDEL AI — All-in-One RAG AI Platform
Designed by Kandel Sanjaya
Entry point: streamlit run app.py
"""
import streamlit as st
from config.settings import settings
from database.db import init_db
from ui.themes.css_builder import build_css
from ui.themes.tokens import DEFAULT_THEME
from ui.components.sidebar import render_sidebar
from ui.pages.login import render_login
from ui.pages.dashboard import render_dashboard
from ui.pages.chat import render_chat
from ui.pages.documents import render_documents
from ui.pages.image_gen import render_image_gen
from ui.pages.code_assistant import render_code_assistant
from ui.pages.settings import render_settings
from ui.pages.misc_pages import (
    render_ocr, render_translation, render_voice,
    render_web_search, render_memory, render_analytics,
)
from ui.pages.tools_help import render_tools, render_help

st.set_page_config(
    page_title="KANDEL AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

active_theme = DEFAULT_THEME
if st.session_state.get("user"):
    active_theme = st.session_state.user.get("theme") or DEFAULT_THEME

st.markdown(build_css(active_theme), unsafe_allow_html=True)

if not st.session_state.authenticated:
    render_login()
    st.stop()

user = st.session_state.user
render_sidebar(user)

page = st.session_state.get("page", "dashboard")

PAGES = {
    "dashboard": render_dashboard,
    "chat": render_chat,
    "documents": render_documents,
    "image": render_image_gen,
    "code": render_code_assistant,
    "search": render_web_search,
    "ocr": render_ocr,
    "voice": render_voice,
    "translate": render_translation,
    "memory": render_memory,
    "analytics": render_analytics,
    "tools": render_tools,
    "settings": render_settings,
    "help": render_help,
}

render_fn = PAGES.get(page, render_dashboard)
render_fn(user)

st.markdown(
    f"""<div class="kai-muted" style="text-align:center;margin-top:3rem;font-size:.75rem;">
    {settings.COPYRIGHT} · Designed by {settings.DESIGNER}
    </div>""",
    unsafe_allow_html=True,
)
