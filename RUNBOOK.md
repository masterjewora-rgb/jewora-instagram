# Jewora Instagram Posting — runbook (one post per run)

Each run posts ONE post: a 5-slide carousel OR a Reel (see "Reel or carousel?") to Instagram account **jewora_official** (Windsor connector `instagram`, account `17841475914389502`).
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

## Reel or carousel?
Check the current time in India (Asia/Kolkata). Runs in the **10:xx** or **15:xx** IST hour make a **carousel**; every other run makes a **Reel**.
(Daily 10 posts = 8 Reels + 2 carousels: 09:50 Reel, 10:50 carousel, 11:50 Reel, 12:50 Reel, 13:50 Reel, 15:50 carousel, 17:50 Reel, 18:50 Reel, 19:50 Reel, 20:50 Reel.)
The COMMENT "PRICE" button is drawn big on every slide/frame (formats.py `.cta`, reel_styles.py `cta()`); keep it big when changing layouts.

### Reel steps (replace steps 6–9)
6r. `python3 reel.py ID1 ID2 ID3 ID4 ID5` (style comes from plan.json `reel_style`, rotates through 12 styles; music rotates through music/ — the user's tracks from Drive folder `1tpsn8KwB1vchgkAcREwg49Jo69r3IFpm`).
    Before rendering: list that Drive folder; for any audio file whose name is not yet in music/ (names are lowercased with _), download it and run `python3 add_music.py <result files>`, then commit music/.
    Check 1–2 frames: `ffmpeg -ss 4 -i reels/rNNNN/reel.mp4 -frames:v 1 /tmp/f.jpg` and Read it.
7r. `git add reels && git commit -m "Reel rNNNN" && git push`, wait ~30 s.
8r. Windsor `execute_action`: connector `instagram`, account `17841475914389502`, action `create_video_post`,
    params `{"video_url": "<reel.mp4 url>", "cover_url": "<cover.jpg url>", "share_to_feed": true, "caption": "..."}` (Reel caption: same rules as below).
    If Instagram rejects the video, fall back: run `python3 make_carousel.py` with the same 5 ids, push, and post it as a carousel instead (then record normally).
9r. On success `python3 record.py <media_id>` (it knows it was a reel from current.json), push posted.csv + state.json.

## Caption rules
- **English only**, warm and premium, **80–120 words** (medium length). Write it fresh for this post's category/theme — never copy a previous caption.
- Line 1: a short hook about this category (e.g. earrings → "A little gold, a whole lot of glow ✨").
- 1–2 lines on the pieces: the feel, the occasion (festive, weddings, office, date night, everyday) and what to pair them with (saree, lehenga, kurta, western).
- A compact list of the 5 pieces, one per line with a number emoji, e.g. "1️⃣ Classic Ethnic Gold Earrings Combo" (names only, no prices).
- Optional one-line gifting or styling tip that matches the season.
- "👉 Swipe to find your favourite" (for a Reel: "👀 Watch till the end and pick your favourite")
- Must include: `💬 Comment "PRICE" and we'll DM you the price + details instantly!`
- "🚚 Free shipping across India"
- 8–10 hashtags at the end: #Jewora #JeworaJewellery + category/theme tags (#Jhumka #KundanJewellery #FestiveJewellery #IndianJewellery #JewelleryLovers ...).
- Do NOT write prices, the website address, or product IDs in the caption.

## If something blocks
- No photos found in the first 60 candidates → run `python3 plan.py catalog.csv` again after appending those ids to a temporary skip (or pick the next category by bumping nothing) and report it.
- Windsor permission error → stop and report; do not record the products as posted.
