"""
KANDEL AI - Embedding Service
Designed by Kandel Sanjaya
"""
from sentence_transformers import SentenceTransformer
from config.settings import settings

_model = None


def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed(texts):
    if isinstance(texts, str):
        texts = [texts]
    model = get_embedder()
    return model.encode(texts, normalize_embeddings=True).tolist()
