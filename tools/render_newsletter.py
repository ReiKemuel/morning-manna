#!/usr/bin/env python3
"""Render a devotional edition JSON into a branded, email-safe HTML file.

Deterministic execution layer of the WAT framework — no AI, no network.
The agent writes the edition JSON; this tool only templates it.

Usage:
    python3 tools/render_newsletter.py editions/2026-07-12_am.json
    # writes editions/2026-07-12_am.html next to the JSON

Edition JSON schema:
{
  "title":    "Walking in Wisdom",
  "date":     "Sunday, January 4, 2026",
  "service":  "Sunday AM",
  "preacher": "Ptr. Juan Dela Cruz",             # optional
  "text":     "Proverbs 3:5-6",
  "big_idea": "One sentence that lands the whole message.",   # optional
  "intro":    "<p>...</p>",                      # HTML paragraphs
  "sections": [ {"heading": "...", "body": "<p>...</p>"} ],
  "memory_verse": {"ref": "Proverbs 3:5", "text": "Trust in the LORD..."},
  "application_prompt": "Where am I tempted to...",
  "previous_application": "Yesterday's application prompt",   # optional — renders a check-in
  "recent_verses": [ {"ref": "...", "text": "..."} ],         # optional — spaced-repetition recap
  "signoff": "Kaya today, walk His way."         # optional
}

Required fields fail loudly if missing/empty; a malformed edition never
renders half-empty. Optional brand override: tools/brand.json (same keys
as BRAND) reskins without touching this file.
"""
import html
import json
import sys
from pathlib import Path

# --- Branding (edit here to reskin the whole newsletter) ---------------------
BRAND = {
    "name": "Morning Manna",
    "tagline": "Sunday's message, carried into the week",
    "ink": "#212c3c",          # deep slate-navy — text
    "muted": "#6a798d",        # slate gray — meta
    "accent": "#3568b3",       # cornflower blue (corrected off the violet line)
    "accent_soft": "#e6edfb",  # airy cornflower tint — callout backgrounds
    "rule": "#dbe4f4",         # soft blue hairline
    "bg": "#eef2fb",           # cool cornflower paper
    "gold": "#b0863d",         # antique gold — masthead + sign-off contrast
    "card": "#ffffff",
    "font": "Georgia, 'Times New Roman', serif",
}

_brand_override = Path(__file__).with_name("brand.json")
if _brand_override.exists():
    BRAND.update(json.loads(_brand_override.read_text(encoding="utf-8")))

REQUIRED = ("title", "date", "service", "text", "intro",
            "sections", "memory_verse", "application_prompt")


def validate(edition: dict) -> None:
    missing = [k for k in REQUIRED if not edition.get(k)]
    mv = edition.get("memory_verse") or {}
    if "memory_verse" not in missing and not (mv.get("ref") and mv.get("text")):
        missing.append("memory_verse.ref/text")
    if "sections" not in missing and not all(
        s.get("heading") and s.get("body") for s in edition["sections"]
    ):
        missing.append("sections[].heading/body")
    if missing:
        raise SystemExit(f"edition invalid — missing/empty: {', '.join(missing)}")


def _p(text: str) -> str:
    """Allow simple pre-built HTML paragraphs, else wrap plain text."""
    text = text.strip()
    return text if text.startswith("<") else f"<p>{html.escape(text)}</p>"


def render(edition: dict) -> str:
    b = BRAND
    e = {k: edition.get(k, "") for k in
         ("title", "date", "service", "preacher", "text", "intro",
          "big_idea", "application_prompt", "previous_application", "signoff")}
    mv = edition.get("memory_verse", {})
    sections = edition.get("sections", [])
    recent_verses = edition.get("recent_verses", [])

    section_html = "".join(
        f"""
        <tr><td style="padding:22px 34px 0 34px;">
          <h2 style="margin:0 0 8px 0;font:600 18px {b['font']};color:{b['ink']};">{html.escape(s.get('heading',''))}</h2>
          <div style="font:16px/1.7 {b['font']};color:{b['ink']};">{_p(s.get('body',''))}</div>
        </td></tr>"""
        for s in sections
    )

    big_idea_html = ""
    if e["big_idea"]:
        big_idea_html = f"""
        <tr><td style="padding:16px 34px 0 34px;">
          <div style="border-left:3px solid {b['gold']};padding:2px 0 2px 14px;font:italic 17px/1.55 {b['font']};color:{b['ink']};">{html.escape(e['big_idea'])}</div>
        </td></tr>"""

    prev_app_html = ""
    if e["previous_application"]:
        prev_app_html = f"""
        <tr><td style="padding:18px 34px 0 34px;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background:{b['accent_soft']};border-radius:10px;">
            <tr><td style="padding:14px 20px;">
              <div style="font:600 11px/1.4 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:{b['accent']};">Last edition's application &mdash; how'd it go?</div>
              <div style="margin-top:6px;font:italic 14px/1.6 {b['font']};color:{b['muted']};">{html.escape(e['previous_application'])}</div>
            </td></tr>
          </table>
        </td></tr>"""

    recent_html = ""
    if recent_verses:
        rows = "".join(
            f"""<div style="margin-top:8px;font:14px/1.6 {b['font']};color:{b['ink']};">&ldquo;{html.escape(v.get('text',''))}&rdquo; <span style="font:600 13px {b['font']};color:{b['accent']};">&mdash; {html.escape(v.get('ref',''))}</span></div>"""
            for v in recent_verses
        )
        recent_html = f"""
        <tr><td style="padding:26px 34px 0 34px;">
          <div style="font:600 12px/1.4 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:{b['gold']};">Still carrying &mdash; this week's verses</div>
          {rows}
        </td></tr>"""

    verse_html = ""
    if mv:
        verse_html = f"""
        <tr><td style="padding:26px 34px 4px 34px;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background:{b['accent_soft']};border-radius:10px;">
            <tr><td style="padding:20px 24px;">
              <div style="font:600 12px/1.4 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:{b['accent']};">Memory Verse</div>
              <div style="margin-top:8px;font:italic 19px/1.6 {b['font']};color:{b['ink']};">&ldquo;{html.escape(mv.get('text',''))}&rdquo;</div>
              <div style="margin-top:8px;font:600 14px {b['font']};color:{b['accent']};">{html.escape(mv.get('ref',''))}</div>
            </td></tr>
          </table>
        </td></tr>"""

    app_html = ""
    if e["application_prompt"]:
        app_html = f"""
        <tr><td style="padding:26px 34px 4px 34px;">
          <table width="100%" cellpadding="0" cellspacing="0" style="border:1.5px dashed {b['rule']};border-radius:10px;">
            <tr><td style="padding:20px 24px;">
              <div style="font:600 12px/1.4 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:{b['muted']};">Application &mdash; write it down</div>
              <div style="margin-top:8px;font:16px/1.7 {b['font']};color:{b['ink']};">{html.escape(e['application_prompt'])}</div>
              <div style="margin-top:14px;border-bottom:1px solid {b['rule']};height:26px;"></div>
              <div style="margin-top:14px;border-bottom:1px solid {b['rule']};height:26px;"></div>
              <div style="margin-top:14px;border-bottom:1px solid {b['rule']};height:26px;"></div>
            </td></tr>
          </table>
        </td></tr>"""

    signoff_html = ""
    if e["signoff"]:
        signoff_html = f"""
        <tr><td style="padding:24px 34px 0 34px;font:italic 16px/1.6 {b['font']};color:{b['gold']};">{html.escape(e['signoff'])}</td></tr>"""

    meta_line = " &nbsp;·&nbsp; ".join(
        x for x in (e["service"], e["preacher"], e["text"]) if x
    )

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(e['title'])}</title></head>
<body style="margin:0;padding:0;background:{b['bg']};">
<table width="100%" cellpadding="0" cellspacing="0" style="background:{b['bg']};padding:28px 12px;">
<tr><td align="center">
  <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:{b['card']};border-radius:14px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06);">

    <tr><td style="padding:26px 34px 18px 34px;border-bottom:2px solid {b['gold']};">
      <div style="font:700 13px/1 Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:{b['gold']};">{html.escape(b['name'])}</div>
      <div style="margin-top:4px;font:13px Arial,sans-serif;color:{b['muted']};">{html.escape(b['tagline'])}</div>
    </td></tr>

    <tr><td style="padding:26px 34px 0 34px;">
      <div style="font:12px Arial,sans-serif;color:{b['muted']};">{html.escape(e['date'])}</div>
      <h1 style="margin:6px 0 4px 0;font:700 26px/1.25 {b['font']};color:{b['ink']};">{html.escape(e['title'])}</h1>
      <div style="font:13px Arial,sans-serif;color:{b['muted']};">{meta_line}</div>
    </td></tr>

    {big_idea_html}
    {prev_app_html}

    <tr><td style="padding:18px 34px 0 34px;font:16px/1.7 {b['font']};color:{b['ink']};">{_p(e['intro'])}</td></tr>

    {section_html}
    {verse_html}
    {app_html}
    {recent_html}
    {signoff_html}

    <tr><td style="padding:28px 34px 30px 34px;">
      <div style="border-top:1px solid {b['rule']};padding-top:16px;font:12px/1.6 Arial,sans-serif;color:{b['muted']};">
        Morning Manna &middot; your own notes, carried into the day.
      </div>
    </td></tr>

  </table>
</td></tr>
</table>
</body></html>"""


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: render_newsletter.py <edition.json>", file=sys.stderr)
        return 2
    src = Path(sys.argv[1])
    edition = json.loads(src.read_text(encoding="utf-8"))
    validate(edition)
    out = src.with_suffix(".html")
    out.write_text(render(edition), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
