# Morning Manna — Ideas for a Better Newsletter

Unvetted suggestions to pull from later. (ROADMAP.md = committed plan; this = the idea pool.)

## Highest-value (my top picks)

1. **Memory-verse spaced repetition.** Footer reviews *last few days'* memory verses, not just today's. Turns the daily habit into actual Scripture memorization — the single feature most aligned with the point of the whole thing.
2. **"Yesterday's application — how'd it go?" callback.** Each morning opens by echoing yesterday's Application prompt as a one-line check-in. Creates continuity and gently holds Rei accountable to the step he wrote.
3. **One-line Big Idea / TL;DR at the top.** The theme distilled to a single sentence, above the sections — so even a 20-second skim lands the point.

## Structure / content

4. Reading-time badge ("2 min read") + a warm greeting ("Good morning").
5. A short **prayer prompt** alongside the Application (pray it, then write it).
6. **Scripture links** — verse refs link out to bible.com/YouVersion (email-safe, no offline dependency).
7. **Bilingual verse** — memory verse in English + Tagalog, matching the natural Taglish voice.
8. Weekly (Sun AM) edition that **threads the week's themes** into one arc, not just a list.

## Design / delivery

9. **Dark-mode email variant** (some clients honor it) — softer for very early / late reading.
10. Optional **hero verse-art** per theme (the "Nano Banana" image idea) — only if it stays tasteful, never clip-arty.
11. **Audio version** (TTS) link down the road — listen during the commute / devo.
12. When public: subject-line variants for open rates, a "share this" footer, alt text + semantic structure for accessibility.

## Brand / identity

- **⭐ REMINDER (Rei asked to be reminded): make a wordmark/logo for Morning Manna.** A simple typographic mark, not clip art — likely gold-on-cornflower to match the palette. Optional personalization: a "rei ·" prefix or "from rei" touch. Natural fit for the Day 5 (website/brand) build.
- Palette locked: **Cornflower blue** (`#3d63b0`) + **antique gold** (`#b0863d`) contrast — gold treatment TBD (see palette artifact).

## Engineering

13. Move theme/verse extraction into a small **Python step** with a schema check, so a malformed edition fails loudly instead of rendering half-empty (tighter WAT).
14. A tiny **palette/config file** so reskinning never touches the renderer code.
