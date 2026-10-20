# DICTO 2026-10-20: the two-piece foam curved: the flat Weaire-Phelan cells (wp_flat.py) carried through a smooth bend of space that
# commutes with all 48 symmetries of the structure (Pm-3n): u(x) = average over the group of R^-1 f0(R x + t), f0 a smooth wave of
# period 1. Equivariant, so every dodecahedron bends to the same shape and every tetrakaidecahedron too: still exactly TWO pieces;
# periodic and one-to-one (checked: Jacobian > 0), so they still fill space. Faces are finely meshed (shared faces meshed alike).
import itertools, json, os, sys, numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
G = [(np.array(R), np.array(t)) for R, t in json.load(open(os.path.join(HERE, 'wp-group.json')))]
C = {k: np.array(v) for k, v in json.load(open(os.path.join(HERE, 'wp-flat-cells.json'))).items()}
BASE = {'D': (0, 0, 0), 'D2': (.5, .5, .5), 'T1': (.25, 0, .5), 'T2': (.75, 0, .5), 'T3': (.5, .25, 0), 'T4': (.5, .75, 0), 'T5': (0, .5, .25), 'T6': (0, .5, .75)}
PH = np.array([[.13, .41, .07], [.29, .03, .53], [.61, .17, .37]]); AMP = np.array([[1, .6, .3], [.5, 1, .4], [.35, .45, 1]])
def f0(X):
    """a generic smooth wave of period 1 whose terms survive the half-step symmetries (frequency 2, and products of two frequency-1
    waves): single frequency-1 waves cancel when averaged over the group, because (1/2, 1/2, 1/2) flips their sign"""
    out = np.zeros_like(X)
    for i in range(3):
        for j in range(3):
            a, b = (i + j + 1) % 3, (i + 2 * j + 2) % 3
            out[:, i] += AMP[i, j] * np.sin(4 * np.pi * (X[:, a] + PH[i, j]))
            out[:, i] += 0.7 * AMP[j, i] * np.sin(2 * np.pi * (X[:, a] + PH[j, i])) * np.cos(2 * np.pi * (X[:, b] + PH[i, (j + 1) % 3]))
    return out
def u_raw(X):
    U = np.zeros_like(X)
    for R, t in G: U += f0(X @ R.T + t) @ R          # R^-1 = R^T
    return U / len(G)
# scale so the bend is gentle but clearly visible: largest displacement E
probe = np.random.default_rng(0).uniform(0, 1, (20000, 3)); m = np.abs(u_raw(probe)).max()
E = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
bend = lambda X: X + E * u_raw(X) / m
def jac_min(n=12):
    g = np.stack(np.meshgrid(*[np.linspace(0, 1, n, endpoint=False)] * 3), -1).reshape(-1, 3); h = 1e-5; dets = []
    for x in g:
        J = np.stack([(bend((x + h * e)[None])[0] - bend((x - h * e)[None])[0]) / (2 * h) for e in np.eye(3)], 1); dets.append(np.linalg.det(J))
    return min(dets)
NS = 6
def faces_of(P):
    h = ConvexHull(P); g = {}
    for s, e in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(e, 7)), (set(), e[:3]))[0].update(s)
    out = []
    for idx, n in g.values():
        idx = list(idx); Q = P[idx]; c = Q.mean(0); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        order = [idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]; out.append((P[order], n))
    return out
def cell_mesh(k, shift=np.zeros(3)):
    """the cell's surface: each face fanned from its centre, each fan triangle subdivided NS times; then bent"""
    V, T, key = [], [], {}
    def vid(p):
        kk = tuple(np.round(p, 9))
        if kk not in key: key[kk] = len(V); V.append(p)
        return key[kk]
    for Q, n in faces_of(C[k] + np.array(BASE[k]) + shift):
        c = Q.mean(0)
        for a, b in zip(Q, np.roll(Q, -1, 0)):
            grid = {}
            for i in range(NS + 1):
                for j in range(NS + 1 - i):
                    grid[(i, j)] = vid(c + (a - c) * i / NS + (b - c) * j / NS)
            for i in range(NS):
                for j in range(NS - i):
                    tri = [grid[(i, j)], grid[(i + 1, j)], grid[(i, j + 1)]]
                    tris = [tri] + ([[grid[(i + 1, j)], grid[(i + 1, j + 1)], grid[(i, j + 1)]]] if i + j + 1 < NS else [])
                    for t3 in tris:
                        p0, p1, p2 = [V[x] for x in t3]
                        T.append(t3 if np.cross(p1 - p0, p2 - p0) @ n > 0 else [t3[0], t3[2], t3[1]])
    W = bend(np.array(V))
    return m3.Manifold(m3.Mesh(vert_properties=np.array(W, np.float32), tri_verts=np.array(T, np.uint32))), W, T
if __name__ == '__main__':
    print(f'E {E}; Jacobian min over a grid {jac_min():.3f} (> 0: one-to-one)')
    meshes = {k: cell_mesh(k) for k in C}
    print('valid:', all(v[0].status() == m3.Error.NoError for v in meshes.values()), '; volumes', {k: round(v[0].volume(), 5) for k, v in meshes.items()})
    print('total (one period):', round(sum(v[0].volume() for v in meshes.values()), 5))
    # overlap: the 8 cells and their neighbours one period away
    allc = [(k, s, cell_mesh(k, np.array(s))[0]) for k in C for s in itertools.product((0, 1), repeat=3)]
    over = 0.0
    for (k1, s1, a), (k2, s2, b) in itertools.combinations(allc, 2):
        if np.linalg.norm(np.array(BASE[k1]) + s1 - np.array(BASE[k2]) - s2) < 1.0: over += (a ^ b).volume()
    print(f'overlap among 64 cells: {over:.2e} ->', 'PASS' if over < 1e-5 else 'FAIL')
    # two shapes: D2 is D carried by a group element; T2..T6 are T1 carried by group elements (equivariance), checked on the meshes
    def same(A, B): return len(A) == len(B) and np.abs(np.sort(np.linalg.norm(A - A.mean(0), axis=1)) - np.sort(np.linalg.norm(B - B.mean(0), axis=1))).max() < 1e-6
    print('D and D2 same shape:', same(meshes['D'][1], meshes['D2'][1]), '; T1..T6 same shape:', all(same(meshes['T1'][1], meshes[k][1]) for k in ['T2', 'T3', 'T4', 'T5', 'T6']))
    # is the bend visible: displacement of points on edges
    W0 = np.vstack([C[k] + np.array(BASE[k]) for k in C]); print('largest displacement of a cell corner', np.round(np.abs(bend(W0) - W0).max(), 4), '; of edge midpoints', np.round(max(np.linalg.norm(bend(((a + b) / 2)[None])[0] - (a + b) / 2) for k in C for Q, _ in faces_of(C[k] + np.array(BASE[k])) for a, b in zip(Q, np.roll(Q, -1, 0))), 4))
