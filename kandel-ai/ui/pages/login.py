"""
KANDEL AI - Login / Signup Page
Designed by Kandel Sanjaya
"""
import streamlit as st
from database.auth import signup, login, create_token
from ui.components.icons import icon
from config.settings import settings


def _password_strength(pw: str) -> tuple:
    score = 0
    if len(pw) >= 8: score += 1
    if any(c.isupper() for c in pw): score += 1
    if any(c.isdigit() for c in pw): score += 1
    if any(not c.isalnum() for c in pw): score += 1
    labels = ["Very weak", "Weak", "Fair", "Good", "Strong"]
    colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#22d3ee"]
    return labels[score], colors[score], (score / 4) * 100


def render_login():
    left, right = st.columns([1, 1.2], gap="large")

    with left:
        st.markdown('<div class="kai-orb-hero"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <h1 style="text-align:center;">KANDEL AI</h1>
            <p class="kai-muted" style="text-align:center;">All-in-One RAG AI Platform</p>
            <p class="kai-muted" style="text-align:center;font-style:italic;">Designed by Kandel Sanjaya</p>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="kai-card">', unsafe_allow_html=True)
        mode = st.session_state.get("auth_mode", "login")
        tab_login, tab_signup = st.tabs(["Sign In", "Sign Up"])

        with tab_login:
            st.markdown(f"### Welcome Back")
            st.caption("Sign in to continue to Kandel AI. Passwords are case-sensitive.")
            with st.form("login_form"):
                email = st.text_input(f"Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                c1, c2 = st.columns(2)
                with c1:
                    remember = st.checkbox("Remember me")
                with c2:
                    st.markdown('<div style="text-align:right;padding-top:.4rem;"><a href="#">Forgot password?</a></div>', unsafe_allow_html=True)
                submitted = st.form_submit_button("Sign In", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    ok, msg, user = login(email, password)
                    if ok:
                        st.session_state.token = create_token(user)
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.session_state.page = "dashboard"
                        st.success("Login successful. Redirecting...")
                        st.rerun()
                    else:
                        st.error(msg)

            st.markdown('<p class="kai-muted" style="text-align:center;margin-top:.8rem;">Or continue with</p>', unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown(f'<div class="kai-card" style="text-align:center;">{icon("google",22)}</div>', unsafe_allow_html=True)
            with sc2:
                st.markdown(f'<div class="kai-card" style="text-align:center;">{icon("github",22)}</div>', unsafe_allow_html=True)
            with sc3:
                st.markdown(f'<div class="kai-card" style="text-align:center;">{icon("microsoft",22)}</div>', unsafe_allow_html=True)

        with tab_signup:
            st.markdown("### Create your account")
            with st.form("signup_form"):
                name = st.text_input("Full name")
                email_s = st.text_input("Email", key="signup_email")
                password_s = st.text_input("Password", type="password", key="signup_pw")
                if password_s:
                    label, color, pct = _password_strength(password_s)
                    st.markdown(
                        f"""<div class="kai-progress-track"><div class="kai-progress-fill" style="width:{pct}%;background:{color};"></div></div>
                        <p style="font-size:.75rem;color:{color};margin-top:.2rem;">{label}</p>""",
                        unsafe_allow_html=True,
                    )
                submitted_s = st.form_submit_button("Sign Up", use_container_width=True)

            if submitted_s:
                if not name or not email_s or not password_s:
                    st.error("All fields are required.")
                elif len(password_s) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    ok, msg = signup(name, email_s, password_s)
                    if ok:
                        st.success(f"{msg} Please sign in.")
                    else:
                        st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            f'<p class="kai-muted" style="text-align:center;margin-top:1rem;font-size:.75rem;">{settings.COPYRIGHT}</p>',
            unsafe_allow_html=True,
        )
