import streamlit as st
from utils.icons import icon
from services.image_gen import generate_image_url



def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('image', 20)} Image Generation</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        prompt = st.text_area("Prompt", placeholder='"Cyberpunk city at night, neon lights"', height=100)
        size = st.selectbox("Size", ["1024x1024", "1792x1024", "1024x1792"])
        if st.button("✨ Generate", type="primary") and prompt:
            with st.spinner("Painting your imagination..."):
                # Pollinations-style URL generator (no API key required)
                url, used_seed = generate_image_url(
                    prompt,
                    width=int(size.split("x")[0]),
                    height=int(size.split("x")[1]),
                )
                st.session_state["images_generated"] = st.session_state.get("images_generated", 342) + 1
                st.session_state["last_image"] = url
                st.session_state.setdefault("image_gallery", []).insert(0, {"url": url, "prompt": prompt})



    with col2:
        st.markdown(f"<div class='sub-heading'>{icon('sparkle', 16)} Preview</div>", unsafe_allow_html=True)
        if st.session_state.get("last_image"):
            st.image(st.session_state["last_image"], use_container_width=True)
        else:
            st.markdown(
                """<div class="glass-card" style="height:280px;display:flex;align-items:center;
                justify-content:center;color:var(--text-3);">Your generated image will appear here</div>""",
                unsafe_allow_html=True,
            )

    gallery = st.session_state.get("image_gallery", [])
    if gallery:
        st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
        st.markdown(f"<div class='sub-heading'>{icon('image', 16)} Recent generations</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, item in enumerate(gallery[:8]):
            with cols[i % 4]:
                st.image(item["url"], caption=item["prompt"][:40], use_container_width=True)
