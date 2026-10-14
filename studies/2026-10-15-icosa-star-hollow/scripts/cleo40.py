# DICTO 2026-10-15: "we could also make the core an icosahedron full of Cleo-Icos". The hollow DICTO-ICOSA star with 40 Cleo-Icos
# (edge 1): 20 inner ones meeting at the centre (the core) and 20 outer ones on the shell's triangles, points on the inner ones' base
# centres. Uses the DICTO-Star itself (krp-core idStar via studies/2026-10-12-dicto-icosa-star/dicto-star.json) as the shell.
# Checks: no overlaps among the 40 and with the 12 dodecahedra and 20 J63s; each loose piece alone, can it move?
import itertools, json, sys, numpy as np
from scipy.spatial import ConvexHull
S = json.load(open(sys.argv[1]))
ID = np.array(S['centre']); DOD = [np.array(v) for v in S['dodecahedra']]; J63 = [np.array(v) for v in S['caps']]
g = (1 + 5 ** .5) / 2; r_in = g * g / (2 * 3 ** .5)
H = ConvexHull(ID); F = []
for e in H.equations:
    idx = tuple(sorted(i for i in range(30) if abs(ID[i] @ e[:3] + e[3]) < 1e-9))
    if idx not in [f for f, _ in F]: F.append((idx, e))
tri = [(ID[list(i)], e[:3]) for i, e in F if len(i) == 3]; pent = [e[:3] for i, e in F if len(i) == 5]
outer = [np.vstack([T, T.mean(0) - n * r_in]) for T, n in tri]
core = np.array([n * ((10 + 2 * 5 ** .5) ** .5 / 4) for n in pent]); CH = ConvexHull(core)
inner = [np.vstack([core[s], [0, 0, 0]]) for s in CH.simplices]
assert len(inner) == 20 and abs(min(np.linalg.norm(a - b) for a, b in itertools.combinations(core, 2)) - 1) < 1e-12
def axes(P):
    h = ConvexHull(P); A = [e[:3] for e in h.equations]
    E = {tuple(np.round(P[j] - P[i], 12)) for s in h.simplices for i, j in itertools.combinations(s, 2)}
    return A, [np.array(x) for x in E]
AX = {}
def sep(P, Q):
    a1, e1 = axes(P); a2, e2 = axes(Q); best = -1e9
    for n in a1 + a2 + [np.cross(u, w) / np.linalg.norm(np.cross(u, w)) for u in e1 for w in e2 if np.linalg.norm(np.cross(u, w)) > 1e-12]:
        p, q = P @ n, Q @ n; best = max(best, q.min() - p.max(), p.min() - q.max())
    return best
out = []
pieces = [('inner', P) for P in inner] + [('outer', P) for P in outer]
shell = [('dodeca', P) for P in DOD] + [('J63', P) for P in J63]
s40 = min(sep(a, b) for (_, a), (_, b) in itertools.combinations(pieces, 2))
s_sh = min(sep(a, b) for _, a in pieces for _, b in shell)
out.append(f'1. overlaps: among the 40 Cleo-Icos min separation {s40:.1e}; against the 12 dodecahedra and 20 J63s {s_sh:.1e} (>= -1e-12: none)')
pts = max(abs(np.linalg.norm(P[3]) - r_in) for P in outer)
out.append(f'2. every outer point at the core inradius {r_in:.12f} (worst {pts:.1e}); inner apices all at the centre')
near = lambda P: [Q for _, Q in pieces + shell if Q is not P and sep(P, Q) < 1e-9]
def rot(a, t):
    a = a / np.linalg.norm(a); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]); return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K
rng = np.random.default_rng(2); dirs = rng.normal(size=(60, 3))
for kind in ('inner', 'outer'):
    free_t = free_r = 0; nb = []
    for name, P in pieces:
        if name != kind: continue
        N = near(P); nb.append(len(N)); c = P.mean(0)
        for d in dirs:
            Pt = P + 0.002 * d / np.linalg.norm(d)
            if min(sep(Pt, Q) for Q in N) > -1e-12: free_t += 1
            Pr = (P - c) @ rot(d, np.radians(1)).T + c
            if min(sep(Pr, Q) for Q in N) > -1e-12: free_r += 1
    out.append(f'3. each {kind} Cleo-Ico alone ({min(nb)}-{max(nb)} touching neighbours): free shifts {free_t} of {20 * len(dirs)}, free 1° turns {free_r} of {20 * len(dirs)}')
vol = lambda P: ConvexHull(P).volume
out.append(f'4. volumes: inner 20 {sum(map(vol, inner)):.6f}, outer 20 {sum(map(vol, outer)):.6f}, hollow left empty {vol(ID) - sum(map(vol, inner)) - sum(map(vol, outer)):.6f} (5 + 2√5 = {5 + 2 * 5 ** .5:.6f})')
print('\n'.join(out)); open('cleo40.txt', 'w').write('\n'.join(out) + '\n')
mesh = lambda P: {'v': np.round(P, 6).tolist(), 'f': ConvexHull(P).simplices.tolist(), 'c': np.round(P.mean(0), 6).tolist()}
json.dump({'shell': mesh(ID), 'inner': [mesh(P) for P in inner], 'outer': [mesh(P) for P in outer], 'core': mesh(core)}, open('cleo40.json', 'w'))
