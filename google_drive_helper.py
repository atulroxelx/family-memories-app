# ============================================================
# Google Drive Helper - OAuth 2.0 Version
# ============================================================

import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE, DRIVE_ROOT_FOLDER_NAME


def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"{CREDENTIALS_FILE} not found!")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("drive", "v3", credentials=creds)


def is_authenticated():
    if not os.path.exists(TOKEN_FILE):
        return False
    try:
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if creds and creds.valid:
            return True
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            return True
    except Exception:
        return False
    return False


def get_or_create_root_folder(service):
    query = f"name='{DRIVE_ROOT_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])
    if folders:
        return folders[0]["id"]
    return create_folder(service, DRIVE_ROOT_FOLDER_NAME)


def create_folder(service, name, parent_id=None):
    metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def list_folders(service, parent_id):
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, createdTime)").execute()
    return results.get("files", [])


def list_files(service, folder_id):
    query = f"'{folder_id}' in parents and trashed=false and (mimeType contains 'image/' or mimeType contains 'video/')"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType, size, createdTime, thumbnailLink, webContentLink)",
        orderBy="createdTime desc"
    ).execute()
    return results.get("files", [])


def upload_file(service, file_bytes, file_name, mime_type, folder_id):
    metadata = {"name": file_name, "parents": [folder_id]}
    media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mime_type, resumable=True)
    uploaded = service.files().create(
        body=metadata, media_body=media, fields="id, name, webContentLink"
    ).execute()
    try:
        service.permissions().create(
            fileId=uploaded["id"], body={"type": "anyone", "role": "reader"}
        ).execute()
    except Exception:
        pass
    return uploaded


def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buffer.seek(0)
    return buffer.read()


def get_thumbnail_url(file):
    return file.get("thumbnailLink", None)


def get_direct_url(file_id):
    return f"https://drive.google.com/uc?export=view&id={file_id}"


def get_storage_info(service):
    try:
        about = service.about().get(fields="storageQuota").execute()
        quota = about.get("storageQuota", {})
        used = int(quota.get("usage", 0)) / (1024 ** 3)
        total = int(quota.get("limit", 1)) / (1024 ** 3)
        return round(used, 2), round(total, 2)
    except Exception:
        return 0, 0
