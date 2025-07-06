import os

def log_message(filename, content, log_dir):
    os.makedirs(log_dir, exist_ok=True)
    filepath = os.path.join(log_dir, filename)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def is_already_downloaded(url, log_dir):
    path = os.path.join(log_dir, "success.txt")
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        return url.strip() in [line.strip() for line in f.readlines()]

def mark_as_downloaded(url, log_dir):
    log_message("success.txt", url, log_dir)
