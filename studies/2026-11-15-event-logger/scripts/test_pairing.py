"""Tests of pairing.py (rules T, P, W) on hand-built sphere maps whose swaps are known, with negative cases."""
from eventlog import Tiling, from_triangles, check_tiling
from pairing import pair_census, apply_tolerance

OK = []
def expect(name, cond, info=''):
    OK.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (f'  [{info}]' if info else ''))

# triangular bipyramid: edge a-b flips to N-S; M = the four-fold meeting in between (a-b lost, N-S not yet gained)
N, S, a, b, c = 'N', 'S', 'a', 'b', 'c'
bip = [(N, a, b), (N, b, c), (N, c, a), (S, a, b), (S, b, c), (S, c, a)]
flip = [(N, S, a), (N, S, b), (N, b, c), (N, c, a), (S, b, c), (S, c, a)]
def B0(t): return from_triangles(bip, t)
def B1(t): return from_triangles(flip, t)
def M(t):
    T = B0(t)
    J = [j for j in T.junctions if not (a in j and b in j)] + [(N, S, a, b)]
    return Tiling(T.cells, [s for s in T.segments if s != (a, b)], J, 2, 'sphere', t)
expect('four-fold frame passes Euler, triple formulas do not apply', check_tiling(M(0))['ok'] and check_tiling(M(0))['triple_formulas_ok'] is None)

def seq(kinds, dt=1.0): return [k(i * dt) for i, k in enumerate(kinds)]

# 1. flicker of whole swaps collapses to zero
fl = seq([B0, B1] * 6 + [B0] * 6)
ev, s = pair_census(fl, W=3, P=3)
expect('swap flicker: raw swaps 12, counted 0', s['raw_counts'].get('swap') == 12 and s['swaps'] == 0, (s['raw_counts'], s['swaps']))
# 2. flicker of halves (contact lost and regained) collapses to zero
fh = seq([B0, M] * 6 + [B0] * 6)
ev, s = pair_census(fh, W=3, P=3)
expect('half flicker: 12 halves, counted 0 swaps, 0 halves left', s['raw_one_lost'] + s['raw_one_gained'] == 12 and s['swaps'] == 0
       and s['halves_left_lost'] == s['halves_left_gained'] == 0, s)
# 3. mixed flicker (a-b lost, N-S gained for one frame, N-S lost, a-b regained) collapses to zero
fm = seq([B0, M, B1, M] * 4 + [B0] * 6)
ev, s = pair_census(fm, W=3, P=4)   # a-b is off for 3 frames each time: P must exceed that
expect('mixed flicker: counted 0', s['swaps'] == 0 and s['halves_left_lost'] == s['halves_left_gained'] == 0, s)
# 4. a swap split into halves 3 frames apart: paired at W >= 3, not at W = 2
sp = seq([B0, B0, M, M, M, B1, B1, B1, B1])
for W, want in ((2, 0), (3, 1), (5, 1)):
    ev, s = pair_census(sp, W=W, P=1)
    expect(f'split swap (gap 3 frames), W = {W}: {want} swap', s['swaps'] == want and s['swaps_paired'] == want
           and s['halves_left_lost'] == 1 - want and s['halves_left_gained'] == 1 - want, s)
# 4b. the window is physical time, not frames: same sequence at dt = 0.5, gap 1.5
sp5 = seq([B0, B0, M, M, M, B1, B1, B1, B1], dt=0.5)
expect('physical window: W = 1.5 pairs, W = 1.0 does not',
       pair_census(sp5, W=1.5, P=0.5)[1]['swaps'] == 1 and pair_census(sp5, W=1.0, P=0.5)[1]['swaps'] == 0)
# 4c. gain before loss (all four cells touch for a while) is paired too
def Q(t):    # a-b still touch and N-S already touch: a four-cell meeting read as junctions N S a / N S b plus a-b
    return Tiling([N, S, a, b, c], [(a, b), (N, S), (N, a), (N, b), (S, a), (S, b), (N, c), (S, c), (a, c), (b, c)], None, 2, 'sphere', t)
gb = seq([B0, B0, Q, Q, B1, B1, B1, B1])
ev, s = pair_census(gb, W=3, P=1)
expect('gain 2 frames before loss: paired at W = 3', s['swaps'] == 1 and s['swaps_paired'] == 1, s)
# 5. a clean swap and its reverse after more than P both count; within P both cancel
rv = seq([B0] * 3 + [B1] * 5 + [B0] * 5)
expect('swap and reverse 5 apart: P = 3 counts 2, P = 6 counts 0',
       pair_census(rv, W=3, P=3)[1]['swaps'] == 2 and pair_census(rv, W=3, P=6)[1]['swaps'] == 0)
# 6. P = 0 and W = 0 give the logger's own swap count on a clean sequence
expect('P = W = 0: swaps = logger swaps', pair_census(rv, W=0, P=0)[1]['swaps'] == 2 and pair_census(fl, W=0, P=0)[1]['swaps'] == 12)
# 7. NEGATIVE: a loss and a gain that are not the 2-2 pattern are not paired (octahedron map)
x, X, y, Y, z, Z = 'x', 'X', 'y', 'Y', 'z', 'Z'
octa = [(p, q, r) for p in (x, X) for q in (y, Y) for r in (z, Z)]
def oct_without(*pairs, t=0):
    T = from_triangles(octa, t); J = list(T.junctions); segs = list(T.segments)
    for u, v in pairs:
        ends = [j for j in J if u in j and v in j]
        J = [j for j in J if j not in ends] + [tuple(sorted(set(ends[0]) | set(ends[1])))]
        segs.remove(tuple(sorted((u, v))))
    return Tiling(T.cells, segs, J, 2, 'sphere', t)
o = [oct_without((X, Y), t=0), oct_without((X, Y), (x, y), t=1)] + [oct_without((x, y), t=t) for t in range(2, 7)]
expect('octahedron frames pass Euler', all(check_tiling(T)['ok'] for T in o))
ev, s = pair_census(o, W=10, P=1)
expect('NEGATIVE: loss x-y and gain X-Y (not 2-2) stay unpaired', s['swaps'] == 0 and s['halves_left_lost'] == 1
       and s['halves_left_gained'] == 1, s)
# 8. rule T: a short boundary is removed and its two junctions merge into one four-fold junction (Euler kept)
T0 = B0(0); T0t, dropped = apply_tolerance(T0, {(a, b): [0.2]}, 0.5)
expect('tolerance: short a-b removed, four-fold junction, Euler 2', (a, b) not in T0t.pairs and not dropped
       and check_tiling(T0t)['euler'] == 2 and (N, S, a, b) in T0t.junctions)
# 8b. a swap seen through shrinking and growing boundaries: one direct swap without T; with T it passes through four-fold
#     frames and is paired back into one swap
frames = [B0(0), B0(1), B0(2), B1(3), B1(4), B1(5), B1(6)]
lens = [{(a, b): [1.0]}, {(a, b): [0.3]}, {(a, b): [0.2]}, {(N, S): [0.2]}, {(N, S): [0.3]}, {(N, S): [1.0]}, {(N, S): [1.0]}]
s0 = pair_census(frames, W=3, P=1, lengths=lens)[1]; s1 = pair_census(frames, W=3, P=1, tol=0.5, lengths=lens)[1]
expect('tolerance: 1 swap without T (direct), 1 with T (paired, gap 4 > W = 3 -> unpaired)', s0['swaps'] == 1 and s0['swaps_direct'] == 1
       and s1['swaps'] == 0 and s1['halves_left_lost'] == 1, (s0['swaps'], s1))
s2 = pair_census(frames, W=4, P=1, tol=0.5, lengths=lens)[1]
expect('tolerance with W = 4: paired into 1 swap', s2['swaps'] == 1 and s2['swaps_paired'] == 1, s2)
# 9. parameters are logged
expect('parameters logged', s2['params']['W'] == 4 and s2['params']['P'] == 1 and s2['params']['tol'] == 0.5)
# 10. integer labels (as from_triangles on numbered cells) work the same as string labels
ib = [tuple(sorted(ord(v) for v in t)) for t in bip]; ifl = [tuple(sorted(ord(v) for v in t)) for t in flip]
iseq = [from_triangles(ib if k == 0 else ifl, i) for i, k in enumerate([0, 0, 1, 1, 1, 0, 0, 0])]
expect('integer labels: swap and reverse 3 apart, P = 2 counts 2, P = 4 counts 0',
       pair_census(iseq, W=0, P=2)[1]['swaps'] == 2 and pair_census(iseq, W=0, P=4)[1]['swaps'] == 0)
print(f'{sum(OK)}/{len(OK)} pass')
raise SystemExit(0 if all(OK) else 1)
