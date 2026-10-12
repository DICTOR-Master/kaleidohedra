# Bodhi seed (DICTO, discovery #24): shared geometry for the gap-piece study (2026-10-12).
# Frame: the icosahedron of network_screen.py (all forms share its turn). Edge-1 rhombic triacontahedron RT(1) = zonotope of the
# six 5-fold unit vectors E6 (segments of length 1), so its 5-fold corners sit at distance phi, its 3-fold corners at 1.473606 and
# its faces (normals = the 15 two-fold axes) at the inradius 1.376382. The seed: outer RT(phi^2); 12 copies RT(1) + phi^2 u for the
# 12 five-fold unit vectors u; centre RT(1/phi). Everything is a golden zonotope: all face planes have one of the 15 two-fold
# directions as normal, so the separating-axis test needs only those 15 axes (exact).
import os, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__))
PHI = (1 + 5 ** .5) / 2
EPS = 1e-9

def cyc(v):
    out = set()
    for s in itertools.product(*[(-1, 1) if x else (1,) for x in v]):
        w = [a * b for a, b in zip(v, s)]
        for k in range(3): out.add(tuple(np.round(np.roll(w, k), 12)))
    return out
_I = np.array(sorted(cyc((0, 1, PHI))), float)
U12 = _I / np.linalg.norm(_I, axis=1)[:, None]                      # the 12 five-fold unit vectors
E6 = []
for u in U12:
    if not any(abs(abs(u @ w) - 1) < 1e-9 for w in E6): E6.append(u)
E6 = np.array(E6); assert len(E6) == 6
N15 = []                                                              # the 15 two-fold unit axes = face normals of every RT
for a, b in itertools.combinations(E6, 2):
    n = np.cross(a, b); N15.append(n / np.linalg.norm(n))
N15 = np.array(N15)
TRIANGLES = [t for t in itertools.combinations(range(12), 3)          # the 20 faces of the icosahedron (mutually adjacent)
             if all(abs(U12[i] @ U12[j] - 1 / 5 ** .5) < 1e-9 for i, j in itertools.combinations(t, 2))]
assert len(TRIANGLES) == 20
U20 = np.array([U12[list(t)].sum(0) for t in TRIANGLES]); U20 /= np.linalg.norm(U20, axis=1)[:, None]   # 3-fold axes
U30 = []                                                              # 2-fold unit axes (30, both signs)
for n in N15: U30 += [n, -n]
U30 = np.array(U30)
P_VOL = abs(np.linalg.det(U12[list(TRIANGLES[0])]))                   # prolate golden rhombohedron, edge 1
O_VOL = P_VOL / PHI                                                   # oblate, edge 1

def zonotope(scale=1.0, centre=(0, 0, 0)):
    """RT(scale): hull of (scale/2) * sum(+-e_j) over all sign choices; returns its 32 corners."""
    pts = np.array([scale / 2 * (np.array(s) @ E6) for s in itertools.product((-1, 1), repeat=6)])
    H = ConvexHull(pts); V = pts[H.vertices] + np.asarray(centre, float)
    assert len(V) == 32, len(V)
    return V

def dedupe_planes(E, tol=1e-7):
    out = []
    for e in E:
        if not any(np.linalg.norm(e - q) < tol for q in out): out.append(np.array(e, float))
    return out

def planes_of(V):
    """Halfspaces n.x + d <= 0 of the convex hull of V (merged coplanar facets)."""
    return dedupe_planes(ConvexHull(V).equations)

def interior(H):
    A = np.array(H); n = np.linalg.norm(A[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], n], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    return (r.x[:3], r.x[3]) if r.success else (None, 0.0)

def verts(H, tol=1e-7):
    x, r = interior(H)
    if x is None or r < 1e-7: return None
    V = HalfspaceIntersection(np.array(H), x).intersections
    out = []
    for v in V:
        if all(np.linalg.norm(v - w) > tol for w in out): out.append(v)
    return np.array(out)

def side_range(H, p):
    A = np.array(H)
    lo = linprog(p[:3], A_ub=A[:, :3], b_ub=-A[:, 3], bounds=[(None, None)] * 3, method='highs')
    hi = linprog(-p[:3], A_ub=A[:, :3], b_ub=-A[:, 3], bounds=[(None, None)] * 3, method='highs')
    return lo.fun + p[3], -hi.fun + p[3]

def bsp(start, planes):
    """Cut the convex cell(s) `start` (lists of halfspaces) by every plane; return the cells (lists of halfspaces)."""
    cells = [list(c) for c in start]
    for e in planes:
        nxt = []
        for H in cells:
            lo, hi = side_range(H, e)
            if lo < -1e-7 and hi > 1e-7: nxt += [H + [e], H + [-e]]
            else: nxt.append(H)
        cells = nxt
    return cells

def inside_poly(x, P, tol=-1e-9):
    return all(x @ e[:3] + e[3] < tol for e in P)

def vol(V):
    return ConvexHull(V).volume if len(V) >= 4 else 0.0

def sat_separated(A, B, tol=1e-7):
    """Interiors disjoint? exact for polytopes whose edges all run along the six 5-fold directions (axes = the 15 two-fold normals)."""
    pa, pb = A @ N15.T, B @ N15.T
    return bool(np.any((pa.max(0) <= pb.min(0) + tol) | (pb.max(0) <= pa.min(0) + tol)))

def sat_separated_general(A, B, tol=1e-7):
    """Separating-axis test with face normals and edge cross products of both hulls (for any pair of convex polytopes)."""
    HA, HB = ConvexHull(A), ConvexHull(B)
    axes = list(HA.equations[:, :3]) + list(HB.equations[:, :3])
    def edges(H, V):
        E = set()
        for s in H.simplices:
            for i, j in itertools.combinations(sorted(s), 2): E.add((i, j))
        return [V[i] - V[j] for i, j in E]
    for u in edges(HA, A):
        for v in edges(HB, B):
            w = np.cross(u, v); n = np.linalg.norm(w)
            if n > 1e-9: axes.append(w / n)
    for ax in axes:
        a, b = A @ ax, B @ ax
        if a.max() <= b.min() + tol or b.max() <= a.min() + tol: return True
    return False

def _group():
    I = U12; G = []
    e = min(np.linalg.norm(I[0] - w) for w in I[1:])
    nb = [m for m in range(12) if abs(np.linalg.norm(I[m] - I[0]) - e) < 1e-6]
    b_ = nb[0]; c_ = [m for m in nb if abs(np.linalg.norm(I[m] - I[b_]) - e) < 1e-6][0]
    Ai = np.linalg.inv(np.array([I[0], I[b_], I[c_]]).T)
    for i, j, k in itertools.permutations(range(12), 3):
        R = np.array([I[i], I[j], I[k]]).T @ Ai
        if np.allclose(R @ R.T, np.eye(3), atol=1e-6) and all(np.min(np.linalg.norm(I - y, axis=1)) < 1e-6 for y in I @ R.T): G.append(R)
    return G
GROUP = _group(); assert len(GROUP) == 120

# ---- the seed ----
RT1 = zonotope(1.0)
OUTER = zonotope(PHI ** 2)
CENTRE = zonotope(1 / PHI)
COPIES = [zonotope(1.0, PHI ** 2 * u) for u in U12]
SOLIDS = COPIES + [CENTRE]
F_OUTER = planes_of(OUTER)
F_SOLIDS = [planes_of(S) for S in SOLIDS]
RT_VOL = vol(RT1)
GAP_VOL = vol(OUTER) - 12 * RT_VOL - vol(CENTRE)
R5, R3, RIN = PHI, np.linalg.norm(RT1, axis=1).min(), -F_OUTER[0][3] / PHI ** 2

def rhombohedron(t):
    """Prolate golden rhombohedron [0,1]e_a + [0,1]e_b + [0,1]e_c on icosahedron face t (its 8 corners)."""
    a, b, c = U12[list(t)]
    return np.array([i * a + j * b + k * c for i in (0, 1) for j in (0, 1) for k in (0, 1)])
RH20 = [rhombohedron(t) for t in TRIANGLES]                          # the rhombic hexecontahedron RH(1), 20 blocks at the origin

def chamber():
    """One fundamental cone of the full group: 5-fold axis U12[0], the 3-fold axis of a face on it, the 2-fold axis between."""
    u5 = U12[0]
    t = [t for t in TRIANGLES if 0 in t][0]; u3 = U20[TRIANGLES.index(t)]
    others = [i for i in t if i != 0]
    m = U12[0] + U12[others[0]]; u2 = m / np.linalg.norm(m)
    def cone_plane(a, b, c):
        n = np.cross(a, b); n = n / np.linalg.norm(n)
        if n @ c > 0: n = -n
        return np.r_[n, 0.0]
    return u5, u3, u2, [cone_plane(u5, u3, u2), cone_plane(u3, u2, u5), cone_plane(u2, u5, u3)]

def stabiliser(ax):
    return [g for g in GROUP if np.linalg.norm(g @ ax - ax) < 1e-9]

def key(v, nd=6):
    return tuple(np.round(np.asarray(v) + 0.0, nd))

def canon(V, nd=5):
    return tuple(sorted(key(v, nd) for v in V))

def congruence_sig(V, nd=5):
    """Congruence class signature: corner count, volume, sorted pairwise distances."""
    V = np.asarray(V)
    d = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2))
    return (len(V), round(vol(V), nd), tuple(np.round(d, nd)))

def hull_corners(V):
    H = ConvexHull(V); return V[H.vertices]

def faces_of(V, tol=1e-7):
    """Faces of the convex polytope with corners V: list of (plane, corner indices in cyclic order)."""
    out = []
    for e in planes_of(V):
        idx = [i for i, v in enumerate(V) if abs(v @ e[:3] + e[3]) < tol]
        c = V[idx].mean(0); n = e[:3]
        a = V[idx[0]] - c; a -= (a @ n) * n; a /= np.linalg.norm(a); b = np.cross(n, a)
        ang = [np.arctan2((V[i] - c) @ b, (V[i] - c) @ a) for i in idx]
        out.append((e, [idx[k] for k in np.argsort(ang)]))
    return out

def dihedrals(V):
    """Dihedral angles (degrees) at the edges of the convex polytope with corners V, as {(i,j): angle}."""
    F = faces_of(V); out = {}
    for (e1, f1), (e2, f2) in itertools.combinations(F, 2):
        shared = sorted(set(f1) & set(f2))
        if len(shared) == 2:
            out[tuple(shared)] = float(np.degrees(np.pi - np.arccos(np.clip(e1[:3] @ e2[:3], -1, 1))))
    return out

def describe(V, name='piece'):
    V = hull_corners(np.asarray(V))
    F = faces_of(V); ds = dihedrals(V)
    el = sorted(set(round(np.linalg.norm(V[i] - V[j]), 6) for (i, j) in ds))
    lines = [f'{name}: {len(V)} corners, {len(ds)} edges, {len(F)} faces, volume {vol(V):.9f} = {vol(V) / P_VOL:.6f} prolate(1)']
    lines.append('  edge lengths: ' + ', '.join(f'{x:.6f}' for x in el))
    fs = {}
    for e, f in F:
        L = tuple(round(np.linalg.norm(V[f[k]] - V[f[(k + 1) % len(f)]]), 4) for k in range(len(f)))
        fs.setdefault((len(f), min(L[k:] + L[:k] for k in range(len(L)))), 0); fs[(len(f), min(L[k:] + L[:k] for k in range(len(L))))] += 1
    lines.append('  faces (sides, side lengths): ' + '; '.join(f'{n} x {k[0]}-gon {list(k[1])}' for k, n in sorted(fs.items())))
    lines.append('  dihedral angles: ' + ', '.join(f'{x:.4f}' for x in sorted(set(round(a, 4) for a in ds.values()))))
    return '\n'.join(lines)

if __name__ == '__main__':
    print(f'RT(1): edge 1, 5-fold corner {R5:.9f}, 3-fold corner {R3:.9f}, inradius {RIN:.9f}, volume {RT_VOL:.9f}')
    print(f'prolate {P_VOL:.9f}, oblate {O_VOL:.9f}, 10P+10O = {10 * (P_VOL + O_VOL):.9f}')
    print(f'outer {vol(OUTER):.6f}, 12 copies {12 * RT_VOL:.6f}, centre {vol(CENTRE):.6f}, gap {GAP_VOL:.9f} = {GAP_VOL / O_VOL:.6f} oblate units')
