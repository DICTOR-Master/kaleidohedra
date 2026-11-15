#!/usr/bin/env python3
# Guard (DICTO 15 Nov, "fig 6.7 too big for fig frame again"): a rendered figure whose model runs off the image edge.
# For each image on a plain ground: sample the 2-px border; if more than 3% of border pixels differ from the ground colour
# (taken from the corners), the model touches or crosses the frame. Photos and diagrams with no plain ground are skipped.
# Allowlist: edgecheck-allow.txt beside this script, one line per image: <path relative to this folder> <reason>
# (deliberate crops only: a detail or close-up whose caption says so). '#' lines are comments.
# Usage: python3 edgecheck.py IMAGE...   -> one "EDGE <share> <path>" line per hit not in the allowlist; exit 1 on any hit.
# Called by figcheck.mjs for every book-* folder, so every book build stops on a hit.
import sys, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
def allowed():
    p = os.path.join(HERE, 'edgecheck-allow.txt'); out = {}
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            line = line.strip()
            if line and not line.startswith('#'):
                path, _, reason = line.partition(' ')
                if not reason.strip(): sys.exit(f'edgecheck-allow.txt: no reason given for {path}')
                out[os.path.normpath(path)] = reason.strip()
    return out
def check(p):
    im = Image.open(p).convert('RGB'); w, h = im.size; px = im.load()
    corners = [px[1, 1], px[w - 2, 1], px[1, h - 2], px[w - 2, h - 2]]
    if max(abs(a - b) for c in corners for d in corners for a, b in zip(c, d)) > 24: return None
    g = corners[0]; border = [(x, y) for x in range(w) for y in (0, 1, h - 2, h - 1)] + [(x, y) for y in range(h) for x in (0, 1, w - 2, w - 1)]
    bad = sum(1 for x, y in border if max(abs(a - b) for a, b in zip(px[x, y], g)) > 40)
    return bad / len(border)
if __name__ == '__main__':
    allow = allowed(); rc = 0
    for p in sys.argv[1:]:
        rel = os.path.normpath(os.path.relpath(os.path.abspath(p), HERE))
        if rel in allow: continue
        try: r = check(p)
        except Exception: continue
        if r is not None and r > 0.03: print(f'EDGE {r:.1%} {rel}'); rc = 1
    sys.exit(rc)
