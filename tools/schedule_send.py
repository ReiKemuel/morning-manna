#!/usr/bin/env python3
"""Schedule an approved edition to auto-send at 6AM Manila via Resend.

Delivery layer for the human-in-the-loop daily model: the agent drafts and Rei
approves an edition in the evening; this tool hands the rendered HTML to Resend
with a `scheduled_at` time, and Resend holds it and sends it the next morning.
No cron, no server — Resend's free tier does the waiting. Generation stays local
(free, voice-matched); only the send is automated.

Usage:
    python3 tools/schedule_send.py editions/2026-07-24_thu.json      # → next 6AM Manila
    python3 tools/schedule_send.py editions/2026-07-24_thu.json --at "in 1 min"   # test
    python3 tools/schedule_send.py editions/2026-07-24_thu.json --now             # send now

Reads the edition's rendered `.html` sibling (run render_newsletter.py first) and
pulls the subject line from the edition JSON. Requires RESEND_API_KEY and MY_EMAIL
in the environment or in sermon-newsletter/.env (both gitignored — never committed).
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

MANILA = ZoneInfo("Asia/Manila")
RESEND_ENDPOINT = "https://api.resend.com/emails"
FROM = "Morning Manna <onboarding@resend.dev>"


def load_env() -> dict:
    """Read KEY=VALUE lines from sermon-newsletter/.env; os.environ wins."""
    import os
    env = {}
    dotenv = Path(__file__).resolve().parent.parent / ".env"
    if dotenv.exists():
        for line in dotenv.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    env.update({k: v for k, v in os.environ.items() if k in ("RESEND_API_KEY", "MY_EMAIL")})
    return env


def next_6am_manila(now: datetime | None = None) -> datetime:
    now = now or datetime.now(MANILA)
    target = now.replace(hour=6, minute=0, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target


def send(api_key: str, to: str, subject: str, html: str, scheduled_at: str | None) -> dict:
    payload = {"from": FROM, "to": [to], "subject": subject, "html": html}
    if scheduled_at:
        payload["scheduled_at"] = scheduled_at
    req = urllib.request.Request(
        RESEND_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "morning-manna/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise SystemExit(f"Resend send failed ({e.code}): {body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Resend send failed (network): {e.reason}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Schedule an edition to auto-send via Resend.")
    ap.add_argument("edition", help="path to the edition JSON (its .html sibling is sent)")
    ap.add_argument("--at", help='override schedule, e.g. "in 1 min" (test)')
    ap.add_argument("--now", action="store_true", help="send immediately (no scheduling)")
    ap.add_argument("--to", help="override recipient (defaults to MY_EMAIL)")
    args = ap.parse_args()

    src = Path(args.edition)
    edition = json.loads(src.read_text(encoding="utf-8"))
    html_path = src.with_suffix(".html")
    if not html_path.exists():
        raise SystemExit(f"missing render: {html_path} — run render_newsletter.py first")
    html = html_path.read_text(encoding="utf-8")

    env = load_env()
    api_key = env.get("RESEND_API_KEY")
    to = args.to or env.get("MY_EMAIL")
    if not api_key:
        raise SystemExit("RESEND_API_KEY not set (env or sermon-newsletter/.env)")
    if not to:
        raise SystemExit("MY_EMAIL not set (env or sermon-newsletter/.env), and no --to given")

    title = edition.get("title") or "Today's devotional"
    subject = f"Morning Manna — {title}"

    if args.now:
        scheduled_at, when = None, "now"
    elif args.at:
        scheduled_at, when = args.at, args.at
    else:
        target = next_6am_manila()
        scheduled_at, when = target.isoformat(), target.strftime("%a %Y-%m-%d 06:00 Manila")

    result = send(api_key, to, subject, html, scheduled_at)
    print(f"scheduled: {subject!r} → {to} @ {when}  (id: {result.get('id', '?')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
