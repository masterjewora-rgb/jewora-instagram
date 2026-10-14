"""Render the planned carousel. Usage: python3 make_carousel.py ID1 ID2 ID3 ID4 ID5
Reads plan.json, photos/<id>.png|jpg, writes slides/<carousel>/slide_XX_<id>.jpg and prints their public URLs."""
import json, os, sys, glob
from formats import render

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/masterjewora-rgb/jewora-instagram/main/"

plan = json.load(open(os.path.join(HERE, "plan.json")))
by_id = {c["id"]: c for c in plan["candidates"]}
ids = sys.argv[1:]
prods = []
for pid in ids:
    p = dict(by_id[pid])
    hits = glob.glob(os.path.join(HERE, "photos", pid + ".*"))
    if not hits: sys.exit(f"photo missing for {pid}")
    p["image"] = hits[0]
    prods.append(p)
folder = f"slides/c{plan['carousel_number']:04d}"
out_dir = os.path.join(HERE, folder)
jobs = [(plan["format"], p, i + 1, len(prods), f"slide_{i+1:02d}_{p['id']}.jpg") for i, p in enumerate(prods)]
paths = render(jobs, out_dir)
json.dump({"folder": folder, "ids": ids, "urls": [RAW + folder + "/" + os.path.basename(x) for x in paths]},
          open(os.path.join(HERE, "current.json"), "w"), indent=1)
for x in paths: print(RAW + folder + "/" + os.path.basename(x))
