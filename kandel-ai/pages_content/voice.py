import streamlit as st
from utils.icons import icon
from utils.helpers import chat_completion


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('voice', 20)} Voice Assistant</div>",
                unsafe_allow_html=True)
    st.caption("Record or upload audio to talk to Lucy. Uses OpenAI Whisper for transcription "
               "and TTS for spoken replies. If no `OPENAI_API_KEY` is set, the app shows a placeholder reply.")


    audio = st.audio_input("Record your message") if hasattr(st, "audio_input") else \
        st.file_uploader("Upload audio (wav/mp3)", type=["wav", "mp3", "m4a"])

    if audio and st.button("🎙️ Transcribe & Ask Lucy", type="primary"):
        with st.spinner("Listening..."):
            transcript = _transcribe(audio)
        st.markdown(f"**You said:** {transcript}")
        if transcript.startswith("(No API key"):
            st.caption("Add `OPENAI_API_KEY` to enable transcription and spoken replies.")
        else:
            with st.spinner("Lucy is responding..."):
                reply = chat_completion([
                    {"role": "system", "content": "You are Lucy, speaking to the user out loud — keep replies natural and brief."},
                    {"role": "user", "content": transcript},
                ])
            st.markdown(f'<div class="chat-bubble-bot">{reply}</div>', unsafe_allow_html=True)
            audio_bytes = _speak(reply)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.caption("(No TTS audio: missing `OPENAI_API_KEY` or TTS failed.)")




def _transcribe(audio_file):
    from utils.helpers import get_openai_client
    client = get_openai_client()
    if client is None:
        return "(No API key — can't transcribe. This is placeholder text.)"
    try:
        audio_file.seek(0)
        resp = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        return resp.text
    except Exception as e:
        return f"⚠️ Transcription failed: {e}"


def _speak(text: str):
    from utils.helpers import get_openai_client
    client = get_openai_client()
    if client is None:
        return None
    try:
        resp = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
        return resp.read()
    except Exception:
        return None
