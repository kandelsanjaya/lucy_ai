# 🧠 KANDEL AI — All-in-One RAG AI Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.38-ff4b4b?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LLM-Groq-orange" />
  <img src="https://img.shields.io/badge/VectorDB-ChromaDB-purple" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

<p align="center"><i>Designed by <b>Kandel Sanjaya</b></i></p>

---

## ✨ What is KANDEL AI?

KANDEL AI is a full-stack, animated, cyber-neon AI platform combining **RAG, long-term memory, web search, image generation, OCR, voice, code assistance, and translation** into a single Streamlit app — powered entirely by **Groq** for fast, low-latency LLM inference.

## 🧩 Core Features

| Feature | Description |
|---|---|
| 🔐 Auth | Case-sensitive email/password login, bcrypt hashing, JWT sessions |
| 💬 Chat | Streaming-style responses, neon glass bubbles, source citations, confidence score |
| 🧠 Memory | Every Q&A is stored in SQLite + embedded for semantic recall — persists across restarts |
| 📚 RAG | Upload PDFs/DOCX/CSV/XLSX/TXT → auto chunk → embed (ChromaDB) → hybrid semantic+BM25 retrieval |
| 🌐 Web Search | Automatic fallback via Tavily or DuckDuckGo when memory/RAG can't answer |
| 🎨 Image Generation | Free diffusion backend, prompt gallery, seed/aspect-ratio controls |
| 🔎 OCR | Extract text from images/scans, then summarize or translate it |
| 🎙️ Voice | In-browser mic recording + text-to-speech playback |
| 👨‍💻 Code Assistant | Generates and safely runs Python snippets in a sandboxed subprocess |
| 🌍 Multilingual | Auto-detects input language, replies in kind, translates on request |
| 🎨 10 Themes | 5 dark (Cyber Neon, Midnight, Synthwave, Matrix, Purple Glass) + 5 light (Light, Minimal White, Corporate, Ocean, Sunset) |

## 🧠 How the Supervisor Agent Answers

```
User query
   │
   ▼
1. Check long-term memory (semantic recall)  ──▶ found? answer + cite memory
   │ not found
   ▼
2. Search your uploaded documents (RAG)      ──▶ found? answer + cite documents
   │ not found
   ▼
3. Live web search (Tavily → DuckDuckGo)     ──▶ answer + cite sources
   │
   ▼
4. Write the new Q/A pair back into memory for next time
```

## 🛠️ Tech Stack

- **Frontend:** Streamlit + custom CSS (glassmorphism, neon glow, animated loaders)
- **LLM:** Groq (`llama-3.3-70b-versatile` with automatic fallback to `llama-3.1-8b-instant`, `gemma2-9b-it`, `mixtral-8x7b-32768` if a model is retired)
- **Vector DB:** ChromaDB (persistent, local)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Database:** SQLite (auth, chat history, memory, documents, images)
- **Web Search:** Tavily (optional) → DuckDuckGo (`ddgs`, no key required)
- **Image Gen:** Pollinations.ai (free, no key)
- **OCR:** Tesseract via `pytesseract`
- **Voice:** `streamlit-mic-recorder` + `gTTS`

## 📁 Project Structure

```
kandel-ai/
├── app.py                  # Entry point
├── .env.example
├── requirements.txt
├── config/settings.py      # Central config
├── core/supervisor.py      # Multi-agent routing logic
├── services/                # llm_provider, web_search, embeddings, image_gen, ocr
├── memory/memory_store.py  # Long-term memory (SQLite + semantic recall)
├── rag/                    # loaders, chunker, hybrid retriever
├── database/                # db schema, auth
├── ui/pages/                # login, dashboard, chat, documents, image_gen, code_assistant, settings, misc, tools_help
├── ui/components/            # sidebar, icons (real inline SVGs), widgets/loaders
├── ui/themes/                # theme tokens + CSS builder
├── vector_store/             # ChromaDB persistence (auto-created)
├── uploads/                  # uploaded files (auto-created)
└── logs/
```

## 🚀 Getting Started

```bash
git clone <your-repo-url> kandel-ai
cd kandel-ai
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then add your GROQ_API_KEY
streamlit run app.py
```

Get a free Groq API key at **https://console.groq.com**.

## 🔑 Environment Variables

See `.env.example` — at minimum you need `GROQ_API_KEY`. Everything else (Tavily, custom JWT secret) is optional and has a safe default/fallback.

## 🎨 Themes

Switch anytime from **Settings → Appearance**. Each theme swaps CSS variables instantly with a smooth cross-fade — no reload.

## 🔒 Security Notes

- Passwords are **case-sensitive** — `Password123` and `password123` are different accounts' worth of trouble; we never lowercase or normalize them.
- Passwords are hashed with bcrypt before storage — plaintext is never persisted.
- Sessions are signed JWTs with a configurable timeout.
- All personal data (chats, memory, documents, images) is stored locally per install — nothing is sent anywhere except to Groq (for inference) and your chosen search provider (for web search).

## 📜 Terms & Conditions

This software is provided **as-is**, without warranty of any kind. Kandel Sanjaya is not liable for any damages, data loss, or misuse arising from the use of this software. You are responsible for complying with the terms of service of any third-party API you connect (Groq, Tavily, Pollinations, etc.) and for securing your own `.env` file and API keys. This project is intended for personal, educational, and internal commercial use; redistribution must retain attribution to the original designer.

## 📄 License

MIT License — see [LICENSE](LICENSE).

---

<p align="center">Built with ❤️ using Streamlit, LangChain-style agent routing, Groq, and ChromaDB.<br><b>Designed by Kandel Sanjaya</b><br>© 2026 Kandel Sanjaya. All Rights Reserved.</p>
