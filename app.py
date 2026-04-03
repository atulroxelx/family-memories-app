
# ============================================================
# Setup secrets for Streamlit Cloud
# ============================================================
try:
    from setup_secrets import setup_credentials
    setup_credentials()
except Exception:
    pass

# ============================================================
# Our Family Memories - World Class UI (OAuth 2.0)
# ============================================================
import streamlit as st
import os
import mimetypes
from datetime import datetime
from config import (
    APP_NAME, APP_ICON, APP_SUBTITLE, APP_PASSWORD,
    IMAGE_TYPES, VIDEO_TYPES, GRID_COLUMNS, CREDENTIALS_FILE, TOKEN_FILE
)

st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON, layout="wide", initial_sidebar_state="expanded")

# ============================================================
# WORLD CLASS CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Poppins', sans-serif !important; }
:root {
    --primary: #E91E8C; --secondary: #7B2FBE;
    --accent: #FFD700;  --bg: #0a0a1a;
    --card: rgba(255,255,255,0.05);
    --border: rgba(233,30,140,0.3);
    --text: #ffffff; --subtext: #a0a0c0;
    --success: #00ff88;
}
html, body, [class*="css"] { background-color: var(--bg) !important; color: var(--text) !important; }
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 30%, #1a0a2e 60%, #0a1a2e 100%) !important;
    min-height: 100vh;
    padding-bottom: 90px !important;
}
.stApp::before {
    content: '';
    position: fixed; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(ellipse at 20% 50%, rgba(233,30,140,0.03) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(123,47,190,0.05) 0%, transparent 50%);
    animation: bgPulse 8s ease-in-out infinite alternate;
    pointer-events: none; z-index: 0;
}
@keyframes bgPulse {
    0% { transform: scale(1) rotate(0deg); }
    100% { transform: scale(1.1) rotate(2deg); }
}

/* === GLASSMORPHISM CARD === */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(233,30,140,0.2);
    border-radius: 20px; padding: 1.5rem;
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    transition: all 0.3s ease; position: relative; overflow: hidden;
}
.glass-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #E91E8C, #7B2FBE, transparent);
    opacity: 0.7;
}
.glass-card:hover {
    border-color: rgba(233,30,140,0.6);
    box-shadow: 0 0 30px rgba(233,30,140,0.2), 0 20px 60px rgba(0,0,0,0.3);
    transform: translateY(-5px);
}

/* === GRADIENT TEXT === */
.gradient-text {
    background: linear-gradient(90deg, #E91E8C, #7B2FBE, #FFD700, #E91E8C);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: gradientShift 3s linear infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* === LOGIN === */
.login-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(233,30,140,0.3);
    border-radius: 30px; padding: 3.5rem;
    text-align: center; backdrop-filter: blur(30px);
    max-width: 450px; width: 100%;
    box-shadow: 0 25px 80px rgba(233,30,140,0.15), 0 0 0 1px rgba(255,255,255,0.05);
}
.login-emoji { font-size: 5rem; animation: float 3s ease-in-out infinite; display: block; margin-bottom: 1rem; }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-15px); } }
.login-title {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(90deg, #E91E8C, #ff6b9d, #7B2FBE);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.login-subtitle { color: #a0a0c0; font-size: 0.95rem; margin-bottom: 2rem; }

/* === BREADCRUMB === */
.breadcrumb {
    display: flex; align-items: center; gap: 0.5rem;
    background: rgba(233,30,140,0.08);
    border: 1px solid rgba(233,30,140,0.2);
    border-radius: 12px; padding: 0.6rem 1rem;
    margin-bottom: 1.2rem; font-size: 0.85rem;
}
.breadcrumb-item { color: #a0a0c0; }
.breadcrumb-item.active { color: #ff6b9d; font-weight: 600; }
.breadcrumb-sep { color: rgba(233,30,140,0.4); }

/* === BACK BUTTON === */
.back-btn-container {
    margin-bottom: 1rem;
}

/* === STAT CARDS === */
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(233,30,140,0.2);
    border-radius: 20px; padding: 1.5rem;
    text-align: center; backdrop-filter: blur(20px);
    transition: all 0.3s ease;
}
.stat-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 40px rgba(233,30,140,0.3);
    border-color: rgba(233,30,140,0.6);
}
.stat-icon { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }
.stat-number {
    font-size: 2.5rem; font-weight: 900;
    background: linear-gradient(90deg, #E91E8C, #FFD700);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1;
}
.stat-label { color: #a0a0c0; font-size: 0.85rem; margin-top: 0.3rem; font-weight: 500; }

/* === MEDIA CARDS === */
.media-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; overflow: hidden;
    transition: all 0.3s ease; margin-bottom: 1rem;
}
.media-card:hover {
    border-color: rgba(233,30,140,0.5);
    box-shadow: 0 0 25px rgba(233,30,140,0.2);
    transform: scale(1.02);
}
.media-name {
    color: #e0e0f0; font-size: 0.75rem; font-weight: 500;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px;
}

/* === ALBUM CARDS === */
.album-card {
    background: linear-gradient(135deg, rgba(233,30,140,0.1), rgba(123,47,190,0.1));
    border: 1px solid rgba(233,30,140,0.25);
    border-radius: 20px; padding: 1.8rem 1.2rem;
    text-align: center; transition: all 0.3s ease; margin-bottom: 1rem;
}
.album-card:hover {
    transform: translateY(-8px); border-color: #E91E8C;
    box-shadow: 0 0 40px rgba(233,30,140,0.3), 0 20px 60px rgba(0,0,0,0.3);
}
.album-emoji { font-size: 3rem; display: block; margin-bottom: 0.8rem; }
.album-name { color: #fff; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem; }
.album-count {
    display: inline-block; background: rgba(233,30,140,0.2);
    border: 1px solid rgba(233,30,140,0.3); border-radius: 20px;
    padding: 0.15rem 0.7rem; color: #ff6b9d; font-size: 0.75rem; font-weight: 600;
}

/* === SECTION HEADERS === */
.section-header {
    display: flex; align-items: center; gap: 0.75rem;
    margin-bottom: 1.5rem; padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(233,30,140,0.2);
}
.section-title {
    font-size: 1.4rem; font-weight: 700;
    background: linear-gradient(90deg, #E91E8C, #ff6b9d);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;
}
.section-badge {
    background: rgba(233,30,140,0.15); border: 1px solid rgba(233,30,140,0.3);
    border-radius: 20px; padding: 0.15rem 0.75rem;
    color: #ff6b9d; font-size: 0.8rem; font-weight: 600;
}

/* === UPLOAD AREA === */
.upload-area {
    background: rgba(233,30,140,0.03);
    border: 2px dashed rgba(233,30,140,0.4);
    border-radius: 20px; padding: 3rem 2rem;
    text-align: center; transition: all 0.3s ease; margin-bottom: 1.5rem;
}
.upload-area:hover { border-color: #E91E8C; background: rgba(233,30,140,0.07); }
.upload-icon { font-size: 3rem; display: block; margin-bottom: 1rem; }
.upload-text { color: #ff6b9d; font-size: 1.1rem; font-weight: 600; }
.upload-subtext { color: #a0a0c0; font-size: 0.85rem; margin-top: 0.3rem; }

/* === TIMELINE === */
.timeline-month {
    background: rgba(233,30,140,0.08);
    border-left: 3px solid #E91E8C;
    border-radius: 0 12px 12px 0;
    padding: 0.6rem 1rem; margin-bottom: 1rem;
    color: #ff6b9d; font-weight: 700; font-size: 1rem;
}

/* === SLIDESHOW === */
.slideshow-container {
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(233,30,140,0.3);
    border-radius: 20px; padding: 1rem; text-align: center;
}
.slideshow-counter { color: #a0a0c0; font-size: 0.85rem; margin-top: 0.5rem; }
.slideshow-name { color: #ff6b9d; font-weight: 600; font-size: 1rem; margin-top: 0.5rem; }

/* === QUICK ACTIONS === */
.quick-action {
    background: linear-gradient(135deg, rgba(233,30,140,0.15), rgba(123,47,190,0.15));
    border: 1px solid rgba(233,30,140,0.3);
    border-radius: 16px; padding: 1.2rem;
    text-align: center; transition: all 0.3s ease;
}
.quick-action:hover {
    background: linear-gradient(135deg, rgba(233,30,140,0.3), rgba(123,47,190,0.3));
    transform: translateY(-5px); box-shadow: 0 0 30px rgba(233,30,140,0.3);
}
.quick-icon { font-size: 2rem; display: block; }
.quick-label { color: #e0e0f0; font-size: 0.85rem; font-weight: 600; margin-top: 0.4rem; }

/* === GREETING BANNER === */
.greeting-banner {
    background: linear-gradient(135deg, rgba(233,30,140,0.15) 0%, rgba(123,47,190,0.15) 50%, rgba(255,215,0,0.05) 100%);
    border: 1px solid rgba(233,30,140,0.25);
    border-radius: 20px; padding: 1.8rem 2rem;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
}
.greeting-banner::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #E91E8C, #7B2FBE, #FFD700);
}
.greeting-time { color: #a0a0c0; font-size: 0.85rem; }
.greeting-main {
    font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(90deg, #E91E8C, #ff6b9d, #FFD700);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;
}
.greeting-sub { color: #c0c0d8; font-size: 0.95rem; }

/* === INPUTS === */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(233,30,140,0.3) !important;
    border-radius: 12px !important; color: white !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #E91E8C !important;
    box-shadow: 0 0 20px rgba(233,30,140,0.3) !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(233,30,140,0.3) !important;
    border-radius: 12px !important; color: white !important;
}

/* === BUTTONS === */
.stButton > button {
    background: linear-gradient(135deg, #E91E8C, #7B2FBE) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important; font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(233,30,140,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(233,30,140,0.5) !important;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d25 0%, #0a0a1a 100%) !important;
    border-right: 1px solid rgba(233,30,140,0.2) !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(233,30,140,0.15) !important;
    border-radius: 12px !important; color: #c0c0d8 !important;
    text-align: left !important; padding: 0.6rem 1rem !important;
    box-shadow: none !important; font-weight: 500 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(233,30,140,0.15) !important;
    border-color: rgba(233,30,140,0.4) !important;
    color: #ff6b9d !important; transform: translateX(5px) !important;
    box-shadow: none !important;
}
.sidebar-logo {
    text-align: center; padding: 1.5rem 0 0.5rem 0;
    font-size: 3rem; animation: float 3s ease-in-out infinite;
}
.sidebar-appname {
    text-align: center; font-size: 0.95rem; font-weight: 700;
    background: linear-gradient(90deg, #E91E8C, #7B2FBE);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem;
}
.sidebar-tagline { text-align: center; color: #606080; font-size: 0.7rem; margin-bottom: 1.2rem; }
.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(233,30,140,0.3), transparent);
    margin: 0.8rem 0;
}
.sidebar-label { color: #505070; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; padding: 0.3rem 0; }

/* === SIDEBAR TOGGLE BUTTON HIGHLIGHT === */
[data-testid="collapsedControl"] {
    background: linear-gradient(135deg, #E91E8C, #7B2FBE) !important;
    border-radius: 0 12px 12px 0 !important;
    color: white !important;
    box-shadow: 4px 0 20px rgba(233,30,140,0.5) !important;
}

/* === FIXED BOTTOM NAV BAR === */
.bottom-nav {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: rgba(10,10,26,0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 1px solid rgba(233,30,140,0.3);
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 0.6rem 1rem;
    z-index: 9999;
    box-shadow: 0 -4px 30px rgba(233,30,140,0.15);
}
.bottom-nav-item {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    cursor: pointer; padding: 0.4rem 0.8rem;
    border-radius: 12px; transition: all 0.2s ease;
    text-decoration: none; color: #606080;
    min-width: 50px;
}
.bottom-nav-item:hover {
    background: rgba(233,30,140,0.15);
    color: #ff6b9d;
    transform: translateY(-3px);
}
.bottom-nav-item.active {
    background: rgba(233,30,140,0.2);
    color: #ff6b9d;
}
.bottom-nav-icon { font-size: 1.3rem; line-height: 1; }
.bottom-nav-label { font-size: 0.6rem; font-weight: 600; margin-top: 0.2rem; letter-spacing: 0.3px; }

/* === PROGRESS BAR === */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #E91E8C, #7B2FBE) !important;
    border-radius: 10px !important;
}

/* === MISC === */
.info-chip {
    display: inline-block; background: rgba(233,30,140,0.1);
    border: 1px solid rgba(233,30,140,0.25); border-radius: 20px;
    padding: 0.25rem 0.8rem; color: #ff6b9d; font-size: 0.8rem;
    font-weight: 500; margin-right: 0.4rem; margin-bottom: 0.4rem;
}
.about-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(233,30,140,0.15);
    border-radius: 20px; padding: 2rem; margin-bottom: 1rem;
}
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.stDeployButton {display: none;}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a1a; }
::-webkit-scrollbar-thumb { background: linear-gradient(#E91E8C, #7B2FBE); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "authenticated": False, "drive_service": None,
    "root_folder_id": None, "current_page": "🏠 Home",
    "selected_album": None, "drive_connected": False,
    "favorites": set(), "slideshow_index": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ============================================================
# BOTTOM NAV BAR (Always Visible)
# ============================================================
def render_bottom_nav():
    page = st.session_state.current_page
    nav_items = [
        ("🏠", "Home",      "🏠 Home"),
        ("🖼️", "Gallery",   "🖼️ Gallery"),
        ("📁", "Albums",    "📁 Albums"),
        ("⬆️", "Upload",    "⬆️ Upload"),
        ("🗓️", "Timeline",  "🗓️ Timeline"),
        ("💛", "Favs",      "💛 Favorites"),
        ("🎬", "Slideshow", "🎬 Slideshow"),
    ]
    cols = st.columns(len(nav_items))
    for col, (icon, label, page_key) in zip(cols, nav_items):
        with col:
            is_active = page == page_key
            btn_label = f"{icon}\n{label}" if not is_active else f"{icon}\n**{label}**"
            if st.button(icon, key=f"bnav_{page_key}", help=label, use_container_width=True):
                st.session_state.current_page = page_key
                st.session_state.selected_album = None
                st.rerun()


# ============================================================
# HELPERS
# ============================================================
def get_greeting():
    h = datetime.now().hour
    if h < 12:   return "Good Morning", "☀️"
    elif h < 17: return "Good Afternoon", "🌤️"
    else:        return "Good Evening", "🌙"


def connect_drive():
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


def display_media_card(file, service, show_fav=True):
    from google_drive_helper import download_file
    mime = file.get("mimeType", "")
    name = file.get("name", "Unknown")
    fid  = file["id"]
    is_fav = fid in st.session_state.favorites
    st.markdown('<div class="media-card">', unsafe_allow_html=True)
    try:
        if "image" in mime:
            thumb = file.get("thumbnailLink")
            if thumb:
                st.image(thumb.replace("s220", "s400"), use_container_width=True)
            else:
                st.image(download_file(service, fid), use_container_width=True)
        elif "video" in mime:
            st.video(download_file(service, fid))
    except Exception:
        st.markdown("<div style='color:#a0a0c0;text-align:center;padding:2rem;font-size:2rem;'>🖼️</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="media-name">📄 {name}</div>', unsafe_allow_html=True)
    with col2:
        if show_fav:
            fav_icon = "💛" if is_fav else "🤍"
            if st.button(fav_icon, key=f"fav_{fid}_{name}", help="Toggle Favorite"):
                if fid in st.session_state.favorites:
                    st.session_state.favorites.discard(fid)
                else:
                    st.session_state.favorites.add(fid)
                st.rerun()
    try:
        fb = download_file(service, fid)
        st.download_button("⬇️", data=fb, file_name=name, mime=mime, key=f"dl_{fid}_{name}", use_container_width=True)
    except Exception:
        pass
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# PAGE: LOGIN
# ============================================================
def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown(f"""
        <div class="login-card">
            <span class="login-emoji">💖</span>
            <div class="login-title">{APP_NAME}</div>
            <div class="login-subtitle">{APP_SUBTITLE}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 Family Password", type="password", placeholder="Enter your family password...")
        if st.button("✨ Enter Our World", use_container_width=True):
            if pwd == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password!")
        st.markdown("<p style='color:#505070;font-size:0.8rem;text-align:center;margin-top:1rem;'>🔒 Private — Family Only</p>", unsafe_allow_html=True)


# ============================================================
# PAGE: CONNECT DRIVE
# ============================================================
def connect_drive_page():
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="login-card">
            <span class="login-emoji">☁️</span>
            <div class="login-title">Connect Drive</div>
            <div class="login-subtitle">Connect your Google Drive to store memories</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if not os.path.exists(CREDENTIALS_FILE):
            st.error(f"⚠️ `{CREDENTIALS_FILE}` not found!")
        else:
            if st.button("🔗 Connect to Google Drive", use_container_width=True):
                with st.spinner("Connecting..."):
                    if connect_drive():
                        st.success("✅ Connected!")
                        st.balloons()
                        st.rerun()


# ============================================================
# SIDEBAR
# ============================================================
def sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">💖</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-appname">{APP_NAME}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">Cherish Every Moment</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">📍 Navigation</div>', unsafe_allow_html=True)
        pages = [
            ("🏠 Home",      "🏠 Home"),
            ("🖼️ Gallery",   "🖼️ Gallery"),
            ("📁 Albums",    "📁 Albums"),
            ("⬆️ Upload",    "⬆️ Upload"),
            ("🗓️ Timeline",  "🗓️ Timeline"),
            ("💛 Favorites", "💛 Favorites"),
            ("🎬 Slideshow", "🎬 Slideshow"),
            ("ℹ️ About",     "ℹ️ About"),
        ]
        for label, key in pages:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.session_state.selected_album = None
                st.rerun()
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">💾 Storage</div>', unsafe_allow_html=True)
        if st.session_state.drive_service:
            try:
                from google_drive_helper import get_storage_info
                used, total = get_storage_info(st.session_state.drive_service)
                if total > 0:
                    st.progress(min(used / total, 1.0))
                    st.markdown(f"<small style='color:#606080'>{used} GB / {total} GB</small>", unsafe_allow_html=True)
            except Exception:
                pass
        fav_count = len(st.session_state.favorites)
        if fav_count > 0:
            st.markdown(f"<div class='info-chip'>💛 {fav_count} Favorites</div>", unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ============================================================
# PAGE: HOME
# ============================================================
def home_page():
    from google_drive_helper import list_files, list_folders
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id
    greeting, emoji = get_greeting()
    now_str = datetime.now().strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div class="greeting-banner">
        <div class="greeting-time">{emoji} {now_str}</div>
        <div class="greeting-main">{greeting}, Family! 💖</div>
        <div class="greeting-sub">Welcome back to your beautiful family memories</div>
    </div>
    """, unsafe_allow_html=True)
    all_files = list_files(service, root_id)
    folders   = list_folders(service, root_id)
    photos    = [f for f in all_files if "image" in f.get("mimeType", "")]
    videos    = [f for f in all_files if "video" in f.get("mimeType", "")]
    s1, s2, s3, s4 = st.columns(4)
    for col, icon, val, label, clr in zip(
        [s1, s2, s3, s4],
        ["📸", "🎬", "📁", "💛"],
        [len(photos), len(videos), len(folders), len(st.session_state.favorites)],
        ["Photos", "Videos", "Albums", "Favorites"],
        ["#E91E8C", "#7B2FBE", "#FFD700", "#00ff88"]
    ):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <span class="stat-icon">{icon}</span>
                <div class="stat-number" style="background:linear-gradient(90deg,{clr},#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-title">⚡ Quick Actions</span></div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    for col, (icon, label, page_key) in zip([q1, q2, q3, q4], [
        ("📤", "Upload", "⬆️ Upload"), ("🖼️", "Gallery", "🖼️ Gallery"),
        ("📁", "Albums", "📁 Albums"), ("🎬", "Slideshow", "🎬 Slideshow")
    ]):
        with col:
            st.markdown(f"""<div class="quick-action">
                <span class="quick-icon">{icon}</span>
                <div class="quick-label">{label}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(label, key=f"qa_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    if all_files:
        st.markdown(f'<div class="section-header"><span class="section-title">🌟 Recent Memories</span><span class="section-badge">{min(len(all_files),6)} shown</span></div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, f in enumerate(all_files[:6]):
            with cols[i % 3]:
                display_media_card(f, service)
    else:
        st.markdown("""
        <div style="text-align:center;padding:4rem;color:#505070;">
            <div style="font-size:5rem;">📭</div>
            <div style="font-size:1.2rem;font-weight:600;color:#a0a0c0;margin-top:1rem;">No memories yet!</div>
            <div style="color:#606080;margin-top:0.5rem;">Start uploading your precious moments</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE: GALLERY
# ============================================================
def gallery_page():
    from google_drive_helper import list_files
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id
    st.markdown('<div class="section-header"><span class="section-title">🖼️ Gallery</span></div>', unsafe_allow_html=True)
    with st.spinner("Loading memories..."):
        all_files = list_files(service, root_id)
    c1, c2, c3 = st.columns([2, 1.5, 1])
    with c1:
        search = st.text_input("🔍 Search photos...", placeholder="Type filename to search...")
    with c2:
        filter_opt = st.selectbox("Filter", ["All 📸🎬", "Photos Only 📸", "Videos Only 🎬", "Favorites 💛"])
    with c3:
        sort_opt = st.selectbox("Sort", ["Latest First", "Oldest First", "By Name"])
    files = all_files
    if search:
        files = [f for f in files if search.lower() in f.get("name", "").lower()]
    if "Photos" in filter_opt:
        files = [f for f in files if "image" in f.get("mimeType", "")]
    elif "Videos" in filter_opt:
        files = [f for f in files if "video" in f.get("mimeType", "")]
    elif "Favorites" in filter_opt:
        files = [f for f in files if f["id"] in st.session_state.favorites]
    if sort_opt == "Oldest First":
        files = sorted(files, key=lambda x: x.get("createdTime", ""))
    elif sort_opt == "By Name":
        files = sorted(files, key=lambda x: x.get("name", "").lower())
    st.markdown(f'<div style="margin-bottom:1rem;"><span class="info-chip">📊 {len(files)} items</span></div>', unsafe_allow_html=True)
    if not files:
        st.info("📭 No media found.")
        return
    cols = st.columns(3)
    for i, f in enumerate(files):
        with cols[i % 3]:
            display_media_card(f, service)


# ============================================================
# PAGE: ALBUMS
# ============================================================
def albums_page():
    from google_drive_helper import list_folders, list_files, create_folder
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id

    if st.session_state.selected_album:
        album = st.session_state.selected_album
        # === BREADCRUMB ===
        st.markdown(f"""
        <div class="breadcrumb">
            <span class="breadcrumb-item">📁 Albums</span>
            <span class="breadcrumb-sep">›</span>
            <span class="breadcrumb-item active">📂 {album['name']}</span>
        </div>
        """, unsafe_allow_html=True)
        # === BACK BUTTON ===
        col_back, col_title = st.columns([1, 5])
        with col_back:
            if st.button("⬅️ Back", use_container_width=True, help="Go back to Albums"):
                st.session_state.selected_album = None
                st.rerun()
        with col_title:
            st.markdown(f'<div class="section-header"><span class="section-title">📂 {album["name"]}</span></div>', unsafe_allow_html=True)
        files = list_files(service, album["id"])
        if not files:
            st.info("📭 This album is empty.")
        else:
            st.markdown(f'<span class="info-chip">📊 {len(files)} items</span><br><br>', unsafe_allow_html=True)
            cols = st.columns(3)
            for i, f in enumerate(files):
                with cols[i % 3]:
                    display_media_card(f, service)
        return

    # === ALBUMS LIST ===
    # breadcrumb for root level
    st.markdown("""
    <div class="breadcrumb">
        <span class="breadcrumb-item active">📁 Albums</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="section-title">📁 Albums</span></div>', unsafe_allow_html=True)
    with st.expander("➕ Create New Album"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_name = st.text_input("Album Name", placeholder="e.g. 🎂 Birthday 2024")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create ✅"):
                if new_name.strip():
                    with st.spinner("Creating..."):
                        create_folder(service, new_name.strip(), root_id)
                    st.success(f"✅ '{new_name}' created!")
                    st.rerun()
    folders = list_folders(service, root_id)
    if not folders:
        st.info("📭 No albums yet.")
        return
    cols = st.columns(4)
    for i, folder in enumerate(folders):
        with cols[i % 4]:
            count = len(list_files(service, folder["id"]))
            st.markdown(f"""
            <div class="album-card">
                <span class="album-emoji">📂</span>
                <div class="album-name">{folder['name']}</div>
                <span class="album-count">{count} items</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open 📂", key=f"open_{folder['id']}", use_container_width=True):
                st.session_state.selected_album = folder
                st.rerun()


# ============================================================
# PAGE: UPLOAD
# ============================================================
def upload_page():
    from google_drive_helper import list_folders, upload_file
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id
    st.markdown('<div class="section-header"><span class="section-title">⬆️ Upload Memories</span></div>', unsafe_allow_html=True)
    folders = list_folders(service, root_id)
    folder_options = {"📁 Root (Family Memories)": root_id}
    for f in folders:
        folder_options[f"📂 {f['name']}"] = f["id"]
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_folder = st.selectbox("📁 Upload to Album", list(folder_options.keys()))
    target_id = folder_options[selected_folder]
    st.markdown("""
    <div class="upload-area">
        <span class="upload-icon">📤</span>
        <div class="upload-text">Drop your photos & videos here</div>
        <div class="upload-subtext">Supports JPG, PNG, GIF, WEBP, MP4, MOV, AVI, MKV</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose files", type=IMAGE_TYPES + VIDEO_TYPES, accept_multiple_files=True, label_visibility="collapsed")
    if uploaded:
        st.markdown(f'<span class="info-chip">📎 {len(uploaded)} file(s) selected</span>', unsafe_allow_html=True)
        prev_cols = st.columns(min(len(uploaded), 4))
        for i, uf in enumerate(uploaded[:4]):
            with prev_cols[i]:
                if uf.type.startswith("image"):
                    st.image(uf, use_container_width=True, caption=uf.name[:15])
                else:
                    st.markdown(f'<div style="text-align:center;padding:1rem;background:rgba(123,47,190,0.1);border-radius:10px;color:#a0a0c0;">🎬<br>{uf.name[:15]}</div>', unsafe_allow_html=True)
        if st.button("⬆️ Upload All to Google Drive 🚀", use_container_width=True):
            progress = st.progress(0)
            status   = st.empty()
            ok = 0
            for idx, uf in enumerate(uploaded):
                status.markdown(f'<span class="info-chip">Uploading: {uf.name}</span>', unsafe_allow_html=True)
                try:
                    mt, _ = mimetypes.guess_type(uf.name)
                    upload_file(service, uf.read(), uf.name, mt or "application/octet-stream", target_id)
                    ok += 1
                except Exception as e:
                    st.error(f"❌ {uf.name}: {e}")
                progress.progress((idx + 1) / len(uploaded))
            status.empty()
            st.success(f"✅ {ok}/{len(uploaded)} uploaded successfully!")
            st.balloons()


# ============================================================
# PAGE: TIMELINE
# ============================================================
def timeline_page():
    from google_drive_helper import list_files
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id
    st.markdown('<div class="section-header"><span class="section-title">🗓️ Timeline</span></div>', unsafe_allow_html=True)
    with st.spinner("Building your timeline..."):
        all_files = list_files(service, root_id)
    if not all_files:
        st.info("📭 No memories found.")
        return
    groups = {}
    for f in all_files:
        ct = f.get("createdTime", "")
        try:
            dt  = datetime.strptime(ct[:10], "%Y-%m-%d")
            key = dt.strftime("%B %Y")
        except Exception:
            key = "Unknown Date"
        groups.setdefault(key, []).append(f)
    for month_label, files in groups.items():
        st.markdown(f'<div class="timeline-month">📅 {month_label} · {len(files)} memories</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, f in enumerate(files):
            with cols[i % 3]:
                display_media_card(f, service)
        st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# PAGE: FAVORITES
# ============================================================
def favorites_page():
    from google_drive_helper import list_files
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id
    st.markdown('<div class="section-header"><span class="section-title">💛 Favorites</span></div>', unsafe_allow_html=True)
    if not st.session_state.favorites:
        st.markdown("""
        <div style="text-align:center;padding:4rem;color:#505070;">
            <div style="font-size:5rem;">💛</div>
            <div style="font-size:1.2rem;font-weight:600;color:#a0a0c0;margin-top:1rem;">No favorites yet!</div>
            <div style="color:#606080;margin-top:0.5rem;">Tap 🤍 on any photo to add it here</div>
        </div>
        """, unsafe_allow_html=True)
        return
    all_files = list_files(service, root_id)
    favs = [f for f in all_files if f["id"] in st.session_state.favorites]
    st.markdown(f'<span class="info-chip">💛 {len(favs)} favorites</span><br><br>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, f in enumerate(favs):
        with cols[i % 3]:
            display_media_card(f, service)


# ============================================================
# PAGE: SLIDESHOW
# ============================================================
def slideshow_page():
    from google_drive_helper import list_files, download_file
    service = st.session_state.drive_service
    root_id = st.session_state.root_folder_id
    st.markdown('<div class="section-header"><span class="section-title">🎬 Slideshow</span></div>', unsafe_allow_html=True)
    all_files = list_files(service, root_id)
    photos = [f for f in all_files if "image" in f.get("mimeType", "")]
    if not photos:
        st.info("📭 No photos found for slideshow.")
        return
    total   = len(photos)
    idx     = st.session_state.slideshow_index % total
    current = photos[idx]
    st.markdown(f'<span class="info-chip">📸 {idx+1} of {total} photos</span><br><br>', unsafe_allow_html=True)
    st.markdown('<div class="slideshow-container">', unsafe_allow_html=True)
    try:
        thumb = current.get("thumbnailLink")
        if thumb:
            st.image(thumb.replace("s220", "s800"), use_container_width=True)
        else:
            st.image(download_file(service, current["id"]), use_container_width=True)
    except Exception:
        st.markdown("<div style='padding:3rem;text-align:center;color:#a0a0c0;font-size:3rem;'>🖼️</div>", unsafe_allow_html=True)
    st.markdown(f'<div class="slideshow-name">📄 {current.get("name","")}</div>', unsafe_allow_html=True)
    ct = current.get("createdTime", "")
    if ct:
        try:
            dt = datetime.strptime(ct[:10], "%Y-%m-%d").strftime("%d %B %Y")
            st.markdown(f'<div class="slideshow-counter">📅 {dt}</div>', unsafe_allow_html=True)
        except Exception:
            pass
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
    with c1:
        if st.button("⏮️ First"):
            st.session_state.slideshow_index = 0
            st.rerun()
    with c2:
        if st.button("◀️ Prev"):
            st.session_state.slideshow_index = (idx - 1) % total
            st.rerun()
    with c3:
        st.markdown(f'<div style="text-align:center;color:#a0a0c0;padding-top:0.5rem;">{idx+1} / {total}</div>', unsafe_allow_html=True)
    with c4:
        if st.button("Next ▶️"):
            st.session_state.slideshow_index = (idx + 1) % total
            st.rerun()
    with c5:
        if st.button("Last ⏭️"):
            st.session_state.slideshow_index = total - 1
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        fb = download_file(service, current["id"])
        st.download_button("⬇️ Download This Photo", data=fb, file_name=current.get("name", "photo.jpg"), use_container_width=True)
    except Exception:
        pass


# ============================================================
# PAGE: ABOUT
# ============================================================
def about_page():
    st.markdown('<div class="section-header"><span class="section-title">ℹ️ About</span></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="about-card">
        <h2 style="background:linear-gradient(90deg,#E91E8C,#7B2FBE,#FFD700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:1.8rem;font-weight:800;">💖 {APP_NAME}</h2>
        <p style="color:#a0a0c0;margin-bottom:1.5rem;">{APP_SUBTITLE}</p>
        <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:1.5rem;">
            <span class="info-chip">🐍 Python</span>
            <span class="info-chip">🚀 Streamlit</span>
            <span class="info-chip">☁️ Google Drive</span>
            <span class="info-chip">🔐 OAuth 2.0</span>
            <span class="info-chip">🎨 Glassmorphism UI</span>
        </div>
        <h4 style="color:#ff6b9d;margin-bottom:1rem;">✨ Features</h4>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">
            <div style="color:#c0c0d8;">📸 Photo Gallery</div>
            <div style="color:#c0c0d8;">🎬 Video Player</div>
            <div style="color:#c0c0d8;">⬆️ Easy Upload</div>
            <div style="color:#c0c0d8;">📁 Album Management</div>
            <div style="color:#c0c0d8;">🗓️ Timeline View</div>
            <div style="color:#c0c0d8;">💛 Favorites</div>
            <div style="color:#c0c0d8;">🎬 Slideshow Mode</div>
            <div style="color:#c0c0d8;">🔍 Search & Filter</div>
            <div style="color:#c0c0d8;">⬇️ Download</div>
            <div style="color:#c0c0d8;">🔒 Password Protected</div>
            <div style="color:#c0c0d8;">⬅️ Back Navigation</div>
            <div style="color:#c0c0d8;">📍 Bottom Nav Bar</div>
        </div>
        <hr style="border-color:rgba(233,30,140,0.15);margin:1.5rem 0;">
        <p style="color:#505070;font-size:0.85rem;text-align:center;">Made with ❤️ using Python & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MAIN
# ============================================================
def main():
    if not st.session_state.authenticated:
        login_page()
        return

    if not st.session_state.drive_connected or st.session_state.drive_service is None:
        from google_drive_helper import is_authenticated
        if is_authenticated():
            with st.spinner("Connecting to your memories..."):
                connect_drive()
            st.rerun()
        else:
            connect_drive_page()
        return

    sidebar()

    # ==== BOTTOM NAV BAR =====
    st.markdown("---")
    st.markdown("**📍 Quick Navigate:**")
    render_bottom_nav()
    st.markdown("---")

    page = st.session_state.current_page
    if page == "🏠 Home":         home_page()
    elif page == "🖼️ Gallery":    gallery_page()
    elif page == "📁 Albums":     albums_page()
    elif page == "⬆️ Upload":     upload_page()
    elif page == "🗓️ Timeline":   timeline_page()
    elif page == "💛 Favorites":  favorites_page()
    elif page == "🎬 Slideshow":  slideshow_page()
    elif page == "ℹ️ About":      about_page()


if __name__ == "__main__":
    main()
