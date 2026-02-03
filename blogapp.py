import streamlit as st
import json
import os
from datetime import datetime
from uuid import uuid4
import math

# -----------------------------
# KONFIG
# -----------------------------
DATA_FILE = "blog_data.json"
IMAGE_DIR = "images"

ADMIN_EMAIL = "david@test.test"
ADMIN_PASSWORD = "123456"

os.makedirs(IMAGE_DIR, exist_ok=True)

st.set_page_config(page_title="Mein Blog", page_icon="✎", layout="wide")

# -----------------------------
# LOKALER SPEICHER
# -----------------------------
def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

posts = load_posts()

# -----------------------------
# SESSION STATE
# -----------------------------
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "◻"
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Dark Mode default

# -----------------------------
# GLOBAL FONTS & BASE CSS
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;700&family=Cinzel:wght@600;700&family=Montserrat:wght@300;400;500;600&display=swap');

    html, body, .stApp {
        font-family: 'Montserrat', sans-serif;
    }

    .hero-wrapper {
        overflow: hidden;
        display: inline-block;
    }

    .hero-title {
        font-family: 'Cinzel', serif;
        font-size: 2.4rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 6px;
        transform: translateY(100%);
        filter: blur(6px);
        opacity: 0;
        animation: slideUp 1.1s cubic-bezier(0.19, 1, 0.22, 1) forwards;
    }

    @keyframes slideUp {
        0% { transform: translateY(100%); filter: blur(6px); opacity: 0; }
        60% { filter: blur(2px); opacity: 1; }
        100% { transform: translateY(0%); filter: blur(0); opacity: 1; }
    }

    .hero-sub {
        font-family: 'EB Garamond', serif;
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 4px;
    }

    .post-card {
        padding: 18px 20px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
    }

    .post-title {
        font-family: 'Cinzel', serif;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 4px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .post-meta {
        font-size: 0.8rem;
        color: #6b7280;
        margin-bottom: 12px;
    }

    .post-content {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.95rem;
        line-height: 1.7;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0 16px 0;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 10px;
    }

    .top-nav-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .top-nav-title {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .badge {
        display:inline-block;
        padding:2px 10px;
        border-radius:999px;
        font-size:0.7rem;
        border:1px solid #d1d5db;
        color:#4b5563;
    }

    .login-label {
        font-family: 'EB Garamond', serif;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }

    .chip {
        display:inline-block;
        padding:2px 10px;
        border-radius:999px;
        font-size:0.75rem;
        border:1px solid #d1d5db;
        margin-right:4px;
        margin-bottom:4px;
    }

    .chip-category {
        background: rgba(15,23,42,0.04);
    }

    .chip-tag {
        background: rgba(148,163,184,0.12);
    }

    .stButton button {
        border-radius: 999px;
        padding: 0.4rem 1.2rem;
        font-size: 0.9rem;
        border: 1px solid #111827;
        background: #111827;
        color: #f9fafb;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: #000000;
        color: #ffffff;
        border-color: #000000;
    }

    .stRadio label {
        font-family: 'EB Garamond', serif;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# DARK / LIGHT MODE
# -----------------------------
st.session_state.dark_mode = st.sidebar.toggle("Dark Mode", value=st.session_state.dark_mode)

if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        body, .stApp { background-color: #05070b !important; color: #f9fafb !important; }
        .post-card { background-color: #111827 !important; border-color: #1f2937 !important; }
        .post-meta { color: #9ca3af !important; }
        .top-nav { border-bottom-color: #1f2937 !important; }
        .stRadio label { color: #e5e7eb !important; }
        .hero-sub { color: #9ca3af !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        body, .stApp { background-color: #f5f5f7 !important; color: #111827 !important; }
        .post-card { background-color: #ffffff !important; border-color: #e5e7eb !important; }
        .post-meta { color: #6b7280 !important; }
        .top-nav { border-bottom-color: #e5e7eb !important; }
        .stRadio label { color: #111827 !important; }
        .hero-sub { color: #6b7280 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# LOGIN / LOGOUT
# -----------------------------
def login_screen():
    st.markdown(
        """
        <div style="text-align:center; margin-top:40px; margin-bottom:30px;">
            <div class="hero-wrapper">
                <div class="hero-title">DEIN BLOG</div>
            </div>
            <p class="hero-sub">Schreiben · Lesen · Denken – minimal und klar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="login-label">Modus wählen</p>', unsafe_allow_html=True)
    choice = st.radio("", ["Als Besucher fortfahren", "Einloggen"])

    if choice == "Als Besucher fortfahren":
        st.markdown('<p class="login-label">Als Besucher fortfahren</p>', unsafe_allow_html=True)
        if st.button("Weiter als Besucher", use_container_width=False):
            st.session_state.role = "visitor"
            st.session_state.user_name = "Besucher"
            st.session_state.user_avatar = "◻"
            st.rerun()  # Login-Seite komplett verlassen
    else:
        st.markdown('<p class="login-label">Einloggen</p>', unsafe_allow_html=True)
        email = st.text_input("E-Mail")
        pw = st.text_input("Passwort", type="password")
        st.markdown('<p class="login-label">Anzeigename</p>', unsafe_allow_html=True)
        name = st.text_input("", key="login_name")
        st.markdown('<p class="login-label">Avatar (einfaches Symbol)</p>', unsafe_allow_html=True)
        avatar = st.text_input("", value="◻", key="login_avatar")

        if st.button("Login", use_container_width=False):
            if email == ADMIN_EMAIL and pw == ADMIN_PASSWORD:
                st.session_state.role = "admin"
                st.session_state.user_name = name or "Admin"
                st.session_state.user_avatar = avatar or "◆"
            else:
                st.session_state.role = "user"
                st.session_state.user_name = name or "User"
                st.session_state.user_avatar = avatar or "◻"
            st.rerun()  # Login-Seite komplett verlassen

def logout():
    st.session_state.role = None
    st.session_state.user_name = None
    st.session_state.user_avatar = "◻"
    st.session_state.edit_post_id = None

# -----------------------------
# LOGIN FLOW
# -----------------------------
if st.session_state.role is None:
    login_screen()
    st.stop()

# -----------------------------
# SIDEBAR: PROFIL, FILTER, ABOUT
# -----------------------------
st.sidebar.markdown("### Profil")
st.sidebar.write(f"{st.session_state.user_avatar} **{st.session_state.user_name}**")
st.sidebar.write(f"Rolle: `{st.session_state.role}`")

if st.sidebar.button("Logout", use_container_width=True):
    logout()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Filter")

search_query = st.sidebar.text_input("Suche im Titel/Inhalt")
category_filter = st.sidebar.text_input("Kategorie")
posts_per_page = st.sidebar.slider("Beiträge pro Seite", 1, 10, 3)

st.sidebar.markdown("---")
st.sidebar.markdown("### Über diesen Blog")
st.sidebar.caption(
    "Ein ruhiger Ort für Gedanken, Geschichten und Experimente. "
    "Minimalistisch, lesbar, ohne Ablenkung."
)

st.sidebar.markdown("---")
if posts:
    top_liked = sorted(posts, key=lambda p: p.get("likes", 0), reverse=True)[:3]
    st.sidebar.markdown("### Beliebteste Beiträge")
    if top_liked:
        for p in top_liked:
            st.sidebar.write(f"{p.get('likes',0)} × ❤ – {p['title']}")
    else:
        st.sidebar.caption("Noch keine Likes.")
else:
    st.sidebar.caption("Noch keine Beiträge vorhanden.")

# -----------------------------
# TOP NAVBAR
# -----------------------------
col_nav_left, col_nav_right = st.columns([3, 2])

with col_nav_left:
    st.markdown(
        f"""
        <div class="top-nav">
            <div class="top-nav-left">
                <span class="top-nav-title">BLOG</span>
                <span class="badge">{'ADMIN' if st.session_state.role=='admin' else ('USER' if st.session_state.role=='user' else 'VISITOR')}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_nav_right:
    pass

# -----------------------------
# TABS
# -----------------------------
tabs = ["Beiträge", "Dashboard"]
if st.session_state.role == "admin":
    tabs.append("Neuer Beitrag")
    tabs.append("Admin Panel")

tab_objects = st.tabs(tabs)

# -----------------------------
# HILFSFUNKTIONEN
# -----------------------------
def filter_posts(posts, query, category):
    result = posts
    if query:
        q = query.lower()
        result = [p for p in result if q in p["title"].lower() or q in p["content"].lower()]
    if category:
        c = category.lower()
        result = [p for p in result if p.get("category", "").lower() == c]
    return result

def like_post(post):
    post.setdefault("likes", 0)
    post["likes"] += 1
    save_posts(posts)

def estimate_reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, math.ceil(words / 200))

def render_post_card(post):
    st.markdown('<div class="post-card">', unsafe_allow_html=True)

    if post.get("image_path") and os.path.exists(post["image_path"]):
        st.image(post["image_path"], width=420)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='post-title'>{post['title'].upper()}</div>", unsafe_allow_html=True)

    reading_time = estimate_reading_time(post["content"])
    meta_text = f"{post['date']} • {reading_time} Min. Lesezeit"
    st.markdown(
        f"<div class='post-meta'>{meta_text}</div>",
        unsafe_allow_html=True,
    )

    chips_html = ""
    if post.get("category"):
        chips_html += f"<span class='chip chip-category'>{post['category']}</span>"
    for t in post.get("tags", []):
        chips_html += f"<span class='chip chip-tag'>{t}</span>"
    if chips_html:
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='post-content'>{post['content']}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.session_state.role in ["admin", "user"]:
            if st.button(f"❤ {post.get('likes',0)}", key=f"like_{post['id']}"):
                like_post(post)
                st.rerun()
        else:
            st.caption(f"{post.get('likes',0)} × ❤")
    with col2:
        export_text = f"# {post['title']}\n\n{post['content']}"
        st.download_button("Export", export_text, file_name=f"{post['title']}.md", key=f"exp_{post['id']}")
    with col3:
        tags = ", ".join(post.get("tags", [])) or "–"
        st.caption(f"Tags: {tags}")

    st.markdown("**Kommentare**")
    comments = post.get("comments", [])
    if not comments:
        st.caption("_Noch keine Kommentare._")
    else:
        for c in comments:
            st.markdown(f"- {c.get('avatar','◻')} **{c['author']}**: {c['text']}")

    if st.session_state.role in ["admin", "user"]:
        with st.expander("Kommentar schreiben"):
            author = st.text_input("Name", value=st.session_state.user_name, key=f"c_author_{post['id']}")
            avatar = st.text_input("Avatar", value=st.session_state.user_avatar, key=f"c_avatar_{post['id']}")
            text = st.text_area("Kommentar", key=f"c_text_{post['id']}")

            if st.button("Kommentar speichern", key=f"c_save_{post['id']}"):
                if author.strip() and text.strip():
                    post.setdefault("comments", []).append(
                        {
                            "author": author,
                            "avatar": avatar or "◻",
                            "text": text,
                            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                        }
                    )
                    save_posts(posts)
                    st.rerun()
                else:
                    st.error("Bitte Name und Kommentar eingeben.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")

# -----------------------------
# TAB: BEITRÄGE
# -----------------------------
with tab_objects[0]:
    st.markdown("### Beiträge")

    filtered = filter_posts(posts, search_query, category_filter)
    filtered = list(reversed(filtered))

    if not filtered:
        st.info("Noch keine Beiträge vorhanden.")
    else:
        total = len(filtered)
        total_pages = max(1, (total - 1) // posts_per_page + 1)
        page = st.number_input("Seite", min_value=1, max_value=total_pages, value=1, step=1)

        start = (page - 1) * posts_per_page
        end = start + posts_per_page

        st.caption(f"Seite {page} von {total_pages} • {total} Beiträge")

        for post in filtered[start:end]:
            render_post_card(post)

# -----------------------------
# TAB: DASHBOARD
# -----------------------------
with tab_objects[1]:
    st.markdown("### Dashboard")

    total_posts = len(posts)
    total_comments = sum(len(p.get("comments", [])) for p in posts)
    total_likes = sum(p.get("likes", 0) for p in posts)

    c1, c2, c3 = st.columns(3)
    c1.metric("Beiträge", total_posts)
    c2.metric("Kommentare", total_comments)
    c3.metric("Likes gesamt", total_likes)

    st.markdown("---")
    st.markdown("#### Letzte Beiträge")
    for p in list(reversed(posts))[:5]:
        rt = estimate_reading_time(p["content"])
        st.write(f"- {p['title']} ({p['date']}) – {p.get('likes',0)} × ❤ – {rt} Min.")

# -----------------------------
# TAB: NEUER BEITRAG (Admin)
# -----------------------------
if st.session_state.role == "admin" and len(tab_objects) > 2:
    with tab_objects[2]:
        st.markdown("### Neuer Beitrag")

        title = st.text_input("Titel")
        category = st.text_input("Kategorie")
        tags = st.text_input("Tags (kommagetrennt)")
        content = st.text_area("Inhalt", height=220)
        image_file = st.file_uploader("Bild", type=["png", "jpg", "jpeg"])

        if st.button("Beitrag speichern"):
            if not title.strip() or not content.strip():
                st.error("Titel und Inhalt sind erforderlich.")
            else:
                image_path = None
                if image_file:
                    ext = os.path.splitext(image_file.name)[1]
                    img_name = f"{uuid4().hex}{ext}"
                    image_path = os.path.join(IMAGE_DIR, img_name)
                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())

                new_post = {
                    "id": uuid4().hex,
                    "title": title,
                    "content": content,
                    "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "category": category,
                    "tags": [t.strip() for t in tags.split(",") if t.strip()],
                    "image_path": image_path,
                    "comments": [],
                    "likes": 0,
                }
                posts.append(new_post)
                save_posts(posts)
                st.success("Beitrag gespeichert!")

# -----------------------------
# TAB: ADMIN PANEL (Admin)
# -----------------------------
if st.session_state.role == "admin" and len(tab_objects) > 3:
    with tab_objects[3]:
        st.markdown("### Admin Panel")

        if not posts:
            st.info("Noch keine Beiträge vorhanden.")
        else:
            for post in posts:
                st.markdown(f"**{post['title']}** – {post['date']} – {post.get('likes',0)} × ❤")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Löschen", key=f"del_{post['id']}"):
                        posts.remove(post)
                        save_posts(posts)
                        st.rerun()
                with col2:
                    if st.button("Bearbeiten", key=f"edit_{post['id']}"):
                        st.session_state.edit_post_id = post["id"]
                        st.rerun()

            if st.session_state.edit_post_id:
                post = next((p for p in posts if p["id"] == st.session_state.edit_post_id), None)
                if post:
                    st.markdown("---")
                    st.markdown("#### Beitrag bearbeiten")
                    new_title = st.text_input("Titel", value=post["title"])
                    new_category = st.text_input("Kategorie", value=post.get("category", ""))
                    new_tags = st.text_input("Tags", value=", ".join(post.get("tags", [])))
                    new_content = st.text_area("Inhalt", value=post["content"], height=220)

                    if st.button("Änderungen speichern"):
                        post["title"] = new_title
                        post["category"] = new_category
                        post["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
                        post["content"] = new_content
                        save_posts(posts)
                        st.success("Beitrag aktualisiert.")
                        st.session_state.edit_post_id = None
                        st.rerun()
                else:
                    st.session_state.edit_post_id = None
