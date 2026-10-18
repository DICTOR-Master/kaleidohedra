# DICTO 2026-10-18 spherical containment chamber (outside the kit plan; DICTO: "1, hollow chamber also half RD networks open with golden
# envelope exposed on outside"). Cells of the golden octet (fcc sites, spacing R*sqrt2) between an inner and an outer radius.
# Inner layers: full rhombic dodecahedra (envelope fused). Outermost layer (a cell with a neighbour beyond the outer radius): its golden
# envelope + only the INWARD adaptor half, so the envelopes are exposed outside. The adaptor halves split on a mirror plane x=0, y=0 or z=0;
# each outer cell uses the plane facing most outward. Geometry only, nothing structural claimed. Adds 'chamber' views to the p4 page data.
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data', 'step10-input.json')))['R']
R_IN, R_OUT = 2.4, 5.4
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
k = int(np.ceil(R_OUT / R)) + 1
sites = [np.array(c) * R for c in itertools.product(range(-k, k + 1), repeat=3) if sum(c) % 2 == 0]
cells = [p for p in sites if R_IN <= np.linalg.norm(p) <= R_OUT]
nbr = [R * np.array(v) for v in itertools.chain.from_iterable(set(itertools.permutations(t)) for t in [(1, 1, 0), (1, -1, 0), (-1, -1, 0)])]
def outer(p): return any(np.linalg.norm(p + v) > R_OUT for v in nbr)
place_full, place_cut, n_out = [], [], 0
for p in cells:
    cut = p[1] < 0.0          # cutaway: keep the half of the chamber with y < 0 in the cut view
    if outer(p):
        n_out += 1; a = int(np.argmax(np.abs(p))); inward = np.zeros(3); inward[a] = -np.sign(p[a])
        G = next(G for G in ops if np.allclose(G @ [0, 0, 1], inward))
        items = [['env', False, p.tolist()], ['half', False, p.tolist(), G.ravel().tolist()]]
    else:
        items = [['rd', False, p.tolist()]]
    place_full += items
    if cut: place_cut += items
info = dict(R_in=R_IN, R_out=R_OUT, cells=len(cells), outer_cells=n_out, inner_cells=len(cells) - n_out)
print(info)
json.dump(dict(info=info, full=place_full, cut=place_cut), open(os.path.join(H, '..', 'data', 'p4-chamber.json'), 'w'))
