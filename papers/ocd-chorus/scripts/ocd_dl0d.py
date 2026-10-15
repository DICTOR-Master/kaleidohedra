# Combinatorial identity check (DICTO: "confirm the dL0D face arrangement"). Exact, no floating point in the decision: the OCD's
# face map (faces as consistently oriented vertex cycles, from data/chorus-fork.json) is compared with two constructions from the
# dodecahedron by an oriented-map isomorphism search (seed one dart, propagate by next-in-face and across-edge; mirror allowed).
# For 3-connected planar maps this decides combinatorial equivalence.
#  (A) pentakis dodecahedron with its 20 six-valent corners cut down to the edge midpoints;
#  (B) the dual of L0(D), Antiprism's joined-lace of the dodecahedron (L0: lace with the L1 quads left unsplit: each face gets a
#      twisted smaller copy; per face edge one inner triangle; per original edge one quad).
import json, itertools, numpy as np
J = json.load(open('data/chorus-fork.json')); OV = np.array(J['ocd']); OF = J['faces']
phi = (1 + 5 ** .5) / 2
DV = [np.array(p, float) for p in itertools.product((-1, 1), repeat=3)]
for s in (-1, 1):
    for t in (-1, 1):
        for k in range(3): v = [0, 0, 0]; v[k] = 0; v[(k + 1) % 3] = s / phi; v[(k + 2) % 3] = t * phi; DV.append(np.array(v))
DV = np.array(DV); IC = []
for s in (-1, 1):
    for t in (-1, 1):
        for k in range(3):
            for a_, b_ in ((s, t * phi), (s * phi, t)): v = [0, 0, 0]; v[(k + 1) % 3] = a_; v[(k + 2) % 3] = b_; IC.append(np.array(v))
def ring(ids, P, n):                                       # order points round axis n
    c = P[ids].mean(axis=0); e = P[ids[0]] - c; e2 = np.cross(n, e)
    return sorted(ids, key=lambda i: np.arctan2((P[i] - c) @ e2, (P[i] - c) @ e))
DF = []
for n in IC:
    d = DV @ n; ids = list(np.where(d > d.max() - 1e-9)[0])
    if len(ids) == 5: DF.append(ring(ids, DV, n))
assert len(DF) == 12
def orient(faces, P):                                      # make every face counter-clockwise seen from outside (Newell normal)
    out = []
    for f in faces:
        nn = sum(np.cross(P[f[i]], P[f[(i + 1) % len(f)]]) for i in range(len(f)))
        out.append(list(f) if nn @ P[f].mean(axis=0) > 0 else list(f)[::-1])
    return out
# (A) cut-down pentakis dodecahedron
pts = []; idx = {}
def V(key, p):
    if key not in idx: idx[key] = len(pts); pts.append(p)
    return idx[key]
apex = {i: V(('a', i), DV[f].mean(axis=0) * 1.15) for i, f in enumerate(DF)}
pos = lambda x: DV[x[1]] if x[0] == 'd' else pts[apex[x[1]]]
mid = lambda x, y: V(('m',) + tuple(sorted([x, y])), (pos(x) + pos(y)) / 2)
FA = []
for i, f in enumerate(DF):
    for k in range(5):
        d1, d2 = ('d', f[k]), ('d', f[(k + 1) % 5]); a = ('a', i)
        FA.append([apex[i], mid(a, d1), mid(d1, d2), mid(a, d2)])
P = np.array(pts)
for v in range(20):
    ids = [idx[k] for k in idx if k[0] == 'm' and ('d', v) in k[1:]]; assert len(ids) == 6; FA.append(ring(ids, P, DV[v]))
FA = orient(FA, P); PA = P
# (B) L0(D), then its dual
pts = [p for p in DV]; FB = []; W = {}
for i, f in enumerate(DF):
    c = DV[f].mean(axis=0)
    for k in range(5): W[(i, k)] = len(pts); pts.append(c + 0.55 * ((DV[f[k]] + DV[f[(k + 1) % 5]]) / 2 - c))
    FB.append([W[(i, k)] for k in range(5)])
    for k in range(5): FB.append([W[(i, k)], W[(i, (k + 1) % 5)], f[(k + 1) % 5]])
eside = {}
for i, f in enumerate(DF):
    for k in range(5): eside.setdefault(frozenset((f[k], f[(k + 1) % 5])), []).append((f[k], f[(k + 1) % 5], W[(i, k)]))
for e, ((a, b, wF), (_, _, wG)) in eside.items(): FB.append([a, wG, b, wF])
PB = np.array(pts); FB = orient(FB, PB)
def dual(faces):
    E = {}
    for fi, f in enumerate(faces):
        for k in range(len(f)): E[(f[k], f[(k + 1) % len(f)])] = fi
    out = {}
    for (a, b), fi in E.items():
        if a in out: continue
        cyc = []; f0 = fi; x = b
        while True:
            cyc.append(f0); g = E[(x, a)]; gf = faces[g]; y = gf[(gf.index(a) + 1) % len(gf)]; f0, x = g, y
            if f0 == fi: break
        out[a] = cyc
    return list(out.values())
def stats(faces):
    from collections import Counter
    nv = len({v for f in faces for v in f}); ne = sum(len(f) for f in faces) // 2
    deg = Counter(); [deg.update(f) for f in faces]
    return nv, ne, len(faces), sorted(Counter(len(f) for f in faces).items()), sorted(Counter(deg.values()).items())
def iso(F1, F2):                                           # oriented map isomorphism, F2 tried in both orientations
    def darts(F):
        nxt, opp, D = {}, {}, {}
        for fi, f in enumerate(F):
            for k in range(len(f)): D[(f[k], f[(k + 1) % len(f)])] = (fi, k)
        for (a, b), (fi, k) in D.items():
            f = F[fi]; nxt[(a, b)] = (b, f[(k + 2) % len(f)]); opp[(a, b)] = (b, a)
        return list(D), nxt, opp
    d1, n1, o1 = darts(F1)
    for G in (F2, [f[::-1] for f in F2]):
        d2, n2, o2 = darts(G)
        if len(d1) != len(d2): return False
        for s in d2:
            m = {d1[0]: s}; st = [d1[0]]; ok = True; vm = {}
            while st and ok:
                x = st.pop()
                for f1, f2 in ((n1, n2), (o1, o2)):
                    y, z = f1[x], f2[m[x]]
                    if y in m:
                        if m[y] != z: ok = False; break
                    else: m[y] = z; st.append(y)
            if ok and len(m) == len(d1):
                for (a, b), (c, d) in m.items():
                    if vm.setdefault(a, c) != c: ok = False; break
                if ok and len(set(vm.values())) == len(vm): return True
    return False
OFo = orient(OF, OV)
out = [f'OCD: V, E, F, face sizes, vertex degrees = {stats(OFo)}',
       f'(A) cut-down pentakis dodecahedron: {stats(FA)}; same face arrangement as the OCD: {iso(OFo, FA)}',
       f'(B) L0(D): {stats(FB)}; dual of L0(D): {stats(dual(FB))}; same face arrangement as the OCD: {iso(OFo, dual(FB))}',
       f'    Hecatodihedron (dual of the OCD) vs L0(D) directly: {iso(dual(OFo), FB)}',
       f'    (A) vs (B) dual: {iso(FA, dual(FB))}']
print('\n'.join(out)); open('data/ocd-dl0d.txt', 'w').write('\n'.join(out) + '\n')
# controls: a random relabelling must still match; a map with one quad's corners re-paired (a different arrangement) must not
rng = np.random.default_rng(1); perm = rng.permutation(102)
FR = [[int(perm[v]) for v in f] for f in FA]
FX = [list(f) for f in FA]; h = next(i for i, f in enumerate(FX) if len(f) == 6); FX[h][1], FX[h][2] = FX[h][2], FX[h][1]   # one hexagon's corners out of order
ctl = [f'controls: shuffled labels match {iso(OFo, FR)} (expect True); a map with one hexagon with two corners swapped matches {iso(OFo, FX)} (expect False)']
print('\n'.join(ctl)); open('data/ocd-dl0d.txt', 'a').write('\n'.join(ctl) + '\n')
