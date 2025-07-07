# upload_to_drive.py

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path
import os

def upload_file_to_drive(filepath):
    """
    Uploads a single file to Google Drive using PyDrive.
    """
    # Setup Google authentication
    current_dir = os.path.dirname(os.path.abspath(__file__))
    client_secrets_path = os.path.join(current_dir, "client_secrets.json")

    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(client_secrets_path)
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file_to_upload = drive.CreateFile({'title': Path(filepath).name})
    file_to_upload.SetContentFile(str(filepath))
    file_to_upload.Upload()

    print(f"[✓] Uploaded to Drive: {filepath}")
