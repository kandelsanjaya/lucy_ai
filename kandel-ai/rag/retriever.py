"""
KANDEL AI - RAG Retriever (ChromaDB hybrid semantic + keyword search)
Designed by Kandel Sanjaya
"""
import chromadb
from rank_bm25 import BM25Okapi
from config.settings import settings
from services.embeddings import embed

_chroma_client = None


def get_chroma():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=settings.VECTOR_STORE_PATH)
    return _chroma_client


def get_collection(user_id: int):
    client = get_chroma()
    return client.get_or_create_collection(name=f"user_{user_id}_docs")


def add_document(user_id: int, filename: str, chunks: list):
    collection = get_collection(user_id)
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    embeddings = embed(chunks)
    metadatas = [{"source": filename, "chunk": i} for i in range(len(chunks))]
    collection.add(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)


def hybrid_search(user_id: int, query: str, top_k: int = 5):
    collection = get_collection(user_id)
    count = collection.count()
    if count == 0:
        return []

    q_emb = embed(query)
    semantic = collection.query(query_embeddings=q_emb, n_results=min(top_k * 2, count))

    docs = semantic.get("documents", [[]])[0]
    metas = semantic.get("metadatas", [[]])[0]
    dists = semantic.get("distances", [[]])[0]

    if not docs:
        return []

    # BM25 rerank over the semantically retrieved candidates
    tokenized = [d.lower().split() for d in docs]
    bm25 = BM25Okapi(tokenized)
    bm25_scores = bm25.get_scores(query.lower().split())

    ranked = sorted(
        zip(docs, metas, dists, bm25_scores),
        key=lambda x: (x[3] - x[2]),
        reverse=True,
    )

    return [
        {"text": d, "source": m.get("source", "unknown"), "score": float(score)}
        for d, m, dist, score in ranked[:top_k]
    ]
