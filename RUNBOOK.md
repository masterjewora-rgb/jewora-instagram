# Jewora Instagram Posting — runbook (one carousel per run)

Each run posts ONE 5-slide carousel to Instagram account **jewora_official** (Windsor connector `instagram`, account `17841475914389502`).
Products never repeat: every posted id is in `posted.csv`, and `plan.py` skips them.

## Sources
- Product sheet (Google Sheet "Instagram sheet"): file id `1h8ytLn1dTOBnir3Z_BOyAIzLBXtzNDefm_w90nMsfqI`
- Product photos (Google Drive folder, file name = sheet id, e.g. `4968.png`): folder id `1YDuARLXLLDulwoBvktE47tsV0K72xKNT`

## Steps
1. `git pull` in this repo.
2. Catalog: Google Drive `download_file_content` on the sheet with `exportMimeType: text/csv`. The result is saved to a tool-results file → `python3 get_catalog.py <that file>`.
3. `python3 plan.py catalog.csv` → prints format, category and up to 60 candidate ids (writes plan.json).
4. Photos: Drive `search_files` with
   `parentId = '1YDuARLXLLDulwoBvktE47tsV0K72xKNT' and (title = 'ID1.png' or title = 'ID2.png' ...)` for the candidates, 15 at a time, in plan order,
   until 5 photos are found (also try `.jpg` if needed). Take the first 5 found in plan order.
   Download each with `download_file_content` (results land in tool-results files) → `python3 decode_photos.py <files...>`.
   Look at each photo (Read the jpg in photos/). Skip a product if the photo clearly shows a different kind of item than its title, and use the next candidate.
5. If a title in plan.json reads oddly (cut off, brand words, ALL CAPS, codes), fix it in plan.json (short, elegant, max ~32 chars). Do not change ids or prices.
6. `python3 make_carousel.py ID1 ID2 ID3 ID4 ID5` → renders slides/cNNNN/ and prints 5 raw.githubusercontent URLs.
   Read 1–2 rendered slides to check nothing overlaps or is cut.
7. `git add slides plan.py formats.py && git commit -m "Carousel cNNNN" && git push`. Wait ~20 s.
8. Caption (see below). Post with Windsor `execute_action`: connector `instagram`, account `17841475914389502`,
   action `create_carousel_post`, params `{"image_urls": [5 urls in order], "caption": "..."}`.
   If it fails because an image URL is not reachable yet, wait 60 s and retry once.
9. On success: `python3 record.py <media_id or "posted">`, then `git add posted.csv state.json && git commit -m "Posted cNNNN" && git push`.
10. Finish with a 2–3 line Hinglish summary: carousel number, format, products (ids + names), and the caption's first line.

## Caption rules
- Hinglish (Hindi-English mix), warm, premium, 150–220 words (long caption). Write it fresh for this carousel's category/theme — never copy a previous caption.
- Line 1: a hook about this category (e.g. earrings → "Kaan mein thoda sa sona, look mein poora royal touch ✨").
- A short 2–3 line story/paragraph: the feel of these pieces, kis occasion par pehnein (festive, shaadi, haldi/mehendi, office, date night, daily wear), kis outfit ke saath (saree, lehenga, kurti, western).
- A mini list of the 5 pieces with an emoji each, e.g. "1️⃣ Classic Ethnic Gold Earrings Combo" ... (names only, no prices).
- 1–2 styling tips or gifting line (birthday, anniversary, Karva Chauth, Diwali, etc. — match the season).
- Short trust line: "✨ Premium finish · Handpicked by Jewora".
- "👉 Swipe karke dekho aur apna favourite chuno"
- Must include: `💬 Comment "PRICE" aur hum turant DM mein price + details bhej denge!`
- "🚚 Free shipping all over India"
- 8–12 hashtags at the end: #Jewora #JeworaJewellery + category/theme tags (#Jhumka #KundanJewellery #FestiveJewellery #IndianJewellery #JewelleryLovers ...).
- Do NOT write prices, the website address, or product IDs in the caption.

## If something blocks
- No photos found in the first 60 candidates → run `python3 plan.py catalog.csv` again after appending those ids to a temporary skip (or pick the next category by bumping nothing) and report it.
- Windsor permission error → stop and report; do not record the products as posted.
