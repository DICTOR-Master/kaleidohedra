#!/usr/bin/env python3
"""Do J. Kostick's vZome arrays (3-4 April 2022) contain GET A, GET B, candidate 2 (Hall/Inchbald) or plain T as cells?
Input: the vZome sharing exports *.shapes.json (panel shapes = rhombi in absolute coordinates, 7-digit floats).
1. Snap every panel coordinate to (a + b*phi)/2 with integers |b| < 400 (unique at this precision; residual reported),
   swap x and y (vZome's icosahedral frame is the mirror of ours) and divide by the strut scale, so panel edges become exactly
   +-axis vectors of hall_check.AX. Checked exactly: every panel is a rhombus with two axis edges.
2. For each solid X (T; GET A; GET B; candidate 2) and each of the 120 symmetries g of the six-axis star (both hands) and every
   panel P matching g(f0): place g(X) with f0 on P and count how many of its 30 faces are scene panels. A cell of the array
   that is a copy of X shows all 30 (when no panel was left out).
Usage: kostick_check.py <grunbaum-k10 dir> <out json> <shapes.json>..."""
import sys, json, itertools, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
K10, OUT, FILES = sys.argv[1], sys.argv[2], sys.argv[3:]
import importlib.util
spec = importlib.util.spec_from_file_location('hc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hall_check.py'))
hc = importlib.util.module_from_spec(spec); spec.loader.exec_module(hc)
q, add, sub, mul, inv, dot, cross, det3, sgn, Z, ONE = hc.q, hc.add, hc.sub, hc.mul, hc.inv, hc.dot, hc.cross, hc.det3, hc.sgn, hc.Z, hc.ONE
AX = hc.AX
PHI = (1 + 5 ** 0.5) / 2

def snap(x):
    best = None
    for b in range(-400, 401):
        a = round(2 * x - b * PHI); e = abs((a + b * PHI) / 2 - x)
        if best is None or e < best[0]: best = (e, a, b)
    e, a, b = best
    return (Fr(a, 2), Fr(b, 2)), e

# the 120 symmetries
X3 = [AX[0], AX[2], AX[4]]
G0 = [[dot(a, b) for b in X3] for a in X3]
Xi = hc.matinv([list(r) for r in X3])
signed = [tuple(mul(q(s), c) for c in a) for a in AX for s in (1, -1)]
axset = set(signed)
GROUP = []
for y in itertools.permutations(signed, 3):
    if any(dot(y[i], y[j]) != G0[i][j] for i in range(3) for j in range(3)): continue
    M = [[Z]*3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            s = Z
            for i in range(3): s = add(s, mul(y[i][r], Xi[c][i]))
            M[r][c] = s
    if not all(dot([M[k][a] for k in range(3)], [M[k][b] for k in range(3)]) == (ONE if a == b else Z) for a in range(3) for b in range(3)): continue
    ap = lambda v, M=M: tuple(dot(M[r], v) for r in range(3))
    if {ap(a) for a in signed} != axset: continue
    d = det3(*[[M[k][c] for k in range(3)] for c in range(3)])
    GROUP.append((M, 1 if d == ONE else -1))
assert len(GROUP) == 120, len(GROUP)
apply = lambda M, v: tuple(dot(M[r], v) for r in range(3))

def solids():
    data = json.load(open(K10 + '/data/search6.json'))
    out = {'T': hc.tri_T()}
    for nm, c in zip(['GET A', 'GET B', 'candidate 2 (Hall/Inchbald)'], data['candidates_rank_le_3'][:3]):
        out[nm] = hc.cand_faces(c)
    return out

def key(p): return tuple(hc_float(c) for c in p)
def hc_float(u): return float(u[0]) + float(u[1]) * PHI

res = {'files': {}}
SOL = solids()
for fn in FILES:
    d = json.load(open(fn)); sh = {s['id']: s for s in d['shapes']}
    raw = []
    for inst in d['instances']:
        s = sh[inst['shape']]
        if len(s['vertices']) != 4: continue
        assert 'orientation' not in inst or inst['orientation'] == 0
        p = inst['position']
        raw.append([(v['x'] + p['x'], v['y'] + p['y'], v['z'] + p['z']) for v in s['vertices']])
    maxerr = 0; panels = []
    for P in raw:
        pts = []
        for v in P:
            c = []
            for x in (v[1], v[0], v[2]):          # swap x, y
                z, e = snap(x); maxerr = max(maxerr, e); c.append(z)
            pts.append(tuple(c))
        panels.append(pts)
    # scale from the first edge
    e0 = hc.vsub(panels[0][1], panels[0][0])
    lam = None
    for a in signed:
        # e0 = lam * a  for some lam in Q(phi)
        nz = [i for i in range(3) if a[i] != Z]
        l = mul(e0[nz[0]], inv(a[nz[0]]))
        if all(mul(l, a[i]) == e0[i] for i in range(3)): lam = l; break
    assert lam is not None, 'first panel edge not along an axis'
    li = inv(lam)
    panels = [[tuple(mul(li, c) for c in v) for v in P] for P in panels]
    # exact checks: each panel a rhombus (cyclic order 0-1-2-3) with edges +-axes
    okp = 0
    for P in panels:
        ed = [hc.vsub(P[(i+1) % 4], P[i]) for i in range(4)]
        if all(e in axset for e in ed) and hc.vadd(ed[0], ed[2]) == (Z, Z, Z) and hc.vadd(ed[1], ed[3]) == (Z, Z, Z) and ed[0] != ed[1] and ed[0] != hc.vneg(ed[1]): okp += 1
    pset = {frozenset(P) for P in panels}
    row = {'panels': len(panels), 'distinct_panels': len(pset), 'snap_max_residual': maxerr, 'exact_rhombi_on_axes': okp, 'scale': [str(lam[0]), str(lam[1])]}
    import functools
    def cmpv(a, b):
        for x, y in zip(a, b):
            s = sgn(sub(x, y))
            if s: return s
        return 0
    kmin = lambda F: min(F, key=functools.cmp_to_key(cmpv))
    plist = [frozenset(P) for P in pset]
    for nm, F in SOL.items():
        f0 = F[0]; full = set(); best = 0; byhand = {1: 0, -1: 0}
        for M, dt in GROUP:
            img = [frozenset(apply(M, v) for v in f) for f in F]
            g0 = frozenset(apply(M, v) for v in f0); m0 = kmin(g0)
            dirs = {hc.vsub(v, m0) for v in g0}
            for P in plist:
                mP = kmin(P)
                if {hc.vsub(v, mP) for v in P} != dirs: continue
                t = hc.vsub(mP, m0)
                placed = frozenset(frozenset(hc.vadd(v, t) for v in f) for f in img)
                n = sum(1 for f in placed if f in pset)
                best = max(best, n)
                if n == len(F) and placed not in full:
                    full.add(placed); byhand[dt] += 1
        row[nm] = {'max_faces_present': best, 'full_copies': len(full), 'full_by_hand_in_our_frame': {'proper': byhand[1], 'improper': byhand[-1]}}
    res['files'][os.path.basename(fn)] = row
    print(os.path.basename(fn), json.dumps(row), flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
ok = all(r['exact_rhombi_on_axes'] == r['panels'] and r['snap_max_residual'] < 1e-5 for r in res['files'].values())
print('FINAL ok' if ok else 'FINAL FAIL: a panel is not an exact golden rhombus on the axes')
