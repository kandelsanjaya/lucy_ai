import streamlit as st
from utils.icons import icon
from utils.helpers import memory_usage_stats

ACTIVITY = [
    ("chat", "Asked about AI in Healthcare", "2m ago"),
    ("code", "Debugged a Python script", "1h ago"),
    ("documents", "Uploaded Climate Change Report", "3h ago"),
    ("image", "Generated a cyberpunk cityscape", "5h ago"),
]


def render(user):
    stats = memory_usage_stats()

    st.markdown(
        f"""
        <div class="glass-card" style="display:flex;align-items:center;gap:20px;">
            <div style="width:76px;height:76px;border-radius:50%;background:var(--grad-primary);
                 display:flex;align-items:center;justify-content:center;color:white;
                 font-size:1.8rem;font-weight:800;flex-shrink:0;">
                 {user['name'][0]}
            </div>
            <div style="flex:1;">
                <div style="font-size:1.3rem;font-weight:800;">{user['name']}</div>
                <div class="muted small">{user['email']}</div>
                <div class="pill active" style="margin-top:8px;">{icon('sparkle', 12)} {user['plan']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "Total Chats", len(st.session_state.get("messages", [])) or 1287),
        (c2, "Documents", len(st.session_state.get("documents", [])) or 56),
        (c3, "Images Generated", st.session_state.get("images_generated", 342)),
        (c4, "Memory Items", stats["used"] or 923),
    ]
    for col, label, value in metrics:
        col.markdown(f"""<div class="stat-card"><div class="stat-label">{label}</div>
                        <div class="stat-value">{value:,}</div></div>""", unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.4, 1], gap="medium")

    with left:
        st.markdown(f"<div class='sub-heading'>{icon('user', 16)} Edit Profile</div>", unsafe_allow_html=True)
        with st.form("profile_form"):
            name = st.text_input("Full name", value=user["name"])
            email = st.text_input("Email", value=user["email"])
            bio = st.text_area("About you", placeholder="Tell Lucy a bit about yourself so replies feel more you...")
            saved = st.form_submit_button("💾 Save changes", type="primary")
        if saved:
            st.session_state.user["name"] = name or user["name"]
            st.session_state.user["email"] = email or user["email"]
            st.success("Profile updated!")
            st.rerun()

    with right:
        st.markdown(f"<div class='sub-heading'>{icon('memory', 16)} Recent Activity</div>", unsafe_allow_html=True)
        for ic, text, t in ACTIVITY:
            st.markdown(
                f"""<div class="glass-card" style="padding:10px 14px;margin-bottom:8px;
                    display:flex;align-items:center;justify-content:space-between;">
                    <span class="small">{icon(ic, 14, '#818cf8')} {text}</span>
                    <span class="small muted">{t}</span>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    if st.button("🚪 Log out", type="secondary"):
        st.session_state.logged_in = False
        st.rerun()