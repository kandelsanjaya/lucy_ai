"""
KANDEL AI - OCR, Translation, Voice, Web Search, Memory, Analytics pages
Designed by Kandel Sanjaya
"""
import streamlit as st
import os
from config.settings import settings
from services.ocr import extract_text_from_image
from services.llm_provider import chat_completion
from services.web_search import web_search
from memory.memory_store import get_all_memory
from database.db import get_conn
from ui.components.widgets import electron_loader, stat_card, progress_bar


def render_ocr(user: dict):
    st.markdown("### OCR — Extract Text")
    st.caption("Upload an image, scanned PDF page, or screenshot to extract editable text.")
    file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if file:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        path = os.path.join(settings.UPLOAD_DIR, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        st.image(path, caption=file.name, width=350)
        try:
            text = extract_text_from_image(path)
        except Exception as e:
            text = f"(OCR engine not available in this environment: {e})"
        st.markdown("#### Extracted Text")
        edited = st.text_area("Editable output", value=text, height=200)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Copy Text"):
                st.toast("Text ready to copy from the box above.")
        with c2:
            if st.button("Summarize"):
                electron_loader("Summarizing...")
                answer, _ = chat_completion([{"role": "user", "content": f"Summarize this text:\n{edited}"}])
                st.info(answer)
        with c3:
            if st.button("Translate to English"):
                electron_loader("Translating...")
                answer, _ = chat_completion([{"role": "user", "content": f"Translate this to English:\n{edited}"}])
                st.info(answer)


def render_translation(user: dict):
    st.markdown("### Translation")
    st.caption("100+ languages supported — auto-detects the source language.")
    text = st.text_area("Text to translate", height=120)
    target = st.selectbox("Target language", ["English", "Nepali", "Hindi", "Spanish", "French", "German", "Chinese", "Japanese", "Arabic", "Russian"])
    if st.button("Translate"):
        if text.strip():
            electron_loader("Translating...")
            answer, model = chat_completion([
                {"role": "system", "content": f"Translate the user's text into {target}. Return only the translation."},
                {"role": "user", "content": text},
            ])
            st.markdown(f'<div class="kai-card">{answer}</div>', unsafe_allow_html=True)


def render_voice(user: dict):
    st.markdown("### Voice Assistant")
    st.caption("Record your voice, get a transcript, and hear KANDEL AI's reply spoken back.")
    st.info("Voice capture requires microphone permissions in your browser. Use the recorder below.")
    try:
        from streamlit_mic_recorder import mic_recorder
        audio = mic_recorder(start_prompt="🎙️ Start recording", stop_prompt="⏹ Stop", key="mic")
        if audio:
            st.audio(audio["bytes"])
            st.warning("Speech-to-text transcription requires a configured STT backend (e.g. Groq Whisper). Wire your STT service into services/tts_stt.py.")
    except Exception:
        st.warning("Install `streamlit-mic-recorder` to enable in-browser voice capture.")

    st.markdown("#### Text to Speech")
    tts_text = st.text_area("Text to read aloud")
    if st.button("Speak"):
        try:
            from gtts import gTTS
            import io
            tts = gTTS(text=tts_text)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            st.audio(buf.getvalue())
        except Exception as e:
            st.error(f"TTS failed: {e}")


def render_web_search(user: dict):
    st.markdown("### Web Search")
    q = st.text_input("Search the web")
    if st.button("Search") and q.strip():
        electron_loader("Searching the web...")
        results = web_search(q)
        for r in results:
            st.markdown(
                f"""<div class="kai-card" style="margin-bottom:.6rem;">
                <a href="{r['url']}" target="_blank"><b>{r['title']}</b></a>
                <p class="kai-muted">{r['snippet']}</p>
                </div>""",
                unsafe_allow_html=True,
            )


def render_memory(user: dict):
    st.markdown("### Long-Term Memory")
    st.caption("Everything KANDEL AI remembers from your conversations, stored permanently in your database.")
    records = get_all_memory(user["id"])
    stat_card("Total Memory Items", str(len(records)))
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    for r in records[:50]:
        st.markdown(
            f"""<div class="kai-card" style="margin-bottom:.5rem;">
            <b>Q:</b> {r['question']}<br>
            <b>A:</b> {r['answer'][:200]}{'...' if len(r['answer'])>200 else ''}
            <div class="kai-muted" style="font-size:.7rem;margin-top:.3rem;">{r['topic']} · {r['created_at']}</div>
            </div>""",
            unsafe_allow_html=True,
        )


def render_analytics(user: dict):
    st.markdown("### Analytics")
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM messages m JOIN chats ch ON m.chat_id=ch.id WHERE ch.user_id=?", (user["id"],))
        msg_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM documents WHERE user_id=?", (user["id"],))
        doc_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM images WHERE user_id=?", (user["id"],))
        img_count = c.fetchone()[0]

    c1, c2, c3 = st.columns(3)
    with c1: stat_card("Messages", str(msg_count))
    with c2: stat_card("Documents", str(doc_count))
    with c3: stat_card("Images", str(img_count))

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("#### Storage Usage")
    progress_bar(min(int((doc_count + img_count) * 3), 100))
