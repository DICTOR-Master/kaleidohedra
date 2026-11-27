"""Are DICTO's Star Cores stars Vacuus-Solids? (27 Nov 2026; DICTO: "turn 4 star from star cores app, turn 5 star same, turn 3 star; turn 1
star looks too spikey"; "some of the stars look like vacuus solids"). With Claude (Anthropic). Input: the app's own chain (dump_star_turns.mjs).
A star = solid S with a spike on every face (pyramid on the face, tip from the app). A Vacuus-Solid of a convex P = P with a pyramid pit
on every face whose tip lies on that face's axis, all tips at one size t of P's polar core. Test for each turn:
  P = hull of the star; for each face F of P, the pit bottom c_F = the deepest star point on F's axis (bisection with exact-enough
  membership); (1) is c_F a corner of S? (2) common size: lambda_F = |c_F| * d_F equal for all F (t = lambda / min d^2 as in the paper);
  (3) region test: random points of P, in the star vs in P minus the pits (mismatch fraction). PASS iff all three hold.
Numerical (1e-7). Exact form only for a pass."""
import json, sys
import numpy as np
from scipy.spatial import ConvexHull
D = json.load(open(sys.argv[1])); rng = np.random.default_rng(1)
def planes_of(V, F):
    out = []
    c = V.mean(0)
    for f in F:
        X = V[f]; n = np.cross(X[1] - X[0], X[2] - X[0]); n /= np.linalg.norm(n)
        if n @ (X[0] - c) < 0: n = -n
        out.append((n, n @ X[0]))
    return out
def in_convex(x, planes, tol=1e-12): return all(n @ x <= d + tol for n, d in planes)
def hull_planes(P):
    h = ConvexHull(P); out = []
    for eq in h.equations:
        n, d = eq[:3], -eq[3]
        if not any(np.allclose(n, m, atol=1e-9) and abs(d - e) < 1e-9 for m, e in out): out.append((n, d))
    return out, h
ran = 0
for T in D['turns']:
    V = np.array(T['solid']['vertices'], float); F = T['solid']['faces']; tips = T['tips']
    if tips is None: print(f"turn {T['turn']}: no tips in the dump"); continue
    tips = np.array(tips, float)
    if len(tips) != len(F): print(f"turn {T['turn']}: {len(tips)} tips for {len(F)} faces: skipped"); continue
    c0 = V.mean(0); V = V - c0; tips = tips - c0
    Sp = planes_of(V, F)
    spikes = []
    for f, tp in zip(F, tips):
        X = V[f]; apex = tp; pl = []
        cen = (X.sum(0) + apex) / (len(f) + 1)
        for i in range(len(f)):
            a, b = X[i], X[(i + 1) % len(f)]; n = np.cross(b - a, apex - a); n /= np.linalg.norm(n)
            if n @ (cen - a) > 0: n = -n
            pl.append((n, n @ a))
        nb = np.cross(X[1] - X[0], X[2] - X[0]); nb /= np.linalg.norm(nb)
        if nb @ (cen - X[0]) > 0: nb = -nb
        pl.append((nb, nb @ X[0])); spikes.append(pl)
    def in_star(x): return in_convex(x, Sp, 1e-10) or any(in_convex(x, pl, 1e-10) for pl in spikes)
    pts = np.vstack([V, tips]); Hp, h = hull_planes(pts)
    R = np.linalg.norm(pts, axis=1).max()
    bottoms, lam, on_corner = [], [], 0
    for n, d in Hp:
        lo, hi = 0.0, d                     # along the axis: star from 0 up to the pit bottom, then the pit up to the face
        if not in_star(lo * n): bottoms.append(None); continue
        for _ in range(60):
            mid = (lo + hi) / 2
            if in_star(mid * n): lo = mid
            else: hi = mid
        c = lo * n; bottoms.append(c); lam.append(lo * d)
        on_corner += int(np.min(np.linalg.norm(V - c, axis=1)) < 1e-6 * R)
    ok_axis = all(b is not None for b in bottoms)
    lam = np.array(lam); spread = float(lam.max() - lam.min()) / float(lam.mean()) if len(lam) else 9
    # region test
    lo3, hi3 = pts.min(0), pts.max(0); mis = tot = 0
    pits = []
    for (n, d), c in zip(Hp, bottoms):
        if c is None: continue
        corners = pts[np.abs(pts @ n - d) < 1e-7 * R]
        pits.append((n, d, c, corners))
    def in_pit(x, n, d, c, corners):
        # x in the pyramid conv(face, c): x between face plane and c, and its central projection from c onto the face plane inside the face
        if n @ x > d + 1e-12: return False
        u = x - c; den = n @ u
        if den <= 1e-15: return False
        s = (d - n @ c) / den
        if s < 1: return False
        y = c + s * u; fc = corners - y
        # inside the convex face polygon: y in hull of corners (2D test by angles)
        cen = corners.mean(0); e1 = corners[0] - cen; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        P2 = np.c_[(corners - cen) @ e1, (corners - cen) @ e2]; q = np.array([(y - cen) @ e1, (y - cen) @ e2])
        ang = np.arctan2(P2[:, 1], P2[:, 0]); P2 = P2[np.argsort(ang)]
        for i in range(len(P2)):
            a, b = P2[i], P2[(i + 1) % len(P2)]
            if (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0]) < -1e-12: return False
        return True
    while tot < 4000:
        x = lo3 + (hi3 - lo3) * rng.random(3)
        if not in_convex(x, Hp, 0): continue
        tot += 1
        vs = not any(in_pit(x, *p) for p in pits)
        mis += int(vs != in_star(x))
    ran += 1
    passed = ok_axis and on_corner == len(Hp) and spread < 1e-6 and mis == 0
    print(f"turn {T['turn']}: S {len(V)} corners / {len(F)} faces; hull of the star {len(Hp)} faces; pit bottoms on S's corners "
          f"{on_corner}/{len(Hp)}; common size spread {spread:.2e}; region mismatch {mis}/{tot} -> "
          f"{'IS a Vacuus-Solid of its hull (numerically)' if passed else 'not a Vacuus-Solid'}", flush=True)
print('FINAL ok' if ran == len(D['turns']) else 'FINAL FAIL (some turns not tested)')
