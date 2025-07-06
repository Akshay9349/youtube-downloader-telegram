import re

def clean_filename(title):
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    return title.strip()
