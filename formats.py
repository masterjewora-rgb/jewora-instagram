"""Jewora Instagram carousel formats (12 layouts). Photo is always shown whole; text never sits on the product.
Usage: python3 formats.py products.json out_dir FORMAT_KEY   (FORMAT_KEY from FORMATS, or 'all' for a preview of every format)
products.json: [{"id","title","eyebrow","specs":[[label,value],...],"price","image"}]
"""
import base64, io, json, os, re, sys, html
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo_clean.png")  # original green bag, transparent background

BASE_CSS = """
:root{--g:#2F402F;--gd:#1B261B;--gl:#46604A;--gold:#C9A46C;--goldl:#E8CFA2;--cream:#F6EBDD;--paper:#FBF6EE;--ink:#1E2A1E;
--disp:'GFS Baskerville','Lora',serif;--ital:'Lora',serif;--sans:'Poppins',sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:var(--sans)}
.ph{position:absolute;overflow:hidden}.ph img{width:100%;height:100%;object-fit:cover;display:block}
.eb{font-size:20px;letter-spacing:.38em;text-transform:uppercase;font-weight:500;color:var(--gold)}
.t{font-family:var(--disp);font-variant:small-caps;font-weight:400;line-height:1.04;letter-spacing:.02em;text-wrap:balance}
.ti{font-family:var(--ital);font-style:italic;font-weight:500;line-height:1.08;text-wrap:balance}
.cta{display:inline-block;background:linear-gradient(135deg,var(--goldl),var(--gold) 55%,#A9824C);color:var(--gd);
  padding:18px 34px;font-size:28px;font-weight:700;letter-spacing:.14em;white-space:nowrap;border-radius:6px;
  box-shadow:0 6px 18px rgba(0,0,0,.28);text-shadow:none}
.cta.dark{background:var(--g);color:var(--cream)}
.pr{font-family:var(--disp);font-size:52px;filter:blur(9px);opacity:.8;line-height:1}
.disc{border-radius:50%;background:var(--cream);display:grid;place-items:center;border:2px solid var(--gold)}
.disc img{width:54%;height:auto;display:block}
.bag{display:block}
.idx{font-family:var(--disp);font-size:28px;letter-spacing:.14em}
.sp{font-size:19px;letter-spacing:.2em;text-transform:uppercase}
"""


def uri_png(img):
    b = io.BytesIO(); img.save(b, "PNG"); return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def uri_jpg(path, size=1400):
    im = Image.open(path).convert("RGB")
    im.thumbnail((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=93)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def ctx(p, i, n, logo):
    e = html.escape
    return dict(
        img=uri_jpg(p["image"]) if p.get("image") and os.path.exists(p["image"]) else "",
        title=e(p["title"]), eb=e(p.get("eyebrow", "")), price=f"₹{e(p['price'])}" if p.get("price") else "",
        specs=" · ".join(f"{e(k)} <b>{e(v)}</b>" for k, v in p.get("specs", []) if v),
        idx=f"{i:02d} / {n:02d}", num=f"{i:02d}", logo=logo)


# ---------------- formats ----------------
def f_classic_band(c):
    return f"""<div class="s" style="background:var(--g)">
<div class="ph" style="left:0;top:0;width:1080px;height:1080px"><img src="{c['img']}"></div>
<div style="position:absolute;left:0;right:0;top:1080px;height:270px;display:flex;align-items:center;gap:30px;padding:0 50px;color:var(--cream)">
 <div class="disc" style="width:120px;height:120px;flex:none"><img src="{c['logo']}"></div>
 <div style="flex:1;min-width:0"><div class="eb">{c['eb']}</div><div class="t" style="font-size:52px;margin-top:10px">{c['title']}</div></div>
 <div style="display:flex;flex-direction:column;align-items:flex-end;gap:14px;flex:none"><div class="pr">{c['price']}</div><div class="cta">COMMENT “PRICE”</div></div>
</div></div>"""


def f_masthead_top(c):
    return f"""<div class="s" style="background:var(--paper)">
<div style="position:absolute;left:0;right:0;top:0;height:270px;display:flex;align-items:center;gap:34px;padding:0 56px">
 <img class="bag" src="{c['logo']}" style="height:170px">
 <div style="flex:1;min-width:0"><div class="eb" style="color:#9C7A45">{c['eb']}</div>
  <div class="t" style="font-size:56px;color:var(--g);margin-top:8px">{c['title']}</div>
  <div style="margin-top:14px;display:flex;gap:18px;align-items:center"><span class="cta dark">COMMENT “PRICE”</span><span class="idx" style="color:var(--gold)">{c['idx']}</span></div></div>
</div>
<div class="ph" style="left:0;top:270px;width:1080px;height:1080px"><img src="{c['img']}"></div></div>"""


def f_gallery_frame(c):
    return f"""<div class="s" style="background:#F2E9DA">
<div style="position:absolute;left:70px;right:70px;top:40px;height:80px;display:flex;align-items:center;justify-content:space-between;color:var(--g)">
 <span class="idx">{c['idx']}</span><img src="{c['logo']}" style="height:84px"><span class="sp" style="font-size:17px">The Jewora Edit</span></div>
<div style="position:absolute;left:58px;top:138px;width:964px;height:964px;border:2px solid var(--gold);padding:12px">
 <div class="ph" style="position:relative;width:100%;height:100%"><img src="{c['img']}"></div></div>
<div style="position:absolute;left:60px;right:60px;top:1125px;text-align:center;color:var(--g)">
 <div class="eb" style="color:#9C7A45">{c['eb']}</div><div class="t" style="font-size:54px;margin-top:8px">{c['title']}</div>
 <div style="margin-top:16px"><span class="cta dark">COMMENT “PRICE”</span></div></div></div>"""


def f_polaroid(c):
    return f"""<div class="s" style="background:radial-gradient(ellipse 80% 60% at 50% 40%,var(--gl),var(--g) 55%,var(--gd))">
<div style="position:absolute;left:80px;top:56px;width:920px;background:#FFFDF8;padding:34px 34px 0;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(0,0,0,.4)">
 <div class="ph" style="position:relative;width:852px;height:852px"><img src="{c['img']}"></div>
 <div class="ti" style="font-size:50px;color:var(--g);text-align:center;padding:26px 0 30px">{c['title']}</div></div>
<div style="position:absolute;left:70px;right:70px;bottom:52px;display:flex;align-items:center;justify-content:space-between">
 <div class="disc" style="width:120px;height:120px"><img src="{c['logo']}"></div>
 <div class="eb" style="flex:1;text-align:center;font-size:18px">{c['eb']}</div><span class="cta">COMMENT “PRICE”</span></div></div>"""


def f_two_tone(c):
    return f"""<div class="s" style="background:var(--paper)">
<div class="ph" style="left:0;top:0;width:1080px;height:1080px"><img src="{c['img']}"></div>
<div style="position:absolute;left:0;top:1080px;width:670px;height:270px;padding:34px 40px 0 50px;display:flex;gap:26px">
 <img src="{c['logo']}" style="height:120px;flex:none">
 <div style="min-width:0"><div class="eb" style="color:#9C7A45;font-size:17px">{c['eb']}</div><div class="t" style="font-size:48px;color:var(--g);margin-top:8px">{c['title']}</div>
 <div class="sp" style="margin-top:12px;color:#6B7A68;font-size:16px">{c['specs']}</div></div></div>
<div style="position:absolute;left:670px;right:0;top:1080px;height:270px;background:var(--g);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;color:var(--cream)">
 <div class="pr">{c['price']}</div><span class="cta">COMMENT “PRICE”</span><span class="idx" style="font-size:22px;color:var(--gold)">{c['idx']}</span></div></div>"""


def f_arch(c):
    return f"""<div class="s" style="background:var(--g)">
<div class="ph" style="left:90px;top:60px;width:900px;height:1000px;border-radius:450px 450px 0 0;border:3px solid var(--gold)"><img src="{c['img']}"></div>
<span class="idx" style="position:absolute;left:40px;top:44px;color:var(--cream);font-size:24px">{c['idx']}</span>
<div class="disc" style="position:absolute;right:30px;top:30px;width:120px;height:120px"><img src="{c['logo']}"></div>
<div style="position:absolute;left:60px;right:60px;top:1092px;text-align:center;color:var(--cream)">
 <div class="eb">{c['eb']}</div><div class="t" style="font-size:54px;margin-top:8px">{c['title']}</div>
 <div style="margin-top:18px"><span class="cta">COMMENT “PRICE”</span></div></div></div>"""


def f_magazine_strip(c):
    return f"""<div class="s" style="background:var(--gd)">
<div style="position:absolute;left:0;right:0;top:0;height:110px;display:flex;align-items:center;justify-content:space-between;padding:0 44px;color:var(--cream)">
 <span class="idx" style="font-size:24px">{c['idx']}</span>
 <span style="font-family:var(--disp);font-size:56px;letter-spacing:.42em;padding-left:.42em">JEWORA</span>
 <div class="disc" style="width:84px;height:84px"><img src="{c['logo']}"></div></div>
<div class="ph" style="left:0;top:110px;width:1080px;height:1080px"><img src="{c['img']}"></div>
<div style="position:absolute;left:0;right:0;top:1190px;height:160px;display:flex;align-items:center;gap:24px;padding:0 44px;color:var(--cream)">
 <div style="flex:1;min-width:0"><div class="eb" style="font-size:16px">{c['eb']}</div><div class="t" style="font-size:44px;margin-top:6px">{c['title']}</div></div>
 <span class="cta" style="flex:none">COMMENT “PRICE”</span></div></div>"""


def f_price_tag(c):
    return f"""<div class="s" style="background:var(--paper)">
<div class="ph" style="left:0;top:0;width:1080px;height:1080px"><img src="{c['img']}"></div>
<div style="position:absolute;left:0;right:0;top:1080px;height:270px;display:flex;align-items:center;gap:28px;padding:0 0 0 50px">
 <img src="{c['logo']}" style="height:130px;flex:none">
 <div style="flex:1;min-width:0"><div class="eb" style="color:#9C7A45;font-size:17px">{c['eb']}</div><div class="t" style="font-size:48px;color:var(--g);margin-top:8px">{c['title']}</div></div>
 <div style="flex:none;width:330px;height:190px;background:var(--g);color:var(--cream);clip-path:polygon(16% 0,100% 0,100% 100%,16% 100%,0 50%);
   display:flex;flex-direction:column;justify-content:center;align-items:center;gap:10px;padding-left:40px;position:relative">
  <div style="position:absolute;left:44px;top:50%;width:22px;height:22px;margin-top:-11px;border-radius:50%;background:var(--paper)"></div>
  <div class="pr" style="font-size:44px">{c['price']}</div><div style="font-size:24px;font-weight:700;letter-spacing:.08em;white-space:nowrap">COMMENT “PRICE”</div></div></div></div>"""


def f_big_number(c):
    return f"""<div class="s" style="background:var(--paper)">
<div class="ph" style="left:0;top:0;width:1080px;height:1080px"><img src="{c['img']}"></div>
<div style="position:absolute;left:0;right:0;top:1080px;height:270px;display:flex;align-items:center;gap:30px;padding:0 50px">
 <div style="font-family:var(--ital);font-size:190px;line-height:.8;color:var(--gold);flex:none">{c['num']}</div>
 <div style="flex:1;min-width:0;border-left:2px solid var(--gold);padding-left:30px"><div class="eb" style="color:#9C7A45;font-size:17px">{c['eb']}</div>
  <div class="t" style="font-size:48px;color:var(--g);margin-top:8px">{c['title']}</div>
  <div style="margin-top:14px"><span class="cta dark">COMMENT “PRICE”</span></div></div>
 <img src="{c['logo']}" style="height:130px;flex:none"></div></div>"""


def f_luxe_border(c):
    return f"""<div class="s" style="background:radial-gradient(ellipse 90% 70% at 50% 35%,#24331F,var(--gd))">
<div style="position:absolute;left:60px;top:56px;width:960px;height:960px;outline:2px solid var(--gold);outline-offset:14px;border:2px solid var(--gold)">
 <div class="ph" style="position:relative;width:100%;height:100%"><img src="{c['img']}"></div></div>
<div style="position:absolute;left:60px;right:60px;top:1062px;text-align:center;color:var(--cream)">
 <div class="eb">{c['eb']}</div><div class="t" style="font-size:52px;margin-top:8px">{c['title']}</div></div>
<div style="position:absolute;left:60px;right:60px;bottom:40px;display:flex;align-items:center;justify-content:space-between">
 <span class="idx" style="color:var(--gold);font-size:24px">{c['idx']}</span><span class="cta">COMMENT “PRICE”</span>
 <div class="disc" style="width:96px;height:96px"><img src="{c['logo']}"></div></div></div>"""


def f_minimal_white(c):
    return f"""<div class="s" style="background:#FFFFFF">
<div class="ph" style="left:0;top:0;width:1080px;height:1080px"><img src="{c['img']}"></div>
<div style="position:absolute;left:60px;right:60px;top:1112px;display:flex;align-items:center;gap:30px">
 <img src="{c['logo']}" style="height:120px;flex:none">
 <div style="flex:1;min-width:0;text-align:center"><div class="t" style="font-size:46px;color:var(--g)">{c['title']}</div>
  <div style="height:1px;background:var(--gold);margin:14px 80px"></div>
  <div style="margin-top:6px"><span class="cta dark" style="font-size:24px;padding:14px 26px">COMMENT “PRICE”</span></div></div>
 <span class="idx" style="color:var(--gold);font-size:24px;flex:none">{c['idx']}</span></div></div>"""


def f_side_spine(c):
    return f"""<div class="s" style="background:var(--paper)">
<div style="position:absolute;left:0;top:0;width:140px;height:1350px;background:var(--g);display:flex;flex-direction:column;align-items:center;padding-top:24px;gap:40px">
 <div class="disc" style="width:104px;height:104px"><img src="{c['logo']}"></div>
 <div style="writing-mode:vertical-rl;transform:rotate(180deg);color:var(--cream);font-family:var(--disp);font-size:34px;letter-spacing:.32em">JEWORA · THE EDIT · NO. {c['num']}</div></div>
<div class="ph" style="left:140px;top:0;width:940px;height:940px"><img src="{c['img']}"></div>
<div style="position:absolute;left:200px;right:60px;top:985px;color:var(--g)">
 <div class="eb" style="color:#9C7A45">{c['eb']}</div><div class="t" style="font-size:64px;margin-top:10px">{c['title']}</div>
 <div class="sp" style="margin-top:16px;color:#6B7A68">{c['specs']}</div>
 <div style="margin-top:24px;display:flex;align-items:center;gap:26px"><span class="cta dark">COMMENT “PRICE”</span><span class="pr" style="color:var(--g);font-size:44px">{c['price']}</span></div></div></div>"""


FORMATS = {
    "classic_band": ("Classic Band", f_classic_band),
    "masthead_top": ("Masthead Top", f_masthead_top),
    "gallery_frame": ("Gallery Frame", f_gallery_frame),
    "polaroid": ("Polaroid", f_polaroid),
    "two_tone": ("Two-Tone Band", f_two_tone),
    "arch": ("Arch Window", f_arch),
    "magazine_strip": ("Magazine Strip", f_magazine_strip),
    "price_tag": ("Price Tag", f_price_tag),
    "big_number": ("Big Number", f_big_number),
    "luxe_border": ("Luxe Border", f_luxe_border),
    "minimal_white": ("Minimal White", f_minimal_white),
    "side_spine": ("Side Spine", f_side_spine),
}


def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>{body}</body></html>'


def render(jobs, out_dir):
    """jobs: list of (format_key, product, index, total, out_name)"""
    os.makedirs(out_dir, exist_ok=True)
    logo = uri_png(Image.open(LOGO))
    paths = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1350})
        for key, p, i, n, name in jobs:
            body = FORMATS[key][1](ctx(p, i, n, logo))
            L = len(p["title"])
            k = 1 if L <= 22 else (0.86 if L <= 30 else 0.76)
            body = re.sub(r'class="(t|ti)" style="font-size:(\d+)px', lambda m: f'class="{m.group(1)}" style="font-size:{int(int(m.group(2))*k)}px', body)
            pg.set_content(page(body), wait_until="load")
            pg.wait_for_timeout(120)
            out = os.path.join(out_dir, name)
            pg.screenshot(path=out, type="jpeg", quality=92)
            paths.append(out)
        br.close()
    return paths


if __name__ == "__main__":
    prods = json.load(open(sys.argv[1])); out = sys.argv[2]; key = sys.argv[3]
    if key == "all":
        jobs = [(k, prods[j % len(prods)], j % len(prods) + 1, len(prods), f"{j+1:02d}_{k}.jpg") for j, k in enumerate(FORMATS)]
    else:
        jobs = [(key, p, i + 1, len(prods), f"slide_{i+1:02d}_{p['id']}.jpg") for i, p in enumerate(prods)]
    for p in render(jobs, out):
        print(p)
