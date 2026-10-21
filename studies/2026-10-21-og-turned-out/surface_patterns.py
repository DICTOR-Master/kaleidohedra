# DICTO 2026-10-21: "in fact all the shells so far have different patterns". The surface patterns of every boundary solid of the Kyushindo
# cores, EXACT in Q(sqrt5) with the machinery of #38/#39 (one frame: the icosidodecahedron of circumradius phi):
#   the UP stations ID, RT, GTI, FPD (the Cleo Towers' and Polar Cleo Towers' boundaries are these, scaled by powers of 10/phi^4), and
#   the OG and its downward solids TPH, TQH, TQP, TQHD (the OG turned out's beats are these, scaled by powers of phi).
# For each solid: its faces split into orbits of the 60 rotations ("kinds"), each kind's shape (exact: sides and diagonals), and the
# pattern: faces of one kind joined edge to edge form groups; for each kind the group sizes, and the axis each group is centred on
# (the order of the rotations that map the group to itself: 5, 3, 2, or 1 = none). Writes surface-patterns.json (with float corners and
# ordered faces for the figure).   usage: python3 surface_patterns.py <studies/2026-10-19-five-fold-octet>
import sys, os, json
from collections import Counter
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
Z0 = Q5(0)
d2 = lambda a, b: dot(sub(a, b), sub(a, b))
par = lambda a, b, c, d: all(x == Z0 for x in cross(sub(b, a), sub(d, c)))
UP = [ID]
for _ in range(3): UP.append(step(UP[-1])[0])
DN = [OG]
for _ in range(4): DN.append(rev(DN[-1]))
ok(set(step(UP[3])[0]) == {tuple(Q5(35, -15) * x for x in v) for v in ID}, 'T(FPD) = (35 - 15 sqrt5) ID: the UP stations close (as in #38)')
SOL = [('ID', UP[0]), ('RT', UP[1]), ('GTI', UP[2]), ('FPD', UP[3]), ('OG', DN[0]), ('TPH', DN[1]), ('TQH', DN[2]), ('TQP', DN[3]), ('TQHD', DN[4])]
def shape(P):
    n = len(P); s = [d2(P[i], P[(i + 1) % n]) for i in range(n)]; eq = len({repr(x) for x in s})
    if n == 3: return 'equilateral triangle' if eq == 1 else 'isosceles triangle' if eq == 2 else 'scalene triangle'
    dg = [d2(P[i], P[(i + 2) % n]) for i in range(n)]
    if eq == 1 and len({repr(x) for x in dg}) == 1: return {4: 'square', 5: 'regular pentagon', 6: 'regular hexagon'}.get(n, f'regular {n}-gon')
    if n == 4:
        p02, p13 = par(P[0], P[1], P[3], P[2]), par(P[1], P[2], P[0], P[3])
        if p02 and p13: return 'rhombus' if eq == 1 else 'parallelogram'
        if p02 or p13:
            r = 0 if p02 else 1; return 'isosceles trapezoid' if s[r + 1] == s[(r + 3) % 4] else 'trapezoid'
        return 'kite' if (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]) else 'quadrilateral'
    return {5: 'pentagon', 6: 'hexagon'}.get(n, f'{n}-gon') + (' with equal sides' if eq == 1 else '')
def order(M):
    I3 = tuple(tuple(Q5(1 if i == j else 0) for j in range(3)) for i in range(3)); A = M; k = 1
    while A != I3: A = tuple(tuple(sum((A[i][t] * M[t][j] for t in range(3)), Z0) for j in range(3)) for i in range(3)); k += 1
    return k
ORD = [order(M) for M in G]
res = {'mark': 'DICTO Kyushindo cores, surface patterns, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}}
for nm, S in SOL:
    C, Fc = polytope(solid(S)); faces = [tuple(C[j] for j in o) for o, _ in Fc]; key = {frozenset(f): i for i, f in enumerate(faces)}
    orb = [-1] * len(faces); kinds = []
    for i, f in enumerate(faces):
        if orb[i] >= 0: continue
        imgs = {key[frozenset(app(M, v) for v in f)] for M in G}
        for j in imgs: orb[j] = len(kinds)
        kinds.append({'sides': len(f), 'count': len(imgs), 'shape': shape(list(f))})
    edges = {}
    for i, f in enumerate(faces):
        for a, b in zip(f, f[1:] + f[:1]): edges.setdefault(frozenset((a, b)), []).append(i)
    ok(all(len(v) == 2 for v in edges.values()) and len(C) - len(edges) + len(faces) == 2, f'{nm}: {len(C)} corners, {len(faces)} faces, {len(edges)} edges, closed (Euler)')
    for kd_i, kd in enumerate(kinds):
        mem = [i for i in range(len(faces)) if orb[i] == kd_i]; seen = set(); groups = []
        for i0 in mem:
            if i0 in seen: continue
            st, g = [i0], set()
            while st:
                i = st.pop()
                if i in g: continue
                g.add(i); st += [x for v in edges.values() if i in v for x in v if orb[x] == kd_i]
            seen |= g; groups.append(g)
        g0 = groups[0]; fs = {frozenset(faces[i]) for i in g0}
        stab = [o for M, o in zip(G, ORD) if {frozenset(app(M, v) for v in faces[i]) for i in g0} == fs]
        kd['groups'] = len(groups); kd['group_size'] = sorted({len(g) for g in groups}); kd['group_axis'] = max(stab)   # 1 = on no axis
        kd['same_kind_edges'] = sum(1 for v in edges.values() if orb[v[0]] == orb[v[1]] == kd_i)
    nb = Counter()                                   # edges between kinds: which kinds of face meet along how many edges
    for v in edges.values(): nb[tuple(sorted((orb[v[0]], orb[v[1]])))] += 1
    res_nb = {f'{a}-{b}': n for (a, b), n in sorted(nb.items())}
    res['solids'][nm] = {'kind_edges': res_nb, 'corners': len(C), 'faces': len(faces), 'kinds': kinds,
                         'corners_float': [[x.f() for x in v] for v in C], 'faces_idx': [list(o) for o, _ in Fc], 'face_kind': orb}
    ax = {5: 'on a five-fold axis', 3: 'on a three-fold axis', 2: 'on a two-fold axis', 1: 'on no axis'}
    pl = lambda k: k['shape'].replace('rhombus', 'rhombi') if k['shape'] == 'rhombus' else k['shape'] + 's'
    def say(k):
        if k['groups'] == 1 and k['count'] > 1: return f"{k['count']} {pl(k)} (all joined edge to edge)"
        if k['group_size'] == [1]: return f"{k['count']} {pl(k)} (apart, each {ax[k['group_axis']]})"
        return f"{k['count']} {pl(k)} ({k['groups']} groups of {k['group_size'][0]} joined edge to edge, each {ax[k['group_axis']]})"
    ok(True, f'{nm}: ' + '; '.join(say(k) for k in kinds))
    ok(True, f'{nm}: edges between kinds (kind numbers in the order above, from 0): ' + ', '.join(f'{k}: {n}' for k, n in res_nb.items()))
json.dump(res, open(os.path.join(HERE, 'surface-patterns.json'), 'w'))
