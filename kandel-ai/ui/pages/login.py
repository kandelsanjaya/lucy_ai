"""
KANDEL AI - Login / Signup Page (Cortex AI style split-screen)
Designed by Kandel Sanjaya
"""
import streamlit as st
from database.auth import signup, login, create_token
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
    left, right = st.columns([1, 1.15], gap="large")

    # ---------------- LEFT: credentials panel ----------------
    with left:
        # Header
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:2rem;">
                <div style="width:34px;height:34px;border-radius:12px;background:var(--gradient);box-shadow:0 0 26px color-mix(in srgb, var(--accent2) 45%, transparent);"></div>
                <div>
                    <div style="font-weight:900;font-size:1.25rem;letter-spacing:-.01em;line-height:1;">KANDEL AI</div>
                    <div class="kai-muted" style="font-size:.65rem;margin-top:.25rem;">Secure access to your AI workspace</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        tab_login, tab_signup = st.tabs(["Sign In", "Sign Up"])

        with tab_login:
            st.markdown("### Welcome Back")
            st.caption("Enter your credentials to access your AI neural dashboard. Passwords are case-sensitive.")

            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                remember = st.checkbox("Remember this device for 30 days", value=False)

                submitted = st.form_submit_button("Sign In to Kandel AI", use_container_width=True)


            st.markdown(
                '<div style="text-align:right;margin-top:-.6rem;">'
                '<span class="kai-muted" style="font-size:.8rem;">Forgot password? Contact support to reset.</span>'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown("<div class='kai-divider' style='margin:1rem 0 .7rem 0;'></div>", unsafe_allow_html=True)


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

            st.markdown('<p class="kai-muted" style="text-align:center;margin-top:1.1rem;font-size:.75rem;letter-spacing:1px;">OR CONTINUE WITH</p>', unsafe_allow_html=True)

            sc1, sc2 = st.columns(2)
            with sc1:
                if st.button("Google", use_container_width=True, key="login_google", help="OAuth login not enabled in this build"):
                    st.info("Google login is not enabled yet.")

            with sc2:
                if st.button("GitHub", use_container_width=True, key="login_github", help="OAuth login not enabled in this build"):
                    st.info("GitHub login is not enabled yet.")

            st.markdown('<p class="kai-muted" style="text-align:center;margin-top:1rem;font-size:.8rem;">Don\'t have an account? Use the Sign Up tab above.</p>', unsafe_allow_html=True)


        with tab_signup:
            st.markdown("### Create your workspace")
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
                submitted_s = st.form_submit_button("Create Workspace", use_container_width=True)

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

        st.markdown(
            f'<p class="kai-muted" style="margin-top:2rem;font-size:.7rem;">{settings.COPYRIGHT} · '
            f'<a href="#" style="color:var(--muted);">Privacy Policy</a> · <a href="#" style="color:var(--muted);">Terms of Service</a></p>',
            unsafe_allow_html=True,
        )

    # ---------------- RIGHT: hero panel ----------------
    with right:
        st.markdown(
            f"""
            <div class="kai-card" style="padding:2.2rem;text-align:center;">
                <div style="display:flex;justify-content:center;gap:.5rem;margin-bottom:1.2rem;">
                    <span class="kai-pill">🛡 Enterprise Secure</span>
                    <span class="kai-pill">🧠 Global Memory RAG</span>
                </div>
                <div class="kai-orb-hero" style="width:200px;height:200px;"></div>
                <h1 style="margin-top:1.4rem;font-size:2rem;">The Engine of<br><span style="background:var(--gradient);-webkit-background-clip:text;background-clip:text;color:transparent;">Artificial Intuition</span></h1>
                <p class="kai-muted" style="max-width:420px;margin:.8rem auto 1.5rem;">
                    KANDEL AI bridges the gap between raw data and creative execution —
                    seamlessly integrating multi-modal agents into your workflow, powered by Groq.
                </p>
                <div style="display:flex;justify-content:center;gap:2.5rem;border-top:1px solid var(--border);padding-top:1.2rem;">
                    <div><div class="kai-stat-num" style="font-size:1.4rem;">99.9%</div><div class="kai-stat-label">Uptime SLA</div></div>
                    <div><div class="kai-stat-num" style="font-size:1.4rem;">50ms</div><div class="kai-stat-label">Response</div></div>
                    <div><div class="kai-stat-num" style="font-size:1.4rem;">AES-256</div><div class="kai-stat-label">Encrypted</div></div>
                </div>
            </div>
            <p class="kai-muted" style="text-align:center;margin-top:1rem;font-style:italic;">Designed by Kandel Sanjaya</p>
            """,
            unsafe_allow_html=True,
        )
