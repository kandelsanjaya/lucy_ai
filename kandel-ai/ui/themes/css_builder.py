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

/* ---------- Uiverse-style animated CTA buttons (Streamlit compatible) ---------- */
/* Streamlit markup is typically: div.stButton > button and div.stFormSubmitButton > button */
div.stButton > button, div.stFormSubmitButton > button {{
    position: relative !important;
    padding: 14px 42px !important;

    /* Uiverse base */
    background: #fec195 !important;
    border: 1px solid rgb(88, 28, 135) !important;

    border-radius: 12px !important;

    font-size: 16px !important;
    font-weight: 600 !important;
    color: #000000 !important;


    cursor: pointer !important;
    filter: drop-shadow(2px 2px 3px rgba(0, 0, 0, 0.2));

    transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease, background .35s ease !important;
    box-shadow: 0 10px 30px -18px rgba(0,0,0,.5);

    /* custom animated paint */
    background-size: 250% 250% !important;
    background-position: 0% 50% !important;
    overflow: hidden;
}}

/* Provide decorative “icons” via pseudo-elements so every Streamlit button gets the same feel */
div.stButton > button::before,
div.stFormSubmitButton > button::before {{
    content: "";
    position: absolute;
    inset: -40% -20% auto -20%;
    height: 180%;
    background: radial-gradient(circle at 20% 10%, rgba(255,255,255,.55), transparent 45%),
                linear-gradient(90deg, rgba(255,255,255,.0), rgba(255,255,255,.25), rgba(255,255,255,.0));
    transform: rotate(8deg);
    opacity: .0;
    transition: opacity .25s ease;
    pointer-events: none;
}}

div.stButton > button::after,
div.stFormSubmitButton > button::after {{
    /* left ornament */
    content: "";
    position: absolute;
    top: 0;
    left: 14px;
    width: 18px;
    height: 100%;
    background: radial-gradient(circle at 50% 15%, rgba(0,0,0,.18), transparent 55%),
                linear-gradient(135deg, rgba(255,255,255,.35), rgba(255,255,255,0));
    opacity: .0;
    transform: rotate(-6deg);
    transition: opacity .25s ease, transform .25s ease;
    pointer-events: none;
}}

/* Hover / animation state (match Uiverse logic) */
div.stButton > button:hover,
div.stFormSubmitButton > button:hover {{
    border: 1px solid rgb(88, 28, 135) !important;

    background: linear-gradient(
        85deg,
        #fec195,
        #fcc196,
        #fabd92,
        #fac097,
        #fac39c
    ) !important;

    animation: wind 2s ease-in-out infinite;
    transform: translateY(-1px) scale(1.02) !important;
    box-shadow: 0 0 22px color-mix(in srgb, var(--accent2) 70%, transparent);
}}

div.stButton > button:hover::before,
div.stFormSubmitButton > button:hover::before {{ opacity: .9; }}

div.stButton > button:hover::after,
div.stFormSubmitButton > button:hover::after {{
    opacity: .9;
    animation: slay-2 3s cubic-bezier(0.52, 0, 0.58, 1) 1s infinite;
    transform: rotate(0deg);
}}

div.stButton > button:hover span,
div.stFormSubmitButton > button:hover span {{
    /* tiny lift / glow on label */
    text-shadow: 0 0 18px rgba(34,211,238,.35);
}}

div.stButton > button:active,
div.stFormSubmitButton > button:active {{ transform: scale(0.97) !important; }}

@keyframes wind {{{{ 
    0% {{ background-position: 0% 50%; }}
    0% {{ background-position: 50% 100%; }}
    0% {{ background-position: 0% 50%; }}
}}}}

@keyframes slay-2 {{{{ 
    0% {{ transform: rotate(0deg); }}
    50% {{ transform: rotate(15deg); }}
    100% {{ transform: rotate(0); }}
}}}}







/* Reduced motion accessibility */
@media (prefers-reduced-motion: reduce) {{
    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {{ animation: none !important; }}
    div.stButton > button:hover::after,
    div.stFormSubmitButton > button:hover::after {{ animation: none !important; }}
}}



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

.kai-pill {{
    display: inline-flex;
    align-items: center;
    gap: .3rem;
    padding: .25rem .7rem;
    border-radius: 9999px;
    border: 1px solid var(--border);
    background: var(--surface);
    font-size: .7rem;
    color: var(--muted);
}}

h1, h2, h3, h4, p, span, div {{ color: var(--text); }}
.kai-muted {{ color: var(--muted) !important; }}

/* ---------- ChatGPT-like layout polish ---------- */
.kai-shell {{
    max-width: 1200px;
    margin: 0 auto;
}}

.kai-page-header {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1rem;
}}
.kai-page-title {{
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}}
.kai-page-subtitle {{
    color: var(--muted);
    font-size: .85rem;
    margin-top: .25rem;
}}

.kai-divider {{
    height: 1px;
    width: 100%;
    background: var(--border);
    margin: .9rem 0;
}}

.kai-section-title {{
    font-weight: 800;
    font-size: .95rem;
    letter-spacing: .01em;
}}

.kai-action-btn {{
    width: 100%;
    text-align: left;
    padding: .7rem .75rem !important;
    border-radius: 14px !important;
    background: color-mix(in srgb, var(--surface) 85%, transparent) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease, filter .2s ease !important;
}}
.kai-action-btn:hover {{
    transform: translateY(-2px);
    border-color: color-mix(in srgb, var(--accent2) 55%, var(--border));
    box-shadow: 0 0 22px color-mix(in srgb, var(--accent2) 40%, transparent);
    filter: brightness(1.05);
}}

.kai-action-ico {{
    width: 34px;
    height: 34px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border);
    background: color-mix(in srgb, var(--accent2) 14%, var(--surface));
    margin-right: .55rem;
    font-size: 1.05rem;
}}

.kai-hero-card {{
    padding: 2.1rem 1.6rem !important;
    text-align: center;
}}

.kai-hero-lines {{
    display:flex;
    justify-content:center;
    gap:.6rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}}

.kai-chip {{
    display:inline-flex;
    align-items:center;
    gap:.35rem;
    padding:.35rem .65rem;
    border-radius: 9999px;
    border: 1px solid var(--border);
    background: color-mix(in srgb, var(--surface) 80%, transparent);
    color: var(--muted);
    font-size: .78rem;
}}

.kai-link {{
    color: var(--muted) !important;
    text-decoration: none;
    border-bottom: 1px dashed color-mix(in srgb, var(--muted) 55%, transparent);
}}
.kai-link:hover {{ color: var(--text) !important; border-bottom-color: var(--text); }}

</style>
"""
