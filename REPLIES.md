# Jewora Instagram Comment Replies — runbook (runs every hour)

Replies publicly, in English, to every new top-level comment on jewora_official posts
(Windsor connector `instagram`, account `17841475914389502`). Never replies twice: handled ids live in `replied.csv`.
DMs are NOT possible through Windsor — never write "check your DM" / "we've DMed you".

## Steps
1. `git pull` in this repo (if a pull fails because of local changes: `git stash && git pull && git stash pop`).
2. Catalog: Google Drive `download_file_content` on sheet `1h8ytLn1dTOBnir3Z_BOyAIzLBXtzNDefm_w90nMsfqI`
   with `exportMimeType: text/csv` → result is saved to a tool-results file → `python3 get_catalog.py <that file>`.
3. Comments: Windsor `get_data`, connector `instagram`, accounts `["17841475914389502"]`, `date_preset: "last_30dT"`, fields
   `["media_id","media_caption","media_permalink","comment_id","comment_parent_id","comment_text","comment_username","comment_timestamp","comment_reply_count"]`.
   (Do not pass force_refresh — the trial plan rejects it.) Save the returned JSON to `comments_raw.json` with the Write tool,
   then `python3 comments.py prepare comments_raw.json`. If it says 0 new comments → stop, summary "No new comments".
4. For each entry in `pending.json`, decide and write ONE reply (rules below), then post it with Windsor `execute_action`:
   connector `instagram`, account `17841475914389502`, action `reply_to_comment`, params `{"comment_id": "...", "message": "..."}`.
   After each success: `python3 comments.py mark <comment_id>`. For a comment you deliberately skip:
   `python3 comments.py mark <comment_id> --status skipped`.
   If a reply fails with a permission error → stop, do NOT mark it, and report that the Instagram account must be reconnected in Windsor.
5. `git add replied.csv comments.py REPLIES.md && git commit -m "Comment replies" && git push` (pull --rebase first if push is rejected).
   Do not commit pending.json, comments_raw.json or catalog.csv.
6. Finish with a 2–3 line Hinglish summary: kitne comments, kya reply gaya (short), kuch skip/error hua to kya.

## Reply rules (English, warm, premium, short — max ~350 characters)
- Use the product names from `caption_names` (short ones the customer saw); fall back to `products[].name`, shortened to ~4–5 words.
- Prices = `products[].price` (sale price). Never invent a price. Skip a product whose price is empty.
- **Price / cost / rate / "how much" / "details" / "send" / "link" / "want this" comments** on a post with products:
  greet + list each piece as "1️⃣ Name – ₹price" (one per line) + "Shop now via the link in our bio 🛍️ Free shipping across India 🚚".
- **Comment asks about one piece** ("2nd one", "no 3", "the pendant", "last one"): give that piece's name, price AND its `link` (the full jewora.com URL), plus "Free shipping across India 🚚".
- **Post with no known products** (`products` empty, e.g. older posts): thank them and say "Tap the link in our bio to shop the full collection 🛍️". No prices.
- **Compliments** ("beautiful", "😍", "nice"): warm thank-you, one line, invite them to shop via link in bio.
- **Questions** (COD, delivery time, returns, material, size): answer only what is certain — free shipping across India; for anything else say "Please DM us and our team will help you right away 💛". Never make up policies.
- **Spam, abuse, gibberish, promo from other accounts, or not about Jewora**: skip (mark `--status skipped`), don't reply.
- Never mention DMs being sent by us. No hashtags. 1–2 emojis max besides the number emojis. Don't repeat the exact same wording for every reply in a run — vary the greeting.
