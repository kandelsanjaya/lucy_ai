import streamlit as st
from utils.icons import icon

FAQS = [
    ("How do I add my OpenAI API key?", "Add `OPENAI_API_KEY = \"sk-...\"` to `.streamlit/secrets.toml`, "
     "or export it as an environment variable before running `streamlit run app.py`."),
    ("Why isn't OCR working?", "OCR needs the `tesseract-ocr` binary installed on your system, "
     "in addition to the `pytesseract` Python package."),
    ("How do I enable real web search?", "Set a `TAVILY_API_KEY` environment variable — "
     "Lucy will automatically use it in the Web Search tool."),
    ("Where is my data stored?", "Chat memory and notes are stored locally in `data/memory.json`. "
     "Document embeddings are stored locally via ChromaDB in `data/chroma_store/`."),
]


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('help', 20)} Help & Support</div>",
                unsafe_allow_html=True)

    for q, a in FAQS:
        with st.expander(q):
            st.write(a)

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    st.markdown(f"<div class='sub-heading'>{icon('mail', 16)} Contact</div>", unsafe_allow_html=True)
    st.text_input("Your message", key="help_msg", placeholder="Describe your issue or feedback...")
    if st.button("Send", type="primary"):
        st.success("Thanks! This demo doesn't send real messages — wire this up to email/Slack in production.")
