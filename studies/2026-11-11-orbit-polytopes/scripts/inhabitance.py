"""Strict inhabitance (DICTO 11 Nov: "strict inhabitance of polytope networks by dodecahedrons icosahedrons etc"; "yes that's what I
mean, run the inhabitance test"). For every Atlas polytope (every 0/1 seed of A3, B3, H3, A4, B4, F4, H4): every exact Platonic solid
(D, I, C, T, O) whose corners are all corners of the polytope, found three ways:
  (a) as a CELL (a facet that is a Platonic solid; 4D only),
  (b) as the VERTEX FIGURE (the edge-neighbours of a corner form a Platonic solid; 4D only),
  (c) HIDDEN among the corners, any size: through a fixed corner v0, for every distance d, every triple of v0's d-neighbours whose mutual
      distances match a Platonic corner's three neighbours fixes a frame; the whole solid is built from it (scaled isometry checked) and
      kept only if ALL its corners are polytope corners. Count = (solids through v0) x corners / (corners per solid) (uniform polytopes
      are corner-transitive). Solids that are cells are reported apart from the hidden ones.
Controls: 600-cell (I as vertex figure; T as cells; 25 24-cells' worth of octahedra, i.e. hidden O; hidden I), 120-cell (D cells),
cube (2 hidden T), dodecahedron (5 C, 10 T), 24-cell (O cells, C vertex figure).   usage: inhabitance.py GROUPS"""
import sys, itertools, json, time
import numpy as np
from collections import Counter
from scipy.spatial import cKDTree
want = sys.argv[1].split(',') if len(sys.argv) > 1 else ['A3', 'B3', 'H3']
_want = want; sys.argv = ['x', 'A3']
exec(open('atlas.py').read().split('out = {}')[0])
want = _want
phi = (1 + 5 ** .5) / 2
def canon():
    T = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
    C = np.array(list(itertools.product((1, -1), repeat=3)), float)
    O = np.array([s * np.eye(3)[i] for i in range(3) for s in (1, -1)], float)
    I = np.array([np.roll([0, a, b * phi], c) for c in range(3) for a in (1, -1) for b in (1, -1)], float)
    Dd = np.vstack([C, np.array([np.roll([0, a / phi, b * phi], c) for c in range(3) for a in (1, -1) for b in (1, -1)], float)])
    out = {}
    for name, S in [('D', Dd), ('I', I), ('C', C), ('T', T), ('O', O)]:
        S = S - S.mean(0); dm = np.linalg.norm(S[:, None] - S[None], axis=2); e = dm[dm > 1e-9].min(); S = S / e
        s0 = 0; nb = [j for j in range(len(S)) if abs(np.linalg.norm(S[j] - S[s0]) - 1) < 1e-9][:3]
        out[name] = {'S': S, 'nb': nb, 'k': len(S), 'dist': np.sort(np.round(np.linalg.norm(S[:, None] - S[None], axis=2)[np.triu_indices(len(S), 1)], 6))}
    return out
CAN = canon()
def platonic_of(Q):
    """which Platonic solid the point set Q is (exactly, any size), or None"""
    if len(Q) not in (4, 6, 8, 12, 20): return None
    if np.linalg.matrix_rank(Q - Q.mean(0), tol=1e-7) != 3: return None
    dm = np.linalg.norm(Q[:, None] - Q[None], axis=2)[np.triu_indices(len(Q), 1)]; dm = np.sort(dm / dm.min())
    for name, c in CAN.items():
        if c['k'] == len(Q) and np.allclose(dm, c['dist'], atol=1e-5): return name
    return None
def hidden(P, tree, v0=0):
    found = {n: set() for n in CAN}
    D0 = np.linalg.norm(P - P[v0], axis=1); ds = np.unique(np.round(D0[D0 > 1e-9], 6))
    for d in ds:
        Nd = np.where(np.abs(D0 - d) < 1e-6)[0]
        if len(Nd) < 3: continue
        for name, c in CAN.items():
            S, nb = c['S'] * d, c['nb']; s0 = S[0]; Sv = S[nb] - s0
            d12, d13, d23 = (np.linalg.norm(Sv[0] - Sv[1]), np.linalg.norm(Sv[0] - Sv[2]), np.linalg.norm(Sv[1] - Sv[2]))
            PN = P[Nd]; DD = np.linalg.norm(PN[:, None] - PN[None], axis=2)
            for i in range(len(Nd)):
                for j in np.where(np.abs(DD[i] - d12) < 1e-6)[0]:
                    for k in np.where((np.abs(DD[i] - d13) < 1e-6) & (np.abs(DD[j] - d23) < 1e-6))[0]:
                        A = np.array([PN[i], PN[j], PN[k]]) - P[v0]       # images of Sv (rows)
                        L = np.linalg.lstsq(Sv, A, rcond=None)[0]          # 3 x n map with Sv @ L = A
                        if not np.allclose(L @ L.T, np.eye(3), atol=1e-6): continue
                        img = P[v0] + (S - s0) @ L; dist, idx = tree.query(img)
                        if dist.max() < 1e-6: found[name].add(frozenset(idx.tolist()))
    return found
res = {}; t00 = time.time()
for gname in want:
    R, bonds = chain_any(list(GR[gname])); n = len(R); Rm = np.array(R); G = group(R); Wt = np.linalg.inv(Rm)
    for lab in itertools.product((0, 1), repeat=n):
        if not any(lab): continue
        t0 = time.time(); x = np.linalg.solve(Rm, np.array(lab, float)); P = dedupe(G @ x); tree = cKDTree(P); V = len(P)
        rec = {'cells': {}, 'vertex_figure': None, 'hidden': {}}
        cellsets = set()
        if n == 4:
            for j in range(n):
                Dn = dedupe(np.array([unit(v) for v in (G @ Wt[:, j])]), 1e-7)
                for d in Dn:
                    hv = P @ d; top = np.where(hv > hv.max() - 1e-7)[0]
                    if len(top) >= 4 and np.linalg.matrix_rank(P[top] - P[top].mean(0), tol=1e-7) == 3:
                        cellsets.add(frozenset(top.tolist())); nm = platonic_of(P[top])
                        if nm: rec['cells'][nm] = rec['cells'].get(nm, 0) + 1
            Dv = np.linalg.norm(P - P[0], axis=1); nbrs = np.where(np.abs(Dv - Dv[Dv > 1e-9].min()) < 1e-6)[0]
            rec['vertex_figure'] = platonic_of(P[nbrs])
        H = hidden(P, tree)
        for name, sols in H.items():
            if not sols: continue
            k = CAN[name]['k']; total = len(sols) * V // k
            sizes = Counter(round(float(np.linalg.norm(P[list(s)][0] - P[list(s)][1:], axis=1).min()), 4) for s in sols)
            ascell = sum(1 for s in sols if s in cellsets) * V // k
            rec['hidden'][name] = {'total': total, 'of_which_cells': ascell, 'edge_lengths': sorted(sizes)}
        res[f'{gname} {lab}'] = rec
        hid = ', '.join(f"{nm} {h['total']}" + (f" ({h['of_which_cells']} cells)" if h['of_which_cells'] else '') + f" edges {h['edge_lengths']}" for nm, h in rec['hidden'].items())
        print(f"{gname} {lab}: {V} corners | cells {rec['cells'] or '-'} | vertex figure {rec['vertex_figure'] or '-'} | inhabitants: {hid or 'none'}  ({time.time() - t0:.0f} s)", flush=True)
json.dump(res, open(f"inhabitance_{'_'.join(want)}.json", 'w'), indent=1, default=str)
def get(k): return res.get(k)
checks = []
if get('B3 (1, 0, 0)') or get('B3 (0, 0, 1)'):
    cube = get('B3 (1, 0, 0)') if get('B3 (1, 0, 0)')['hidden'].get('C') else get('B3 (0, 0, 1)')
    checks.append(('cube holds 2 tetrahedra', cube['hidden'].get('T', {}).get('total') == 2))
for k in ('H3 (1, 0, 0)', 'H3 (0, 0, 1)'):
    r = get(k)
    if r and r['hidden'].get('D'): checks.append(('dodecahedron holds 5 cubes and 10 tetrahedra', r['hidden'].get('C', {}).get('total') == 5 and r['hidden'].get('T', {}).get('total') == 10))
for k in ('F4 (1, 0, 0, 0)',):
    r = get(k)
    if r: checks.append(('24-cell: octahedral cells, cube vertex figure', r['cells'].get('O') == 24 and r['vertex_figure'] == 'C'))
for k, nm in (('H4 (0, 0, 0, 1)', '600'), ('H4 (1, 0, 0, 0)', '120')):
    r = get(k)
    if r and nm == '600': checks.append(('600-cell: 600 tetrahedral cells, icosahedral vertex figure', r['cells'].get('T') == 600 and r['vertex_figure'] == 'I'))
    if r and nm == '120': checks.append(('120-cell: 120 dodecahedral cells', r['cells'].get('D') == 120))
for c in checks: print('control:', c[0], 'ok' if c[1] else 'FAIL')
print('FINAL ok' if checks and all(c[1] for c in checks) else 'FINAL FAIL (controls)', f'({time.time() - t00:.0f} s)')
