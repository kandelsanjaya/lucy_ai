import streamlit as st
from utils.icons import icon
from utils.helpers import calculate, get_weather, translate_text

MORE_TOOLS = [
    ("documents", "PDF Summarizer"),
    ("voice", "Text to Speech"),
    ("voice", "Speech to Text"),
    ("globe", "Translate"),
    ("calculator", "Calculator"),
    ("weather", "Weather"),
    ("dashboard", "News"),
    ("image", "YouTube Summarizer"),
    ("documents", "File Analyzer"),
    ("plus", "And More..."),
]


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('tools', 20)} Tools</div>",
                unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🧮 Calculator", "🌦️ Weather", "🌐 Translate"])

    with tab1:
        expr = st.text_input("Expression", placeholder="e.g. (12 + 8) * 3 / 2")
        if st.button("Calculate", type="primary") and expr:
            st.markdown(f"### = {calculate(expr)}")

    with tab2:
        city = st.text_input("City", placeholder="e.g. Kathmandu")
        if st.button("Get Weather", type="primary") and city:
            st.markdown(get_weather(city))

    with tab3:
        text = st.text_area("Text to translate")
        target = st.selectbox("Target language", ["Spanish", "French", "Chinese", "Hindi", "Nepali", "Japanese", "German"])
        if st.button("Translate", type="primary") and text:
            st.markdown(f'<div class="chat-bubble-bot">{translate_text(text, target)}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:1.1rem;">MORE TOOLS</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (ic, label) in enumerate(MORE_TOOLS):
        with cols[i % 5]:
            st.markdown(
                f"""<div class="feature-tile" style="padding:14px 8px;">
                        <div class="feature-icon-wrap" style="width:38px;height:38px;">{icon(ic, 18)}</div>
                        <div class="feature-title" style="font-size:0.8rem;">{label}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
        if i % 5 == 4 and i != len(MORE_TOOLS) - 1:
            st.write("")
            cols = st.columns(5)
