# Frames, groups, orbits for the Aequi enumeration (study 2026-11-19-aequi-complete).
# Cube frame: cube axes = coordinate axes (26 axis directions: C6, O8, RD12).
# Icosahedron frame: a 2-fold axis on each coordinate axis (62 directions: D12, I20, RT30).
# Union U: 74 directions (C6 c RT30, O8 c I20 shared).
import itertools, numpy as np
phi = (1 + 5 ** .5) / 2
def u(v): v = np.array(v, float); return v / np.linalg.norm(v)
def cyc_signs(t):
    S = set()
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(a * b for a, b in zip(s, t))
        for k in range(3): S.add(tuple(np.roll(q, k)))
    return [u(p) for p in S]
def dedup(L, tol=1e-9):
    out = []
    for v in L:
        if not any(np.abs(v - w).max() < tol for w in out): out.append(v)
    return out
FAM = {}
FAM['C6'] = dedup(cyc_signs((1, 0, 0)))
FAM['O8'] = dedup(cyc_signs((1, 1, 1)))
FAM['RD12'] = dedup(cyc_signs((1, 1, 0)))
FAM['D12'] = dedup(cyc_signs((0, phi, 1)))   # icosahedron vertices (0, ±φ, ±1) cyclic: the frame of Equanimity and D191
FAM['I12'] = dedup(cyc_signs((0, 1 / phi, phi)))
FAM['RT24'] = dedup(cyc_signs((1, phi, 1 / phi)))
CUBE = ['C6', 'O8', 'RD12']; ICO = ['D12', 'I12', 'RT24', 'C6', 'O8']   # I20 = O8 + I12, RT30 = C6 + RT24
DIRS = []; DFAM = []
for f in ['C6', 'O8', 'RD12', 'D12', 'I12', 'RT24']:
    for v in FAM[f]: DIRS.append(v); DFAM.append(f)
DIRS = np.array(DIRS)
def key(M): return tuple(np.round(np.asarray(M).ravel(), 6))
def closure(gens):
    G = {key(np.eye(3)): np.eye(3)}; frontier = [np.eye(3)]
    while frontier:
        nf = []
        for A in frontier:
            for g in gens:
                B = g @ A; k = key(B)
                if k not in G: G[k] = B; nf.append(B)
        frontier = nf
    return list(G.values())
def rot(axis, ang):
    a = u(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
P3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)
OH = closure([rot((0, 0, 1), np.pi / 2), P3, -np.eye(3)])
IH = closure([rot((0, phi, 1), 2 * np.pi / 5), P3, rot((0, 0, 1), np.pi), -np.eye(3)])
assert len(OH) == 48 and len(IH) == 120
ALL = {key(g): g for g in OH + IH}; ALLG = list(ALL.values())   # 144 maps (Th = 24 shared)
assert len(ALLG) == 144
DKEY = {tuple(np.round(v, 6)): i for i, v in enumerate(DIRS)}
assert len(DIRS) == 74 and len(FAM['C6']) + len(FAM['O8']) + len(FAM['RD12']) == 26
assert sum(len(FAM[f]) for f in ['C6', 'O8', 'D12', 'I12', 'RT24']) == 62
def dperm(g):
    """permutation of the 74 directions under g, -1 where the image leaves U"""
    return [DKEY.get(tuple(np.round(g @ v, 6)), -1) for v in DIRS]
def subgroups(G):
    keys = [key(g) for g in G]; idx = {k: i for i, k in enumerate(keys)}
    mult = np.array([[idx[key(a @ b)] for b in G] for a in G])
    e = idx[key(np.eye(3))]
    def clo(gens):
        S = {e}; fr = [e]
        while fr:
            nf = []
            for a in fr:
                for g in gens:
                    c = mult[a, g]
                    if c not in S: S.add(c); nf.append(c)
            fr = nf
        return frozenset(S)
    subs = {}
    for i in range(len(G)):
        S = clo([i]); subs.setdefault(S, [i])
    frontier = list(subs)
    while frontier:
        nf = []
        for S in frontier:
            gens = subs[S]
            for i in range(len(G)):
                if i not in S:
                    T = clo(gens + [i])
                    if T not in subs: subs[T] = gens + [i]; nf.append(T)
        frontier = nf
    return [[G[i] for i in sorted(S)] for S in subs]
def schoenflies(H):
    """name a finite point group from its elements"""
    n = len(H); inv = any(np.allclose(h, -np.eye(3)) for h in H)
    proper = [h for h in H if np.linalg.det(h) > 0]; improper = [h for h in H if np.linalg.det(h) < 0]
    def order(h):
        A = np.eye(3)
        for k in range(1, 200):
            A = A @ h
            if np.allclose(A, np.eye(3), atol=1e-8): return k
    ro = [order(h) for h in proper]
    mirrors = sum(1 for h in improper if np.allclose(h @ h, np.eye(3), atol=1e-8) and not np.allclose(h, -np.eye(3)))
    np_ = len(proper); mx = max(ro)
    c2 = ro.count(2)
    # rotation group type
    if np_ == 60: R = 'I'
    elif np_ == 24 and mx == 4 and c2 == 9: R = 'O'
    elif np_ == 12 and ro.count(3) == 8: R = 'T'
    elif mx == np_: R = 'C%d' % np_
    else: R = 'D%d' % (np_ // 2)
    if not improper: return R
    if R == 'I': return 'Ih'
    if R == 'O': return 'Oh'
    if R == 'T': return 'Th' if inv else 'Td'
    k = int(R[1:])
    if R[0] == 'C':
        if mirrors == k and k >= 1 and not (k == 1 and inv): return 'Cs' if k == 1 else 'C%dv' % k
        # improper: horizontal mirror (Cnh) or rotoreflection (S2n)
        if k == 1: return 'Ci'
        hm = any(np.allclose(h @ h, np.eye(3), atol=1e-8) and not np.allclose(h, -np.eye(3)) for h in improper)
        if hm and mirrors == 1: return 'C%dh' % k
        return 'S%d' % (2 * k)
    # dihedral rotation group with improper: Dnh (horizontal mirror, n+1 mirrors) or Dnd (n mirrors)
    return 'D%dh' % k if mirrors == k + 1 else 'D%dd' % k
if __name__ == '__main__':
    for f in FAM: print(f, len(FAM[f]))
    print('cube frame', 26, 'ico frame', 62, 'union', len(DIRS), '| maps', len(ALLG))
# frame check: every Ih map permutes the 62 icosahedron-frame directions
_ico = [i for i, f in enumerate(DFAM) if f != 'RD12']
assert all(sorted(dperm(g)[i] for i in _ico) == _ico for g in IH), 'icosahedron frame inconsistent'
