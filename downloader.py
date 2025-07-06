# downloader.py
# import os
import json
import time
from pathlib import Path
from yt_dlp import YoutubeDL
from logger import log_message, is_already_downloaded, mark_as_downloaded
from compressor import compress_folder
from pdf_summary import generate_pdf_log

# Load config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Folders
main_download_folder = Path(config["download_path"])
main_download_folder.mkdir(parents=True, exist_ok=True)
Path(config["log_path"]).mkdir(parents=True, exist_ok=True)
Path("url_input").mkdir(exist_ok=True)
Path("url_backup").mkdir(exist_ok=True)
Path("Summaries").mkdir(exist_ok=True)

# Determine URL input file
url_file = Path(config.get("input_file", "url_input/urls.txt"))

# Read URLs
def read_urls(file_path):
    if not file_path.exists():
        return []
    with file_path.open("r", encoding="utf-8") as input_file:
        return [line.strip() for line in input_file if line.strip()]

urls = read_urls(url_file)

# Fallback to back up if empty
if not urls:
    print("[INFO] Input file empty. Checking backup folder...")
    backups = sorted(Path("url_backup").glob("*.txt"), reverse=True)
    if backups:
        url_file = backups[0]
        print(f"[FALLBACK] Using: {url_file.name}")
        urls = read_urls(url_file)
    else:
        print("[ERROR] No URLs found.")
        exit(1)

# Backup + rename input
if url_file.parts[0] == "url_input":
    base_name = url_file.stem
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{base_name}_{timestamp}.txt"
    backup_path = Path("url_backup") / backup_filename
    with backup_path.open("w", encoding="utf-8") as backup_file:
        backup_file.write("\n".join(urls))
    print(f"[BACKUP] Input backed up to: {backup_path}")

    new_input_path = Path("url_input") / f"{base_name}_{timestamp}.txt"
    url_file.rename(new_input_path)
    print(f"[RENAMED] Input renamed to: {new_input_path}")

# Create subfolder for current session
subfolder = url_file.stem
download_path = main_download_folder / subfolder
download_path.mkdir(parents=True, exist_ok=True)

# Auto or manual mode
if config.get("auto_mode", False):
    media_type = config["media_type"]
    quality = config["quality"]
    compress = config["compress"]
else:
    media_type = input("Download [audio/video]? ").strip().lower() or config["media_type"]
    quality = input("Enter quality (e.g., 720p/best): ").strip() or config["quality"]
    compress = input("Compress after download? (y/n): ").strip().lower() == 'y'

# Format builder
def get_format(media, qual):
    if media == "audio":
        return "best-audio"
    elif qual == "best":
        return "best video+best-audio/best"
    else:
        return f"best-video[height<={qual}]+best-audio/best[height<={qual}]"

# Progress feedback
def download_hook(d):
    if d['status'] == 'finished':
        print(f"[DONE] {d.get('filename')}")

# YT-DLP settings
ydl_opts = {
    'format': get_format(media_type, quality),
    'outplay': str(download_path / '%(uploader)s' / '%(title)s.%(ext)s'),
    'merge_output_format': 'mp4' if media_type == "video" else None,
    'quiet': False,
    'progress_hooks': [download_hook],
    'playlist': False
}

# Start download
with YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        if is_already_downloaded(url, config["log_path"]):
            print(f"[SKIPPED] Already downloaded: {url}")
            continue
        try:
            ydl.download([url])
            log_message("success.txt", url, config["log_path"])
            mark_as_downloaded(url, config["log_path"])
        except Exception as e:
            print(f"[ERROR] {url} - {e}")
            log_message("failed.txt", f"{url} - {e}", config["log_path"])

# Ask to compress
zip_path = None
if compress:
    if config.get("ask_password_each_time", True):
        zip_pass = input("🔐 Enter password to encrypt ZIP: ").strip()
        save = input("💾 Save this password to config? (y/n): ").strip().lower()
        if save == 'y':
            config["zip_password"] = zip_pass
            with open("config.json", "w") as config_file:
                json.dump(config, config_file, indent=4)
    else:
        zip_pass = config.get("zip_password", "")

    compress_folder(str(download_path), password=zip_pass)

    # Construct expected ZIP path
    base_name = download_path.name
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    zip_path = download_path.parent / f"{base_name}_{timestamp}_encrypted.zip"

    # Ask to upload to Telegram
    upload = input("📤 Upload ZIP to Telegram? (y/n): ").strip().lower()
    if upload == 'y':
        from telegram_uploader import upload_zip
        import asyncio
        asyncio.run(upload_zip(str(zip_path)))

# Generate PDF Summary
generate_pdf_log(
    Path(config["log_path"]) / "success.txt",
    Path(config["log_path"]) / "failed.txt",
    Path("Summaries") / "Download_Summary.pdf"
)

print("📄 Summary PDF saved to Summaries/Download_Summary.pdf")
