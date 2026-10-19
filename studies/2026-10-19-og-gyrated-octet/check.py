# The OG in the gyrated octet (DICTO 2026-10-19), first EXACT check in Q(sqrt5). In the octet (#37) every regular octahedron holds an OG
# with its 8 joint hexagons on the 8 faces. In the gyrated octet (hcp stacking), at each gyrated layer two octahedra share a face: the
# neighbour is the octahedron's mirror image in that face, so its OG is the OG's mirror image. Checks: the two OGs meet exactly on the
# shared face (the same hexagon); whether the mirror OG is just a translate (as in the bcc joint) or a genuinely mirrored copy; and what
# meets round the hexagon's edges (the angle between the faces of the two OGs).
import json, os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-10-19-five-fold-octet'))
from exact_cycle import Q5, Fr, dot
from exact_shells import solid, cross, sub
D = json.load(open(os.path.join(HERE, '..', '2026-10-18-ocd-octet', 'data', 'step1-ocd-exact.json')))
q = lambda s: Q5(*[Fr(x) for x in s.split('|')])
V = [tuple(q(c) for c in v) for v in D['V']]; R = q(D['R']) if isinstance(D['R'], str) else None
print('corners', len(V), 'R', D['R'])
n = (Q5(1), Q5(1), Q5(1)); nn = dot(n, n)                       # the shared face: x + y + z = R
Rv = R if R is not None else max((dot(n, v) for v in V), key=lambda x: x.f())
on = [v for v in V if dot(n, v) == Rv]; print('OG corners on the face x+y+z=R:', len(on))
refl = lambda v: tuple(v[k] - 2 * (dot(n, v) - Rv) / nn * n[k] for k in range(3))
M = [refl(v) for v in V]
print('mirror OG meets OG on the face in the same corners:', {v for v in M if dot(n, v) == Rv} == set(on))
t = tuple(2 * Rv / nn * n[k] for k in range(3))                 # translation by twice the face distance along the normal
print('mirror OG equals the translated OG (bcc-type joint):', set(M) == {tuple(v[k] + t[k] for k in range(3)) for v in V})
# the angle across the joint: the OG faces that share an edge with the joint hexagon, and their mirror partners
H = solid(V); hexplane = [(m, d) for m, d in H if all((dot(m, v) - d) == Q5(0) for v in on)]
print('joint face is one face of the OG:', len(hexplane) == 1)
edges = [(a, b) for a, b in itertools.combinations(on, 2)]
adj = [(m, d) for m, d in H if (m, d) not in hexplane and sum((dot(m, v) - d) == Q5(0) for v in on) == 2]
print('OG faces round the hexagon:', len(adj))
m, d = adj[0]; mm = (m, d); mr = tuple(m[k] - 2 * dot(m, n) / nn * n[k] for k in range(3))
c = dot(m, mr) / dot(m, m)                                       # cos of the angle between the face and its mirror (same length normals)
print('cos(angle between an adjacent face and its mirror) =', c, '≈', round(c.f(), 6))
