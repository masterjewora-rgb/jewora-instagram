# Jewora DM Sender — runbook (runs every hour, only when the user's laptop is on)

Sends one Instagram DM with product links to each commenter queued in `dm_queue.csv` (filled by the hourly
comment-reply task, see REPLIES.md). Sent ones go to `dm_sent.csv`, so nobody gets two DMs.
Uses the **built-in browser** of the Claude desktop app on the user's laptop (fallback: Claude in Chrome), signed in as **jewora_official**.

## Steps
1. `git pull` in this repo.
2. Catalog: Google Drive `download_file_content` on sheet `1h8ytLn1dTOBnir3Z_BOyAIzLBXtzNDefm_w90nMsfqI` with
   `exportMimeType: text/csv` → `python3 get_catalog.py <tool-results file>`.
3. `python3 comments.py dm-todo` → `dm_todo.json`. If 0 pending → stop, summary "No DMs pending".
4. Browser: load the browser tools. If the laptop/browser cannot be reached → stop quietly (next run retries; do not mark anything).
   Open `https://business.facebook.com/latest/inbox/instagram` (Meta Business Suite inbox → Instagram comments).
   If it asks to log in, stop and tell the user to log in once in the built-in browser as jewora_official — never type passwords.
5. For each entry in dm_todo.json (max 15 per run, oldest first):
   a. Find that comment: in the Business Suite inbox Instagram **comments** view, open the post / comment matching
      `comment_text` and time; or open `permalink` on instagram.com to see the commenter's username.
   b. Send the DM:
      - Preferred: on the comment in Business Suite use **"Send private reply" / "Message"** (private reply to the comment).
      - Fallback: `https://www.instagram.com/direct/new/` → search the commenter's username → open chat.
   c. Paste the message (template below), send it, and check it appears in the conversation.
   d. Success → `python3 comments.py dm-sent <comment_id>`. If Instagram says the person can't be messaged / the private
      reply window has closed → `python3 comments.py dm-sent <comment_id> --status failed` and move on.
   Wait 20–40 seconds between DMs (natural pace, avoids Instagram's spam limits). If Instagram shows a "try again later" /
   action-blocked warning → stop the run immediately and report it.
6. `git add dm_sent.csv && git commit -m "DMs sent" && git push` (pull --rebase first if rejected). Don't commit dm_todo.json or catalog.csv.
7. 2–3 line Hinglish summary: kitne DM gaye, kitne fail, koi warning.

## DM message (English) — fill from the entry's `products`
Use short names (from the post caption if you saw it, else `name` shortened to ~4–6 words). Never invent a price; skip a product with empty price or link.

```
Hi! 💛 Thank you for your interest in Jewora.
Here are the details of the pieces you loved:

1️⃣ <Name> – <price>
👉 <link>

2️⃣ <Name> – <price>
👉 <link>

... (all pieces of that post)

🚚 Free Shipping across India
💵 Cash on Delivery Available
🔄 7-Day Easy Returns

Tap any link to order. Need help choosing? Just reply here — we're happy to help! ✨
Team Jewora
```

If the comment asked about one specific piece ("2nd one", "the pendant"), put that piece first with "⭐ The one you asked about:" and then the rest.
If `products` is empty (older post): send the greeting + "Shop our full collection: https://jewora.com" + the three trust lines.
