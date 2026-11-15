#!/usr/bin/env python3
"""DICTO's theory (16 Nov 2026): the recently found shapes are Vacuus because their walls (central plates) were
indistinguishable from 600-cell walls. Test: for each 2-face of solid A (hull of X) and solid B (hull of F) take the central
hyperplane it spans with the centre; is it (i) an H4 mirror of the 600-cell P (normal parallel to a vertex of P), or
(ii) one of P's own Vacuus plates (central hyperplane spanned by a triangle of P)? Controls: P's own triangles (positive),
an ordinary nearby orbit (negative expected). Floating point (matches at 1e-7; hits and misses are separated by orders of magnitude). Exact Q(sqrt5) recheck: next step."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
p = (1 + 5 ** .5) / 2
def orbit(base):
    S = np.array(sorted(set(itertools.permutations(base))), float); return S
def to4(S, mean):  # sum-zero 5-space -> orthonormal 4D coordinates
    Q = np.linalg.qr(np.vstack([np.ones(5), np.eye(5)[:4]]).T)[0][:, 1:5]
    return (S - mean) @ Q
X5 = orbit((p*p, p*p, p*p, p, 0)); F5 = orbit((p*p, p*p, 1, 1, 0))
m = X5.mean(0)
X = to4(X5, m); F = to4(F5, F5.mean(0))
r = np.linalg.norm(X[0]); assert np.allclose(np.linalg.norm(X, axis=1), r)
# 600-cell P: closure of X under reflections in its own members
key = lambda u: tuple(np.round(u, 6) + 0.0)
Pd = {key(v): v for v in X}; grow = True
while grow:
    grow = False; A_ = list(Pd.values())
    for v in A_:
        for w in A_:
            u = w - 2 * (w @ v) / (v @ v) * v; k = key(u)
            if k not in Pd: Pd[k] = u; grow = True
    if len(Pd) > 200: raise SystemExit(f'closure exploded {len(Pd)}')
P = np.array(list(Pd.values())); print('600-cell P vertices:', len(P)); assert len(P) == 120
Fn = F * (r / np.linalg.norm(F[0])); onP = sum(any(np.allclose(f, q, atol=1e-7) for q in P) for f in Fn)
print('F (rescaled to radius of X) lies in P:', onP, 'of', len(F))
def unit(v): return v / np.linalg.norm(v)
def canon(n):
    n = unit(n); i = np.argmax(np.abs(n) > 1e-9); return n if n[i] > 0 else -n
def faces2(V):
    h = ConvexHull(V); eqs = {}
    for e, s in zip(h.equations, h.simplices):
        k = tuple(np.round(e, 7)); eqs.setdefault(k, set()).update(s)
    fac = list(eqs.values()); out = set()
    for a, b in itertools.combinations(fac, 2):
        c = sorted(a & b)
        if len(c) >= 3 and np.linalg.matrix_rank(V[c] - V[c].mean(0), tol=1e-7) == 2: out.add(tuple(c))
    return fac, sorted(out)
def plane_normal(V, c):  # hyperplane through 0 and 2-face c
    M = V[list(c)]; _, s, vt = np.linalg.svd(M); assert s[2] > 1e-6 and (len(s) < 4 or s[3] < 1e-7); return canon(vt[3])
mirrors = np.array([canon(v) for v in P]); mirrors = np.unique(np.round(mirrors, 9), axis=0); print('H4 mirrors:', len(mirrors))
fP, ridP = faces2(P); print('P: facets', len(fP), '2-faces', len(ridP))
Pplates = np.unique(np.round([plane_normal(P, c) for c in ridP], 9), axis=0); print("P's own Vacuus plates:", len(Pplates))
def test(name, V):
    fac, rid = faces2(V); ns = [plane_normal(V, c) for c in rid]
    planes = np.unique(np.round(ns, 9), axis=0)
    inM = sum(np.min(np.linalg.norm(mirrors - n, axis=1)) < 1e-7 for n in planes)
    inP = sum(np.min(np.linalg.norm(Pplates - n, axis=1)) < 1e-7 for n in planes)
    # which face types
    kinds = {}
    for c, n in zip(rid, ns):
        key = (len(c), bool(np.min(np.linalg.norm(mirrors - n, axis=1)) < 1e-7), bool(np.min(np.linalg.norm(Pplates - n, axis=1)) < 1e-7))
        kinds[key] = kinds.get(key, 0) + 1
    print(f'{name}: facets {len(fac)} 2-faces {len(rid)} plates {len(planes)} | in H4 mirrors {inM} | in P plates {inP} | by (corners, mirror, Pplate): {kinds}')
    return len(planes), inM, inP
pc = test('positive control P', P)
a = test('solid A (X, 20)', X); b = test('solid B (F, 30)', F)
neg = []
for name, base in (('negative control (phi^2,phi^2,phi^2,1.5,0)', (p*p, p*p, p*p, 1.5, 0)), ('negative control (phi^2,phi^2,1.2,1.2,0)', (p*p, p*p, 1.2, 1.2, 0))):
    S = orbit(base); neg.append(test(name, to4(S, S.mean(0))))
checks = [len(P) == 120, onP == len(F), len(mirrors) == 60, pc == (60, 60, 60),   # positive control: every plate of P is a wall
          all(n[1] < n[0] for n in neg),                                          # negative controls: ordinary orbits are NOT all walls
          a[0] == 30 and b[0] == 80]
print('checks', checks); print('FINAL ok' if all(checks) else 'FINAL FAIL checks')
