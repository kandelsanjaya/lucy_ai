import streamlit as st
import io
import contextlib
from utils.icons import icon
from utils.helpers import chat_completion


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('code', 20)} Code Assistant</div>",
                unsafe_allow_html=True)

    lang = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "Go", "Rust"])
    default_code = 'def fibonacci(n):\n    a, b = 0, 1\n    while a < n:\n        print(a, end=" ")\n        a, b = b, a + b\n\nfibonacci(100)'
    code = st.text_area("Code", value=st.session_state.get("code_editor", default_code), height=220, key="code_editor")

    c1, c2 = st.columns(2)
    ask = c1.text_input("Ask Lucy about this code (explain / fix / optimize)", key="code_ask")
    run_it = c2.button("▶ Run Code", type="primary", use_container_width=True, disabled=(lang != "Python"))

    if c1.button("💬 Ask Lucy") and ask:
        with st.spinner("Thinking through your code..."):
            reply = chat_completion([
                {"role": "system", "content": f"You are an expert {lang} engineer. Be concise and precise."},
                {"role": "user", "content": f"Code:\n```{lang.lower()}\n{code}\n```\n\nRequest: {ask}"},
            ])
        st.markdown(f'<div class="chat-bubble-bot">{reply}</div>', unsafe_allow_html=True)

    if run_it:
        st.markdown(f"<div class='sub-heading'>{icon('arrow-right', 16)} Output</div>", unsafe_allow_html=True)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(code, {"__name__": "__main__"})
            st.code(buf.getvalue() or "(no output)", language="text")
        except Exception as e:
            st.code(f"{buf.getvalue()}\nError: {e}", language="text")

    if lang != "Python":
        st.caption("⚠️ In-browser execution is only available for Python in this demo. "
                   "Use 'Ask Lucy' to get explanations or generated code for other languages.")
