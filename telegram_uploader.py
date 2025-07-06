# telegram_uploader.py
import os
import json
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from datetime import datetime

# Load config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

API_ID = config["telegram_api_id"]
API_HASH = config["telegram_api_hash"]
SESSION = config["telegram_session"]
CHAT = config["telegram_target_chat"]
UPLOAD_LOG = "telegram_upload_log.json"

def log_upload(zip_path, message_link):
    log = {}
    if os.path.exists(UPLOAD_LOG):
        with open(UPLOAD_LOG, "r", encoding="utf-8") as log_file:
            log = json.load(log_file)

    log_entry = {
        "file": os.path.basename(zip_path),
        "timestamp": datetime.now().isoformat(),
        "message_link": message_link
    }

    log.setdefault("uploads", []).append(log_entry)

    with open(UPLOAD_LOG, "w", encoding="utf-8") as log_file:
        json.dump(log, log_file, indent=4)

async def upload_zip(zip_path):
    if not os.path.exists(zip_path):
        print("[ERROR] ZIP file not found.")
        return

    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        await client.connect()

        if not await client.is_user_authorized():
            print("[AUTH] Please log in to your Telegram account.")
            phone = input("Enter your phone number: ")
            await client.send_code_request(phone)
            code = input("Enter the code you received: ")
            try:
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                pw = input("Two-step verification password: ")
                await client.sign_in(password=pw)

        print(f"[UPLOAD] Uploading {os.path.basename(zip_path)} to {CHAT}...")
        result = await client.send_file(CHAT, zip_path)
        message_link = f"https://t.me/{CHAT.lstrip('@')}/{result.id}"
        print(f"[LINK] Uploaded: {message_link}")

        log_upload(zip_path, message_link)

if __name__ == "__main__":
    zip_to_upload = input("Enter path to ZIP file to upload: ").strip('"')
    asyncio.run(upload_zip(zip_to_upload))
