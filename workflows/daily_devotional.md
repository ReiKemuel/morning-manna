# Workflow: Daily Devotional Email

**Objective:** Turn one set of sermon notes into a voice-matched devotional email Rei reads after his morning devo.

**Inputs:**
- Raw sermon notes — **primary: Notion** (Day 2, live 2026-07-16); fallback: pasted by Rei.
- The service context (e.g. "Sunday AM", date, preacher, text) — in Notion notes this is the
  first line of the page (date, preacher, text refs).

**Steps:**
0. **Notion retrieval (primary):** `notion-search` for the "Sermon Notes" page (top-level page;
   one child page per sermon, titled by message title). Pick the child by date/title for the
   edition being built, `notion-fetch` it. Notes are tab-indented outline bullets with `###`
   section heads; italics in the notes are often already inner-speech/creative-imagination —
   carry them into the edition's `<em>` treatment. (Page IDs stay out of this repo — search by
   title each time; it's cheap.)
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
6. **Deliver — review, then schedule the 6AM auto-send** (target model, live 2026-07-23):
   - **a. Review.** Rei reads the rendered `editions/<slug>.html` (or a Gmail preview draft) and approves. Generation stays human-in-the-loop; nothing sends unreviewed.
     - Gmail preview note: the `create_draft` MCP tool takes `htmlBody` **inline** (no file-path arg), and the ~30KB base64 masthead can't be hand-transcribed into a tool arg reliably — render a **logo-off compact body** for the draft (`import render_newsletter; render_newsletter.BRAND['logo_file']=''`, then `render(edition)`), keeping the on-disk `.html` with the image.
   - **b. Schedule.** Once approved, run `python3 tools/schedule_send.py editions/<slug>.json` → hands the rendered HTML to **Resend** with `scheduled_at` = next 6AM Manila. Resend holds and sends it (free tier; no cron/server). **Standing 6AM auto-send authorized 2026-07-23** — only for an edition Rei has approved. `--at "in 1 min"` / `--now` for testing.
   - **Skip empty days:** no approved edition → nothing sends. (daily-verse retired 2026-07-23 — redundant with the memory verse.)
   - Needs `RESEND_API_KEY` + `MY_EMAIL` in `.env` (gitignored). Masthead is a data-URI — confirm it renders in Gmail via Resend; CID-inline is still the queued upgrade.

**Edge cases / learnings:**
- Notes are outline-form (I/II/III, A/B/C). Convert to prose; don't paste the outline verbatim.
- If a note has no clean single verse, pick the one the message hinges on.
- Keep the Application block genuinely fillable — a prompt, not a lecture.
