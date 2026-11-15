"""Tests of eventlog.py with hand-built tilings whose events are known, plus negative controls (each must be caught)."""
import itertools, sys
from eventlog import Tiling, from_triangles, from_tets, classify, check_tiling, run, rebalance_log, balance

OK = []
def expect(name, cond, info=''):
    OK.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (f'  [{info}]' if info else ''))

def types(A, B): return sorted(e['type'] for e in classify(A, B))

tet = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
T0 = from_triangles(tet, 0)
r = check_tiling(T0); expect('tetrahedron map: Euler and triple formulas', r['ok'] and r['euler'] == 2 and r['triple_formulas_ok'])
# birth at junction (0,1,2) and its reverse
T1 = from_triangles([(0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 4), (0, 2, 4), (1, 2, 4)], 1)
expect('1-3 birth', types(T0, T1) == ['birth'], types(T0, T1)); expect('3-1 death', types(T1, T0) == ['death'], types(T1, T0))
# same newcomer with lineage from one parent = split; from three parents = birth
T1s = from_triangles(T1.junctions, 1, parents={4: {0: 1.0}})
expect('newcomer with one parent = split', types(T0, T1s) == ['split'], types(T0, T1s))
T1b = from_triangles(T1.junctions, 1, parents={4: {0: .4, 1: .3, 2: .3}})
expect('newcomer from three parents = birth', types(T0, T1b) == ['birth'], types(T0, T1b))
T0m = from_triangles(tet, 2); T1h = from_triangles(T1.junctions, 1, heirs={4: {0: 1.0}})
expect('vanishing cell with one heir = merge', types(T1h, T0m) == ['merge'], types(T1h, T0m))
# swap on the triangular bipyramid: edge a-b flips to N-S
N, S, a, b, c = 'N', 'S', 'a', 'b', 'c'
bip = [(N, a, b), (N, b, c), (N, c, a), (S, a, b), (S, b, c), (S, c, a)]
flip = [(N, S, a), (N, S, b), (N, b, c), (N, c, a), (S, b, c), (S, c, a)]
B0, B1 = from_triangles(bip, 0), from_triangles(flip, 1)
expect('2-2 swap', types(B0, B1) == ['swap'] and check_tiling(B1)['ok'], types(B0, B1))
# split of the top face of the cube map by a cut from its E side to its W side (no lineage: combinatorial rule)
U, D, E_, W, F, K, X = 'U', 'D', 'E', 'W', 'F', 'K', 'X'
cube = [(U, E_, F), (U, F, W), (U, W, K), (U, K, E_), (D, E_, F), (D, F, W), (D, W, K), (D, K, E_)]
cut = [(U, E_, F), (U, F, W), (X, W, K), (X, K, E_), (U, X, E_), (U, X, W), (D, E_, F), (D, F, W), (D, W, K), (D, K, E_)]
C0, C1 = from_triangles(cube, 0), from_triangles(cut, 1)
expect('cut map passes Euler (10 - 15 + 7)', check_tiling(C1)['euler'] == 2 and len(C1.segments) == 15)
expect('split (cut across a cell)', types(C0, C1) == ['split'], types(C0, C1)); expect('merge (reverse)', types(C1, C0) == ['merge'], types(C1, C0))
# relabel
R1 = from_triangles([tuple('Z' if v == U else v for v in x) for x in cube], 1)
expect('relabel', types(C0, R1) == ['relabel'], types(C0, R1))
# clump: tetrahedron map straight to the cube map (two adjacent newcomers, one contact lost): one local event of pattern born 2 lost 1
oct_ = [(0, 2, 1), (0, 1, 3), (0, 3, 5), (0, 5, 2), (4, 2, 1), (4, 1, 3), (4, 3, 5), (4, 5, 2)]   # opposite pairs (0,4) (1,5) (2,3)
O1 = from_triangles(oct_, 1); ev = classify(T0, O1)
expect('clump (two newcomers at one place)', [e['type'] for e in ev] == ['clump'] and balance(T0, O1, ev)[0], [(e['type'], e['pattern']) for e in ev])
# two separate events in one step stay separate: birth in one place, swap elsewhere (octahedron map, far apart)
O = from_triangles(oct_, 0)
O2 = from_triangles([x for x in oct_ if x != (4, 3, 5)] + [(4, 3, 9), (4, 5, 9), (3, 5, 9)], 1)          # birth at junction (3,4,5)
o2 = [x for x in O2.junctions if set(x) not in ({0, 1, 2}, {0, 1, 3})] + [(0, 2, 3), (1, 2, 3)]        # flip edge 0-1 -> 2-3
O3 = from_triangles(o2, 1)
expect('birth and a distant swap stay two events', types(O, O3) == ['birth', 'swap'], types(O, O3))
# 3D: boundary of the 4-simplex; 1-4 birth; 2-3 flip = one contact gained; reverse = contact lost
S0 = from_tets(list(itertools.combinations(range(5), 4)), 0)
expect('S3 Euler on the 4-simplex boundary', check_tiling(S0)['ok'] and check_tiling(S0)['euler'] == 0)
q = [x for x in S0.corners if x != (0, 1, 2, 3)] + [tuple(sorted((5,) + f)) for f in itertools.combinations((0, 1, 2, 3), 3)]
S1 = from_tets(q, 1)
expect('3D birth (1-4)', types(S0, S1) == ['birth'] and check_tiling(S1)['ok'], types(S0, S1))
q2 = [x for x in q if x not in ((0, 1, 2, 5), (0, 1, 2, 4))] + [(0, 1, 4, 5), (1, 2, 4, 5), (0, 2, 4, 5)]
S2 = from_tets(q2, 2)
expect('3D contact gained (2-3 flip)', types(S1, S2) == ['contact gained'] and check_tiling(S2)['ok'], types(S1, S2))
expect('3D contact lost (3-2 flip)', types(S2, S1) == ['contact lost'], types(S2, S1))
expect('3D death (4-1)', types(S1, S0) == ['death'], types(S1, S0))
# whole-sequence run and the NEGATIVE CONTROLS
rows, summ = run([T0, T1, from_triangles(tet, 2)])
expect('run: balance and checks pass', summ['ok'] and summ['counts'] == {'birth': 1, 'death': 1}, summ['counts'])
bad = [dict(r) for r in rows]; bad[0]['type'] = 'swap'
expect('NEG: a birth relabelled as swap is caught by the balance check', len(rebalance_log([T0, T1, from_triangles(tet, 2)], bad)) == 1)
expect('NEG: a deleted event row is caught', len(rebalance_log([T0, T1, from_triangles(tet, 2)], rows[1:])) == 1)
broken = Tiling(T1.cells, T1.segments[:-1], T1.junctions, t=9)
expect('NEG: a frame with one boundary missing fails Euler', not check_tiling(broken)['ok'])
c4 = Tiling(['A', 'B', 'C', 'D', 'P'], [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')] + [('P', x) for x in 'ABCD'], [('A', 'B', 'P'), ('B', 'C', 'P'), ('C', 'D', 'P'), ('D', 'A', 'P'), ('A', 'B', 'C', 'D')])
r4 = check_tiling(c4)
expect('a four-fold junction: Euler holds, triple formulas do not apply', r4['euler_ok'] and r4['triple_formulas_ok'] is None, r4)
print(f'{sum(OK)}/{len(OK)} tests passed'); sys.exit(0 if all(OK) else 1)
