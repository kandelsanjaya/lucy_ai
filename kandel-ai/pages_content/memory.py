import streamlit as st
from utils.icons import icon
from utils.helpers import get_memory, add_memory_item, memory_usage_stats

CATEGORIES = [
    ("preferences", "User Preferences", "user"),
    ("chat_log", "Chat History", "chat"),
    ("documents_notes", "Uploaded Documents", "documents"),
    ("notes", "Important Notes", "sparkle"),
]


def render(user):
    st.markdown(f"<div class='sub-heading' style='font-size:1.2rem;'>{icon('memory', 20)} Memory & Personalization</div>",
                unsafe_allow_html=True)

    stats = memory_usage_stats()
    st.progress(stats["pct"] / 100, text=f"Memory usage: {stats['used']} / {stats['capacity']} items ({stats['pct']}%)")

    new_note = st.text_input("Add something for Lucy to remember", placeholder="e.g. I prefer concise answers")
    if st.button("💾 Save to memory", type="primary") and new_note:
        add_memory_item("notes", new_note)
        st.success("Saved!")
        st.rerun()

    st.markdown('<hr class="lucy-divider">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (key, label, ic) in enumerate(CATEGORIES):
        items = get_memory(key)
        with cols[i % 2]:
            st.markdown(f"<div class='sub-heading'>{icon(ic, 16)} {label}</div>", unsafe_allow_html=True)
            if items:
                for it in items[-6:][::-1]:
                    txt = it["text"] if isinstance(it, dict) else it
                    st.markdown(f"""<div class="glass-card" style="padding:10px 14px;margin-bottom:6px;">
                                    <span class="small">{txt}</span></div>""", unsafe_allow_html=True)
            else:
                st.caption("Nothing here yet.")
