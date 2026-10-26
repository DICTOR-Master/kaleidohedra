# Pyrochlore polytypes (DICTO 2026-10-27: "close packing halves rule pyrochlore network"). For a close-packed stacking word, the
# diamond-type crystal = the balls + one tetrahedral hole over each ball (#57's hole "over X at 3/4", nearest layer k+1); the
# pyrochlore network = the midpoints of its bonds: each atom's 4 bond midpoints are a tetrahedron, neighbours share a corner.
# Units and positions as #57 (k-mix src/app/stackings-geometry.js): ball spacing 1, layers sqrt(2/3) apart.
import numpy as np, itertools, sys
H = np.sqrt(2 / 3); A1 = np.array([1, 0, 0.]); A2 = np.array([.5, np.sqrt(3) / 2, 0])
POS = {'A': (0, 0), 'B': (1 / 3, 1 / 3), 'C': (2 / 3, 2 / 3)}
def xy(L): f, g = POS[L]; return f * A1 + g * A2
def layer_types(w): return ['h' if w[k - 1] == w[(k + 1) % len(w)] else 'c' for k in range(len(w))]
def atoms(word):
    """One period: balls (kind 'S', layer k) and holes over each ball at 3/4 (kind 'C', bonded to it and to 3 balls of layer k+1)."""
    out = []
    for k, X in enumerate(word):
        out.append(('S', k, xy(X) + np.array([0, 0, k * H])))
        out.append(('C', k, xy(X) + np.array([0, 0, (k + .75) * H])))
    return out
def periodic(word, P, reach):
    n = len(word); T = n * H; out = []
    for kind, k, p in P:
        for i, j, l in itertools.product(range(-3, 4), range(-3, 4), range(-1, 2)):
            out.append((kind, k, p + i * A1 + j * A2 + np.array([0, 0, l * T])))
    return out
def pyrochlore(word):
    P = atoms(word); n = len(word); T = n * H
    big = periodic(word, P, 3)
    bond = np.sqrt(3 / 8)                                      # Si-C bond = 3/4 of the layer spacing
    tets, mids = [], {}
    for kind, k, p in P:
        nb = [q for kk, _, q in big if kk != kind and abs(np.linalg.norm(q - p) - bond) < 1e-9]
        if len(nb) != 4: raise SystemExit(f'{word}: atom {kind}{k} has {len(nb)} bonds')
        M = [(p + q) / 2 for q in nb]; tets.append((kind, k, p, M))
    # corner sharing: every midpoint (mod the period) in exactly two tetrahedra
    def key(x):
        y = x.copy(); y[2] = y[2] % T
        # reduce in-plane by the lattice
        B = np.array([A1[:2], A2[:2]]).T; c = np.linalg.solve(B, y[:2]); c = c - np.floor(c + 1e-9); y[:2] = B @ c
        return tuple(np.round(y, 6))
    cnt = {}
    for _, _, _, M in tets:
        for m in M: cnt[key(m)] = cnt.get(key(m), 0) + 1
    edges = sorted({round(float(np.linalg.norm(a - b)), 9) for _, _, _, M in tets for a, b in itertools.combinations(M, 2)})
    return tets, cnt, edges
if __name__ == '__main__':
    for name, w in [('3C', 'ABC'), ('2H', 'AB'), ('4H', 'ABAC'), ('6H', 'ABCACB')]:
        tets, cnt, edges = pyrochlore(w)
        print(f'{name} {w}: {len(tets)} tetrahedra per period, {len(cnt)} corners; corners per tetrahedron-count {sorted(set(cnt.values()))}; '
              f'tetrahedron edges {edges}; layers {"".join(layer_types(w))}')
