"""Save Drive download results (mp3/m4a, base64 JSON) into music/ as 32-second 160k MP3 clips.
Usage: python3 add_music.py RESULT_FILE [...]"""
import base64, json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "music"), exist_ok=True)
for f in sys.argv[1:]:
    j = json.load(open(f))
    name = re.sub(r"[^a-z0-9]+", "_", os.path.splitext(j["title"])[0].lower()).strip("_") + ".mp3"
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(j["title"])[1]) as t:
        t.write(base64.b64decode(j["content"])); t.flush()
        out = os.path.join(HERE, "music", name)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", t.name, "-t", "32", "-ac", "2", "-b:a", "160k", out], check=True)
    print(j["title"], "->", out)
