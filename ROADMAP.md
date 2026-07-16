# Morning Manna — Roadmap

MVP shipped: notes → voice-matched devotional → branded HTML → Gmail draft, via the WAT framework.
Everything below is the intended build-out. Sequenced against Nate Herk's 7-Day AIS Challenge where it lines up.

## Delivery model (target)

Human-in-the-loop daily: **each evening** the next morning's edition is drafted and reviewed; once
approved it's **scheduled to send the next AM**. Keeps the Gmail-safety rule intact even at daily cadence.

## The weekly drip (each day pulls a different source)

| Day | Edition |
|-----|---------|
| Mon | Yesterday's **Sunday AM** notes |
| Tue | **Sunday PM** notes |
| Wed | Last **Wednesday** service |
| Thu | **Sunday School** notes |
| Fri | Random pick from resources / a book currently being read |
| Sat | Random pick again (or Friday's chosen interest) |
| Sun AM | **Week-in-summary** newsletter |
| Sun PM (~9pm) | Potter's House Mandaluyong AM & PM preachings — **unlocked early**: `tools/fetch_sermon.sh` + `workflows/preaching_recap.md` (works for Vimeo/Prescott showcase too) |

## Build-out (mapped to the challenge)

- **Note source → Notion (Day 2).** New daily notes live in Notion; Notion MCP retrieves them. Notion holds *new* notes only — the archive stays in the Church folder. (No 2019 backfill into Notion.)
- **Voice + format → a reusable Skill (Day 3).** Freeze the voice signatures (incl. the italics-for-inner-speech rule) and the layout so every edition is consistent.
- **Collapsible web version (Day 5).** Email can't do `<details>`; a hosted page can. Each section becomes an expand/collapse panel (teaser → full text). The email links to it with "Read the full devotional →".
- **Scheduled AM send (Day 6).** Scheduled task fires the approved edition; requires the note source to be machine-readable first (depends on Day 2).
- **Executive-assistant integration (Day 7).** Morning Manna becomes one routine inside a broader daily EA.

## Branding & visuals (added 2026-07-16)

- **Logo (in progress):** blue + beige, generated via Kie.ai Nano Banana 2 Lite —
  `branding/logo-brief.md` (5 concepts) + `tools/generate_image.py` (createTask → poll → download).
  Blocked on `KIE_API_KEY` in `.env`.
- **Per-edition infographics** (bottom-of-newsletter visual summary and/or table-of-contents card).
  Two candidate routes:
  1. **Kie.ai Nano Banana 2 Lite** — reuse `tools/generate_image.py`; agent condenses the edition
     into an infographic prompt (title, 3-4 points, memory verse). ~$0.03/image, no daily cap,
     brand-colored. Risk: rendered text accuracy — keep text short, verify each render.
  2. **NotebookLM MCP** (e.g. `roomi-fields/notebooklm-mcp`) — free, source-grounded, 2026 styles;
     but free tier = **3 infographics/day**, needs a third-party MCP server driving Rei's Google
     account, and output style is NotebookLM's, not the newsletter brand.
  Default plan: start with route 1 (already tooled, on-brand); try route 2 as a free A/B once the
  MCP is vetted.
- **Embedding constraint (RESOLVED 07-16):** data-URI images get stripped by Gmail's compose
  editor on edit/send (confirmed — the Thursday edition went out logo-less). Use the Gmail MCP's
  **inline attachment (CID)** support for the masthead + future infographics. Editions stay
  gitignored, so repo-hosting remains off the table for content-bearing images.

## Efficiency / engineering (down the road)

- Push more logic into deterministic **Python tools** and tighten the **WAT** separation (agent reasons, tools execute) so daily runs are cheap and predictable.
- Voice corpus: one-time migrate past OneNote notes → Church folder as an archive + voice sample (decoupled from the newsletter; not a blocker).
- Fellowship-resource editions (Fri/Sat) are a **different mode** — summarizing others' material. Personal-study use only while the audience is just Rei; revisit before anything goes public.
