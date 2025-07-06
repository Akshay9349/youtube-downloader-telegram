# compressor.py
import os
import json
import pyzipper
from datetime import datetime

# Load config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

PASSLOG_PATH = "zip_passlog.json"

# Save password used per zip file
def log_password(zip_path, password):
    if not password:
        return
    log = {}
    if os.path.exists(PASSLOG_PATH):
        with open(PASSLOG_PATH, "r", encoding="utf-8") as log_file:
            log = json.load(log_file)
    log[os.path.basename(zip_path)] = password
    with open(PASSLOG_PATH, "w", encoding="utf-8") as log_file:
        json.dump(log, log_file, indent=4)

# Compress folder with encryption
def compress_folder(folder_path, password, upload_after_zip=False):
    if not os.path.exists(folder_path):
        print("[ERROR] Folder not found for compression.")
        return None

    base_name = os.path.basename(folder_path.rstrip("\\/"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{base_name}_{timestamp}_encrypted.zip"
    zip_path = os.path.join(os.path.dirname(folder_path), zip_name)

    with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password.encode())
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                arcname = os.path.relpath(abs_path, folder_path)
                zf.write(abs_path, arcname)

    log_password(zip_path, password)
    print(f"[ZIP] Folder compressed to: {zip_path}")

    if upload_after_zip:
        from telegram_uploader import upload_zip
        import asyncio
        asyncio.run(upload_zip(zip_path))

    return zip_path
