"""12 Reel styles. Each = product-frame layout + light/dark theme + transition + motion.
Instagram covers ~220px at top and ~380px at bottom (+ icons on the right), so text stays between y=220 and y=1560."""
import html

def esc(s): return html.escape(s or "")

THEME_CSS = {
    "dark": "--bg:radial-gradient(ellipse 90% 60% at 50% 45%,#3A5239,#2F402F 50%,#1B261B);--fg:#F6EBDD;--acc:#C9A46C;--sub:#B9C4B3",
    "light": "--bg:linear-gradient(180deg,#FBF6EE,#F2E9DA);--fg:#2F402F;--acc:#9C7A45;--sub:#6B7A68",
    "white": "--bg:#FFFFFF;--fg:#2F402F;--acc:#9C7A45;--sub:#6B7A68",
}


def _title(p, big=64, small=52):
    return big if len(p["title"]) <= 24 else small


def head(c, top=200):
    return f"""<div style="position:absolute;left:0;right:0;top:{top}px;display:flex;flex-direction:column;align-items:center;gap:16px">
 <div class="disc" style="width:110px;height:110px"><img src="{c['logo']}"></div>
 <div class="eb" style="font-size:22px;color:var(--acc)">{esc(c['cat'])} · {c['i']:02d} / {c['n']:02d}</div></div>"""


def cta(dark_btn=False, size=44):
    cls = "cta dark" if dark_btn else "cta"
    return f'<span class="{cls}" style="font-size:{size}px;padding:28px 60px;letter-spacing:.12em">COMMENT “PRICE”</span>'


def text_block(c, top, align="center", dark_btn=False, italic=False):
    p = c["p"]; cls = "ti" if italic else "t"
    return f"""<div style="position:absolute;left:80px;right:80px;top:{top}px;text-align:{align};color:var(--fg)">
 <div class="eb" style="font-size:19px;color:var(--acc)">{esc(p.get('eyebrow',''))}</div>
 <div class="{cls}" style="font-size:{_title(p)}px;margin-top:12px">{esc(p['title'])}</div>
 <div style="margin-top:26px">{cta(dark_btn)}</div></div>"""


def img(c, style):
    return f'<div style="position:absolute;overflow:hidden;{style}"><img src="{c["img"]}" style="width:100%;height:100%;object-fit:cover;display:block"></div>'


# ---------------- layouts ----------------
def L_gold_frame(c):
    return head(c) + img(c, "left:60px;top:400px;width:960px;height:960px;border:3px solid var(--acc);box-shadow:0 30px 70px rgba(0,0,0,.45)") + text_block(c, 1395)

def L_full_bleed(c):
    return head(c, 170) + img(c, "left:0;top:380px;width:1080px;height:1080px") + text_block(c, 1490)

def L_cream_gallery(c):
    return head(c) + f'<div style="position:absolute;left:70px;top:395px;width:940px;height:940px;border:2px solid var(--acc);padding:12px">' \
        + img(c, "left:12px;top:12px;right:12px;bottom:12px") + "</div>" + text_block(c, 1370, dark_btn=True)

def L_arch(c):
    return head(c, 170) + img(c, "left:90px;top:360px;width:900px;height:1040px;border-radius:450px 450px 0 0;border:3px solid var(--acc)") + text_block(c, 1425)

def L_polaroid(c):
    rot = -2.5 if c["i"] % 2 else 2.5
    return head(c) + f"""<div style="position:absolute;left:95px;top:400px;width:890px;background:#FFFDF8;padding:30px 30px 0;transform:rotate({rot}deg);box-shadow:0 30px 60px rgba(0,0,0,.4)">
 <div style="width:830px;height:830px;overflow:hidden"><img src="{c['img']}" style="width:100%;height:100%;object-fit:cover"></div>
 <div class="ti" style="font-size:46px;color:#2F402F;text-align:center;padding:22px 0 26px">{esc(c['p']['title'])}</div></div>
<div style="position:absolute;left:0;right:0;top:1440px;text-align:center">{cta()}</div>"""

def L_rounded_card(c):
    return head(c) + img(c, "left:70px;top:400px;width:940px;height:940px;border-radius:48px;box-shadow:0 26px 60px rgba(47,64,47,.28)") + text_block(c, 1385, dark_btn=True, italic=True)

def L_magazine(c):
    return f"""<div style="position:absolute;left:0;right:0;top:190px;text-align:center;color:var(--fg)">
 <div style="font-family:var(--disp);font-size:130px;letter-spacing:.2em;padding-left:.2em;line-height:1">JEWORA</div>
 <div style="margin:14px 80px 0;border-top:2px solid var(--acc);border-bottom:1px solid var(--acc);padding:10px 0;display:flex;justify-content:space-between" class="eb">
 <span style="color:var(--acc);font-size:19px">The {esc(c['cat'])} Issue</span><span style="color:var(--acc);font-size:19px">No. {c['i']:02d}</span></div></div>""" \
        + img(c, "left:80px;top:430px;width:920px;height:920px") + text_block(c, 1385, italic=True)

def L_big_number(c):
    p = c["p"]
    return head(c) + img(c, "left:0;top:400px;width:1080px;height:1080px") + f"""
<div style="position:absolute;left:70px;right:70px;top:1500px;display:flex;align-items:center;gap:28px;color:var(--fg)">
 <div style="font-family:var(--ital);font-size:150px;line-height:.8;color:var(--acc)">{c['i']:02d}</div>
 <div style="border-left:2px solid var(--acc);padding-left:26px;min-width:0"><div class="t" style="font-size:{_title(p,50,42)}px">{esc(p['title'])}</div>
 <div style="margin-top:14px">{cta(size=36)}</div></div></div>"""

def L_split_color(c):
    return f'<div style="position:absolute;left:0;right:0;top:0;height:880px;background:#2F402F"></div>' \
        + f"""<div style="position:absolute;left:0;right:0;top:200px;display:flex;flex-direction:column;align-items:center;gap:14px">
 <div class="disc" style="width:110px;height:110px"><img src="{c['logo']}"></div>
 <div class="eb" style="font-size:22px">{esc(c['cat'])} · {c['i']:02d} / {c['n']:02d}</div></div>""" \
        + img(c, "left:110px;top:420px;width:860px;height:860px;box-shadow:0 30px 60px rgba(0,0,0,.35)") + text_block(c, 1320, dark_btn=True)

def L_minimal_white(c):
    p = c["p"]
    return img(c, "left:0;top:300px;width:1080px;height:1080px") + f"""
<div style="position:absolute;left:0;right:0;top:170px;display:flex;justify-content:center"><img src="{c['logo']}" style="height:105px"></div>
<div style="position:absolute;left:80px;right:80px;top:1420px;text-align:center;color:var(--fg)">
 <div class="t" style="font-size:{_title(p,56,46)}px">{esc(p['title'])}</div>
 <div style="height:1px;background:var(--acc);margin:18px 200px"></div>
 <div style="margin-top:10px">{cta(dark_btn=True)}</div></div>"""

def L_luxe_border(c):
    return head(c) + f'<div style="position:absolute;left:80px;top:410px;width:920px;height:920px;border:2px solid var(--acc);outline:2px solid var(--acc);outline-offset:14px">' \
        + img(c, "inset:0") + "</div>" + text_block(c, 1390)

def L_side_spine(c):
    p = c["p"]
    return f"""<div style="position:absolute;left:0;top:0;width:130px;height:1920px;background:#2F402F;display:flex;flex-direction:column;align-items:center;padding-top:200px;gap:40px">
 <div class="disc" style="width:96px;height:96px"><img src="{c['logo']}"></div>
 <div style="writing-mode:vertical-rl;transform:rotate(180deg);color:#F6EBDD;font-family:var(--disp);font-size:36px;letter-spacing:.32em">JEWORA · {esc(c['cat']).upper()} · NO. {c['i']:02d}</div></div>""" \
        + img(c, "left:130px;top:330px;width:950px;height:950px") + f"""
<div style="position:absolute;left:190px;right:70px;top:1320px;color:var(--fg)">
 <div class="eb" style="font-size:19px;color:var(--acc)">{esc(p.get('eyebrow',''))}</div>
 <div class="t" style="font-size:{_title(p,62,52)}px;margin-top:10px">{esc(p['title'])}</div>
 <div style="margin-top:22px">{cta(dark_btn=True)}</div></div>"""


# key: (label, layout, theme, xfade transition, motion)  motion: zin | zout | alt | pan
REEL_STYLES = {
    "gold_frame":    ("Gold Frame",    L_gold_frame,    "dark",  "fade",        "alt"),
    "full_bleed":    ("Full Bleed",    L_full_bleed,    "dark",  "slideleft",   "zin"),
    "cream_gallery": ("Cream Gallery", L_cream_gallery, "light", "dissolve",    "zout"),
    "arch":          ("Arch Window",   L_arch,          "dark",  "circleopen",  "zin"),
    "polaroid":      ("Polaroid Drop", L_polaroid,      "dark",  "slideup",     "alt"),
    "rounded_card":  ("Rounded Card",  L_rounded_card,  "light", "smoothleft",  "zin"),
    "magazine":      ("Magazine",      L_magazine,      "light", "fadeblack",   "zout"),
    "big_number":    ("Big Number",    L_big_number,    "white", "wipeleft",    "pan"),
    "split_color":   ("Split Colour",  L_split_color,   "light", "smoothup",    "alt"),
    "minimal_white": ("Minimal White", L_minimal_white, "white", "fadewhite",   "zin"),
    "luxe_border":   ("Luxe Border",   L_luxe_border,   "dark",  "radial",      "zout"),
    "side_spine":    ("Side Spine",    L_side_spine,    "light", "slideright",  "pan"),
}
REEL_ORDER = list(REEL_STYLES)
