#!/usr/bin/env python3
"""Generate an image via Kie.ai (Nano Banana 2 Lite by default).

Deterministic WAT tool: createTask -> poll recordInfo -> download result.
No AI reasoning here; the agent supplies the prompt.

Usage:
  python3 tools/generate_image.py --prompt "..." --out branding/logo_v1.png \
      [--model nano-banana-2-lite] [--aspect 1:1] [--image-url https://... ...]

Lite input schema (per official docs): prompt, aspect_ratio, optional image_urls (max 10).

Auth: KIE_API_KEY env var, or KIE_API_KEY=... line in this repo's .env (gitignored).
Result URLs expire after 24h — this tool always downloads immediately.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

API_BASE = "https://api.kie.ai/api/v1/jobs"


def load_api_key():
    key = os.environ.get("KIE_API_KEY")
    if key:
        return key.strip()
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            if line.strip().startswith("KIE_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"')
    sys.exit("ERROR: KIE_API_KEY not found (env var or sermon-newsletter/.env)")


def api(url, key, payload=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST" if payload else "GET",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt")
    p.add_argument("--out", required=True)
    p.add_argument("--model", default="nano-banana-2-lite")
    p.add_argument("--aspect", default="1:1")
    p.add_argument("--image-url", action="append", default=[],
                   help="reference image URL (repeatable, max 10)")
    p.add_argument("--timeout", type=int, default=240)
    p.add_argument("--task-id", help="resume an existing task instead of creating one")
    args = p.parse_args()

    if not args.task_id and not args.prompt:
        p.error("--prompt is required unless --task-id is given")
    key = load_api_key()
    if args.task_id:
        task_id = args.task_id
        print(f"resuming task {task_id}; polling...")
    else:
        input_obj = {"prompt": args.prompt, "aspect_ratio": args.aspect}
        if args.image_url:
            input_obj["image_urls"] = args.image_url
        resp = api(f"{API_BASE}/createTask", key, {
            "model": args.model,
            "input": input_obj,
        })
        if resp.get("code") != 200:
            sys.exit(f"ERROR createTask: {json.dumps(resp)}")
        task_id = resp["data"]["taskId"]
        print(f"task {task_id} created; polling...")

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        time.sleep(4)
        info = api(f"{API_BASE}/recordInfo?taskId={task_id}", key)
        state = info.get("data", {}).get("state")
        if state == "success":
            result = json.loads(info["data"]["resultJson"])
            url = result["resultUrls"][0]
            os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
            # result CDN 403s python's default UA and truncates urllib reads; curl is reliable
            subprocess.run(
                ["curl", "-sS", "--retry", "3", "-A", "Mozilla/5.0", "-o", args.out, url],
                check=True,
            )
            credits = info["data"].get("creditsConsumed")
            print(f"saved {args.out} (credits: {credits})")
            return
        if state == "fail":
            sys.exit(f"ERROR task failed: {info['data'].get('failCode')} {info['data'].get('failMsg')}")
        print(f"  state={state}")
    sys.exit("ERROR: timed out waiting for task")


if __name__ == "__main__":
    main()
