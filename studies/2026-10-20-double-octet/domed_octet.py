# DICTO 2026-10-20: the double octet set, rounded (DICTO: the octahedron's faces alternate on the body): the octahedron with 4 convex and 4
# concave faces in checkerboard order, so the tetrahedra come in two kinds, all-convex (rounded, Meissner-like) and all-concave, alternating.
# Faces: smooth pillow domes (or hollows) with the octet's straight edges: height k * L1 L2 L3 (L the barycentric coordinates), k chosen so
# that every dome stays inside its face's cone from the tetrahedron's centre (z <= (k/4) L_i <= tan 35.26 deg * distance to the edge), so a
# hollow tetrahedron's four dents never meet. (True spherical faces with shared curved edges are impossible here: tested, only flat fits.)
# Float, manifold3d: pieces as watertight meshes (edges sampled alike on both sides), a 2 x 2 x 2 block filled without overlap; figures.
import itertools, json, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
T_PLUS = {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}             # octahedron faces convex when their outward normal is here
H_TRI = np.sqrt(2) * np.sqrt(3) / 2; K = 0.98 * 4 * H_TRI * np.tan(np.arctan(1 / np.sqrt(2)))   # 35.26 deg = the tetrahedron's half dihedral
NG = 14
def patch(P, sign, out):
    """dome (sign +1, bulging along out) or hollow (-1) on triangle P: grid points and triangles; edge points exactly on the edges"""
    pts, idx = [], {}
    for i in range(NG + 1):
        for j in range(NG + 1 - i):
            L = np.array([i, j, NG - i - j], float) / NG
            idx[(i, j)] = len(pts); pts.append(L @ P + sign * K * L.prod() * out)
    tris = []
    for i in range(NG):
        for j in range(NG - i):
            tris.append([idx[(i, j)], idx[(i + 1, j)], idx[(i, j + 1)]])
            if j + i + 1 < NG: tris.append([idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]])
    return np.array(pts), tris
def solid(faces):
    """faces: [(P (3 corners), sign, outward unit normal)] -> manifold (vertices merged by position)"""
    V, T, key = [], [], {}
    for P, sign, out in faces:
        pts, tris = patch(np.array(P, float), sign, out); loc = []
        for p in pts:
            k = tuple(np.round(p, 9))
            if k not in key: key[k] = len(V); V.append(p)
            loc.append(key[k])
        for a, b, c in tris:
            n = np.cross(V[loc[b]] - V[loc[a]], V[loc[c]] - V[loc[a]])
            T.append([loc[a], loc[b], loc[c]] if n @ out > 0 or sign < 0 and False else [loc[a], loc[c], loc[b]] if n @ out < 0 else [loc[a], loc[b], loc[c]])
    m = m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(T, np.uint32)))
    return m
def tet(V, convex):
    V = np.array(V, float); c = V.mean(0); F = []
    for f in itertools.combinations(range(4), 3):
        P = V[list(f)]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        if n @ (P.mean(0) - c) < 0: n = -n
        F.append((P, 1 if convex else -1, n))
    return solid(F)
def octa(cen):
    cen = np.array(cen, float); F = []
    for sg in itertools.product((1, -1), repeat=3):
        P = np.array([cen + sg[j] * np.eye(3)[j] for j in range(3)]); n = np.array(sg, float) / np.sqrt(3)
        F.append((P, 1 if tuple(sg) in T_PLUS else -1, n))
    return solid(F)
if __name__ == '__main__':
    t0 = 1 / 3; o0 = 4 / 3; dome = K * (np.sqrt(3) / 4 * 2) / 60          # k * area / 60 (the integral of L1 L2 L3)
    Tv, Tc, O = tet([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], True), tet([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], False), octa((1, 0, 0))
    print(f'K {K:.4f}, dome height {K / 27:.4f} (tetrahedron inradius {1 / (2 * np.sqrt(3)):.4f}); volumes: convex tetrahedron {Tv.volume():.6f} (want {t0 + 4 * dome:.6f}), concave {Tc.volume():.6f} (want {t0 - 4 * dome:.6f}), octahedron {O.volume():.6f} (want {o0:.6f}); manifold {Tv.status()}, {Tc.status()}, {O.status()}')
    pieces = []
    for x, y, z in itertools.product(range(-1, 3), repeat=3):
        if (x + y + z) % 2: pieces.append(('oct', octa((x, y, z))))
        base = np.array([x, y, z], float); even = (x + y + z) % 2 == 0
        corners = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if even else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
        V = base + np.array(corners, float); c = V.mean(0)
        # which kind: the octahedra's convex faces (T_PLUS normals) push into this tetrahedron when its own outward normals are -T_PLUS
        n0 = np.sign(np.cross(V[2] - V[1], V[3] - V[1])); m_ = V[1:].mean(0)
        normals = {tuple(int(v) for v in np.sign(np.array(V[list(f)]).mean(0) - c)) for f in itertools.combinations(range(4), 3)}
        convex = normals <= T_PLUS                      # its faces face T_PLUS: the octahedra's faces there face -T_PLUS (concave): it bulges into them
        pieces.append(('tetC' if convex else 'tetH', tet(V, convex)))
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 block: {len(inb)} parts, volume {tot:.6f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 1e-4 and over < 1e-5 else 'FAIL')
    from collections import Counter; print('kinds', Counter(k for k, _ in pieces))
