"""kandel-ai utils.loader

The app imports `SPLASH_HTML` from here:

    from utils.loader import SPLASH_HTML

The original project used an electron-style splash loader. Some builds were
missing this module, causing:

    ModuleNotFoundError: No module named 'utils.loader'

This file restores that module and keeps it dependency-free.
"""

SPLASH_HTML = r"""
<div class="lucy-splash" style="position:relative;display:flex;align-items:center;justify-content:center;min-height:200px;">
  <div class="lucy-splash-card" style="width:360px;max-width:92vw;padding:24px 20px;border-radius:18px;">
    <div style="display:flex;align-items:center;justify-content:center;margin-bottom:14px;">
      <div style="width:64px;height:64px;border-radius:16px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#a78bfa,#60a5fa);color:white;font-weight:800;font-size:28px;box-shadow:0 10px 30px rgba(99,102,241,.35);">
        ✨
      </div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:16px;font-weight:800;color:var(--text-1,#111827);margin-bottom:8px;">Loading Lucy AI</div>
      <div style="font-size:13px;color:var(--text-3,#6b7280);">Preparing tools, memory & retrieval…</div>
      <div style="margin-top:18px;height:10px;border-radius:999px;background:rgba(167,139,250,.18);overflow:hidden;">
        <div style="height:100%;width:40%;border-radius:999px;background:linear-gradient(90deg,#a78bfa,#38bdf8);animation:lucy-splash-progress 1.1s ease-in-out infinite;"></div>
      </div>
    </div>
  </div>

  <style>
    @keyframes lucy-splash-progress {
      0% { transform: translateX(-120%); }
      50% { transform: translateX(80%); }
      100% { transform: translateX(160%); }
    }
  </style>
</div>
"""


def galaxy_background() -> str:
    """Background used across the dashboard pages (dependency-free)."""
    return r"""
    <div class="lucy-galaxy-bg" style="position:fixed;inset:0;z-index:-1;overflow:hidden;">
      <div style="position:absolute;inset:-40px;">
        <div style="position:absolute;inset:0;background:radial-gradient(circle at 20% 10%, rgba(167,139,250,.28), transparent 45%),
                                         radial-gradient(circle at 80% 30%, rgba(56,189,248,.22), transparent 50%),
                                         radial-gradient(circle at 50% 70%, rgba(52,211,153,.18), transparent 55%);"></div>
        <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(17,24,39,.6), rgba(2,6,23,.75));"></div>
      </div>
      <div style="position:absolute;inset:0;opacity:.55;filter:blur(.2px);
                  background-image:url('data:image/svg+xml;utf8,
                    <svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
                      <g fill="white" fill-opacity="0.55">
                        <circle cx="9" cy="16" r="1.2"/>
                        <circle cx="44" cy="88" r="1.0"/>
                        <circle cx="120" cy="52" r="1.3"/>
                        <circle cx="200" cy="140" r="1.1"/>
                        <circle cx="160" cy="210" r="1.0"/>
                        <circle cx="230" cy="60" r="1.1"/>
                        <circle cx="72" cy="172" r="1.2"/>
                      </g>
                    </svg>');
                    background-size:240px 240px;"></div>
    </div>
    """


def run_with_loader(slot, fn, args=None, label: str = "Loading..."):
    """Show an in-place loader while `fn(*args)` runs.

    `slot` should be a Streamlit element (e.g., st.empty()).
    Returns the function result.
    """
    if args is None:
        args = []
    try:
        # Lazy import so this module stays Streamlit-optional.
        slot.markdown(
            f"""<div style="margin:12px 0;">{SPLASH_HTML}<div style="font-size:12px;color:var(--text-3,#6b7280);margin-top:8px;">{label}</div></div>""",
            unsafe_allow_html=True,
        )
    except Exception:
        pass

    res = fn(*args)
    try:
        slot.empty()
    except Exception:
        pass
    return res


