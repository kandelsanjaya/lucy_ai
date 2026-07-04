"""
KANDEL AI - Documents / RAG Page
Designed by Kandel Sanjaya
"""
import streamlit as st
import os
from config.settings import settings
from rag.loaders import load_text_from_file, chunk_text
from rag.retriever import add_document
from database.db import get_conn


def _record_document(user_id, filename, n_chunks):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO documents (user_id, filename, chunks) VALUES (?, ?, ?)",
            (user_id, filename, n_chunks),
        )


def _list_documents(user_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM documents WHERE user_id=? ORDER BY created_at DESC", (user_id,))
        return [dict(r) for r in c.fetchall()]


def render_documents(user: dict):
    st.markdown("### Knowledge Base — Documents")
    st.caption("Upload PDFs, DOCX, TXT, CSV, or Excel files. They'll be chunked, embedded, and used automatically in chat via RAG.")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    files = st.file_uploader(
        "Drag & drop files here",
        type=["pdf", "docx", "txt", "csv", "xlsx", "md", "json", "html"],
        accept_multiple_files=True,
    )

    if files:
        for f in files:
            path = os.path.join(settings.UPLOAD_DIR, f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            with st.spinner(f"Processing {f.name}..."):
                try:
                    text = load_text_from_file(path)
                    chunks = chunk_text(text)
                    add_document(user["id"], f.name, chunks)
                    _record_document(user["id"], f.name, len(chunks))
                    st.success(f"{f.name} — {len(chunks)} chunks indexed.")
                except Exception as e:
                    st.error(f"Failed to process {f.name}: {e}")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("#### Your Knowledge Base")
    docs = _list_documents(user["id"])
    if not docs:
        st.info("No documents uploaded yet.")
    for d in docs:
        st.markdown(
            f"""<div class="kai-card" style="margin-bottom:.5rem;">
            <b>{d['filename']}</b><br><span class="kai-muted">{d['chunks']} chunks · added {d['created_at']}</span>
            </div>""",
            unsafe_allow_html=True,
        )
