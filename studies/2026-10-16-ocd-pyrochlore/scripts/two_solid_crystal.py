# Two-solid crystals of the companion solid and icosahedra (DICTO 2026-10-16: "search for arrangements where companions and icosahedra
# alternate and fill space, like a two-solid crystal"; "Cleo icosa and Antonius gaps"). Icosahedra of the companion's triangle edge sit face to
# face on its triangles and bridge to the next companion through their opposite face. Frameworks:
#   bcc8    icosahedra on the 8 triangles of one inscribed cube (no clashes): companions on a bcc lattice, an icosahedron at every joint;
#   dia4    icosahedra on the 4 triangles of one tetrahedron: a diamond network of companions (the opposite four on the other sublattice).
# For each: the single framework's fill, then a second identical framework shifted by s, scanning s over a grid of the cell; reports the
# best clash-free shifts and their fill (two frameworks). Float; overlap test = LP for the deepest common point of two convex bodies.
import json, itertools, sys, numpy as np
from multiprocessing import Pool
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
D = json.load(open('crystal/comp-icos.json')); I = [np.array(x) for x in D['icos']]; C = np.array(D['companion']['v'])
U = np.array([x.mean(0) / np.linalg.norm(x.mean(0)) for x in I]); G = U @ U.T
cube = next(S for S in itertools.combinations(range(20), 8) if all(abs(abs(G[a, b]) - 1 / 3) < 1e-4 or abs(abs(G[a, b]) - 1) < 1e-4 for a, b in itertools.combinations(S, 2)))
tet = [cube[0]] + [k for k in cube if abs(G[cube[0], k] + 1 / 3) < 1e-4]
vC, vI = ConvexHull(C).volume, ConvexHull(I[0]).volume
EQ = {}
def eq(V):
    k = id(V)
    if k not in EQ:
        E = ConvexHull(V).equations; n = E[:, :3] / np.linalg.norm(E[:, :3], axis=1)[:, None]; EQ[k] = (n, -E[:, 3] / np.linalg.norm(E[:, :3], axis=1))
    return EQ[k]
def depth(A, sa, B, sb):
    na, da = eq(A); nb, db = eq(B)
    n = np.vstack([na, nb]); d = np.r_[da + na @ sa, db + nb @ sb]
    r = linprog([0, 0, 0, -1], A_ub=np.hstack([n, np.ones((len(n), 1))]), b_ub=d, bounds=[(None, None)] * 4, method='highs')
    return -r.fun
bond = lambda k: U[k] * ((I[k] @ U[k]).max() + (C @ U[k]).max())
def framework(name):
    """bodies per cell as (template, offset) and the lattice basis"""
    if name == 'bcc8':
        sh = [bond(k) for k in cube]
        vecs = sorted([v for v in sh + [a + b for a, b in itertools.combinations(sh, 2)] if np.linalg.norm(v) > 1e-6], key=np.linalg.norm); basis = []
        for v in vecs:
            if len(basis) < 3 and np.linalg.matrix_rank(np.array(basis + [v])) == len(basis) + 1: basis.append(v)
        B = np.array(basis).T
        bodies = [(C, np.zeros(3))] + [(I[k], np.zeros(3)) for k in cube[:4] if True]
        # one icosahedron per bond, 4 per site: those on the 4 tetrahedral triangles of one sign
        bodies = [(C, np.zeros(3))] + [(I[k], np.zeros(3)) for k in tet]
        return B, bodies
    if name == 'dia4':
        sh = [bond(k) for k in tet]                                     # A -> B bonds
        Bm = np.array([sh[0] - sh[1], sh[0] - sh[2], sh[0] - sh[3]]).T     # fcc lattice of A sites
        opp = [k2 for k in tet for k2 in range(20) if np.allclose(U[k2], -U[k], atol=1e-6)]
        bodies = [(C, np.zeros(3))] + [(I[k], np.zeros(3)) for k in tet] + [(C, sh[0])]
        return Bm, bodies
def near_list(B, bodies, R=2.6):
    out = []
    for m in itertools.product(range(-2, 3), repeat=3):
        t = B @ np.array(m, float)
        for V, o in bodies:
            c = V.mean(0) + o + t
            if np.linalg.norm(c) < R: out.append((V, o + t))
    return out
def single(name):
    B, bodies = framework(name); vol = abs(np.linalg.det(B)); L = near_list(B, bodies)
    worst = max(depth(a[0], a[1], b[0], b[1]) for a, b in itertools.combinations(L, 2)
                if np.linalg.norm((a[0].mean(0) + a[1]) - (b[0].mean(0) + b[1])) < 1.6)
    fill = sum(ConvexHull(V).volume for V, _ in bodies) / vol
    return B, bodies, vol, worst, fill
def scan_one(args):
    name, f = args
    B, bodies = framework(name); s = B @ np.array(f)
    A = [(V, o) for V, o in near_list(B, bodies, 1.9)]
    Bsh = [(V, o + s) for V, o in near_list(B, bodies, 2.6) if np.linalg.norm(V.mean(0) + o + s) < 1.9]
    worst = -9
    for a in A:
        ca = a[0].mean(0) + a[1]
        for b in Bsh:
            if np.linalg.norm(ca - (b[0].mean(0) + b[1])) < 1.6:
                worst = max(worst, depth(a[0], a[1], b[0], b[1]))
                if worst > 1e-6: return f, worst
    return f, worst
if __name__ == '__main__':
    lines = ['DICTO · dictospheres.com', 'Two-solid crystals: companion + icosahedra (float)']
    for name in ('bcc8', 'dia4'):
        B, bodies, vol, worst, fill = single(name)
        lines.append(f'  {name}: one framework, cell volume {vol:.5f}, bodies per cell {len(bodies)}, deepest overlap {worst:.6f}, fill {fill:.4f}')
        n = 8; grid = [(name, (a / n, b / n, c / n)) for a in range(n) for b in range(n) for c in range(n)]
        with Pool(4) as P: res = P.map(scan_one, grid, chunksize=4)
        free = sorted([r for r in res if r[1] <= 1e-6], key=lambda r: r[1])
        lines.append(f'    second framework: {len(free)} of {len(res)} shifts clash-free' + (f'; fill with two {2 * fill:.4f}; e.g. shifts {[tuple(round(x, 3) for x in r[0]) for r in free[:6]]}, clearances {[round(-r[1], 4) for r in free[:6]]}' if free else ''))
        print('\n'.join(lines[-2:]), flush=True)
    open('data/two-solid-crystal.txt', 'w').write('\n'.join(lines) + '\n')
