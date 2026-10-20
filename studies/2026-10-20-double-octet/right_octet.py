# DICTO 2026-10-20: the octet with every edge a right angle (no edge sharper than it must be). Four pieces meet round every edge,
# tetrahedron 70.53 deg, octahedron 109.47 deg, twice each (360 deg). Tilting every face by a = (109.47 - 90)/2 = 9.74 deg at its edges,
# from the tetrahedron into the octahedron, makes all four 90 deg. The face: a dome over the triangle, height tan a * h_tri * g with
# g = L1 L2 L3 / (L1 L2 + L2 L3 + L3 L1) (L the barycentric coordinates, h_tri the triangle's height): g = L_i to first order at every
# point of the edge L_i = 0, so the slope there is exactly tan a along the whole edge. Tetrahedra bulge (rounded), octahedra are hollowed.
# Float, manifold3d: a block filled exactly; the angle measured along edges; figures.
import itertools, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
NG = 30; H_TRI = np.sqrt(2) * np.sqrt(3) / 2
A = (np.degrees(np.arccos(-1 / 3)) - 90) / 2; TA = np.tan(np.radians(A))
def g(L):
    s = L[0] * L[1] + L[1] * L[2] + L[2] * L[0]
    return 0.0 if s == 0 else L.prod() / s
def patch(P, out):
    """out: the tetrahedron's outward normal on this face (the dome rises that way, into the octahedron)"""
    pts, idx = [], {}
    for i in range(NG + 1):
        for j in range(NG + 1 - i):
            L = np.array([i, j, NG - i - j], float) / NG; idx[(i, j)] = len(pts); pts.append(L @ P + TA * H_TRI * g(L) * out)
    tris = []
    for i in range(NG):
        for j in range(NG - i):
            tris.append([idx[(i, j)], idx[(i + 1, j)], idx[(i, j + 1)]])
            if j + i + 1 < NG: tris.append([idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]])
    return np.array(pts), tris
def solid(faces):
    """faces: (P, dome direction, outward normal of this piece)"""
    V, T, key = [], [], {}
    for P, d, out in faces:
        pts, tris = patch(np.array(P, float), d); loc = []
        for p in pts:
            k = tuple(np.round(p, 9))
            if k not in key: key[k] = len(V); V.append(p)
            loc.append(key[k])
        for a, b, c in tris:
            n = np.cross(V[loc[b]] - V[loc[a]], V[loc[c]] - V[loc[a]])
            T.append([loc[a], loc[b], loc[c]] if n @ out >= 0 else [loc[a], loc[c], loc[b]])
    return m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(T, np.uint32))), np.array(V), T
def tet(V):
    V = np.array(V, float); c = V.mean(0); F = []
    for k in range(4):
        P = V[[i for i in range(4) if i != k]]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n); n = n if n @ (P.mean(0) - c) > 0 else -n
        F.append((P, n, n))
    return solid(F)
def octa(cen):
    cen = np.array(cen, float); F = []
    for sg in itertools.product((1, -1), repeat=3):
        n = np.array(sg, float) / np.sqrt(3); F.append((np.array([cen + sg[j] * np.eye(3)[j] for j in range(3)]), -n, n))   # dents: the tetrahedron's dome
    return solid(F)
def tets_in(rng):
    for x, y, z in itertools.product(rng, repeat=3):
        base = np.array([x, y, z], float)
        yield base, base + np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if (x + y + z) % 2 == 0 else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)], float)
def surface_normal(P, d, L, h=1e-5):
    """unit normal of the face surface at barycentric L (numerical)"""
    f = lambda L_: L_ @ P + TA * H_TRI * g(L_) * d
    u = (f(L + np.array([h, -h, 0])) - f(L - np.array([h, -h, 0]))); v = (f(L + np.array([h, 0, -h])) - f(L - np.array([h, 0, -h])))
    n = np.cross(u, v); return n / np.linalg.norm(n)
if __name__ == '__main__':
    print(f'tilt at the edges {A:.4f} deg; dome height {TA * H_TRI / 9:.4f}')
    # the angle inside the tetrahedron along its edge (1,1,0)-(1,0,1)... use the up tetrahedron and the edge between corners 1 and 2
    V = np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], float); c = V.mean(0)
    def face(k):
        P = V[[i for i in range(4) if i != k]]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n); return P, (n if n @ (P.mean(0) - c) > 0 else -n)
    (P0, n0), (P3, n3) = face(0), face(3)              # the two faces through the edge from corner 1 to corner 2
    angs = []
    for t in [0.1, 0.25, 0.5, 0.75, 0.9]:
        def Lfor(P):
            L = np.zeros(3); a = np.where(np.all(np.isclose(P, V[1]), 1))[0][0]; b = np.where(np.all(np.isclose(P, V[2]), 1))[0][0]
            L[a], L[b] = 1 - t, t; L = L * (1 - 3e-6) + 1e-6; return L
        m0, m3_ = surface_normal(P0, n0, Lfor(P0)), surface_normal(P3, n3, Lfor(P3))
        m0 = m0 if m0 @ n0 > 0 else -m0; m3_ = m3_ if m3_ @ n3 > 0 else -m3_
        angs.append(180 - np.degrees(np.arccos(np.clip(m0 @ m3_, -1, 1))))
    print('angle inside the tetrahedron along an edge (should be 90):', np.round(angs, 3))
    pieces = [('oct', octa((x, y, z))[0]) for x, y, z in itertools.product(range(-1, 3), repeat=3) if (x + y + z) % 2] + [('tet', tet(V_)[0]) for _, V_ in tets_in(range(-1, 3))]
    print('valid:', all(p.status() == m3.Error.NoError for _, p in pieces), '; volumes tet', sorted({round(p.volume(), 5) for k, p in pieces if k == 'tet'}), 'oct', sorted({round(p.volume(), 5) for k, p in pieces if k == 'oct'}))
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 box: volume {tot:.5f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 1e-4 and over < 1e-5 else 'FAIL')
