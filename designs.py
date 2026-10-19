"""Jewora design system: 12 distinct post designs shared by carousels (1080x1350) and Reels (1080x1920).

Rules every design follows:
- The product photo is always shown WHOLE (object-fit: contain, square box) and nothing is ever drawn on top of it.
- COMMENT "PRICE" is a big, bold button (56px+ Inter Black) on every slide/frame.
- All content sits in a 1080x1350 "stage". Carousels: stage = whole slide. Reels: stage starts at y=215 so it stays
  inside Instagram's safe zone (UI covers ~top 200px and bottom ~360px); the rest of the 1920 frame is background only.
"""
import html

esc = lambda s: html.escape(s or "")

FONTS = """
*{box-sizing:border-box;margin:0;padding:0}
.cv{position:relative;width:1080px;overflow:hidden;font-family:'Poppins',sans-serif}
.stage{position:absolute;left:0;width:1080px;height:1350px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.ph{flex:none;overflow:hidden;background:#fff}.ph img{width:100%;height:100%;object-fit:contain;display:block}
.cta{display:inline-flex;align-items:center;justify-content:center;gap:22px;font-family:'Inter',sans-serif;font-weight:900;
  font-size:58px;letter-spacing:.03em;line-height:1;padding:30px 58px;white-space:nowrap}
.cta svg{width:56px;height:56px;flex:none}
.one{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:960px;text-align:center}
"""

BUBBLE = ('<svg viewBox="0 0 24 24"><path fill="currentColor" d="M4 2.5h16A2.5 2.5 0 0 1 22.5 5v10.5A2.5 2.5 0 0 1 20 18H10l-5.2 4'
          'v-4H4A2.5 2.5 0 0 1 1.5 15.5V5A2.5 2.5 0 0 1 4 2.5z"/><circle cx="7.5" cy="10.2" r="1.4" fill="{dot}"/>'
          '<circle cx="12" cy="10.2" r="1.4" fill="{dot}"/><circle cx="16.5" cy="10.2" r="1.4" fill="{dot}"/></svg>')
CTA_TXT = "COMMENT “PRICE”"
TAGLINE = "India’s First Unified Jewellery Marketplace"   # brand line under the CTA on every slide/frame


def bubble(dot): return BUBBLE.replace("{dot}", dot)


def fit(text, maxpx, k, width=960):
    """font size so `text` fits on one line of `width` px (k = average glyph width / font size)."""
    return max(30, min(maxpx, int(width / (k * max(len(text), 1)))))


def photo(c, size, style=""):
    return f'<div class="ph" style="width:{size}px;height:{size}px;{style}"><img src="{c["img"]}"></div>'


def logo(c, size, bg="#F6EBDD", ring="#C9A46C"):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{bg};border:2px solid {ring};'
            f'display:grid;place-items:center;flex:none"><img src="{c["logo"]}" style="width:56%"></div>')


# ------------------------------------------------------------------ the 12 designs
# each: dict(label, bg (css for the whole canvas), deco(H)->html, fg, acc, cta(scale)->html, card(c)->stage html,
#            title_font, transition, motion)

def _royal_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:linear-gradient(135deg,#F3DDA8,#C9A46C 55%,#9E7740);'
            f'color:#1B261B;border-radius:14px;box-shadow:0 14px 34px rgba(0,0,0,.4)">{bubble("#C9A46C")}{CTA_TXT}</div>')

def royal_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:22px">{logo(c, 92)}
  <div style="text-align:left"><div style="font-size:22px;letter-spacing:.34em;color:#C9A46C;text-transform:uppercase">{esc(c['eb'])}</div>
  <div style="font-size:20px;letter-spacing:.3em;color:#B9C4B3;margin-top:6px">NO. {c['i']:02d} / {c['n']:02d}</div></div></div>
 {photo(c, 780, "border:2px solid #C9A46C;outline:2px solid #C9A46C;outline-offset:12px;margin:34px 0 30px")}
 <div class="one" style="font-family:'GFS Baskerville';font-variant:small-caps;color:#F6EBDD;font-size:{fit(t,60,.58)}px;margin-bottom:22px">{esc(t)}</div>
 {_royal_cta()}"""


def _maroon_cta(s=1):
    m = "radial-gradient(circle 20px at 0 50%,#0000 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 20px at 100% 50%,#0000 98%,#000) right/51% 100% no-repeat"
    return (f'<div style="filter:drop-shadow(0 12px 22px rgba(0,0,0,.45))"><div class="cta" style="font-size:{58*s:.0f}px;'
            f'padding:32px 74px;background:linear-gradient(180deg,#F6D98E,#D9A94B);color:#5E0F1E;-webkit-mask:{m};mask:{m};'
            f'outline:3px dashed rgba(94,15,30,.45);outline-offset:-14px">{bubble("#E2B866")}{CTA_TXT}</div></div>')

def maroon_card(c):
    t = c["title"]
    corner = lambda pos: f'<div style="position:absolute;{pos};width:26px;height:26px;background:#E2B866;transform:rotate(45deg)"></div>'
    return f"""<div style="display:flex;align-items:center;gap:26px;color:#E2B866">
  <div style="width:150px;height:2px;background:linear-gradient(90deg,#0000,#E2B866)"></div>
  <div style="font-family:'Lora';font-style:italic;font-size:38px">{esc(c['cat'])} Utsav</div>
  <div style="width:150px;height:2px;background:linear-gradient(90deg,#E2B866,#0000)"></div></div>
 <div style="position:relative;padding:14px;background:linear-gradient(135deg,#F6D98E,#B8862F,#F6D98E);margin:22px 0 10px">
  {photo(c, 800)}{corner("left:-13px;top:-13px")}{corner("right:-13px;top:-13px")}{corner("left:-13px;bottom:-13px")}{corner("right:-13px;bottom:-13px")}</div>
 <div class="one" style="font-family:'Lora';font-style:italic;font-weight:600;color:#F6D98E;font-size:{fit(t,60,.5)}px">{esc(t)}</div>
 <div style="font-size:20px;letter-spacing:.36em;color:#E9B8A6;margin:10px 0 26px">JEWORA · {c['i']:02d} OF {c['n']:02d}</div>
 {_maroon_cta()}"""


def _blush_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:#151515;color:#fff;padding:32px 56px">'
            f'{bubble("#151515")}{CTA_TXT}<span style="font-size:{50*s:.0f}px;margin-left:4px">→</span></div>')

def blush_card(c):
    t, cat = c["title"], c["cat"].upper()
    return f"""<div style="font-family:'Inter';font-weight:900;font-size:{fit(cat,178,.72,1000)}px;line-height:.9;letter-spacing:-.01em;
   color:transparent;-webkit-text-stroke:2.5px #C98473">{esc(cat)}</div>
 <div style="display:flex;justify-content:space-between;width:800px;font-size:21px;letter-spacing:.28em;color:#8A4F43;margin:14px 0 12px">
  <span>JEWORA</span><span>NO. {c['i']:02d}</span></div>
 {photo(c, 770, "border:16px solid #fff;box-shadow:0 24px 50px rgba(110,50,40,.25);box-sizing:content-box")}
 <div class="one" style="font-family:'Lora';font-style:italic;color:#4A2A25;font-size:{fit(t,56,.5)}px;margin:26px 0 22px">{esc(t)}</div>
 {_blush_cta()}"""


def _midnight_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:linear-gradient(135deg,#FFE7B0,#D4A95C 50%,#A57A35);color:#0C0C0E;'
            f'border-radius:6px;box-shadow:0 0 0 5px #0C0C0E,0 0 0 8px #D4A95C,0 0 60px rgba(212,169,92,.55)">{bubble("#D4A95C")}{CTA_TXT}</div>')

def midnight_card(c):
    t = c["title"]
    return f"""<div style="font-family:'GFS Baskerville';font-size:46px;letter-spacing:.6em;color:#D4A95C;margin-right:-.6em">JEWORA</div>
 <div style="font-size:19px;letter-spacing:.4em;color:#8E8574;margin-top:10px">{esc(c['eb']).upper()}</div>
 {photo(c, 840, "margin:30px 0 26px;box-shadow:0 0 70px rgba(212,169,92,.30);border:1px solid rgba(212,169,92,.6)")}
 <div class="one" style="font-family:'Lora';font-style:italic;font-weight:500;font-size:{fit(t,62,.5)}px;
   background:linear-gradient(90deg,#B98B45,#FFE7B0,#B98B45);-webkit-background-clip:text;color:transparent;padding-bottom:6px">{esc(t)}</div>
 <div style="margin-top:26px">{_midnight_cta()}</div>"""


def _temple_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:#B5543C;color:#FFF6EA;border-radius:999px;padding:32px 64px;'
            f'outline:2px dashed rgba(255,246,234,.7);outline-offset:-12px;box-shadow:0 14px 30px rgba(120,45,25,.35)">{bubble("#B5543C")}{CTA_TXT}</div>')

def temple_card(c):
    t = c["title"]
    return f"""<div style="width:930px;padding:34px 0 52px;border-radius:465px 465px 0 0;background:linear-gradient(180deg,#C9674C,#A64A33);
   display:flex;flex-direction:column;align-items:center;gap:22px;box-shadow:0 20px 40px rgba(120,45,25,.25)">
  {logo(c, 96, "#FFF6EA", "#FFF6EA")}
  <div style="font-size:21px;letter-spacing:.34em;color:#FFE3CF">{esc(c['eb']).upper()}</div>
  {photo(c, 790, "border:8px solid #FFF6EA")}</div>
 <div class="one" style="font-family:'GFS Baskerville';font-variant:small-caps;color:#6E2B1D;font-size:{fit(t,58,.58)}px;margin:26px 0 20px">{esc(t)}</div>
 {_temple_cta()}"""


def _pop_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:#FF5C93;color:#111;border:5px solid #111;border-radius:18px;'
            f'box-shadow:12px 12px 0 #111">{bubble("#FF5C93")}{CTA_TXT}</div>')

def pop_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:20px;width:860px;justify-content:space-between">
  <div style="background:#111;color:#FFE07A;font-family:'Inter';font-weight:900;font-size:34px;padding:12px 24px;transform:rotate(-3deg)">NEW DROP · {esc(c['cat']).upper()}</div>
  <div style="width:96px;height:96px;border-radius:50%;background:#fff;border:5px solid #111;display:grid;place-items:center;
    font-family:'Inter';font-weight:900;font-size:40px;color:#111">{c['i']:02d}</div></div>
 {photo(c, 800, "border:6px solid #111;box-shadow:18px 18px 0 #111;margin:30px 0 34px;box-sizing:content-box")}
 <div class="one" style="font-family:'Inter';font-weight:800;color:#111;font-size:{fit(t,54,.56)}px;margin-bottom:28px">{esc(t)}</div>
 {_pop_cta()}"""


def _glass_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:#fff;color:#5B3FA0;border-radius:999px;padding:32px 64px;'
            f'box-shadow:0 18px 40px rgba(91,63,160,.28)">{bubble("#fff")}{CTA_TXT}</div>')

def glass_card(c):
    t = c["title"]
    return f"""<div style="background:rgba(255,255,255,.42);border:2px solid rgba(255,255,255,.85);border-radius:44px;padding:30px 30px 24px;
   box-shadow:0 30px 60px rgba(91,63,160,.18);display:flex;flex-direction:column;align-items:center">
  <div style="display:flex;justify-content:space-between;align-items:center;width:800px;margin-bottom:22px">
   {logo(c, 74, "#fff", "#D9CCF5")}<div style="font-size:21px;letter-spacing:.3em;color:#6E5A9C">{esc(c['eb']).upper()}</div></div>
  {photo(c, 800, "border-radius:26px")}
  <div class="one" style="font-family:'Lora';font-weight:600;color:#3B2A5C;font-size:{fit(t,54,.52,800)}px;max-width:800px;margin-top:22px">{esc(t)}</div></div>
 <div style="margin-top:34px">{_glass_cta()}</div>"""


def _navy_cta(s=1):
    return (f'<div style="transform:skewX(-12deg);background:linear-gradient(90deg,#E3B85A,#C99A3B);box-shadow:0 14px 28px rgba(20,33,61,.35)">'
            f'<div class="cta" style="font-size:{58*s:.0f}px;transform:skewX(12deg);color:#14213D;padding:30px 70px">{bubble("#D4A94B")}{CTA_TXT}</div></div>')

def navy_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;justify-content:space-between;width:880px;color:#F4EFE6">
  <div style="display:flex;align-items:center;gap:20px">{logo(c, 84)}<div style="font-size:21px;letter-spacing:.3em">{esc(c['eb']).upper()}</div></div>
  <div style="font-family:'GFS Baskerville';font-size:84px;color:#E3B85A;line-height:1">{c['i']:02d}</div></div>
 {photo(c, 820, "border:12px solid #fff;box-shadow:0 30px 60px rgba(0,0,0,.35);margin:24px 0 28px;box-sizing:content-box")}
 <div class="one" style="font-family:'GFS Baskerville';color:#14213D;font-size:{fit(t,58,.5)}px;margin-bottom:26px">{esc(t)}</div>
 {_navy_cta()}"""


def _stamp_cta(s=1):
    d = int(330 * s)
    return (f'<div style="width:{d}px;height:{d}px;border-radius:50%;background:#F2B84B;transform:rotate(-8deg);flex:none;'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Inter;font-weight:900;color:#0F4C4C;'
            f'box-shadow:0 0 0 8px #0F4C4C,0 0 0 12px #F2B84B,0 20px 40px rgba(0,0,0,.4);text-align:center;line-height:1">'
            f'<div style="font-size:{46*s:.0f}px;letter-spacing:.06em">COMMENT</div><div style="font-size:{74*s:.0f}px;margin-top:8px">“PRICE”</div>'
            f'<div style="font-size:{19*s:.0f}px;letter-spacing:.2em;margin-top:12px;font-weight:700">FOR DETAILS</div></div>')

def stamp_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:20px;color:#F3E9D2">{logo(c, 80)}
  <div style="font-size:22px;letter-spacing:.32em">{esc(c['eb']).upper()}</div></div>
 {photo(c, 790, "border:16px solid #F3E9D2;margin:26px 0 22px;box-sizing:content-box")}
 <div style="display:flex;align-items:center;justify-content:space-between;width:900px;gap:30px">
  <div style="flex:1;min-width:0;color:#F3E9D2"><div style="font-size:22px;letter-spacing:.3em;color:#F2B84B">NO. {c['i']:02d} / {c['n']:02d}</div>
   <div style="font-family:'Lora';font-style:italic;font-size:{min(56, fit(t,56,.5,1040))}px;line-height:1.12;margin-top:10px">{esc(t)}</div></div>
  {_stamp_cta(0.95)}</div>"""


def _plaque_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:#1E1E1E;color:#F6EBDD;border-radius:4px;'
            f'box-shadow:0 14px 30px rgba(0,0,0,.3)"><span style="color:#D2AE6D;display:flex">{bubble("#1E1E1E")}</span>{CTA_TXT}</div>')

def plaque_card(c):
    t = c["title"]
    return f"""<div style="padding:34px;background:#fff;border:22px solid #1C1A17;box-shadow:0 40px 70px rgba(40,30,20,.35),inset 0 0 12px rgba(0,0,0,.15)">
  {photo(c, 740)}</div>
 <div style="margin:34px 0 28px;padding:18px 44px;background:linear-gradient(135deg,#E9D29C,#B8924E 50%,#E5C98C);border-radius:4px;
   box-shadow:0 6px 14px rgba(0,0,0,.25);text-align:center;max-width:960px">
  <div style="font-size:17px;letter-spacing:.34em;color:#4A3818">JEWORA GALLERY · NO. {c['i']:02d}</div>
  <div class="one" style="font-family:'GFS Baskerville';font-size:{fit(t,46,.5,860)}px;color:#2A1F0E;margin-top:6px;max-width:860px">{esc(t)}</div></div>
 {_plaque_cta()}"""


def _news_cta(s=1):
    return (f'<div class="cta" style="font-size:{60*s:.0f}px;background:#C8102E;color:#fff;width:{int(940*s)}px;padding:32px 0">'
            f'{bubble("#C8102E")}{CTA_TXT}<span style="font-size:{44*s:.0f}px">▶</span></div>')

def news_card(c):
    t = c["title"]
    rule = '<div style="width:940px;height:6px;border-top:3px solid #111;border-bottom:1px solid #111"></div>'
    return f"""{rule}
 <div style="font-family:'Caladea';font-weight:700;font-size:84px;color:#111;line-height:1.05;margin:6px 0 2px">The Jewora Edit</div>
 <div style="display:flex;justify-content:space-between;width:940px;font-family:'Caladea';font-size:22px;letter-spacing:.14em;color:#333">
  <span>NO. {c['i']:02d}</span><span>{esc(c['cat']).upper()} SPECIAL</span><span>FREE SHIPPING</span></div>
 {rule}
 {photo(c, 780, "border:2px solid #111;margin:24px 0 18px")}
 <div class="one" style="font-family:'Caladea';font-weight:700;color:#111;font-size:{fit(t,58,.5)}px;margin-bottom:22px">{esc(t)}</div>
 {_news_cta()}"""


def _rose_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:linear-gradient(135deg,#F2C9B8,#C98A8E 55%,#A9606C);color:#fff;'
            f'border-radius:999px;width:{int(900*s)}px;padding:34px 0;box-shadow:0 16px 34px rgba(169,96,108,.35)">{bubble("#C98A8E")}{CTA_TXT}</div>')

def rose_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:26px">
  <div style="width:120px;height:1px;background:#C98A8E"></div><img src="{c['logo']}" style="height:84px">
  <div style="width:120px;height:1px;background:#C98A8E"></div></div>
 {photo(c, 820, "border-radius:10px;margin:26px 0 24px;box-shadow:0 20px 50px rgba(169,96,108,.18)")}
 <div class="one" style="font-family:'Poppins';font-weight:300;text-transform:uppercase;letter-spacing:.16em;color:#5A3A3E;font-size:{fit(t,40,.78)}px">{esc(t)}</div>
 <div style="font-size:19px;letter-spacing:.38em;color:#B07A80;margin:10px 0 26px">{c['i']:02d} — {c['n']:02d}</div>
 {_rose_cta()}"""


# ------------------------------------------------------------------ photo treatments (v2: no more "everything in a box")
FADE = ("-webkit-mask-image:linear-gradient(90deg,#0000,#000 {e}%,#000 {f}%,#0000),linear-gradient(#0000,#000 {e}%,#000 {f}%,#0000);"
        "-webkit-mask-composite:source-in;mask-composite:intersect")

def faded(c, size, edge=5, style=""):
    """photo whose edges dissolve into the background (product stays sharp in the middle)."""
    return f'<div style="width:{size}px;height:{size}px;flex:none;{FADE.format(e=edge, f=100-edge)};{style}"><img src="{c["img"]}" style="width:100%;height:100%;object-fit:contain;display:block"></div>'

def band(c, h, style="", vfade=False):
    """edge-to-edge band: the whole square photo sits sharp in the middle, the sides are a blurred copy of the same photo."""
    vm = ";-webkit-mask-image:linear-gradient(#0000,#000 7%,#000 93%,#0000)" if vfade else ""
    side = "-webkit-mask-image:linear-gradient(90deg,#0000,#000 3%,#000 97%,#0000)"
    return (f'<div style="position:relative;width:1080px;height:{h}px;overflow:hidden;flex:none{vm};{style}">'
            f'<img src="{c["img"]}" style="position:absolute;left:-60px;top:-60px;width:1200px;height:{h+120}px;object-fit:cover;filter:blur(34px) saturate(1.05) brightness(.92)">'
            f'<img src="{c["img"]}" style="position:relative;display:block;width:{h}px;height:{h}px;margin:0 auto;object-fit:contain;{side}"></div>')


def royal_card(c):
    t = c["title"]
    return f"""{band(c, 960, "border-top:3px solid #C9A46C;border-bottom:3px solid #C9A46C")}
 <div style="display:flex;align-items:center;gap:18px;margin:24px 0 6px">{logo(c, 58)}
  <div style="font-size:21px;letter-spacing:.32em;color:#C9A46C">{esc(c['eb']).upper()} · {c['i']:02d}/{c['n']:02d}</div></div>
 <div class="one" style="font-family:'GFS Baskerville';font-variant:small-caps;color:#F6EBDD;font-size:{fit(t,58,.58)}px;margin-bottom:18px">{esc(t)}</div>
 {_royal_cta()}"""


def maroon_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:26px;color:#E2B866">
  <div style="width:150px;height:2px;background:linear-gradient(90deg,#0000,#E2B866)"></div>
  <div style="font-family:'Lora';font-style:italic;font-size:38px">{esc(c['cat'])} Utsav</div>
  <div style="width:150px;height:2px;background:linear-gradient(90deg,#E2B866,#0000)"></div></div>
 {photo(c, 840, "border-radius:34px;margin:30px 0 26px;box-shadow:0 0 0 5px #E2B866,0 0 0 14px rgba(226,184,102,.25),0 0 70px rgba(246,217,142,.35)")}
 <div class="one" style="font-family:'Lora';font-style:italic;font-weight:600;color:#F6D98E;font-size:{fit(t,60,.5)}px">{esc(t)}</div>
 <div style="font-size:20px;letter-spacing:.36em;color:#E9B8A6;margin:8px 0 24px">JEWORA · {c['i']:02d} OF {c['n']:02d}</div>
 {_maroon_cta()}"""


def blush_card(c):
    t, cat = c["title"], c["cat"].upper()
    rot = -3 if c["i"] % 2 else 3
    return f"""<div style="font-family:'Inter';font-weight:900;font-size:{fit(cat,178,.72,1000)}px;line-height:.9;letter-spacing:-.01em;
   color:transparent;-webkit-text-stroke:2.5px #C98473;position:relative;z-index:0">{esc(cat)}</div>
 <div style="position:relative;margin:-10px 0 40px;z-index:1">
  <div style="position:absolute;inset:0;background:#E9B3A5;transform:rotate({-rot*2}deg) translate({rot*-10}px,14px)"></div>
  {photo(c, 760, f"position:relative;transform:rotate({rot}deg);box-shadow:0 28px 50px rgba(110,50,40,.28)")}</div>
 <div class="one" style="font-family:'Lora';font-style:italic;color:#4A2A25;font-size:{fit(t,56,.5)}px;margin-bottom:22px">{esc(t)}</div>
 {_blush_cta()}"""


def midnight_card(c):
    t = c["title"]
    return f"""<div style="font-family:'GFS Baskerville';font-size:44px;letter-spacing:.6em;color:#D4A95C;margin-right:-.6em">JEWORA</div>
 <div style="font-size:19px;letter-spacing:.4em;color:#8E8574;margin:10px 0 6px">{esc(c['eb']).upper()}</div>
 {band(c, 940, vfade=True)}
 <div class="one" style="font-family:'Lora';font-style:italic;font-weight:500;font-size:{fit(t,62,.5)}px;
   background:linear-gradient(90deg,#B98B45,#FFE7B0,#B98B45);-webkit-background-clip:text;color:transparent;padding-bottom:6px">{esc(t)}</div>
 <div style="margin-top:20px">{_midnight_cta()}</div>"""


def temple_card(c):
    t = c["title"]
    return f"""<div style="width:960px;padding:30px 0 0;border-radius:480px 480px 0 0;background:linear-gradient(180deg,#C9674C,#A64A33);
   display:flex;flex-direction:column;align-items:center;gap:16px;overflow:hidden">
  {logo(c, 90, "#FFF6EA", "#FFF6EA")}
  <div style="font-size:21px;letter-spacing:.34em;color:#FFE3CF">{esc(c['eb']).upper()}</div>
  {photo(c, 860, "margin-top:4px")}</div>
 <div class="one" style="font-family:'GFS Baskerville';font-variant:small-caps;color:#6E2B1D;font-size:{fit(t,58,.58)}px;margin:24px 0 20px">{esc(t)}</div>
 {_temple_cta()}"""


def pop_card(c):
    t = c["title"]
    rot = 3 if c["i"] % 2 else -3
    return f"""<div style="display:flex;align-items:center;width:900px;justify-content:space-between">
  <div style="background:#111;color:#FFE07A;font-family:'Inter';font-weight:900;font-size:34px;padding:12px 24px;transform:rotate(-3deg)">NEW DROP · {esc(c['cat']).upper()}</div>
  <div style="width:96px;height:96px;border-radius:50%;background:#fff;border:5px solid #111;display:grid;place-items:center;
    font-family:'Inter';font-weight:900;font-size:40px;color:#111">{c['i']:02d}</div></div>
 <div style="position:relative;margin:26px 0 34px">
  <div style="position:absolute;left:-70px;top:-50px;width:380px;height:380px;border-radius:50%;background:#FF5C93"></div>
  <div style="position:absolute;right:-60px;bottom:-40px;width:300px;height:300px;border-radius:50%;background:#6FD6C3"></div>
  {photo(c, 800, f"position:relative;border-radius:36px;transform:rotate({rot}deg);box-shadow:16px 16px 0 #111")}</div>
 <div class="one" style="font-family:'Inter';font-weight:800;color:#111;font-size:{fit(t,54,.56)}px;margin-bottom:28px">{esc(t)}</div>
 {_pop_cta()}"""


def glass_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:18px;margin-bottom:26px">{logo(c, 70, "#fff", "#D9CCF5")}
  <div style="font-size:21px;letter-spacing:.3em;color:#6E5A9C">{esc(c['eb']).upper()}</div></div>
 {photo(c, 820, "border-radius:48px;box-shadow:0 40px 80px rgba(91,63,160,.25)")}
 <div style="margin:26px 0 28px;position:relative;background:rgba(255,255,255,.6);border:2px solid #fff;border-radius:999px;padding:18px 44px;
   box-shadow:0 14px 30px rgba(91,63,160,.15)"><div class="one" style="font-family:'Lora';font-weight:600;color:#3B2A5C;font-size:{fit(t,48,.52,780)}px;max-width:780px">{esc(t)}</div></div>
 {_glass_cta()}"""


def navy_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;justify-content:space-between;width:900px;color:#F4EFE6;margin-bottom:22px">
  <div style="display:flex;align-items:center;gap:20px">{logo(c, 80)}<div style="font-size:21px;letter-spacing:.3em">{esc(c['eb']).upper()}</div></div>
  <div style="font-family:'GFS Baskerville';font-size:84px;color:#E3B85A;line-height:1">{c['i']:02d}</div></div>
 {band(c, 900, "box-shadow:0 30px 60px rgba(0,0,0,.3)")}
 <div class="one" style="font-family:'GFS Baskerville';color:#14213D;font-size:{fit(t,58,.5)}px;margin:26px 0 22px">{esc(t)}</div>
 {_navy_cta()}"""


def stamp_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:20px;color:#F3E9D2">{logo(c, 80)}
  <div style="font-size:22px;letter-spacing:.32em">{esc(c['eb']).upper()}</div></div>
 {photo(c, 800, f"margin:26px 0 30px;transform:rotate({-2 if c['i'] % 2 else 2}deg);box-shadow:0 30px 60px rgba(0,0,0,.45)")}
 <div style="display:flex;align-items:center;justify-content:space-between;width:900px;gap:30px">
  <div style="flex:1;min-width:0;color:#F3E9D2"><div style="font-size:22px;letter-spacing:.3em;color:#F2B84B">NO. {c['i']:02d} / {c['n']:02d}</div>
   <div style="font-family:'Lora';font-style:italic;font-size:{min(56, fit(t,56,.5,1040))}px;line-height:1.12;margin-top:10px">{esc(t)}</div></div>
  {_stamp_cta(0.92)}</div>"""


def news_card(c):
    t = c["title"]
    rule = '<div style="width:940px;height:6px;border-top:3px solid #111;border-bottom:1px solid #111"></div>'
    return f"""{rule}
 <div style="font-family:'Caladea';font-weight:700;font-size:84px;color:#111;line-height:1.05;margin:6px 0 2px">The Jewora Edit</div>
 <div style="display:flex;justify-content:space-between;width:940px;font-family:'Caladea';font-size:22px;letter-spacing:.14em;color:#333">
  <span>NO. {c['i']:02d}</span><span>{esc(c['cat']).upper()} SPECIAL</span><span>FREE SHIPPING</span></div>
 {rule}
 {photo(c, 820, "margin:24px 0 16px;filter:contrast(1.03)")}
 <div class="one" style="font-family:'Caladea';font-weight:700;color:#111;font-size:{fit(t,58,.5)}px;margin-bottom:20px">{esc(t)}</div>
 {_news_cta()}"""


def rose_card(c):
    t = c["title"]
    return f"""<div style="display:flex;align-items:center;gap:26px">
  <div style="width:120px;height:1px;background:#A9606C"></div><img src="{c['logo']}" style="height:84px">
  <div style="width:120px;height:1px;background:#A9606C"></div></div>
 {photo(c, 860, "border-radius:18px;margin:26px 0 24px;box-shadow:0 30px 70px rgba(90,40,50,.28)")}
 <div class="one" style="font-family:'Poppins';font-weight:400;text-transform:uppercase;letter-spacing:.16em;color:#4A2C30;font-size:{fit(t,40,.78)}px">{esc(t)}</div>
 <div style="font-size:19px;letter-spacing:.38em;color:#8A5A60;margin:10px 0 24px">{c['i']:02d} — {c['n']:02d}</div>
 {_rose_cta()}"""


LEAF = ('<svg width="{w}" height="{h}" viewBox="0 0 60 200" style="{st}"><path d="M30 200 C30 140 30 80 30 0" stroke="{c}" stroke-width="2" fill="none"/>'
        + "".join(f'<path d="M30 {y} C{10 if k%2 else 50} {y-14} {4 if k%2 else 56} {y-34} {30} {y-40}" stroke="{{c}}" stroke-width="2" fill="{{f}}"/>'
                  for k, y in enumerate(range(190, 30, -26))) + '</svg>')

def _sage_cta(s=1):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:#FFF8EC;color:#2F4A3A;border-radius:999px;padding:32px 66px;'
            f'box-shadow:0 0 0 4px #2F4A3A,0 18px 36px rgba(30,50,35,.35)">{bubble("#FFF8EC")}{CTA_TXT}</div>')

def sage_card(c):
    t = c["title"]
    leaf = lambda st: LEAF.format(w=90, h=300, st=st, c="#FFF8EC", f="rgba(255,248,236,.18)").replace("{c}", "#FFF8EC").replace("{f}", "rgba(255,248,236,.18)")
    return f"""<div style="display:flex;align-items:center;gap:18px;color:#FFF8EC">{logo(c, 72, "#FFF8EC", "#FFF8EC")}
  <div style="font-size:21px;letter-spacing:.32em">{esc(c['eb']).upper()}</div></div>
 <div style="position:relative;margin:30px 0 28px">
  <div style="position:absolute;left:50%;top:-22px;width:860px;height:860px;margin-left:-430px;border-radius:50%;background:radial-gradient(circle,#F6E2B6,#E7BE78)"></div>
  {photo(c, 780, "position:relative;border-radius:30px;box-shadow:0 34px 60px rgba(30,50,35,.35)")}</div>
 <div class="one" style="font-family:'Lora';font-style:italic;font-weight:600;color:#FFF8EC;margin-top:30px;font-size:{fit(t,58,.5)}px;margin-bottom:24px">{esc(t)}</div>
 {_sage_cta()}"""


D = {
    "royal_emerald": dict(label="Royal Emerald", card=royal_card, cta=_royal_cta, fg="#F6EBDD", acc="#C9A46C", tf="'GFS Baskerville'",
        bg="radial-gradient(ellipse 90% 60% at 50% 42%,#3D5A3C,#24331F 62%,#17211A)",
        deco=lambda H: '',
        transition="fade", motion="alt"),
    "maroon_festive": dict(label="Maroon Festive", card=maroon_card, cta=_maroon_cta, fg="#F6D98E", acc="#E2B866", tf="'Lora';font-style:italic",
        bg="radial-gradient(rgba(232,190,110,.16) 2px,transparent 2.6px) 0 0/36px 36px,radial-gradient(ellipse at 50% 40%,#7A1527,#4A0B17)",
        deco=lambda H: '', transition="circleopen", motion="zin"),
    "blush_editorial": dict(label="Blush Editorial", card=blush_card, cta=_blush_cta, fg="#4A2A25", acc="#C98473", tf="'Lora';font-style:italic",
        bg="linear-gradient(180deg,#F8E2DA,#F1CFC4)", deco=lambda H: '', transition="slideleft", motion="zout"),
    "midnight_gold": dict(label="Midnight Gold", card=midnight_card, cta=_midnight_cta, fg="#F3E2BE", acc="#D4A95C", tf="'Lora';font-style:italic",
        bg="radial-gradient(ellipse 70% 40% at 50% 30%,rgba(212,169,92,.22),transparent 70%),#0C0C0E",
        deco=lambda H: '', transition="fadeblack", motion="zin"),
    "sage_botanical": dict(label="Sage Botanical", card=sage_card, cta=_sage_cta, fg="#FFF8EC", acc="#F3D9A4", tf="'Lora';font-style:italic",
        bg="radial-gradient(ellipse at 50% 30%,#9DB09A,#6F8A73 60%,#55705B)", deco=lambda H: '', transition="dissolve", motion="zout"),
    "pop_bold": dict(label="Pop Bold", card=pop_card, cta=_pop_cta, fg="#111", acc="#FF5C93", tf="'Inter';font-weight:900",
        bg="linear-gradient(#0000 calc(100% - 2px),rgba(0,0,0,.07) 0) 0 0/60px 60px,linear-gradient(90deg,#0000 calc(100% - 2px),rgba(0,0,0,.07) 0) 0 0/60px 60px,#FFE07A",
        deco=lambda H: '', transition="slideup", motion="alt"),
    "lavender_glass": dict(label="Lavender Glass", card=glass_card, cta=_glass_cta, fg="#3B2A5C", acc="#7E62C4", tf="'Lora'",
        bg="linear-gradient(160deg,#E7DDFF,#FBE2EE 55%,#FFEBD8)",
        deco=lambda H: f'<div style="position:absolute;left:-160px;top:{int(H*.12)}px;width:620px;height:620px;border-radius:50%;background:#CDB8FF;filter:blur(90px);opacity:.8"></div>'
                       f'<div style="position:absolute;right:-180px;top:{int(H*.55)}px;width:640px;height:640px;border-radius:50%;background:#FFC0D5;filter:blur(90px);opacity:.8"></div>',
        transition="smoothleft", motion="zin"),
    "navy_diagonal": dict(label="Navy Diagonal", card=navy_card, cta=_navy_cta, fg="#14213D", acc="#E3B85A", tf="'GFS Baskerville'",
        bg="linear-gradient(168deg,#14213D 0 50%,#F4EFE6 50% 100%)", outro_fg="#F4EFE6", deco=lambda H: '', transition="wipeleft", motion="pan"),
    "teal_stamp": dict(label="Teal Stamp", card=stamp_card, cta=_stamp_cta, fg="#F3E9D2", acc="#F2B84B", tf="'Lora';font-style:italic",
        bg="repeating-linear-gradient(135deg,rgba(255,255,255,.035) 0 18px,transparent 18px 36px),radial-gradient(ellipse at 50% 40%,#15605F,#0B3B3B)",
        deco=lambda H: '', transition="radial", motion="zout"),
    "gallery_plaque": dict(label="Gallery Plaque", card=plaque_card, cta=_plaque_cta, fg="#2A1F0E", acc="#B8924E", tf="'GFS Baskerville'",
        bg="radial-gradient(ellipse 60% 35% at 50% 18%,rgba(255,255,255,.75),transparent 70%),linear-gradient(180deg,#EEE8DF,#D8CFC1)",
        deco=lambda H: '', transition="fade", motion="zin"),
    "newspaper": dict(label="Newspaper Bold", card=news_card, cta=_news_cta, fg="#111", acc="#C8102E", tf="'Caladea';font-weight:700",
        bg="#F4EDDF", deco=lambda H: '', transition="slideright", motion="pan"),
    "rose_minimal": dict(label="Rose Minimal", card=rose_card, cta=_rose_cta, fg="#5A3A3E", acc="#C98A8E", tf="'Poppins';font-weight:300",
        bg="#FFFFFF", photo_bg="rgba(255,248,246,.72)", deco=lambda H: '',
        transition="fadewhite", motion="zin"),
}
ORDER = list(D)


def canvas(key, H, stage_html, top, c=None):
    d = D[key]
    foot = ""
    pb = ""
    if c is not None and d.get("photo_bg"):   # soft, blurred copy of the product photo as the whole background
        pb = (f'<img src="{c["img"]}" style="position:absolute;left:-120px;top:-120px;width:1320px;height:{H+240}px;object-fit:cover;filter:blur(46px)">'
              f'<div style="position:absolute;inset:0;background:{d["photo_bg"]}"></div>')
    if H > 1350:   # Reel: low-priority brand line in the area Instagram's caption UI may cover
        foot = (f'<div style="position:absolute;left:0;right:0;top:1640px;text-align:center;color:{d["acc"]}">'
                f'<div style="font-size:26px;letter-spacing:.38em">FREE SHIPPING ACROSS INDIA</div>'
                f'<div style="font-size:24px;letter-spacing:.2em;margin-top:14px;color:{d["fg"]};opacity:.7">@jewora_official</div></div>')
    tag = (f'<div style="flex:none;margin-top:22px;font-family:\'Poppins\';font-weight:600;font-size:22px;letter-spacing:.2em;'
           f'text-transform:uppercase;white-space:nowrap;color:{d["fg"]};opacity:.9">{TAGLINE}</div>')
    return (f'<div class="cv" style="height:{H}px;background:{d["bg"]};color:{d["fg"]}">{pb}{d["deco"](H)}'
            f'<div class="stage" style="top:{top}px">{stage_html}{tag}</div>{foot}</div>')


def page(body, H):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}body{{width:1080px;height:{H}px;overflow:hidden}}</style>'
            f'</head><body>{body}</body></html>')


def slide(key, c, H=1350):
    """one product slide. Reels (H=1920) put the stage at y=215 (Instagram safe zone)."""
    return canvas(key, H, D[key]["card"](c), 0 if H == 1350 else 215, c)


def intro(key, cs, H=1920):
    d = D[key]; c = cs[0]
    thumbs = "".join(f'<div class="ph" style="width:176px;height:176px;border:4px solid {d["acc"]}"><img src="{x["img"]}"></div>' for x in cs)
    st = f"""{logo(c, 190, "#F6EBDD", d['acc'])}
 <div style="font-size:26px;letter-spacing:.4em;color:{d['acc']};margin-top:40px">JEWORA PRESENTS</div>
 <div style="font-family:{d['tf']};font-size:118px;line-height:1.02;text-align:center;margin-top:18px">The {esc(c['cat'])}<br>Edit</div>
 <div style="display:flex;gap:16px;margin-top:56px">{thumbs}</div>
 <div style="font-size:26px;letter-spacing:.3em;margin-top:40px;opacity:.85">{len(cs)} HANDPICKED PIECES</div>"""
    return canvas(key, H, st, 215, c)


def outro(key, c, H=1920):
    d = D[key]
    st = f"""{logo(c, 170, "#F6EBDD", d['acc'])}
 <div style="font-family:{d['tf']};font-size:76px;margin:44px 40px 50px;text-align:center;line-height:1.1;color:{d.get('outro_fg', d['fg'])}">Which one is your favourite?</div>
 {d['cta'](1.05)}
 <div style="font-size:30px;letter-spacing:.06em;margin-top:46px;text-align:center;line-height:1.5;opacity:.9">Comment below and we'll DM you<br>the price + details instantly</div>"""
    return canvas(key, H, st, 215)
