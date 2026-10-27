# Five pyramids study (DICTO, 2026-10-27): exact face-matching table of the pieces, at the scales used in the search.
# For every face shape that is not an equilateral triangle: which pieces carry a congruent face (exact: equal sorted
# squared sides for triangles; for quadrilaterals the cyclic side sequence and both diagonals, up to rotation/reversal).
# This is what limits gluings: in a deltahedron every such face must be glued to a congruent face (or merged into a
# coplanar equilateral face).
import json, sys, os, itertools
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import build, phi

USE = ['Tetrahedron', 'Octahedron', 'Icosahedron', 'Q (tetrahedron face pyramid)', 'Octahedron face pyramid', 'Cleo-Icos',
       'Half octahedron P', 'Antonius', 'Admiral Cap', 'M-S t1', 'Hound Tooth (M-S t2)', 'Tricap (M-S t3)', 'CLEO (M-S t4)',
       'M-S t5', 'AXE (M-S t6)', 'Weirdstone', 'Tadpole', 'Cube face pyramid', 'Dodecahedron face pyramid']  # Penta-cleo: float source, no equilateral face
MS = ['M-S t1', 'Hound Tooth (M-S t2)', 'Tricap (M-S t3)', 'CLEO (M-S t4)', 'M-S t5', 'AXE (M-S t6)']

def d2(a, b): return sp.nsimplify(sp.radsimp(sp.expand(((a - b).T * (a - b))[0])))

def key(V, f, s2):
    n = len(f); sides = [sp.nsimplify(sp.radsimp(s2 * d2(V[f[i]], V[f[(i + 1) % n]]))) for i in range(n)]
    if n == 3: return ('tri',) + tuple(sorted(sides, key=lambda x: float(x)))
    diags = tuple(sorted([sp.nsimplify(sp.radsimp(s2 * d2(V[f[i]], V[f[(i + 2) % n]]))) for i in range(n)], key=lambda x: float(x)))
    rots = [tuple(sides[i:] + sides[:i]) for i in range(n)]; rots += [tuple(reversed(r)) for r in rots]
    return ('poly%d' % n, min(rots, key=lambda r: [float(x) for x in r]), diags)

def run():
    L = build(); table = {}; pieces = {}
    for nm in USE:
        P = L[nm]; V = P['V']
        eqs = [d2(V[f[0]], V[f[1]]) for f in P['F'] if len(f) == 3 and len({d2(V[f[i]], V[f[(i + 1) % 3]]) for i in range(3)}) == 1]
        scales = [1 / min(eqs, key=float)] if eqs else [sp.Integer(1)]
        if nm in MS:
            ls = sorted({d2(V[f[i]], V[f[(i + 1) % 3]]) for f in P['F'] for i in range(3)}, key=float)
            scales.append(1 / [x for x in ls if sp.simplify(x - 1 / scales[0]) != 0][0])
        for s2 in scales:
            tag = nm if s2 == scales[0] else nm + ' [other scale]'
            ks = [key(V, f, s2) for f in P['F']]; pieces[tag] = ks
            for k in ks:
                if k[0] == 'tri' and k[1] == k[2] == k[3]: continue
                table.setdefault(k, set()).add(tag)
    rows = []
    for k, who in sorted(table.items(), key=lambda kv: (kv[0][0], [float(x) for x in (kv[0][1:] if kv[0][0] == 'tri' else kv[0][1])])):
        shape = (k[0], [str(sp.sqrt(x)) for x in (k[1:] if k[0] == 'tri' else k[1])])
        rows.append(dict(shape=shape, pieces=sorted(who)))
        print(shape, '->', sorted(who))
    json.dump(rows, open('data/face-matching-exact.json', 'w'), indent=1)

if __name__ == '__main__':
    run()
