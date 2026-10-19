# Universal PiTet (UP), DICTO 2026-10-19: data for the UP world (src/app/up-data.js). The geometry and its exact proofs are in the research
# study studies/2026-10-19-five-fold-octet (exact_cycle.py, exact_shells.py, exact_inner.py): from the Cleo star outward, then a cycle of
# four shells, ID -> RT -> golden truncated icosahedron -> Q -> ID x 10/phi^4, without end. Rule of the cycle: each next solid has its
# faces through the last one's corners, at right angles to them. Built here in float in the study's frame (icosahedron of edge 1);
# the build re-checks every view: pieces' volumes add up to their solids (1e-9).
# Views: shells (Cleo star to the second ID, 308 pieces), vajras (the 12 five-sided Vajras on the core), hexcleo (ID -> OG -> RT with
# the 20 hexagonal Cleos). The cycle's film is its own world (world-up-film.js, data up-film-data.js, built here too).
import itertools, json, os
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

PHI = (1 + 5 ** .5) / 2; K = 10 / PHI ** 4
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'app', 'up-data.js')
hv = lambda P: ConvexHull(np.asarray(P)).volume
def uniq(P): P = np.asarray(P); return P[np.unique(np.round(P, 9), axis=0, return_index=True)[1]]
def planes(V):
    q = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, w, atol=1e-7) for w in q): q.append(e)
    q = np.array(q); return q[:, :3], -q[:, 3]
def faces(V):
    """Faces of the convex hull as ordered corner lists (coplanar triangles merged)."""
    V = np.asarray(V); n, d = planes(V); out = []
    for k in range(len(d)):
        idx = [i for i in range(len(V)) if abs(V[i] @ n[k] - d[k]) < 1e-7]
        P = V[idx]; c = P.mean(0); a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(n[k], a)
        out.append([idx[i] for i in np.argsort(np.arctan2((P - c) @ b, (P - c) @ a))])
    return out
def piece(role, V): V = uniq(V); return [role, np.round(V, 6).tolist(), faces(V)]
def nxt(S):
    r = np.linalg.norm(S, axis=1); return uniq(HalfspaceIntersection(np.hstack([S / r[:, None], -r[:, None]]), np.zeros(3)).intersections)
def cone_pieces(S, N, role_of):
    """One piece per face of S: the cone from the centre over that face, cut by N and by the face's plane."""
    nS, dS = planes(S); nN, dN = planes(N); out = []
    for k in range(len(dS)):
        F = S[np.abs(S @ nS[k] - dS[k]) < 1e-9]; c = F.mean(0); B = np.linalg.svd(F - c)[2][:2]
        F = F[np.argsort(np.arctan2((F - c) @ B[1], (F - c) @ B[0]))]
        hs = [np.r_[nN[i], -dN[i]] for i in range(len(dN))] + [np.r_[-nS[k], dS[k]]]
        for i in range(len(F)):
            m = np.cross(F[i], F[(i + 1) % len(F)]); m /= np.linalg.norm(m); m = m if m @ c > 0 else -m; hs.append(np.r_[-m, 0])
        out.append(piece(role_of(len(F)), HalfspaceIntersection(np.array(hs), c + nS[k] * 1e-3).intersections))
    return out
def check(name, pieces, inner_vol, outer):
    tot = sum(hv(p[1]) for p in pieces if p[0] not in GLASS_ONLY)
    assert abs(tot + inner_vol - hv(outer)) < 1e-6 * hv(outer), (name, tot + inner_vol, hv(outer))
GLASS_ONLY = {'upCoreGlass', 'upIDGlass'}

# the frame: icosahedron of edge 1, 5-fold axes on its corners
z = 0.0
I = np.array([v for a, b in ((0.5, PHI / 2),) for v in [(z, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)] +
              [(sb * b, z, sa * a) for sa in (1, -1) for sb in (1, -1)] + [(sa * a, sb * b, z) for sa in (1, -1) for sb in (1, -1)]])
hI = ConvexHull(I); tri = [I[s] for s in hI.simplices]
tips = np.array([2 * t.mean(0) for t in tri]); Dp = tips                                   # D': the spike tips
ID = uniq([p + q for t in tri for p, q in itertools.combinations(t, 2)])                  # twice the edge midpoints, radius phi
u5 = I / np.linalg.norm(I, axis=1)[:, None]
RT, T, Q = nxt(ID), None, None; T = nxt(RT); Q = nxt(T); ID2 = nxt(Q)
assert np.max(np.linalg.norm(ID2[:, None] - (ID * K)[None], axis=2).min(1)) < 1e-9          # the cycle closes at 10/phi^4
A5 = np.array([v for v in RT if np.max(np.abs(v @ u5.T)) / np.linalg.norm(v) > 1 - 1e-9]); A3 = np.array([v for v in RT if v.tolist() not in A5.tolist()])

# ---- stage 1: the Cleo star ----
cleo = [piece('upCleo', np.vstack([t, [[0, 0, 0]]])) for t in tri]
spikes = [piece('upCleo', np.vstack([t, [tp]])) for t, tp in zip(tri, tips)]
nD, dD = planes(Dp); pyr = []
for k in range(len(dD)):
    base = Dp[np.abs(Dp @ nD[k] - dD[k]) < 1e-9]; pyr.append(piece('upInPyr5', np.vstack([base, [I[np.argmax(I @ nD[k])]]])))
val = []
for i, j in [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(np.linalg.norm(I[i] - I[j]) - 1) < 1e-9]:
    two = [tp for s, tp in zip(hI.simplices, tips) if i in s and j in s]; val.append(piece('upCValley', [I[i], I[j], *two]))
check('Cleo star', cleo + spikes + pyr + val, 0, Dp)
# ---- stage 2: D' -> ID, 12 twisted frusta ----
fr = []
for k in range(len(dD)):
    base = Dp[np.abs(Dp @ nD[k] - dD[k]) < 1e-9]; fr.append(piece('upFrustum', np.vstack([base, ID[np.argsort(-(ID @ nD[k]))[:5]]])))
check('D\' -> ID', fr, hv(Dp), ID)
# ---- stage 3: ID -> RT, fine cut ----
nI, dI = planes(ID); fine = []
for k in range(len(dI)):
    F = ID[np.abs(ID @ nI[k] - dI[k]) < 1e-9]; Ap = A5 if len(F) == 5 else A3
    fine.append(piece('upPyr5' if len(F) == 5 else 'upPyr3', np.vstack([F, [Ap[np.argmax(Ap @ nI[k])]]])))
e = min(np.linalg.norm(a - b) for a, b in itertools.combinations(ID, 2))
for i, j in [(i, j) for i, j in itertools.combinations(range(30), 2) if abs(np.linalg.norm(ID[i] - ID[j]) - e) < 1e-9]:
    m = (ID[i] + ID[j]) / 2; a5 = A5[np.argmax(A5 @ m / np.linalg.norm(A5, axis=1))]; a3 = A3[np.argmax(A3 @ m / np.linalg.norm(A3, axis=1))]
    fine.append(piece('upValley', [ID[i], ID[j], a5, a3]))
check('ID -> RT fine', fine, hv(ID), RT)
# ---- the cycle's shells (cone pieces) ----
def turn(s, idpieces='cone'):
    """One turn of the cycle at scale s (ID*s -> ID*s*K)."""
    out = []
    out += cone_pieces(ID * s, RT * s, lambda n: 'upCone5' if n == 5 else 'upCone3') if idpieces == 'cone' else []
    out += cone_pieces(RT * s, T * s, lambda n: 'upRhomb')
    out += cone_pieces(T * s, Q * s, lambda n: 'upPent' if n == 5 else 'upHex')
    out += cone_pieces(Q * s, ID2 * s, lambda n: 'upTri')
    return out
outer1 = turn(1, idpieces='fine')
check('RT -> ID2', outer1, hv(RT), ID2)
shells = cleo + spikes + pyr + val + fr + fine + outer1
# ---- the Vajras ----
vaj = []
for u in u5:
    ip = I[np.argmax(I @ u)]; df = Dp[np.argsort(-(Dp @ u))[:5]]; idp = ID[np.argsort(-(ID @ u))[:5]]; ap = A5[np.argmax(A5 @ u)]
    V = np.vstack([[ip], df, idp, [ap]]); vaj.append(piece('upVajra', V))
    parts = hv(np.vstack([[ip], df])) + hv(np.vstack([df, idp])) + hv(np.vstack([idp, [ap]]))
    assert abs(hv(V) - parts) < 1e-9                                                       # convex: exactly its three parts
vajras = cleo + vaj
# ---- the hexagonal Cleo stage: ID -> OG -> RT ----
nI3 = [k for k in range(len(dI)) if np.sum(np.abs(ID @ nI[k] - dI[k]) < 1e-9) == 3]
X = uniq([2 * ID[np.abs(ID @ nI[k] - dI[k]) < 1e-9].mean(0) - v for k in nI3 for v in ID[np.abs(ID @ nI[k] - dI[k]) < 1e-9]])
apex = []
for a5 in A5:
    u = a5 / np.linalg.norm(a5); cs = ID[np.argsort(-(ID @ u))[:5]]; xs = X[np.argsort(-(X @ u))[:5]]; c0 = cs[0]
    x2 = xs[np.argsort(np.linalg.norm(xs - c0, axis=1))[:2]]; n = np.cross(x2[0] - c0, x2[1] - c0); apex.append(u * (n @ c0) / (n @ u))
OG = np.vstack([ID, X, apex]); assert len(uniq(OG)) == 102
low, caps, hexc, tets = [], [], [], []
for a5, ap in zip(A5, apex):
    u = a5 / np.linalg.norm(a5); cs = ID[np.argsort(-(ID @ u))[:5]]; xs = X[np.argsort(-(X @ u))[:5]]
    L = np.vstack([cs, xs, [ap]]); low.append(piece('upLow', L))
    # the dimpled cap over this low piece is exactly 5 pyramids from the RT's five-fold corner over the OG's 5 kites (DICTO 2026-10-19:
    # drawn as one piece its rim was open); their volumes add up to hull(cap) minus the low piece, checked below
    LV = uniq(L)
    for f in faces(LV):
        if len(f) == 4: caps.append(piece('upKitePyr', np.vstack([LV[f], [a5]])))
nO, dO = planes(OG)
for k in range(len(dO)):
    F = OG[np.abs(OG @ nO[k] - dO[k]) < 1e-9]
    if len(F) == 6: hexc.append(piece('upHexCleo', np.vstack([F, [A3[np.argmax(A3 @ nO[k])]]])))
for x in X:
    a5 = A5[np.argmax(A5 @ x / np.linalg.norm(A5, axis=1))]; a3 = A3[np.argmax(A3 @ x / np.linalg.norm(A3, axis=1))]
    for c in ID[np.argsort(np.linalg.norm(ID - x, axis=1))[:2]]: tets.append(piece('upTet', [c, x, a5, a3]))
capvol = sum(hv(uniq(np.vstack([ID[np.argsort(-(ID @ (a / np.linalg.norm(a))))[:5]], X[np.argsort(-(X @ (a / np.linalg.norm(a))))[:5]], [a]]))) for a in A5) - sum(hv(p[1]) for p in low)
assert abs(sum(hv(p[1]) for p in low) + hv(ID) - hv(OG)) < 1e-5   # pieces are stored to 6 decimals
assert abs(sum(hv(p[1]) for p in hexc + tets) + capvol + hv(OG) - hv(RT)) < 1e-5
idglass = piece('upIDGlass', ID)
assert abs(sum(hv(p[1]) for p in caps) - capvol) < 1e-5 and len(caps) == 60
hexcleo = [idglass] + low + hexc + caps + tets
# Colour by shape (DICTO 2026-10-19): one role per shape, whatever its size or turn; mirror images count as one shape.
def sig(V):
    D = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(np.array(V), 2)); return (len(V), tuple(np.round(np.array(D) / D[-1], 4)))
shape_of = {}
for r, V, F in shells + vajras + hexcleo:
    if r not in GLASS_ONLY: shape_of.setdefault(r, set()).add(sig(V))     # the ID glass of the hexagonal view is the cycle's ID
assert all(len(s) == 1 for s in shape_of.values()), {r: len(s) for r, s in shape_of.items() if len(s) > 1}
assert len({next(iter(s)) for r, s in shape_of.items()}) == len(shape_of)       # every role a different shape
# ---- the film world's data (world-up-film.js, cloned from Vajrayana's cycle; DICTO 2026-10-19 "Dual Vision is the standard"): the stations
# of one turn and, for the pieces toggle, each shell's pieces keyed by the station that closes it (they peel with it)
def solid_of(S): S = uniq(S); return {'v': np.round(S, 6).tolist(), 'f': faces(S)}
film_pieces = {'RT': cone_pieces(ID, RT, lambda n: 'p'), 'GTI': cone_pieces(RT, T, lambda n: 'p'), 'FPD': cone_pieces(T, Q, lambda n: 'p'),
               'IDk': cone_pieces(Q, ID2, lambda n: 'p')}
film = {'K': K, 'stations': {'ID': solid_of(ID), 'RT': solid_of(RT), 'GTI': solid_of(T), 'FPD': solid_of(Q)},
        'pieces': {k: [{'v': p[1], 'f': p[2]} for p in v] for k, v in film_pieces.items()},
        'cleo': [{'v': p[1], 'f': p[2], 'spike': k >= 20} for k, p in enumerate(cleo + spikes)],   # the Cleo star at the centre (DICTO)
        'view': {'dir': [0.45, 0.35, 1.0], 'up': [0.0, 1.0, 0.0]}, 'radius': float(np.linalg.norm(ID2, axis=1).max())}
with open(os.path.join(os.path.dirname(OUT), 'up-film-data.js'), 'w') as f:
    f.write('// Built by scripts/build-up-data.py (Universal PiTet film, DICTO 2026-10-19). Do not edit.\nexport default ' + json.dumps(film, separators=(',', ':')) + ';\n')
data = {'up': {'views': {'shells': shells, 'vajras': vajras, 'hexcleo': hexcleo, }, 'K': K, 'turnRadius': float(np.linalg.norm(RT, axis=1).max())}}
with open(OUT, 'w') as f:
    f.write('// Built by scripts/build-up-data.py (Universal PiTet, DICTO 2026-10-19). Do not edit.\nexport default ' + json.dumps(data, separators=(',', ':')) + ';\n')
print({k: len(v) for k, v in data['up']['views'].items()}, 'bytes', os.path.getsize(OUT))
