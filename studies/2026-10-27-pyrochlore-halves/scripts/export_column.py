# Pictures (DICTO 2026-10-27): one period of each stacking at weight a, every piece as an OBJ object named <role>_<type>_<n>:
# role tet (S, C: the network's pieces) or void (O, Y halves); type c / h = the layer it is borrowed from. Usage: export_column.py a word...
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import cells
from pyro import layer_types
from halves import pieces as _p
from scipy.spatial import ConvexHull
a = float(sys.argv[1]); W = {'S': a, 'C': a, 'O': 0, 'Y': 0}
PATCH = '--patch' in sys.argv; sys.argv = [x for x in sys.argv if x != '--patch']
from pyro import A1, A2
for word in sys.argv[2:]:
    S = cells.sites(word); ty = layer_types(word); n = len(word); s = ''; base = 1; m = 0
    for i, (t, k, p) in enumerate(S):
        parts = [('tet', k if t == 'S' else (k + 1) % n, cells.cell(word, i, W))] if t in 'SC' else \
                [('void', k, cells.cell_cut(word, i, W, 1, (k + .5) * cells.H - p[2])), ('void', (k + 1) % n, cells.cell_cut(word, i, W, -1, (k + .5) * cells.H - p[2]))]
        reps = [i * A1 + j * A2 + np.array([0, 0, l * n * cells.H]) for i in range(-1, 2) for j in range(-1, 2) for l in range(0, max(1, 6 // n))] if PATCH else [np.zeros(3)]
        for role, layer, h in parts:
          if h is None or (PATCH and role == 'void'): continue
          for sh in reps:
            V = h.points[h.vertices]; hh = ConvexHull(V); V = V + p + sh
            s += f'o {role}_{ty[layer]}_{m}\n' + ''.join(f'v {x} {y} {z}\n' for x, y, z in V)
            for tri in hh.simplices:
                a_, b_, c_ = tri
                nrm = np.cross(hh.points[b_] - hh.points[a_], hh.points[c_] - hh.points[a_])
                if np.dot(nrm, hh.points[a_] - hh.points.mean(0)) < 0: b_, c_ = c_, b_
                s += f'f {a_ + base} {b_ + base} {c_ + base}\n'
            base += len(V); m += 1
    open(f'{"patch" if PATCH else "col"}_{word}.obj', 'w').write(s); print(word, m, 'pieces')
