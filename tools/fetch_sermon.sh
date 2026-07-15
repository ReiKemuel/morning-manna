#!/bin/sh
# One command: preaching URL -> compact transcript at .tmp/<slug>.txt
#
#   tools/fetch_sermon.sh <video_url> <slug> [max_minutes]
#
# Works on Vimeo (subtitles direct — fast) and YouTube (audio + local whisper
# fallback, ~15 min per hour of audio). max_minutes caps whisper for smoke tests.
# First run bootstraps a cached venv (+ PO-token provider for YouTube) into
# .tools-cache/ (gitignored). Requires python3; node+npm+git for YouTube.
#
# Vimeo notes: showcase pages list videos —
#   yt-dlp --flat-playlist --print "%(id)s" "https://vimeo.com/showcase/<id>"
# then fetch each as https://vimeo.com/<id>. If a video 403s, retry with
# --referer "<showcase url>".
set -e
cd "$(dirname "$0")/.."
URL="$1"; SLUG="$2"; MAXMIN="$3"
[ -n "$URL" ] && [ -n "$SLUG" ] || { echo "usage: fetch_sermon.sh <url> <slug> [max_minutes]" >&2; exit 2; }

CACHE=".tools-cache"; VENV="$CACHE/venv"; YTDLP="$VENV/bin/yt-dlp"; PY="$VENV/bin/python3"
mkdir -p "$CACHE" .tmp

if [ ! -x "$YTDLP" ]; then
  echo "bootstrapping venv (first run)..." >&2
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q yt-dlp curl_cffi faster-whisper bgutil-ytdlp-pot-provider
fi

POT_ARGS=""
case "$URL" in
  *youtube.com*|*youtu.be*)
    BGUTIL="$CACHE/bgutil-ytdlp-pot-provider"
    if [ ! -f "$BGUTIL/server/build/generate_once.js" ]; then
      echo "building PO-token provider (first run, needs node+npm)..." >&2
      git clone -q --depth 1 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git "$BGUTIL"
      (cd "$BGUTIL/server" && npm install --silent && npx tsc)
    fi
    POT_ARGS="--extractor-args youtubepot-bgutilscript:script_path=$PWD/$BGUTIL/server/build/generate_once.js"
    ;;
esac

rm -f "$CACHE/$SLUG".*.vtt
# Cheap path first: platform subtitles (works on Vimeo; YouTube blocks ASR subs as of 2026-07)
"$YTDLP" --skip-download --ignore-no-formats-error --write-subs --write-auto-subs \
  --sub-langs "en-x-autogen,en-orig,en,fil,tl" --sub-format vtt \
  --impersonate chrome --js-runtimes node $POT_ARGS \
  -o "$CACHE/$SLUG" "$URL" >&2 || true

VTT=$(ls "$CACHE/$SLUG".*.vtt 2>/dev/null | head -1 || true)
if [ -n "$VTT" ]; then
  "$PY" tools/compact_vtt.py "$VTT" ".tmp/$SLUG.txt"
else
  echo "no subtitles available — audio + whisper fallback" >&2
  "$YTDLP" -f bestaudio --impersonate chrome --js-runtimes node $POT_ARGS \
    -o "$CACHE/$SLUG.audio.%(ext)s" "$URL" >&2
  AUDIO=$(ls "$CACHE/$SLUG".audio.* | head -1)
  "$PY" tools/transcribe_sermon.py "$AUDIO" ".tmp/$SLUG.txt" $MAXMIN
fi

rm -f "$CACHE/$SLUG".*.vtt "$CACHE/$SLUG".audio.*
wc -w ".tmp/$SLUG.txt"
