# 📥 YouTube Downloader & Telegram Uploader

A powerful Python-based utility for downloading YouTube videos or audio with playlist support, encryption, compression, logging, and optional cloud upload to Telegram.

---

## 🚀 Features

### ✅ Core Functionalities

* **🎞️ Video & 🎵 Audio Download**: Choose format with quality control (e.g., `720p`, `bestaudio`)
* **📁 Playlist Support**: Handles individual links or playlists
* **🔠 Title Sanitization**: Auto-removes special characters from filenames
* **📂 Folder Structure**: Downloads go into `Youtube Downloads/<input_filename>/...`

### 🧩 Profiles & Input Management

* **🧾 URL Input Profiles**: Select from saved profiles in `url_input/`
* **🔄 Backup URLs**: Every session creates a backup in `url_backup/`
* **🧠 Auto Profile Switching**: Uses backup if main input is empty

### 🔒 Compression & Encryption

* **🔐 Encrypted ZIP**: Compresses downloaded folder with optional password
* **💾 Password Log**: Passwords saved securely per ZIP (optional)

### 📤 Cloud Upload (Telegram)

* Upload encrypted ZIPs via Telegram bot
* Auto-login or 2FA supported
* Links logged in `telegram_upload_log.json`

### 📊 Logging & Reports

* `Logs/success.txt` and `Logs/failed.txt`
* **📄 PDF Summary**: `Summaries/Download_Summary.pdf`
* **📘 Password Log**: `zip_passlog.json`

---

## 🧪 Setup Instructions

### 🔧 Requirements

```bash
pip install -r requirements.txt
```

### 🔑 Configuration (`config.json`)

```json
{
  "download_path": "Youtube Downloads",
  "log_path": "Logs",
  "media_type": "video",
  "quality": "720",
  "compress": true,
  "ask_password_each_time": true,
  "input_file": "url_input/urls.txt",
  "upload_after_zip": false,
  "telegram_api_id": 123456,
  "telegram_api_hash": "YOUR_HASH",
  "telegram_session": "session_name",
  "telegram_target_chat": "@YourGroupOrChannel"
}
```

---

## 🛠️ Project Structure

```
project_root/
├── downloader.py
├── logger.py
├── compressor.py
├── telegram_uploader.py
├── pdf_summary.py
├── config.json
├── requirements.txt
├── zip_passlog.json
├── telegram_upload_log.json
├── url_input/
├── url_backup/
├── Logs/
├── Summaries/
└── Youtube Downloads/
```

---

## ▶️ Usage

```bash
python downloader.py
```

* Prompts for audio/video and quality if `auto_mode` is disabled
* Asks whether to compress and upload if enabled in config
* Produces logs and summary PDF

---

## 🔐 Security Notes

* Encrypted ZIPs use `pyzipper` for AES-256 security
* Passwords can be saved in `zip_passlog.json` for recovery

---

## 🧾 To-Do / Suggestions

* [ ] Add Google Drive or Dropbox upload
* [ ] Add GUI (PyQt5-based)
* [ ] Add support for YouTube channel archiving

---

## 🧠 Credits

Built using:

* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [pyzipper](https://pypi.org/project/pyzipper/)
* [telethon](https://github.com/LonamiWebs/Telethon)

MIT License © 2025
