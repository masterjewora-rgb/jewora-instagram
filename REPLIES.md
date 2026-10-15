# Jewora Instagram Comment Replies — runbook (runs every hour)

Replies publicly, in English, to every new top-level comment on jewora_official posts
(Windsor connector `instagram`, account `17841475914389502`). Never replies twice: handled ids live in `replied.csv`.
DMs are sent separately by the "Jewora Inbox Engine" task (browser on the user's laptop) from `dm_queue.csv`.

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
5. `git add replied.csv dm_queue.csv comments.py REPLIES.md && git commit -m "Comment replies" && git push` (pull --rebase first if push is rejected).
   Do not commit pending.json, comments_raw.json or catalog.csv.
6. Finish with a 2–3 line Hinglish summary: kitne comments, kya reply gaya (short), kuch skip/error hua to kya.

## Reply rules (English, warm, premium, short — max ~250 characters)
Product details now go by DM (sent later from the browser by the "Jewora Inbox Engine" task, see INBOX.md), so public replies stay short and do NOT list prices or links.
- **Price / cost / rate / "how much" / "details" / "send" / "link" / "want this" / "which one" / asks about a piece** (any comment showing buying interest):
  warm greeting + "Details will be shared soon in your DM 📩" + the trust line on its own line:
  "🚚 Free Shipping | 💵 COD Available | 🔄 7-Day Easy Returns"
  e.g. "Hi there! 💛 Thank you for loving this edit. Details will be shared soon in your DM 📩
  🚚 Free Shipping | 💵 COD Available | 🔄 7-Day Easy Returns"
  Mark these `replied` (default) — that also queues their DM.
- **Compliments** ("beautiful", "😍", "nice"): warm one-line thank-you + "Comment PRICE and we'll send you the details in DM 📩". Mark `--status thanked` (no DM queued).
- **Questions** (COD, delivery, returns, material, size): answer what is certain — free shipping across India, Cash on Delivery available, 7-day easy returns — and add "More details will be shared soon in your DM 📩". Mark `replied` (queues a DM).
- **Spam, abuse, gibberish, promo from other accounts, or not about Jewora**: skip (mark `--status skipped`), don't reply, no DM.
- No hashtags, no prices, no URLs in public replies. 1–3 emojis. Vary the greeting across replies in a run.
