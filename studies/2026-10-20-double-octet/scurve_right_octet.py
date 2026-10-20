# DICTO 2026-10-20: the octet with every edge a right angle (right_octet.py), carried through the S-bend of space of scurve_octet.py
# (x -> x + E (sin 2 pi y, sin 2 pi z, sin 2 pi x): corners and edge midpoints fixed, every edge an S-curve). Still filling space; the
# bend is not angle-preserving, so the 90 deg edges drift a little: measured here along edges of every kind. Float, manifold3d.
import itertools, os, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "if __name__ == " + "'__main__':"
exec(open(os.path.join(HERE, 'right_octet.py')).read().split(MAIN)[0])
E = 0.07
bend = lambda P: P + E * np.stack([np.sin(2 * np.pi * P[:, 1]), np.sin(2 * np.pi * P[:, 2]), np.sin(2 * np.pi * P[:, 0])], 1)
_solid = solid
def solid(faces):
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
    W = bend(np.array(V, float))
    return m3.Manifold(m3.Mesh(vert_properties=np.array(W, np.float32), tri_verts=np.array(T, np.uint32))), W, T
def bent_normal(P, d, L, h=1e-5):
    f = lambda L_: bend((L_ @ P + TA * H_TRI * g(L_) * d)[None])[0]
    u = f(L + np.array([h, -h, 0])) - f(L - np.array([h, -h, 0])); v = f(L + np.array([h, 0, -h])) - f(L - np.array([h, 0, -h]))
    n = np.cross(u, v); return n / np.linalg.norm(n)
def tet_edge_angles(V):
    """the angle inside a tetrahedron (after the bend) along each of its 6 edges, at 5 points each"""
    V = np.array(V, float); c = V.mean(0); out = []
    faces = {}
    for k in range(4):
        P = V[[i for i in range(4) if i != k]]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n); faces[k] = (P, n if n @ (P.mean(0) - c) > 0 else -n)
    for i, j in itertools.combinations(range(4), 2):
        fa, fb = [k for k in range(4) if k not in (i, j)]
        for t in [0.1, 0.3, 0.5, 0.7, 0.9]:
            ns = []
            for k in (fa, fb):
                P, n = faces[k]; L = np.zeros(3)
                L[np.where(np.all(np.isclose(P, V[i]), 1))[0][0]] = 1 - t; L[np.where(np.all(np.isclose(P, V[j]), 1))[0][0]] = t
                L = L * (1 - 3e-6) + 1e-6; m = bent_normal(P, n, L)
                # orient outward: compare with the bent outward direction (normal mapped approximately)
                ns.append(m if m @ n > 0 else -m)
            out.append(180 - np.degrees(np.arccos(np.clip(ns[0] @ ns[1], -1, 1))))
    return out
if __name__ == '__main__':
    angs = []
    for _, V_ in tets_in(range(0, 2)): angs += tet_edge_angles(V_)
    print(f'angles inside the tetrahedra along their edges after the bend: min {min(angs):.2f}, max {max(angs):.2f}, mean {np.mean(angs):.2f} deg (straight: 90.00; plain octet 70.53)')
    pieces = [('oct', octa((x, y, z))[0]) for x, y, z in itertools.product(range(-1, 3), repeat=3) if (x + y + z) % 2] + [('tet', tet(V_)[0]) for _, V_ in tets_in(range(-1, 3))]
    print('valid:', all(p.status() == m3.Error.NoError for _, p in pieces), '; volumes tet', sorted({round(p.volume(), 4) for k, p in pieces if k == 'tet'}), 'oct', sorted({round(p.volume(), 4) for k, p in pieces if k == 'oct'}))
    box = m3.Manifold.cube([2, 2, 2]); inb = [(k, p ^ box) for k, p in pieces]; inb = [(k, p) for k, p in inb if p.volume() > 1e-9]
    tot = sum(p.volume() for _, p in inb); over = sum((a ^ b).volume() for (_, a), (_, b) in itertools.combinations(inb, 2))
    print(f'2 x 2 x 2 box: volume {tot:.5f} (8), overlap {over:.2e} ->', 'PASS' if abs(tot - 8) < 1e-3 and over < 1e-4 else 'FAIL')
