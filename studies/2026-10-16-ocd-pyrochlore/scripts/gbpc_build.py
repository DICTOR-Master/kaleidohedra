# Fable, GBPC pass 3 (2026-10-16): BUILD TEST for G' by golden rhombohedra, not face to face. Exact in Q(sqrt5) unless marked FLOAT.
# G' = space minus the union of the uncut RTs (pass 1). Every body here (RTs, golden rhombohedra) has face normals on the 15 two-fold
# axes and edges on five-fold axes, so the separating-axis test needs only the 15 two-fold directions: two such bodies have disjoint
# interiors iff on one of these 15 axes their projections meet in at most a point (exact).
# Greedy periodic fill: anchors = corners of G' and corners of placed tiles; at each anchor try the 160 corner orientations of a golden
# rhombohedron of edge s|v|, keep the placement with most face contacts; repeat; then halve s. Every placement is checked exactly.
import sys, io, os, contextlib, itertools, json, numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
os.environ['FAST'] = '1'   # pass 1 checked the triple overlaps exactly
lines = open(os.path.join(HERE, 'gbpc_tiling.py')).read().split('\n')
src = '\n'.join(lines[:199])
with contextlib.redirect_stdout(io.StringIO()):
    exec(src)
out = []; say = lambda s: (print(s, flush=True), out.append(s))
say("DICTO · dictospheres.com — Fable, GBPC pass 3: greedy build test for G' (exact placements)")
phiQ = Q(Fr(1, 2), Fr(1, 2))
N15 = AX['2']; N15f = np.array([fl(n) for n in N15])
rtmax = [max((dot(n, v) for v in RT['V']), key=lambda x: x.f()) for n in N15]
rtmin = [min((dot(n, v) for v in RT['V']), key=lambda x: x.f()) for n in N15]
LATT = []
for m in itertools.product(range(-5, 6), repeat=3):
    c = add(add(mul(LB[0], Q(m[0])), mul(LB[1], Q(m[1]))), mul(LB[2], Q(m[2])))
    if np.linalg.norm(fl(c)) < 4.5 * RT['r']: LATT.append(c)
LATTf = np.array([fl(c) for c in LATT])
def rt_int(c):   # support intervals of RT + c (exact and float)
    lo = [rtmin[i] + dot(N15[i], c) for i in range(15)]; hi = [rtmax[i] + dot(N15[i], c) for i in range(15)]
    return lo, hi
RTS = [(c, *rt_int(c)) for c in LATT]
RTSf = [(fl(c), np.array([x.f() for x in lo]), np.array([x.f() for x in hi])) for c, lo, hi in RTS]
P5 = AX['5'] + [neg(v) for v in AX['5']]
ORI = [r for r in itertools.combinations(P5, 3) if not any(iszero(add(x, y)) for x, y in itertools.combinations(r, 2))]
assert len(ORI) == 160
dets = {}
def tile(p, r, s):
    w = [mul(x, s) for x in r]
    lo, hi = [], []
    for n in N15:
        a = dot(n, p); proj = [dot(n, x) for x in w]
        lo.append(a + sum((x for x in proj if sgn(x) < 0), Z)); hi.append(a + sum((x for x in proj if sgn(x) > 0), Z))
    d = det3(*w); d = d if sgn(d) > 0 else -d
    V = [add(p, add(add(mul(w[0], Q(i)), mul(w[1], Q(j))), mul(w[2], Q(k)))) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    return dict(p=p, r=r, s=s, lo=lo, hi=hi, lof=np.array([x.f() for x in lo]), hif=np.array([x.f() for x in hi]), vol=d, V=V,
                c=fl(p) + sum(fl(x) for x in w) / 2, rad=float(sum(np.linalg.norm(fl(x)) for x in w)) / 2 + 1e-9)
def disjoint(A, B, shiftB=None):
    """exact: interiors disjoint? A, B dicts with lo/hi (B optionally translated by shiftB)."""
    sh = [Z] * 15 if shiftB is None else [dot(n, shiftB) for n in N15]
    shf = np.zeros(15) if shiftB is None else N15f @ fl(shiftB)
    g1 = (B['lof'] + shf) - A['hif']; g2 = A['lof'] - (B['hif'] + shf)
    if np.max(g1) > 1e-9 or np.max(g2) > 1e-9: return True
    if np.max(g1) < -1e-9 and np.max(g2) < -1e-9: return False
    for i in range(15):
        if abs(g1[i]) <= 1e-9 and sgn(B['lo'][i] + sh[i] - A['hi'][i]) >= 0: return True
        if abs(g2[i]) <= 1e-9 and sgn(A['lo'][i] - B['hi'][i] - sh[i]) >= 0: return True
    return False
RTB = [dict(lo=lo, hi=hi, lof=f[1], hif=f[2], c=f[0], rad=RT['r']) for (c, lo, hi), f in zip(RTS, RTSf)]
def contacts(T, B, shiftB=None):
    sh = [Z] * 15 if shiftB is None else [dot(n, shiftB) for n in N15]
    k = 0
    for i in range(15):
        if abs(B['lof'][i] + (0 if shiftB is None else N15f[i] @ fl(shiftB)) - T['hif'][i]) < 1e-9 and B['lo'][i] + sh[i] == T['hi'][i]: k += 1
        if abs(T['lof'][i] - B['hif'][i] - (0 if shiftB is None else N15f[i] @ fl(shiftB))) < 1e-9 and T['lo'][i] == B['hi'][i] + sh[i]: k += 1
    return k
placed = []
def near_bodies(p, reach):
    pf = fl(p)
    rts = [B for B in RTB if np.linalg.norm(pf - B['c']) <= reach + B['rad']]
    pls = [(B, c) for B in placed for c, cf in zip(LATT, LATTf) if np.linalg.norm(pf - B['c'] - cf) <= reach + B['rad']]
    return rts, pls
def fits(T, rts, pls):
    k = 0
    for B in rts:
        if np.linalg.norm(T['c'] - B['c']) > T['rad'] + B['rad']: continue
        if not disjoint(T, B): return None
        k += contacts(T, B)
    for B, c in pls:
        if np.linalg.norm(T['c'] - B['c'] - fl(c)) > T['rad'] + B['rad']: continue
        if not disjoint(T, B, c): return None
        k += contacts(T, B, c)
    return k
Linv = np.linalg.inv(np.array([fl(b) for b in LB]).T)
OFFS = [np.array(m) for m in itertools.product(range(-2, 3), repeat=3)]
def red(p):   # nearest-lattice-point reduction (Wigner-Seitz style), exact result
    base = np.round(Linv @ fl(p)).astype(int); Lf = np.array([fl(b) for b in LB]).T
    m = min((base + o for o in OFFS), key=lambda mm: np.linalg.norm(fl(p) - Lf @ mm))
    out_ = sub(p, add(add(mul(LB[0], Q(int(m[0]))), mul(LB[1], Q(int(m[1])))), mul(LB[2], Q(int(m[2])))))
    assert np.linalg.norm(fl(out_)) < 1.2, 'reduction failed'
    return out_
dO = Q(376, -168)   # oblate volume at edge |v| (gbpc_two_size.py), checked next
assert any(det3(*r) == dO or det3(*r) == -dO for r in ORI)
vG2 = cellv - (pvol(RT) - Q(4) * Q(Fr(-704, 729), Fr(320, 729)))
filled = Z; log = []
CORN = [red(p) for p in CORN]   # every anchor within 1.2 of the origin (asserted in red), so the RT list (radius 4.5 r) covers every tile
anchors = {key(p): p for p in CORN}
SIZES = [(phiQ / 9, 'phi/9'), (phiQ / 18, 'phi/18'), (phiQ / 36, 'phi/36')][:int(os.environ.get('NSIZES', '3'))]
for s, nm in SIZES:
    dead = set(); reach = 3 * s.f() * float(np.linalg.norm(fl(AX['5'][0]))) + 1e-6
    while True:
        added = 0
        for k_, p in list(anchors.items()):
            if k_ in dead: continue
            rts, pls = near_bodies(p, reach); best = None
            for r in ORI:
                T = tile(p, r, s); f = fits(T, rts, pls)
                if f is not None and (best is None or f > best[0]): best = (f, T)
            if best:
                T = best[1]; placed.append(T); filled = filled + T['vol']; added += 1
                for v in T['V']:
                    q = red(v); anchors.setdefault(key(q), q)
            else: dead.add(k_)
        say(f'  edge {nm}|v|: pass placed {added}; tiles {len(placed)}; filled {filled.f() / vG2.f():.2%} of G\' (FLOAT ratio of exact volumes)')
        if added == 0: break
kinds = {}
for T in placed:
    t = ('oblate' if T['vol'] == T['s'] * T['s'] * T['s'] * dO else 'prolate', repr(T['s']))
    kinds[t] = kinds.get(t, 0) + 1
say(f"result: {len(placed)} tiles per cell, {kinds}; exact filled volume {filled!r} of G' {vG2!r}; remainder {vG2 - filled!r} = {(vG2 - filled).f():.6f} ({(vG2 - filled).f() / vG2.f():.2%})")
# FLOAT Monte Carlo check: sample points in every tile; none may lie inside an RT or inside another tile (with translates)
rng = np.random.default_rng(1); Hn = np.array([fl(n) for n, d in RT['H']]); Hd = np.array([d.f() for n, d in RT['H']])
mc_rt = mc_tt = 0
for i, A in enumerate(placed):
    W_ = np.array([fl(mul(x, A['s'])) for x in A['r']]); X = fl(A['p']) + rng.random((200, 3)) @ W_
    for cf in LATTf:
        mc_rt += int(np.sum(np.all((X - cf) @ Hn.T < Hd - 1e-9, axis=1)))
    for j, B in enumerate(placed):
        WB = np.array([fl(mul(x, B['s'])) for x in B['r']]); IB = np.linalg.inv(WB.T)
        for c, cf in zip(LATT, LATTf):
            if (j == i and iszero(c)) or np.linalg.norm(A['c'] - B['c'] - cf) > A['rad'] + B['rad']: continue
            t = (X - fl(B['p']) - cf) @ IB.T
            mc_tt += int(np.sum(np.all((t > 1e-9) & (t < 1 - 1e-9), axis=1)))
say(f'FLOAT Monte Carlo (200 points per tile): points inside an RT {mc_rt}; points inside another tile {mc_tt}')
# exact recheck of every pair (with translates) and against every RT
bad = 0
for i, A in enumerate(placed):
    for B in RTB:
        if np.linalg.norm(A['c'] - B['c']) <= A['rad'] + B['rad'] and not disjoint(A, B): bad += 1
    for j, B in enumerate(placed):
        for c, cf in zip(LATT, LATTf):
            if (j == i and iszero(c)) or np.linalg.norm(A['c'] - B['c'] - cf) > A['rad'] + B['rad']: continue
            if not disjoint(A, B, c): bad += 1
say(f'exact recheck: overlapping pairs {bad}')
open(os.path.join(STUDY, 'data', 'gbpc-build.txt'), 'w').write('\n'.join(out) + '\n')
json.dump({'mark': 'DICTO · dictospheres.com', 'units': '|v| = icosahedron circumradius, frame of golden-fill.json; tiles per bcc cell (periodic)',
           'tiles': [{'corner': fl(T['p']).tolist(), 'edges': [fl(mul(x, T['s'])).tolist() for x in T['r']], 'edge': T['s'].f()} for T in placed]},
          open(os.path.join(STUDY, 'data', 'gbpc-build.json'), 'w'))
