import streamlit as st
from utils.icons import icon
from utils.helpers import extract_text_from_image


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('ocr', 20)} OCR — Extract Text from Images</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "webp"])
        if img:
            st.image(img, use_container_width=True)
    with col2:
        st.markdown(f"<div class='sub-heading'>{icon('documents', 16)} Extracted Text</div>", unsafe_allow_html=True)
        if img:
            with st.spinner("Reading the image..."):
                text = extract_text_from_image(img)
            st.text_area("Extracted text", value=text, height=280, label_visibility="collapsed")
            st.download_button("📋 Copy / Download", text, file_name="extracted_text.txt")
        else:
            st.markdown(
                """<div class="glass-card" style="height:280px;display:flex;align-items:center;
                justify-content:center;color:var(--text-3);">Extracted text will appear here</div>""",
                unsafe_allow_html=True,
            )
    st.caption("Requires the `tesseract-ocr` binary installed on your system "
               "(`sudo apt install tesseract-ocr` on Linux, `brew install tesseract` on macOS).")
