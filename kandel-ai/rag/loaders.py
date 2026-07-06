"""
Lucy AI — Loader & Background FX
--------------------------------
Two visual pieces, both adapted (restyled to Lucy's palette) from
Uiverse.io community CSS patterns:

1. `LOADER_HTML`   — an orbiting-electron "thinking" loader, used anywhere
   we'd otherwise show a plain spinner (chat replies, image generation, etc).
2. `galaxy_background()` — a multi-layer animated starfield, used as the
   fixed backdrop on the Dashboard and Chat pages.
"""

import random

# --------------------------------------------------------------------------
# Electron loader
# --------------------------------------------------------------------------
LOADER_HTML = """
<div class="lucy-loader-wrap">
  <div class="lucy-loader">
    <div class="nucleus"></div>
    <div class="electron electron1"></div>
    <div class="electron electron2"></div>
    <div class="electron electron3"></div>
  </div>
  <div class="lucy-loader-label">{label}</div>
</div>
"""

SPLASH_HTML = """
<div class="lucy-splash">
  <div class="lucy-loader">
    <div class="nucleus"></div>
    <div class="electron electron1"></div>
    <div class="electron electron2"></div>
    <div class="electron electron3"></div>
  </div>
  <div class="lucy-splash-title">Lucy AI is waking up...</div>
</div>
"""


def loader_html(label: str = "Lucy is thinking...") -> str:
    return LOADER_HTML.format(label=label)


# --------------------------------------------------------------------------
# Galaxy / starfield background
# --------------------------------------------------------------------------
def _star_shadows(n: int, width: int, height: int, seed: int) -> str:
    rnd = random.Random(seed)
    return ", ".join(
        f"{rnd.randint(0, width)}px {rnd.randint(0, height)}px #fff" for _ in range(n)
    )


# Generated once at import time — deterministic (seeded) so the starfield
# looks the same on every rerun instead of jumping around.
_STARS_1 = _star_shadows(140, 1600, 1000, seed=1)
_STARS_2 = _star_shadows(70, 1600, 1000, seed=2)
_STARS_3 = _star_shadows(40, 1600, 1000, seed=3)

GALAXY_HTML = f"""
<div class="lucy-galaxy">
  <div id="g-stars" style="box-shadow:{_STARS_1};"></div>
  <div id="g-stars2" style="box-shadow:{_STARS_2};"></div>
  <div id="g-stars3" style="box-shadow:{_STARS_3};"></div>
</div>
"""


def run_with_loader(container, fn, *args, label: str = "Lucy is thinking...", **kwargs):
    """
    Show the electron loader inside `container` (an st.empty() placeholder)
    while `fn(*args, **kwargs)` executes, then clear it and return the result.
    """
    container.markdown(loader_html(label), unsafe_allow_html=True)
    try:
        result = fn(*args, **kwargs)
    finally:
        container.empty()
    return result


def galaxy_background() -> str:
    """Return the HTML for the fixed animated starfield backdrop."""
    return GALAXY_HTML