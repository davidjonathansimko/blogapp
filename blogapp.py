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
if "selected_post_id" not in st.session_state:
    st.session_state.selected_post_id = None

# -----------------------------
# SPRACHEN
# -----------------------------
TEXTS = {
    "de": {
        "app_title": "Blog",
        "hero_title": "DEIN BLOG",
        "hero_sub": "Schreiben · Lesen · Denken – minimal und klar.",
        "mode_choose": "Modus wählen",
        "continue_visitor": "Als Besucher fortfahren",
        "login": "Einloggen",
        "email": "E-Mail",
        "password": "Passwort",
        "display_name": "Anzeigename",
        "avatar_label": "Avatar (einfaches Symbol)",
        "visitor": "Besucher",
        "admin": "Admin",
        "user": "User",
        "role": "Rolle",
        "logout": "Logout",
        "profile": "Profil",
        "filter": "Filter",
        "search": "Suche im Titel/Inhalt",
        "category": "Kategorie",
        "collection": "Kollektion",
        "collection_filter": "Kollektion filtern",
        "posts_per_page": "Beiträge pro Seite",
        "about_blog_title": "Über diesen Blog",
        "about_blog_text": "Ein ruhiger Ort für Gedanken, Geschichten und Experimente. Minimalistisch, lesbar, ohne Ablenkung.",
        "popular_posts": "Beliebteste Beiträge",
        "no_likes_yet": "Noch keine Likes.",
        "no_posts_yet": "Noch keine Beiträge vorhanden.",
        "posts_tab": "Beiträge",
        "dashboard_tab": "Dashboard",
        "new_post_tab": "Neuer Beitrag",
        "admin_panel_tab": "Admin Panel",
        "posts_heading": "Beiträge",
        "page_info": "Seite {page} von {total_pages} • {total} Beiträge",
        "reading_time": "{minutes} Min. Lesezeit",
        "comments": "Kommentare",
        "no_comments": "Noch keine Kommentare.",
        "comment_name": "Name",
        "comment_avatar": "Avatar",
        "comment_text": "Kommentar",
        "comment_save": "Kommentar speichern",
        "comment_error": "Bitte Name und Kommentar eingeben.",
        "export": "Export",
        "tags_label": "Tags",
        "likes_total": "Likes gesamt",
        "posts_total": "Beiträge",
        "comments_total": "Kommentare",
        "latest_posts": "Letzte Beiträge",
        "new_post_heading": "Neuer Beitrag",
        "title": "Titel",
        "tags": "Tags (kommagetrennt)",
        "content": "Inhalt",
        "image": "Bild",
        "save_post": "Beitrag speichern",
        "title_content_required": "Titel und Inhalt sind erforderlich.",
        "post_saved": "Beitrag gespeichert!",
        "admin_panel_heading": "Admin Panel",
        "delete": "Löschen",
        "edit": "Bearbeiten",
        "edit_post_heading": "Beitrag bearbeiten",
        "save_changes": "Änderungen speichern",
        "post_updated": "Beitrag aktualisiert.",
        "language": "Sprache",
        "german": "Deutsch",
        "english": "Englisch",
        "read_more": "Lesen",
        "back": "Zurück",
        "full_view": "Beitrag",
        "status": "Status",
        "status_published": "Veröffentlicht",
        "status_draft": "Entwurf",
        "seo_description": "SEO Beschreibung",
        "seo_keywords": "SEO Keywords (kommagetrennt)",
        "accent_color": "Akzentfarbe (z.B. #ffcc00)",
        "show_drafts": "Entwürfe anzeigen (nur Admin)",
    },
    "en": {
        "app_title": "Blog",
        "hero_title": "YOUR BLOG",
        "hero_sub": "Write · Read · Think – minimal and clear.",
        "mode_choose": "Choose mode",
        "continue_visitor": "Continue as visitor",
        "login": "Log in",
        "email": "Email",
        "password": "Password",
        "display_name": "Display name",
        "avatar_label": "Avatar (simple symbol)",
        "visitor": "Visitor",
        "admin": "Admin",
        "user": "User",
        "role": "Role",
        "logout": "Logout",
        "profile": "Profile",
        "filter": "Filter",
        "search": "Search in title/content",
        "category": "Category",
        "collection": "Collection",
        "collection_filter": "Filter by collection",
        "posts_per_page": "Posts per page",
        "about_blog_title": "About this blog",
        "about_blog_text": "A quiet place for thoughts, stories and experiments. Minimal, readable, distraction-free.",
        "popular_posts": "Most liked posts",
        "no_likes_yet": "No likes yet.",
        "no_posts_yet": "No posts yet.",
        "posts_tab": "Posts",
        "dashboard_tab": "Dashboard",
        "new_post_tab": "New post",
        "admin_panel_tab": "Admin panel",
        "posts_heading": "Posts",
        "page_info": "Page {page} of {total_pages} • {total} posts",
        "reading_time": "{minutes} min read",
        "comments": "Comments",
        "no_comments": "No comments yet.",
        "comment_name": "Name",
        "comment_avatar": "Avatar",
        "comment_text": "Comment",
        "comment_save": "Save comment",
        "comment_error": "Please enter name and comment.",
        "export": "Export",
        "tags_label": "Tags",
        "likes_total": "Total likes",
        "posts_total": "Posts",
        "comments_total": "Comments",
        "latest_posts": "Latest posts",
        "new_post_heading": "New post",
        "title": "Title",
        "tags": "Tags (comma separated)",
        "content": "Content",
        "image": "Image",
        "save_post": "Save post",
        "title_content_required": "Title and content are required.",
        "post_saved": "Post saved!",
        "admin_panel_heading": "Admin panel",
        "delete": "Delete",
        "edit": "Edit",
        "edit_post_heading": "Edit post",
        "save_changes": "Save changes",
        "post_updated": "Post updated.",
        "language": "Language",
        "german": "German",
        "english": "English",
        "read_more": "Read",
        "back": "Back",
        "full_view": "Post",
        "status": "Status",
        "status_published": "Published",
        "status_draft": "Draft",
        "seo_description": "SEO description",
        "seo_keywords": "SEO keywords (comma separated)",
        "accent_color": "Accent color (e.g. #ffcc00)",
        "show_drafts": "Show drafts (admin only)",
    },
}

if "lang" not in st.session_state:
    st.session_state.lang = "de"

# -----------------------------
# SPRACHAUSWAHL
# -----------------------------
lang_choice = st.sidebar.selectbox(
    TEXTS[st.session_state.lang]["language"],
    (("de", TEXTS["de"]["german"]), ("en", TEXTS["en"]["english"])),
    format_func=lambda x: x[1],
)
st.session_state.lang = lang_choice[0]
T = TEXTS[st.session_state.lang]

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
        position: relative;
        overflow: hidden;
    }

    .post-card-accent {
        position:absolute;
        top:0;
        left:0;
        height:4px;
        width:100%;
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

    .chip-collection {
        background: rgba(59,130,246,0.12);
        border-color: rgba(59,130,246,0.4);
    }

    .chip-status-draft {
        background: rgba(248, 113, 113, 0.12);
        border-color: rgba(248, 113, 113, 0.5);
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
        f"""
        <div style="text-align:center; margin-top:40px; margin-bottom:30px;">
            <div class="hero-wrapper">
                <div class="hero-title">{T['hero_title']}</div>
            </div>
            <p class="hero-sub">{T['hero_sub']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"<p class='login-label'>{T['mode_choose']}</p>", unsafe_allow_html=True)
    choice = st.radio("", [T["continue_visitor"], T["login"]])

    if choice == T["continue_visitor"]:
        st.markdown(f"<p class='login-label'>{T['continue_visitor']}</p>", unsafe_allow_html=True)
        if st.button(T["continue_visitor"], use_container_width=False):
            st.session_state.role = "visitor"
            st.session_state.user_name = T["visitor"]
            st.session_state.user_avatar = "◻"
            st.rerun()
    else:
        st.markdown(f"<p class='login-label'>{T['login']}</p>", unsafe_allow_html=True)
        email = st.text_input(T["email"])
        pw = st.text_input(T["password"], type="password")
        st.markdown(f"<p class='login-label'>{T['display_name']}</p>", unsafe_allow_html=True)
        name = st.text_input("", key="login_name")
        st.markdown(f"<p class='login-label'>{T['avatar_label']}</p>", unsafe_allow_html=True)
        avatar = st.text_input("", value="◻", key="login_avatar")

        if st.button(T["login"], use_container_width=False):
            if email == ADMIN_EMAIL and pw == ADMIN_PASSWORD:
                st.session_state.role = "admin"
                st.session_state.user_name = name or T["admin"]
                st.session_state.user_avatar = avatar or "◆"
            else:
                st.session_state.role = "user"
                st.session_state.user_name = name or T["user"]
                st.session_state.user_avatar = avatar or "◻"
            st.rerun()

def logout():
    st.session_state.role = None
    st.session_state.user_name = None
    st.session_state.user_avatar = "◻"
    st.session_state.edit_post_id = None
    st.session_state.selected_post_id = None

# -----------------------------
# LOGIN FLOW
# -----------------------------
if st.session_state.role is None:
    login_screen()
    st.stop()

# -----------------------------
# SIDEBAR: PROFIL, FILTER, ABOUT
# -----------------------------
st.sidebar.markdown(f"### {T['profile']}")
st.sidebar.write(f"{st.session_state.user_avatar} **{st.session_state.user_name}**")
st.sidebar.write(f"{T['role']}: `{st.session_state.role}`")

if st.sidebar.button(T["logout"], use_container_width=True):
    logout()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {T['filter']}")

search_query = st.sidebar.text_input(T["search"])
category_filter = st.sidebar.text_input(T["category"])
collection_filter = st.sidebar.text_input(T["collection_filter"])
posts_per_page = st.sidebar.slider(T["posts_per_page"], 1, 10, 3)

show_drafts = False
if st.session_state.role == "admin":
    show_drafts = st.sidebar.checkbox(T["show_drafts"], value=False)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {T['about_blog_title']}")
st.sidebar.caption(T["about_blog_text"])

st.sidebar.markdown("---")
if posts:
    top_liked = sorted(posts, key=lambda p: p.get("likes", 0), reverse=True)[:3]
    st.sidebar.markdown(f"### {T['popular_posts']}")
    if top_liked:
        for p in top_liked:
            st.sidebar.write(f"{p.get('likes',0)} × ❤ – {p['title']}")
    else:
        st.sidebar.caption(T["no_likes_yet"])
else:
    st.sidebar.caption(T["no_posts_yet"])

# -----------------------------
# TOP NAVBAR
# -----------------------------
col_nav_left, col_nav_right = st.columns([3, 2])

with col_nav_left:
    role_label = (
        T["admin"] if st.session_state.role == "admin"
        else (T["user"] if st.session_state.role == "user" else T["visitor"])
    )
    st.markdown(
        f"""
        <div class="top-nav">
            <div class="top-nav-left">
                <span class="top-nav-title">{T['app_title'].upper()}</span>
                <span class="badge">{role_label.upper()}</span>
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
tabs = [T["posts_tab"], T["dashboard_tab"]]
if st.session_state.role == "admin":
    tabs.append(T["new_post_tab"])
    tabs.append(T["admin_panel_tab"])

tab_objects = st.tabs(tabs)

# -----------------------------
# HILFSFUNKTIONEN
# -----------------------------
def filter_posts(posts, query, category, collection, show_drafts, is_admin):
    result = posts
    if not show_drafts or not is_admin:
        result = [p for p in result if p.get("status", "published") == "published"]
    if query:
        q = query.lower()
        result = [p for p in result if q in p["title"].lower() or q in p["content"].lower()]
    if category:
        c = category.lower()
        result = [p for p in result if p.get("category", "").lower() == c]
    if collection:
        col = collection.lower()
        result = [p for p in result if p.get("collection", "").lower() == col]
    return result

def like_post(post):
    post.setdefault("likes", 0)
    post["likes"] += 1
    save_posts(posts)

def estimate_reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, math.ceil(words / 200))

def get_accent_color(post):
    color = post.get("accent_color", "").strip()
    if not color:
        return "#4b5563"
    return color

def render_post_card(post):
    accent = get_accent_color(post)
    st.markdown(
        f"<div class='post-card'><div class='post-card-accent' style='background:{accent};'></div>",
        unsafe_allow_html=True,
    )

    if post.get("image_path") and os.path.exists(post["image_path"]):
        st.image(post["image_path"], width=420)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    col_title, col_read = st.columns([4, 1])
    with col_title:
        st.markdown(f"<div class='post-title'>{post['title'].upper()}</div>", unsafe_allow_html=True)
    with col_read:
        if st.button(T["read_more"], key=f"read_{post['id']}"):
            st.session_state.selected_post_id = post["id"]
            st.rerun()

    reading_time = estimate_reading_time(post["content"])
    meta_text = T["reading_time"].format(minutes=reading_time)
    meta_full = f"{post['date']} • {meta_text}"
    st.markdown(
        f"<div class='post-meta'>{meta_full}</div>",
        unsafe_allow_html=True,
    )

    chips_html = ""
    if post.get("category"):
        chips_html += f"<span class='chip chip-category'>{post['category']}</span>"
    if post.get("collection"):
        chips_html += f"<span class='chip chip-collection'>{post['collection']}</span>"
    for t in post.get("tags", []):
        chips_html += f"<span class='chip chip-tag'>{t}</span>"
    if post.get("status", "published") == "draft":
        chips_html += f"<span class='chip chip-status-draft'>{T['status_draft']}</span>"
    if chips_html:
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    preview = post["content"]
    if len(preview) > 260:
        preview = preview[:260].rstrip() + " …"
    st.markdown(f"<div class='post-content'>{preview}</div>", unsafe_allow_html=True)

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
        st.download_button(T["export"], export_text, file_name=f"{post['title']}.md", key=f"exp_{post['id']}")
    with col3:
        tags = ", ".join(post.get("tags", [])) or "–"
        st.caption(f"{T['tags_label']}: {tags}")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")

def render_full_post(post):
    accent = get_accent_color(post)
    st.markdown("### " + T["full_view"])
    if st.button("← " + T["back"]):
        st.session_state.selected_post_id = None
        st.rerun()

    st.markdown(
        f"<div class='post-card'><div class='post-card-accent' style='background:{accent};'></div>",
        unsafe_allow_html=True,
    )

    if post.get("image_path") and os.path.exists(post["image_path"]):
        st.image(post["image_path"], width=520)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='post-title'>{post['title'].upper()}</div>", unsafe_allow_html=True)

    reading_time = estimate_reading_time(post["content"])
    meta_text = T["reading_time"].format(minutes=reading_time)
    meta_full = f"{post['date']} • {meta_text}"
    st.markdown(
        f"<div class='post-meta'>{meta_full}</div>",
        unsafe_allow_html=True,
    )

    chips_html = ""
    if post.get("category"):
        chips_html += f"<span class='chip chip-category'>{post['category']}</span>"
    if post.get("collection"):
        chips_html += f"<span class='chip chip-collection'>{post['collection']}</span>"
    for t in post.get("tags", []):
        chips_html += f"<span class='chip chip-tag'>{t}</span>"
    if post.get("status", "published") == "draft":
        chips_html += f"<span class='chip chip-status-draft'>{T['status_draft']}</span>"
    if chips_html:
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='post-content'>{post['content']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.session_state.role in ["admin", "user"]:
            if st.button(f"❤ {post.get('likes',0)}", key=f"like_full_{post['id']}"):
                like_post(post)
                st.rerun()
        else:
            st.caption(f"{post.get('likes',0)} × ❤")
    with col2:
        export_text = f"# {post['title']}\n\n{post['content']}"
        st.download_button(T["export"], export_text, file_name=f"{post['title']}.md", key=f"exp_full_{post['id']}")

    st.markdown("**" + T["comments"] + "**")
    comments = post.get("comments", [])
    if not comments:
        st.caption("_" + T["no_comments"] + "_")
    else:
        for c in comments:
            st.markdown(f"- {c.get('avatar','◻')} **{c['author']}**: {c['text']}")

    if st.session_state.role in ["admin", "user"]:
        with st.expander(T["comment_text"]):
            author = st.text_input(T["comment_name"], value=st.session_state.user_name, key=f"c_author_full_{post['id']}")
            avatar = st.text_input(T["comment_avatar"], value=st.session_state.user_avatar, key=f"c_avatar_full_{post['id']}")
            text = st.text_area(T["comment_text"], key=f"c_text_full_{post['id']}")

            if st.button(T["comment_save"], key=f"c_save_full_{post['id']}"):
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
                    st.error(T["comment_error"])

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")

# -----------------------------
# TAB: BEITRÄGE
# -----------------------------
with tab_objects[0]:
    st.markdown("### " + T["posts_heading"])

    if st.session_state.selected_post_id:
        post = next((p for p in posts if p["id"] == st.session_state.selected_post_id), None)
        if post:
            render_full_post(post)
        else:
            st.session_state.selected_post_id = None
            st.info(T["no_posts_yet"])
    else:
        filtered = filter_posts(
            posts,
            search_query,
            category_filter,
            collection_filter,
            show_drafts,
            st.session_state.role == "admin",
        )
        filtered = list(reversed(filtered))

        if not filtered:
            st.info(T["no_posts_yet"])
        else:
            total = len(filtered)
            total_pages = max(1, (total - 1) // posts_per_page + 1)
            page = st.number_input("Seite", min_value=1, max_value=total_pages, value=1, step=1)

            start = (page - 1) * posts_per_page
            end = start + posts_per_page

            st.caption(T["page_info"].format(page=page, total_pages=total_pages, total=total))

            for post in filtered[start:end]:
                render_post_card(post)

# -----------------------------
# TAB: DASHBOARD
# -----------------------------
with tab_objects[1]:
    st.markdown("### " + T["dashboard_tab"])

    total_posts = len(posts)
    total_comments = sum(len(p.get("comments", [])) for p in posts)
    total_likes = sum(p.get("likes", 0) for p in posts)

    c1, c2, c3 = st.columns(3)
    c1.metric(T["posts_total"], total_posts)
    c2.metric(T["comments_total"], total_comments)
    c3.metric(T["likes_total"], total_likes)

    st.markdown("---")
    st.markdown("#### " + T["latest_posts"])
    for p in list(reversed(posts))[:5]:
        rt = estimate_reading_time(p["content"])
        st.write(f"- {p['title']} ({p['date']}) – {p.get('likes',0)} × ❤ – {rt} Min.")

# -----------------------------
# TAB: NEUER BEITRAG (Admin)
# -----------------------------
if st.session_state.role == "admin" and len(tab_objects) > 2:
    with tab_objects[2]:
        st.markdown("### " + T["new_post_heading"])

        title = st.text_input(T["title"])
        category = st.text_input(T["category"])
        collection = st.text_input(T["collection"])
        tags = st.text_input(T["tags"])
        content = st.text_area(T["content"], height=220)
        image_file = st.file_uploader(T["image"], type=["png", "jpg", "jpeg"])

        st.markdown("#### SEO")
        seo_description = st.text_input(T["seo_description"])
        seo_keywords = st.text_input(T["seo_keywords"])

        st.markdown("#### " + T["status"])
        status = st.radio("", [T["status_published"], T["status_draft"]])
        status_value = "published" if status == T["status_published"] else "draft"

        accent_color = st.text_input(T["accent_color"], value="#4b5563")

        if st.button(T["save_post"]):
            if not title.strip() or not content.strip():
                st.error(T["title_content_required"])
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
                    "collection": collection,
                    "tags": [t.strip() for t in tags.split(",") if t.strip()],
                    "image_path": image_path,
                    "comments": [],
                    "likes": 0,
                    "status": status_value,
                    "seo_description": seo_description,
                    "seo_keywords": [k.strip() for k in seo_keywords.split(",") if k.strip()],
                    "accent_color": accent_color,
                }
                posts.append(new_post)
                save_posts(posts)
                st.success(T["post_saved"])

# -----------------------------
# TAB: ADMIN PANEL (Admin)
# -----------------------------
if st.session_state.role == "admin" and len(tab_objects) > 3:
    with tab_objects[3]:
        st.markdown("### " + T["admin_panel_heading"])

        if not posts:
            st.info(T["no_posts_yet"])
        else:
            for post in posts:
                status_label = T["status_published"] if post.get("status", "published") == "published" else T["status_draft"]
                st.markdown(f"**{post['title']}** – {post['date']} – {post.get('likes',0)} × ❤ – _{status_label}_")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(T["delete"], key=f"del_{post['id']}"):
                        posts.remove(post)
                        save_posts(posts)
                        st.rerun()
                with col2:
                    if st.button(T["edit"], key=f"edit_{post['id']}"):
                        st.session_state.edit_post_id = post["id"]
                        st.rerun()

            if st.session_state.edit_post_id:
                post = next((p for p in posts if p["id"] == st.session_state.edit_post_id), None)
                if post:
                    st.markdown("---")
                    st.markdown("#### " + T["edit_post_heading"])
                    new_title = st.text_input(T["title"], value=post["title"])
                    new_category = st.text_input(T["category"], value=post.get("category", ""))
                    new_collection = st.text_input(T["collection"], value=post.get("collection", ""))
                    new_tags = st.text_input(T["tags"], value=", ".join(post.get("tags", [])))
                    new_content = st.text_area(T["content"], value=post["content"], height=220)

                    st.markdown("#### SEO")
                    new_seo_description = st.text_input(T["seo_description"], value=post.get("seo_description", ""))
                    new_seo_keywords = st.text_input(
                        T["seo_keywords"],
                        value=", ".join(post.get("seo_keywords", [])),
                    )

                    st.markdown("#### " + T["status"])
                    current_status = post.get("status", "published")
                    status_radio = st.radio(
                        "",
                        [T["status_published"], T["status_draft"]],
                        index=0 if current_status == "published" else 1,
                        key="edit_status_radio",
                    )
                    new_status_value = "published" if status_radio == T["status_published"] else "draft"

                    new_accent_color = st.text_input(
                        T["accent_color"],
                        value=post.get("accent_color", "#4b5563"),
                    )

                    if st.button(T["save_changes"]):
                        post["title"] = new_title
                        post["category"] = new_category
                        post["collection"] = new_collection
                        post["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
                        post["content"] = new_content
                        post["seo_description"] = new_seo_description
                        post["seo_keywords"] = [k.strip() for k in new_seo_keywords.split(",") if k.strip()]
                        post["status"] = new_status_value
                        post["accent_color"] = new_accent_color
                        save_posts(posts)
                        st.success(T["post_updated"])
                        st.session_state.edit_post_id = None
                        st.rerun()
                else:
                    st.session_state.edit_post_id = None
