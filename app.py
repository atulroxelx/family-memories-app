try:
    from setup_secrets import setup_credentials
    setup_credentials()
except Exception:
    pass

import streamlit as st
import os, mimetypes, random
from datetime import datetime, date
from config import (APP_NAME, APP_ICON, APP_SUBTITLE, APP_PASSWORD,
    IMAGE_TYPES, VIDEO_TYPES, GRID_COLUMNS, CREDENTIALS_FILE, TOKEN_FILE)

st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON,
    layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Poppins', sans-serif !important; }
html, body, [class*="css"] { background:#0a0a1a !important; color:#ffffff !important; }
.stApp { background:linear-gradient(135deg,#0a0a1a 0%,#0d0d2b 50%,#0a0a1a 100%) !important; padding-bottom:85px !important; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
@keyframes gshift { 0%{background-position:0% center} 100%{background-position:200% center} }
.gtxt { background:linear-gradient(90deg,#E91E8C,#7B2FBE,#FFD700,#E91E8C); background-size:200%; -webkit-background-clip:text; -webkit-text-fill-color:transparent; animation:gshift 3s linear infinite; }
.glass { background:rgba(255,255,255,0.04); border:1px solid rgba(233,30,140,0.22); border-radius:18px; padding:1.4rem; backdrop-filter:blur(20px); transition:all .3s ease; }
.glass:hover { border-color:rgba(233,30,140,0.6); box-shadow:0 0 28px rgba(233,30,140,0.2); transform:translateY(-4px); }
.login-card { background:rgba(255,255,255,0.04); border:1px solid rgba(233,30,140,0.3); border-radius:28px; padding:3rem; text-align:center; backdrop-filter:blur(28px); max-width:430px; margin:auto; box-shadow:0 20px 70px rgba(233,30,140,0.15); }
.lemoji { font-size:4.5rem; display:block; animation:float 3s ease-in-out infinite; margin-bottom:.8rem; }
.ltitle { font-size:2rem; font-weight:800; background:linear-gradient(90deg,#E91E8C,#ff6b9d,#7B2FBE); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.lsub { color:#a0a0c0; font-size:.88rem; margin-bottom:1.5rem; }
.scard { background:rgba(255,255,255,0.04); border:1px solid rgba(233,30,140,0.2); border-radius:16px; padding:1.2rem; text-align:center; transition:all .3s ease; }
.scard:hover { transform:translateY(-6px); box-shadow:0 0 32px rgba(233,30,140,0.25); }
.sicon { font-size:2rem; display:block; margin-bottom:.4rem; }
.snum { font-size:2rem; font-weight:900; background:linear-gradient(90deg,#E91E8C,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.slbl { color:#a0a0c0; font-size:.78rem; margin-top:.2rem; }
.mcard { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; overflow:hidden; transition:all .3s ease; margin-bottom:.8rem; }
.mcard:hover { border-color:rgba(233,30,140,0.5); box-shadow:0 0 20px rgba(233,30,140,0.18); transform:scale(1.015); }
.mname { color:#c0c0d8; font-size:.72rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; padding:.25rem .5rem; }
.acard { background:linear-gradient(135deg,rgba(233,30,140,0.08),rgba(123,47,190,0.08)); border:1px solid rgba(233,30,140,0.22); border-radius:16px; padding:1.5rem 1rem; text-align:center; transition:all .3s ease; margin-bottom:.8rem; }
.acard:hover { transform:translateY(-6px); border-color:#E91E8C; box-shadow:0 0 32px rgba(233,30,140,0.25); }
.aemoji { font-size:2.5rem; display:block; margin-bottom:.5rem; }
.aname { color:#fff; font-weight:700; font-size:.9rem; }
.abadge { display:inline-block; background:rgba(233,30,140,0.18); border:1px solid rgba(233,30,140,0.3); border-radius:20px; padding:.1rem .55rem; color:#ff6b9d; font-size:.7rem; font-weight:600; }
.bc { display:flex; align-items:center; gap:.45rem; background:rgba(233,30,140,0.07); border:1px solid rgba(233,30,140,0.2); border-radius:10px; padding:.45rem .9rem; margin-bottom:1rem; font-size:.8rem; }
.bci { color:#a0a0c0; } .bca { color:#ff6b9d; font-weight:600; } .bcs { color:rgba(233,30,140,0.4); }
.shdr { display:flex; align-items:center; gap:.55rem; margin-bottom:1.1rem; padding-bottom:.55rem; border-bottom:1px solid rgba(233,30,140,0.2); }
.stitle { font-size:1.25rem; font-weight:700; background:linear-gradient(90deg,#E91E8C,#ff6b9d); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0; }
.sbadge { background:rgba(233,30,140,0.12); border:1px solid rgba(233,30,140,0.25); border-radius:20px; padding:.1rem .65rem; color:#ff6b9d; font-size:.73rem; }
.chip { display:inline-block; background:rgba(233,30,140,0.1); border:1px solid rgba(233,30,140,0.22); border-radius:20px; padding:.18rem .65rem; color:#ff6b9d; font-size:.75rem; margin:.12rem; }
.tag { display:inline-block; background:rgba(123,47,190,0.15); border:1px solid rgba(123,47,190,0.28); border-radius:20px; padding:.08rem .5rem; color:#c084fc; font-size:.66rem; margin:.08rem; }
.cbox { background:rgba(255,255,255,0.03); border:1px solid rgba(233,30,140,0.15); border-radius:8px; padding:.5rem; margin-top:.35rem; font-size:.76rem; color:#a0a0c0; }
.chall { background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(233,30,140,0.08)); border:1px solid rgba(255,215,0,0.28); border-radius:16px; padding:1.2rem; margin-bottom:1.1rem; }
.otdbanner { background:linear-gradient(135deg,rgba(255,215,0,0.12),rgba(233,30,140,0.1)); border:2px solid rgba(255,215,0,0.3); border-radius:16px; padding:1.2rem; margin-bottom:1.1rem; text-align:center; }
.gbanner { background:linear-gradient(135deg,rgba(233,30,140,0.12),rgba(123,47,190,0.12)); border:1px solid rgba(233,30,140,0.22); border-radius:16px; padding:1.5rem 1.8rem; margin-bottom:1.1rem; position:relative; overflow:hidden; }
.gbanner::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#E91E8C,#7B2FBE,#FFD700); }
.gtime { color:#a0a0c0; font-size:.8rem; }
.gmain { font-size:1.4rem; font-weight:800; background:linear-gradient(90deg,#E91E8C,#ff6b9d,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.gsub { color:#c0c0d8; font-size:.88rem; }
.qact { background:linear-gradient(135deg,rgba(233,30,140,0.1),rgba(123,47,190,0.1)); border:1px solid rgba(233,30,140,0.22); border-radius:12px; padding:.9rem; text-align:center; transition:all .3s ease; }
.qact:hover { transform:translateY(-4px); box-shadow:0 0 22px rgba(233,30,140,0.25); }
.qicon { font-size:1.6rem; display:block; }
.qlbl { color:#c0c0d8; font-size:.78rem; font-weight:600; margin-top:.25rem; }
.uarea { background:rgba(233,30,140,0.03); border:2px dashed rgba(233,30,140,0.38); border-radius:16px; padding:2.2rem; text-align:center; margin-bottom:1.1rem; }
.thdr { background:rgba(233,30,140,0.07); border-left:3px solid #E91E8C; border-radius:0 8px 8px 0; padding:.45rem .9rem; margin-bottom:.7rem; color:#ff6b9d; font-weight:700; }
.sswrap { background:rgba(0,0,0,0.35); border:1px solid rgba(233,30,140,0.25); border-radius:16px; padding:.8rem; text-align:center; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0d0d25 0%,#0a0a1a 100%) !important; border-right:1px solid rgba(233,30,140,0.18) !important; }
[data-testid="stSidebar"] .stButton>button { background:transparent !important; border:1px solid rgba(233,30,140,0.14) !important; border-radius:9px !important; color:#c0c0d8 !important; text-align:left !important; padding:.45rem .9rem !important; box-shadow:none !important; font-weight:500 !important; }
[data-testid="stSidebar"] .stButton>button:hover { background:rgba(233,30,140,0.14) !important; border-color:rgba(233,30,140,0.38) !important; color:#ff6b9d !important; transform:translateX(4px) !important; box-shadow:none !important; }
.stButton>button { background:linear-gradient(135deg,#E91E8C,#7B2FBE) !important; color:white !important; border:none !important; border-radius:10px !important; padding:.5rem 1.2rem !important; font-weight:600 !important; transition:all .3s ease !important; box-shadow:0 4px 14px rgba(233,30,140,0.28) !important; }
.stButton>button:hover { transform:translateY(-2px) !important; box-shadow:0 7px 20px rgba(233,30,140,0.42) !important; }
.stTextInput>div>div>input { background:rgba(255,255,255,0.06) !important; border:1px solid rgba(233,30,140,0.28) !important; border-radius:9px !important; color:white !important; }
.stTextInput>div>div>input:focus { border-color:#E91E8C !important; box-shadow:0 0 16px rgba(233,30,140,0.28) !important; }
.stSelectbox>div>div { background:rgba(255,255,255,0.06) !important; border:1px solid rgba(233,30,140,0.28) !important; border-radius:9px !important; }
.stProgress>div>div>div>div { background:linear-gradient(90deg,#E91E8C,#7B2FBE) !important; border-radius:6px !important; }
[data-testid="collapsedControl"] { background:linear-gradient(135deg,#E91E8C,#7B2FBE) !important; border-radius:0 10px 10px 0 !important; box-shadow:4px 0 16px rgba(233,30,140,0.42) !important; }
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}.stDeployButton{display:none;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:#0a0a1a;}::-webkit-scrollbar-thumb{background:linear-gradient(#E91E8C,#7B2FBE);border-radius:3px;}
.slogo{text-align:center;padding:1.1rem 0 .35rem;font-size:2.6rem;animation:float 3s ease-in-out infinite;}
.sname{text-align:center;font-size:.88rem;font-weight:700;background:linear-gradient(90deg,#E91E8C,#7B2FBE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.stag{text-align:center;color:#505070;font-size:.66rem;margin-bottom:.9rem;}
.sdiv{height:1px;background:linear-gradient(90deg,transparent,rgba(233,30,140,0.28),transparent);margin:.65rem 0;}
.slabel{color:#505070;font-size:.66rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;padding:.22rem 0;}
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────
_defs = {
    "authenticated": False, "drive_service": None, "root_folder_id": None,
    "current_page": "🏠 Home", "selected_album": None, "drive_connected": False,
    "favorites": set(), "slideshow_index": 0, "comments": {}, "reactions": {},
    "votes": {}, "trash": set(), "capsules": [], "theme": "dark",
    "language": "English", "secret_password": "secret123",
    "secret_unlocked": False, "view_counts": {},
}
for _k, _v in _defs.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── TRANSLATIONS ─────────────────────────────────────────────────
_LANG = {
    "English": {"no_mem": "No memories yet! Start uploading.", "back": "⬅️ Back",
                "search": "🔍 Search photos...", "upload_btn": "⬆️ Upload All"},
    "Hindi":   {"no_mem": "अभी तक कोई यादें नहीं!", "back": "⬅️ वापस",
                "search": "🔍 फोटो खोजें...", "upload_btn": "⬆️ सभी अपलोड करें"},
}
def T(key):
    return _LANG.get(st.session_state.language, _LANG["English"]).get(key, key)

# ── HELPERS ──────────────────────────────────────────────────────
def get_greeting():
    h = datetime.now().hour
    if h < 12:   return "Good Morning ☀️"
    elif h < 17: return "Good Afternoon 🌤️"
    else:        return "Good Evening 🌙"

def get_auto_tags(fn):
    fn = fn.lower()
    tags = {"birthday":"🎂","party":"🎉","beach":"🏖️","vacation":"✈️",
            "food":"🍔","wedding":"💍","baby":"👶","school":"🏫",
            "travel":"🗺️","christmas":"🎄","diwali":"🪔","holi":"🎨",
            "family":"👨‍👩‍👧","nature":"🌿","selfie":"🤳"}
    return [f"{v} {k.title()}" for k, v in tags.items() if k in fn]

def connect_drive():
    try:
        from google_drive_helper import authenticate, get_or_create_root_folder
        svc = authenticate()
        rid = get_or_create_root_folder(svc)
        st.session_state.drive_service = svc
        st.session_state.root_folder_id = rid
        st.session_state.drive_connected = True
        return True
    except Exception as e:
        st.error(f"❌ Drive connection failed: {e}")
        return False

def get_visible(files):
    return [f for f in files if f["id"] not in st.session_state.trash]

# ── DISPLAY MEDIA CARD ───────────────────────────────────────────
def display_media_card(file, service, show_actions=True):
    from google_drive_helper import download_file
    mime = file.get("mimeType",""); name = file.get("name","Unknown"); fid = file["id"]
    is_fav = fid in st.session_state.favorites
    st.session_state.view_counts[fid] = st.session_state.view_counts.get(fid,0) + 1
    views = st.session_state.view_counts[fid]
    tags  = get_auto_tags(name)
    rxns  = st.session_state.reactions.get(fid,{})
    votes = st.session_state.votes.get(fid,0)
    st.markdown('<div class="mcard">', unsafe_allow_html=True)
    try:
        if "image" in mime:
            thumb = file.get("thumbnailLink")
            st.image(thumb.replace("s220","s400") if thumb else download_file(service,fid), use_container_width=True)
        elif "video" in mime:
            st.video(download_file(service,fid))
    except Exception:
        st.markdown("<div style='text-align:center;padding:2rem;font-size:2.5rem;'>🖼️</div>", unsafe_allow_html=True)
    st.markdown(f'<div class="mname">📄 {name}</div>', unsafe_allow_html=True)
    if tags:
        st.markdown("".join(f'<span class="tag">{t}</span>' for t in tags), unsafe_allow_html=True)
    st.markdown(f'<div style="padding:.1rem .4rem"><span class="chip">👁️ {views}</span></div>', unsafe_allow_html=True)
    if show_actions:
        EMOJIS = ["❤️","😍","🥹","😂","🎉"]
        st.markdown("".join(f'<span class="chip">{e} {rxns.get(e,0)}</span>' for e in EMOJIS), unsafe_allow_html=True)
        rc1,rc2,rc3 = st.columns(3)
        with rc1:
            if st.button("💛 Unfav" if is_fav else "🤍 Fav", key=f"fv_{fid}_{name}", use_container_width=True):
                if is_fav: st.session_state.favorites.discard(fid)
                else:      st.session_state.favorites.add(fid)
                st.rerun()
        with rc2:
            if st.button(f"👍 {votes}", key=f"vt_{fid}_{name}", use_container_width=True):
                st.session_state.votes[fid] = votes+1; st.rerun()
        with rc3:
            if st.button("🗑️", key=f"tr_{fid}_{name}", use_container_width=True, help="Move to Trash"):
                st.session_state.trash.add(fid); st.rerun()
        re_cols = st.columns(5)
        for idx,em in enumerate(EMOJIS):
            with re_cols[idx]:
                if st.button(em, key=f"rx_{fid}_{em}_{name}", use_container_width=True):
                    if fid not in st.session_state.reactions:
                        st.session_state.reactions[fid] = {}
                    st.session_state.reactions[fid][em] = st.session_state.reactions[fid].get(em,0)+1
                    st.rerun()
        cmts = st.session_state.comments.get(fid,[])
        if cmts:
            for c in cmts[-2:]:
                st.markdown(f'<div class="cbox">💬 <b>{c["name"]}</b>: {c["text"]} <small>· {c["time"]}</small></div>', unsafe_allow_html=True)
        with st.expander("💬 Comment"):
            cn  = st.text_input("Name", key=f"cn_{fid}_{name}", placeholder="Your name")
            ct2 = st.text_input("Comment", key=f"ct_{fid}_{name}", placeholder="Write something...")
            if st.button("Post 📤", key=f"cp_{fid}_{name}"):
                if cn and ct2:
                    if fid not in st.session_state.comments:
                        st.session_state.comments[fid] = []
                    st.session_state.comments[fid].append({"name":cn,"text":ct2,"time":datetime.now().strftime("%b %d %H:%M")})
                    st.rerun()
        try:
            fb = download_file(service,fid)
            st.download_button("⬇️ Download", data=fb, file_name=name, mime=mime, key=f"dl_{fid}_{name}", use_container_width=True)
        except Exception:
            pass
    st.markdown("</div>", unsafe_allow_html=True)

# ── BOTTOM NAV ───────────────────────────────────────────────────
def render_bottom_nav():
    nav = [("🏠","Home","🏠 Home"),("🖼️","Gallery","🖼️ Gallery"),
           ("📁","Albums","📁 Albums"),("⬆️","Upload","⬆️ Upload"),
           ("📅","Today","📅 On This Day"),("💛","Favs","💛 Favorites"),
           ("🎬","Show","🎬 Slideshow"),("📊","Stats","📊 Stats")]
    cols = st.columns(len(nav))
    for col,(icon,lbl,key) in zip(cols,nav):
        with col:
            if st.button(icon, key=f"bn_{key}", help=lbl, use_container_width=True):
                st.session_state.current_page = key
                st.session_state.selected_album = None
                st.rerun()

# ── SIDEBAR ──────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown('<div class="slogo">💖</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sname">{APP_NAME}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stag">Cherish Every Moment ✨</div>', unsafe_allow_html=True)
        st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
        st.markdown('<div class="slabel">📍 Navigate</div>', unsafe_allow_html=True)
        pages = [
            ("🏠 Home","🏠 Home"),("🖼️ Gallery","🖼️ Gallery"),
            ("📁 Albums","📁 Albums"),("⬆️ Upload","⬆️ Upload"),
            ("🗓️ Timeline","🗓️ Timeline"),("💛 Favorites","💛 Favorites"),
            ("🎬 Slideshow","🎬 Slideshow"),("📅 On This Day","📅 On This Day"),
            ("📊 Stats","📊 Stats"),("💌 Capsule","💌 Capsule"),
            ("🗑️ Trash","🗑️ Trash"),("⚙️ Settings","⚙️ Settings"),("ℹ️ About","ℹ️ About"),
        ]
        for lbl,key in pages:
            if st.button(lbl, key=f"sb_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.session_state.selected_album = None
                st.rerun()
        st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
        st.markdown('<div class="slabel">💾 Storage</div>', unsafe_allow_html=True)
        if st.session_state.drive_service:
            try:
                from google_drive_helper import get_storage_info
                used,total = get_storage_info(st.session_state.drive_service)
                if total > 0:
                    st.progress(min(used/total,1.0))
                    st.markdown(f"<small style='color:#606080'>{used} GB / {total} GB used</small>", unsafe_allow_html=True)
            except Exception: pass
        fc = len(st.session_state.favorites)
        tc = len(st.session_state.trash)
        if fc: st.markdown(f"<div class='chip'>💛 {fc} Favorites</div>", unsafe_allow_html=True)
        if tc: st.markdown(f"<div class='chip'>🗑️ {tc} Trash</div>", unsafe_allow_html=True)
        st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

# ── LOGIN PAGE ───────────────────────────────────────────────────
def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown(f'<div class="login-card"><span class="lemoji">💖</span><div class="ltitle">{APP_NAME}</div><div class="lsub">{APP_SUBTITLE}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        pwd = st.text_input("🔑 Family Password", type="password", placeholder="Enter family password...")
        if st.button("✨ Enter Our World", use_container_width=True):
            if pwd == APP_PASSWORD: st.session_state.authenticated=True; st.rerun()
            else: st.error("❌ Incorrect password!")
        st.markdown("<p style='color:#505070;font-size:.75rem;text-align:center;margin-top:.7rem;'>🔒 Private — Family Only</p>", unsafe_allow_html=True)

# ── CONNECT DRIVE PAGE ───────────────────────────────────────────
def connect_drive_page():
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown('<div class="login-card"><span class="lemoji">☁️</span><div class="ltitle">Connect Drive</div><div class="lsub">Link Google Drive to store your memories</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if not os.path.exists(CREDENTIALS_FILE):
            st.error(f"⚠️ `{CREDENTIALS_FILE}` not found! Follow README setup.")
        else:
            if st.button("🔗 Connect to Google Drive", use_container_width=True):
                with st.spinner("Connecting..."):
                    if connect_drive(): st.success("✅ Connected!"); st.balloons(); st.rerun()

# ── HOME PAGE ────────────────────────────────────────────────────
def home_page():
    from google_drive_helper import list_files, list_folders
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    all_files = list_files(svc,rid); folders = list_folders(svc,rid)
    visible = get_visible(all_files)
    photos  = [f for f in visible if "image" in f.get("mimeType","")]
    videos  = [f for f in visible if "video" in f.get("mimeType","")]
    now_str = datetime.now().strftime("%A, %d %B %Y")
    st.markdown(f'<div class="gbanner"><div class="gtime">📅 {now_str}</div><div class="gmain">{get_greeting()}, Family! 💖</div><div class="gsub">Welcome back — your memories are waiting 🌟</div></div>', unsafe_allow_html=True)
    s1,s2,s3,s4 = st.columns(4)
    for col,icon,val,lbl,clr in zip([s1,s2,s3,s4],["📸","🎬","📁","💛"],
        [len(photos),len(videos),len(folders),len(st.session_state.favorites)],
        ["Photos","Videos","Albums","Favorites"],["#E91E8C","#7B2FBE","#FFD700","#00ff88"]):
        with col:
            st.markdown(f'<div class="scard"><span class="sicon">{icon}</span><div class="snum" style="background:linear-gradient(90deg,{clr},#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{val}</div><div class="slbl">{lbl}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    today = date.today()
    otd = [f for f in visible if f.get("createdTime","")[:10][5:] == today.strftime("%m-%d")]
    if otd:
        st.markdown(f'<div class="otdbanner"><div style="font-size:2rem;">📅</div><div style="font-size:1rem;font-weight:700;color:#FFD700;">On This Day in the Past</div><div style="color:#a0a0c0;font-size:.82rem;">{len(otd)} memory from today\'s date in previous years!</div></div>', unsafe_allow_html=True)
        if st.button("🌟 View On This Day Memories"):
            st.session_state.current_page = "📅 On This Day"; st.rerun()
    if photos:
        random.seed(str(today))
        daily = random.choice(photos)
        st.markdown('<div class="shdr"><span class="stitle">🌅 Daily Memory</span><span class="sbadge">Picked for today</span></div>', unsafe_allow_html=True)
        dc1,dc2 = st.columns([1,2])
        with dc1:
            try:
                thumb = daily.get("thumbnailLink")
                st.image(thumb.replace("s220","s400") if thumb else daily["id"], use_container_width=True)
            except Exception: pass
        with dc2:
            st.markdown(f"<div style='color:#ff6b9d;font-weight:700;'>📄 {daily.get('name','')}</div>", unsafe_allow_html=True)
            ct = daily.get("createdTime","")[:10]
            if ct: st.markdown(f"<div style='color:#a0a0c0;font-size:.82rem;'>📅 {ct}</div>", unsafe_allow_html=True)
            tags = get_auto_tags(daily.get("name",""))
            if tags: st.markdown("".join(f'<span class="tag">{t}</span>' for t in tags), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    challenges = ["📸 Upload your best smile photo this week!","🌅 Share a beautiful sunrise/sunset memory!","👨‍👩‍👧 Upload a family group photo!","🍽️ Share your favourite family meal moment!","🎉 Upload your most fun celebration photo!"]
    chall = challenges[today.isocalendar()[1] % len(challenges)]
    st.markdown(f'<div class="chall"><div style="font-size:1.4rem;">🏆</div><div style="font-weight:700;color:#FFD700;font-size:.95rem;margin-top:.3rem;">This Week\'s Family Challenge</div><div style="color:#e0e0c0;font-size:.85rem;margin-top:.3rem;">{chall}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="shdr"><span class="stitle">⚡ Quick Actions</span></div>', unsafe_allow_html=True)
    acts = [("📤","Upload","⬆️ Upload"),("🖼️","Gallery","🖼️ Gallery"),("📁","Albums","📁 Albums"),("🎬","Slideshow","🎬 Slideshow"),("📅","On This Day","📅 On This Day"),("📊","Stats","📊 Stats")]
    qs = st.columns(6)
    for col,(icon,lbl,pg) in zip(qs,acts):
        with col:
            st.markdown(f'<div class="qact"><span class="qicon">{icon}</span><div class="qlbl">{lbl}</div></div>', unsafe_allow_html=True)
            if st.button(lbl, key=f"qa_{pg}", use_container_width=True):
                st.session_state.current_page = pg; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    if visible:
        st.markdown(f'<div class="shdr"><span class="stitle">🌟 Recent Memories</span><span class="sbadge">{min(len(visible),6)} shown</span></div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i,f in enumerate(visible[:6]):
            with cols[i%3]: display_media_card(f,svc)
    else:
        st.markdown(f"<div style='text-align:center;padding:3rem;color:#505070;'>📭 {T('no_mem')}</div>", unsafe_allow_html=True)

# ── GALLERY PAGE ─────────────────────────────────────────────────
def gallery_page():
    from google_drive_helper import list_files
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">🖼️ Gallery</span></div>', unsafe_allow_html=True)
    with st.spinner("Loading memories..."): all_files = list_files(svc,rid)
    visible = get_visible(all_files)
    c1,c2,c3,c4 = st.columns([2,1.2,1.2,1.2])
    with c1: search = st.text_input("", placeholder=T("search"), label_visibility="collapsed")
    with c2: filt = st.selectbox("", ["All 📸🎬","Photos Only 📸","Videos Only 🎬","Favorites 💛"], label_visibility="collapsed")
    with c3: srt = st.selectbox("", ["Latest First","Oldest First","By Name"], label_visibility="collapsed")
    with c4: css_filt = st.selectbox("", ["No Filter","Vintage","Warm","Cool","B&W"], label_visibility="collapsed")
    files = visible
    if search: files = [f for f in files if search.lower() in f.get("name","").lower()]
    if "Photos" in filt: files = [f for f in files if "image" in f.get("mimeType","")]
    elif "Videos" in filt: files = [f for f in files if "video" in f.get("mimeType","")]
    elif "Favorites" in filt: files = [f for f in files if f["id"] in st.session_state.favorites]
    if srt == "Oldest First": files = sorted(files, key=lambda x: x.get("createdTime",""))
    elif srt == "By Name": files = sorted(files, key=lambda x: x.get("name","").lower())
    filter_css = {"Vintage":"sepia(0.6) contrast(1.1)","Warm":"saturate(1.4) hue-rotate(-15deg)","Cool":"saturate(0.8) hue-rotate(15deg) brightness(1.1)","B&W":"grayscale(1)"}.get(css_filt,"")
    if filter_css: st.markdown(f"<style>.mcard img{{filter:{filter_css}!important;}}</style>", unsafe_allow_html=True)
    st.markdown(f'<div style="margin-bottom:.8rem;"><span class="chip">📊 {len(files)} items</span></div>', unsafe_allow_html=True)
    if not files: st.info("📭 No media found."); return
    cols = st.columns(3)
    for i,f in enumerate(files):
        with cols[i%3]: display_media_card(f,svc)

# ── ALBUMS PAGE ──────────────────────────────────────────────────
def albums_page():
    from google_drive_helper import list_folders, list_files, create_folder
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    if st.session_state.selected_album:
        album = st.session_state.selected_album
        st.markdown(f'<div class="bc"><span class="bci">📁 Albums</span><span class="bcs">›</span><span class="bca">📂 {album["name"]}</span></div>', unsafe_allow_html=True)
        bc,tc = st.columns([1,5])
        with bc:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.selected_album=None; st.rerun()
        with tc:
            st.markdown(f'<div class="shdr"><span class="stitle">📂 {album["name"]}</span></div>', unsafe_allow_html=True)
        files = get_visible(list_files(svc,album["id"]))
        if not files: st.info("📭 This album is empty.")
        else:
            st.markdown(f'<span class="chip">📊 {len(files)} items</span><br><br>', unsafe_allow_html=True)
            cols = st.columns(3)
            for i,f in enumerate(files):
                with cols[i%3]: display_media_card(f,svc)
        return
    st.markdown('<div class="bc"><span class="bca">📁 Albums</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="shdr"><span class="stitle">📁 Albums</span></div>', unsafe_allow_html=True)
    with st.expander("➕ Create New Album"):
        c1,c2 = st.columns([3,1])
        with c1: new_name = st.text_input("Album Name", placeholder="e.g. 🎂 Birthday 2024")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create ✅"):
                if new_name.strip():
                    with st.spinner("Creating..."): create_folder(svc,new_name.strip(),rid)
                    st.success(f"✅ '{new_name}' created!"); st.rerun()
    with st.expander("🔐 Secret Album"):
        if not st.session_state.secret_unlocked:
            sp = st.text_input("Secret Password", type="password", key="secret_input")
            if st.button("🔓 Unlock"):
                if sp == st.session_state.secret_password: st.session_state.secret_unlocked=True; st.rerun()
                else: st.error("❌ Wrong password!")
        else:
            st.success("🔓 Secret Album Unlocked!")
            if st.button("🔒 Lock Again"): st.session_state.secret_unlocked=False; st.rerun()
    folders = list_folders(svc,rid)
    if not folders: st.info("📭 No albums yet. Create one above!"); return
    cols = st.columns(4)
    for i,folder in enumerate(folders):
        with cols[i%4]:
            count = len(list_files(svc,folder["id"]))
            st.markdown(f'<div class="acard"><span class="aemoji">📂</span><div class="aname">{folder["name"]}</div><span class="abadge">{count} items</span></div>', unsafe_allow_html=True)
            if st.button(f"Open 📂", key=f"op_{folder['id']}", use_container_width=True):
                st.session_state.selected_album=folder; st.rerun()

# ── UPLOAD PAGE ──────────────────────────────────────────────────
def upload_page():
    from google_drive_helper import list_folders, upload_file
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">⬆️ Upload Memories</span></div>', unsafe_allow_html=True)
    folders = list_folders(svc,rid)
    opts = {"📁 Root (Family Memories)": rid}
    for f in folders: opts[f"📂 {f['name']}"] = f["id"]
    sel = st.selectbox("📁 Upload to Album", list(opts.keys()))
    tid = opts[sel]
    st.markdown('<div class="uarea"><div style="font-size:2.5rem;">📤</div><div style="color:#ff6b9d;font-size:1rem;font-weight:600;">Drop photos & videos here</div><div style="color:#a0a0c0;font-size:.82rem;margin-top:.3rem;">JPG, PNG, GIF, WEBP, MP4, MOV, AVI, MKV</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="chip">📷 Tip: On mobile, tap "Browse files" to use your camera!</div><br>', unsafe_allow_html=True)
    ups = st.file_uploader("Choose files", type=IMAGE_TYPES+VIDEO_TYPES, accept_multiple_files=True, label_visibility="collapsed")
    if ups:
        st.markdown(f'<span class="chip">📎 {len(ups)} file(s) selected</span>', unsafe_allow_html=True)
        pc = st.columns(min(len(ups),4))
        for i,uf in enumerate(ups[:4]):
            with pc[i]:
                if uf.type.startswith("image"): st.image(uf, use_container_width=True, caption=uf.name[:14])
                else: st.markdown(f'<div style="text-align:center;padding:1rem;background:rgba(123,47,190,0.1);border-radius:10px;color:#a0a0c0;">🎬<br>{uf.name[:14]}</div>', unsafe_allow_html=True)
        if st.button("⬆️ Upload All to Google Drive 🚀", use_container_width=True):
            prog=st.progress(0); stat=st.empty(); ok=0
            for idx,uf in enumerate(ups):
                stat.markdown(f'<span class="chip">Uploading: {uf.name}</span>', unsafe_allow_html=True)
                try:
                    mt,_ = mimetypes.guess_type(uf.name)
                    upload_file(svc,uf.read(),uf.name,mt or "application/octet-stream",tid); ok+=1
                except Exception as e: st.error(f"❌ {uf.name}: {e}")
                prog.progress((idx+1)/len(ups))
            stat.empty(); st.success(f"✅ {ok}/{len(ups)} uploaded!"); st.balloons()

# ── TIMELINE PAGE ────────────────────────────────────────────────
def timeline_page():
    from google_drive_helper import list_files
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">🗓️ Timeline</span></div>', unsafe_allow_html=True)
    with st.spinner("Building timeline..."): all_files = list_files(svc,rid)
    visible = get_visible(all_files)
    if not visible: st.info("📭 No memories found."); return
    groups = {}
    for f in visible:
        ct = f.get("createdTime","")[:7]
        try: key = datetime.strptime(ct,"%Y-%m").strftime("%B %Y")
        except Exception: key = "Unknown Date"
        groups.setdefault(key,[]).append(f)
    for month,files in groups.items():
        st.markdown(f'<div class="thdr">📅 {month} · {len(files)} memories</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i,f in enumerate(files):
            with cols[i%3]: display_media_card(f,svc)
        st.markdown("<br>", unsafe_allow_html=True)

# ── FAVORITES PAGE ───────────────────────────────────────────────
def favorites_page():
    from google_drive_helper import list_files
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">💛 Favorites</span></div>', unsafe_allow_html=True)
    if not st.session_state.favorites:
        st.markdown("<div style='text-align:center;padding:3rem;'><div style='font-size:4rem;'>💛</div><div style='color:#a0a0c0;margin-top:1rem;'>No favorites yet! Tap 🤍 Fav on any photo.</div></div>", unsafe_allow_html=True)
        return
    all_files = list_files(svc,rid)
    favs = [f for f in all_files if f["id"] in st.session_state.favorites]
    st.markdown(f'<span class="chip">💛 {len(favs)} favorites</span><br><br>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i,f in enumerate(favs):
        with cols[i%3]: display_media_card(f,svc)

# ── SLIDESHOW PAGE ───────────────────────────────────────────────
def slideshow_page():
    from google_drive_helper import list_files, download_file
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">🎬 Slideshow</span></div>', unsafe_allow_html=True)
    all_files = list_files(svc,rid)
    photos = [f for f in get_visible(all_files) if "image" in f.get("mimeType","")]
    if not photos: st.info("📭 No photos found for slideshow."); return
    css_filt = st.selectbox("🎨 Photo Filter", ["No Filter","Vintage","Warm","Cool","B&W"])
    filter_css = {"Vintage":"sepia(0.6) contrast(1.1)","Warm":"saturate(1.4) hue-rotate(-15deg)","Cool":"saturate(0.8) hue-rotate(15deg) brightness(1.1)","B&W":"grayscale(1)"}.get(css_filt,"")
    if filter_css: st.markdown(f"<style>.sswrap img{{filter:{filter_css}!important;}}</style>", unsafe_allow_html=True)
    total=len(photos); idx=st.session_state.slideshow_index%total; cur=photos[idx]
    st.markdown(f'<span class="chip">📸 {idx+1} of {total}</span><br><br>', unsafe_allow_html=True)
    st.markdown('<div class="sswrap">', unsafe_allow_html=True)
    try:
        thumb = cur.get("thumbnailLink")
        st.image(thumb.replace("s220","s800") if thumb else download_file(svc,cur["id"]), use_container_width=True)
    except Exception: st.markdown("<div style='padding:3rem;text-align:center;font-size:3rem;'>🖼️</div>", unsafe_allow_html=True)
    ct = cur.get("createdTime","")[:10]
    try: dt_str = datetime.strptime(ct,"%Y-%m-%d").strftime("%d %B %Y")
    except Exception: dt_str = ct
    st.markdown(f'<div style="color:#ff6b9d;font-weight:600;margin-top:.4rem;">📄 {cur.get("name","")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#a0a0c0;font-size:.8rem;">📅 {dt_str}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns([1,1,2,1,1])
    with c1:
        if st.button("⏮️ First"): st.session_state.slideshow_index=0; st.rerun()
    with c2:
        if st.button("◀️ Prev"): st.session_state.slideshow_index=(idx-1)%total; st.rerun()
    with c3:
        st.markdown(f"<div style='text-align:center;color:#a0a0c0;padding-top:.5rem;'>{idx+1} / {total}</div>", unsafe_allow_html=True)
    with c4:
        if st.button("Next ▶️"): st.session_state.slideshow_index=(idx+1)%total; st.rerun()
    with c5:
        if st.button("Last ⏭️"): st.session_state.slideshow_index=total-1; st.rerun()
    try:
        fb = download_file(svc,cur["id"])
        st.download_button("⬇️ Download This Photo", data=fb, file_name=cur.get("name","photo.jpg"), use_container_width=True)
    except Exception: pass

# ── ON THIS DAY PAGE ─────────────────────────────────────────────
def on_this_day_page():
    from google_drive_helper import list_files
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">📅 On This Day</span></div>', unsafe_allow_html=True)
    today = date.today(); today_md = today.strftime("%m-%d")
    all_files = list_files(svc,rid); visible = get_visible(all_files)
    matches = [f for f in visible if f.get("createdTime","")[:10][5:] == today_md]
    st.markdown(f'<div class="otdbanner"><div style="font-size:2.5rem;">📅</div><div style="font-size:1.1rem;font-weight:700;color:#FFD700;">On This Day — {today.strftime("%B %d")}</div><div style="color:#a0a0c0;font-size:.82rem;margin-top:.3rem;">Memories from today\'s date in past years</div></div>', unsafe_allow_html=True)
    if not matches: st.info(f"📭 No memories found for {today.strftime('%B %d')} in past years. Keep making memories! 💖"); return
    st.markdown(f'<span class="chip">🌟 {len(matches)} memory/memories found</span><br><br>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i,f in enumerate(matches):
        with cols[i%3]: display_media_card(f,svc)

# ── STATS PAGE ───────────────────────────────────────────────────
def stats_page():
    import pandas as pd
    from google_drive_helper import list_files
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">📊 Memory Statistics</span></div>', unsafe_allow_html=True)
    all_files = list_files(svc,rid); visible = get_visible(all_files)
    photos = [f for f in visible if "image" in f.get("mimeType","")]
    videos = [f for f in visible if "video" in f.get("mimeType","")]
    total_cmts  = sum(len(v) for v in st.session_state.comments.values())
    total_votes = sum(st.session_state.votes.values()) if st.session_state.votes else 0
    c1,c2,c3,c4,c5 = st.columns(5)
    for col,icon,val,lbl in zip([c1,c2,c3,c4,c5],["📸","🎬","💛","💬","👍"],
        [len(photos),len(videos),len(st.session_state.favorites),total_cmts,total_votes],
        ["Photos","Videos","Favorites","Comments","Votes"]):
        with col:
            st.markdown(f'<div class="scard"><span class="sicon">{icon}</span><div class="snum">{val}</div><div class="slbl">{lbl}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    monthly = {}
    for f in visible:
        ct = f.get("createdTime","")[:7]
        if ct: monthly[ct] = monthly.get(ct,0)+1
    if monthly:
        st.markdown("**📅 Photos by Month**")
        df = pd.DataFrame(list(monthly.items()), columns=["Month","Count"]).sort_values("Month")
        st.bar_chart(df.set_index("Month"))
    days = {}; day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    for f in visible:
        ct = f.get("createdTime","")[:10]
        if ct:
            try:
                d = datetime.strptime(ct,"%Y-%m-%d").weekday()
                days[day_names[d]] = days.get(day_names[d],0)+1
            except Exception: pass
    if days:
        best = max(days, key=days.get)
        st.markdown(f'<div class="thdr">🏆 Most active day: <b>{best}</b> with {days[best]} uploads!</div>', unsafe_allow_html=True)

# ── CAPSULE PAGE ─────────────────────────────────────────────────
def capsule_page():
    st.markdown('<div class="shdr"><span class="stitle">💌 Memory Capsule</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="background:linear-gradient(135deg,rgba(0,255,136,0.05),rgba(123,47,190,0.1));border:1px solid rgba(0,255,136,0.22);border-radius:14px;padding:1.2rem;margin-bottom:1.1rem;"><div style="font-size:1.5rem;">💌</div><div style="color:#00ff88;font-weight:600;">Lock memories to open on a future date!</div></div>', unsafe_allow_html=True)
    with st.expander("➕ Create New Time Capsule"):
        c1,c2 = st.columns(2)
        with c1:
            cap_title = st.text_input("Capsule Title 🏷️", placeholder="e.g. Our 2025 Memories")
            cap_msg   = st.text_area("Message 💬", placeholder="Write a message to your future self...", height=100)
        with c2:
            cap_date = st.date_input("Unlock Date 📅", min_value=date.today())
            cap_from = st.text_input("From 👤", placeholder="Your name")
        if st.button("🔒 Create Capsule", use_container_width=True):
            if cap_title and cap_msg and cap_from:
                st.session_state.capsules.append({"title":cap_title,"message":cap_msg,"unlock_date":str(cap_date),"from":cap_from,"created":str(date.today())})
                st.success(f"✅ Capsule '{cap_title}' locked until {cap_date} 🎉"); st.rerun()
            else: st.error("Please fill all fields!")
    if not st.session_state.capsules: st.info("💌 No capsules yet. Create your first memory capsule!"); return
    for i,cap in enumerate(st.session_state.capsules):
        unlock = date.fromisoformat(cap["unlock_date"]); unlocked = date.today() >= unlock
        color = "#00ff88" if unlocked else "#FFD700"
        icon_str = "🔓" if unlocked else "🔒"
        status = "UNLOCKED ✅" if unlocked else f"Unlocks {unlock.strftime('%B %d, %Y')}"
        msg_part = f'<div style="color:#e0e0d0;font-size:.83rem;margin-top:.5rem;border-top:1px solid rgba(255,255,255,0.08);padding-top:.5rem;">💬 {cap["message"]}</div>' if unlocked else '<div style="color:#505070;font-size:.8rem;margin-top:.4rem;">🔒 Message hidden until unlock date...</div>'
        st.markdown(f'<div style="background:rgba(255,255,255,0.04);border:1px solid {color}44;border-radius:12px;padding:1.1rem;margin-bottom:.7rem;"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="font-weight:700;color:{color};">{icon_str} {cap["title"]}</div><div style="font-size:.73rem;color:{color};background:{color}22;border-radius:20px;padding:.15rem .65rem;">{status}</div></div><div style="color:#a0a0c0;font-size:.8rem;margin-top:.3rem;">From: {cap["from"]} · Created: {cap["created"]}</div>{msg_part}</div>', unsafe_allow_html=True)
        if st.button(f"🗑️ Delete", key=f"dcap_{i}"):
            st.session_state.capsules.pop(i); st.rerun()

# ── TRASH PAGE ───────────────────────────────────────────────────
def trash_page():
    from google_drive_helper import list_files
    svc = st.session_state.drive_service; rid = st.session_state.root_folder_id
    st.markdown('<div class="shdr"><span class="stitle">🗑️ Trash</span></div>', unsafe_allow_html=True)
    trash_ids = st.session_state.trash
    all_files = list_files(svc,rid)
    trashed = [f for f in all_files if f["id"] in trash_ids]
    if not trashed: st.info("🗑️ Trash is empty!"); return
    c1,c2 = st.columns([3,1])
    with c1: st.markdown(f'<span class="chip" style="background:rgba(255,100,100,0.15);color:#ff6b6b;border-color:rgba(255,100,100,0.3);">{len(trashed)} item(s) in trash</span>', unsafe_allow_html=True)
    with c2:
        if st.button("🧹 Empty All"): st.session_state.trash.clear(); st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i,f in enumerate(trashed):
        with cols[i%3]:
            fid=f["id"]; name=f.get("name",""); mime=f.get("mimeType","")
            st.markdown('<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,100,100,0.2);border-radius:12px;overflow:hidden;margin-bottom:.7rem;">', unsafe_allow_html=True)
            try:
                if "image" in mime:
                    thumb = f.get("thumbnailLink")
                    if thumb: st.image(thumb.replace("s220","s400"), use_container_width=True)
            except Exception: st.markdown("<div style='text-align:center;padding:1.5rem;'>🖼️</div>", unsafe_allow_html=True)
            st.markdown(f'<div style="padding:.3rem .5rem;color:#a0a0c0;font-size:.72rem;">🗑️ {name[:25]}</div>', unsafe_allow_html=True)
            if st.button("♻️ Restore", key=f"rst_{fid}", use_container_width=True):
                st.session_state.trash.discard(fid); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ── SETTINGS PAGE ────────────────────────────────────────────────
def settings_page():
    st.markdown('<div class="shdr"><span class="stitle">⚙️ Settings</span></div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("**🎨 Theme**")
        theme = st.radio("Theme", ["dark","light"], index=0 if st.session_state.theme=="dark" else 1, horizontal=True)
        if theme != st.session_state.theme: st.session_state.theme=theme; st.rerun()
        st.markdown("<br>**🌍 Language**", unsafe_allow_html=True)
        lang = st.selectbox("Language", ["English","Hindi"], index=0 if st.session_state.language=="English" else 1)
        if lang != st.session_state.language: st.session_state.language=lang; st.rerun()
    with c2:
        st.markdown("**🔐 Secret Album Password**")
        new_sp = st.text_input("New Password", type="password", placeholder="New secret password")
        if st.button("💾 Save Password"):
            if new_sp.strip(): st.session_state.secret_password=new_sp.strip(); st.success("✅ Password updated!")
            else: st.error("Password cannot be empty!")
        total_cmts  = sum(len(v) for v in st.session_state.comments.values())
        total_votes = sum(st.session_state.votes.values()) if st.session_state.votes else 0
        st.markdown(f'<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(233,30,140,0.15);border-radius:12px;padding:1rem;font-size:.83rem;color:#a0a0c0;margin-top:1rem;">💛 Favorites: {len(st.session_state.favorites)}<br>💬 Comments: {total_cmts}<br>🗑️ Trash: {len(st.session_state.trash)}<br>💌 Capsules: {len(st.session_state.capsules)}<br>👍 Total Votes: {total_votes}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧹 Clear All App Data (Reset)"):
        for k in ["favorites","comments","reactions","votes","trash","capsules","view_counts"]:
            if k in st.session_state:
                val = st.session_state[k]
                if isinstance(val,set): st.session_state[k]=set()
                elif isinstance(val,dict): st.session_state[k]={}
                elif isinstance(val,list): st.session_state[k]=[]
        st.success("✅ App data cleared!"); st.rerun()

# ── ABOUT PAGE ───────────────────────────────────────────────────
def about_page():
    st.markdown('<div class="shdr"><span class="stitle">ℹ️ About</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="background:linear-gradient(90deg,#E91E8C,#7B2FBE,#FFD700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:1.7rem;font-weight:800;">💖 {APP_NAME}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#a0a0c0;">{APP_SUBTITLE}</p>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;flex-wrap:wrap;gap:.4rem;margin:.8rem 0;"><span class="chip">🐍 Python</span><span class="chip">🚀 Streamlit</span><span class="chip">☁️ Google Drive</span><span class="chip">🔐 OAuth 2.0</span><span class="chip">🎨 Glassmorphism</span></div>', unsafe_allow_html=True)
    st.markdown('<h4 style="color:#ff6b9d;margin-top:1rem;">✨ All Features</h4>', unsafe_allow_html=True)
    st.markdown('<div style="display:grid;grid-template-columns:1fr 1fr;gap:.4rem;font-size:.85rem;color:#c0c0d8;"><div>📸 Photo Gallery</div><div>🎬 Video Player</div><div>⬆️ Easy Upload</div><div>📁 Album Management</div><div>🗓️ Timeline View</div><div>💛 Favorites</div><div>🎬 Slideshow + Filters</div><div>🔍 Search & Filter</div><div>📅 On This Day</div><div>📊 Memory Stats</div><div>💌 Time Capsule</div><div>🗑️ Trash & Restore</div><div>❤️ Emoji Reactions</div><div>💬 Photo Comments</div><div>👍 Photo Voting</div><div>🏷️ Auto Tags</div><div>👁️ View Counter</div><div>🔐 Secret Album</div><div>⚙️ Dark/Light Theme</div><div>🌍 Hindi/English</div><div>⬅️ Back Navigation</div><div>📍 Bottom Nav Bar</div></div>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:rgba(233,30,140,0.15);margin:1.2rem 0;"><p style="color:#505070;font-size:.82rem;text-align:center;">Made with ❤️ using Python & Streamlit</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── MAIN ─────────────────────────────────────────────────────────
def main():
    if not st.session_state.authenticated:
        login_page(); return
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
    st.markdown("---")
    render_bottom_nav()
    st.markdown("---")
    page = st.session_state.current_page
    if   page == "🏠 Home":          home_page()
    elif page == "🖼️ Gallery":       gallery_page()
    elif page == "📁 Albums":        albums_page()
    elif page == "⬆️ Upload":        upload_page()
    elif page == "🗓️ Timeline":      timeline_page()
    elif page == "💛 Favorites":     favorites_page()
    elif page == "🎬 Slideshow":     slideshow_page()
    elif page == "📅 On This Day":   on_this_day_page()
    elif page == "📊 Stats":         stats_page()
    elif page == "💌 Capsule":       capsule_page()
    elif page == "🗑️ Trash":         trash_page()
    elif page == "⚙️ Settings":      settings_page()
    elif page == "ℹ️ About":         about_page()

if __name__ == "__main__":
    main()
