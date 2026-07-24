# Sermon Devotional Newsletter — WAT Project

Turn Rei's own sermon notes into a voice-matched daily devotional email he reads after his
morning devo. Built on the **WAT framework** (Workflows · Agent · Tools).

## The WAT layers

- **Workflows** (`workflows/`) — plain-language SOPs. `daily_devotional.md` is the recipe: notes in → devotional email out.
- **Agent** (Claude Code) — reads the workflow, extracts theme/summary/memory verse from the raw notes, writes the devotional **in Rei's voice**, then calls the tool to render it. Recovers from errors and improves the workflow.
- **Tools** (`tools/`) — deterministic Python. `render_newsletter.py` takes a structured edition JSON and emits branded HTML. No AI, no network — just templating.

## Sources of notes (in order of adoption)

1. **Primary (Day 2, active):** New daily notes live in **Notion** → Notion MCP retrieves them.
   Notion holds *new* notes only; the archive stays in the Church folder.
2. **Ask-pathway (still supported):** Rei pastes notes or requests a topic in chat → agent writes
   to `.tmp/` → builds the edition.
3. **Later:** Sunday-night recap pulls Potter's House Mandaluyong AM/PM preachings via
   `tools/fetch_sermon.sh` + `workflows/preaching_recap.md`.

**Source policy:** editions may be built from any pathway for Rei's personal reading, but anything
**publicized** (sent beyond Rei, posted, shared) must be sourced from **Rei's own sermon notes** —
never from fellowship resources or ask-pathway topics that aren't his material.

## Delivery

- **Live delivery model (2026-07-23):** each edition is drafted and **Rei reviews it**; once he approves, `tools/schedule_send.py` schedules it to auto-send at **6AM Manila** via **Resend** (`scheduled_at`, free tier — no cron/server). Human-in-the-loop by design: generation + approval stay manual; only the send is automated.
- **Standing authorization:** Rei granted standing 6AM auto-send 2026-07-23 — but **only for an edition he has approved**. Never schedule an unreviewed edition. No approved edition on a given day → nothing sends (empty days are skipped).
- This send path uses Resend (Rei's own inbox), not the Gmail `create_draft` MCP tool, so it doesn't touch the `gmail-mcp-safe-handling` write-side rule; Gmail stays a read/preview surface only.

See `ROADMAP.md` for the full future build-out.

## Voice

Write devotionals in **Rei's voice**, not sermon-report voice:
- Teaching-oriented, Scripture-anchored, one main thought per section.
- Occasional natural Taglish where it adds warmth ("masyadong kampante," "para makaahon").
- Earnest, direct, application-focused. Emphatic where he'd be emphatic.
- Faithful to the notes — never invent theology beyond what the notes contain.
- **Italics = a person talking.** Wrap first-person inner speech, decision-making, and specific illustrative examples in `<em>` — Abram's reasons, Sarai's thinking, the tempting inner monologue. This is a voice signature Rei likes; apply it consistently.
- **Italics also cover rhetorical self-questions** — "*what do I do when the leader is wrong?*" (Rei's 07-16 edit).
- **Taglish switches at clause level, never word level** — "profit for me o kung lugi ako", not "profit or lugi for me". A lone Tagalog word dropped into an English sentence reads fake; a natural clause switch reads like him.
- **Tagalog inside quotes must be grammatically natural** — draft it as a Tagalog speaker would say it, not translated word-by-word.
- **Capital-W "Word"** when referring to the preaching/Scripture.
- **Go easy on em-dashes** — Rei converts many of them to "but"/commas. One per sentence max as a default.

## Sensitivity

- Content sources are **Rei's own notes**. Fellowship resources (not his) are for **personal study only** while the audience is just Rei — revisit before anything goes public.
- **Never commit note content or generated editions.** `editions/`, `.tmp/`, and `.env` are gitignored. Content reaches Rei via Gmail, not via git.

## File layout

```
workflows/   # markdown SOPs
tools/       # deterministic Python renderers
editions/    # generated HTML + edition JSON (GITIGNORED)
.tmp/        # raw pasted notes (GITIGNORED, disposable)
.env         # only if a tool ever needs a key (MVP needs none — Gmail is via MCP)
```
