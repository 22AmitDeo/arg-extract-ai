

# extracted_text.py
# text = "This is the extracted text"
# with open("extracted_output.txt", "w") as f:
#     f.write(text)



from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Set the path to the directory containing client_secrets.json
current_dir = os.path.dirname(os.path.abspath(__file__))
client_secrets_path = os.path.join(current_dir, "client_secrets.json")

# Set settings manually
gauth = GoogleAuth()
gauth.LoadClientConfigFile(client_secrets_path)
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# Upload file (adjust the filename as needed)
file_to_upload = os.path.join(current_dir, "extracted_text.txt")
upload_file = drive.CreateFile({'title': 'uploaded_extracted_text.txt'})
upload_file.SetContentFile(file_to_upload)
upload_file.Upload()

print("Upload successful.")
