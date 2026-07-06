import streamlit as st
from utils.icons import icon
from utils.helpers import memory_usage_stats, chat_completion
from utils.loader import galaxy_background, run_with_loader

TILE_COLORS = ["tile-violet", "tile-blue", "tile-cyan", "tile-teal", "tile-green",
               "tile-lime", "tile-amber", "tile-orange", "tile-pink", "tile-rose"]

FEATURES = [
    ("documents", "RAG Chat", "Chat with your documents", "rag_chat"),
    ("websearch", "Web Search", "Real-time information", "web_search"),
    ("image", "Image Generation", "Create with AI", "image_gen"),
    ("ocr", "OCR", "Extract text from images", "ocr"),
    ("code", "Code Assistant", "Write & debug code", "code_assistant"),
    ("voice", "Voice Assistant", "Speak to Lucy", "voice"),
    ("globe", "Multi-language", "100+ languages", "tools"),
    ("brain", "Data Analysis", "Analyze & visualize", "tools"),
    ("memory", "Memory", "Remembers you", "memory"),
    ("tools", "Tools", "Calculator, weather & more", "tools"),
]

QUICK_ACTIONS = [
    ("documents", "Summarize PDF", "rag_chat"),
    ("image", "Generate Image", "image_gen"),
    ("code", "Write Code", "code_assistant"),
    ("globe", "Translate Text", "tools"),
    ("dashboard", "Analyze Data", "tools"),
]


def render(user):
    st.markdown(galaxy_background(), unsafe_allow_html=True)
    stats = memory_usage_stats()

    st.markdown(
        f"""
        <div class="flex-between">
            <div>
                <div style="font-size:1.3rem;font-weight:800;">Your AI Agent Workspace {icon('sparkle', 18, '#a78bfa')}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Stat row ----
    c1, c2, c3, c4 = st.columns(4)
    stat_data = [
        (c1, "Total Chats", len(st.session_state.get("chat_history", [])) or 1287, "+12.5%"),
        (c2, "Documents", len(st.session_state.get("documents", [])) or 56, "+8.2%"),
        (c3, "Images Generated", st.session_state.get("images_generated", 342), "+18.7%"),
        (c4, "Memory Items", stats["used"] or 923, "+23.1%"),
    ]
    for col, label, value, delta in stat_data:
        col.markdown(
            f"""<div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value:,}</div>
                    <div class="stat-delta">▲ {delta}</div>
                </div>""",
            unsafe_allow_html=True,
        )

    st.write("")
    left, right = st.columns([2.4, 1], gap="medium")

    # ---- Hero / ask box ----
    with left:
        st.markdown(
            f"""
            <div class="glass-card hero-wrap">
                <div class="hero-greet">Hello, <span class="name">{user['name'].split()[0]}!</span> 👋</div>
                <div class="hero-sub">How can I help you today?</div>
                <div class="orb"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("ask_form", clear_on_submit=True):
            q = st.text_input("Ask me anything...", label_visibility="collapsed",
                               placeholder="Ask me anything...")
            cols = st.columns([1, 1, 1, 5, 1])
            mode = cols[0].selectbox("mode", ["RAG", "Web", "Auto"], label_visibility="collapsed")
            submitted = cols[4].form_submit_button("➤", use_container_width=True)
        if submitted and q:
            loader_slot = st.empty()
            reply = run_with_loader(loader_slot, chat_completion, [
                {"role": "system", "content": "You are Lucy, a friendly all-in-one AI agent."},
                {"role": "user", "content": q},
            ], label="Lucy is thinking...")
            st.markdown(f'<div class="chat-bubble-bot">{reply}</div>', unsafe_allow_html=True)

        st.write("")
        qcols = st.columns(len(QUICK_ACTIONS))
        for col, (ic, label, target) in zip(qcols, QUICK_ACTIONS):
            with col:
                st.markdown(
                    f"""<div class="pill" style="justify-content:center;width:100%;margin-bottom:6px;">
                        {icon(ic, 14, '#a78bfa')} {label}</div>""",
                    unsafe_allow_html=True,
                )
                if st.button("Open", key=f"qa_{target}_{label}", use_container_width=True):
                    st.session_state.page = target
                    st.rerun()

    # ---- Right column: memory ring + recent chats + model/lang ----
    with right:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="sub-heading">{icon('memory', 16)} Memory Status</div>
                <div class="ring-wrap">
                    <div class="ring-pct" style="color:#38bdf8;">{stats['pct']}%</div>
                    <div>
                        <div class="small muted">Memory Usage</div>
                        <div style="font-weight:700;color:#34d399;">Good</div>
                        <div class="small muted">{stats['used']} / {stats['capacity']} items</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        recent = st.session_state.get("recent_chats", [
            ("AI in Healthcare", "2m ago"),
            ("Python Code Help", "1h ago"),
            ("Climate Change Report", "3h ago"),
            ("Image Generation", "5h ago"),
        ])
        rows = "".join(
            f"""<div class="flex-between" style="padding:6px 0;border-bottom:1px solid var(--border-soft);">
                    <span class="small">{icon('chat', 13, '#818cf8')} {title}</span>
                    <span class="small muted">{t}</span>
                </div>"""
            for title, t in recent
        )
        st.markdown(
            f"""<div class="glass-card"><div class="sub-heading">{icon('chat', 16)} Recent Chats</div>{rows}</div>""",
            unsafe_allow_html=True,
        )
        st.write("")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"<div class='sub-heading'>{icon('sparkle', 16)} Model</div>", unsafe_allow_html=True)
        st.selectbox("Model", ["GPT-4o", "GPT-4o-mini", "Claude", "Llama-3"], label_visibility="collapsed", key="model_choice")
        st.markdown(f"<div class='sub-heading' style='margin-top:12px;'>{icon('globe', 16)} Language</div>", unsafe_allow_html=True)
        st.selectbox("Language", ["Auto Detect", "English", "Spanish", "French", "Chinese", "Hindi", "Nepali"],
                     label_visibility="collapsed", key="lang_choice")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Powerful features grid ----
    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">POWERFUL FEATURES</div>', unsafe_allow_html=True)
    grid_cols = st.columns(5)
    for i, (ic, title, sub, target) in enumerate(FEATURES):
        with grid_cols[i % 5]:
            color_cls = TILE_COLORS[i % len(TILE_COLORS)]
            st.markdown(
                f"""<div class="feature-tile {color_cls}" style="animation-delay:{i * 0.05:.2f}s;">
                        <div class="feature-icon-wrap">{icon(ic, 22)}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-sub">{sub}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
            if st.button("Try it", key=f"feat_{target}_{i}", use_container_width=True):
                st.session_state.page = target
                st.rerun()
        if i % 5 == 4 and i != len(FEATURES) - 1:
            st.write("")
            grid_cols = st.columns(5)

    st.markdown(
        """<div class="lucy-footer">Designed by <span class="credit">Kandel Sanjaya</span> &nbsp;·&nbsp;
        Built with Streamlit, Python, LangChain, ChromaDB, OpenAI, and more ❤️</div>""",
        unsafe_allow_html=True,
    )