"""Branch D: smallest lattice scale at which translated C1 copies (T_h axes on the cube axes) do not overlap, per cubic lattice.
C1 = convex TI + 12 convex pyramids; overlap depth of two convex parts = Chebyshev radius of their intersection (LP, float64).
Scan from s0 (the Voronoi-containment scale of resin.py) downward in steps of 0.01, then bisect the first overlap; prints s_free.
Below s0 the copies may interlock, but C1 then sticks out of its Voronoi cell, so the Voronoi mould needs s >= s0."""
import itertools, sys
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from resin import build_C1, tofl
C = build_C1()
TV = np.array([tofl(v) for v in C["TV"]]); AP = np.array([tofl(v) for v in C["apex"]])
dirs = np.array([tofl(d) for d in C["hd"] + C["pd"]]); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
bTI = np.array([max(d @ v for v in TV) for d in dirs])
parts = [(dirs, bTI, np.zeros(3), np.linalg.norm(TV, axis=1).max())]
for p in range(12):
    rows = [(-dirs[20+p], -bTI[20+p])]
    for fi in range(20 + 5*p, 25 + 5*p):
        n = tofl(C["planes"][fi][0]); L = np.linalg.norm(n); rows.append((n/L, float(C["planes"][fi][1])/L))
    pts = np.vstack([TV[C["pents"][p]], AP[p]]); cen = pts.mean(0)
    parts.append((np.array([r[0] for r in rows]), np.array([r[1] for r in rows]), cen, np.linalg.norm(pts - cen, axis=1).max()))
RA = np.linalg.norm(AP, axis=1).max()
def depth(P1, P2, t):
    A = np.vstack([P1[0], P2[0]]); b = np.concatenate([P1[1], P2[1] + P2[0] @ t])
    r = linprog([0, 0, 0, -1], A_ub=np.hstack([A, np.ones((len(A), 1))]), b_ub=b, bounds=[(None, None)]*3 + [(None, 10)], method="highs")
    return -r.fun if r.status == 0 else -1
LAT = {"sc": [np.array(v, float) for v in itertools.product(range(-2, 3), repeat=3) if any(v)],
       "bcc": [np.array(v, float)/2 for v in itertools.product(range(-4, 5), repeat=3) if any(v) and len({x % 2 for x in v}) == 1],
       "fcc": [np.array(v, float)/2 for v in itertools.product(range(-4, 5), repeat=3) if any(v) and sum(v) % 2 == 0]}
S0 = {"sc": (5 + 3*5**.5)/2, "bcc": (10 + 4*5**.5)/3, "fcc": 5 + 2*5**.5}
def overlap(lat, s):
    for v in LAT[lat]:
        t = v*s
        if np.linalg.norm(t) >= 2*RA or v[0] < 0 or (v[0] == 0 and (v[1] < 0 or (v[1] == 0 and v[2] < 0))): continue  # central symmetry
        for P1 in parts:
            for P2 in parts:
                if np.linalg.norm(P1[2] - (P2[2] + t)) >= P1[3] + P2[3]: continue
                d = depth(P1, P2, t)
                if d > 1e-9: return d
    return 0
RES = {}
for lat in ("sc", "bcc", "fcc"):
    s = S0[lat]
    assert overlap(lat, s) == 0
    while overlap(lat, s - 0.01) == 0 and s > 2: s -= 0.01
    lo, hi = s - 0.01, s
    for _ in range(25):
        m = (lo + hi)/2
        if overlap(lat, m) == 0: hi = m
        else: lo = m
    print(f"{lat}: s0 (C1 inside its Voronoi cell) = {S0[lat]:.6f}; smallest scan scale with no overlap s_free = {hi:.6f} "
          f"(scan step 0.01 from s0 down; ratio s_free/s0 = {hi/S0[lat]:.4f})", flush=True)
    RES[lat] = (hi, overlap(lat, hi) == 0 and overlap(lat, lo) > 0)
ok = all(v[1] and v[0] <= S0[k] + 1e-9 for k, v in RES.items())
print("FINAL ok" if ok else f"FINAL FAIL {RES}")
