import streamlit as st
from utils.icons import icon
from utils.helpers import ingest_document, rag_answer


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('documents', 20)} Documents (RAG)</div>",
                unsafe_allow_html=True)
    st.caption("Upload documents, then ask Lucy questions grounded in their content.")

    up = st.file_uploader("Upload a document", type=["txt", "md", "pdf"], accept_multiple_files=True)
    if up:
        for f in up:
            if f.name.endswith((".txt", ".md")):
                text = f.read().decode("utf-8", errors="ignore")
            else:
                try:
                    import pypdf
                    reader = pypdf.PdfReader(f)
                    text = "\n".join(page.extract_text() or "" for page in reader.pages)
                except Exception:
                    text = ""
                    st.warning(f"Couldn't parse {f.name} — install `pypdf` for PDF support.")
            if text:
                msg = ingest_document(f.name, text)
                st.success(msg)
                st.session_state.setdefault("documents", []).append(f.name)

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    st.markdown(f"<div class='sub-heading'>{icon('chat', 16)} Ask your documents</div>", unsafe_allow_html=True)
    q = st.text_input("Question", placeholder="e.g. What are the key findings in the report?")
    if st.button("Ask", type="primary") and q:
        with st.spinner("Searching your documents..."):
            answer, sources = rag_answer(q)
        st.markdown(f'<div class="chat-bubble-bot">{answer}</div>', unsafe_allow_html=True)
        if sources:
            st.markdown(f"<div class='chat-sources'>Sources: {', '.join(sources)}</div>", unsafe_allow_html=True)

    docs = st.session_state.get("documents", [])
    if docs:
        st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
        st.markdown(f"<div class='sub-heading'>{icon('documents', 16)} Indexed documents</div>", unsafe_allow_html=True)
        for d in docs:
            st.markdown(f"- {d}")
