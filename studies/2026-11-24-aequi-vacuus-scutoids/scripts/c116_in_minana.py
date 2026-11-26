"""The T_h C116 core inside Minana #377, face to face (26 Nov 2026; DICTO: "yes build the c116 core in minana"). With Claude (Anthropic).
1. Realise the unique T_h C116 (fullgen, data/c116/Full_codes_116_Th) as a convex polyhedron: spectral start, Hart's canonical
   iteration (edges tangent to the unit sphere, planar faces), then symmetrised: T_h's three half-turn axes put on the coordinate
   axes; each face orbit's plane fixed by one representative, averaged over its stabiliser, rounded to a rational grid, and carried
   to the whole orbit by T_h's 24 signed permutation matrices (exact, so the core is EXACTLY T_h-symmetric with rational planes).
2. Exact check: the 116 corners (each the meet of its 3 face planes) lie strictly inside every other face plane, so the polyhedron
   bounded by the 60 planes has exactly C116's faces and corners.
3. Orientation (one of the two T_h frames, 90 degrees about z) and the pairing core face -> Minana face: pentagons -> squares,
   24 -> 24, the two 12-hexagon orbits -> heptagons / hexagons whichever way fits the directions better; each face to the Minana face
   of its orbit with the nearest direction; must be a bijection.
4. The cell: amber_aequus.py with ASSIGN = that pairing (outer end of each piece = its Minana face), all its checks.
Usage: python c116_in_minana.py FACTOR   (e.g. 6/5)"""
import os, sys, itertools
from fractions import Fraction as Fr
import numpy as np
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
from resin import Q, dot, cross, det3
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
pr = lambda *a: print(*a, flush=True)

# ---- the graph, its faces and automorphisms (as c116_orbits.py) ----
raw = open(os.path.join(HERE, '../data/c116/Full_codes_116_Th'), 'rb').read(); data = raw[raw.index(b'<<') + 2:]
n = data[0]; adj = []; p = 1
for v in range(n):
    nb = []
    while data[p] != 0: nb.append(data[p] - 1); p += 1
    p += 1; adj.append(nb)
def face(u, v):
    f = [u]; a, b = u, v
    while True:
        k = adj[b].index(a); a, b = b, adj[b][(k + 1) % 3]
        if (a, b) == (u, v): return f
        f.append(a)
faces, seen = [], set()
for u in range(n):
    for v in adj[u]:
        if (u, v) in seen: continue
        f = face(u, v); faces.append(f)
        for a, b in zip(f, f[1:] + f[:1]): seen.add((a, b))
assert len(faces) == 60
def build_map(u0, v0, u1, v1, o):
    m = {u0: u1}; q = [(u0, v0, u1, v1)]; done = set()
    while q:
        a, b, c, d = q.pop()
        if (a, b) in done: continue
        done.add((a, b))
        if m.setdefault(b, d) != d: return None
        kb, kd = adj[b].index(a), adj[d].index(c)
        for t in (1, 2):
            x, y = adj[b][(kb + t) % 3], adj[d][(kd + o * t) % 3]
            if m.setdefault(x, y) != y: return None
            q.append((b, x, d, y))
    return m if len(m) == n and len(set(m.values())) == n else None
G = [m for u1 in range(n) for v1 in adj[u1] for o in (1, -1) for m in [build_map(0, adj[0][0], u1, v1, o)] if m]
assert len(G) == 24, len(G)
fkey = {frozenset(f): k for k, f in enumerate(faces)}
gface = [[fkey[frozenset(m[x] for x in f)] for f in faces] for m in G]
vfaces = [[k for k, f in enumerate(faces) if v in f] for v in range(n)]

# ---- 1. canonical realisation (float) ----
L = np.zeros((n, n))
for v in range(n):
    for w in adj[v]: L[v, w] = -1
    L[v, v] = 3
w_, U = np.linalg.eigh(L); P = U[:, 1:4].copy(); P /= np.linalg.norm(P, axis=1)[:, None]
edges = sorted({tuple(sorted((v, w))) for v in range(n) for w in adj[v]})
for it in range(4000):
    D = np.zeros_like(P); cs = []
    for a, b in edges:
        d = P[b] - P[a]; t = -(P[a] @ d) / (d @ d); c = P[a] + t * d; r = np.linalg.norm(c); cs.append(c)
        D[a] += (1 - r) * c / r; D[b] += (1 - r) * c / r
    P += 0.1 * D / 3; P -= 0.1 * np.mean(cs, axis=0)
    for f in faces:
        X = P[f]; c = X.mean(0); nrm = np.linalg.svd(X - c)[2][2]
        P[f] -= 0.3 * np.outer((X - c) @ nrm, nrm)
tang = max(abs(np.linalg.norm(P[a] + (-(P[a] @ (P[b] - P[a])) / ((P[b] - P[a]) @ (P[b] - P[a]))) * (P[b] - P[a])) - 1) for a, b in edges)
plan = max(abs((P[f] - P[f].mean(0)) @ np.linalg.svd(P[f] - P[f].mean(0))[2][2]).max() for f in faces)
pr(f"canonical iteration: edge tangency error {tang:.2e}, face planarity error {plan:.2e}")

# ---- symmetry frame: Procrustes matrix of each automorphism; half-turns -> coordinate axes ----
Rg = []
for m in G:
    Y = P[[m[v] for v in range(n)]]; Uu, _, Vt = np.linalg.svd(P.T @ Y); Rg.append((Uu @ Vt).T)
half = [R for R in Rg if np.linalg.det(R) > 0 and abs(np.trace(R) + 1) < 1e-3]
assert len(half) == 3, len(half)
axes = [np.linalg.eigh(R + R.T)[1][:, -1] for R in half]
F0 = np.array(axes); F0[2] = np.cross(F0[0], F0[1])
P = P @ F0.T; Rg = [F0 @ R @ F0.T for R in Rg]
S = [np.round(R).astype(int) for R in Rg]
assert all(np.abs(R - Sg).max() < 1e-3 for R, Sg in zip(Rg, S)), "automorphisms are not signed permutations in this frame"
pr("frame: T_h half-turn axes on x, y, z; every automorphism a signed permutation matrix")

# ---- Minana and the orientation ----
Dm = A.build("aequus-377"); MP = Dm["planes"]; MFk = [len(vs) for vs, k in Dm["faces"]]
mdir = np.array([[float(x) for x in u] for u, c in MP]); mdir /= np.linalg.norm(mdir, axis=1)[:, None]
def fplanes(P):
    out = []
    for f in faces:
        X = P[f]; c = X.mean(0); nrm = np.linalg.svd(X - c)[2][2]
        if nrm @ c < 0: nrm = -nrm
        out.append(nrm / (nrm @ c))           # plane nrm . x = 1
    return np.array(out)
pent = [k for k, f in enumerate(faces) if len(f) == 5]; sq = [t for t, k in enumerate(MFk) if k == 4]
def score(P):
    N = fplanes(P); N = N / np.linalg.norm(N, axis=1)[:, None]
    return sum(max(N[k] @ mdir[t] for t in sq) for k in pent)
turn = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
if score(P @ turn.T) > score(P):
    P = P @ turn.T; S = [turn @ Sg @ turn.T for Sg in S]; pr("core turned 90 degrees about z (other T_h frame)")

# ---- exact rational planes, orbit by orbit ----
N = fplanes(P); planes = [None] * 60; orbit_of = [None] * 60
for k in range(60):
    if planes[k] is not None: continue
    stab = [g for g in range(24) if gface[g][k] == k]
    nk = np.mean([S[g] @ N[k] for g in stab], axis=0)
    r = [Fr(int(round(x * 10**6)), 10**6) for x in nk]
    for g in range(24):
        j = gface[g][k]
        img = [sum(int(S[g][i, t]) * r[t] for t in range(3)) for i in range(3)]
        if planes[j] is None: planes[j] = img; orbit_of[j] = k
        else: assert planes[j] == img, "orbit image inconsistent"
planes = [([Q(x) for x in nv], Q(1)) for nv in planes]
V = []
for v in range(n):
    a, b, c = (planes[k][0] for k in vfaces[v]); Dt = det3(a, b, c); assert Dt.sign() != 0
    cx, cy, cz = cross(b, c), cross(c, a), cross(a, b)
    V.append([(cx[t] + cy[t] + cz[t]) / Dt for t in range(3)])
bad = [(v, k) for v in range(n) for k in range(60) if k not in vfaces[v] and (dot(planes[k][0], V[v]) - 1).sign() >= 0]
assert not bad, f"corner outside or on a non-incident plane: {bad[:5]}"
pr("EXACT: 60 rational planes, T_h-symmetric by construction; the 116 corners lie strictly inside every non-incident plane: C116 realised")
fcs = []
for f in faces:   # orient each face outward (counterclockwise seen from outside)
    nrm = cross([V[f[1]][t] - V[f[0]][t] for t in range(3)], [V[f[2]][t] - V[f[0]][t] for t in range(3)])
    fcs.append((f if dot(nrm, V[f[0]]).sign() > 0 else f[::-1], {5: "pent", 6: "hex"}[len(f)]))

# ---- 3. pairing ----
cdir = np.array([[float(x) for x in u] for u, c in planes]); cdir /= np.linalg.norm(cdir, axis=1)[:, None]
corb = {}
for k in range(60): corb.setdefault(orbit_of[k], []).append(k)
morb = {}
for t in range(60):
    rep = min(t2 for t2 in range(60) if any(np.abs(mdir[t2] - (S[g] @ mdir[t])).max() < 1e-9 for g in range(24)))
    morb.setdefault(rep, []).append(t)
co = sorted(corb.values(), key=lambda o: (len(o), len(faces[o[0]]))); mo = sorted(morb.values(), key=lambda o: (len(o), MFk[o[0]]))
pr("core orbits:", [(len(o), len(faces[o[0]])) for o in co], " Minana orbits:", [(len(o), MFk[o[0]]) for o in mo])
c12p = [o for o in co if len(o) == 12 and len(faces[o[0]]) == 5][0]; c12h = [o for o in co if len(o) == 12 and len(faces[o[0]]) == 6]
c24 = [o for o in co if len(o) == 24][0]
m4 = [o for o in mo if MFk[o[0]] == 4][0]; m7 = [o for o in mo if MFk[o[0]] == 7][0]
m6 = [o for o in mo if len(o) == 12 and MFk[o[0]] == 6][0]; m24 = [o for o in mo if len(o) == 24][0]
def pair(cs, ms):
    out, tot = {}, 0.0
    for k in cs:
        t = max(ms, key=lambda t: cdir[k] @ mdir[t]); out[k] = t; tot += cdir[k] @ mdir[t]
    return out, tot, len(set(out.values())) == len(ms)
best = None
for h7, h6 in (c12h, c12h[::-1]):
    parts = [pair(c12p, m4), pair(h7, m7), pair(h6, m6), pair(c24, m24)]
    tot = sum(x[1] for x in parts); ok = all(x[2] for x in parts)
    if ok and (best is None or tot > best[0]): best = (tot, {k: t for x in parts for k, t in x[0].items()})
assert best, "no bijective pairing by nearest direction"
# ---- best pairing by neighbours: every T_h-equivariant bijection (sigma(g F) = S_g sigma(F)), the one keeping most adjacencies ----
cadj = {frozenset((k, j)) for k in range(60) for j in range(60) if k < j and len(set(faces[k]) & set(faces[j])) == 2}
mverts = [vs for vs, kk in Dm["faces"]]
madj = {frozenset((k, j)) for k in range(60) for j in range(60) if k < j and len(set(mverts[k]) & set(mverts[j])) == 2}
assert len(cadj) == len(madj) == 174, (len(cadj), len(madj))
def mimg(g, t):   # Minana face index of S_g applied to face t
    v = S[g] @ mdir[t]; return int(np.argmax(mdir @ v))
Mg = [[mimg(g, t) for t in range(60)] for g in range(24)]
def equivariant_choices(o, mo_):
    k = o[0]; stab = [g for g in range(24) if gface[g][k] == k]
    out = []
    for t in mo_:
        if all(Mg[g][t] == t for g in stab):
            sig = {}
            for g in range(24):
                j, u = gface[g][k], Mg[g][t]
                if sig.setdefault(j, u) != u: break
            else:
                if len(set(sig.values())) == len(o): out.append(sig)
    return out
bestA = None
for h7, h6 in (c12h, c12h[::-1]):
    ch = [equivariant_choices(c12p, m4), equivariant_choices(h7, m7), equivariant_choices(h6, m6), equivariant_choices(c24, m24)]
    for combo in itertools.product(*ch):
        sig = {}
        for d_ in combo: sig.update(d_)
        keep = sum(1 for e in cadj if frozenset(sig[x] for x in e) in madj)
        if bestA is None or keep > bestA[0]: bestA = (keep, sig)
pr(f"choices per orbit {[len(c) for c in ch]}; best equivariant pairing keeps {bestA[0]} of 174 neighbour pairs (nearest-direction pairing kept "
   f"{sum(1 for e in cadj if frozenset(best[1][x] for x in e) in madj)})")
ASSIGN = bestA[1] if os.environ.get('PAIR', 'adjacency') == 'adjacency' else best[1]
ang = [np.degrees(np.arccos(np.clip(cdir[k] @ mdir[t], -1, 1))) for k, t in ASSIGN.items()]
pr(f"PAIRING: bijection core face -> Minana face (pentagon->square, hexagon->heptagon/hexagon, 24->24); angle between paired normals max {max(ang):.2f} deg, mean {np.mean(ang):.2f} deg")

# ---- 4. the cell ----
H1 = [(u, c) for (u, c) in MP]
def shell(lat, s): return [(u, s * c) for (u, c) in H1]
Z = Q(0); vol = Z
for mi, poly in A.mould_faces(H1):
    for q in range(1, len(poly) - 1):
        d = det3(poly[0], poly[q], poly[q + 1]); vol = vol + (d if d.sign() > 0 else -d)
A.CELLVOL["minana"] = vol / 6; A.shell = shell; A.ASSIGN = ASSIGN
A.build = lambda name: dict(V=V, faces=fcs, planes=planes, name=name)
sys.argv = [argv[0], "c116", "minana", argv[1], "cen"]
A.main()
