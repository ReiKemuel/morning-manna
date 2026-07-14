# Sermon Devotional Newsletter — WAT Project

Turn Rei's own sermon notes into a voice-matched daily devotional email he reads after his
morning devo. Built on the **WAT framework** (Workflows · Agent · Tools).

## The WAT layers

- **Workflows** (`workflows/`) — plain-language SOPs. `daily_devotional.md` is the recipe: notes in → devotional email out.
- **Agent** (Claude Code) — reads the workflow, extracts theme/summary/memory verse from the raw notes, writes the devotional **in Rei's voice**, then calls the tool to render it. Recovers from errors and improves the workflow.
- **Tools** (`tools/`) — deterministic Python. `render_newsletter.py` takes a structured edition JSON and emits branded HTML. No AI, no network — just templating.

## Sources of notes (in order of adoption)

1. **MVP (now):** Rei pastes a week's notes into chat → agent writes them to `.tmp/` → builds the edition.
2. **Day 2:** New daily notes live in **Notion** → Notion MCP retrieves them.
3. **Later:** Sunday-night recap pulls Potter's House Mandaluyong AM/PM preachings via YouTube MCP.

## Delivery

- Output is a **Gmail draft** by default. **Never auto-send without Rei's explicit standing authorization** for this specific automation (see the hub's `gmail-mcp-safe-handling` rule).
- **Target delivery model:** each evening the next morning's edition is drafted and Rei reviews it; once he approves, it's scheduled to send the next AM. Human-in-the-loop by design — keeps the Gmail-safety rule intact even when running daily.
- The 6AM daily send (Day 6, scheduled task) is a standing pre-authorization Rei grants once he trusts the output.

See `ROADMAP.md` for the full future build-out.

## Voice

Write devotionals in **Rei's voice**, not sermon-report voice:
- Teaching-oriented, Scripture-anchored, one main thought per section.
- Occasional natural Taglish where it adds warmth ("masyadong kampante," "para makaahon").
- Earnest, direct, application-focused. Emphatic where he'd be emphatic.
- Faithful to the notes — never invent theology beyond what the notes contain.
- **Italics = a person talking.** Wrap first-person inner speech, decision-making, and specific illustrative examples in `<em>` — Abram's reasons, Sarai's thinking, the tempting inner monologue. This is a voice signature Rei likes; apply it consistently.

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
