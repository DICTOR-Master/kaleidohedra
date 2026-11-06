"""Route (c), the middle slice (DICTO 11-06: "or parts of the 120 and 600 or mid structure"; UNITY = DICTO's 13-cell, icosidodecahedron +
12 J11 on its pentagons, "sounds perfect"). The 600-cell's equatorial slice is the icosidodecahedron (ID). Each J11 (gyroelongated
pentagonal pyramid) + its pentagonal cap (J2) = an icosahedron; the caps point into the ID. Checks: the 12 icosahedra (J11 + cap) are
regular; whether the 12 caps overlap inside the ID; the ID's own core (ID minus the caps); a five-solid nest in every icosahedron
(I > D > C > T, with O through six of I's edge midpoints) and in the ID's core."""
import itertools, json, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
ID = np.vstack([orbit((0, 0, phi)), orbit((0.5, phi / 2, phi * phi / 2))])     # edge 1
def faces(V, r=6):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, r)), set()).update(sp)
    return [(np.array(k[:3]), -k[3], V[list(s)]) for k, s in F.items()]
def edges(V):
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); e = D_[D_ > 1e-9].min()
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D_[i, j] - e) < 1e-6]
def inside(a, b):
    h = ConvexHull(b); return bool(((a @ h.equations[:, :3].T + h.equations[:, 3]) <= 1e-7).all())
pents = [f for f in faces(ID) if len(f[2]) == 5]
print(f"ID: {len(ID)} corners, edge {min(np.linalg.norm(ID[i]-ID[j]) for i,j in edges(ID)):.6f}, {len(pents)} pentagons")
# icosahedron on each pentagon: the pentagon is a vertex ring; cap apex inside (toward the centre), the rest outside
R5 = 1 / (2 * np.sin(np.pi / 5)); hcap = np.sqrt(1 - R5 ** 2)          # J2 height
icos = []; caps = []
for n, d, P in pents:
    c = P.mean(0); apex_in = c - hcap * n
    # the opposite ring: the pentagon turned 36 deg, at distance (ring spacing) outward; and the far apex
    u = P - c
    th = np.pi / 5; Rt = lambda v: v * np.cos(th) + np.cross(n, v) * np.sin(th) + n * (n @ v) * (1 - np.cos(th))
    ring_gap = np.sqrt(1 - (2 * R5 * np.sin(np.pi / 10)) ** 2 - 0) if False else None
    # icosahedron of edge 1: ring-to-ring height = sqrt(1 - (R5 - R5*cos36... )): solve from edge between rings
    a = np.array([R5, 0, 0]); b = np.array([R5 * np.cos(np.pi / 5), R5 * np.sin(np.pi / 5), 0]); hr = np.sqrt(1 - np.sum((a - b)[:2] ** 2))
    P2 = np.array([Rt(v) for v in u]) + c + hr * n
    apex_out = c + (hr + hcap) * n
    I = np.vstack([P, P2, apex_in, apex_out]); icos.append(I); caps.append(np.vstack([P, apex_in]))
ok_reg = all(len(edges(I)) == 30 and abs(min(np.linalg.norm(I[i] - I[j]) for i, j in edges(I)) - 1) < 1e-6 for I in icos)
print("12 icosahedra (J11 + cap) regular, edge 1:", ok_reg)
def overlap_vol(A, B, N=60000, seed=0):
    rng = np.random.default_rng(seed); lo = np.minimum(A.min(0), B.min(0)); hi = np.maximum(A.max(0), B.max(0))
    X = rng.uniform(lo, hi, (N, 3)); hA, hB = ConvexHull(A), ConvexHull(B)
    inA = ((X @ hA.equations[:, :3].T + hA.equations[:, 3]) <= 0).all(1); inB = ((X @ hB.equations[:, :3].T + hB.equations[:, 3]) <= 0).all(1)
    return (inA & inB).mean() * np.prod(hi - lo)
ov_caps = max(overlap_vol(caps[a], caps[b]) for a, b in itertools.combinations(range(12), 2))
ov_ico = max(overlap_vol(icos[a], icos[b]) for a, b in itertools.combinations(range(12), 2))
print(f"largest overlap: caps {ov_caps:.5f}, icosahedra {ov_ico:.5f}")
apex = np.array([c[-1] for c in caps]); print(f"cap apexes at distance {np.linalg.norm(apex[0]):.6f} from the centre; they form a regular icosahedron:", len(edges(apex)) == 30)
vID = ConvexHull(ID).volume; vcap = ConvexHull(caps[0]).volume
print(f"ID volume {vID:.6f}; 12 caps {12*vcap:.6f}; ID core (ID minus caps, if disjoint) {vID - 12*vcap:.6f}")
# nests in the icosahedra: I > D (face centres) > C (8 of D's corners) > T; O through six of I's edge midpoints
def nest_I(I):
    c = I.mean(0); D = np.array([f[2].mean(0) for f in faces(I, 5)])
    mids = np.array([(I[i] + I[j]) / 2 for i, j in edges(I)]) - c; O = None
    for a, b, e in itertools.combinations(range(len(mids)), 3):
        u = mids[[a, b, e]]; r = np.linalg.norm(u, axis=1)
        if np.allclose(r, r[0], atol=1e-6) and max(abs(u[0] @ u[1]), abs(u[0] @ u[2]), abs(u[1] @ u[2])) < 1e-5: O = np.vstack([u, -u]) + c; break
    ax = (O[:3] - c) / np.linalg.norm(O[0] - c); co = (D - c) @ ax.T
    C = D[np.all(np.isclose(np.abs(co), np.abs(co[:, :1]), atol=1e-6), axis=1)]
    dd = np.linalg.norm(C - C[0], axis=1); fd = np.sort(np.unique(np.round(dd, 6)))[2]   # face diagonal
    T = C[np.isclose(dd, 0) | np.isclose(dd, fd, atol=1e-5)]
    return {'O': O, 'D': D, 'C': C, 'T': T}
nests = [nest_I(I) for I in icos]
okn = all(len(n['C']) == 8 and len(n['T']) == 4 and len(edges(n['T'])) == 6 and len(edges(n['C'])) == 12 and inside(n['D'], I) and inside(n['C'], n['D']) and inside(n['T'], n['C']) and inside(n['O'], I) for n, I in zip(nests, icos))
print("every icosahedron holds D > C > T and O, all inside:", okn)
json.dump({'ID': ID.tolist(), 'icos': [I.tolist() for I in icos], 'caps': [c.tolist() for c in caps], 'nests': [{k: v.tolist() for k, v in n.items()} for n in nests]}, open('../unity-nests.json', 'w'))
print("FINAL", "ok" if ok_reg and okn else "FAIL")
