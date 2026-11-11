# twin_disc_levels.py, DICTO 11 Nov 2026 ("yes test the disc law on levels 1-10"). For each level k of the OG downward family, the twin
# points (sqrt5 -> -sqrt5 on the exact Q(sqrt5) corners of D_k, computed without cancellation as (a^2 - 5b^2)/(a + b sqrt5)), their
# convex hull (the twin hull), and its Vacuus. DISC = a set of fins in one plane through O whose apex angles add to 360 degrees and
# that close around O (a full central polygon). Per level: corners on the hull, faces (by sides), edges, fin apex classes, discs (count,
# fins per disc, fin angle, which axis the disc is perpendicular to: 5-, 3-, 2-fold or a mirror plane only). Control: k = 0 reproduces
# the OG's twin hull (102 corners, 200 triangles, 6 discs of ten 36-degree fins).
# usage: python -u twin_disc_levels.py <five-fold-octet dir> <K> <out.json>
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
    apex = np.array([np.degrees(np.arccos(np.clip(T[a] @ T[b] / (np.linalg.norm(T[a]) * np.linalg.norm(T[b])), -1, 1))) for a, b in E])
    nrm = []
    for a, b in E:
        n = np.cross(T[a], T[b]); n /= np.linalg.norm(n); n *= np.sign(n[np.argmax(np.abs(n) > 1e-9)]); nrm.append(n)
    nrm = np.array(nrm); planes = {}
    for i in range(len(E)): planes.setdefault(tuple(np.round(nrm[i], 7)), []).append(i)
    discs = []
    for key, ids in planes.items():
        tot = apex[ids].sum()
        if abs(tot - 360) < 1e-5:                                          # fins in this plane fill a full turn round O
            ang = sorted(set(np.round(apex[ids], 4)))
            discs.append(dict(fins=len(ids), angles=[float(a) for a in ang], perpendicular_to=axis_type(np.array(key))))
    dsum = Counter((d['fins'], tuple(d['angles']), d['perpendicular_to']) for d in discs)
    hullpts = len(h.vertices)
    row = dict(k=k, twin_points=len(T), hull_corners=hullpts, faces=len(faces), face_types=dict(Counter(len(f) for f in faces)), edges=len(E),
               fin_classes=len(set(np.round(apex, 4))), discs=len(discs), disc_kinds={f'{c[0]} fins {list(c[1])} perp {c[2]}': v for c, v in dsum.items()})
    if k == 0: ok &= hullpts == 102 and len(faces) == 200 and len(discs) == 6 and all(d['fins'] == 10 and d['angles'] == [36.0] for d in discs)
    rows.append(row)
    print(f'PROGRESS {(k + 1) / (_K + 1):.3f}', flush=True)
    print(f"k {k:2d}: twin points {len(T)}, on hull {hullpts} | faces {len(faces)} {dict(sorted(row['face_types'].items()))} | edges {len(E)} | fin classes {row['fin_classes']} | DISCS {len(discs)}: {row['disc_kinds']} ({time.time() - t0:.0f}s)", flush=True)
    feet = {}
    for n_, d_, _ in F.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    W = list(feet)
json.dump(rows, open(_OUT, 'w'), indent=1)
print('disc law (six discs of ten 36-degree fins) at levels:', [r['k'] for r in rows if r['disc_kinds'] == {'10 fins [36.0] perp 5-fold': 6}])
print('FINAL ok' if ok else 'FINAL FAIL: k = 0 does not reproduce the OG twin hull (102 corners, 200 triangles, 6 discs of 10 x 36 deg)')
