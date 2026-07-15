#!/usr/bin/env python3
"""Compact a WebVTT subtitle file into token-efficient paragraphs.

Strips cue numbers/timestamps, dedupes rolling-caption repeats (YouTube style),
merges text into ~700-char paragraphs, and prefixes each paragraph with one
sparse [mm:ss] marker so the agent can locate the preaching section by grep
instead of reading everything twice.

Usage: compact_vtt.py <in.vtt> <out.txt>
"""
import re
import sys
from pathlib import Path

TS = re.compile(r"(\d+):(\d\d):(\d\d)\.\d+\s+-->")
TAG = re.compile(r"<[^>]+>")


def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    cues = []  # (seconds, text)
    t = 0
    for line in src.read_text(encoding="utf-8").splitlines():
        m = TS.match(line.strip())
        if m:
            t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            continue
        text = TAG.sub("", line).strip()
        if not text or text == "WEBVTT" or text.isdigit() or ":" in text[:6]:
            continue
        if cues and (text == cues[-1][1] or text in cues[-1][1]):
            continue  # rolling-caption repeat
        cues.append((t, text))

    paras, buf, start = [], [], 0
    for sec, text in cues:
        if not buf:
            start = sec
        buf.append(text)
        if sum(len(x) + 1 for x in buf) > 700:
            paras.append(f"[{start // 60:02d}:{start % 60:02d}] " + " ".join(buf))
            buf = []
    if buf:
        paras.append(f"[{start // 60:02d}:{start % 60:02d}] " + " ".join(buf))

    out.write_text("\n\n".join(paras) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(paras)} paragraphs, {sum(len(p) for p in paras)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
