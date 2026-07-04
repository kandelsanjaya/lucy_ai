"""
KANDEL AI - OCR Service
Designed by Kandel Sanjaya
"""
from PIL import Image
import pytesseract


def extract_text_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)
