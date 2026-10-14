# 102 clean pieces for the Theaetetus Hecatodihedron (DICTO 2026-10-15: "look for new cuts for 102 clean pieces"):
#   20 core Cleo-Icos (the edge-1 core cut from its centre) + 20 radial columns (the dodecahedron minus the core, cut from the centre
#   through the core's 30 edges: one column per core face) + Dharma's 12 twisted pentagonal frusta + 30 t1 + 20 caps.
# Each column = cone(core face) ∩ dodecahedron ∩ {beyond the face plane}: an intersection of convex sets, hence convex. Checked here.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
J = json.load(open('cleo_heca.json')); P = lambda m: np.array(m['v']); vol = lambda Q: ConvexHull(Q).volume
core = P(J['core icosahedron'][0]); CH = ConvexHull(core)
D = ConvexHull(np.vstack([P(m) for k in ('core icosahedron', 'Cleo-Ico', 'flat pentagonal pyramid', 'X', 'Y', 'tripyr (to dodecahedron)') for m in J[k]]))
Dv = D.points[D.vertices]; Dh = []
for e in D.equations:
    if not any(np.allclose(e, f, atol=1e-5) for f in Dh): Dh.append(e)
cleo_in = [np.vstack([core[t], [0, 0, 0]]) for t in CH.simplices]
cols = []
for t, e in zip(CH.simplices, CH.equations):
    T = core[t]; n = e[:3]; c = T.mean(0)
    hs = [np.r_[-n, -e[3]]]             # beyond the face plane: n.x + e[3] >= 0, written as -n.x - e[3] <= 0
    for i in range(3):
        a, b = T[i], T[(i + 1) % 3]; m = np.cross(a, b); m = m if m @ c > 0 else -m   # plane through 0, a, b; keep the face side
        hs.append(np.r_[-m, 0.0])
    hs += [np.array(f) for f in Dh]
    inner = c * 1.2                                   # a point strictly inside the column
    HS = HalfspaceIntersection(np.array(hs), inner)
    cols.append(np.unique(np.round(HS.intersections, 9), axis=0))
outer = {k: [P(m) for m in J[k]] for k in ('twisted pentagonal frustum', 't1', 'cap (to Hecatodihedron)')}
pieces = [('core Cleo-Ico', Q) for Q in cleo_in] + [('column', Q) for Q in cols] + [(k, Q) for k, L in outer.items() for Q in L]
out = []
out.append(f'pieces: ' + ', '.join(f'{sum(1 for k2, _ in pieces if k2 == k)} {k}' for k in dict.fromkeys(k for k, _ in pieces)) + f' = {len(pieces)}')
convex = sum(abs(vol(Q) - ConvexHull(Q).volume) < 1e-12 for _, Q in pieces)
vc, vD = sum(map(vol, cleo_in)) + sum(map(vol, cols)), D.volume
out.append(f'core + 20 columns = {vc:.9f}; dodecahedron {vD:.9f} (diff {vc - vD:.1e})')
Hk = ConvexHull(np.vstack([Q for _, Q in pieces]))
out.append(f'all 102 = {sum(vol(Q) for _, Q in pieces):.6f}; Hecatodihedron hull {Hk.volume:.6f}')
# sampled cover of the Hecatodihedron: each point in exactly one piece
inside = lambda Q, x: all(e[:3] @ x + e[3] <= 1e-7 for e in ConvexHull(Q).equations)
rng = np.random.default_rng(5); h = {0: 0, 1: 0, 2: 0}; R = np.linalg.norm(Hk.points, axis=1).max()
eqs = [ConvexHull(Q).equations for _, Q in pieces]
for x in rng.uniform(-R, R, size=(30000, 3)):
    if all(e[:3] @ x + e[3] < -1e-7 for e in Hk.equations):
        k = sum(all(e[:3] @ x + e[3] <= 1e-7 for e in E) for E in eqs); h[min(k, 2)] += 1
out.append(f'sampled points in the Hecatodihedron: once {h[1]}, missed {h[0]}, twice {h[2]}')
C0 = cols[0]; hc = ConvexHull(C0); planes = []
for e, s in zip(hc.equations, hc.simplices):
    for p in planes:
        if np.allclose(p['e'], e, atol=1e-7): p['i'] |= set(s); break
    else: planes.append({'e': e, 'i': set(s)})
out.append(f'column: {len(C0)} corners, {len(planes)} faces (sides {sorted(len(p["i"]) for p in planes)}), volume {vol(C0):.6f}')
print('\n'.join(out)); open('cut102.txt', 'w').write('\n'.join(out) + '\n')
mesh = lambda Q: {'v': np.round(Q, 6).tolist(), 'f': ConvexHull(Q).simplices.tolist(), 'c': np.round(Q.mean(0), 6).tolist()}
groups = {}
for k, Q in pieces: groups.setdefault(k, []).append(mesh(Q))
json.dump(groups, open('cut102.json', 'w'))
