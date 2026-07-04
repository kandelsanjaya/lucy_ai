"""
KANDEL AI - Image Generation Page
Designed by Kandel Sanjaya
"""
import streamlit as st
import requests
import time
from services.image_gen import generate_image_url
from ui.components.widgets import electron_loader
from database.db import get_conn


def _save_image(user_id, prompt, url):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO images (user_id, prompt, url) VALUES (?, ?, ?)", (user_id, prompt, url))


def _gallery(user_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM images WHERE user_id=? ORDER BY created_at DESC LIMIT 12", (user_id,))
        return [dict(r) for r in c.fetchall()]


def _fetch_image_bytes(url: str):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.content
    except Exception:
        return None


def render_image_gen(user: dict):
    st.markdown("### AI Image Generation")
    st.caption("Describe what you want to see — powered by a free diffusion backend.")

    with st.form("image_form"):
        prompt = st.text_area("Prompt", placeholder="Cyberpunk city at night, neon lights, rain reflections")
        c1, c2, c3 = st.columns(3)
        with c1:
            aspect = st.selectbox("Aspect Ratio", ["1:1", "16:9", "9:16"])
        with c2:
            negative = st.text_input("Negative prompt", placeholder="blurry, low quality")
        with c3:
            seed = st.number_input("Seed (0 = random)", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Generate")

    if submitted and prompt.strip():
        w, h = {"1:1": (768, 768), "16:9": (1024, 576), "9:16": (576, 1024)}[aspect]
        with st.spinner(""):
            electron_loader("Generating your image...")
            url, used_seed = generate_image_url(prompt, width=w, height=h, seed=seed or None, negative_prompt=negative)
        st.image(url, caption=f"Seed: {used_seed}")
        img_bytes = _fetch_image_bytes(url)
        if img_bytes:
            st.download_button(
                "⬇ Download Image", data=img_bytes,
                file_name=f"kandel_ai_{used_seed}_{int(time.time())}.png",
                mime="image/png", key="dl_generated_img",
            )
        _save_image(user["id"], prompt, url)
        st.success("Image generated and saved to your gallery.")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("#### Your Gallery")
    imgs = _gallery(user["id"])
    if not imgs:
        st.info("No images generated yet.")
    else:
        cols = st.columns(4)
        for i, img in enumerate(imgs):
            with cols[i % 4]:
                st.image(img["url"], caption=img["prompt"][:40])
                gallery_bytes = _fetch_image_bytes(img["url"])
                if gallery_bytes:
                    st.download_button(
                        "⬇", data=gallery_bytes, file_name=f"kandel_ai_gallery_{img['id']}.png",
                        mime="image/png", key=f"dl_gallery_{img['id']}", use_container_width=True,
                    )
