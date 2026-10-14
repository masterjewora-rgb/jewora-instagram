"""Pick the next carousel: format (rotates through 12) + category + candidate products that were never posted.

Usage:
  python3 plan.py CATALOG_CSV            -> writes plan.json
CATALOG_CSV = the Instagram sheet exported as CSV (columns id,title,availability,price,sale_price,color,material,...).
Excludes every id in posted.csv and missing_photos.txt. Never repeats a product.
"""
import csv, json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
csv.field_size_limit(10**9)
from reel_styles import REEL_ORDER

FORMAT_ORDER = ["classic_band", "polaroid", "magazine_strip", "luxe_border", "masthead_top", "two_tone",
                "price_tag", "minimal_white", "gallery_frame", "arch", "big_number", "side_spine"]

# category: (display type for eyebrow, keyword regex) — first match wins
CATEGORIES = [
    ("earrings", "Earrings", r"jhumk|earring|ear ?cuff|studs?\b|chandbali|bali\b|danglers?|hoops?"),
    ("necklace_set", "Necklace Set", r"necklace set|haar|choker|rani haar|mangalsutra|jewell?ery set|jewelry set"),
    ("pendant", "Pendant", r"pendant|locket|chain"),
    ("necklace", "Necklace", r"necklace|mala"),
    ("bangles", "Bangles", r"bangle|kada|bracelet|cuff"),
    ("rings", "Ring", r"\brings?\b"),
    ("tikka", "Maang Tikka", r"tikka|matha ?patti|passa"),
    ("anklet", "Anklet", r"anklet|payal|pajeb"),
]
CATEGORY_CYCLE = ["earrings", "necklace_set", "pendant", "bangles", "earrings", "necklace", "rings", "necklace_set", "tikka", "anklet"]

THEMES = [
    (r"kundan", "Kundan"), (r"polki", "Polki"), (r"temple|lakshmi|laxmi", "Temple"), (r"pearl|moti", "Pearl"),
    (r"\bad\b|american diamond|cz\b|zircon|diamond|solitaire", "Diamond"), (r"oxidi[sz]ed|silver[- ]tone", "Oxidised"),
    (r"meena|enamel", "Meenakari"), (r"rose gold", "Everyday"), (r"antique|rajwadi|jadau|heritage", "Heritage"),
    (r"925|sterling", "Sterling Silver"), (r"floral|flower|petal|leaf", "Floral"),
]

STONES = [(r"ruby", "Ruby"), (r"emerald|panna|green stone", "Emerald"), (r"pearl|moti", "Pearl"), (r"kundan", "Kundan"),
          (r"polki", "Polki"), (r"\bad\b|american diamond|cz\b|zircon|diamond", "White AD"), (r"sapphire|blue stone", "Sapphire"),
          (r"crystal", "Crystal")]


def clean_title(t):
    t = re.sub(r"[^\w\s&'\-–|,.()]", "", t, flags=re.UNICODE).strip()
    t = re.sub(r"^[A-Z][a-zA-Z]+'s\s+", "", t)                 # "Avnee's ..." -> "..."
    t = re.split(r"\s[–|-]\s|\s\|\s|:", t)[0].strip()          # drop subtitles
    t = re.sub(r"\s+for women.*$", "", t, flags=re.I)
    t = re.sub(r"\(.*?\)", "", t).strip(" .,-")
    t = re.sub(r"\s+by\s+\w+.*$", "", t, flags=re.I)
    if t.isupper() or t.islower():
        t = t.title()
    words = t.split()
    if len(t) > 42:
        out = []
        for w in words:
            if len(" ".join(out + [w])) > 42: break
            out.append(w)
        while out and out[-1].lower() in ("with", "by", "and", "&", "for", "in", "of", "-", "–"):
            out.pop()
        t = " ".join(out)
    return t


def category_of(title):
    title = re.split(r"\s[–|-]\s|\s\|\s|:", title)[0]
    title = re.split(r"\s(?:with|by|&|and|\+)\s", title, flags=re.I)[0]
    # the product noun usually comes last ("... Pearl Drop Necklace Set"), so the latest keyword wins
    tl = title.lower()
    best, pos = ("other", "Jewellery"), -1
    for key, label, rx in CATEGORIES:
        for m in re.finditer(rx, tl):
            if m.end() >= pos:
                best, pos = (key, label), m.end()
    return best


def theme_of(title):
    tl = title.lower()
    for rx, name in THEMES:
        if re.search(rx, tl):
            return name
    return "Signature"


def money(s):
    s = (s or "").replace("INR", "").replace(",", "").strip()
    try:
        v = float(s)
        return f"{int(round(v)):,}" if v > 0 else ""
    except ValueError:
        return ""


def read_ids(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p): return set()
    with open(p) as f:
        return {line.split(",")[0].strip() for line in f if line.strip() and not line.startswith("id")}


def main():
    catalog = sys.argv[1]
    state = json.load(open(os.path.join(HERE, "state.json")))
    nc = state.get("carousels_posted", 0); nr = state.get("reels_posted", 0)
    n = nc + nr                     # total posts so far: drives category rotation + numbering
    exclude = read_ids("posted.csv") | read_ids("missing_photos.txt")

    pool = {}
    for r in csv.DictReader(open(catalog, encoding="utf-8")):
        pid = (r.get("id") or "").strip()
        if not pid or pid in exclude or (r.get("availability") or "").strip().lower() != "in stock":
            continue
        raw = r.get("title") or ""
        key, label = category_of(raw)
        title = clean_title(raw)
        if not title: continue
        stones = next((name for rx, name in STONES if re.search(rx, raw.lower())), "")
        finish = (r.get("material") or "").strip() or "Gold"
        shade = (r.get("color") or "").strip()
        specs = [["Stones", stones]] if stones else ([["Shade", shade]] if shade and shade != "Multicolor" else [])
        specs.append(["Finish", finish if finish != "Multiple" else "Mixed"])
        pool.setdefault(key, []).append({
            "id": pid, "title": title, "category": key,
            "eyebrow": f"The {theme_of(raw)} Edit · {label}",
            "specs": specs, "price": money(r.get("sale_price")) or money(r.get("price")),
        })

    # category: follow the cycle, skip ones with too few products left
    start = n % len(CATEGORY_CYCLE)
    order = CATEGORY_CYCLE[start:] + CATEGORY_CYCLE[:start] + ["other"]
    cat = next((c for c in order if len(pool.get(c, [])) >= 8), None)
    if cat is None:
        cat = max(pool, key=lambda c: len(pool[c])) if pool else None
    if cat is None:
        print("NO PRODUCTS LEFT"); sys.exit(2)

    cands = pool[cat][:]
    random.Random(n * 7919 + 13).shuffle(cands)
    plan = {"carousel_number": n + 1, "format": FORMAT_ORDER[nc % len(FORMAT_ORDER)],
            "reel_style": REEL_ORDER[nr % len(REEL_ORDER)], "category": cat,
            "remaining_in_category": len(pool[cat]), "remaining_total": sum(len(v) for v in pool.values()),
            "candidates": cands[:60]}
    json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in plan.items() if k != "candidates"}))
    print("candidate ids:", " ".join(c["id"] for c in plan["candidates"]))


if __name__ == "__main__":
    main()
