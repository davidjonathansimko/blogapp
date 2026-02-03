import streamlit as st
import json
import os
from datetime import datetime
from uuid import uuid4
from textwrap import shorten

# -----------------------------
# KONFIG
# -----------------------------
DATA_FILE = "blog_data.json"
IMAGE_DIR = "images"

ADMIN_EMAIL = "david@test.test"
ADMIN_PASSWORD = "123456"

os.makedirs(IMAGE_DIR, exist_ok=True)

st.set_page_config(page_title="Mein Blog", page_icon="📝", layout="wide")

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
# SESSION STATE INITIALISIERUNG
# -----------------------------
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "🙂"
if "page" not in st.session_state:
    st.session_state.page = "login"
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None

# -----------------------------
# LOGIN / LOGOUT
# -----------------------------
def login_screen():
    st.markdown(
        """
        <h1 style="text-align:center; margin-bottom:20px;">📝 Willkommen im Blog</h1>
        """,
        unsafe_allow_html=True,
    )

    choice = st.radio("Wie möchtest du fortfahren:", ["Als Besucher", "Einloggen"])

    if choice == "Als Besucher":
        if st.button("Weiter als Besucher"):
            st.session_state.role = "visitor"
            st.session_state.user_name = "Besucher"
            st.session_state.user_avatar = "👀"
            st.session_state.page = "app"

    else:
        st.subheader("🔐 Einloggen")
        email = st.text_input("E-Mail")
        pw = st.text_input("Passwort", type="password")
        name = st.text_input("Anzeigename")
        avatar = st.text_input("Avatar (Emoji)", value="🙂")

        if st.button("Login"):
            if email == ADMIN_EMAIL and pw == ADMIN_PASSWORD:
                st.session_state.role = "admin"
                st.session_state.user_name = name or "Admin"
                st.session_state.user_avatar = avatar or "👑"
            else:
                st.session_state.role = "user"
                st.session_state.user_name = name or "User"
                st.session_state.user_avatar = avatar or "🙂"

            st.session_state.page = "app"

def logout():
    st.session_state.role = None
    st.session_state.user_name = None
    st.session_state.user_avatar = "🙂"
    st.session_state.page = "login"
    st.session_state.edit_post_id = None

# -----------------------------
# HAUPT-NAVIGATION
# -----------------------------
if st.session_state.page == "login":
    login_screen()
    st.stop()

# -----------------------------
# DARK MODE + STYLING
# -----------------------------
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

if dark_mode:
    st.markdown("""
        <style>
        body, .stApp { background-color: #0e1117 !important; color: #fafafa !important; }
        .post-card { background-color: #161a23 !important; border: 1px solid #2a2f3a !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp { background-color: #ffffff !important; color: #000000 !important; }
        .post-card { background-color: #ffffff !important; border: 1px solid #e0e0e0 !important; }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📚 Navigation")
st.sidebar.write(f"👤 {st.session_state.user_avatar} {st.session_state.user_name}")
st.sidebar.write(f"Rolle: **{st.session_state.role}**")

if st.sidebar.button("🚪 Logout"):
    logout()
    st.experimental_rerun()

# Menü
if st.session_state.role == "admin":
    menu = st.sidebar.radio("Seite wählen", ["📖 Blog lesen", "✍️ Beitrag erstellen", "⚙️ Admin Panel"])
else:
    menu = st.sidebar.radio("Seite wählen", ["📖 Blog lesen"])

search_query = st.sidebar.text_input("🔍 Suche")
category_filter = st.sidebar.text_input("Kategorie filtern")
posts_per_page = st.sidebar.slider("Beiträge pro Seite", 1, 10, 3)

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

def render_post(post):
    st.markdown('<div class="post-card" style="padding:20px; border-radius:12px;">', unsafe_allow_html=True)

    st.markdown(f"### {post['title']}")
    st.caption(f"{post['date']} • Kategorie: {post.get('category','–')}")

    if post.get("image_path") and os.path.exists(post["image_path"]):
        st.image(post["image_path"], width=350)  # kleiner & schöner

    st.markdown(post["content"])

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.role in ["admin", "user"]:
            if st.button(f"👍 Like ({post.get('likes',0)})", key=f"like_{post['id']}"):
                like_post(post)
                st.experimental_rerun()
        else:
            st.write(f"👍 Likes: {post.get('likes',0)}")

    with col2:
        export_text = f"# {post['title']}\n\n{post['content']}"
        st.download_button("📄 Export", export_text, file_name="post.md")

    st.markdown("### 💬 Kommentare")
    for c in post.get("comments", []):
        st.markdown(f"- {c['avatar']} **{c['author']}**: {c['text']}")

    if st.session_state.role in ["admin", "user"]:
        with st.expander("Kommentar schreiben"):
            author = st.text_input("Name", value=st.session_state.user_name, key=f"a{post['id']}")
            avatar = st.text_input("Avatar", value=st.session_state.user_avatar, key=f"b{post['id']}")
            text = st.text_area("Kommentar", key=f"c{post['id']}")

            if st.button("Speichern", key=f"d{post['id']}"):
                post.setdefault("comments", []).append({
                    "author": author,
                    "avatar": avatar,
                    "text": text,
                    "date": datetime.now().strftime("%d.%m.%Y %H:%M")
                })
                save_posts(posts)
                st.experimental_rerun()

    st.markdown("</div><br>", unsafe_allow_html=True)

# -----------------------------
# BLOG LESEN
# -----------------------------
if menu == "📖 Blog lesen":
    st.markdown("## 📖 Blog Übersicht")

    filtered = filter_posts(posts, search_query, category_filter)
    filtered = list(reversed(filtered))  # neueste zuerst

    total = len(filtered)
    total_pages = max(1, (total - 1) // posts_per_page + 1)

    page = st.number_input("Seite", min_value=1, max_value=total_pages, value=1)

    start = (page - 1) * posts_per_page
    end = start + posts_per_page

    for post in filtered[start:end]:
        render_post(post)

# -----------------------------
# BEITRAG ERSTELLEN
# -----------------------------
if menu == "✍️ Beitrag erstellen" and st.session_state.role == "admin":
    st.markdown("## ✍️ Neuen Beitrag erstellen")

    title = st.text_input("Titel")
    category = st.text_input("Kategorie")
    tags = st.text_input("Tags (kommagetrennt)")
    content = st.text_area("Inhalt", height=250)
    image_file = st.file_uploader("Bild", type=["png", "jpg", "jpeg"])

    if st.button("Speichern"):
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
            "likes": 0
        }

        posts.append(new_post)
        save_posts(posts)
        st.success("Beitrag gespeichert!")
        st.balloons()

# -----------------------------
# ADMIN PANEL
# -----------------------------
if menu == "⚙️ Admin Panel" and st.session_state.role == "admin":
    st.markdown("## ⚙️ Admin Panel")

    for post in posts:
        st.markdown(f"### {post['title']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Löschen", key=f"del{post['id']}"):
                posts.remove(post)
                save_posts(posts)
                st.experimental_rerun()

        with col2:
            if st.button("✏️ Bearbeiten", key=f"edit{post['id']}"):
                st.session_state.edit_post_id = post["id"]
                st.experimental_rerun()

    if st.session_state.edit_post_id:
        post = next(p for p in posts if p["id"] == st.session_state.edit_post_id)

        st.markdown("### Beitrag bearbeiten")
        new_title = st.text_input("Titel", value=post["title"])
        new_content = st.text_area("Inhalt", value=post["content"])

        if st.button("Speichern Änderungen"):
            post["title"] = new_title
            post["content"] = new_content
            save_posts(posts)
            st.session_state.edit_post_id = None
            st.experimental_rerun()
