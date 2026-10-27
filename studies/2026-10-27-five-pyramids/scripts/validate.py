# Five pyramids study (DICTO, 2026-10-27): known-case sanity checks of the gluing engine (enum_glue.py).
#  1. icosahedron + 6 Admiral Caps (glued greedily on the icosahedron) = the regular octahedron of edge phi^2/sqrt2 (#47);
#  2. Cleo-Icos + Antonius + Cleo-Icos = the prolate golden rhombohedron, 6 golden rhombi (#20, #44);
#  3. 20 Cleo-Icos round one centre = the icosahedron;  4. 4 Q = the tetrahedron.
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enum_glue as E

lib = E.library(); ix = {p['name']: i for i, p in enumerate(lib)}

def greedy(start, piece, n, want=None):
    cl = [(ix[start], np.eye(3), np.zeros(3))] if start else []
    while len(cl) < n:
        done = False
        for x in E.exposed(lib, cl):
            for pl in E.placements(lib, x, ix[piece]):
                if want and not want(lib, cl, pl): continue
                if not E.overlaps(lib, cl, pl): cl.append(pl[:3]); done = True; break
            if done: break
        if not done: break
    return cl

def report(name, cl):
    info = {}; F = E.surface_report(lib, cl, info)
    if F is None: print(name, 'FAILED', info); return
    shapes = sorted(tuple(np.round(sorted(np.linalg.norm(P - np.roll(P, -1, 0), axis=1)), 6)) for P in F)
    print(name, '| pieces', len(cl), '| merged faces', len(F), '| side lengths', sorted(set(shapes)), '| chi', info.get('chi'))

# 1: caps only on edge pairs of the icosahedron, i.e. both equilateral faces of the cap on the icosahedron
def both_on_ico(lib, cl, pl):
    j, R, t = pl[:3]; P = lib[j]['V'] @ R.T + t
    PHI = (1 + 5 ** 0.5) / 2; octa = np.vstack([np.eye(3), -np.eye(3)]) * PHI ** 2 / 2   # Pacioli's octahedron round it
    return min(np.linalg.norm(octa - P[2], axis=1)) < 1e-6      # vertex 2 of the cap is its apex (edgeRoof.js order)
report('icosahedron + Admiral Caps', greedy('Icosahedron', 'Admiral Cap', 7, both_on_ico))
# 2
cl = [(ix['Antonius'], np.eye(3), np.zeros(3))]
for x in [f for f in E.exposed(lib, cl) if f['eq']]:
    cl.append(E.placements(lib, x, ix['Cleo-Icos'])[0][:3])
report('Cleo-Icos + Antonius + Cleo-Icos', cl)
# 3, 4: pyramids sharing one apex
def same_apex(lib, cl, pl):
    j, R, t = pl[:3]; return np.linalg.norm(lib[j]['V'][-1] @ R.T + t - lib[cl[0][0]]['V'][-1]) < 1e-6
for nm, n in [('Cleo-Icos', 20), ('Q (tetrahedron face pyramid)', 4), ('Octahedron face pyramid', 8)]:
    report('%d x %s' % (n, nm), greedy(nm, nm, n, same_apex))
