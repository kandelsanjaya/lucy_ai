"""
Lucy AI — Backend helpers
-------------------------
Thin wrappers around OpenAI, ChromaDB (RAG), pytesseract (OCR),
and small local "tools" (calculator, weather). Every function fails
soft: if a dependency or API key is missing, it returns a clear
message instead of crashing the UI.
"""

import os
import json
import time
import base64
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_store")
os.makedirs(DATA_DIR, exist_ok=True)


# --------------------------------------------------------------------------
# API key / client
# --------------------------------------------------------------------------
def get_api_key() -> str:
    return os.environ.get("OPENAI_API_KEY", "")


def get_openai_client():
    key = get_api_key()
    if not key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key)
    except Exception:
        return None


# --------------------------------------------------------------------------
# Memory (persisted locally as JSON — simple, dependency-free)
# --------------------------------------------------------------------------
def _load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"preferences": [], "notes": [], "chat_log": []}


def _save_memory(data: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_memory_item(category: str, text: str):
    mem = _load_memory()
    mem.setdefault(category, []).append(
        {"text": text, "ts": datetime.now().isoformat()}
    )
    _save_memory(mem)


def get_memory(category: str = None):
    mem = _load_memory()
    return mem if category is None else mem.get(category, [])


def memory_usage_stats():
    mem = _load_memory()
    total_items = sum(len(v) for v in mem.values() if isinstance(v, list))
    capacity = 1200
    pct = min(100, int((total_items / capacity) * 100)) if capacity else 0
    return {"used": total_items, "capacity": capacity, "pct": pct}


# --------------------------------------------------------------------------
# Chat completion (general assistant + code assistant share this)
# --------------------------------------------------------------------------
def chat_completion(messages, model="gpt-4o-mini", temperature=0.6):
    client = get_openai_client()
    if client is None:
        return ("⚠️ No `OPENAI_API_KEY` found in your environment. "
                "Add one to `.streamlit/secrets.toml` or as an env var "
                "to enable live responses. (This is a placeholder reply.)")
    try:
        resp = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error contacting the model: {e}"


# --------------------------------------------------------------------------
# RAG — document chat via ChromaDB + OpenAI embeddings
# --------------------------------------------------------------------------
def get_chroma_collection(name="lucy_docs"):
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        return client.get_or_create_collection(name)
    except Exception:
        return None


def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [c for c in chunks if c.strip()]


def embed_texts(texts):
    client = get_openai_client()
    if client is None:
        return None
    try:
        resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
        return [d.embedding for d in resp.data]
    except Exception:
        return None


def ingest_document(doc_id: str, text: str) -> str:
    collection = get_chroma_collection()
    if collection is None:
        return "⚠️ ChromaDB isn't available — install `chromadb` to enable RAG."
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    if embeddings is None:
        return "⚠️ No API key / embeddings unavailable — document stored without vector search."
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids,
                    metadatas=[{"source": doc_id} for _ in chunks])
    return f"✅ Ingested `{doc_id}` into memory as {len(chunks)} chunks."


def query_documents(question: str, n_results=4):
    collection = get_chroma_collection()
    if collection is None:
        return [], "ChromaDB unavailable."
    q_embed = embed_texts([question])
    if q_embed is None:
        return [], "Embeddings unavailable (no API key)."
    try:
        results = collection.query(query_embeddings=q_embed, n_results=n_results)
        docs = results.get("documents", [[]])[0]
        sources = [m.get("source", "unknown") for m in results.get("metadatas", [[]])[0]]
        return list(zip(docs, sources)), None
    except Exception as e:
        return [], str(e)


def rag_answer(question: str):
    chunks, err = query_documents(question)
    if err or not chunks:
        # Fall back to plain chat if no docs are indexed yet
        answer = chat_completion([
            {"role": "system", "content": "You are Lucy, a helpful RAG AI assistant."},
            {"role": "user", "content": question},
        ])
        return answer, []
    context = "\n\n".join(f"[{src}] {doc}" for doc, src in chunks)
    prompt = (f"Answer the question using the context below. Cite sources by name.\n\n"
              f"Context:\n{context}\n\nQuestion: {question}")
    answer = chat_completion([
        {"role": "system", "content": "You are Lucy, a RAG assistant. Be concise and cite sources."},
        {"role": "user", "content": prompt},
    ])
    sources = sorted(set(src for _, src in chunks))
    return answer, sources


# --------------------------------------------------------------------------
# Image generation
# --------------------------------------------------------------------------
def generate_image(prompt: str, size="1024x1024"):
    client = get_openai_client()
    if client is None:
        return None, "⚠️ No API key configured — can't generate images yet."
    try:
        resp = client.images.generate(model="dall-e-3", prompt=prompt, size=size, n=1)
        return resp.data[0].url, None
    except Exception as e:
        return None, f"⚠️ Image generation failed: {e}"


# --------------------------------------------------------------------------
# OCR
# --------------------------------------------------------------------------
def extract_text_from_image(image_path_or_file):
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path_or_file)
        text = pytesseract.image_to_string(img)
        return text.strip() or "(No text detected in image.)"
    except Exception as e:
        return f"⚠️ OCR failed ({e}). Ensure `tesseract-ocr` is installed on your system."


# --------------------------------------------------------------------------
# Simple tools: calculator + weather (Open-Meteo, no key required)
# --------------------------------------------------------------------------
def calculate(expression: str):
    import ast
    import operator as op
    ops = {
        ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
        ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg,
        ast.Mod: op.mod,
    }

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression")

    try:
        tree = ast.parse(expression, mode="eval").body
        return _eval(tree)
    except Exception as e:
        return f"Error: {e}"


def get_weather(city: str):
    try:
        import requests
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}, timeout=8
        ).json()
        if not geo.get("results"):
            return f"Couldn't find '{city}'."
        loc = geo["results"][0]
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": loc["latitude"], "longitude": loc["longitude"],
                    "current_weather": True}, timeout=8
        ).json()
        cw = weather.get("current_weather", {})
        return (f"**{loc['name']}, {loc.get('country', '')}** — "
                f"{cw.get('temperature', '?')}°C, wind {cw.get('windspeed', '?')} km/h")
    except Exception as e:
        return f"⚠️ Weather lookup failed: {e}"


# --------------------------------------------------------------------------
# Multi-language translate (LLM-backed, no external key beyond OpenAI)
# --------------------------------------------------------------------------
def translate_text(text: str, target_language: str):
    return chat_completion([
        {"role": "system", "content": f"Translate the user's text into {target_language}. Return only the translation."},
        {"role": "user", "content": text},
    ])
