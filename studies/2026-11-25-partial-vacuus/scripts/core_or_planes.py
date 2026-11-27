# DICTO · Vacuus-Solids (27 Nov 2026): for each special member (P, s) and each solid Q whose face planes carry the pit walls, is lam*Q
# really the CORE (the pits end on it: Q's faces covered by the walls, no pit enters Q), or does Q only share planes with the walls?
# DICTO: "is it really mathematically sound to include the figs with the far more complex inner cores?". With Claude (Anthropic).
# Numerical (sampling) first pass: coverage = fraction of sample points on Q's faces that lie on a wall triangle in the same plane;
# entry = fraction of sample points inside Q that lie strictly inside some pit. TRUE CORE iff coverage 1 and entry 0 (to sampling).
import json, os, sys
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
exec(open(os.path.join(HERE, 'special_depths_all.py')).read().split('found = []')[0])
found = json.load(open(os.path.join(HERE, '../data-special-all.json')))
rng = np.random.default_rng(7)
def orient(P, Q, s, lam):
    V, F, N, D = S[P]; W = walls(V, F, N, D); VQ, FQ, NQ0, DQ = S[Q]
    for M in FRAME:
        NQ = NQ0 @ M.T; ok = True
        for fj, m0j, m1j, uj in W:
            a = s * D[fj]; m = m0j + a * m1j; m /= np.linalg.norm(m); dist = abs(m @ uj)
            if not any(abs(abs(m @ w) - 1) < 1e-7 and abs(dist - lam * dq) < 1e-6 for w, dq in zip(NQ, DQ)): ok = False; break
        if ok: return NQ, DQ
    return None
def in_tri2(p, a, b, c, n):
    s1 = np.cross(b - a, p - a) @ n; s2 = np.cross(c - b, p - b) @ n; s3 = np.cross(a - c, p - c) @ n
    return (s1 >= -1e-9 and s2 >= -1e-9 and s3 >= -1e-9) or (s1 <= 1e-9 and s2 <= 1e-9 and s3 <= 1e-9)
def in_pit(x, base, apex):
    c = (base.sum(0) + apex) / (len(base) + 1)
    for a, b, d in [(base[i], base[(i + 1) % len(base)], apex) for i in range(len(base))] + [(base[0], base[1], base[2])]:
        n = np.cross(b - a, d - a); t = n @ (x - a)
        if np.sign(t) != np.sign(n @ (c - a)) or abs(t) < 1e-9 * np.linalg.norm(n): return False
    return True
out = []
for f in found:
    P, Q, s, lam = f['P'], f['Q'], f['s'], f['lam']
    V, F, N, D = S[P]; o = orient(P, Q, s, lam)
    if o is None: print(f'{P} / {Q}: orientation not recovered', flush=True); continue
    NQ, DQ = o
    H = HalfspaceIntersection(np.hstack([NQ, -(lam * np.array(DQ))[:, None]]), np.zeros(3)); QV = H.intersections
    pits = [(V[fc], s * D[fi] * N[fi]) for fi, fc in enumerate(F)]
    wall_tris = [(base[i], base[(i + 1) % len(base)], apex) for base, apex in pits for i in range(len(base))]
    cov_hit = cov_n = 0
    for j, (w, dq) in enumerate(zip(NQ, DQ)):
        on = QV[np.abs(QV @ w - lam * dq) < 1e-7]
        if len(on) < 3: continue
        c0 = on.mean(0); e1 = on[0] - c0; e2 = np.cross(w, e1); on = on[np.argsort(np.arctan2((on - c0) @ e2, (on - c0) @ e1))]
        tris_here = [t for t in wall_tris if abs(np.cross(t[1] - t[0], t[2] - t[0]) / np.linalg.norm(np.cross(t[1] - t[0], t[2] - t[0])) @ w) > 1 - 1e-7
                     and abs(t[0] @ w - lam * dq) < 1e-7]
        for _ in range(60):
            i = rng.integers(1, len(on) - 1); r = rng.dirichlet([1, 1, 1]); p = r[0] * on[0] + r[1] * on[i] + r[2] * on[i + 1]
            cov_n += 1; cov_hit += any(in_tri2(p, *t, w) for t in tris_here)
    ent = 0; NS = 600
    for _ in range(NS):
        r = rng.dirichlet(np.ones(len(QV))); x = r @ QV
        ent += any(in_pit(x, b, a) for b, a in pits)
    cov = cov_hit / max(cov_n, 1); entf = ent / NS
    tips = np.array([a for b, a in pits]); g = (tips @ NQ.T - lam * np.array(DQ)).max(axis=1); scl = np.abs(QV).max()
    tips_on = int((np.abs(g) < 1e-7 * scl).sum()); tips_out = int((g > 1e-7 * scl).sum()); tips_in = int((g < -1e-7 * scl).sum())
    tip_corner = int(sum(np.min(np.linalg.norm(QV - t, axis=1)) < 1e-7 * scl for t in tips))
    kind = ('pit tips = all corners of Q (Q is the hull of the tips)' if tip_corner == len(tips) == len(QV) else
            f'{tip_corner} of {len(tips)} tips at corners of Q, {tips_on - tip_corner} on its faces, {tips_out} outside, {tips_in} inside')
    out.append(dict(P=P, Q=Q, s=s, lam=lam, coverage=cov, entry=entf, tips_at_corners=tip_corner, tips_on=tips_on, tips_out=tips_out, tips_in=tips_in, Q_corners=len(QV), kind=kind))
    print(f'{P:24s} s {s:.7f}  Q {Q:30s}: walls cover {100 * cov:4.1f}% of its faces; pits enter it {100 * entf:4.1f}%; {kind}', flush=True)
json.dump(out, open(os.path.join(HERE, '../data-core-or-planes.json'), 'w'), indent=1)
print('FINAL ok' if out and len(out) == len(found) else 'FINAL FAIL (orientation not recovered for some)')
