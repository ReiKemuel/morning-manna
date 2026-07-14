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
| Sun PM (~9pm) | Potter's House Mandaluyong AM & PM preachings, pulled + summarized via YouTube MCP |

## Build-out (mapped to the challenge)

- **Note source → Notion (Day 2).** New daily notes live in Notion; Notion MCP retrieves them. Notion holds *new* notes only — the archive stays in the Church folder. (No 2019 backfill into Notion.)
- **Voice + format → a reusable Skill (Day 3).** Freeze the voice signatures (incl. the italics-for-inner-speech rule) and the layout so every edition is consistent.
- **Collapsible web version (Day 5).** Email can't do `<details>`; a hosted page can. Each section becomes an expand/collapse panel (teaser → full text). The email links to it with "Read the full devotional →".
- **Scheduled AM send (Day 6).** Scheduled task fires the approved edition; requires the note source to be machine-readable first (depends on Day 2).
- **Executive-assistant integration (Day 7).** Morning Manna becomes one routine inside a broader daily EA.

## Efficiency / engineering (down the road)

- Push more logic into deterministic **Python tools** and tighten the **WAT** separation (agent reasons, tools execute) so daily runs are cheap and predictable.
- Voice corpus: one-time migrate past OneNote notes → Church folder as an archive + voice sample (decoupled from the newsletter; not a blocker).
- Fellowship-resource editions (Fri/Sat) are a **different mode** — summarizing others' material. Personal-study use only while the audience is just Rei; revisit before anything goes public.
