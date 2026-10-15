"""Comment reply engine — prepares new Instagram comments for replying.

Usage:
  python3 comments.py prepare COMMENTS_JSON   # COMMENTS_JSON = Windsor get_data result (JSON with "data" list, or a bare list)
      -> writes pending.json: one entry per new comment, with the post's products (name, price, link)
  python3 comments.py mark COMMENT_ID [COMMENT_ID ...] [--status replied|skipped]
      -> appends to replied.csv so the comment is never handled again; "replied" ones are also queued in dm_queue.csv
  python3 comments.py dm-todo                       # DMs still to send -> dm_todo.json (needs catalog.csv)
  python3 comments.py dm-sent COMMENT_ID [...] [--status sent|failed|expired]

Needs catalog.csv (see get_catalog.py) and posted.csv (media_id -> product ids).
"""
import csv, json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OWN = "jewora_official"
MAX_AGE_DAYS = 7


def load_replied():
    p = os.path.join(HERE, "replied.csv")
    if not os.path.exists(p):
        return set()
    return {r["comment_id"] for r in csv.DictReader(open(p, encoding="utf-8"))}


def price_of(row):
    raw = (row.get("sale_price") or row.get("price") or "").replace("INR", "").replace(",", "").strip()
    try:
        v = float(raw)
    except ValueError:
        return ""
    return "₹" + f"{v:,.0f}"


def prepare(path):
    j = json.load(open(path, encoding="utf-8"))
    rows = j["data"] if isinstance(j, dict) else j

    catalog = {}
    cp = os.path.join(HERE, "catalog.csv")
    if os.path.exists(cp):
        for r in csv.DictReader(open(cp, encoding="utf-8")):
            catalog[r["id"]] = r
    by_media = {}
    for r in csv.DictReader(open(os.path.join(HERE, "posted.csv"), encoding="utf-8")):
        by_media.setdefault(r["media_id"], []).append(r["id"])

    replied = load_replied()
    # comments we already answered on Instagram (a reply from our own account exists)
    answered = {r.get("comment_parent_id") for r in rows
                if r.get("comment_parent_id") and (r.get("comment_username") or "") == OWN}

    now = datetime.datetime.now(datetime.timezone.utc)
    pending, seen = [], set()
    for r in rows:
        cid = r.get("comment_id")
        if not cid or cid in seen:
            continue
        seen.add(cid)
        if r.get("comment_parent_id"):          # only top-level comments
            continue
        if (r.get("comment_username") or "") == OWN:
            continue
        if cid in replied or cid in answered:
            continue
        ts = r.get("comment_timestamp") or ""
        try:
            t = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")
            if (now - t).days > MAX_AGE_DAYS:
                continue
        except ValueError:
            pass
        products = []
        for n, pid in enumerate(by_media.get(r.get("media_id"), []), 1):
            c = catalog.get(pid, {})
            products.append({"n": n, "id": pid, "name": c.get("title", ""), "price": price_of(c),
                             "link": c.get("link", ""), "in_stock": c.get("availability", "") == "in stock"})
        pending.append({"comment_id": cid, "media_id": r.get("media_id"), "permalink": r.get("media_permalink"),
                        "text": r.get("comment_text"), "time": ts,
                        "caption_first_line": (r.get("media_caption") or "").split("\n")[0][:100],
                        "caption_names": [l.strip() for l in (r.get("media_caption") or "").split("\n")
                                          if l.strip()[:1] in "12345" and "️⃣" in l[:4]],
                        "products": products})
    json.dump(pending, open(os.path.join(HERE, "pending.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(pending)} new comment(s) to handle -> pending.json")
    for p in pending:
        print(f"- {p['comment_id']} | {p['text']!r} | {len(p['products'])} products known")


def mark(ids, status):
    p = os.path.join(HERE, "replied.csv")
    new = not os.path.exists(p)
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(p, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["comment_id", "handled_at", "status"])
        for i in ids:
            w.writerow([i, t, status])
    print("marked", ids, status)
    if status == "replied":
        queue_dm(ids, t)


DMQ_FIELDS = ["comment_id", "queued_at", "comment_time", "media_id", "permalink", "comment_text", "product_ids"]


def queue_dm(ids, t):
    """Every replied comment also gets a DM later (sent from the browser by the DM task, see DMS.md)."""
    pp = os.path.join(HERE, "pending.json")
    pend = {x["comment_id"]: x for x in json.load(open(pp, encoding="utf-8"))} if os.path.exists(pp) else {}
    q = os.path.join(HERE, "dm_queue.csv")
    new = not os.path.exists(q)
    with open(q, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=DMQ_FIELDS)
        if new:
            w.writeheader()
        for i in ids:
            x = pend.get(i, {})
            w.writerow({"comment_id": i, "queued_at": t, "comment_time": x.get("time", ""),
                        "media_id": x.get("media_id", ""), "permalink": x.get("permalink", ""),
                        "comment_text": (x.get("text") or "").replace("\n", " ")[:200],
                        "product_ids": " ".join(pr["id"] for pr in x.get("products", []))})
    print("queued for DM:", ids)


def dm_todo():
    """Print DMs still to send (queued, not yet in dm_sent.csv, comment younger than 7 days) with message drafts' data."""
    q = os.path.join(HERE, "dm_queue.csv")
    if not os.path.exists(q):
        print("0 DMs pending"); return
    sentp = os.path.join(HERE, "dm_sent.csv")
    sent = {r["comment_id"] for r in csv.DictReader(open(sentp, encoding="utf-8"))} if os.path.exists(sentp) else set()
    catalog = {}
    cp = os.path.join(HERE, "catalog.csv")
    if os.path.exists(cp):
        for r in csv.DictReader(open(cp, encoding="utf-8")):
            catalog[r["id"]] = r
    now = datetime.datetime.now(datetime.timezone.utc)
    todo = []
    for r in csv.DictReader(open(q, encoding="utf-8")):
        if r["comment_id"] in sent:
            continue
        try:
            age = (now - datetime.datetime.strptime(r["comment_time"], "%Y-%m-%dT%H:%M:%S%z")).days
            if age >= 7:
                continue
        except ValueError:
            pass
        prods = [{"id": pid, "name": catalog.get(pid, {}).get("title", ""), "price": price_of(catalog.get(pid, {})),
                  "link": catalog.get(pid, {}).get("link", "")} for pid in r["product_ids"].split()]
        todo.append({**r, "products": prods})
    json.dump(todo, open(os.path.join(HERE, "dm_todo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(todo)} DM(s) pending -> dm_todo.json")
    for x in todo:
        print(f"- {x['comment_id']} | {x['comment_text']!r} | {x['permalink']} | {len(x['products'])} products")


def dm_sent(ids, status):
    p = os.path.join(HERE, "dm_sent.csv")
    new = not os.path.exists(p)
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(p, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["comment_id", "sent_at", "status"])
        for i in ids:
            w.writerow([i, t, status])
    print("DM marked", ids, status)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare(sys.argv[2])
    elif sys.argv[1] == "mark":
        args = sys.argv[2:]
        status = "replied"
        if "--status" in args:
            k = args.index("--status"); status = args[k + 1]; args = args[:k] + args[k + 2:]
        mark(args, status)
    elif sys.argv[1] == "dm-todo":
        dm_todo()
    elif sys.argv[1] == "dm-sent":
        args = sys.argv[2:]
        status = "sent"
        if "--status" in args:
            k = args.index("--status"); status = args[k + 1]; args = args[:k] + args[k + 2:]
        dm_sent(args, status)
