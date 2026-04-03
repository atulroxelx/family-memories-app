# ============================================================
# Our Family Memories - Main Streamlit App (OAuth 2.0)
# ============================================================

import streamlit as st
import os
import mimetypes
from config import (
    APP_NAME, APP_ICON, APP_SUBTITLE, APP_PASSWORD,
    IMAGE_TYPES, VIDEO_TYPES, GRID_COLUMNS, CREDENTIALS_FILE, TOKEN_FILE
)

# ---- Page Config ----
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS ----
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #f0f0f0;
    }
    .login-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(233,30,140,0.3);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        backdrop-filter: blur(10px);
        max-width: 420px;
        margin: auto;
    }
    .login-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #E91E8C, #ff6b9d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .login-subtitle { color: #aaa; margin-bottom: 2rem; }
    .app-header {
        background: linear-gradient(90deg, rgba(233,30,140,0.2), rgba(255,107,157,0.1));
        border-bottom: 2px solid rgba(233,30,140,0.4);
        padding: 1.2rem 2rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 1.5rem;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #E91E8C, #ff6b9d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .app-subtitle-small { color: #bbb; font-size: 0.85rem; margin: 0; }
    .media-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(233,30,140,0.2);
        border-radius: 14px;
        padding: 0.6rem;
        margin-bottom: 1rem;
        overflow: hidden;
        transition: transform 0.2s, border-color 0.2s;
    }
    .media-card:hover { transform: scale(1.02); border-color: rgba(233,30,140,0.7); }
    .media-filename {
        color: #ddd; font-size: 0.75rem; text-align: center;
        margin-top: 0.4rem; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
    }
    .album-card {
        background: rgba(233,30,140,0.1);
        border: 1px solid rgba(233,30,140,0.3);
        border-radius: 14px; padding: 1.2rem;
        text-align: center; margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .album-card:hover {
        background: rgba(233,30,140,0.25);
        border-color: #E91E8C; transform: translateY(-3px);
    }
    .section-title {
        font-size: 1.5rem; font-weight: 700; color: #ff6b9d;
        border-left: 4px solid #E91E8C;
        padding-left: 0.75rem; margin-bottom: 1.2rem;
    }
    .connect-card {
        background: rgba(255,255,255,0.05);
        border: 2px solid rgba(233,30,140,0.4);
        border-radius: 20px; padding: 3rem;
        text-align: center; max-width: 500px; margin: auto;
    }
    .stat-chip {
        background: rgba(233,30,140,0.15);
        border: 1px solid rgba(233,30,140,0.3);
        border-radius: 20px; padding: 0.3rem 0.9rem;
        color: #ff6b9d; font-size: 0.85rem;
        display: inline-block; margin-right: 0.5rem;
    }
    [data-testid="stSidebar"] {
        background: rgba(15,15,35,0.95);
        border-right: 1px solid rgba(233,30,140,0.2);
    }
    .sidebar-logo { text-align: center; padding: 1rem 0 0.5rem 0; font-size: 2.5rem; }
    .sidebar-title { text-align: center; font-size: 1rem; font-weight: 700; color: #ff6b9d; margin-bottom: 1.5rem; }
    .stButton > button {
        background: linear-gradient(90deg, #E91E8C, #ff6b9d);
        color: white; border: none; border-radius: 25px;
        padding: 0.5rem 1.5rem; font-weight: 600; transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; color: white; }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(233,30,140,0.4);
        border-radius: 10px; color: white;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "drive_service" not in st.session_state:
    st.session_state.drive_service = None
if "root_folder_id" not in st.session_state:
    st.session_state.root_folder_id = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"
if "selected_album" not in st.session_state:
    st.session_state.selected_album = None
if "drive_connected" not in st.session_state:
    st.session_state.drive_connected = False


# ============================================================
# CONNECT TO GOOGLE DRIVE
# ============================================================
def connect_drive():
    """Connect to Google Drive using OAuth 2.0."""
    try:
        from google_drive_helper import authenticate, get_or_create_root_folder
        service = authenticate()
        root_id = get_or_create_root_folder(service)
        st.session_state.drive_service = service
        st.session_state.root_folder_id = root_id
        st.session_state.drive_connected = True
        return True
    except Exception as e:
        st.error(f"❌ Google Drive connection failed: {e}")
        return False


# ============================================================
# PAGE: LOGIN
# ============================================================
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="login-card">
            <div style="font-size:4rem;">💖</div>
            <div class="login-title">{APP_NAME}</div>
            <div class="login-subtitle">{APP_SUBTITLE}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        password = st.text_input("🔑 Enter Family Password", type="password", placeholder="Enter password...")
        if st.button("✨ Enter Our World", use_container_width=True):
            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
        st.markdown("<p style='color:#666;font-size:0.8rem;text-align:center;margin-top:1rem;'>🔒 Private — For Family Only</p>", unsafe_allow_html=True)


# ============================================================
# PAGE: CONNECT GOOGLE DRIVE (OAuth)
# ============================================================
def connect_drive_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="connect-card">
            <div style="font-size:4rem;">☁️</div>
            <h2 style="color:#ff6b9d;margin-bottom:0.5rem;">Connect Google Drive</h2>
            <p style="color:#aaa;margin-bottom:2rem;">
                Connect your personal Google Drive to store and access your family memories securely.
            </p>
            <div style="background:rgba(233,30,140,0.1);border-radius:12px;padding:1rem;text-align:left;margin-bottom:1.5rem;">
                <p style="color:#ff6b9d;font-weight:600;margin-bottom:0.5rem;">📋 Before clicking connect:</p>
                <p style="color:#ccc;font-size:0.9rem;">
                    ✅ Make sure <b>client_secrets.json</b> is in the app folder<br>
                    ✅ A browser window will open to sign in<br>
                    ✅ Sign in with your Google account<br>
                    ✅ Click <b>"Allow"</b> to grant access<br>
                    ✅ Come back here — you're done!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if not os.path.exists(CREDENTIALS_FILE):
            st.error(f"⚠️ `{CREDENTIALS_FILE}` not found in app folder! Please follow the README setup guide.")
            st.info("📖 Check README.md for instructions on how to download client_secrets.json from Google Cloud Console.")
        else:
            if st.button("🔗 Connect to Google Drive", use_container_width=True):
                with st.spinner("Opening Google login in your browser..."):
                    success = connect_drive()
                if success:
                    st.success("✅ Google Drive connected successfully!")
                    st.balloons()
                    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================
def sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">💖</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-title">{APP_NAME}</div>', unsafe_allow_html=True)
        st.markdown("---")

        pages = ["🏠 Home", "📸 Gallery", "📁 Albums", "⬆️ Upload", "ℹ️ About"]
        for page in pages:
            if st.button(page, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.session_state.selected_album = None
                st.rerun()

        st.markdown("---")

        # Storage info
        if st.session_state.drive_service:
            try:
                from google_drive_helper import get_storage_info
                used, total = get_storage_info(st.session_state.drive_service)
                if total > 0:
                    pct = (used / total) * 100
                    st.markdown("**💾 Storage**")
                    st.progress(min(pct / 100, 1.0))
                    st.markdown(f"<small style='color:#aaa'>{used} GB / {total} GB used</small>", unsafe_allow_html=True)
            except Exception:
                pass

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ============================================================
# HELPER: Display Media Card
# ============================================================
def display_media_card(file, service):
    from google_drive_helper import download_file
    mime = file.get("mimeType", "")
    name = file.get("name", "Unknown")
    file_id = file["id"]

    st.markdown('<div class="media-card">', unsafe_allow_html=True)
    try:
        if "image" in mime:
            thumb = file.get("thumbnailLink")
            if thumb:
                st.image(thumb.replace("s220", "s400"), use_container_width=True)
            else:
                img_bytes = download_file(service, file_id)
                st.image(img_bytes, use_container_width=True)
        elif "video" in mime:
            video_bytes = download_file(service, file_id)
            st.video(video_bytes)
    except Exception:
        st.markdown("<div style='color:#aaa;text-align:center;padding:1rem;'>⚠️ Preview unavailable</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="media-filename">📄 {name}</div>', unsafe_allow_html=True)

    try:
        file_bytes = download_file(service, file_id)
        st.download_button(
            label="⬇️ Download",
            data=file_bytes,
            file_name=name,
            mime=mime,
            key=f"dl_{file_id}",
            use_container_width=True
        )
    except Exception:
        pass
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PAGE: HOME
# ============================================================
def home_page():
    st.markdown("""
    <div class="app-header">
        <p class="app-title">💖 Our Family Memories</p>
        <p class="app-subtitle-small">Cherish every precious moment together</p>
    </div>
    """, unsafe_allow_html=True)

    from google_drive_helper import list_files, list_folders
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id

    all_files = list_files(service, root_id)
    folders = list_folders(service, root_id)

    photos = [f for f in all_files if "image" in f.get("mimeType", "")]
    videos = [f for f in all_files if "video" in f.get("mimeType", "")]

    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <span class="stat-chip">📸 {len(photos)} Photos</span>
        <span class="stat-chip">🎬 {len(videos)} Videos</span>
        <span class="stat-chip">📁 {len(folders)} Albums</span>
    </div>
    """, unsafe_allow_html=True)

    if all_files:
        st.markdown('<div class="section-title">🌟 Recent Memories</div>', unsafe_allow_html=True)
        recent = all_files[:6]
        cols = st.columns(3)
        for i, file in enumerate(recent):
            with cols[i % 3]:
                display_media_card(file, service)
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#aaa;">
            <div style="font-size:4rem;">📭</div>
            <p>No memories yet! Start by uploading photos & videos.</p>
        </div>
        """, unsafe_allow_html=True)

    if folders:
        st.markdown('<div class="section-title">📁 Albums</div>', unsafe_allow_html=True)
        album_cols = st.columns(min(len(folders), 4))
        for i, folder in enumerate(folders[:4]):
            with album_cols[i % 4]:
                if st.button(f"📂 {folder['name']}", key=f"home_album_{folder['id']}", use_container_width=True):
                    st.session_state.selected_album = folder
                    st.session_state.current_page = "📁 Albums"
                    st.rerun()


# ============================================================
# PAGE: GALLERY
# ============================================================
def gallery_page():
    st.markdown('<div class="section-title">📸 Full Gallery</div>', unsafe_allow_html=True)
    from google_drive_helper import list_files
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id

    with st.spinner("Loading your memories..."):
        all_files = list_files(service, root_id)

    if not all_files:
        st.info("📭 No media found. Upload some memories first!")
        return

    col1, col2 = st.columns([2, 1])
    with col1:
        filter_type = st.selectbox("Filter", ["All", "📸 Photos Only", "🎬 Videos Only"])
    with col2:
        st.markdown(f"<p style='color:#aaa;margin-top:2rem;'>{len(all_files)} items total</p>", unsafe_allow_html=True)

    if filter_type == "📸 Photos Only":
        all_files = [f for f in all_files if "image" in f.get("mimeType", "")]
    elif filter_type == "🎬 Videos Only":
        all_files = [f for f in all_files if "video" in f.get("mimeType", "")]

    cols = st.columns(GRID_COLUMNS)
    for i, file in enumerate(all_files):
        with cols[i % GRID_COLUMNS]:
            display_media_card(file, service)


# ============================================================
# PAGE: ALBUMS
# ============================================================
def albums_page():
    from google_drive_helper import list_folders, list_files, create_folder
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id

    if st.session_state.selected_album:
        album = st.session_state.selected_album
        if st.button("⬅️ Back to Albums"):
            st.session_state.selected_album = None
            st.rerun()
        st.markdown(f'<div class="section-title">📂 {album["name"]}</div>', unsafe_allow_html=True)
        files = list_files(service, album["id"])
        if not files:
            st.info("📭 This album is empty.")
        else:
            cols = st.columns(GRID_COLUMNS)
            for i, file in enumerate(files):
                with cols[i % GRID_COLUMNS]:
                    display_media_card(file, service)
        return

    st.markdown('<div class="section-title">📁 Albums</div>', unsafe_allow_html=True)

    with st.expander("➕ Create New Album"):
        new_album_name = st.text_input("Album Name", placeholder="e.g. Birthday 2024")
        if st.button("Create Album"):
            if new_album_name.strip():
                with st.spinner("Creating album..."):
                    create_folder(service, new_album_name.strip(), root_id)
                st.success(f"✅ Album '{new_album_name}' created!")
                st.rerun()
            else:
                st.error("Please enter an album name.")

    folders = list_folders(service, root_id)
    if not folders:
        st.info("📭 No albums yet. Create your first album above!")
        return

    cols = st.columns(4)
    for i, folder in enumerate(folders):
        with cols[i % 4]:
            files_in_folder = list_files(service, folder["id"])
            st.markdown(f"""
            <div class="album-card">
                <div style="font-size:2.5rem;">📂</div>
                <div style="color:#fff;font-weight:600;margin-top:0.4rem;">{folder["name"]}</div>
                <div style="color:#aaa;font-size:0.8rem;">{len(files_in_folder)} items</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open", key=f"open_{folder['id']}", use_container_width=True):
                st.session_state.selected_album = folder
                st.rerun()


# ============================================================
# PAGE: UPLOAD
# ============================================================
def upload_page():
    st.markdown('<div class="section-title">⬆️ Upload Memories</div>', unsafe_allow_html=True)
    from google_drive_helper import list_folders, upload_file
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id
    folders = list_folders(service, root_id)

    folder_options = {"📁 Root (Family Memories)": root_id}
    for f in folders:
        folder_options[f"📂 {f['name']}"] = f["id"]

    selected_folder_name = st.selectbox("📁 Upload to Album", list(folder_options.keys()))
    target_folder_id = folder_options[selected_folder_name]

    uploaded_files = st.file_uploader(
        "📂 Choose photos or videos",
        type=IMAGE_TYPES + VIDEO_TYPES,
        accept_multiple_files=True,
        help="Supported: JPG, PNG, GIF, WEBP, MP4, MOV, AVI, MKV"
    )

    if uploaded_files:
        st.markdown(f"**{len(uploaded_files)} file(s) selected**")
        if st.button("⬆️ Upload All to Google Drive", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            success_count = 0
            for idx, file in enumerate(uploaded_files):
                status_text.text(f"Uploading: {file.name}...")
                try:
                    mime_type, _ = mimetypes.guess_type(file.name)
                    if not mime_type:
                        mime_type = "application/octet-stream"
                    upload_file(service, file.read(), file.name, mime_type, target_folder_id)
                    success_count += 1
                except Exception as e:
                    st.error(f"❌ Failed to upload {file.name}: {e}")
                progress_bar.progress((idx + 1) / len(uploaded_files))
            status_text.empty()
            st.success(f"✅ Uploaded {success_count}/{len(uploaded_files)} file(s) to {selected_folder_name}!")
            st.balloons()


# ============================================================
# PAGE: ABOUT
# ============================================================
def about_page():
    st.markdown('<div class="section-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);border-radius:16px;padding:2rem;border:1px solid rgba(233,30,140,0.2);">
        <h3 style="color:#ff6b9d;">💖 Our Family Memories</h3>
        <p style="color:#ccc;">A private, beautiful space to store, share and cherish all the precious moments of your family.</p>
        <hr style="border-color:rgba(233,30,140,0.2);">
        <h4 style="color:#ff6b9d;">✨ Features</h4>
        <ul style="color:#ccc;">
            <li>📸 View and browse photos & videos</li>
            <li>📁 Organize memories into albums</li>
            <li>⬆️ Upload new photos & videos from any device</li>
            <li>☁️ Stored securely on your personal Google Drive</li>
            <li>🔐 Password-protected for family only</li>
            <li>⬇️ Download any memory</li>
        </ul>
        <hr style="border-color:rgba(233,30,140,0.2);">
        <p style="color:#888;font-size:0.85rem;">Built with ❤️ using Python & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MAIN APP
# ============================================================
def main():
    # Step 1: Login check
    if not st.session_state.authenticated:
        login_page()
        return

    # Step 2: Google Drive connection check
    if not st.session_state.drive_connected or st.session_state.drive_service is None:
        # Try auto-connect with existing token
        from google_drive_helper import is_authenticated
        if is_authenticated():
            with st.spinner("Connecting to your memories..."):
                connect_drive()
            st.rerun()
        else:
            connect_drive_page()
        return

    # Step 3: Main app
    sidebar()
    page = st.session_state.current_page
    if page == "🏠 Home":
        home_page()
    elif page == "📸 Gallery":
        gallery_page()
    elif page == "📁 Albums":
        albums_page()
    elif page == "⬆️ Upload":
        upload_page()
    elif page == "ℹ️ About":
        about_page()


if __name__ == "__main__":
    main()
