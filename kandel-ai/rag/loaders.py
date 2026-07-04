"""
KANDEL AI - Document Loaders
Designed by Kandel Sanjaya

PDF parsing prefers LlamaParse (better table/layout-aware chunking) when
LLAMA_CLOUD_API_KEY is set in .env, and transparently falls back to pypdf
otherwise so the app still works with zero extra keys.
"""
import os
import pandas as pd
from pypdf import PdfReader
import docx

LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY", "")


def _parse_pdf_with_llamaparse(filepath: str) -> str:
    from llama_parse import LlamaParse
    parser = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown")
    documents = parser.load_data(filepath)
    return "\n\n".join(doc.text for doc in documents)


def _parse_pdf_with_pypdf(filepath: str) -> str:
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_text_from_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        if LLAMA_CLOUD_API_KEY:
            try:
                return _parse_pdf_with_llamaparse(filepath)
            except Exception:
                # LlamaParse failed (bad key, network, package missing) - fall back safely
                return _parse_pdf_with_pypdf(filepath)
        return _parse_pdf_with_pypdf(filepath)

    if ext == ".docx":
        d = docx.Document(filepath)
        return "\n".join(p.text for p in d.paragraphs)

    if ext in (".txt", ".md", ".html", ".json"):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    if ext == ".csv":
        df = pd.read_csv(filepath)
        return df.to_string()

    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(filepath)
        return df.to_string()

    raise ValueError(f"Unsupported file type: {ext}")


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c.strip() for c in chunks if c.strip()]
