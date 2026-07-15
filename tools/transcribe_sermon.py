#!/usr/bin/env python3
"""Transcribe sermon audio locally with faster-whisper, output compact paragraphs.

Fallback path for platforms whose caption downloads are blocked (YouTube, as of
2026-07: ASR captions require PO tokens even with the bgutil provider). Output
format matches compact_vtt.py: ~700-char paragraphs, sparse [mm:ss] markers.

Usage: transcribe_sermon.py <audio> <out.txt> [max_minutes]
(max_minutes caps the run for smoke tests; omit for a full sermon.)
Budget: roughly 15 min per hour of audio on this Mac (base model, int8, CPU).
"""
import sys
from pathlib import Path

from faster_whisper import WhisperModel


def main() -> int:
    audio, out = sys.argv[1], Path(sys.argv[2])
    max_sec = float(sys.argv[3]) * 60 if len(sys.argv) > 3 else None

    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio, vad_filter=True, beam_size=1)
    print(f"language={info.language} p={info.language_probability:.2f} "
          f"duration={info.duration:.0f}s", file=sys.stderr)

    paras, buf, start = [], [], 0
    for seg in segments:
        if max_sec and seg.start > max_sec:
            break
        text = seg.text.strip()
        if not text:
            continue
        if not buf:
            start = int(seg.start)
        buf.append(text)
        if sum(len(x) + 1 for x in buf) > 700:
            paras.append(f"[{start // 60:02d}:{start % 60:02d}] " + " ".join(buf))
            buf = []
    if buf:
        paras.append(f"[{start // 60:02d}:{start % 60:02d}] " + " ".join(buf))

    out.write_text("\n\n".join(paras) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(paras)} paragraphs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
