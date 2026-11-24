#!/usr/bin/env python3
"""Smallest angle between points of N. J. A. Sloane's spherical packings (with R. H. Hardin and W. D. Smith),
files pack.3.N.txt from neilsloane.com/packings/dim3 (downloaded 25 Nov 2026 into data/sloane-pack3).
Plain double precision: the values are compared with ours at 0.01 degree or more, far above rounding."""
import math, os, sys, json
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/sloane-pack3")
out = {}
for f in sorted(os.listdir(D), key=lambda s: int(s.split(".")[2])):
    L = open(os.path.join(D, f)).read().split("\n")
    x = [float(t) for l in L if l.strip() and not any(ch.isalpha() and ch not in "Ee" for ch in l) for t in l.split()]
    P = [x[i:i + 3] for i in range(0, len(x), 3)]
    n = int(f.split(".")[2]); assert len(P) == n, f
    P = [[c / math.sqrt(sum(d * d for d in p)) for c in p] for p in P]
    c = max(sum(a * b for a, b in zip(P[i], P[j])) for i in range(n) for j in range(i + 1, n))
    out[n] = round(math.degrees(math.acos(c)), 4)
print(json.dumps(out))
json.dump(out, open(os.path.join(D, "../sloane-min-angles.json"), "w"), indent=1)
print("FINAL ok" if len(out) == len(os.listdir(D)) == 15 else "FINAL FAIL file count")
