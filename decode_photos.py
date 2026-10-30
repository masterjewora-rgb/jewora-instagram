"""Decode Google Drive download_file_content results (JSON with base64 'content' + 'title') into photos/<title>.
Usage: python3 decode_photos.py RESULT_FILE [RESULT_FILE ...]   (photos are shrunk to 1600px JPEG-quality PNG->JPG)"""
import base64, io, json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "photos"), exist_ok=True)
# Raw image results (newer Drive tool saves the image file itself): pass RESULT_FILE=ID
for f in sys.argv[1:]:
    pid = None
    if "=" in f:
        f, pid = f.rsplit("=", 1)
    try:
        j = json.load(open(f))
        im = Image.open(io.BytesIO(base64.b64decode(j["content"]))).convert("RGB")
        pid = pid or os.path.splitext(j["title"])[0]
    except (UnicodeDecodeError, json.JSONDecodeError):
        im = Image.open(f).convert("RGB")
        assert pid, "raw image result needs RESULT_FILE=ID"
    im.thumbnail((1600, 1600), Image.LANCZOS)
    out = os.path.join(HERE, "photos", pid + ".jpg")
    im.save(out, "JPEG", quality=92)
    print(pid, im.size, "->", out)
