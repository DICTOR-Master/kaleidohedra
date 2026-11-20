#!/usr/bin/env python3
"""Tabulate blind pre-score outputs and judge them against Palomar's floor.

  python3 -I tally.py RAW_DIR [--floor 4]

RAW_DIR holds the scorers' JSON verbatim, one file per scorer and candidate: blind-<A|B>-<CAND>.json.
Prints one row per candidate (notability / literature / outcome / number of findings for each scorer) and a verdict:
  clears   every scorer gives notability >= floor (notability is mandatory);
  at risk  the scorers split across the floor;
  fails    every scorer gives notability below the floor.
Literature below the floor with outcome `warning` does not block, but the finding must be fixed before submission.
The tally is not the judgement: write the review of the reviews (what is right, what is mistaken) in the study README."""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("raw")
ap.add_argument("--floor", type=int, default=4)
a = ap.parse_args()
rows = collections.defaultdict(dict)
for p in sorted(Path(a.raw).glob("blind-*-*.json")):
    m = re.match(r"blind-([A-Za-z0-9]+)-(.+)\.json$", p.name)
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        sys.exit(f"{p.name}: not JSON ({err}); record the scorer's hand-back verbatim")
    s = d.get("scores", {})
    rows[m.group(2)][m.group(1)] = (s.get("notability"), s.get("literature"), d.get("outcome"),
                                    len(d.get("findings", [])))
if not rows:
    sys.exit(f"no blind-<scorer>-<candidate>.json files in {a.raw}")
print(f"floor {a.floor}  (notability / literature, outcome, findings)")
for cand, by in rows.items():
    cells = "  |  ".join(f"{k}: {n} / {l}, {o}, {f} finding(s)" for k, (n, l, o, f) in sorted(by.items()))
    ns = [v[0] for v in by.values() if isinstance(v[0], int)]
    ls = [v[1] for v in by.values() if isinstance(v[1], int)]
    verdict = ("clears" if ns and min(ns) >= a.floor else "fails" if ns and max(ns) < a.floor else "at risk")
    lit = "" if ls and min(ls) >= a.floor else "; literature below the floor: fix the finding(s) first"
    print(f"{cand}: {cells}\n  -> notability {verdict}{lit}")
