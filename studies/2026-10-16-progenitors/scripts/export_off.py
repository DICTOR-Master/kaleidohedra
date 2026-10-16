# Exports the progenitors solids as OFF files for an independent check with Antiprism (A. Rossiter, antiprism.com):
# H, O (at 3φ²/4), the H–O hull (jtI) and core (rTI), X (Palintriacontahedron), M (Metaxyhexecontahedron) and M's polar (in ρ² = φ²/4),
# from data/full-cycle.json (float corners of exact stations) and data/gap-chain.json. Faces are the hull's planes, merged. -> antiprism/*.off
import json, numpy as np
from scipy.spatial import ConvexHull
J = json.load(open('data/full-cycle.json'))['st']; C = dict((n, np.array(v)) for n, v in json.load(open('data/gap-chain.json')))
def faces(P):
    h = ConvexHull(P); E = []; F = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-6) for q in E): continue
        E.append(e); idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-6]; Q = P[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return F
def write(name, P):
    P = np.array(P); P = P[ConvexHull(P).vertices]; F = faces(P)
    with open(f'antiprism/{name}.off', 'w') as f:
        f.write(f'OFF\n# DICTO · dictospheres.com — {name} (progenitors study)\n{len(P)} {len(F)} 0\n')
        for v in P: f.write(' '.join(f'{x:.12f}' for x in v) + '\n')
        for fc in F: f.write(f'{len(fc)} ' + ' '.join(map(str, fc)) + '\n')
    print(name, len(P), 'vertices', len(F), 'faces')
for k, n in (('H', 'hecatodihedron'), ('O94', 'ogdoecontahedron'), ('hull', 'ho-hull'), ('rTI', 'ho-core'), ('X', 'palintriacontahedron'), ('RT', 'rt'), ('Ip3', 'ico-phi3')):
    write(n, J[k]['v'])
write('metaxyhexecontahedron', C['G'])
G = C['G']; h = ConvexHull(G); E = []
for e in h.equations:
    if not any(np.allclose(e, q, atol=1e-9) for q in E): E.append(e)
rho2 = ((1 + 5 ** .5) / 2) ** 2 / 4
write('metaxy-dual', [-e[:3] / e[3] * rho2 for e in E])
