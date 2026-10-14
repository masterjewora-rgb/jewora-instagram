"""Make a 9:16 Instagram Reel (slideshow with music) from the planned products.
Usage: python3 reel.py ID1 ID2 ID3 ID4 ID5 [--music path.mp3|wav]
Reads plan.json + photos/<id>.jpg, writes reels/rNNNN/reel.mp4 (+ cover.jpg) and prints public URLs.
Without --music it uses a random track from music/ (royalty-free / generated)."""
import glob, json, os, random, subprocess, sys
from PIL import Image
from playwright.sync_api import sync_playwright
from formats import BASE_CSS, uri_png, uri_jpg, LOGO
import html

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/masterjewora-rgb/jewora-instagram/main/"
W, H = 1080, 1920

CSS = BASE_CSS.replace("body{width:1080px;height:1350px;overflow:hidden}", "body{width:1080px;height:1920px;overflow:hidden}") + """
.r{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:var(--sans);color:var(--cream);
 background:radial-gradient(ellipse 90% 60% at 50% 45%,#3A5239,var(--g) 50%,var(--gd))}
.hdr{position:absolute;left:0;right:0;top:200px;display:flex;flex-direction:column;align-items:center;gap:18px}
.ph2{position:absolute;left:60px;top:400px;width:960px;height:960px;border:3px solid var(--gold);box-shadow:0 30px 70px rgba(0,0,0,.45);overflow:hidden}
.ph2 img{width:100%;height:100%;object-fit:cover}
.txt{position:absolute;left:70px;right:70px;top:1395px;text-align:center}
"""


def esc(s): return html.escape(s or "")


def frame_product(p, i, n, logo, cat_label):
    return f"""<div class="r"><div class="hdr">
 <div class="disc" style="width:120px;height:120px"><img src="{logo}"></div>
 <div class="eb" style="font-size:24px">{esc(cat_label)} · {i:02d} / {n:02d}</div></div>
<div class="ph2"><img src="{uri_jpg(p['image'], 1200)}"></div>
<div class="txt"><div class="eb" style="font-size:20px">{esc(p.get('eyebrow',''))}</div>
 <div class="t" style="font-size:{64 if len(p['title'])<=24 else 54}px;margin-top:12px">{esc(p['title'])}</div>
 <div style="margin-top:26px"><span class="cta" style="font-size:24px;padding:18px 34px">COMMENT “PRICE”</span></div></div></div>"""


def frame_intro(logo, cat_label, cover_img):
    return f"""<div class="r">
<div style="position:absolute;inset:0;opacity:.28"><img src="{cover_img}" style="width:100%;height:100%;object-fit:cover;filter:blur(6px)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(27,38,27,.55),rgba(27,38,27,.9))"></div>
<div style="position:absolute;left:0;right:0;top:560px;display:flex;flex-direction:column;align-items:center;gap:34px;text-align:center">
 <div class="disc" style="width:220px;height:220px"><img src="{logo}"></div>
 <div class="eb" style="font-size:26px">Jewora presents</div>
 <div class="t" style="font-size:110px;line-height:1">The {esc(cat_label)}<br>Edit</div>
 <div style="width:200px;height:2px;background:var(--gold)"></div>
 <div class="sp" style="font-size:24px">5 handpicked pieces</div></div></div>"""


def frame_outro(logo):
    return f"""<div class="r"><div style="position:absolute;left:0;right:0;top:560px;display:flex;flex-direction:column;align-items:center;gap:36px;text-align:center">
 <div class="disc" style="width:200px;height:200px"><img src="{logo}"></div>
 <div class="ti" style="font-size:64px">Kaunsa pasand aaya?</div>
 <span class="cta" style="font-size:34px;padding:26px 46px">COMMENT “PRICE”</span>
 <div class="sp" style="font-size:24px;line-height:1.6">aur hum turant DM mein<br>price + details bhejenge</div>
 <div class="eb" style="font-size:22px;margin-top:20px">Free shipping all over India</div></div></div>"""


def render_frames(htmls, out_dir):
    paths = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        for k, body in enumerate(htmls):
            pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>', wait_until="load")
            pg.wait_for_timeout(120)
            p = os.path.join(out_dir, f"f{k:02d}.png"); pg.screenshot(path=p); paths.append(p)
        br.close()
    return paths


def build_video(frames, durs, music, out):
    fps, xf = 30, 0.5
    inputs, filters = [], []
    for k, (f, d) in enumerate(zip(frames, durs)):
        inputs += ["-loop", "1", "-t", f"{d}", "-i", f]
        n = int(d * fps)
        z = "1+0.045*on/%d" % n if k % 2 == 0 else "1.045-0.045*on/%d" % n   # gentle zoom in / out
        filters.append(f"[{k}:v]scale=1188:2112,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={fps},setsar=1,format=yuv420p[v{k}]")
    last, t = "v0", durs[0]
    for k in range(1, len(frames)):
        off = t - xf
        filters.append(f"[{last}][v{k}]xfade=transition=fade:duration={xf}:offset={off:.2f}[x{k}]")
        last, t = f"x{k}", t + durs[k] - xf
    total = t
    filters.append(f"[{len(frames)}:a]atrim=0:{total:.2f},afade=t=in:d=0.6,afade=t=out:st={total-1.5:.2f}:d=1.5,volume=0.9[a]")
    cmd = ["ffmpeg", "-y", *inputs, "-i", music, "-filter_complex", ";".join(filters), "-map", f"[{last}]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(fps),
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{total:.2f}", out]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return total


def main():
    args = sys.argv[1:]
    music = None
    if "--music" in args:
        i = args.index("--music"); music = args[i + 1]; args = args[:i] + args[i + 2:]
    if not music:
        tracks = sorted(glob.glob(os.path.join(HERE, "music", "*.*")))
        music = random.choice(tracks)
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    by_id = {c["id"]: c for c in plan["candidates"]}
    prods = []
    for pid in args:
        p = dict(by_id[pid]); p["image"] = glob.glob(os.path.join(HERE, "photos", pid + ".*"))[0]; prods.append(p)
    cat_label = prods[0]["eyebrow"].split("·")[-1].strip()
    folder = f"reels/r{plan['carousel_number']:04d}"
    out_dir = os.path.join(HERE, folder); os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(HERE, "photos", "_frames"); os.makedirs(tmp, exist_ok=True)
    logo = uri_png(Image.open(LOGO))
    htmls = [frame_intro(logo, cat_label, uri_jpg(prods[0]["image"], 800))]
    htmls += [frame_product(p, k + 1, len(prods), logo, cat_label) for k, p in enumerate(prods)]
    htmls += [frame_outro(logo)]
    frames = render_frames(htmls, tmp)
    durs = [2.2] + [2.8] * len(prods) + [2.6]
    video = os.path.join(out_dir, "reel.mp4")
    total = build_video(frames, durs, music, video)
    Image.open(frames[1]).convert("RGB").save(os.path.join(out_dir, "cover.jpg"), quality=90)
    json.dump({"folder": folder, "ids": args, "kind": "reel", "music": os.path.basename(music),
               "video_url": RAW + folder + "/reel.mp4", "cover_url": RAW + folder + "/cover.jpg"},
              open(os.path.join(HERE, "current.json"), "w"), indent=1)
    print(f"{total:.1f}s", RAW + folder + "/reel.mp4", RAW + folder + "/cover.jpg")


if __name__ == "__main__":
    main()
