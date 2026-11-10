"""The cycle (DICTO 10 Nov "can we do a cycle of them"): the scutoid move is its own inverse (TI <-> TD), and so is the flip (PD <-> TK).
Onion 1: S (TI 1 -> ID 1.18 -> TD 1.42) then A (TD -> ID -> TI, run at TI 1, ID 0.95, TD 0.90) scaled by 1.42/0.90 -> back to TI at
lam = 1.42/0.90; repeat scaled by lam^k. Onion 2 (polar): B (PD 1 -> RT 1.25 -> TK 1.55) then back (PD 1, RT 0.95, TK 0.86) scaled
by 1.55/0.86. Checks: each interface (outer corners of one shell = inner corners of the next) matches exactly; volumes add to
V(outer) - V(core) over 3 periods. Inputs: scutoid-sphere.json, scutoid-sphere-A.json, scutoid-polar.json, scutoid-polar-back.json"""
import json, numpy as np
from scipy.spatial import ConvexHull
def load(f, s=1.0): return [{'V': (np.array(c['V']) * s).tolist(), 'F': c['F'], 'kind': c['kind'], 'vol': c['vol'] * s ** 3} for c in json.load(open(f))]
def radii(cells): return np.linalg.norm(np.array([v for c in cells for v in c['V']]), axis=1)
def surf(cells, outer):
    P = np.array([v for c in cells for v in c['V']]); r = np.linalg.norm(P, axis=1)
    # the inner / outer surface corners: those on the hull of the shell (outer) or the hull of the core (inner)
    h = ConvexHull(P)
    if outer: S = P[np.unique(h.vertices)]
    else:
        # inner: corners not on the outer hull and not interior middle-level ones: smallest radius on each ray family
        S = P[r < np.sort(np.unique(np.round(r, 9)))[1] + 1e-9] if False else None
    return {tuple(np.round(p, 9)) for p in S} if S is not None else None
def run(name, f1, f2, k_out, k_in_scale):
    S1 = load(f1); lam_half = k_out; S2 = load(f2, lam_half)
    lam = None; out = []
    # the joining scale: shell 2 was computed with its OUTER surface type at radius 1 (TI or PD); its inner at k_in; scale so inner = shell 1 outer
    o1 = {tuple(np.round(p, 7)) for p in np.array([v for c in S1 for v in c['V']]) if True}
    pts2 = {tuple(np.round(p, 7)) for c in S2 for p in np.array(c['V'])}
    shared = len(o1 & pts2)
    lam = k_in_scale
    vol = 0.0
    for k in range(3):
        for sh in (S1, S2):
            for c in sh: vol += abs(c['vol']) * lam ** (3 * k)
    print(f'{name}: corners shared by shell 1 and shell 2 (their interface): {shared}; period scale {lam:.6f}')
    return S1, S2, lam, vol, shared
S1, S2, lamA, volA, shA = run('scutoid onion', 'scutoid-sphere.json', 'scutoid-sphere-A.json', 1.42 / 0.90, 1.42 / 0.90)
P1, P2, lamB, volB, shB = run('flip onion', 'scutoid-polar.json', 'scutoid-polar-back.json', 1.55 / 0.86, 1.55 / 0.86)
# exact volume of the cores: TI (circumradius 1) and PD (5-fold corners at 1): from the inner corners of shell 1
def core_vol(cells):
    P = np.array([v for c in cells for v in c['V']]); r = np.linalg.norm(P, axis=1); rmin = r.min()
    # inner surface = corners at the inner radii: the cells' bottom faces F[0] (and F[0], F[1] for the flip cells)
    return P, rmin
TIv = ConvexHull(np.array([p for c in S1 for p in np.array(c['V'])[c['F'][0]]])).volume
PDv = ConvexHull(np.array([p for c in P1 for f in c['F'][:2] for p in np.array(c['V'])[f]])).volume
print(f'scutoid onion 3 periods: cell volumes {volA:.10f} vs V(TI x lam^3) - V(TI) {TIv * (lamA ** 9 - 1):.10f}')
print(f'flip onion 3 periods:    cell volumes {volB:.10f} vs V(PD x lam^3) - V(PD) {PDv * (lamB ** 9 - 1):.10f}')
ok = shA == 60 and shB == 32 and abs(volA - TIv * (lamA ** 9 - 1)) < 1e-6 and abs(volB - PDv * (lamB ** 9 - 1)) < 1e-6
onion = []
for k in range(3):
    for sh in (S1, S2):
        for c in sh: onion.append({'V': (np.array(c['V']) * lamA ** k).tolist(), 'F': c['F'], 'kind': c['kind']})
json.dump(onion, open('scutoid-onion.json', 'w'))
ponion = []
for k in range(3):
    for i, sh in enumerate((P1, P2)):
        for c in sh: ponion.append({'V': (np.array(c['V']) * lamB ** k).tolist(), 'F': c['F'], 'kind': 'flip' if i == 0 else 'flipback'})
json.dump(ponion, open('scutoid-flip-onion.json', 'w'))
print('FINAL ok' if ok else 'FINAL FAIL')
