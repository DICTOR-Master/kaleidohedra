# DICTO 2026-10-17: "a construction of a scutoid turning it into a polyhedron that nests and fills space" — route A: are there scutoids
# already in DICTO's exact shell dissections? Every layer piece of the Spheres of Dharma (orig), the Inverted Shells (flip, ends setting)
# and Vajrayana's two closing layers is a cone cut: its side faces lie in planes through the centre, its two "bases" on the inner and
# outer shells. A piece is a (polyhedral) scutoid when its two bases have different numbers of sides and at least one corner lies on
# neither base (the Y-junction, giving a triangle on the side). Float classification of exact pieces (faces merged by plane, 1e-7).
# -> data/scutoid-survey.txt
import json, numpy as np
from scipy.spatial import ConvexHull
D = '/home/dicto/kaleidohedra/studies/'
SRC = [('Spheres of Dharma', D + '2026-10-16-interlock/data/orig-pieces.json'), ('Inverted Shells', D + '2026-10-16-interlock/data/flip-ends-pieces.json'),
       ('Vajrayana closing layers', D + '2026-10-16-progenitors/data/gap-pieces.json')]
def faces(V):
    h = ConvexHull(V); out = []
    for e in h.equations:
        if any(np.allclose(e, q[0], atol=1e-7) for q in out): continue
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]; out.append((e, idx))
    return out
def classify(P):
    V = np.array(P); F = faces(V); scale = np.linalg.norm(V, axis=1).max()
    lat = [f for f in F if abs(f[0][3]) < 1e-6 * scale]; base = [f for f in F if abs(f[0][3]) >= 1e-6 * scale]
    base.sort(key=lambda f: -f[0][3])        # -d: distance of the plane from the centre, inner first
    on_base = set(i for f in base for i in f[1]); free = [i for i in range(len(V)) if i not in on_base]
    sides = [len(f[1]) for f in base]
    tri_lat = sum(1 for f in lat if len(f[1]) == 3)
    sig = tuple(np.round(sorted(np.linalg.norm(V[i] - V[j]) for i in range(len(V)) for j in range(i + 1, len(V))), 4))
    kind = ('scutoid' if len(base) == 2 and sides[0] != sides[1] and free else
            'scutoid-like (bases differ, no free corner)' if len(base) == 2 and sides[0] != sides[1] else
            'frustum-like (equal bases)' if len(base) == 2 else f'{len(base)} base face(s)')
    return dict(kind=kind, bases=sides, free=len(free), corners=len(V), faces=len(F), lateral_triangles=tri_lat, sig=sig)
out = ['DICTO · dictospheres.com', 'Scutoid survey of DICTO\'s exact shell dissections (float classification of exact pieces)']
found = 0
for name, path in SRC:
    d = json.load(open(path)); out.append(f'\n== {name}')
    for layer, pieces in d.items():
        kinds = {}
        for P in pieces:
            c = classify(P); key = (c['kind'], tuple(c['bases']), c['free'], c['corners'], c['faces'], c['lateral_triangles']); kinds.setdefault(key, set()).add(c['sig'])
        out.append(f'  {layer}: {len(pieces)} pieces')
        for (k, b, fr, nc, nf, lt), sigs in sorted(kinds.items(), key=lambda x: x[0][0]):
            n = sum(1 for P in pieces if classify(P)['kind'] == k and tuple(classify(P)['bases']) == b and classify(P)['free'] == fr)
            mark = '  <== SCUTOID' if k == 'scutoid' else ''
            found += k == 'scutoid'
            out.append(f'     {k}: bases (inner, outer) sides {list(b)}, {fr} free corner(s), {nc} corners, {nf} faces, {lt} side triangles; {len(sigs)} shape(s){mark}')
out.append(f'\nscutoid kinds found: {found}')
print('\n'.join(out)); open('/home/dicto/kaleidohedra/studies/2026-10-17-scutoids/data/scutoid-survey.txt', 'w').write('\n'.join(out) + '\n')
