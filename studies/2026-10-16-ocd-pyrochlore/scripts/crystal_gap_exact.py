# The crystal's gap in convex pieces, exact in Q(√5) (DICTO 2026-10-16: "exact pass"). Stella–icosahedron crystal: OCD Stellas S on one
# network of the OCD's bcc packing, on the other the icosahedron I of the OCD's 20 hexagon planes. Each sits in its Voronoi cell V; V minus
# the solid is cut by cones from the centre over the solid's free faces. Exact: containment, every piece's corners, squared edges, volume,
# sums, and the kinds (pieces with equal multisets of squared edges and equal volume; congruent up to mirror image).
# -> data/crystal-gap-exact.txt
src = open('scripts/golden_fill.py').read(); exec(src[:src.index('A0 = ADP[0]')])
from collections import Counter
OK = {key(v) for v in OCD}; OPS = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        img = lambda v: [Q(sg[i]) * v[perm[i]] for i in range(3)]
        if all(key(img(v)) in OK for v in OCD): OPS.append((perm, sg))
orbit = {}
for A in ADP:
    for perm, sg in OPS:
        W = [[Q(sg[i]) * v[perm[i]] for i in range(3)] for v in A['V']]; orbit[frozenset(key(w) for w in W)] = W
corners = [v for W in orbit.values() for v in W]
HEX = [(n, max((dot(n, v) for v in corners + OCD), key=lambda x: x.f())) for _, n, _ in hexes]
LAT = []
for m in itertools.product(range(-2, 3), repeat=3):
    if not any(m): continue
    t = [Z, Z, Z]
    for c, b in zip(m, LB): t = add(t, mul(b, Q(c)))
    LAT.append(t)
CELL = polytope([(t, dot(t, t) / 2) for t in LAT]); HC = CELL['H']
S = polytope(H_K + HEX + HC); I = polytope([(n, d) for _, n, d in hexes])
vC, vS, vI = pvol(CELL), pvol(S), pvol(I)
out.clear(); say('DICTO · dictospheres.com'); say('The stella–icosahedron crystal: its gap in convex pieces (exact in Q(√5))')
say(f'cell V: {len(CELL["V"])} corners, volume {vC!r}; OCD Stella S: {len(S["V"])} corners, volume {vS!r}; icosahedron I: {len(I["V"])} corners, volume {vI!r}')
def where(P):
    worst = max(sgn(dot(n, v) - d) for v in P['V'] for n, d in HC)
    onw = sum(1 for v in P['V'] if any(dot(n, v) == d for n, d in HC))
    return f'{"inside V" if worst <= 0 else "NOT inside V"}, corners on the walls {onw} of {len(P["V"])}'
say(f'S: {where(S)};  I: {where(I)}')
def pieces(P, name):
    res = []; skipped = 0
    for n, d, on in P['F']:
        if any(iszero(cross(n, m)) and sgn(dot(n, m)) > 0 and d * dot(m, m) == dot(n, m) * e for m, e in HC): skipped += 1; continue   # face on a wall
        Vf = np.array([fl(P['V'][i]) for i in on]); c = Vf.mean(0); u = Vf[0] - c; u /= np.linalg.norm(u); w = np.cross(fl(n), u)
        ring = [on[i] for i in np.argsort(np.arctan2((Vf - c) @ w, (Vf - c) @ u))]
        H = [(neg(n), -d)]
        for i in range(len(ring)):
            m = cross(P['V'][ring[i]], P['V'][ring[(i + 1) % len(ring)]])
            if fl(m) @ c > 0: m = neg(m)
            H.append((m, Z))
        X = polytope(H + HC); res.append((name, len(on), X, pvol(X)))
    return res, skipped
PS, sS = pieces(S, 'OCD Stella'); PI, sI = pieces(I, 'icosahedron')
say(f'faces lying on the cell walls (no gap piece): S {sS} of {len(S["F"])}, I {sI} of {len(I["F"])}')
sumS = sum((p[3] for p in PS), Z); sumI = sum((p[3] for p in PI), Z)
say(f'sum of pieces around S {sumS!r}  vs V − S {(vC - vS)!r}: {"equal" if sumS == vC - vS else "DIFFERENT"}')
say(f'sum of pieces around I {sumI!r}  vs V − I {(vC - vI)!r}: {"equal" if sumI == vC - vI else "DIFFERENT"}')
gap = (vC - vS + vC - vI) / (Q(2) * vC); fill = Q(1) - gap
say(f'gap share of space {gap!r} = {gap.f():.6f}; fill {fill!r} = {fill.f():.6f} (crystal fill stated: 1523/32 − 669√5/32)')
say(f'  the icosahedra\'s share of the gap {(sumI / (sumI + sumS))!r} = {(sumI / (sumI + sumS)).f():.4f}')
def sig(X, vol):
    E = sorted(((lambda q: (q.a, q.b))(dot(sub(X['V'][i], X['V'][j]), sub(X['V'][i], X['V'][j]))) for i, j in X['E']))
    return (tuple(E), (vol.a, vol.b))
kinds = {}
for name, nf, X, vol in PS + PI: kinds.setdefault((name, nf, sig(X, vol)), []).append((X, vol))
say(f'kinds (equal squared edges and volume): {len(kinds)}')
for (name, nf, (E, _)), L in sorted(kinds.items(), key=lambda kv: -kv[1][0][1].f()):
    X, vol = L[0]; fc = dict(Counter(len(on) for _, _, on in X['F']))
    say(f'  around the {name}, on a {nf}-gon face: {len(L)} pieces; {len(X["V"])} corners, {len(X["F"])} faces {fc}, {len(X["E"])} edges; volume {vol!r} = {vol.f():.6f}')
    say(f'     squared edges: {", ".join(sorted({repr(dot(sub(X["V"][i], X["V"][j]), sub(X["V"][i], X["V"][j]))) for i, j in X["E"]}))}')
open('data/crystal-gap-exact.txt', 'w').write('\n'.join(out) + '\n')
