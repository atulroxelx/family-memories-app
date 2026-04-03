
# ============================================================
# App Configuration
# ============================================================

APP_NAME = "Our Family Memories"
APP_ICON = "💖"
APP_SUBTITLE = "A beautiful space to cherish our precious moments"

# --- Password Protection ---
APP_PASSWORD = "family123"  # Change this to your desired password

# --- Google Drive Settings ---
DRIVE_ROOT_FOLDER_NAME = "FamilyMemories"
SCOPES = ["https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "client_secrets.json"   # OAuth 2.0 client secrets file
TOKEN_FILE = "token.json"                  # Auto-generated after first login

# --- Supported File Types ---
IMAGE_TYPES = ["jpg", "jpeg", "png", "gif", "webp"]
VIDEO_TYPES = ["mp4", "mov", "avi", "mkv"]
ALL_MEDIA_TYPES = IMAGE_TYPES + VIDEO_TYPES

# --- UI Settings ---
GRID_COLUMNS = 3
ACCENT_COLOR = "#E91E8C"
BG_COLOR = "#1a1a2e"
CARD_BG = "#16213e"
