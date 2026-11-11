# Faces of the #59 stage solids and assemblies (study 2026-10-27-icosaxes-twenty, data/*-union.obj, joined with manifold3d):
# merge coplanar triangles into faces, classify each face (regular polygon, truncated triangle with ratio, other), count golden ones.
import sys, glob, os, numpy as np
from collections import defaultdict, Counter
g = (1 + 5 ** .5) / 2
def read_obj(f):
    V, F = [], []
    for line in open(f):
        t = line.split()
        if not t: continue
        if t[0] == 'v': V.append([float(x) for x in t[1:4]])
        elif t[0] == 'f': F.append([int(x.split('/')[0]) - 1 for x in t[1:]])
    return np.array(V), F
def classify(P):
    n = len(P); L = np.array([np.linalg.norm(P[(i + 1) % n] - P[i]) for i in range(n)])
    A = np.array([np.degrees(np.arccos(np.clip(np.dot(P[i - 1] - P[i], P[(i + 1) % n] - P[i]) / (np.linalg.norm(P[i - 1] - P[i]) * np.linalg.norm(P[(i + 1) % n] - P[i])), -1, 1))) for i in range(n)])
    t = 1e-5 * L.max()
    if all(abs(L - L[0]) < t) and all(abs(A - A[0]) < 1e-3): return f'regular {n}-gon'
    if n == 6 and all(abs(A - 120) < 1e-3) and all(abs(L[i] - L[(i + 2) % 6]) < t for i in range(6)):
        r = max(L[0], L[1]) / min(L[0], L[1]); return 'truncated triangle φ' if abs(r - g) < 1e-5 else f'truncated triangle {r:.4f}'
    return f'other {n}-gon'
def faces(V, F):
    # group triangles by plane, then build each face boundary from edges used once
    planes = defaultdict(list)
    for tri in F:
        P = V[tri]; n = np.cross(P[1] - P[0], P[2] - P[0]); l = np.linalg.norm(n)
        if l < 1e-12: continue
        n /= l; planes[(tuple(np.round(n, 5)), round(float(n @ P[0]), 5))].append(tri)
    out = []
    for key, tris in planes.items():
        cnt = Counter()
        for tri in tris:
            for i in range(len(tri)): cnt[tuple(sorted((tri[i], tri[(i + 1) % len(tri)])))] += 1
        bnd = [e for e, c in cnt.items() if c == 1]
        adj = defaultdict(list)
        for a, b in bnd: adj[a].append(b); adj[b].append(a)
        seen = set()
        for s in list(adj):
            if s in seen: continue
            loop = [s]; seen.add(s); prev = None; cur = s
            while True:
                nxt = [x for x in adj[cur] if x != prev and (x not in seen or (x == s and len(loop) > 2))]
                if not nxt: break
                prev, cur = cur, nxt[0]
                if cur == s: break
                loop.append(cur); seen.add(cur)
            P = V[loop]
            # drop collinear points
            keep = [i for i in range(len(P)) if np.linalg.norm(np.cross(P[i] - P[i - 1], P[(i + 1) % len(P)] - P[i])) > 1e-9]
            if len(keep) >= 3: out.append(P[keep])
    return out
base = os.path.expanduser('~/work/studies/2026-10-27-icosaxes-twenty/data')
for f in sorted(glob.glob(base + '/*-union.obj')):
    V, F = read_obj(f); fs = faces(V, F); c = Counter(classify(P) for P in fs)
    print(f"{os.path.basename(f)}: {len(fs)} faces; " + '; '.join(f'{k} ×{v}' for k, v in sorted(c.items(), key=lambda kv: -kv[1])))
