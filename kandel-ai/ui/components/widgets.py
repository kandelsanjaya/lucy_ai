"""
KANDEL AI - Reusable UI Components
Designed by Kandel Sanjaya
"""
import streamlit as st
from ui.components.icons import icon


def electron_loader(label: str = "Generating..."):
    st.markdown(
        f"""
        <div class="kai-loader">
            <div class="kai-orbit">
                <div class="kai-nucleus"></div>
                <div class="kai-electron e1"></div>
                <div class="kai-electron e2"></div>
                <div class="kai-electron e3"></div>
            </div>
        </div>
        <p class="kai-muted" style="text-align:center;font-size:.85rem;">{label}</p>
        """,
        unsafe_allow_html=True,
    )


def nav_item(name_key: str, label: str, active: bool = False):
    cls = "kai-nav-item active" if active else "kai-nav-item"
    return f"""<div class="{cls}">{icon(name_key, 18)}<span>{label}</span></div>"""


def stat_card(label: str, value: str, delta: str = ""):
    delta_html = f'<div class="kai-stat-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kai-card">
            <div class="kai-stat-label">{label}</div>
            <div class="kai-stat-num">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def progress_bar(percent: float):
    st.markdown(
        f"""
        <div class="kai-progress-track">
            <div class="kai-progress-fill" style="width:{percent}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sun_moon_switch(checked: bool, key: str):
    # Real toggle logic is handled by a Streamlit checkbox (hidden) paired with this visual;
    # we use st.toggle for actual state and just theme it via CSS.
    return st.toggle("Light mode", value=checked, key=key, label_visibility="collapsed")


def chat_bubble_user(text: str):
    st.markdown(f'<div class="kai-bubble-user">{text}</div>', unsafe_allow_html=True)


def chat_bubble_ai(text: str, streaming: bool = False):
    cursor = '<span class="kai-cursor"></span>' if streaming else ""
    st.markdown(f'<div class="kai-bubble-ai">{text}{cursor}</div>', unsafe_allow_html=True)


def message_meta(agent: str, model: str, confidence: float, response_time: float, sources: list):
    src_html = ""
    if sources:
        li_parts = []
        best_link_html = ""
        for s in sources:
            title = s.get("title", "")
            url = s.get("url", "")
            is_best = s.get("best", False)
            line = f"<li>{'⭐ ' if is_best else ''}{title}{' — ' + url if url else ''}</li>"
            li_parts.append(line)
            if is_best and url:
                best_link_html = f'<a href="{url}" target="_blank" class="kai-best-link">🔗 Best source: {title}</a>'
        items = "".join(li_parts)
        src_html = f"<details><summary>Sources ({len(sources)})</summary><ul>{items}</ul></details>{best_link_html}"
    st.markdown(
        f"""
        <div class="kai-muted" style="font-size:.75rem; margin-top:.2rem;">
            Agent: <b>{agent}</b> · Model: <b>{model}</b> · Confidence: <b>{int(confidence*100)}%</b> · {response_time}s
            {src_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
