# Space groups of the OCD Stella crystals (DICTO 2026-10-16: "a paper on their symmetry group"). Each solid is marked by its corners (one
# atom type per kind of solid) and its centre (own type), in a periodic cell; spglib finds the space group and the site symmetry of each
# centre. Float positions, tolerance 1e-4. -> data/crystal-symmetry.txt
import json, itertools, numpy as np, spglib
from scipy.spatial import ConvexHull, HalfspaceIntersection
N = json.load(open('data/network.json')); T = np.array(N['T']); Lb = np.array(N['Lb']).T; OCD = np.array(N['ocd'])
R = json.load(open('data/crystal-render.json')); S = np.array(R['stella']['v']); I = np.array(R['ico']['v'])
sites = [Lb @ np.array(m, float) + k * T[0] for m in itertools.product(range(-2, 3), repeat=3) for k in range(4)]
nb = [s for s in sites if 1e-9 < np.linalg.norm(s) < 2.0]
HV = np.array([np.r_[s, -(s @ s) / 2] for s in nb]); Vc = HalfspaceIntersection(HV, np.zeros(3)).intersections; Hc = ConvexHull(Vc)
P = []
for e in Hc.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
P = np.array(P); on = lambda e: sum(abs(Vc @ e[:3] + e[3]) < 1e-7)
O = np.unique(np.round(HalfspaceIntersection(np.array([e for e in P if on(e) == 6]), np.zeros(3)).intersections, 10), axis=0)
cube = [2 * (-e[3]) * e[:3] / (e[:3] @ e[:3]) for e in P if on(e) == 4]
e1 = cube[0]; e2 = next(v for v in cube if abs(v @ e1) < 1e-9); e3 = next(v for v in cube if abs(v @ e1) < 1e-9 and abs(v @ e2) < 1e-9)
SOL = {'OCD': OCD, 'OCD Stella': S, 'icosahedron': I, 'octahedron': O}
def analyse(label, cell, placed):
    # cell: 3x3 columns; placed: list of (centre, solid name)
    Ci = np.linalg.inv(cell); pos, typ = [], []; names = sorted({n for _, n in placed}); code = {n: i for i, n in enumerate(names)}
    for c, n in placed:
        for v in SOL[n]: pos.append(Ci @ (c + v)); typ.append(1 + code[n])
        pos.append(Ci @ c); typ.append(50 + code[n])
    pos = np.mod(np.array(pos), 1.0); pos[np.isclose(pos, 1.0, atol=1e-9)] = 0
    keep = []; seen = []
    for p, t in zip(pos, typ):
        if not any(np.allclose(np.mod(p - q + 0.5, 1) - 0.5, 0, atol=1e-7) and t == u for q, u in seen): seen.append((p, t))
    pos = np.array([p for p, _ in seen]); typ = [t for _, t in seen]
    ds = spglib.get_symmetry_dataset((cell.T, pos, typ), symprec=1e-4)
    cs = {}
    for i, t in enumerate(typ):
        if t >= 50: cs.setdefault(names[t - 50], set()).add((ds.wyckoffs[i], ds.site_symmetry_symbols[i]))
    return f'{label}: space group {ds.international} (No. {ds.number}), point group {ds.pointgroup}, {len(ds.rotations)} operations per cell; ' + \
           '; '.join(f'{n} centres at Wyckoff {", ".join(w + " (site " + s + ")" for w, s in sorted(v))}' for n, v in cs.items())
out = ['DICTO · dictospheres.com', 'Space groups of the OCD Stella crystals (spglib 2.8, solids marked by their corners and centres; float, tolerance 1e-4)']
four = [(k * T[0], k) for k in range(4)]
out.append(analyse('OCD packing (bcc), reference', Lb, [(c, 'OCD') for c, k in four]))
out.append(analyse('OCD Stella alone (bcc)', Lb, [(c, 'OCD Stella') for c, k in four]))
out.append(analyse('OCD Stella + icosahedra, pyrochlore', Lb, [(c, 'OCD Stella' if k < 2 else 'icosahedron') for c, k in four]))
out.append(analyse('OCD Stella + octahedra, pyrochlore', Lb, [(c, 'OCD Stella' if k < 2 else 'octahedron') for c, k in four]))
C2 = np.c_[2 * e1, 2 * e2, 2 * e3]; t = T[0]; rs = []
for i, j, k in itertools.product((0, 1), repeat=3):   # the cube cell of side 2 holds 8 A sites and 8 B = A + t sites
    A = i * e1 + j * e2 + k * e3; rs.append((A, 'octahedron' if (i + j + k) % 2 == 0 else 'OCD Stella')); rs.append((A + t, 'OCD Stella'))
out.append(analyse(f'OCD Stella + octahedra, rock salt ({len(rs)} sites per cell)', C2, rs))
print('\n'.join(out)); open('data/crystal-symmetry.txt', 'w').write('\n'.join(out) + '\n')
