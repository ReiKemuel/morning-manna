#!/usr/bin/env python3
"""Key a white background out of flat logo art -> transparent PNG.

Deterministic WAT tool. Assumes art was generated on pure/near-white.
Computes alpha from pixel whiteness, then un-blends the foreground color
so anti-aliased edges carry no white fringe. Crops to content + margin.

Usage: python3 tools/make_transparent.py in.jpg out.png [--margin 24]
"""

import argparse
import sys

from PIL import Image


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--margin", type=int, default=24)
    p.add_argument("--w-lo", type=float, default=0.78,
                   help="whiteness below this -> fully opaque")
    p.add_argument("--w-hi", type=float, default=0.97,
                   help="whiteness above this -> fully transparent")
    p.add_argument("--sat-tol", type=int, default=24,
                   help="channel spread above this -> pixel is colored, keep opaque")
    args = p.parse_args()
    W_LO, W_HI = args.w_lo, args.w_hi

    img = Image.open(args.src).convert("RGB")
    px = img.load()
    out = Image.new("RGBA", img.size)
    po = out.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) > args.sat_tol:
                po[x, y] = (r, g, b, 255)
                continue
            w = min(r, g, b) / 255.0
            a = (W_HI - w) / (W_HI - W_LO)
            a = max(0.0, min(1.0, a))
            if a == 0:
                po[x, y] = (0, 0, 0, 0)
                continue
            # un-blend: c = a*fg + (1-a)*255  =>  fg = (c - (1-a)*255) / a
            fg = tuple(max(0, min(255, round((c - (1 - a) * 255) / a))) for c in (r, g, b))
            po[x, y] = (*fg, round(a * 255))

    bbox = out.getchannel("A").getbbox()
    if not bbox:
        sys.exit("ERROR: image is entirely white/transparent")
    m = args.margin
    bbox = (max(0, bbox[0] - m), max(0, bbox[1] - m),
            min(img.width, bbox[2] + m), min(img.height, bbox[3] + m))
    out.crop(bbox).save(args.dst)
    print(f"saved {args.dst} ({bbox[2]-bbox[0]}x{bbox[3]-bbox[1]})")


if __name__ == "__main__":
    main()
