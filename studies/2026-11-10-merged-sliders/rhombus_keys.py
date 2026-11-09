"""Merged sliders, step 2(b) (DICTO 10 Nov 2026: 'go on with the rhombus keys'). Half-cell packings of close-packed spheres for a
stacking word; one piece P0 = the upper half of the RD (= upper half of the TRD). Keys: signs on the four corners of each of P0's
three upper rhombi (+ bump, - notch, 0 flat) and on the six triangles of its hexagon. For every half of every cell, the piece can be
placed in 6 ways (the isometries mapping P0 onto that half). A packing fits when at every shared rhombus and every hexagon the two
pieces' signs never agree in nonzero value (no bump on bump, notch on notch). Exact search (backtracking) on a periodic patch.
Sanity: unmarked piece fits every word; a c-forcing hexagon key fits only c-words. usage: python -u rhombus_keys.py"""
import itertools, sys
import numpy as np
SQ3 = np.sqrt(3)
# ---------- the piece P0 in its own frame (cube coordinates, axis u = (1,1,1)/sqrt3)
u = np.array([1, 1, 1]) / SQ3
T = np.array([.5, .5, .5])
RH = {}          # three upper rhombi: name -> corners dict
for (a, b, c) in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
    A1 = np.zeros(3); A1[a] = 1; A2 = np.zeros(3); A2[b] = 1
    O = np.array([.5, .5, .5]); O[c] = -.5
    RH[f'r{c}'] = {'T': T.copy(), 'O': O, 'A1': A1, 'A2': A2}
# hexagon: section of the RD by u.x = 0: vertices = midpoints where the plane cuts the RD edges; six triangles (centre + edge)
def hex_vertices():
    V = []
    for s in itertools.permutations([1, -1, 0]):
        V.append(np.array(s, float) / 2)            # points like (1/2,-1/2,0): on RD edges, u.x = 0
    ang = lambda v: np.arctan2(v @ np.array([1, -1, 0]) / np.sqrt(2), v @ np.array([1, 1, -2]) / np.sqrt(6))
    return sorted(V, key=ang)
HV = hex_vertices()
HT = [(HV[k] + HV[(k + 1) % 6]) / 3 for k in range(6)]    # triangle centroids (centre at 0)
# all isometries of space fixing the origin that map P0 onto itself: C3v (rotations about u by 0/120/240 and 3 mirrors)
def rot(axis, ang):
    axis = axis / np.linalg.norm(axis); K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
C3V = [rot(u, k * 2 * np.pi / 3) for k in range(3)] + [rot(u, k * 2 * np.pi / 3) @ np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]]) for k in range(3)]
INV = -np.eye(3)
MIR = np.eye(3) - 2 * np.outer(u, u)
R60 = rot(u, np.pi / 3)
# ---------- packings: layers perpendicular to u. In-plane lattice vectors e1 = (1,-1,0), e2 = (0,1,-1) (fcc neighbours in the plane)
e1 = np.array([1., -1, 0]); e2 = np.array([0., 1, -1]); up = 2 * u / SQ3 * 1.0   # layer spacing: (1,1,0).u = 2/sqrt3 ... height h
H = (np.array([1, 1, 0]) @ u)                        # 2/sqrt3
SH = {'A': np.zeros(3), 'B': (np.array([1., 1, 0]) - H * u), 'C': -(np.array([1., 1, 0]) - H * u)}   # in-plane offsets
def placements_for_cell(pos_lo, pos_hi, ctr):
    """the two halves of the cell at ctr: upper half oriented by the offset to the layer above, lower half by the layer below.
    Returns (list of 6 maps for the upper half, list of 6 maps for the lower half); a map is (M, t): x -> M x + t."""
    # upper half: P0 (whose upper neighbours sit at offset SH['B'] relative to A, i.e. the RD's own) turned 60 deg if the offset is -B
    d_hi = pos_hi; d_lo = pos_lo
    Mu = np.eye(3) if np.allclose(d_hi, SH['B'], atol=1e-9) else R60
    # lower half: point inversion of an upper half whose 'upper neighbours' are the lower layer: inversion maps offset d to -d
    Ml = INV @ (np.eye(3) if np.allclose(-d_lo, SH['B'], atol=1e-9) else R60)
    return [(Mu @ g, ctr) for g in C3V], [(Ml @ g, ctr) for g in C3V]
def build(word, N=3):
    """cells of a periodic patch: positions; returns list of cells with their two placement lists and the contacts."""
    L = len(word); cells = {}
    for z in range(L):
        off = SH[word[z]]
        for i in range(N):
            for j in range(N):
                cells[(z, i, j)] = z * H * u + off + i * e1 + j * e2
    return cells
def key_of(place, kind, point, K):
    M, t = place
    # find which piece feature maps to 'point'
    if kind == 'rh':
        for name, cs in RH.items():
            for cn, p in cs.items():
                if np.allclose(M @ p + t, point, atol=1e-6): return K['rh'].get((name, cn), 0)
        return None
    for k, c in enumerate(HT):
        if np.allclose(M @ c + t, point, atol=1e-6): return K['hx'][k]
    return None
def solve(word, K, N=3):
    L = len(word); cells = build(word, N)
    per = lambda z, i, j: (z % L, i % N, j % N)
    var = {}; dom = {}
    for (z, i, j), ctr in cells.items():
        lo = SH[word[(z - 1) % L]] - SH[word[z]]; hi = SH[word[(z + 1) % L]] - SH[word[z]]
        def norm(d):
            for k, v in SH.items():
                for a in range(-2, 3):
                    for b in range(-2, 3):
                        if np.allclose(d, v + a * e1 + b * e2, atol=1e-9) and k != 'A': return v
            return None
        pu, pl = placements_for_cell(norm(lo), norm(hi), ctr)
        dom[((z, i, j), 'U')] = pu; dom[((z, i, j), 'L')] = pl
    # constraints: hexagon (U vs L of the same cell) and upper rhombi of (z) vs lower rhombi of the three cells above
    cons = []
    for (z, i, j), ctr in cells.items():
        # hexagon triangles in world coordinates via the U placement 0 (the geometry is the same for all 6)
        cons.append(('hx', ((z, i, j), 'U'), ((z, i, j), 'L'), ctr))
        for (dz, di, dj) in itertools.product([1], range(-1, 2), range(-1, 2)):
            nb = per(z + dz, i + di, j + dj); pos = cells[(z, i, j)]
            tgt = (z + dz) * H * u + SH[word[(z + dz) % L]] + (i + di) * e1 + (j + dj) * e2
            if abs(np.linalg.norm(tgt - pos) - np.sqrt(2)) < 1e-9: cons.append(('rh', ((z, i, j), 'U'), (nb, 'L'), (pos, tgt, z + dz)))
    return dom, cons, cells
def face_of(M, t, mid, nrm):
    """the piece's upper rhombus (in placement M, t) lying in the plane through mid with normal nrm: all four corners on it"""
    for name, cs in RH.items():
        if all(abs((M @ p + t - mid) @ nrm) < 1e-9 for p in cs.values()): return name
    return None
def check(word, K, N=3):
    dom, cons, cells = solve(word, K, N); L = len(word)
    keys = list(dom); assign = {}
    # precompute pairwise compatibility tables
    def pts_hx(ctr): return [None]
    def ok(c, a, b):
        kind, x, y, data = c
        if kind == 'hx':
            ctr = data
            for k in range(6):
                pw = dom[x][a][0] @ HT[k] + dom[x][a][1]
                s1 = key_of(dom[x][a], 'hx', pw, K); s2 = key_of(dom[y][b], 'hx', pw, K)
                if s1 and s1 == s2: return False
            return True
        pos, tgt, zz = data
        Mx, tx = dom[x][a]; My, ty = dom[y][b]
        nrm = (tgt - pos) / np.linalg.norm(tgt - pos); mid = (pos + tgt) / 2
        fx = face_of(Mx, tx, mid, nrm); fy = face_of(My, tgt, mid, nrm)
        if fx is None or fy is None: raise RuntimeError('shared rhombus not found')
        for cn, p in RH[fx].items():
            w = Mx @ p + tx; s1 = K['rh'].get((fx, cn), 0)
            c2 = [c for c, p2 in RH[fy].items() if np.allclose(My @ p2 + tgt, w, atol=1e-6)]
            if len(c2) != 1: raise RuntimeError('corner not matched')
            s2 = K['rh'].get((fy, c2[0]), 0)
            if s1 and s2 and s1 == s2: return False
        return True
    tabs = {}
    for c in cons:
        _, x, y, _ = c
        tabs[id(c)] = [[ok(c, a, b) for b in range(6)] for a in range(6)]
    nbrs = {k: [] for k in keys}
    for c in cons: nbrs[c[1]].append(c); nbrs[c[2]].append(c)
    order = sorted(keys)
    sys.setrecursionlimit(10000)
    def bt(idx):
        if idx == len(order): return True
        k = order[idx]
        for a in range(6):
            good = True
            for c in nbrs[k]:
                _, x, y, _ = c; o = y if x == k else x
                if o in assign:
                    t = tabs[id(c)]
                    if not (t[a][assign[o]] if x == k else t[assign[o]][a]): good = False; break
            if good:
                assign[k] = a
                if bt(idx + 1): return True
                del assign[k]
        return False
    return bt(0)
WORDS = {'c (ABC)': 'ABC', 'h (AB)': 'AB', 'chh (ABCB... )': 'ABCB', 'cchh (ABCACB)': 'ABCACB'}
if __name__ == '__main__' and len(sys.argv) == 1:
    Z = {'rh': {}, 'hx': [0] * 6}
    print('sanity, unmarked piece:', {w: check(s, Z) for w, s in WORDS.items()})
    Kc = {'rh': {}, 'hx': [1, -1, 1, -1, 1, -1]}
    print('sanity, alternating hexagon key (expect c-words only):', {w: check(s, Kc) for w, s in WORDS.items()})

def corner_matches(word='ABCB', N=3):
    dom, cons, cells = solve(word, {'rh': {}, 'hx': [0] * 6}, N); counts = set()
    for c in cons:
        if c[0] != 'rh': continue
        _, x, y, (pos, tgt, zz) = c; Mx, tx = dom[x][0]; My, ty = dom[y][0]
        nrm = (tgt - pos) / np.linalg.norm(tgt - pos); mid = (pos + tgt) / 2
        fx = face_of(Mx, tx, mid, nrm); fy = face_of(My, tgt, mid, nrm)
        n = sum(1 for p in RH[fx].values() if any(np.allclose(My @ p2 + tgt, Mx @ p + tx, atol=1e-6) for p2 in RH[fy].values())) if fx and fy else -1
        counts.add(n)
    return counts
def classify(kp):
    kind, rh = kp; K = {'rh': rh, 'hx': [0] * 6}
    return tuple(w for w, s in WORDS.items() if check(s, K))
def search():
    import random
    print('shared rhombus corners matched per contact (must be {4}):', corner_matches(), flush=True)
    res = {}
    cn = ['T', 'O', 'A1', 'A2']
    pats = []
    for s in itertools.product((-1, 0, 1), repeat=4):
        if any(s): pats.append(('same', {(r, cn[k]): s[k] for r in RH for k in range(4) if s[k]}))
    random.seed(1)
    for _ in range(150):
        s = [random.choice((-1, 0, 1)) for _ in range(12)]
        if any(s): pats.append(('mixed', {(r, cn[k]): s[3 * ri + k] if False else s[ri * 4 + k] for ri, r in enumerate(sorted(RH)) for k in range(4) if s[ri * 4 + k]}))
    from multiprocessing import Pool
    with Pool(20) as pool:
        res = pool.map(classify, pats, chunksize=2)
    summary = {}
    for (kind, rh), allowed in zip(pats, res):
        summary.setdefault((kind, allowed), []).append(rh)
    for (kind, allowed), lst in sorted(summary.items(), key=lambda z: (z[0][0], -len(z[1]))):
        print(f'{kind:5s} patterns {len(lst):3d}: allow {list(allowed)}  e.g. {dict(list(lst[0].items())[:4])}', flush=True)
    hforce = [k for k in summary if k[1] and all(w.startswith('h') for w in k[1])]
    print('patterns allowing h-words but not c:', [(k, len(summary[k])) for k in hforce])
    return summary
if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'search':
    search(); print('FINAL ok')
