# DICTO 2026-10-20: the octet with an S across every face (DICTO: "every edge crosses the centre of a face that is half convex and half
# concave"): each face is half dome, half hollow; the line where it changes runs through the face's centre, along the median at right
# angles to the face's one edge parallel to the xy-plane. The face is a surface z = K * L_a L_b L_c (L_b - L_c) above its plane, along the
# face normal with positive x, b the corner on the +x side: the same surface for both pieces sharing it, so every bump meets a dent.
# Straight edges. K keeps the slope at the edges below the tetrahedron's half dihedral (no two faces of a piece cross). Float, manifold3d.
import itertools, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
NG = 24; H_TRI = np.sqrt(2) * np.sqrt(3) / 2
t = np.linspace(0, 1, 20001); EDGE = (t * (1 - t) * np.abs(2 * t - 1)).max()          # max of L_b L_c |L_b - L_c| along an edge
K = 0.9 * np.tan(np.arctan(1 / np.sqrt(2))) * H_TRI / EDGE
def face_frame(P):
    """corners ordered (a, b, c): a opposite the edge parallel to the xy-plane, b the other corner with the larger x (then y); normal N_x > 0"""
    P = [np.array(p, float) for p in P]
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        if abs(P[j][2] - P[k][2]) < 1e-12: a = i; break
    b, c = sorted([x for x in range(3) if x != a], key=lambda x: (-P[x][0], -P[x][1]))
    N = np.cross(P[b] - P[a], P[c] - P[a]); N /= np.linalg.norm(N); N = N if N[0] > 0 or (N[0] == 0 and N[1] > 0) else -N
    return np.array([P[a], P[b], P[c]]), N
def patch(P):
    Q, N = face_frame(P); pts, idx = [], {}
    for i in range(NG + 1):
        for j in range(NG + 1 - i):
            L = np.array([i, j, NG - i - j], float) / NG; idx[(i, j)] = len(pts)
            pts.append(L @ Q + K * L.prod() * (L[1] - L[2]) * N)
    tris = []
    for i in range(NG):
        for j in range(NG - i):
            tris.append([idx[(i, j)], idx[(i + 1, j)], idx[(i, j + 1)]])
            if j + i + 1 < NG: tris.append([idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]])
    return np.array(pts), tris
def solid(faces):
    V, T, key = [], [], {}
    for P, out in faces:
        pts, tris = patch(P); loc = []
        for p in pts:
            k = tuple(np.round(p, 9))
            if k not in key: key[k] = len(V); V.append(p)
            loc.append(key[k])
        for a, b, c in tris:
            n = np.cross(V[loc[b]] - V[loc[a]], V[loc[c]] - V[loc[a]])
            T.append([loc[a], loc[b], loc[c]] if n @ out >= 0 else [loc[a], loc[c], loc[b]])
    return m3.Manifold(m3.Mesh(vert_properties=np.array(V, np.float32), tri_verts=np.array(T, np.uint32)))
def tet(V):
    V = np.array(V, float); c = V.mean(0); F = []
    for k in range(4):
        P = V[[i for i in range(4) if i != k]]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        F.append((P, n if n @ (P.mean(0) - c) > 0 else -n))
    return solid(F)
def octa(cen):
    cen = np.array(cen, float)
    return solid([(np.array([cen + sg[j] * np.eye(3)[j] for j in range(3)]), np.array(sg, float) / np.sqrt(3)) for sg in itertools.product((1, -1), repeat=3)])
def tets_in(rng):
    for x, y, z in itertools.product(rng, repeat=3):
        base = np.array([x, y, z], float)
        yield base, base + np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if (x + y + z) % 2 == 0 else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)], float)
if __name__ == '__main__':
    print(f'K {K:.3f}; the largest rise of a face {K * max((L[0] * L[1] * L[2] * abs(L[1] - L[2])) for L in [np.array([i, j, 60 - i - j]) / 60 for i in range(61) for j in range(61 - i)]):.4f}')
    pieces = [('oct', octa((x, y, z))) for x, y, z in itertools.product(range(-1, 3), repeat=3) if (x + y + z) % 2] + [('tet', tet(V)) for _, V in tets_in(range(-1, 3))]
    print('valid:', all(p.status() == m3.Error.NoError for _, p in pieces), '; volumes tet', sorted({round(p.volume(), 5) for k, p in pieces if k == 'tet'}), 'oct', sorted({round(p.volume(), 5) for k, p in pieces if k == 'oct'}))
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 box: volume {tot:.5f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 1e-4 and over < 1e-5 else 'FAIL')
