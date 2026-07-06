import streamlit as st
from utils.icons import icon
from utils.helpers import chat_completion, add_memory_item


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('chat', 20)} Chat with Lucy</div>",
                unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm Lucy 👋 Ask me anything — I can search the web, "
                                              "read your documents, write code, or just chat."}
        ]

    chat_box = st.container(height=480, border=False)
    with chat_box:
        for m in st.session_state.messages:
            css = "chat-bubble-user" if m["role"] == "user" else "chat-bubble-bot"
            align = "text-align:right;" if m["role"] == "user" else ""
            st.markdown(f"<div style='{align}margin-bottom:10px;'><span class='{css}' "
                        f"style='display:inline-block;'>{m['content']}</span></div>",
                        unsafe_allow_html=True)

    prompt = st.chat_input("Type your message...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        history = [{"role": "system", "content": "You are Lucy, a warm, capable all-in-one AI agent."}]
        history += st.session_state.messages[-10:]
        with st.spinner("Lucy is typing..."):
            reply = chat_completion(history)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        add_memory_item("chat_log", prompt)
        st.rerun()

    cols = st.columns([1, 1, 5])
    if cols[0].button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()
