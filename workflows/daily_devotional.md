# Workflow: Daily Devotional Email

**Objective:** Turn one set of sermon notes into a voice-matched devotional email Rei reads after his morning devo.

**Inputs:**
- Raw sermon notes (pasted by Rei, or later pulled from Notion/YouTube MCP).
- The service context (e.g. "Sunday AM", date, preacher, text).

**Steps:**
1. Save the raw notes to `.tmp/` (disposable). Never commit them.
2. Read the notes. Extract:
   - The **theme** (one line — what the message is really about).
   - A short **intro** that frames it.
   - 2–4 **sections** — the message's movements, rewritten as readable devotional prose in Rei's voice (see CLAUDE.md → Voice). Keep his Scripture references.
   - One **memory verse** — the single verse most worth carrying through the day.
   - An **application prompt** — a concrete question/step for Rei to fill in.
3. Assemble a structured edition JSON (schema in `tools/render_newsletter.py`).
4. Run `python3 tools/render_newsletter.py editions/<slug>.json` → produces `editions/<slug>.html`.
5. Voice-check the prose before delivery — "does this sound like Rei would say it?" If not, revise, don't ship.
6. Deliver as a **Gmail draft** (never auto-send without explicit standing authorization).

**Edge cases / learnings:**
- Notes are outline-form (I/II/III, A/B/C). Convert to prose; don't paste the outline verbatim.
- If a note has no clean single verse, pick the one the message hinges on.
- Keep the Application block genuinely fillable — a prompt, not a lecture.
