#!/usr/bin/env python3
"""Merge the seven stage-1 files into data/j84_90_exact.json; FINAL ok only if all seven are present and checked."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for J in ("J84", "J85", "J86", "J87", "J88", "J89", "J90"):
    p = os.path.join(HERE, f"../data/j84_90_exact_{J}.json")
    if os.path.exists(p):
        out.update(json.load(open(p)))
        log = open(os.path.join(HERE, f"../logs/stage1-{J}.log")).read()
        assert "exact checks passed" in log
        print("PROGRESS", len(out) / 7, J, "degree", len(out[J]["poly"]) - 1, flush=True)
    else:
        print(J, "missing", flush=True)
json.dump(out, open(os.path.join(HERE, "../data/j84_90_exact.json"), "w"))
if len(out) == 7:
    print("FINAL ok 7 solids exact")
