"""10 Reel formats (v3) — each one has its OWN story structure, hook line, colours, timing and transitions,
so consecutive Reels never look alike (no more "The Necklace Edit" every time).

Rules kept from designs.py:
- product photo always shown WHOLE (object-fit: contain) and nothing is drawn on top of it
- big bold COMMENT "PRICE" button on every frame + TAGLINE under it
- all content inside Instagram's safe zone: y 215 .. 1565 of the 1080x1920 frame

build(key, dcs, n) -> (pages_html, durations, transition, motion, label)
  dcs = list of product dicts (title, eb, cat, i, n, img, logo);  n = reel number (rotates the hook lines)
"""
import re
from designs import FONTS, TAGLINE, CTA_TXT, bubble, fit, photo, logo, esc

H = 1920
TOP = 215          # safe stage starts here
STAGE_H = 1350


# ------------------------------------------------------------------ helpers
def plural(cat):
    c = cat.strip()
    if c.lower().endswith(("s", "set")) and not c.lower().endswith("set"):
        return c
    if c.lower().endswith("set"):
        return c + "s"
    return c + "s"


def theme_word(eb):
    """'The Kundan Edit · Necklace Set' -> 'Kundan'  (Signature -> '')."""
    m = re.match(r"The (.+?) Edit", eb or "")
    w = m.group(1) if m else ""
    return "" if w == "Signature" else w


def label(c):
    """short eyebrow without the word 'Edit': 'KUNDAN · NECKLACE SET'."""
    t = theme_word(c["eb"])
    return (f"{t} · {c['cat']}" if t else c["cat"]).upper()


def pick(options, n):
    return options[n % len(options)]


def page(body):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}body{{width:1080px;height:{H}px;overflow:hidden}}'
            f'</style></head><body>{body}</body></html>')


def frame(bg, fg, stage, foot_col, extra="", tag_col=None):
    tag = (f'<div style="flex:none;margin-top:22px;font-family:\'Poppins\';font-weight:600;font-size:22px;letter-spacing:.2em;'
           f'text-transform:uppercase;white-space:nowrap;color:{tag_col or fg};opacity:.9">{TAGLINE}</div>')
    foot = (f'<div style="position:absolute;left:0;right:0;top:1640px;text-align:center;color:{foot_col}">'
            f'<div style="font-size:26px;letter-spacing:.38em">FREE SHIPPING · COD · 7-DAY RETURNS</div>'
            f'<div style="font-size:24px;letter-spacing:.2em;margin-top:14px;opacity:.75">@jewora_official</div></div>')
    return page(f'<div class="cv" style="height:{H}px;background:{bg};color:{fg}">{extra}'
                f'<div class="stage" style="top:{TOP}px;height:{STAGE_H}px">{stage}{tag}</div>{foot}</div>')


def cta(bg, fg, dot, s=1.0, style=""):
    return (f'<div class="cta" style="font-size:{58*s:.0f}px;background:{bg};color:{fg};{style}">'
            f'{bubble(dot)}{CTA_TXT}</div>')


def title_line(t, font, col, maxpx=56, k=.52, width=960, style=""):
    return f'<div class="one" style="font-family:{font};color:{col};font-size:{fit(t, maxpx, k, width)}px;max-width:{width}px;{style}">{esc(t)}</div>'


def thumbs(cs, size, border):
    return "".join(f'<div class="ph" style="width:{size}px;height:{size}px;border:{border}"><img src="{x["img"]}"></div>' for x in cs)


# ================================================================== 1. COUNTDOWN — "Top 5", numbers 05 -> 01
def countdown(cs, n):
    bg = "radial-gradient(ellipse 80% 45% at 50% 40%,#2A2A2A,#0E0E0E 70%)"
    gold = "#F2C14E"
    C = lambda s=1: cta(f"linear-gradient(135deg,#FFE08A,{gold})", "#111", gold, s, "border-radius:12px")
    cat = plural(cs[0]["cat"])
    hook = pick([f"{cat} you need<br>this season",
                 f"{cat} you'll wear<br>on repeat",
                 f"{cat} our team<br>is loving right now"], n)
    pages = [frame(bg, "#fff", f"""
 <div style="font-family:Inter;font-weight:900;font-size:300px;line-height:.85;color:{gold}">TOP 5</div>
 <div style="font-family:Inter;font-weight:800;font-size:72px;line-height:1.08;text-align:center;margin:30px 40px 46px">{hook}</div>
 <div style="display:flex;gap:14px">{thumbs(cs, 170, f'3px solid {gold}')}</div>
 <div style="margin-top:50px">{C(.9)}</div>""", gold)]
    for k, c in enumerate(cs):
        rank = len(cs) - k
        pages.append(frame(bg, "#fff", f"""
 <div style="display:flex;align-items:center;gap:26px;width:980px">
  <div style="font-family:Inter;font-weight:900;font-size:120px;line-height:.8;color:{gold}">#{rank}</div>
  <div style="flex:1;min-width:0"><div style="font-size:22px;letter-spacing:.32em;color:#BDBDBD">{label(c)}</div>
   <div style="font-family:Inter;font-weight:800;font-size:{fit(c['title'],46,.56,780)}px;line-height:1.1;margin-top:6px">{esc(c['title'])}</div></div></div>
 {photo(c, 980, f"margin:22px 0 24px;border-radius:24px;box-shadow:0 0 0 4px {gold},0 0 80px rgba(242,193,78,.35)")}
 {C()}""", gold))
    pages.append(frame(bg, "#fff", f"""
 {logo(cs[0], 170, "#fff", gold)}
 <div style="font-family:Inter;font-weight:900;font-size:86px;line-height:1.05;text-align:center;margin:44px 40px">Which number<br>is your pick? 👇</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5;opacity:.85">Comment the number + PRICE<br>and we'll DM you instantly</div>""", gold))
    durs = [2.2] + [2.6] * len(cs) + [2.6]
    return pages, durs, "slideup", "zin", "Top 5 Countdown"


# ================================================================== 2. THIS OR THAT — two pieces side by side
def this_or_that(cs, n):
    bg = "linear-gradient(180deg,#FFF1E6,#FFD9C7)"
    ink, red = "#2B1B17", "#E4572E"
    C = lambda s=1: cta(ink, "#fff", ink, s, "border-radius:999px;padding:30px 62px")
    hook = pick(["This or That?", "Pick ONE 👀", "Team A or Team B?"], n)
    cat = plural(cs[0]["cat"])
    pages = [frame(bg, ink, f"""
 <div style="font-family:Inter;font-weight:900;font-size:150px;line-height:.95;text-align:center;color:{red}">{hook}</div>
 <div style="font-family:Lora;font-style:italic;font-size:60px;margin:24px 0 50px">{cat} edition</div>
 <div style="display:flex;gap:12px;align-items:center">
  {photo(cs[0], 450, "border-radius:28px;border:6px solid #fff")}
  <div style="width:90px;height:90px;border-radius:50%;background:{red};color:#fff;display:grid;place-items:center;font-family:Inter;font-weight:900;font-size:38px;flex:none">VS</div>
  {photo(cs[1], 450, "border-radius:28px;border:6px solid #fff")}</div>
 <div style="margin-top:56px">{C(.9)}</div>""", ink)]

    def card(c, tagtxt):
        return f"""<div style="display:flex;flex-direction:column;align-items:center;width:520px">
  <div style="font-family:Inter;font-weight:900;font-size:64px;color:{red};margin-bottom:14px">{tagtxt}</div>
  {photo(c, 520, "border-radius:30px;border:7px solid #fff;box-shadow:0 20px 40px rgba(120,50,30,.22)")}
  <div style="font-family:Poppins;font-weight:600;font-size:30px;line-height:1.2;text-align:center;margin-top:20px;height:74px;overflow:hidden">{esc(c['title'])}</div></div>"""
    pairs = [(cs[0], cs[1]), (cs[2], cs[3])]
    for a, b in pairs:
        pages.append(frame(bg, ink, f"""
 <div style="font-size:24px;letter-spacing:.34em;margin-bottom:30px">{label(a)}</div>
 <div style="display:flex;gap:16px;align-items:flex-start">{card(a, "A")}{card(b, "B")}</div>
 <div style="font-family:Lora;font-style:italic;font-size:46px;margin:34px 0 30px">Comment A or B 👇</div>
 {C()}""", ink))
    last = cs[4]
    pages.append(frame(bg, ink, f"""
 <div style="background:{red};color:#fff;font-family:Inter;font-weight:900;font-size:40px;padding:14px 34px;border-radius:999px;transform:rotate(-3deg)">BONUS PICK ✨</div>
 {photo(last, 980, "margin:24px 0 20px;border-radius:34px;border:8px solid #fff;box-shadow:0 26px 50px rgba(120,50,30,.25)")}
 {title_line(last['title'], "Poppins;font-weight:600", ink, 52, .55)}
 <div style="margin-top:28px">{C()}</div>""", ink))
    pages.append(frame(bg, ink, f"""
 {logo(cs[0], 160, "#fff", red)}
 <div style="font-family:Inter;font-weight:900;font-size:92px;line-height:1.02;text-align:center;margin:40px 40px 50px">Couldn't pick?<br><span style="color:{red}">Get both 😉</span></div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5">Comment PRICE and we'll DM you<br>price + details instantly</div>""", ink))
    durs = [2.4, 3.4, 3.4, 2.8, 2.6]
    return pages, durs, "wipeleft", "zin", "This or That"


# ================================================================== 3. FILM STRIP — cinema / photo-roll look
def film_strip(cs, n):
    bg = "#1A1714"
    amber = "#FF9F43"
    holes = lambda: "".join('<div style="width:28px;height:22px;border-radius:6px;background:#1A1714"></div>' for _ in range(13))
    rail = lambda side: (f'<div style="position:absolute;{side}:0;top:0;width:52px;height:{H}px;background:#2B2621;display:flex;'
                         f'flex-direction:column;align-items:center;justify-content:space-around;padding:30px 0">{holes()}</div>')
    extra = rail("left") + rail("right")
    C = lambda s=1: cta(amber, "#1A1714", amber, s, "border-radius:8px")
    hook = pick(["Now showing:", "Shot on Jewora 🎞", "Scene by scene:"], n)
    cat = plural(cs[0]["cat"])
    pages = [frame(bg, "#F7EBDD", f"""
 <div style="font-family:Caladea;font-size:40px;letter-spacing:.5em;color:{amber}">▶ JEWORA FILMS</div>
 <div style="font-family:Caladea;font-weight:700;font-size:70px;margin-top:40px">{hook}</div>
 <div style="font-family:Lora;font-style:italic;font-size:120px;line-height:1;margin:10px 0 50px;text-align:center">{cat}</div>
 <div style="display:flex;gap:12px">{thumbs(cs, 150, '3px solid #F7EBDD')}</div>
 <div style="margin-top:56px">{C(.9)}</div>""", amber, extra)]
    for c in cs:
        pages.append(frame(bg, "#F7EBDD", f"""
 <div style="display:flex;justify-content:space-between;width:940px;font-family:Caladea;font-size:28px;letter-spacing:.3em;color:{amber}">
  <span>SCENE {c['i']:02d}</span><span>TAKE 1</span><span>{c['i']:02d}/{c['n']:02d}</span></div>
 {photo(c, 940, "margin:18px 0 20px;border:8px solid #F7EBDD")}
 <div style="font-size:22px;letter-spacing:.34em;color:#B9A996">{label(c)}</div>
 {title_line(c['title'], "Caladea;font-weight:700", "#F7EBDD", 58, .5, 820, "margin:10px 0 26px")}
 {C()}""", amber, extra))
    pages.append(frame(bg, "#F7EBDD", f"""
 <div style="font-family:Caladea;font-size:40px;letter-spacing:.5em;color:{amber}">THE END?</div>
 <div style="font-family:Lora;font-style:italic;font-size:84px;line-height:1.1;text-align:center;margin:40px 40px 50px">Your favourite scene<br>can be yours</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5;opacity:.85">Comment PRICE and we'll DM you<br>price + details instantly</div>""", amber, extra))
    durs = [2.2] + [2.7] * len(cs) + [2.6]
    return pages, durs, "slideleft", "pan", "Film Strip"


# ================================================================== 4. PROGRESS ROW — big photo + all 5 thumbnails, current one lit
def progress_row(cs, n):
    bg = "linear-gradient(180deg,#E6F4EF,#CFE9DF)"
    ink, mint = "#16423C", "#16423C"
    C = lambda s=1: cta(ink, "#fff", ink, s, "border-radius:20px")
    hook = pick(["Swipe through all 5", "5 looks, 1 vibe", "Which one is you?"], n)
    cat = plural(cs[0]["cat"])

    def row(active, sz=150):
        out = []
        for x in cs:
            on = x["i"] == active
            st = (f"border:5px solid {ink};transform:translateY(-10px)" if on else "border:3px solid #fff;opacity:.55")
            out.append(f'<div class="ph" style="width:{sz}px;height:{sz}px;border-radius:{sz//8}px;{st}"><img src="{x["img"]}"></div>')
        return f'<div style="display:flex;gap:16px;align-items:flex-end;height:{sz+20}px">{"".join(out)}</div>'
    pages = [frame(bg, ink, f"""
 {logo(cs[0], 150, "#fff", ink)}
 <div style="font-family:Poppins;font-weight:600;font-size:96px;line-height:1.05;text-align:center;margin:40px 40px 20px">{hook}</div>
 <div style="font-family:Lora;font-style:italic;font-size:54px;margin-bottom:46px">handpicked {cat.lower()}</div>
 {row(0)}
 <div style="margin-top:50px">{C(.9)}</div>""", ink)]
    for c in cs:
        pages.append(frame(bg, ink, f"""
 {row(c['i'], 96)}
 {photo(c, 930, "margin:16px 0 18px;border-radius:40px;box-shadow:0 30px 60px rgba(22,66,60,.22)")}
 {title_line(c['title'], "Poppins;font-weight:600", ink, 48, .55, 960, "margin-bottom:18px")}
 {C()}""", ink))
    pages.append(frame(bg, ink, f"""
 {row(0)}
 <div style="font-family:Poppins;font-weight:600;font-size:84px;line-height:1.08;text-align:center;margin:50px 40px">Tell us your<br>favourite 💚</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5">Comment PRICE and we'll DM you<br>price + details instantly</div>""", ink))
    durs = [2.2] + [2.6] * len(cs) + [2.6]
    return pages, durs, "smoothleft", "zout", "Progress Row"


# ================================================================== 5. OCCASION GUIDE — every piece gets a moment
OCCASIONS = [("Wedding Guest", "with a silk saree or lehenga"), ("Festive Nights", "with your brightest kurta set"),
             ("Office Ready", "with a crisp kurti or blazer"), ("Date Night", "with a little black dress"),
             ("Everyday Glam", "with anything, honestly"), ("Haldi & Mehendi", "with yellows and pastels"),
             ("Sangeet Party", "with a sparkly lehenga"), ("Puja at Home", "with a simple cotton saree")]

def occasion(cs, n):
    bg = "radial-gradient(ellipse at 50% 30%,#5B2A4E,#3A1532 70%)"
    champ = "#F1D3A6"
    C = lambda s=1: cta(f"linear-gradient(135deg,#FBE7C6,{champ},#D9AE78)", "#3A1532", champ, s, "border-radius:6px")
    cat = cs[0]["cat"]
    hook = pick([f"{cat} for<br>every occasion", f"Where will you<br>wear yours?", f"Your {cat.lower()}<br>occasion guide"], n)
    occ = [OCCASIONS[(n * 3 + k) % len(OCCASIONS)] for k in range(len(cs))]
    pages = [frame(bg, "#FFF5E8", f"""
 <div style="font-size:26px;letter-spacing:.5em;color:{champ}">JEWORA · STYLE GUIDE</div>
 <div style="font-family:Lora;font-style:italic;font-size:108px;line-height:1.05;text-align:center;margin:40px 40px 50px">{hook}</div>
 <div style="display:flex;flex-direction:column;gap:14px;font-size:34px;letter-spacing:.12em;text-align:center">
  {''.join(f'<div>— {o[0]} —</div>' for o in occ)}</div>
 <div style="margin-top:56px">{C(.9)}</div>""", champ)]
    for c, (o, pair) in zip(cs, occ):
        pages.append(frame(bg, "#FFF5E8", f"""
 <div style="font-size:24px;letter-spacing:.42em;color:{champ}">PERFECT FOR</div>
 <div style="font-family:Lora;font-style:italic;font-weight:600;font-size:70px;line-height:1.05;margin:4px 0 16px">{o}</div>
 {photo(c, 900, f"border-radius:28px;border:4px solid {champ}")}
 {title_line(c['title'], "'GFS Baskerville';font-variant:small-caps", "#FFF5E8", 46, .55, 960, "margin-top:14px")}
 <div style="font-family:Lora;font-style:italic;font-size:30px;color:{champ};margin:2px 0 16px">Style it {pair}</div>
 {C()}""", champ))
    pages.append(frame(bg, "#FFF5E8", f"""
 {logo(cs[0], 160, "#FFF5E8", champ)}
 <div style="font-family:Lora;font-style:italic;font-size:86px;line-height:1.1;text-align:center;margin:44px 40px 50px">Which occasion<br>are you dressing for?</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5;opacity:.9">Comment PRICE and we'll DM you<br>price + details instantly</div>""", champ))
    durs = [2.4] + [2.8] * len(cs) + [2.6]
    return pages, durs, "fadeblack", "zin", "Occasion Guide"


# ================================================================== 6. GIFT GUIDE — gift tags "For the bride / For mom ..."
GIFT_FOR = ["For the Bride", "For Mom", "For your Bestie", "For your Sister", "For Yourself", "For your Bhabhi", "For your Wife", "For your Daughter"]

def gift_guide(cs, n):
    bg = "#FBF3E4"
    red, ink = "#B3202A", "#3D2410"
    ribbon = (f'<div style="position:absolute;left:0;right:0;top:0;height:{H}px;pointer-events:none">'
              f'<div style="position:absolute;left:0;top:0;width:24px;height:{H}px;background:{red};opacity:.9"></div>'
              f'<div style="position:absolute;right:0;top:0;width:24px;height:{H}px;background:{red};opacity:.9"></div></div>')
    C = lambda s=1: cta(red, "#fff", red, s, "border-radius:14px;box-shadow:0 14px 30px rgba(179,32,42,.3)")
    cat = plural(cs[0]["cat"])
    hook = pick([f"Gift Guide:<br>5 {cat.lower()} she'll love", f"Gifting season,<br>sorted.", f"Not sure what<br>to gift?"], n)
    who = [GIFT_FOR[(n * 2 + k) % len(GIFT_FOR)] for k in range(len(cs))]
    tagbox = lambda t: (f'<div style="display:flex;align-items:center;gap:0">'
                        f'<div style="width:0;height:0;border-top:42px solid transparent;border-bottom:42px solid transparent;border-right:40px solid {ink}"></div>'
                        f'<div style="background:{ink};color:#FBF3E4;font-family:Lora;font-style:italic;font-size:54px;padding:12px 44px 12px 20px;border-radius:0 12px 12px 0;position:relative">'
                        f'<span style="position:absolute;left:-14px;top:34px;width:16px;height:16px;border-radius:50%;background:#FBF3E4"></span>{t}</div></div>')
    pages = [frame(bg, ink, f"""
 <div style="font-size:120px">🎁</div>
 <div style="font-family:Lora;font-weight:600;font-size:98px;line-height:1.06;text-align:center;margin:20px 60px 46px">{hook}</div>
 <div style="display:flex;flex-direction:column;gap:12px;font-family:Lora;font-style:italic;font-size:40px;text-align:center;color:{red}">
  {''.join(f'<div>{w}</div>' for w in who)}</div>
 <div style="margin-top:50px">{C(.9)}</div>""", red, ribbon)]
    for c, w in zip(cs, who):
        pages.append(frame(bg, ink, f"""
 {tagbox(w)}
 {photo(c, 940, "margin:18px 0 18px;border:12px solid #fff;box-shadow:0 26px 50px rgba(61,36,16,.2)")}
 {title_line(c['title'], "Lora;font-weight:600", ink, 50, .5, 960, "margin-bottom:18px")}
 {C()}""", red, ribbon))
    pages.append(frame(bg, ink, f"""
 {logo(cs[0], 160, "#fff", red)}
 <div style="font-family:Lora;font-weight:600;font-size:86px;line-height:1.1;text-align:center;margin:44px 60px 50px">Who are you<br>gifting this to? 💝</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5">Comment PRICE and we'll DM you<br>price + details instantly</div>""", red, ribbon))
    durs = [2.4] + [2.7] * len(cs) + [2.6]
    return pages, durs, "circleopen", "alt", "Gift Guide"


# ================================================================== 7. CHAT STORY — POV: bestie asks for advice
ASKS = ["Babe help 😭 need something for my cousin's wedding", "Office party tomorrow, what do I wear?? 👀",
        "Kuch simple but classy chahiye 🙏", "Something that goes with my red saree?", "Gift for mummy's birthday? 💝",
        "Date night outfit ready, jewellery missing 😅", "Need something for Diwali puja ✨", "Want something I can wear daily 💛"]
REPLIES_ = ["Trust me, this one 😍", "Okay but THIS 👇", "Obsessed with this one", "Wear this & thank me later ✨", "This one is SO you 💚"]

def chat_story(cs, n):
    bg = "#EDE7DF"
    green, ink = "#2F402F", "#1F1F1F"
    C = lambda s=1: cta(green, "#fff", green, s, "border-radius:999px;padding:30px 64px")
    header = lambda c: f"""<div style="display:flex;align-items:center;gap:18px;width:960px;background:#fff;border-radius:26px;padding:16px 24px;box-shadow:0 6px 20px rgba(0,0,0,.06)">
  {logo(c, 72, "#F6EBDD", "#C9A46C")}<div><div style="font-family:Poppins;font-weight:600;font-size:32px;color:{ink}">Jewora Stylist</div>
  <div style="font-size:22px;color:#3BA55C">● online</div></div></div>"""
    them = lambda t: f'<div style="align-self:flex-start;margin-left:60px;max-width:760px;background:#fff;color:{ink};font-family:Poppins;font-size:36px;line-height:1.3;padding:22px 30px;border-radius:30px 30px 30px 6px;box-shadow:0 4px 14px rgba(0,0,0,.06)">{esc(t)}</div>'
    me = lambda t: f'<div style="align-self:flex-end;margin-right:60px;background:#DCF2D4;color:{ink};font-family:Poppins;font-size:36px;padding:20px 30px;border-radius:30px 30px 6px 30px">{esc(t)}</div>'
    hook = pick(["POV: your bestie asks<br>for jewellery advice", "When the group chat<br>needs a stylist 💬", "Every girl's<br>DMs right now 😂"], n)
    asks = [ASKS[(n + k) % len(ASKS)] for k in range(len(cs))]
    pages = [frame(bg, ink, f"""
 {header(cs[0])}
 <div style="font-family:Poppins;font-weight:600;font-size:88px;line-height:1.08;text-align:center;margin:70px 40px 50px">{hook}</div>
 <div style="display:flex;flex-direction:column;gap:20px;width:1080px">{them(asks[0])}{me("Wait, I got you 😌")}</div>
 <div style="margin-top:60px">{C(.9)}</div>""", green)]
    for k, c in enumerate(cs):
        pages.append(frame(bg, ink, f"""
 {header(c)}
 <div style="display:flex;flex-direction:column;gap:14px;width:1080px;margin-top:16px">{them(asks[k])}
  <div style="align-self:flex-end;margin-right:40px;background:#DCF2D4;border-radius:34px 34px 8px 34px;padding:14px;display:flex;flex-direction:column;gap:10px">
   {photo(c, 800, "border-radius:22px")}
   <div style="font-family:Poppins;font-size:34px;color:{ink};padding:0 8px">{esc(REPLIES_[(n + k) % len(REPLIES_)])}</div></div></div>
 <div style="height:22px"></div>
 {C()}""", green))
    pages.append(frame(bg, ink, f"""
 {header(cs[0])}
 <div style="display:flex;flex-direction:column;gap:20px;width:1080px;margin:50px 0 46px">{them("Okay which one did YOU like? 🤔")}{me("Comment PRICE, I'll DM you 💌")}</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5">Price + details straight<br>to your DMs, instantly</div>""", green))
    durs = [2.6] + [3.0] * len(cs) + [2.6]
    return pages, durs, "slideup", "zin", "Chat Story"


# ================================================================== 8. SPOTLIGHT — black stage, stage light on the piece
def spotlight(cs, n):
    bg = "#060606"
    light = (f'<div style="position:absolute;left:50%;top:-200px;width:1500px;height:{H+200}px;margin-left:-750px;'
             f'background:conic-gradient(from 160deg at 50% 0%,transparent 0deg,rgba(255,236,190,.20) 14deg,rgba(255,236,190,.20) 26deg,transparent 40deg);"></div>'
             f'<div style="position:absolute;left:50%;top:1150px;width:1000px;height:180px;margin-left:-500px;border-radius:50%;'
             f'background:radial-gradient(ellipse,rgba(255,236,190,.35),transparent 70%)"></div>')
    neon = "#FFD27A"
    C = lambda s=1: cta("transparent", neon, "#060606", s, f"border:4px solid {neon};border-radius:8px;box-shadow:0 0 24px rgba(255,210,122,.6),inset 0 0 18px rgba(255,210,122,.35);text-shadow:0 0 14px rgba(255,210,122,.8)")
    hook = pick(["In the spotlight", "Main character energy", "All eyes on these"], n)
    cat = plural(cs[0]["cat"])
    pages = [frame(bg, "#fff", f"""
 <div style="font-family:Inter;font-weight:900;font-size:120px;line-height:1;text-align:center;color:{neon};text-shadow:0 0 30px rgba(255,210,122,.7)">{hook.upper()}</div>
 <div style="font-family:Lora;font-style:italic;font-size:62px;margin:30px 0 60px;opacity:.9">5 {cat.lower()} that steal the show</div>
 <div style="display:flex;gap:14px">{thumbs(cs, 170, '2px solid rgba(255,210,122,.6)')}</div>
 <div style="margin-top:60px">{C(.9)}</div>""", neon, light)]
    for c in cs:
        pages.append(frame(bg, "#fff", f"""
 <div style="font-size:24px;letter-spacing:.5em;color:{neon}">★ STARRING ★</div>
 {title_line(c['title'], "Inter;font-weight:800", "#fff", 50, .58, 960, "margin:10px 0 20px")}
 {photo(c, 980, "border-radius:36px;box-shadow:0 0 0 3px rgba(255,210,122,.7),0 0 90px rgba(255,210,122,.35)")}
 <div style="height:24px"></div>
 {C()}""", neon, light))
    pages.append(frame(bg, "#fff", f"""
 {logo(cs[0], 160, "#111", neon)}
 <div style="font-family:Inter;font-weight:900;font-size:88px;line-height:1.05;text-align:center;margin:44px 40px 50px">Who's your<br><span style="color:{neon}">star?</span> ⭐</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:44px;text-align:center;line-height:1.5;opacity:.85">Comment PRICE and we'll DM you<br>price + details instantly</div>""", neon, light))
    durs = [2.2] + [2.6] * len(cs) + [2.6]
    return pages, durs, "fadeblack", "zin", "Spotlight"


# ================================================================== 9. TRENDING — bold ticker stripes, fast cuts
def trending(cs, n):
    bg = "#FF6B1A"
    ink = "#111"
    tick = lambda top, rot, txt: (f'<div style="position:absolute;left:-100px;right:-100px;top:{top}px;transform:rotate({rot}deg);background:{ink};'
                                  f'color:#FFE14D;font-family:Inter;font-weight:900;font-size:40px;letter-spacing:.08em;white-space:nowrap;padding:14px 0;overflow:hidden">'
                                  f'{(txt + " ✦ ") * 8}</div>')
    extra = tick(150, -4, "TRENDING NOW") + tick(1790, 3, "NEW IN · HOT PICKS")
    C = lambda s=1: cta("#FFE14D", ink, "#FFE14D", s, f"border:5px solid {ink};border-radius:16px;box-shadow:10px 10px 0 {ink}")
    hook = pick(["Trending this week 🔥", "Hot right now 🔥", "Everyone's loving these 🔥"], n)
    cat = plural(cs[0]["cat"])
    pages = [frame(bg, ink, f"""
 <div style="font-family:Inter;font-weight:900;font-size:{fit(cat.upper(), 170, .66, 1000)}px;line-height:.9;color:#fff;-webkit-text-stroke:4px {ink}">{esc(cat.upper())}</div>
 <div style="font-family:Inter;font-weight:900;font-size:76px;margin:30px 0 50px;text-align:center">{hook}</div>
 <div style="display:grid;grid-template-columns:repeat(3,250px);gap:18px;justify-content:center">{thumbs(cs[:3], 250, f'5px solid {ink}')}</div>
 <div style="margin-top:60px">{C(.9)}</div>""", ink, extra)]
    for c in cs:
        pages.append(frame(bg, ink, f"""
 <div style="display:flex;justify-content:space-between;align-items:center;width:960px">
  <div style="background:#fff;border:5px solid {ink};font-family:Inter;font-weight:900;font-size:32px;padding:8px 22px;transform:rotate(-3deg)">🔥 HOT PICK</div>
  <div style="font-family:Inter;font-weight:900;font-size:64px;color:#fff;-webkit-text-stroke:3px {ink}">{c['i']:02d}</div></div>
 {photo(c, 950, f"margin:16px 0 22px;border:6px solid {ink};border-radius:30px;box-shadow:12px 12px 0 {ink}")}
 {title_line(c['title'], "Inter;font-weight:900", ink, 48, .6)}
 <div style="margin-top:16px">{C()}</div>""", ink, extra))
    pages.append(frame(bg, ink, f"""
 <div style="font-family:Inter;font-weight:900;font-size:100px;line-height:1;text-align:center;color:#fff;-webkit-text-stroke:4px {ink}">DON'T MISS<br>OUT!</div>
 <div style="font-family:Inter;font-weight:800;font-size:44px;margin:40px 0 50px;text-align:center">Your next favourite is here</div>
 {C(1.05)}
 <div style="font-size:30px;font-weight:600;margin-top:50px;text-align:center;line-height:1.5">Comment PRICE and we'll DM you<br>price + details instantly</div>""", ink, extra))
    durs = [2.0] + [2.2] * len(cs) + [2.4]
    return pages, durs, "hrslice", "pan", "Trending Now"


# ================================================================== 10. MOOD BOARD — kraft paper, tape, handwritten notes
NOTES = ["obsessed!!", "must-have", "so pretty 😍", "wedding ready", "add to cart?", "need this", "elegant af", "pure love"]

def mood_board(cs, n):
    bg = "repeating-linear-gradient(0deg,rgba(0,0,0,.025) 0 2px,transparent 2px 6px),linear-gradient(180deg,#D9C3A0,#C9AE84)"
    ink = "#3B2A1A"
    tape = lambda x, y, r: f'<div style="position:absolute;left:{x}px;top:{y}px;width:170px;height:46px;background:rgba(255,248,220,.75);transform:rotate({r}deg);box-shadow:0 2px 6px rgba(0,0,0,.1)"></div>'
    C = lambda s=1: cta(ink, "#F8EEDC", ink, s, "border-radius:6px;box-shadow:0 12px 24px rgba(59,42,26,.3)")
    cat = plural(cs[0]["cat"])
    hook = pick([f"My {cat.lower()}<br>mood board", "Saving these for<br>wedding season", "Pinned: the<br>dream list 📌"], n)
    pol = lambda c, size, rot, extra="": (f'<div style="position:relative;background:#FFFDF7;padding:18px 18px 0;transform:rotate({rot}deg);box-shadow:0 18px 34px rgba(59,42,26,.3);{extra}">'
                                          f'{photo(c, size)}<div style="height:{int(size*.07)}px"></div>{tape(int(size/2)-85+18, -24, -4)}</div>')
    pages = [frame(bg, ink, f"""
 <div style="font-family:Lora;font-style:italic;font-weight:600;font-size:110px;line-height:1.02;text-align:center">{hook}</div>
 <div style="position:relative;width:960px;height:640px;margin:40px 0 30px">
  <div style="position:absolute;left:20px;top:40px">{pol(cs[0], 330, -7)}</div>
  <div style="position:absolute;left:330px;top:0">{pol(cs[1], 330, 4)}</div>
  <div style="position:absolute;left:610px;top:60px">{pol(cs[2], 300, -3)}</div></div>
 {C(.9)}""", ink)]
    for k, c in enumerate(cs):
        rot = -2.5 if k % 2 else 2.5
        pages.append(frame(bg, ink, f"""
 <div style="font-size:24px;letter-spacing:.36em">PIN {c['i']:02d} · {label(c)}</div>
 <div style="margin:34px 0 0">{pol(c, 840, rot)}</div>
 <div style="font-family:Lora;font-style:italic;font-size:52px;color:#8C2F1B;transform:rotate(-4deg);margin:-6px 0 0">{NOTES[(n + k) % len(NOTES)]}</div>
 {title_line(c['title'], "Lora;font-weight:600", ink, 42, .5, 960, "margin-bottom:14px")}
 {C()}""", ink))
    pages.append(frame(bg, ink, f"""
 <div style="position:relative;width:900px;height:420px;margin-bottom:40px">
  <div style="position:absolute;left:30px;top:30px">{pol(cs[3], 260, -6)}</div>
  <div style="position:absolute;left:320px;top:0">{pol(cs[4], 260, 3)}</div>
  <div style="position:absolute;left:600px;top:40px">{pol(cs[0], 240, -2)}</div></div>
 <div style="font-family:Lora;font-style:italic;font-weight:600;font-size:80px;line-height:1.1;text-align:center;margin-bottom:40px">Which one makes<br>your board?</div>
 {C(1.05)}
 <div style="font-size:30px;margin-top:40px;text-align:center;line-height:1.5">Comment PRICE and we'll DM you<br>price + details instantly</div>""", ink))
    durs = [2.4] + [2.7] * len(cs) + [2.6]
    return pages, durs, "dissolve", "alt", "Mood Board"


FORMATS = {
    "countdown": countdown, "this_or_that": this_or_that, "film_strip": film_strip, "progress_row": progress_row,
    "occasion": occasion, "gift_guide": gift_guide, "chat_story": chat_story, "spotlight": spotlight,
    "trending": trending, "mood_board": mood_board,
}
# order chosen so neighbours never share a colour family or mood
ORDER = ["countdown", "gift_guide", "chat_story", "spotlight", "progress_row", "trending", "occasion", "this_or_that", "mood_board", "film_strip"]


def build(key, dcs, n=0):
    return FORMATS[key](dcs, n)
