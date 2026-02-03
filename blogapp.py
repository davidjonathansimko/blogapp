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
    st.session_state.role = None  # "admin", "user", "visitor"
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "🙂"
if "page" not in st.session_state:
    st.session_state.page = "login"  # "login" oder "app"
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None

# -----------------------------
# LOGIN / LOGOUT
# -----------------------------
def login_screen():
    st.markdown(
        """
        <h1 style="text-align:center;">📝 Willkommen in deinem Blog</h1>
        <p style="text-align:center; font-size:16px;">Wähle, wie du fortfahren möchtest.</p>
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
        name = st.text_input("Anzeigename (für Kommentare)")
        avatar = st.text_input("Avatar (Emoji, z.B. 🙂, 😎, 🐍)", value="🙂")

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
# HAUPT-NAVIGATION (LOGIN / APP)
# -----------------------------
if st.session_state.page == "login":
    login_screen()
    st.stop()

# Ab hier: Benutzer ist in der App (visitor / user / admin)

# -----------------------------
# DARK MODE + GLOBAL STYLING
# -----------------------------
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=True)

if dark_mode:
    st.markdown(
        """
        <style>
        body { background-color: #0e1117; color: #fafafa; }
        .stApp { background-color: #0e1117; }
        .post-card {
            padding: 1rem;
            border-radius: 0.75rem;
            background-color: #161a23;
            margin-bottom: 1rem;
            border: 1px solid #2a2f3a;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .post-card {
            padding: 1rem;
            border-radius: 0.75rem;
            background-color: #ffffff;
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# SIDEBAR: USER INFO & LOGOUT
# -----------------------------
st.sidebar.title("📚 Navigation")
st.sidebar.write(f"👤 {st.session_state.user_avatar} {st.session_state.user_name}")
st.sidebar.write(f"Rolle: **{st.session_state.role}**")

if st.sidebar.button("🚪 Logout"):
    logout()
    st.experimental_rerun()

# -----------------------------
# NAVIGATIONSMENÜ
# -----------------------------
if st.session_state.role == "admin":
    menu = st.sidebar.radio(
        "Seite wählen",
        ["📖 Blog lesen", "✍️ Beitrag erstellen", "⚙️ Admin Panel"],
    )
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

def render_post(post, compact=False):
    with st.container():
        st.markdown('<div class="post-card">', unsafe_allow_html=True)

        st.markdown(f"### {post['title']}")
        st.caption(
            f"{post['date']} | Kategorie: {post.get('category', '–')} | "
            f"Tags: {', '.join(post.get('tags', [])) or '–'}"
        )

        if post.get("image_path") and os.path.exists(post["image_path"]):
            st.image(post["image_path"], use_column_width=True)

        if compact:
            st.markdown(shorten(post["content"], width=200, placeholder="..."))
        else:
            st.markdown(post["content"])

        col_like, col_export = st.columns(2)
        with col_like:
            if st.session_state.role in ["admin", "user"]:
                if st.button(f"👍 Like ({post.get('likes', 0)})", key=f"like_{post['id']}"):
                    like_post(post)
                    st.experimental_rerun()
            else:
                st.write(f"👍 Likes: {post.get('likes', 0)}")

        with col_export:
            export_text = (
                f"# {post['title']}\n\n{post['content']}\n\n"
                f"Kategorie: {post.get('category','')}\n"
                f"Tags: {', '.join(post.get('tags', []))}"
            )
            st.download_button(
                "📄 Export (Markdown)",
                data=export_text,
                file_name=f"{post['title'].replace(' ', '_')}.md",
                mime="text/markdown",
                key=f"export_{post['id']}",
            )

        if not compact:
            st.markdown("### 💬 Kommentare")
            comments = post.get("comments", [])
            if not comments:
                st.write("_Noch keine Kommentare._")
            else:
                for c in comments:
                    st.markdown(
                        f"- {c.get('avatar','🙂')} **{c['author']}** "
                        f"({c['date']}): {c['text']}"
                    )

            if st.session_state.role in ["admin", "user"]:
                with st.expander("Kommentar schreiben"):
                    author = st.text_input(
                        f"Name (Post {post['id']})",
                        value=st.session_state.user_name,
                        key=f"author_{post['id']}",
                    )
                    avatar = st.text_input(
                        "Avatar (Emoji)",
                        value=st.session_state.user_avatar,
                        key=f"avatar_{post['id']}",
                    )
                    text = st.text_area(
                        f"Kommentar (Post {post['id']})",
                        key=f"text_{post['id']}",
                    )

                    if st.button("Kommentar speichern", key=f"save_comment_{post['id']}"):
                        if author.strip() == "" or text.strip() == "":
                            st.error("Bitte Name und Kommentar eingeben.")
                        else:
                            new_comment = {
                                "author": author,
                                "avatar": avatar or "🙂",
                                "text": text,
                                "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                            }
                            post.setdefault("comments", []).append(new_comment)
                            save_posts(posts)
                            st.success("Kommentar gespeichert!")
                            st.experimental_rerun()
            else:
                st.info("Nur eingeloggte User können kommentieren.")

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# SEITE: BLOG LESEN
# -----------------------------
if menu == "📖 Blog lesen":
    st.markdown("## 📖 Blog")
    filtered = filter_posts(posts, search_query, category_filter)

    if not filtered:
        st.info("Keine Beiträge gefunden.")
    else:
        total_posts = len(filtered)
        total_pages = (total_posts - 1) // posts_per_page + 1
        page = st.number_input(
            "Seite wählen",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
        )

        start = (page - 1) * posts_per_page
        end = start + posts_per_page
        for post in reversed(filtered[start:end]):
            render_post(post, compact=False)

        st.caption(f"Seite {page} von {total_pages}")

# -----------------------------
# SEITE: BEITRAG ERSTELLEN (nur Admin)
# -----------------------------
if menu == "✍️ Beitrag erstellen" and st.session_state.role == "admin":
    st.markdown("## ✍️ Neuen Beitrag erstellen")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        title = st.text_input("Titel")
        category = st.text_input("Kategorie")
        tags_input = st.text_input("Tags (kommagetrennt)")
        content = st.text_area("Inhalt (Markdown)", height=300)

    with col_right:
        image_file = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"])
        st.info("Tipp: Nutze Markdown für Überschriften, Listen, Code usw.")

    if st.button("Beitrag speichern"):
        if title.strip() == "" or content.strip() == "":
            st.error("Titel und Inhalt erforderlich.")
        else:
            image_path = None
            if image_file:
                ext = os.path.splitext(image_file.name)[1]
                img_name = f"{uuid4().hex}{ext}"
                image_path = os.path.join(IMAGE_DIR, img_name)
                with open(image_path, "wb") as f:
                    f.write(image_file.getbuffer())

            tags = [t.strip() for t in tags_input.split(",") if t.strip()]

            new_post = {
                "id": uuid4().hex,
                "title": title,
                "content": content,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "category": category,
                "tags": tags,
                "image_path": image_path,
                "comments": [],
                "likes": 0,
            }

            posts.append(new_post)
            save_posts(posts)
            st.success("Beitrag gespeichert!")
            st.balloons()

# -----------------------------
# SEITE: ADMIN PANEL (nur Admin)
# -----------------------------
if menu == "⚙️ Admin Panel" and st.session_state.role == "admin":
    st.markdown("## ⚙️ Admin Panel")

    if not posts:
        st.info("Noch keine Beiträge vorhanden.")
    else:
        for post in posts:
            with st.container():
                st.markdown('<div class="post-card">', unsafe_allow_html=True)
                st.markdown(f"### {post['title']}")
                st.caption(f"{post['date']} | Likes: {post.get('likes',0)}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🗑️ Löschen", key=f"del_{post['id']}"):
                        posts.remove(post)
                        save_posts(posts)
                        st.success("Beitrag gelöscht.")
                        st.experimental_rerun()
                with col2:
                    if st.button("✏️ Bearbeiten", key=f"edit_{post['id']}"):
                        st.session_state.edit_post_id = post["id"]
                        st.experimental_rerun()
                with col3:
                    st.write(f"Kommentare: {len(post.get('comments', []))}")

                st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.edit_post_id is not None:
            post = next((p for p in posts if p["id"] == st.session_state.edit_post_id), None)
            if post:
                st.markdown("---")
                st.markdown("### ✏️ Beitrag bearbeiten")

                new_title = st.text_input("Titel", value=post["title"])
                new_category = st.text_input("Kategorie", value=post.get("category", ""))
                new_tags = st.text_input("Tags", value=", ".join(post.get("tags", [])))
                new_content = st.text_area("Inhalt", value=post["content"], height=250)

                if st.button("Änderungen speichern"):
                    post["title"] = new_title
                    post["category"] = new_category
                    post["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
                    post["content"] = new_content
                    save_posts(posts)
                    st.success("Beitrag aktualisiert.")
                    st.session_state.edit_post_id = None
                    st.experimental_rerun()
            else:
                st.session_state.edit_post_id = None
