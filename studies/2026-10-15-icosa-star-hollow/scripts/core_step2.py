# Cleo core step 2 (DICTO 2026-10-15): cut each antiprism around its outer Cleo-Ico, group the cuts by symmetry (12 corners, 30 edges,
# 20 faces) and compare every piece with the kit (krp-core ICOSA_SOLIDS: AXE, FUJI, CLEO, ...) and with classical pieces.
import itertools, json, sys, numpy as np
from scipy.spatial import ConvexHull
S = json.load(open(sys.argv[1])); KIT = json.load(open(sys.argv[2]))
ID = np.array(S['centre']); g = (1 + 5 ** .5) / 2; R = (10 + 2 * 5 ** .5) ** .5 / 4; r = g * g / (2 * 3 ** .5)
H = ConvexHull(ID); F = []
for e in H.equations:
    idx = tuple(sorted(i for i in range(30) if abs(ID[i] @ e[:3] + e[3]) < 1e-9))
    if idx not in [f for f, _ in F]: F.append((idx, e))
tri = [(ID[list(i)], e[:3]) for i, e in F if len(i) == 3]; pent = [(ID[list(i)], e[:3]) for i, e in F if len(i) == 5]
core = np.array([n * R for _, n in pent]); CH = ConvexHull(core); cf = [core[s] for s in CH.simplices]
vol = lambda P: ConvexHull(P).volume
out = []
X, Y, C, A = [], [], [], []
for T, n in tri:
    B = max(cf, key=lambda Q: Q.mean(0) @ n); b0 = B.mean(0); A.append(np.vstack([T, B])); C.append(np.vstack([T, b0]))
    for i, j in itertools.combinations(range(3), 2):           # top edge t_i t_j with the bottom vertex facing it
        bk = min(B, key=lambda b: np.linalg.norm(b - (T[i] + T[j]) / 2)); X.append(np.array([T[i], T[j], bk, b0]))
    for k, l in itertools.combinations(range(3), 2):           # bottom edge b_k b_l with the top vertex facing it
        tm = min(T, key=lambda t: np.linalg.norm(t - (B[k] + B[l]) / 2)); Y.append(np.array([B[k], B[l], tm, b0]))
sA = sum(map(vol, A)); sP = sum(map(vol, C)) + sum(map(vol, X)) + sum(map(vol, Y))
out.append(f'1. each antiprism = its Cleo-Ico + 3 top-edge tetrahedra (X) + 3 bottom-edge tetrahedra (Y): volumes {sP:.12f} vs {sA:.12f} (diff {sP - sA:.1e})')
L = lambda P: sorted(round(np.linalg.norm(a - b), 6) for a, b in itertools.combinations(P, 2))
out.append(f'   X edges {L(X[0])} vol {vol(X[0]):.6f};  Y edges {L(Y[0])} vol {vol(Y[0]):.6f};  Cleo-Ico vol {vol(C[0]):.6f}')
key = lambda P: tuple(np.round(sorted(map(tuple, np.round(P, 6))), 6).ravel())
def pairs_over(items, share):
    groups = {}
    for P in items: groups.setdefault(share(P), []).append(P)
    return groups
# 30 edge pieces: the two Y's over each core edge
Ygroups = pairs_over(Y, lambda P: tuple(sorted(map(tuple, np.round(P[:2], 6)))))
E = [np.unique(np.round(np.vstack(G), 9), axis=0) for G in Ygroups.values()]
convE = [abs(vol(Pe) - sum(vol(q) for q in G)) < 1e-9 for Pe, G in zip(E, Ygroups.values())]
out.append(f'2. edge pieces: {len(E)} (Y pairs over the core edges, sizes {sorted(set(len(G) for G in Ygroups.values()))}); convex: {sum(convE)} of {len(E)}; vertices {len(E[0])}, edges {L(E[0])[:3]}..., vol {vol(E[0]):.6f}')
# 12 corner pieces: each flat pentagonal pyramid + the X's that touch it face to face
pyr = [np.vstack([P, nn * R]) for P, nn in pent]
corner = []
for P in pyr:
    apex = P[5]; mine = [x for x in X if np.linalg.norm(x[2] - apex) < 1e-9]   # X whose bottom vertex is this core corner
    pts = np.unique(np.round(np.vstack([P] + mine), 9), axis=0); corner.append((pts, len(mine), abs(vol(pts) - vol(P) - sum(map(vol, mine))) < 1e-9))
out.append(f'3. corner pieces: {len(corner)}, each the flat pyramid + {corner[0][1]} X; convex: {sum(c[2] for c in corner)} of 12; vertices {len(corner[0][0])}, vol {vol(corner[0][0]):.6f}')
tot = vol(core) + sum(vol(c[0]) for c in corner) + sum(map(vol, E)) + sum(map(vol, C))
out.append(f'4. hollow = core + 12 corner pieces + 30 edge pieces + 20 Cleo-Icos: {tot:.12f} vs ID {vol(ID):.12f} (diff {tot - vol(ID):.1e})')
# compare with the kit and classical pieces by shape (scale-free: edge ratios and vol/edge^3)
def sig(P):
    h = ConvexHull(P); Ls = sorted({round(np.linalg.norm(P[a] - P[b]), 9) for s in h.simplices for a, b in itertools.combinations(s, 2)})
    m = Ls[-1]; return len(P), tuple(round(x / m, 4) for x in Ls), round(vol(P) / m ** 3, 5)
lib = {k: sig(np.array(v)) for k, v in KIT.items() if len(v) >= 4}
J2 = np.vstack([np.array([[np.cos(2 * np.pi * k / 5), np.sin(2 * np.pi * k / 5), 0] for k in range(5)]) / (2 * np.sin(np.pi / 5)), [0, 0, ((5 - 5 ** .5) / 10) ** .5]])
lib['J2 (pentagonal pyramid)'] = sig(J2); lib['regular tetrahedron'] = sig(np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float))
for name, P in [('X', X[0]), ('Y', Y[0]), ('edge piece', E[0]), ('corner piece', corner[0][0]), ('flat pyramid', pyr[0]), ('Cleo-Ico', C[0])]:
    s = sig(P); same = [k for k, v in lib.items() if v[1] == s[1] and v[2] == s[2]]
    near = sorted(lib, key=lambda k: abs(lib[k][2] - s[2]) + (0 if lib[k][0] == s[0] else 1))[:2]
    out.append(f'5. {name}: {s[0]} vertices, vol/edge³ {s[2]} -> same shape as: {same or "none"} (closest by volume ratio: {near})')
print('\n'.join(out)); open('core_step2.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'core': np.round(core, 6).tolist(), 'cleo': [np.round(c, 6).tolist() for c in C], 'edge': [np.round(e, 6).tolist() for e in E],
           'corner': [np.round(c[0], 6).tolist() for c in corner]}, open('core_step2.json', 'w'))
