<div align="center">

# 💖 Our Family Memories App

### A beautiful private family photo & video showcase app

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge&logo=streamlit)
![Google Drive](https://img.shields.io/badge/Google%20Drive-API%20v3-green?style=for-the-badge&logo=googledrive)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

## 📱 Screenshots

| Login | Gallery | Upload |
|---|---|---|
| 🔐 Beautiful login | 📸 Photo grid | ⬆️ Easy upload |

---

## ✨ Features

- 📸 **Photo Gallery** — Beautiful grid layout with thumbnails
- 🎬 **Video Player** — Inline video playback
- ⬆️ **Upload** — Upload photos & videos from any device
- 📁 **Albums** — Create & browse albums/folders
- 🔐 **Password Protected** — Private family access only
- ☁️ **Google Drive** — Stored on your personal Drive (15 GB free)
- ⬇️ **Download** — Download any memory
- 📱 **Mobile Friendly** — Works on Android & iOS browsers

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.9+ | Backend |
| Streamlit | Web UI |
| Google Drive API v3 | Cloud Storage |
| OAuth 2.0 | Authentication |

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/family-memories-app.git
cd family-memories-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Google credentials
- Download `client_secrets.json` from Google Cloud Console
- Place it in the root folder

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Open in browser
```
http://localhost:8501
```

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push code to GitHub (without secret files)
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Add secrets in Streamlit Cloud settings
5. Deploy & share link with family!

---

## 📱 Access on Android

1. Deploy on Streamlit Cloud (above)
2. Open the app URL in **Chrome** on Android
3. Tap **⋮ Menu** → **"Add to Home Screen"**
4. App icon appears on your home screen!
5. Opens like a real Android app! 🎉

---

## 📁 Project Structure

```
📦 family-memories-app/
├── app.py                  ← Main Streamlit app
├── google_drive_helper.py  ← Google Drive API (OAuth 2.0)
├── config.py               ← App configuration
├── setup_secrets.py        ← Streamlit Cloud helper
├── requirements.txt        ← Python dependencies
├── .gitignore              ← Git ignore rules
├── .streamlit/
│   └── secrets_template.toml ← Secrets template
└── README.md               ← This file
```

---

## ⚙️ Configuration

Open `config.py` to customize:
```python
APP_NAME = "Our Family Memories"   # Your app title
APP_PASSWORD = "family123"         # Change your password!
```

---

## 🔒 Security

- ✅ Password protected app
- ✅ OAuth 2.0 Google authentication
- ✅ Secret files never uploaded to GitHub
- ✅ Only approved test users can connect

---

## 📄 License

MIT License — Free to use for personal projects

---

<div align="center">
Made with ❤️ using Python & Streamlit
</div>
