#!/usr/bin/env python3
"""Put the rows of a partial rerun (data/catalogue-<tag>.json) into data/catalogue-all.json, replacing rows of the same name."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "../data")
allr = json.load(open(os.path.join(D, "catalogue-all.json")))
new = json.load(open(os.path.join(D, f"catalogue-{sys.argv[1]}.json")))
names = {r["name"] for r in new}
allr = [r for r in allr if r["name"] not in names] + new
json.dump(allr, open(os.path.join(D, "catalogue-all.json"), "w"), default=str)
print("rows", len(allr))
if len(allr) == 168 and sum(1 for r in allr if r["family"] == "Johnson") == 92:
    print("FINAL ok merged")
