"""
KANDEL AI - Code Assistant Page
Designed by Kandel Sanjaya
"""
import streamlit as st
import subprocess
import tempfile
import os
from services.llm_provider import chat_completion
from ui.components.widgets import electron_loader


def render_code_assistant(user: dict):
    st.markdown("### Code Assistant")
    st.caption("Ask for code, get an explanation, or run Python snippets safely in a sandboxed subprocess.")

    lang = st.selectbox("Language", ["python", "javascript", "java", "c", "cpp", "sql", "bash"])
    prompt = st.text_area("Describe what you want the code to do", height=100)

    if st.button("Generate Code"):
        if prompt.strip():
            electron_loader("Writing code...")
            messages = [
                {"role": "system", "content": f"You are an expert {lang} developer. Return clean, correct, well-commented {lang} code for the request. Wrap code in a single fenced code block."},
                {"role": "user", "content": prompt},
            ]
            answer, model = chat_completion(messages, temperature=0.3)
            st.session_state.generated_code = answer
            st.session_state.code_model = model

    if st.session_state.get("generated_code"):
        st.markdown(st.session_state.generated_code)
        st.caption(f"Model: {st.session_state.get('code_model')}")

        if lang == "python":
            code_editor = st.text_area("Edit & run", value=_extract_code(st.session_state.generated_code), height=250)
            if st.button("Run Code"):
                output = _run_python(code_editor)
                st.code(output, language="text")


def _extract_code(markdown_text: str) -> str:
    if "```" in markdown_text:
        parts = markdown_text.split("```")
        for p in parts:
            cleaned = p.strip()
            if cleaned and not cleaned.lower().startswith(("python", "javascript", "java", "sql", "bash", "c\n", "cpp")):
                return cleaned
            if cleaned.startswith("python"):
                return cleaned[len("python"):].strip()
    return markdown_text


def _run_python(code: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            path = f.name
        result = subprocess.run(
            ["python3", path], capture_output=True, text=True, timeout=8
        )
        os.unlink(path)
        return result.stdout + ("\n" + result.stderr if result.stderr else "")
    except Exception as e:
        return f"Execution error: {e}"
