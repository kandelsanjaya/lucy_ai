"""
KANDEL AI - CSS Builder
Designed by Kandel Sanjaya

Converts a theme token dict into a full CSS string injected into Streamlit,
carrying over the animation concepts (electron-orbit loader, sparkle button,
sun/moon switch, glass accent-bar menu, neon chat glow).
"""
from ui.themes.tokens import THEMES


def build_css(theme_key: str) -> str:
    t = THEMES.get(theme_key, THEMES["cyber_neon"])

    return f"""
<style>
:root {{
    --bg: {t['bg']};
    --surface: {t['surface']};
    --border: {t['border']};
    --text: {t['text']};
    --muted: {t['muted']};
    --accent: {t['accent']};
    --accent2: {t['accent2']};
    --gradient: {t['gradient']};
}}

.stApp {{
    background: var(--bg);
    color: var(--text);
    transition: background 0.4s ease, color 0.4s ease;
}}

section[data-testid="stSidebar"] {{
    background: var(--surface);
    backdrop-filter: blur(18px);
    border-right: 1px solid var(--border);
}}

/* ---------- Glass card ---------- */
.kai-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    backdrop-filter: blur(16px);
    transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}}
.kai-card:hover {{
    transform: translateY(-3px);
    border-color: var(--accent);
    box-shadow: 0 0 24px color-mix(in srgb, var(--accent) 35%, transparent);
}}

/* ---------- Sidebar menu item (glass accent-bar pattern) ---------- */
.kai-nav-item {{
    position: relative;
    display: flex;
    align-items: center;
    gap: .6rem;
    padding: .55rem .8rem;
    border-radius: 10px;
    color: var(--muted);
    cursor: pointer;
    transition: all .3s ease;
    border: 2px solid transparent;
}}
.kai-nav-item:hover {{
    border-color: var(--border);
    color: var(--text);
    filter: brightness(1.1);
}}
.kai-nav-item.active {{
    background: color-mix(in srgb, var(--accent) 16%, transparent);
    color: var(--text);
    margin-left: 6px;
}}
.kai-nav-item.active::before {{
    content: "";
    position: absolute;
    top: 15%;
    left: -10px;
    width: 4px;
    height: 70%;
    border-radius: 6px;
    background: var(--accent);
    box-shadow: 0 0 10px var(--accent);
}}

/* ---------- Neon chat bubbles ---------- */
.kai-bubble-user {{
    background: var(--gradient);
    color: white;
    padding: .8rem 1.1rem;
    border-radius: 16px 16px 4px 16px;
    margin: .4rem 0;
    max-width: 80%;
    margin-left: auto;
    animation: kai-fade-in .35s ease;
}}
.kai-bubble-ai {{
    background: var(--surface);
    border: 1px solid var(--accent);
    box-shadow: 0 0 18px color-mix(in srgb, var(--accent) 45%, transparent);
    color: var(--text);
    padding: .8rem 1.1rem;
    border-radius: 16px 16px 16px 4px;
    margin: .4rem 0;
    max-width: 85%;
    animation: kai-fade-in .35s ease;
}}
@keyframes kai-fade-in {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* ---------- Typing cursor ---------- */
.kai-cursor::after {{
    content: "▍";
    display: inline-block;
    color: var(--accent2);
    animation: kai-blink 1s steps(2) infinite;
}}
@keyframes kai-blink {{ 50% {{ opacity: 0; }} }}

/* ---------- Electron-orbit generation loader ---------- */
.kai-loader {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 5rem;
}}
.kai-orbit {{
    position: relative;
    width: 4.5rem;
    height: 4.5rem;
    animation: kai-rotate 3s linear infinite;
}}
.kai-nucleus {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    width: .7rem; height: .7rem;
    border-radius: 50%;
    background: var(--gradient);
    box-shadow: 0 0 12px var(--accent2);
}}
.kai-electron {{
    position: absolute;
    top: 50%; left: 50%;
    width: 4.5rem; height: 1.8rem;
    margin-top: -0.9rem; margin-left: -2.25rem;
    border-radius: 50%;
    border: 2px solid var(--accent2);
    animation: kai-revolve 1s linear infinite;
}}
.kai-electron.e2 {{ transform: rotate(60deg); animation-delay: -0.4s; }}
.kai-electron.e3 {{ transform: rotate(-60deg); animation-delay: -0.7s; }}
@keyframes kai-rotate {{ to {{ transform: rotate(360deg); }} }}
@keyframes kai-revolve {{
    0% {{ border-color: var(--accent2); border-right-color: transparent; }}
    25% {{ border-bottom-color: transparent; }}
    50% {{ border-left-color: transparent; }}
    75% {{ border-top-color: transparent; }}
    100% {{ border-right-color: transparent; }}
}}

/* ---------- Sparkle gradient CTA button ---------- */
div.stButton > button, div.stFormSubmitButton > button {{
    position: relative;
    background: var(--gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: 9999px !important;
    padding: .6rem 1.5rem !important;
    font-weight: 600 !important;
    transition: transform .25s ease, box-shadow .25s ease !important;
    box-shadow: 0 4px 14px -4px color-mix(in srgb, var(--accent) 60%, transparent);
}}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {{
    transform: scale(1.04);
    box-shadow: 0 0 22px color-mix(in srgb, var(--accent2) 70%, transparent);
}}
div.stButton > button:active {{ transform: scale(0.97); }}

/* ---------- Theme sun/moon switch ---------- */
.kai-switch {{ position: relative; width: 3.4em; height: 1.9em; display: inline-block; }}
.kai-switch input {{ opacity: 0; width: 0; height: 0; }}
.kai-slider {{
    position: absolute; inset: 0; cursor: pointer;
    background: #20262c; border-radius: 30px; transition: .5s;
}}
.kai-slider:before {{
    position: absolute; content: ""; height: 1.35em; width: 1.35em;
    left: 8%; bottom: 12%; border-radius: 50%;
    background: linear-gradient(#fef08a,#fde047);
    box-shadow: inset 4px -2px 0 0 #fef9c3;
    transition: .5s;
}}
.kai-switch input:checked + .kai-slider {{ background: var(--accent); }}
.kai-switch input:checked + .kai-slider:before {{ transform: translateX(115%); background: #e5e7eb; }}

/* ---------- Login parallax orb ---------- */
.kai-orb-hero {{
    width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, var(--accent2), var(--accent) 60%, transparent 75%);
    filter: blur(2px);
    animation: kai-pulse 4s ease-in-out infinite;
    margin: 0 auto;
}}
@keyframes kai-pulse {{
    0%,100% {{ transform: scale(1); opacity: .85; }}
    50% {{ transform: scale(1.06); opacity: 1; }}
}}

/* ---------- Progress ring / bars ---------- */
.kai-progress-track {{
    background: var(--border); border-radius: 20px; height: 8px; overflow: hidden;
}}
.kai-progress-fill {{
    height: 100%; border-radius: 20px; background: var(--gradient);
    animation: kai-grow 1.1s ease-out;
}}
@keyframes kai-grow {{ from {{ width: 0; }} }}

/* ---------- Stat card number ---------- */
.kai-stat-num {{ font-size: 1.8rem; font-weight: 700; color: var(--text); }}
.kai-stat-label {{ color: var(--muted); font-size: .8rem; text-transform: uppercase; letter-spacing: .04em; }}
.kai-stat-delta {{ color: var(--accent2); font-size: .8rem; font-weight: 600; }}

.kai-best-link {{
    display: inline-block;
    margin-top: .4rem;
    padding: .3rem .7rem;
    border-radius: 8px;
    background: color-mix(in srgb, var(--accent2) 18%, transparent);
    color: var(--accent2) !important;
    text-decoration: none;
    font-size: .75rem;
    font-weight: 600;
    border: 1px solid var(--accent2);
}}
.kai-best-link:hover {{ filter: brightness(1.2); }}

h1, h2, h3, h4, p, span, div {{ color: var(--text); }}
.kai-muted {{ color: var(--muted) !important; }}
</style>
"""
