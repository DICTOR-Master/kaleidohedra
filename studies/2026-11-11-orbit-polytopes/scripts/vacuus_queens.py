"""The Vacuus of the Queens (DICTO 11 Nov: "go on with the vacuus of the queens"). For the 600-cell, truncated 600-cell, bitruncated
600-cell, truncated 120-cell and 120-cell (built by truncation from the 600-cell's corners, as in the queen-stages atlas and #104):
their 2-faces (shared by two cells), the one central hyperplane each spans with the centre, how many faces each hyperplane carries,
the hyperplanes' classes under the 14400 symmetries (H4), and the 3D slice of each class (corners, faces). As #105 Theorem 1.
Check: every 2-face lies in exactly one central hyperplane (counts add up); classes are whole symmetry orbits."""
import itertools, sys, json, time
import numpy as np
from collections import Counter
from scipy.spatial import ConvexHull, cKDTree
sys.argv_saved = sys.argv; sys.argv = ['x', 'none']
exec(open('orbit4d.py').read().split("if __name__ == '__main__':")[0])
sys.argv = sys.argv_saved
exec(open('stages.py').read().split('keys = ')[0])
V6 = V.copy(); adj = {i: set(j for j in range(120) if abs(D[i, j] - e0) < 1e-9) for i in range(120)}
E6 = [(i, j) for i in range(120) for j in adj[i] if j > i]; T6 = [(i, j, k) for i, j in E6 for k in adj[i] & adj[j] if k > j]
C6 = [(i, j, k, l) for i, j, k in T6 for l in adj[i] & adj[j] & adj[k] if l > k]; cen = lambda q: V6[list(q)].mean(0)
def stage(name):
    pt = {}; X = []
    if name == '600-cell':
        X = list(V6); cells = [frozenset(c) for c in C6]
    elif name == 'truncated 600-cell':
        def P(a, b):
            if (a, b) not in pt: pt[(a, b)] = len(X); X.append((2 * V6[a] + V6[b]) / 3)
            return pt[(a, b)]
        cells = [frozenset(P(v, w) for w in adj[v]) for v in range(120)] + [frozenset(P(a, b) for a in c for b in c if a != b) for c in C6]
    elif name == '120-cell':
        X = [cen(c) for c in C6]; cells = [frozenset(ci for ci, c in enumerate(C6) if v in c) for v in range(120)]
    elif name == 'truncated 120-cell':
        s_ = (5 - 5 ** .5) / 10; byf = {}
        for ci, c in enumerate(C6):
            for f in itertools.combinations(sorted(c), 3): byf.setdefault(f, []).append(ci)
        def P(a, b):
            if (a, b) not in pt: pt[(a, b)] = len(X); X.append((1 - s_) * cen(C6[a]) + s_ * cen(C6[b]))
            return pt[(a, b)]
        tri_of = {}
        for f, (a, b) in byf.items(): P(a, b); P(b, a); tri_of[(a, b)] = f; tri_of[(b, a)] = f
        cells = [frozenset(idx for (a, b), idx in pt.items() if v in tri_of[(a, b)]) for v in range(120)] + [frozenset(idx for (a, b), idx in pt.items() if a == ci) for ci in range(600)]
    else:
        def P(t, a, b):
            key = (t, frozenset((a, b)))
            if key not in pt: pt[key] = len(X); X.append(0.4 * (V6[a] + V6[b]) / 2 + 0.6 * cen(t))
            return pt[key]
        for t in T6:
            for a, b in itertools.combinations(t, 2): P(t, a, b)
        cells = [frozenset(idx for (t, e), idx in pt.items() if v in e) for v in range(120)] + [frozenset(idx for (t, e), idx in pt.items() if set(t) <= set(c)) for c in C6]
    X = np.array(X, float); X -= X.mean(0)
    by = {}
    for ci, c in enumerate(cells):
        for p in c: by.setdefault(p, []).append(ci)
    faces = set()
    for p, cs in by.items():
        for a, b in itertools.combinations(cs, 2):
            sh = cells[a] & cells[b]
            if len(sh) >= 3: faces.add(frozenset(sh))
    return X, [sorted(f) for f in faces]
def normal_of(P):
    u, s, vt = np.linalg.svd(P); n = vt[-1]; n /= np.linalg.norm(n)
    return n if n[np.argmax(np.abs(n))] > 0 else -n
out = []
for name in (sys.argv[1].split(',') if len(sys.argv) > 1 else ['600-cell']):
    t0 = time.time(); X, F = stage(name); n = len(X)
    nn = cKDTree(X).query(X, k=2)[0][:, 1].min()
    E = [(i, j) for i, j in cKDTree(X).query_pairs(nn * 1.0001)]
    H = {}; reps = []                                       # group normals by nearness (tolerance), not by rounded digits
    for f in F:
        nv = normal_of(X[f])
        hit = None
        for r in reps:
            if abs(abs(r @ nv) - 1) < 1e-7: hit = r; break
        if hit is None: reps.append(nv); hit = nv
        H.setdefault(tuple(hit), []).append(f)
    total = sum(len(v) for v in H.values())
    # classes under the full symmetry group of the corners
    mats = sym_group(X); keys = list(H); seen = set(); classes = []
    kt = cKDTree(np.array(keys))
    for k in keys:
        if k in seen: continue
        nvec = np.array(k); members = set()
        for M in mats:
            m = M @ nvec
            for mm in (m, -m):
                d, j = kt.query(mm)
                if d < 1e-6: members.add(keys[j])
        seen |= members
        # slice shape: corners on the hyperplane + edge crossings
        pts = [X[i] for i in range(n) if abs(X[i] @ nvec) < 1e-9]
        for a, b in E:
            sa, sb = X[a] @ nvec, X[b] @ nvec
            if sa * sb < -1e-18: pts.append(X[a] + (X[b] - X[a]) * sa / (sa - sb))
        Q = np.unique(np.round(np.array(pts), 7), axis=0)
        Bs = np.linalg.svd(nvec.reshape(1, -1))[2][1:]
        try:
            hh = ConvexHull(Q @ Bs.T); G = {}
            for simp, eq in zip(hh.simplices, hh.equations): G.setdefault(tuple(np.round(eq, 5)), set()).update(simp)
            shape = (len(Q), len(G), dict(sorted(Counter(len(v) for v in G.values()).items())))
        except Exception as e:
            shape = (len(Q), None, str(e)[:40])
        classes.append({'slices': len(members), 'faces_each': len(H[k]), 'face_sizes': dict(Counter(len(f) for f in H[k])), 'slice_corners': shape[0], 'slice_faces': shape[1], 'slice_face_sizes': shape[2]})
    res = {'stage': name, 'corners': n, '2-faces': len(F), 'face_kinds': dict(Counter(len(f) for f in F)), 'central_hyperplanes': len(H), 'faces_carried': total,
           'symmetry': len(mats), 'classes': sorted(classes, key=lambda c: -c['slices'])}
    out.append(res)
    print(f"{name}: {n} corners, {len(F)} 2-faces {res['face_kinds']}, {len(H)} central hyperplanes carry {total}; {len(classes)} classes "
          f"(symmetry {len(mats)}): " + '; '.join(f"{c['slices']} slices x {c['faces_each']} faces {c['face_sizes']}, slice {c['slice_corners']} corners {c['slice_faces']} faces {c['slice_face_sizes']}" for c in res['classes']) + f"  ({time.time() - t0:.0f} s)", flush=True)
json.dump(out, open('vacuus_queens.json', 'w'), indent=1, default=str)
ok = all(r['faces_carried'] == r['2-faces'] and sum(c['slices'] for c in r['classes']) == r['central_hyperplanes'] for r in out)
print('FINAL ok' if ok else 'FINAL FAIL')
