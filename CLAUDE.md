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

- **Live delivery model (2026-07-23, retimed to 5AM 2026-08-06):** each edition is drafted and **Rei reviews it**; once he approves, `tools/schedule_send.py` schedules it to auto-send at **5AM Manila** via **Resend** (`scheduled_at`, free tier — no cron/server). Human-in-the-loop by design: generation + approval stay manual; only the send is automated.
- **Standing authorization:** Rei granted standing auto-send 2026-07-23 (**5AM** as of 2026-08-06) — but **only for an edition he has approved**. Never schedule an unreviewed edition. No approved edition on a given day → nothing sends (empty days are skipped).
- **The send is irreversible.** The `RESEND_API_KEY` is send-only — `GET` and `PATCH` on `/emails/:id` both return **403** (verified 2026-08-06). A queued edition cannot be cancelled or rescheduled. Consequence: **never queue more than a few days ahead** while voice or content is still being tuned, because a correction cannot reach an edition already in Resend. Upgrading to a full-access key is the fix and is an open item.
- **Every send is logged** to `editions/.send_log.jsonl` (gitignored) by `schedule_send.py` itself — slug, Resend id, scheduled time, subject. It is the only record of what is queued.
- **Batch scheduling needs an explicit `--at` per edition** (full ISO, e.g. `--at "2026-08-09T05:00:00+08:00"`). The bare default resolves to the *next* 5AM on every call, so a loop without `--at` stacks the entire queue onto one morning.
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

### GOAL: simple and actionable, never clever (Rei, 2026-08-06)

Rei's correction on the first 10-edition queue: **"don't try to sound TOO SMARTASS and ALLKNOWING —
true genius lies in making simple and actionable steps."** The failure mode is an edition that
*comments on* the sermon instead of delivering it. This governs everything below it.

- **Never narrate or admire the message.** Cut every "the message said / gave / named / stacked /
  pulled the word apart," "here's the part that…," "an illustration I won't forget," "worth sitting
  with," "reading it, I noticed," "that reframing does something to…". Just say the thing. His own
  notes never praise themselves.
- **Two short paragraphs per section, not one dense block.** Target **≤110 words per section body**;
  break at the turn from doctrine to application. The first queue ran 175–197 words in single blocks
  and that is what read as lecturing.
- **Short sentences, one idea each.** Three commas plus a subordinate clause is an essay sentence,
  not his.
- **No literary aphorisms.** "It is power that has an owner" is a writer being clever. Prefer the
  plain statement plus his own household illustration, which is already concrete.
- **Every edition ends in `steps`** — 2–3 numbered, concrete, doable before lunch. `application_prompt`
  names the ONE thing to identify; `steps` say what to physically do (write it, call them, set the
  alarm, go to that person). At least one step is normally Taglish.
- The renderer supports an optional `steps` array, rendered as a **DO THIS TODAY** block inside the
  application box. Editions without it render unchanged.

### Signatures re-derived from the raw notes (2026-08-05)

Read off four of Rei's own Notion notes (`God's Spirit Working In You`, `It Would Take A Lifetime`,
`Created To Become Like Christ III`, the 08-05 Matthew 24 message). These are what his *own* writing
does, so an edition that does them reads like him:

- **ALL-CAPS is the hammer, and he swings it once.** "IT IS HIS OWN WILL" · "it is ALREADY too late" ·
  "NO, you have to buy FOR YOURSELVES" · "SOME DAY is never promised" · "MASTER YOUR fleshly impulses."
  It lands on the *consequence*, never on the concept. **At most one per section**, or it stops meaning anything.
- **Coined contrast-compounds.** "humanBEINGS, not humanDOINGS" · "Beautiful + Attitudes" · "spiritually
  married to it." He fuses or splits a word to make a pair stick. Reuse his coinages; don't manufacture new ones.
- **Household illustrations, never abstract analogy.** Hair growing where nobody hears it · a chair you
  trust your whole weight to without thinking · everyone building pillars with their own elbow for a ruler ·
  roots underground vs. the leaves everyone sees · reaching for the phone, FB, Gmail before the Bible.
- **The application is a self-audit question, not advice.** Not "pray more," but "*when we're alone at the
  mercy of our leisure, what eats up our time?*" First/second person, italicised, answerable before lunch.
- **Doctrine → "so"/"therefore" → a decision.** Every movement lands on a choice, never on a feeling.
- **Inclusive "we/us/our."** He preaches from inside the room, not above it. Second-person "you should" is off-voice.
- **Three or four quick probes in a row.** In the notes they're slash-stacked ("what takes most of our time/
  what's prioritized/ what's easily let go of"); in an edition they become a comma series, but keep the rhythm.
- **Tagalog carries the convicting or tender beat; English carries the doctrine.** Consistent in all four notes.
  The Tagalog is a whole sentence or clause and is usually the illustration or the gentle warning.

#### GOAL: write Taglish, never translated Tagalog (Rei, 2026-08-05)

Rei's standing correction: a clean, fully-Tagalog sentence at the end of a section reads like English run
through Google Translate. **Real Taglish is the target — the way he actually talks.** What his own notes do:

- **English abstract and technical nouns stay in English**, inside a Tagalog sentence: *character, destiny,
  habits, prayer, signs, standardized measurement, situations, duties, reputation.* Do not hunt for the
  Tagalog equivalent — reaching for "palatandaan" when he'd say "signs" is the tell.
- **English verbs take Tagalog affixes.** His own: *magde-determine, ma-practice, na-eenganyo, ma-learn,
  nag-promise, magte-tempt, na-prioritize.* This is the single strongest signal of natural code-switching.
- **The switch lands mid-sentence, both directions.** "The Bible compares our growth *sa iba't ibang mga
  antas* ng paglago ng puno" · "love would hinder us *sa pag-tsismis sa iba*" · "uunahin ang Diyos, Bible,
  prayer, *instead na* ang cellphone, FB, gmail."
- **English discourse glue inside Tagalog:** *instead na, one day, after ng, kaya, pero, so.*
- **Tagalog discourse glue inside English:** *Bakit?* rather than "Why?" when the next line is Tagalog.
- **Contractions and casual forms**: *wag* over *huwag*, *'to* over *ito*, *barkada*, *exact na araw*.

**The test before shipping any Tagalog line:** could this sentence be produced by translating an English
sentence word-for-word? If yes, it is wrong — rewrite it until at least one English word is carrying its
own weight inside it. Sign-offs especially: the approved 08-02 sign-off is Taglish
("Isa lang ang may pangako ng *they shall be filled*"), not pure Tagalog.
- **Notes register ≠ edition register.** His raw notes are dash-heavy; his *edits to editions* convert those
  dashes to "but"/commas. Match the edited editions, not the notes, on punctuation.

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
