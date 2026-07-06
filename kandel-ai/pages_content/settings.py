import streamlit as st
from utils.icons import icon

THEMES = {
    "Cyber Neon": "linear-gradient(135deg,#a78bfa,#38bdf8)",
    "Dark": "linear-gradient(135deg,#1f2937,#111827)",
    "Light": "linear-gradient(135deg,#f3f4f6,#e5e7eb)",
    "Ocean": "linear-gradient(135deg,#0891b2,#164e63)",
    "Sunset": "linear-gradient(135deg,#f97316,#be123c)",
}


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('settings', 20)} Settings</div>",
                unsafe_allow_html=True)

    st.markdown(f"<div class='sub-heading'>{icon('user', 16)} Profile</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.text_input("Name", value=user["name"])
    c2.text_input("Email", value=user["email"], disabled=True)

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    st.markdown(f"<div class='sub-heading'>{icon('sparkle', 16)} API Keys</div>", unsafe_allow_html=True)
    st.text_input("OpenAI API Key", type="password",
                  value="•" * 20 if __import__("os").environ.get("OPENAI_API_KEY") else "",
                  help="Set via environment variable OPENAI_API_KEY or .streamlit/secrets.toml")
    st.caption("For security, keys are read from environment variables / `secrets.toml`, "
               "never stored in the UI.")

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:1.1rem;">THEMES</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for col, (name, grad) in zip(cols, THEMES.items()):
        with col:
            st.markdown(f"""<div class="theme-swatch" style="background:{grad};">{name}</div>""",
                        unsafe_allow_html=True)
            st.button("Apply", key=f"theme_{name}", use_container_width=True)

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    if st.button("🚪 Log out"):
        st.session_state.logged_in = False
        st.rerun()
