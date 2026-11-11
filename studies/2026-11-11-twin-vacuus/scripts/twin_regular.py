# twin_regular.py (from twin_disc_levels.py), DICTO 11 Nov 2026 ("check if the twin hulls are exactly regular"): per level, are the twin
# hull's faces regular polygons (all sides equal, all angles equal) and all its edges one length (= a uniform, Platonic/Archimedean
# solid exactly)? Reports distinct edge lengths (ratio max/min), per face type the side and angle spread, and the verdict.
# Original header: twin_disc_levels.py, DICTO 11 Nov 2026 ("yes test the disc law on levels 1-10"). For each level k of the OG downward family, the twin
# points (sqrt5 -> -sqrt5 on the exact Q(sqrt5) corners of D_k, computed without cancellation as (a^2 - 5b^2)/(a + b sqrt5)), their
# convex hull (the twin hull), and its Vacuus. DISC = a set of fins in one plane through O whose apex angles add to 360 degrees and
# that close around O (a full central polygon). Per level: corners on the hull, faces (by sides), edges, fin apex classes, discs (count,
# fins per disc, fin angle, which axis the disc is perpendicular to: 5-, 3-, 2-fold or a mirror plane only). Control: k = 0 reproduces
# the OG's twin hull (102 corners, 200 triangles, 6 discs of ten 36-degree fins).
# usage: python -u twin_regular.py <five-fold-octet dir> <K> <out.json>
import sys, os, json, time
here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
src = open(os.path.join(here, 'exact_family.py')).read(); head = src.split("t0 = time.time()")[0]
_K, _OUT = int(sys.argv[2]), os.path.abspath(sys.argv[3]); sys.argv = [sys.argv[0], sys.argv[1], '0', '/dev/null']; exec(head)
import numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
def twinf(x):
    if x.b == 0: return float(x.a)
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 else float(x.a * x.a - 5 * x.b * x.b) / re
AX = {}
for order in (5, 3, 2):
    for M in Gf:
        if abs(np.trace(M) - (1 + 2 * np.cos(2 * np.pi / order))) < 1e-9:
            w, v = np.linalg.eig(M); a = np.real(v[:, np.argmin(abs(w - 1))]); AX.setdefault(order, []).append(a / np.linalg.norm(a))
def axis_type(n):
    for order in (5, 3, 2):
        if any(abs(abs(n @ a) - 1) < 1e-7 for a in AX[order]): return f'{order}-fold'
    return 'mirror/other'
def merged_faces(P, tol=1e-9):
    h = ConvexHull(P); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    out = []
    for pts in grp.values():
        idx = np.array(sorted(pts)); Q = P[idx]; c0 = Q.mean(0); B = np.linalg.svd(Q - c0)[2][:2]; q = (Q - c0) @ B.T
        out.append(list(idx[np.argsort(np.arctan2(q[:, 1], q[:, 0]))]))
    return out, h
rows = []; ok = True; t0 = time.time()
W = [tuple(cv(x) for x in v) for v in OG]
for k in range(_K + 1):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W])
    F, ne, _ = exact_faces(W, idx, Wfx)
    corners = sorted(set(i for mem in F for i in mem))
    T = np.array([[twinf(x) for x in W[i]] for i in corners]); T /= np.linalg.norm(T, axis=1).max()
    faces, h = merged_faces(T)
    E = sorted({(min(a, b), max(a, b)) for f in faces for a, b in zip(f, f[1:] + f[:1])})
    L = np.array([np.linalg.norm(T[a] - T[b]) for a, b in E]); Ls = np.unique(np.round(L / L.max(), 9))
    per = {}
    for f in faces:
        P = T[f]; e = np.linalg.norm(np.roll(P, -1, 0) - P, axis=1); e1 = np.roll(P, -1, 0) - P; e0 = P - np.roll(P, 1, 0)
        an = np.degrees(np.arccos(np.clip((-e0 * e1).sum(1) / (np.linalg.norm(e0, axis=1) * np.linalg.norm(e1, axis=1)), -1, 1)))
        d = per.setdefault(len(f), dict(n=0, side_spread=0.0, angle_spread=0.0))
        d['n'] += 1; d['side_spread'] = max(d['side_spread'], float(e.max() / e.min() - 1)); d['angle_spread'] = max(d['angle_spread'], float(an.max() - an.min()))
    rad = np.linalg.norm(T[np.unique(np.concatenate(faces))], axis=1); rad_spread = float(rad.max() / rad.min() - 1)
    regular_faces = all(v['side_spread'] < 1e-9 and v['angle_spread'] < 1e-7 for v in per.values())
    one_edge = len(Ls) == 1
    verdict = 'EXACTLY UNIFORM (regular faces, one edge length)' if regular_faces and one_edge else ('regular faces, several edge lengths' if regular_faces else 'NOT regular')
    row = dict(k=k, hull_corners=len(h.vertices), faces=len(faces), face_types={str(kk): v for kk, v in sorted(per.items())}, edge_lengths=len(Ls),
               edge_ratio=float(Ls.max() / Ls.min()), corner_radius_spread=rad_spread, verdict=verdict)
    if k == 0: ok &= len(h.vertices) == 102 and len(faces) == 200
    rows.append(row)
    print(f'PROGRESS {(k + 1) / (_K + 1):.3f}', flush=True)
    print(f"k {k:2d}: hull corners {len(h.vertices)}, faces {len(faces)} | edge lengths {len(Ls)} (max/min {Ls.max() / Ls.min():.6f}) | corners on one sphere: {rad_spread < 1e-9} | " +
          ' '.join(f"{kk}-gons x{v['n']}: sides spread {v['side_spread']:.1e}, angles spread {v['angle_spread']:.1e} deg;" for kk, v in sorted(per.items())) + f" | {verdict}", flush=True)
    feet = {}
    for n_, d_, _ in F.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    W = list(feet)
json.dump(rows, open(_OUT, 'w'), indent=1)
print('exactly uniform twin hulls at levels:', [r['k'] for r in rows if r['verdict'].startswith('EXACTLY')])
print('FINAL ok' if ok else 'FINAL FAIL: k = 0 does not reproduce the OG twin hull (102 corners, 200 triangles)')
