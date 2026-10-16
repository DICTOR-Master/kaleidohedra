# The stella-cut companion, exact in Q(√5) (DICTO 2026-10-16: "make the stella cut"; "could it have a partner to fill space?").
# Companion C = hull of the OCD and the 60 GBPCs around it (the orbit of golden_fill.py's exact adapters under the copy's cubic symmetry):
# the golden envelope's 30 planes ∩ 20 three-fold planes through the GBPCs' outer corners (NOT the OCD's own hexagon planes, which lie at
# the icosahedron that only touches the golden planes; correction of the float description, 2026-10-16).
# Stella cut S = C ∩ the Voronoi cell of the bcc packing (all lattice vectors with coefficients up to 2; planes t·x ≤ |t|²/2).
# Reports, exact: corners, faces by sides, which planes cut, volume, its share of the cell, and whether copies of S at the lattice sites
# overlap (they cannot: S ⊂ cell) and which faces touch. Then the gap: cell − S per cell. -> data/stella-cut-exact.txt, .json
import os
src = open('scripts/golden_fill.py').read(); head = src[:src.index('A0 = ADP[0]')]
exec(head)
from collections import Counter
# exact symmetry of the copy in its packing: signed permutations fixing the OCD's corner set
OK = {key(v) for v in OCD}; OPS = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        img = lambda v: [Q(sg[i]) * v[perm[i]] for i in range(3)]
        if all(key(img(v)) in OK for v in OCD): OPS.append((perm, sg))
orbit = {}
for A in ADP:
    for perm, sg in OPS:
        W = [[Q(sg[i]) * v[perm[i]] for i in range(3)] for v in A['V']]
        orbit[frozenset(key(w) for w in W)] = W
GB = list(orbit.values())
say(f'symmetry of the copy in its packing: {len(OPS)} signed permutations; GBPCs around one copy: {len(GB)} (from {len(ADP)} per cell)')
corners = [v for W in GB for v in W]
HEX = [(n, max((dot(n, v) for v in corners + OCD), key=lambda x: x.f())) for _, n, _ in hexes]   # 20 three-fold planes through the outermost points

LAT = []
for m in itertools.product(range(-2, 3), repeat=3):
    if not any(m): continue
    t = [Z, Z, Z]
    for c, b in zip(m, LB): t = add(t, mul(b, Q(c)))
    LAT.append(t)
VOR = [(t, dot(t, t) / 2) for t in LAT]
C = polytope(H_K + HEX)
hexd = [d / Q(1) for _, d in HEX]
say(f'three-fold planes of the companion vs the OCD hexagon planes (distance², exact): {(HEX[0][1] * HEX[0][1] / dot(HEX[0][0], HEX[0][0]))!r} vs {(hexes[0][2] * hexes[0][2] / dot(hexes[0][1], hexes[0][1]))!r}')
CELL = polytope(VOR)
S = polytope(H_K + HEX + VOR)
vC, vS, vCell = pvol(C), pvol(S), pvol(CELL)
fs = lambda P: dict(Counter(len(g[2]) for g in P['F']))
kind = lambda n: ('golden (2-fold)' if axtype(n) == '2' else 'OCD hexagon (3-fold)' if axtype(n) == '3' else 'other')
def which(P):
    c = Counter()
    for n, d, on in P['F']:
        tag = 'Voronoi' if any(iszero(cross(n, t)) and dot(n, t).f() > 0 and d * dot(t, t) == dot(n, t) * dot(t, t) / 2 for t in LAT) else kind(n)
        c[(tag, len(on))] += 1
    return dict(c)
say('== The companion C and its stella cut S (exact)')
say(f'bcc cell (Voronoi): {len(CELL["V"])} corners, faces {fs(CELL)}, volume {vCell!r} = {vCell.f():.6f} (det of the basis {cellv!r})')
say(f'companion C: {len(C["V"])} corners, faces {fs(C)}, volume {vC!r} = {vC.f():.6f}')
say(f'stella cut S = C ∩ cell: {len(S["V"])} corners, faces {fs(S)}, by plane kind {which(S)}')
say(f'  volume {vS!r} = {vS.f():.6f}; share of the cell {(vS / vCell)!r} = {(vS / vCell).f():.6f}')
say(f'  the Voronoi planes that cut C: {sorted(set((round(fl(t)[0], 4), round(fl(t)[1], 4), round(fl(t)[2], 4)) for t in LAT if any(iszero(cross(n, t)) and dot(n, t).f() > 0 for n, d, on in S["F"])))[:16]}')
json.dump({'S': {'v': [fl(v).tolist() for v in S['V']], 'f': [on for _, _, on in S['F']]}, 'cell': {'v': [fl(v).tolist() for v in CELL['V']], 'f': [on for _, _, on in CELL['F']]},
           'basis': [fl(b).tolist() for b in LB]}, open('data/stella-cut-exact.json', 'w'))
open('data/stella-cut-exact.txt', 'w').write('DICTO · dictospheres.com\n' + '\n'.join(out) + '\n')
