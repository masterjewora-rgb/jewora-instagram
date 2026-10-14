"""After a successful Instagram post: python3 record.py MEDIA_ID
Appends the posted product ids to posted.csv and bumps state.json. Optional: --missing ID [ID..] only records missing photos."""
import csv, json, os, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
if sys.argv[1] == "--missing":
    with open(os.path.join(HERE, "missing_photos.txt"), "a") as f:
        for pid in sys.argv[2:]: f.write(pid + "\n")
    sys.exit()
media_id = sys.argv[1]
plan = json.load(open(os.path.join(HERE, "plan.json")))
cur = json.load(open(os.path.join(HERE, "current.json")))
today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
new = not os.path.exists(os.path.join(HERE, "posted.csv"))
with open(os.path.join(HERE, "posted.csv"), "a", newline="") as f:
    w = csv.writer(f)
    if new: w.writerow(["id", "posted_at", "carousel", "format", "category", "media_id"])
    for pid in cur["ids"]:
        w.writerow([pid, today, plan["carousel_number"], ("reel:" + plan["reel_style"]) if cur.get("kind") == "reel" else plan["format"], plan["category"], media_id])
st = json.load(open(os.path.join(HERE, "state.json")))
key = "reels_posted" if cur.get("kind") == "reel" else "carousels_posted"
st[key] = st.get(key, 0) + 1
json.dump(st, open(os.path.join(HERE, "state.json"), "w"))
print("recorded", cur["ids"], "carousel", plan["carousel_number"])
