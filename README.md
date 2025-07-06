# 🎬 YouTube Downloader with Telegram Upload

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A feature-rich Python-based YouTube downloader with support for:

* ✅ Audio & video download
* ✅ Encrypted ZIP compression
* ✅ Telegram cloud upload
* ✅ Configurable profiles, logging & stats dashboard
* ✅ Backup URL handling & file sanitization

---

## 📦 Features

### 🎧 Audio / 🎞️ Video Downloads

* Choose between audio or video
* Supports highest available quality or custom resolution

### 📁 Folder Structure

* Auto-organized by profile name (from input file)
* Example: `Youtube Downloads/music_urls/`

### 🔐 Encrypted ZIP Compression

* Prompt for password
* Save password securely per file
* Compatible with cross-platform zip extractors

### 📤 Telegram Upload

* Send ZIPs to Telegram channels or private messages
* Logs message links for future access

### 🧠 Smart Input Handling

* Supports multiple input files via `url_input/`
* Fallback to `url_backup/` if input is empty
* Auto-renames and stores old input

### 📜 Logging

* Logs successful and failed URLs separately
* PDF summary generator included

### 📊 Stats Dashboard (HTML)

* Download counts
* Size summaries
* Most frequent channels
* Failure rate

### 🧽 Title Cleaner

* Removes special characters
* Custom word removal support

---

## 🚀 Usage

### 📥 Clone & Setup

```bash
git clone https://github.com/Akshay9349/youtube-downloader-telegram.git
cd youtube-downloader-telegram
pip install -r requirements.txt
```

### 🔧 Configure

Edit `config.json` for your defaults:

```json
{
  "download_path": "Youtube Downloads",
  "log_path": "Logs",
  "input_file": "url_input/urls.txt",
  "media_type": "video",
  "quality": "720",
  "compress": true,
  "upload_after_zip": true,
  "ask_password_each_time": true,
  "telegram_api_id": 123456,
  "telegram_api_hash": "your_hash",
  "telegram_session": "session_name",
  "telegram_target_chat": "@your_channel"
}
```

### ▶️ Run the Downloader

```bash
python downloader.py
```

You’ll be prompted to:

* Select quality (if `auto_mode` is false)
* Enter ZIP password
* Upload ZIP to Telegram (optional)

---

### 📦 Download ZIP Release

> 🔰 For non-developers or quick usage

Download the latest pre-zipped version from the [Releases Page](https://github.com/Akshay9349/youtube-downloader-telegram/releases):

➡️ [youtube-downloader-telegram-v1.0.0.zip](https://github.com/Akshay9349/youtube-downloader-telegram/releases/download/v1.0.0/youtube-downloader-telegram-v1.0.0.zip)

Just extract it, install requirements, and run:

```bash
pip install -r requirements.txt
python downloader.py
```

---

## 📂 Project Structure

```
youtube-downloader-telegram/
├── downloader.py
├── compressor.py
├── telegram_uploader.py
├── logger.py
├── pdf_summary.py
├── stats_dashboard.py
├── title_cleaner.py
├── url_input/            # Place your urls.txt or profile_x.txt here
├── url_backup/           # Auto-created backups of input files
├── Youtube Downloads/    # Actual downloaded media
├── Logs/                 # Download success/failure logs
├── Summaries/            # PDF reports
├── config.json
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## 🧪 Requirements

* Python 3.8+
* `yt-dlp`, `pyzipper`, `telethon`, `fpdf`, `beautifulsoup4`, `requests`

Install with:

```bash
pip install -r requirements.txt
```

---

## 📝 License

MIT License © 2025 [Akshay9349](https://github.com/Akshay9349)

---

## 💬 Credits

Created with ❤️ by [Akshay9349](https://github.com/Akshay9349)
Contributions welcome via pull request or issue!
