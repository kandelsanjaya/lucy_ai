"""
KANDEL AI - Tools & Help Pages
Designed by Kandel Sanjaya
"""
import streamlit as st
from config.settings import settings


def render_tools(user: dict):
    st.markdown("### Tools")
    tools = [
        ("Calculator", "Basic arithmetic and unit conversions."),
        ("Weather", "Check current weather (wire to a weather API of your choice)."),
        ("Currency Converter", "Convert between currencies."),
        ("Word/Character Counter", "Quick text statistics."),
    ]
    cols = st.columns(2)
    for i, (name, desc) in enumerate(tools):
        with cols[i % 2]:
            st.markdown(f'<div class="kai-card"><b>{name}</b><p class="kai-muted">{desc}</p></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("#### Word / Character Counter")
    text = st.text_area("Paste text")
    if text:
        st.write(f"Words: **{len(text.split())}** · Characters: **{len(text)}**")


def render_help(user: dict):
    st.markdown("### Help & Support")
    st.markdown(
        f"""
        <div class="kai-card">
        <p><b>KANDEL AI</b> — {settings.TAGLINE}</p>
        <p>Designed by <b>{settings.DESIGNER}</b></p>
        <p class="kai-muted">{settings.COPYRIGHT}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("How does memory work?"):
        st.write("Every question and answer is saved to your personal SQLite database and embedded for semantic recall. On your next visit, KANDEL AI checks memory first, then your documents (RAG), then the live web, before answering.")
    with st.expander("Which LLM does this use?"):
        st.write("KANDEL AI runs entirely on Groq-hosted open models (Llama 3.3, Llama 3.1, Gemma2, Mixtral) for fast inference. You can switch models in Settings → Model & LLM.")
    with st.expander("Is my data private?"):
        st.write("All your chats, documents, and memory are stored locally in your own SQLite + ChromaDB files. Nothing is shared between users.")
