# DICTO 2026-10-21: "the ribbon pattern ... might denote a new shell structure". The ribbons of the OG turned out, EXACT in Q(sqrt5) with
# the #39 machinery: on each solid of the golden sequence (phi TPH, phi^2 TQH, phi^3 TQP, phi^4 TQHD) the four-sided faces are classified
# exactly (parallel sides by an exact zero cross product, equal sides by exact squared lengths); four-sided faces that share an edge are
# paired, and for each pair we test exactly whether a half-turn of the 60 rotations fixes the shared edge's midpoint and swaps the two faces
# (the pair centred on a two-fold axis). Floats (lengths, angles, the bend across the seam) are printed from the exact corners.
# usage: python3 golden_ribbons.py <studies/2026-10-19-five-fold-octet>
import sys, os, json, math
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_downward.py').read(); exec(src.split("log = {")[0].replace("os.path.dirname(os.path.abspath(__file__))", repr(os.getcwd())))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
Z0 = Q5(0)
def pw(k):
    r = Q5(1)
    for _ in range(k): r = r * PHI
    return r
D = [OG]
for k in range(1, 5): D.append(rev(D[-1]))
names = ['OG', 'phi TPH', 'phi^2 TQH', 'phi^3 TQP', 'phi^4 TQHD']
d2 = lambda a, b: dot(sub(a, b), sub(a, b))
par = lambda a, b, c, d: all(x == Z0 for x in cross(sub(b, a), sub(d, c)))
I3 = tuple(tuple(Q5(1 if i == j else 0) for j in range(3)) for i in range(3))
half = [M for M in G if M != I3 and all(sum((M[i][k] * M[k][j] for k in range(3)), Z0) == I3[i][j] for i in range(3) for j in range(3))]
mid = lambda a, b: tuple((x + y) / 2 for x, y in zip(a, b))
res = {'mark': 'DICTO OG turned out, golden step, ribbons, exact, 2026-10-21 · DICTO · dictospheres.com', 'solids': {}}
ok(len(half) == 15, f'the 60 rotations contain {len(half)} half-turns (the 15 two-fold axes)')
for k in range(1, 5):
    S = [tuple(pw(k) * x for x in v) for v in D[k]]; C, Fc = polytope(solid(S))
    quads = [[C[j] for j in o] for o, _ in Fc if len(o) == 4]; info = {'quads': len(quads)}
    kinds = {}
    for P in quads:
        s = [d2(P[i], P[(i + 1) % 4]) for i in range(4)]
        p02, p13 = par(P[0], P[1], P[3], P[2]), par(P[1], P[2], P[0], P[3])
        if p02 and p13: kd = 'rhombus' if len({repr(x) for x in s}) == 1 else 'parallelogram'
        elif p02 or p13:
            r = 0 if p02 else 1                        # sides r and r+2 are the parallel pair
            kd = 'isosceles trapezoid' if s[r + 1] == s[(r + 3) % 4] else 'trapezoid'
        else: kd = 'kite' if (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]) else 'other'
        kinds.setdefault(kd, []).append(P)
    info['kinds'] = {kd: len(v) for kd, v in kinds.items()}
    ok(True, f"{names[k]}: {len(quads)} four-sided faces: {info['kinds']}")
    tz = kinds.get('isosceles trapezoid', [])
    if tz:
        P = tz[0]; s = [d2(P[i], P[(i + 1) % 4]) for i in range(4)]; r = 0 if par(P[0], P[1], P[3], P[2]) else 1
        long_, short_ = sorted([s[r], s[r + 2]], key=lambda q: -q.f()); leg = s[r + 1]
        same = all(sorted([repr(x) for x in [d2(Q[i], Q[(i + 1) % 4]) for i in range(4)]]) == sorted(repr(x) for x in s) for Q in tz)
        a, b = (P[r], P[r + 1]) if s[r] == short_ else (P[r + 2], P[(r + 3) % 4])
        ang = lambda p, q, w: math.degrees(math.acos(dot(sub(q, p), sub(w, p)).f() / (d2(q, p).f() * d2(w, p).f()) ** .5))
        angs = sorted({round(ang(P[i], P[(i + 1) % 4], P[(i - 1) % 4]), 2) for i in range(4)})
        Lf, Sf, lf = long_.f() ** .5, short_.f() ** .5, leg.f() ** .5; h = (lf ** 2 - ((Lf - Sf) / 2) ** 2) ** .5
        info['trapezoid'] = {'parallel_sides2': [repr(long_), repr(short_)], 'leg2': repr(leg), 'parallel_sides': [round(Lf, 4), round(Sf, 4)], 'leg': round(lf, 4),
                             'angles_deg': angs, 'height': round(h, 4), 'all_congruent_sides': same}
        ok(same, f"{names[k]}: {len(tz)} isosceles trapezoids, all with the same sides: parallel sides^2 {long_!r} and {short_!r} ({Lf:.4f}, {Sf:.4f}), legs^2 {leg!r} ({lf:.4f}), angles {angs}, height {h:.4f}")
        # pairs: trapezoids sharing an edge, and which edge
        E = {}
        for i, Q in enumerate(tz):
            for j in range(4): E.setdefault(frozenset((Q[j], Q[(j + 1) % 4])), []).append(i)
        shared = {e: v for e, v in E.items() if len(v) == 2}
        which = lambda e: 'shorter parallel side' if d2(*tuple(e)) == short_ else 'longer parallel side' if d2(*tuple(e)) == long_ else 'leg'
        deg = [sum(i in v for v in shared.values()) for i in range(len(tz))]
        comp, seen = [], set()                         # connected groups of trapezoids joined edge to edge
        for i0 in range(len(tz)):
            if i0 in seen: continue
            st, g = [i0], set()
            while st:
                i = st.pop()
                if i in g: continue
                g.add(i); st += [x for v in shared.values() if i in v for x in v]
            seen |= g; comp.append(len(g))
        info['shared_edges'] = {w: sum(which(e) == w for e in shared) for w in ('shorter parallel side', 'longer parallel side', 'leg')}
        info['trapezoid_neighbours'] = sorted(set(deg)); info['groups'] = sorted(set(comp)); info['n_groups'] = len(comp)
        ok(True, f"{names[k]}: {len(shared)} edges shared by two trapezoids ({info['shared_edges']}); each trapezoid meets {info['trapezoid_neighbours']} others; {len(comp)} groups of {info['groups']} trapezoids")
        if set(deg) == {1}:
            ok(info['shared_edges']['shorter parallel side'] == len(shared) == len(tz) // 2, f"{names[k]}: the trapezoids pair up across their shorter parallel sides: {len(shared)} pairs (ribbons)")
            axis = []
            for e, (i, j) in shared.items():
                p, q = tuple(e); m = mid(p, q)
                axis.append(any(app(M, m) == m and {app(M, v) for v in tz[i]} == set(tz[j]) for M in half))
            ok(all(axis), f"{names[k]}: every pair is centred on a two-fold axis (a half-turn fixes the seam's midpoint and swaps the two trapezoids): {len(axis)} pairs on the 15 axes, two per axis")
            i, j = shared[next(iter(shared))]; A, B = tz[i], tz[j]
            nrm = lambda Q: (lambda n: [x.f() for x in n])(cross(sub(Q[1], Q[0]), sub(Q[2], Q[0])))
            na, nb = nrm(A), nrm(B); cosb = abs(sum(x * y for x, y in zip(na, nb))) / (sum(x * x for x in na) * sum(x * x for x in nb)) ** .5
            info['bend_across_seam_deg'] = round(math.degrees(math.acos(min(1, cosb))), 3)
            ok(True, f"{names[k]}: the two trapezoids of a pair meet at {info['bend_across_seam_deg']} deg off flat across the seam (float); the seam and the two outer parallel sides are parallel (exact: each is a parallel side of a trapezoid that has the seam as its other one)")
        info['pairs'] = len(shared)
    res['solids'][names[k]] = info
json.dump(res, open(os.path.join(HERE, 'golden-ribbons.json'), 'w'), indent=1)
