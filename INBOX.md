# Jewora Inbox Engine — runbook (runs every hour, only when the user's laptop is on)

Answers customers EVERYWHERE they write to Jewora, from one place — **Meta Business Suite inbox**
(`https://business.facebook.com/latest/inbox/all`), which shows all four channels:
- **Instagram comments** (public reply is already done by the cloud "Jewora Comment Replies" task → here we only send the queued DMs)
- **Facebook comments** on Jewora Page posts (public reply + Messenger private reply, both here)
- **Messenger** messages to the Jewora Page
- **Instagram DMs** to jewora_official

Uses the **built-in browser** of the Claude desktop app on the user's laptop (fallback: Claude in Chrome), signed in to Facebook /
Business Suite with access to the Jewora Page and jewora_official. Never type passwords; if a login is asked, stop and tell the user.

## Setup each run
1. `git pull` in this repo.
2. Catalog: Google Drive `download_file_content` on sheet `1h8ytLn1dTOBnir3Z_BOyAIzLBXtzNDefm_w90nMsfqI` with
   `exportMimeType: text/csv` → `python3 get_catalog.py <tool-results file>`.
3. Load the browser tools. If the laptop/browser can't be reached → stop quietly (next run retries; mark nothing).
4. Product lookup helpers:
   - `python3 comments.py media <instagram media_id>` → the 5 products of one of our Instagram posts.
   - `python3 comments.py find <words from post caption / product name / customer message>` → id | name | price | link.
   - Product names in our post captions are listed as "1️⃣ Name" lines — search those names with `find`.
   Never invent a price or link: only use what these helpers print.

## A. Queued Instagram DMs (from public comment replies)
`python3 comments.py dm-todo` → `dm_todo.json`. For each (oldest first):
open the comment in Business Suite inbox → Instagram comments (or the `permalink` on instagram.com to see the username),
send the **Product DM** (template below) via "Send private reply"/"Message" (fallback: instagram.com/direct/new → username).
Then `python3 comments.py dm-sent <comment_id>` (or `--status failed` if Instagram won't allow messaging that person).

## B. Facebook comments (Business Suite inbox → Facebook comments)
For each comment on a Jewora Page post that has **no reply from the Page yet**:
- Buying interest (price, details, link, "want this", which one…): reply publicly with
  "Hi <first name>! 💛 Thank you for loving this. Details will be shared soon in your inbox 📩
  🚚 Free Shipping | 💵 COD Available | 🔄 7-Day Easy Returns" — then send the **Product DM** as a Messenger private reply
  ("Send private message"/"Message" on that comment). Products = the post's pieces (find them from the post caption with `find`).
- Compliment → warm one-line thank-you, no DM. Question → answer (free shipping, COD, 7-day returns) + offer details in inbox.
- Spam / abuse / gibberish → leave it.

## C. Messenger + Instagram DMs (Business Suite inbox → Messenger, Instagram direct)
Open every conversation whose **last message is from the customer** (unread / not answered by us). Read the whole thread and reply in English:
- Asks price/details of a product (named, or a shared post/reel/screenshot): identify it (shared post caption → `media`/`find`;
  product name → `find`; picture only → describe it in words and `find`). Send name, price and link of the matching piece(s)
  (max 5) + the trust lines. If you can't identify it confidently, ask politely: "Could you share the product name or a screenshot? 💛"
  — never guess.
- Generic "price?" / "hi" with nothing shared: greet + ask which piece they liked + link to the full collection https://jewora.com + trust lines.
- Order status, return / exchange, damaged item, payment problem, complaint, wholesale, anything you're not sure about:
  "Thank you for reaching out! 💛 Our team will get back to you shortly." — do not promise anything else, and list it in the summary
  so the user can handle it personally.
- If our team (a human) already replied after the customer's last message, skip the conversation.

## Pace and safety
- Max 25 messages per run in total, 20–40 seconds between sends. If Instagram/Facebook shows "try again later", "action blocked"
  or any warning → stop immediately and report it.
- Never send the same message twice in a conversation; check the thread before sending.
- Never share customer data anywhere else.

## Finish
`git add dm_sent.csv && git commit -m "Inbox run" && git push` (pull --rebase first if rejected); don't commit dm_todo.json or catalog.csv.
Hinglish summary (3–5 lines): Instagram queued DMs sent, FB comments replied, Messenger + Instagram DMs answered,
**conversations needing the team** (name + one-line issue), any warnings.

## Product DM template (English)
Use short names (~4–6 words). Skip any piece without price or link.

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

If the customer asked about one piece ("2nd one", "the pendant"), put it first under "⭐ The one you asked about:" then the rest.
If no products are known (older post): greeting + "Shop our full collection: https://jewora.com" + the three trust lines.
