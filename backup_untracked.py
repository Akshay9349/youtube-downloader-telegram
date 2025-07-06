import os
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

def get_untracked_files():
    result = subprocess.run(["git", "clean", "-ndx"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    files = []

    for line in lines:
        if line.startswith("Would remove "):
            path = line.replace("Would remove ", "").strip('"').strip()
            files.append(path)

    return files

def backup_untracked():
    untracked = get_untracked_files()
    if not untracked:
        print("✅ No untracked files to back up.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"untracked_backup_{timestamp}.zip"
    zip_path = Path(zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in untracked:
            path_obj = Path(path)
            if path_obj.is_file():
                zipf.write(path_obj, path_obj)
            elif path_obj.is_dir():
                for root, _, files in os.walk(path_obj):
                    for f in files:
                        full_path = Path(root) / f
                        zipf.write(full_path, full_path.relative_to(path_obj.parent))

    print(f"📦 Backup saved to: {zip_path}")
    print("🔒 You're now safe to run: git clean -fdX")

if __name__ == "__main__":
    backup_untracked()
