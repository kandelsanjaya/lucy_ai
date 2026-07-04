"""
KANDEL AI - Settings Page
Designed by Kandel Sanjaya
"""
import streamlit as st
from ui.themes.tokens import THEMES
from database.db import get_conn
from ui.components.icons import icon


def _update_user_field(user_id, field, value):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(f"UPDATE users SET {field} = ? WHERE id = ?", (value, user_id))


SETTINGS_NAV = [
    ("profile", "user", "Public Profile"),
    ("account", "settings", "Account"),
    ("appearance", "image", "Appearance"),
    ("model", "code", "Model & LLM"),
    ("notifications", "bell", "Notifications"),
]


def render_settings(user: dict):
    st.markdown("### Settings")

    nav_col, content_col = st.columns([1, 3])
    with nav_col:
        st.markdown('<div class="kai-card">', unsafe_allow_html=True)
        section = st.session_state.get("settings_section", "profile")
        for key, icon_key, label in SETTINGS_NAV:
            if st.button(f"{label}", key=f"settings_nav_{key}", use_container_width=True):
                st.session_state.settings_section = key
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        section = st.session_state.get("settings_section", "profile")

    with content_col:
        st.markdown('<div class="kai-card">', unsafe_allow_html=True)

        if section == "profile":
            st.markdown("#### Public Profile")
            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown(
                    f'<div style="width:70px;height:70px;border-radius:50%;background:var(--gradient);"></div>',
                    unsafe_allow_html=True,
                )
            with c2:
                st.write(f"**{user['name']}**")
                st.caption(user["email"])
                st.caption(f"Role: {user.get('role','user').title()} · Plan: Pro")

        elif section == "account":
            st.markdown("#### Account")
            st.text_input("Name", value=user["name"], key="acc_name")
            st.text_input("Email", value=user["email"], disabled=True)
            if st.button("Save Account Changes"):
                _update_user_field(user["id"], "name", st.session_state.acc_name)
                st.success("Account updated. Refresh to see changes reflected everywhere.")

        elif section == "appearance":
            st.markdown("#### Appearance — Choose your theme")
            current = user.get("theme") or "cyber_neon"
            dark_themes = {k: v for k, v in THEMES.items() if v["mode"] == "dark"}
            light_themes = {k: v for k, v in THEMES.items() if v["mode"] == "light"}

            st.markdown("**Dark Themes**")
            cols = st.columns(5)
            for col, (key, t) in zip(cols, dark_themes.items()):
                with col:
                    if st.button(t["label"], key=f"theme_{key}", use_container_width=True):
                        _update_user_field(user["id"], "theme", key)
                        st.session_state.user["theme"] = key
                        st.rerun()

            st.markdown("**Light Themes**")
            cols2 = st.columns(5)
            for col, (key, t) in zip(cols2, light_themes.items()):
                with col:
                    if st.button(t["label"], key=f"theme_{key}", use_container_width=True):
                        _update_user_field(user["id"], "theme", key)
                        st.session_state.user["theme"] = key
                        st.rerun()

            st.caption(f"Active theme: **{THEMES[current]['label']}**")

        elif section == "model":
            st.markdown("#### Model & LLM (Groq)")
            st.selectbox(
                "Model",
                ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"],
                key="model_select",
            )
            st.slider("Temperature", 0.0, 1.5, 0.7, key="temp_select")
            st.slider("Top P", 0.0, 1.0, 0.9, key="topp_select")
            st.slider("Max tokens", 256, 4096, 1024, step=128, key="maxtok_select")
            if st.button("Save Model Settings"):
                _update_user_field(user["id"], "model", st.session_state.model_select)
                st.success("Model preference saved.")
            st.markdown("---")
            st.caption("API keys are managed via your `.env` file and are never shown in the UI once set.")

        elif section == "notifications":
            st.markdown("#### Notifications")
            st.checkbox("Email me weekly usage summaries", value=True)
            st.checkbox("Notify me when a document finishes indexing", value=True)
            st.checkbox("Notify me about new KANDEL AI features", value=False)

        st.markdown("</div>", unsafe_allow_html=True)
