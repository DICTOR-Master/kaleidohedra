#!/usr/bin/env python3
"""Lead 1 (CMB / Poincaré dodecahedral space): count the harmonics of degree k on S³ invariant under the 120 icosians (left action), from OUR 600-cell corners,
and compare with Aurich–Lustig–Steiner (astro-ph/0412569, eqs. 26–27): β = k + 1 ∈ {1,13,21,25,31,33,37,41,43,45,49,51,53,55,57} ∪ {2n+1, n ≥ 30},
r(β) = β(⌊(β−1)/10⌋ + ⌊(β−1)/6⌋ + ⌊(β−1)/4⌋ − ⌊(β−3)/2⌋). Degree-k harmonics = V_{k/2} ⊗ V_{k/2}; left-invariant dimension = (k+1)·(1/120) Σ_q χ_{k/2}(q),
χ_{k/2}(cos θ + u sin θ) = sin((k+1)θ)/sin θ. Links: 600-cell silent in degrees 1–11 (11-design) ⇔ first mode k = 12."""
import itertools, math, json, numpy as np
phi = (1 + 5**.5)/2
V = [p for p in itertools.product((-1, 1, 0), repeat=4) if sum(abs(x) for x in p) == 1] + [tuple(s/2 for s in sg) for sg in itertools.product((1, -1), repeat=4)]
base = (phi/2, 1/2, 1/(2*phi), 0)
for p in itertools.permutations(range(4)):
    if sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2: continue
    for sg in itertools.product((1, -1), repeat=3):
        v = [0]*4; vals = [base[0]*sg[0], base[1]*sg[1], base[2]*sg[2], 0]
        for i in range(4): v[p[i]] = vals[i]
        V.append(tuple(v))
V = np.unique(np.round(np.array(V), 12), axis=0); assert len(V) == 120
th = np.arccos(np.clip(V[:, 0], -1, 1))
def chi(k, t): return (k + 1) if abs(math.sin(t)) < 1e-12 and math.cos(t) > 0 else ((-1)**k*(k + 1) if abs(math.sin(t)) < 1e-12 else math.sin((k + 1)*t)/math.sin(t))
def r_lit(b):
    allowed = b in {1, 13, 21, 25, 31, 33, 37, 41, 43, 45, 49, 51, 53, 55, 57} or (b % 2 == 1 and b >= 61)
    return b*((b - 1)//10 + (b - 1)//6 + (b - 1)//4 - (b - 3)//2) if allowed and b > 1 else (1 if b == 1 else 0)
rows = []; agree = True
for k in range(0, 121):
    m = sum(chi(k, t) for t in th)/120; ours = round((k + 1)*m)
    lit = r_lit(k + 1); rows.append((k, ours, lit)); agree &= (ours == lit)
print('degrees with modes (ours):', [k for k, o, l in rows if o][:20])
print('all 121 degrees agree with Aurich–Lustig–Steiner:', agree)
print('mismatches:', [(k, o, l) for k, o, l in rows if o != l][:10])
json.dump({'rows': rows, 'agree': agree}, open('data/pds-modes.json', 'w'))
