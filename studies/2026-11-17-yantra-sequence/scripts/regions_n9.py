"""Where in Chiodo's parameters (u, v, Q, S) each nine-triangle count pattern was found (family.py samples).
usage: python3 regions_n9.py <family json> <out json>"""
import sys, json
from fractions import Fraction as Fr
d = json.load(open(sys.argv[1]))
pat = {}
for r in d['raw']['9']:
    key = f"{r['odd']} {[r['rings'].get(str(c), r['rings'].get(c, 0)) for c in (1, 3, 5, 7, 9)]}"
    pat.setdefault(key, []).append([float(Fr(z)) for z in r['params'][:4]])
out = {}
for k, ps in sorted(pat.items(), key=lambda kv: -len(kv[1])):
    cols = list(zip(*ps))
    rng = {nm: (round(min(c), 4), round(max(c), 4)) for nm, c in zip('uvQS', cols)}
    uv = [p[0] * p[1] for p in ps]; ratio = [p[0] / p[1] for p in ps]
    rng['uv'] = (round(min(uv), 4), round(max(uv), 4)); rng['u/v'] = (round(min(ratio), 4), round(max(ratio), 4))
    out[k] = dict(samples=len(ps), ranges=rng)
    print(f"{len(ps):5d}  {k:28s} " + "  ".join(f"{nm} {a}-{b}" for nm, (a, b) in rng.items()))
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print("FINAL ok" if sum(v['samples'] for v in out.values()) == len(d['raw']['9']) > 0 else "FINAL FAIL")
