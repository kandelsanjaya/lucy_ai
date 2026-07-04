"""
KANDEL AI - Image Generation Service
Designed by Kandel Sanjaya

Uses Pollinations.ai (free, no API key) by default. Swappable for
Stable Diffusion / Automatic1111 / OpenAI Images later via IMAGE_GEN_PROVIDER.
"""
import urllib.parse
import random


def generate_image_url(prompt: str, width: int = 768, height: int = 768, seed: int = None, negative_prompt: str = ""):
    seed = seed if seed is not None else random.randint(0, 999999)
    full_prompt = prompt
    if negative_prompt:
        full_prompt += f" ### negative: {negative_prompt}"
    encoded = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true"
    return url, seed
