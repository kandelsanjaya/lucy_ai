"""
KANDEL AI - Global Configuration
Designed by Kandel Sanjaya
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Brand
    APP_NAME = "Lucy AI"
    TAGLINE = "Family-friendly All-in-One RAG AI Assistant"
    DESIGNER = "Kandel Sanjaya"
    COPYRIGHT = "© 2026 Kandel Sanjaya. All Rights Reserved."

    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Fallback list in case the configured model is deprecated/unavailable
    GROQ_MODEL_FALLBACKS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
        "mixtral-8x7b-32768",
    ]

    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

    JWT_SECRET = os.getenv("JWT_SECRET", "insecure_dev_secret_change_me")
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))

    DATABASE_PATH = os.getenv("DATABASE_PATH", "database/kandel_ai.db")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    IMAGE_GEN_PROVIDER = os.getenv("IMAGE_GEN_PROVIDER", "pollinations")

    UPLOAD_DIR = "uploads"
    LOG_DIR = "logs"

settings = Settings()
