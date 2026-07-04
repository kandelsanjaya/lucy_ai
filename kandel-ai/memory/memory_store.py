"""
KANDEL AI - Long-Term Memory
Designed by Kandel Sanjaya

Every Q/A pair is written to SQLite (survives restarts) plus embedded so it
can be semantically recalled later, even if worded differently.
"""
import json
from database.db import get_conn
from services.embeddings import embed
import numpy as np


def save_memory(user_id: int, question: str, answer: str, topic: str = "", summary: str = "", keywords=None):
    keywords = keywords or []
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO memory (user_id, question, answer, topic, summary, keywords) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, question, answer, topic, summary, json.dumps(keywords)),
        )


def get_all_memory(user_id: int):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM memory WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        return [dict(r) for r in c.fetchall()]


def recall_relevant_memory(user_id: int, query: str, top_k: int = 3, threshold: float = 0.55):
    """Semantic recall over past Q/A pairs. Returns [] if nothing similar enough exists."""
    records = get_all_memory(user_id)
    if not records:
        return []

    corpus = [r["question"] + " " + (r.get("summary") or "") for r in records]
    try:
        query_vec = np.array(embed(query)[0])
        corpus_vecs = np.array(embed(corpus))
        sims = corpus_vecs @ query_vec  # cosine sim since embeddings are normalized
        ranked = sorted(zip(sims, records), key=lambda x: x[0], reverse=True)
        return [r for s, r in ranked[:top_k] if s >= threshold]
    except Exception:
        return []


def memory_stats(user_id: int):
    records = get_all_memory(user_id)
    return {"total": len(records)}
