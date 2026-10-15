# Ogdoecontahedron pyrochlore network (DICTO, 2026-10-16). Step 1, exact in Q(sqrt5).
# Copies of the DICTO Ogdoecontahedron (OCD) joined face to face on hexagons. The solid is centrally symmetric, so a copy shifted
# by t = 2 d n / |n|^2 (n.x = d a hexagon plane) puts its opposite hexagon exactly on ours. Joining through one tetrahedral set of
# four hexagons gives a diamond network (sites A on an fcc lattice, sites B = A + t1); the joint hexagons sit at the bond
# midpoints, which form a pyrochlore lattice. Collision test, exact: copies at u and v overlap iff (u - v)/2 is inside the OCD,
# touch iff it is on the surface, are apart iff outside (K - K = 2K for a centrally symmetric K).
import sys, io, os, contextlib, itertools, json, numpy as np
from scipy.spatial import ConvexHull
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
f = lambda v: np.array([x.f() for x in v]); F = lambda V: np.array([f(v) for v in V])
dot = lambda a, b: sum((a[i] * b[i] for i in range(3)), Q(0))
cross = lambda u, w: [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
sub = lambda u, w: [u[i] - w[i] for i in range(3)]; add = lambda u, w: [u[i] + w[i] for i in range(3)]
St = dict(rev); OCD = St['dual of the Hecatodihedron']; Of = F(OCD)
gc.frame(Of, gc.icosa_axes(F(St['icosahedron'])), 'Ogdoecontahedron')
# exact face planes n.x = d (outward), with the number of corners on each
planes = []
for e in ConvexHull(Of).equations:
    idx = [i for i in range(len(OCD)) if abs(Of[i] @ e[:3] + e[3]) < 1e-7]
    if any(set(idx) == set(p[0]) for p in planes): continue
    n = cross(sub(OCD[idx[1]], OCD[idx[0]]), sub(OCD[idx[2]], OCD[idx[0]])); d = dot(n, OCD[idx[0]])
    if d.f() < 0: n, d = [-x for x in n], -d
    assert all(dot(n, OCD[i]) == d for i in idx); planes.append((idx, n, d))
hexes = [p for p in planes if len(p[0]) == 6]; assert len(hexes) == 20 and len(planes) == 80
unit = lambda n: f(n) / np.linalg.norm(f(n))
# a tetrahedral set of four hexagon normals (pairwise cos = -1/3)
tet = next(c for c in itertools.combinations(range(20), 4) if all(abs(unit(hexes[a][1]) @ unit(hexes[b][1]) + 1 / 3) < 1e-9 for a, b in itertools.combinations(c, 2)))
T = [[x * (Q(2) * hexes[i][2] / dot(hexes[i][1], hexes[i][1])) for x in hexes[i][1]] for i in tet]   # exact bond vectors t_i
# the opposite hexagon of a copy shifted by t_i lands exactly on hexagon i (central symmetry), checked exactly
for i, t in zip(tet, T):
    face = [OCD[j] for j in hexes[i][0]]; opp = [[-x for x in OCD[j]] for j in hexes[i][0]]   # the antipodal hexagon's corners
    moved = [add(v, t) for v in opp]
    assert all(any(all(m[k] == w[k] for k in range(3)) for w in face) for m in moved), 'hexagons do not coincide'
def where(D):   # position of D/2 relative to the OCD: 'inside', 'surface' (with face sizes), 'outside'; exact
    h = [x * Q(Fr(1, 2)) for x in D]; worst = None; on = []
    for idx, n, d in planes:
        r = dot(n, h) - d
        if r.f() > 0: return 'outside', []
        if r == Q(0): on.append(len(idx))
    return ('surface', sorted(on)) if on else ('inside', [])
# a patch of the diamond network: A sites = integer combinations of t_i - t_j, B = A + t_0
Lb = [sub(T[0], T[k]) for k in (1, 2, 3)]
A = []
for m in itertools.product(range(-2, 3), repeat=3):
    s = [Q(0)] * 3
    for c, b in zip(m, Lb): s = add(s, [x * Q(c) for x in b])
    A.append(s)
sites = [('A', s) for s in A] + [('B', add(s, T[0])) for s in A]
c0 = np.array([0., 0., 0.]); sites = sorted(sites, key=lambda s: np.linalg.norm(f(s[1]) - c0))[:60]
over, touch, apart = 0, {}, 0
for (ka, u), (kb, v) in itertools.combinations(sites, 2):
    w, on = where(sub(u, v))
    if w == 'inside': over += 1
    elif w == 'surface': touch[(ka + kb, tuple(on))] = touch.get((ka + kb, tuple(on)), 0) + 1
    else: apart += 1
# pyrochlore: the four joint centres around a site form a regular tetrahedron, exact
J = [[x * Q(Fr(1, 2)) for x in t] for t in T]
e2 = {(dot(sub(J[a], J[b]), sub(J[a], J[b])).a, dot(sub(J[a], J[b]), sub(J[a], J[b])).b) for a, b in itertools.combinations(range(4), 2)}
# packing: two OCDs per primitive fcc cell
cellv = det3(*Lb); cellv = cellv if cellv.f() > 0 else Q(0) - cellv; vO = volume(OCD, Of); frac = Q(2) * vO / cellv
out = [f'OCD: {len(planes)} faces (20 hexagons at distance {(hexes[0][2] * hexes[0][2] / dot(hexes[0][1], hexes[0][1])).f() ** .5:.6f}), volume {vO!r}',
       f'tetrahedral hexagon set {tet}; bond vectors exact, |t|^2 = {dot(T[0], T[0])!r} = {dot(T[0], T[0]).f():.6f}',
       'joined copies: the opposite hexagon lands exactly on the shared hexagon (exact check passed for all four bonds)',
       f'collision test over {len(sites)} sites ({len(sites) * (len(sites) - 1) // 2} pairs): overlapping {over}; touching {sum(touch.values())} '
       + '; '.join(f'{k[0]} on faces of {list(k[1])} corners: {c}' for k, c in sorted(touch.items())) + f'; apart {apart}',
       f'joints: the four hexagon centres around a site form a regular tetrahedron: {len(e2) == 1} (edge^2 {Q(*next(iter(e2)))!r}); bond midpoints of diamond = pyrochlore',
       f'packing: fcc primitive cell volume {cellv!r} = {cellv.f():.6f}; two OCDs per cell fill {frac!r} = {frac.f():.6f} of space; gap {1 - frac.f():.6f}']
print('\n'.join(out)); open('data/network.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'T': [f(t).tolist() for t in T], 'Lb': [f(b).tolist() for b in Lb], 'ocd': Of.tolist(), 'tet': list(tet)}, open('data/network.json', 'w'))

# Step 2a (gaps): in diamond the large empty spaces sit at the sites shifted by 2 t_0 (and 3 t_0), the other half of the
# four-sublattice fcc frame. Does a second OCD network shifted by 2 t_0 fit into the first one's gaps (a double network)?
S2 = [(k, add(s, [x * Q(2) for x in T[0]])) for k, s in sites]
over2, touch2, apart2 = 0, {}, 0
for (ka, u) in sites[:30]:
    for (kb, v) in S2:
        w, on = where(sub(u, v))
        if w == 'inside': over2 += 1
        elif w == 'surface': touch2[tuple(on)] = touch2.get(tuple(on), 0) + 1
        else: apart2 += 1
frac2 = frac * Q(2)
out2 = [f'second network shifted by 2 t0: overlapping pairs {over2}; touching {sum(touch2.values())} '
        + '; '.join(f'on faces of {list(k)} corners: {c}' for k, c in sorted(touch2.items())) + f'; apart {apart2}',
        f'double network would fill {frac2!r} = {frac2.f():.6f} of space' + (' (if no overlap)' if over2 == 0 else ' (but the networks overlap)')]
print('\n'.join(out2)); open('data/network.txt', 'a').write('\n'.join(out2) + '\n')
