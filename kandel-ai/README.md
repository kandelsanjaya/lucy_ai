# ✨ Lucy AI Agent — All-in-One RAG AI Platform

A Streamlit-based AI agent dashboard: **RAG + Web Search + Memory + Multi-language +
Image Generation + OCR + Voice + Code Assistant + Tools** — all in one clean,
Gemini-inspired dark UI.

![status](https://img.shields.io/badge/status-active-brightgreen) ![python](https://img.shields.io/badge/python-3.10+-blue) ![streamlit](https://img.shields.io/badge/streamlit-1.38+-red)

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Chat** | General-purpose conversation with Lucy |
| 📄 **Documents (RAG)** | Upload `.txt` / `.md` / `.pdf` files, ask grounded questions with ChromaDB + OpenAI embeddings |
| 🎨 **Image Generation** | Text-to-image via DALL·E 3 |
| 🧠 **Code Assistant** | Explain, fix, or run Python code in-browser; ask about JS/Java/C++/Go/Rust |
| 🔍 **Web Search** | Summarized, cited web results (plug in Tavily/SerpAPI/Bing) |
| 🖼️ **OCR** | Extract text from images via Tesseract |
| 🎙️ **Voice Assistant** | Speech-to-text (Whisper) + text-to-speech (OpenAI TTS) |
| 🧩 **Memory** | Persistent local memory of preferences, notes, and chat history |
| 🛠️ **Tools** | Calculator, live weather (Open-Meteo, no key needed), translator, and more |
| ⚙️ **Settings** | Model/language switch, theme gallery, API key info |

Every page is real, working Python — not just static mockup. Anything that needs
an API key will **fail soft** with a clear message instead of crashing, so the UI
is fully explorable even with zero keys configured.

---

## 📁 Project Structure

```
lucy_ai/
├── app.py                     # Main entry point — login, sidebar, router
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml            # Theme (dark, purple/blue accents)
│   └── secrets.toml.example   # Copy to secrets.toml and fill in keys
├── styles/
│   └── style.css              # Full custom Gemini-style dark theme
├── utils/
│   ├── icons.py                # Hand-authored SVG icon library (source of truth)
│   └── helpers.py              # LLM calls, RAG, OCR, memory, tools
├── pages_content/
│   ├── dashboard.py            # Home dashboard (stats, hero orb, feature grid)
│   ├── chat.py
│   ├── documents.py             # RAG
│   ├── image_gen.py
│   ├── code_assistant.py
│   ├── web_search.py
│   ├── ocr.py
│   ├── voice.py
│   ├── memory.py
│   ├── tools.py
│   ├── settings.py
│   └── help.py
├── assets/
│   └── icons/                  # Every icon also exported as standalone .svg
├── data/                       # Local memory.json + ChromaDB store (gitignored)
└── uploads/                    # Scratch space for uploaded documents/images
```

---

## 🚀 Quick Start

```bash
# 1. Clone / unzip the project, then enter it
cd lucy_ai

# 2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste your OpenAI key
#   OPENAI_API_KEY = "sk-..."
#   TAVILY_API_KEY = ""   # optional, for live web search

# 5. (Optional, for OCR) Install the Tesseract system binary
#   Ubuntu/Debian: sudo apt install tesseract-ocr
#   macOS:         brew install tesseract
#   Windows:       https://github.com/UB-Mannheim/tesseract/wiki

# 6. Run it
streamlit run app.py
```

The app opens at `http://localhost:8501`. Sign in with any email/password
(this demo login is UI-only — wire up real auth for production).

---

## 🔑 Environment Variables

You can set keys either in `.streamlit/secrets.toml` **or** as real environment
variables — `app.py` bridges both into `os.environ` automatically.

| Variable | Required for | Notes |
|---|---|---|
| `OPENAI_API_KEY` | Chat, RAG embeddings, image generation, code assistant, voice | Get one at platform.openai.com |
| `TAVILY_API_KEY` | Live web search results | Optional — falls back to a placeholder without it |

---

## 🎨 Design System

The UI is built to feel like a **Gemini-style dashboard**: a soft dark background
with subtle radial gradients, glassmorphism cards (`.glass-card`), a purple → blue
→ cyan gradient accent (`--grad-primary`), and a calm, minimal sidebar. All colors
and spacing live in `styles/style.css` as CSS variables — change the `:root` block
to re-theme the whole app in one place.

All icons are hand-authored SVGs (no external icon font/CDN dependency) — see
`utils/icons.py` for the source, and `assets/icons/*.svg` for standalone files
you can drop into Figma, other apps, or edit directly.

---

## 🧩 Extending Lucy

- **Swap the LLM provider** — edit `chat_completion()` in `utils/helpers.py`.
- **Add a real search API** — set `TAVILY_API_KEY`, or edit `_mock_or_real_search()`
  in `pages_content/web_search.py` to call SerpAPI/Bing/etc.
- **Persist memory to a real database** — replace the JSON read/write in
  `utils/helpers.py` with Postgres/Redis/etc.
- **Add authentication** — replace the demo login in `app.py` with
  `streamlit-authenticator`, Auth0, or your own backend.

---

## 📜 License

MIT — do whatever you like, credit appreciated.

---

Designed by **Kandel Sanjaya** ✨ · Built with Streamlit, Python, LangChain, ChromaDB, OpenAI, and more ❤️
