"""Make a 9:16 Instagram Reel (slideshow + music) from planned products, in one of 12 styles (reel_styles.py).
Usage: python3 reel.py ID1 ID2 ID3 ID4 ID5 [--style KEY] [--music path]
Defaults: style = plan.json "reel_style", music = random track from music/.
Writes reels/rNNNN/reel.mp4 + cover.jpg, current.json, prints public URLs.
Preview all styles as stills: python3 reel.py --preview ID1..ID5 (writes reels/_preview/*.png)"""
import glob, json, os, random, subprocess, sys
from PIL import Image
from playwright.sync_api import sync_playwright
from formats import BASE_CSS, uri_png, uri_jpg, LOGO
from reel_styles import REEL_STYLES, THEME_CSS, esc

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/masterjewora-rgb/jewora-instagram/main/"
W, H, FPS = 1080, 1920, 30

CSS = BASE_CSS.replace("body{width:1080px;height:1350px;overflow:hidden}", "body{width:1080px;height:1920px;overflow:hidden}") + """
.r{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:var(--sans);background:var(--bg);color:var(--fg)}
"""


def intro(c, cover):
    return f"""<div style="position:absolute;inset:0;opacity:.22"><img src="{cover}" style="width:100%;height:100%;object-fit:cover;filter:blur(8px)"></div>
<div style="position:absolute;left:0;right:0;top:560px;display:flex;flex-direction:column;align-items:center;gap:34px;text-align:center">
 <div class="disc" style="width:220px;height:220px"><img src="{c['logo']}"></div>
 <div class="eb" style="font-size:26px;color:var(--acc)">Jewora presents</div>
 <div class="t" style="font-size:110px;line-height:1">The {esc(c['cat'])}<br>Edit</div>
 <div style="width:200px;height:2px;background:var(--acc)"></div>
 <div class="sp" style="font-size:24px">5 handpicked pieces</div></div>"""


def outro(c):
    return f"""<div style="position:absolute;left:0;right:0;top:560px;display:flex;flex-direction:column;align-items:center;gap:36px;text-align:center">
 <div class="disc" style="width:200px;height:200px"><img src="{c['logo']}"></div>
 <div class="ti" style="font-size:64px">Kaunsa pasand aaya?</div>
 <span class="cta" style="font-size:34px;padding:26px 46px">COMMENT “PRICE”</span>
 <div class="sp" style="font-size:24px;line-height:1.6">aur hum turant DM mein<br>price + details bhejenge</div>
 <div class="eb" style="font-size:22px;margin-top:20px;color:var(--acc)">Free shipping all over India</div></div>"""


def page(theme, body):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="r" style="{THEME_CSS[theme]}">{body}</div></body></html>')


def render(pages, out_dir, prefix="f"):
    os.makedirs(out_dir, exist_ok=True); paths = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        for k, html_ in enumerate(pages):
            pg.set_content(html_, wait_until="load"); pg.wait_for_timeout(120)
            p = os.path.join(out_dir, f"{prefix}{k:02d}.png"); pg.screenshot(path=p); paths.append(p)
        br.close()
    return paths


def motion_filter(k, n, mode):
    if mode == "alt": mode = "zin" if k % 2 == 0 else "zout"
    if mode == "zin":  z, x = f"1+0.05*on/{n}", "iw/2-(iw/zoom/2)"
    elif mode == "zout": z, x = f"1.05-0.05*on/{n}", "iw/2-(iw/zoom/2)"
    else:  # pan sideways at fixed zoom
        z = "1.06"; x = f"(iw-iw/zoom)*({'on' if k % 2 == 0 else f'{n}-on'})/{n}"
    return f"scale=1188:2112,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS}"


def build_video(frames, durs, music, out, transition, motion):
    xf = 0.5; inputs, flt = [], []
    for k, (f, d) in enumerate(zip(frames, durs)):
        inputs += ["-loop", "1", "-t", f"{d}", "-i", f]
        flt.append(f"[{k}:v]{motion_filter(k, int(d * FPS), motion)},setsar=1,format=yuv420p[v{k}]")
    last, t = "v0", durs[0]
    for k in range(1, len(frames)):
        tr = "fade" if k in (1, len(frames) - 1) else transition     # intro/outro always soft fade
        flt.append(f"[{last}][v{k}]xfade=transition={tr}:duration={xf}:offset={t - xf:.2f}[x{k}]")
        last, t = f"x{k}", t + durs[k] - xf
    flt.append(f"[{len(frames)}:a]atrim=0:{t:.2f},afade=t=in:d=0.6,afade=t=out:st={t-1.5:.2f}:d=1.5,volume=0.9[a]")
    cmd = ["ffmpeg", "-y", *inputs, "-i", music, "-filter_complex", ";".join(flt), "-map", f"[{last}]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{t:.2f}", out]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return t


def load(ids):
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    by_id = {c["id"]: c for c in plan["candidates"]}
    prods = []
    for pid in ids:
        p = dict(by_id[pid]); p["image"] = glob.glob(os.path.join(HERE, "photos", pid + ".*"))[0]; prods.append(p)
    return plan, prods


def ctxs(prods, logo):
    cat = prods[0]["eyebrow"].split("·")[-1].strip()
    return [dict(p=p, img=uri_jpg(p["image"], 1200), logo=logo, cat=cat, i=k + 1, n=len(prods)) for k, p in enumerate(prods)]


def main():
    a = sys.argv[1:]
    opt = lambda name: (a.pop(a.index(name) + 1), a.remove(name))[0] if name in a else None
    preview = "--preview" in a
    if preview: a.remove("--preview")
    style, music = opt("--style"), opt("--music")
    plan, prods = load(a)
    logo = uri_png(Image.open(LOGO))
    cs = ctxs(prods, logo)
    if preview:
        pages = [page(REEL_STYLES[k][2], REEL_STYLES[k][1](cs[j % len(cs)])) for j, k in enumerate(REEL_STYLES)]
        for p in render(pages, os.path.join(HERE, "reels", "_preview"), "s"): print(p)
        return
    style = style or plan["reel_style"]
    label, layout, theme, transition, motion = REEL_STYLES[style]
    music = music or random.choice(sorted(glob.glob(os.path.join(HERE, "music", "*.*"))))
    pages = [page(theme, intro(cs[0], uri_jpg(prods[0]["image"], 800)))] + [page(theme, layout(c)) for c in cs] + [page(theme, outro(cs[0]))]
    folder = f"reels/r{plan['carousel_number']:04d}"
    out_dir = os.path.join(HERE, folder); os.makedirs(out_dir, exist_ok=True)
    frames = render(pages, os.path.join(HERE, "photos", "_frames"))
    durs = [2.2] + [2.8] * len(prods) + [2.6]
    total = build_video(frames, durs, music, os.path.join(out_dir, "reel.mp4"), transition, motion)
    Image.open(frames[1]).convert("RGB").save(os.path.join(out_dir, "cover.jpg"), quality=90)
    json.dump({"folder": folder, "ids": a, "kind": "reel", "style": style, "music": os.path.basename(music),
               "video_url": RAW + folder + "/reel.mp4", "cover_url": RAW + folder + "/cover.jpg"},
              open(os.path.join(HERE, "current.json"), "w"), indent=1)
    print(f"{label} | {total:.1f}s | music {os.path.basename(music)}")
    print(RAW + folder + "/reel.mp4"); print(RAW + folder + "/cover.jpg")


if __name__ == "__main__":
    main()
