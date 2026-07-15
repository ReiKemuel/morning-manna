# Workflow: Preaching → Edition (YouTube / Vimeo)

**Objective:** Turn a preaching video into a devotional edition at minimum token cost.
Use for services Rei has no notes for: Mandaluyong Sunday PM (YouTube) and the
Potter's House Prescott showcase (Vimeo, `https://vimeo.com/showcase/10231643`).

## The loop (per video)

1. **Fetch (one command, zero agent reasoning):**
   `sh tools/fetch_sermon.sh <video_url> <slug>` → writes `.tmp/<slug>.txt`
   — compact paragraphs, sparse `[mm:ss]` markers, ~5k words for a 50-min preaching.
   Subtitles are tried first (fast, both platforms); audio + local whisper is the
   automatic fallback (~15 min per hour of audio).
2. **Locate the preaching before reading.** Don't read the file top-to-bottom —
   the first 5–15 min are worship. `grep -n "chapter\|verse\|[Bb]ible" .tmp/<slug>.txt | head`
   or skim marker timestamps; then Read once from that offset.
3. **Write the edition JSON** (`workflows/daily_devotional.md` steps 2–3 — voice,
   structure, faithfulness rules all apply; never invent beyond what the transcript supports).
4. Render + voice-check + Gmail draft (daily_devotional.md steps 4–6).

## Finding videos

- **Vimeo showcase:**
  `.tools-cache/venv/bin/yt-dlp --flat-playlist --print "%(id)s" "https://vimeo.com/showcase/10231643"`
  then fetch `https://vimeo.com/<id>`. If a showcase video 403s, add `--referer "<showcase url>"`.
- **YouTube channel (Mandaluyong):** RSS is cheapest —
  `https://www.youtube.com/feeds/videos.xml?channel_id=UCxtr3bmWSPYeuRV6AFODTAw`
  (WebFetch it; gives titles + dates + IDs, no scraping).

## Edge cases / learnings (2026-07-15)

- **YouTube 429 on subtitles = transient rate-limit.** Retry later (or fall through
  to whisper) — don't rebuild the pipeline. PO-token provider is required and
  auto-bootstrapped into `.tools-cache/` on first YouTube run (needs node+npm+git).
- **Taglish preachings:** default sub priority delivers YouTube's English
  auto-translation — usually more usable than whisper-base Tagalog. For the
  original-language track, rerun with `--sub-langs fil,tl` manually.
- **Smoke tests:** `fetch_sermon.sh <url> <slug> 5` caps the whisper fallback at
  5 minutes. Openings are music — speech often starts past 08:00, so a tiny cap
  can legitimately produce an empty file.
- **Provenance:** these editions summarize *someone else's* preaching — keep the
  preacher + church named in the edition meta, personal-study use only while the
  audience is just Rei (CLAUDE.md → Sensitivity).
- **Never commit `.tmp/` or `.tools-cache/`** (both gitignored).
