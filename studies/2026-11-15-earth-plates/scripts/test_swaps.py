"""Tests of swaps.py on hand-built sequences with known answers (bipyramid flip of the event-logger tests)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-11-15-event-logger', 'scripts'))
from eventlog import Tiling, from_triangles, run
from swaps import swap_list, persistent
OK = []
def expect(name, cond, info=''):
    OK.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (f'  [{info}]' if info else ''))
N, S, a, b, c = 'N', 'S', 'a', 'b', 'c'
bip = [(N, a, b), (N, b, c), (N, c, a), (S, a, b), (S, b, c), (S, c, a)]
flip = [(N, S, a), (N, S, b), (N, b, c), (N, c, a), (S, b, c), (S, c, a)]
def seq(pattern):
    return [from_triangles(bip if x == 0 else flip, t) for t, x in zip(range(len(pattern), 0, -1), pattern)]
def count(F, k):
    rows, summ = run(F, by_segment=True); return persistent(F, swap_list(F, rows), k)
F = seq([0, 1, 0, 0, 0])
expect('flip and flip back: 2 swaps at k=1', count(F, 1) == (2, 0), count(F, 1))
expect('flip and flip back within 1 Myr: both drop at k=2', count(F, 2)[0] == 0, count(F, 2))
F = seq([0, 0, 0, 1, 1, 1, 0, 0, 0])
expect('contacts lasting 3 Myr: 2 swaps at k=2 and k=3', count(F, 2)[0] == 2 and count(F, 3)[0] == 2, (count(F, 2), count(F, 3)))
expect('contacts lasting 3 Myr: none at k=5 (both swaps touch the 3 Myr run)', count(F, 5)[0] == 0, count(F, 5))
F = seq([0, 0, 1, 1, 1])
expect('one swap with censored ends passes at k=5 and is marked censored', count(F, 5) == (1, 1), count(F, 5))
# swap through a four-fold meeting: edge a-b shrinks to a point (junction N, S, a, b) for two frames, then N-S grows
mid = Tiling([N, S, a, b, c], [(N, a), (N, b), (N, c), (S, a), (S, b), (S, c), (b, c), (c, a)],
             [(N, b, c), (N, c, a), (S, b, c), (S, c, a), (N, S, a, b)], t=0)
F = [from_triangles(bip, 5), Tiling(mid.cells, mid.segments, mid.junctions, t=4), Tiling(mid.cells, mid.segments, mid.junctions, t=3), from_triangles(flip, 2), from_triangles(flip, 1)]
rows, summ = run(F, by_segment=True)
expect('four-fold frames pass Euler', summ['ok'], summ['n_frames_failing'])
expect('logger alone: one-contact-lost and one-contact-gained clumps', sorted(r['pattern'] for r in rows) == ['born 0 died 0 lost 0 gained 1', 'born 0 died 0 lost 1 gained 0'])
sw = swap_list(F, rows)
expect('joined into one swap through the four-fold meeting', len(sw) == 1 and sw[0]['via'] == 'four-fold' and sw[0]['lost'] == (a, b) and sw[0]['gained'] == (N, S), sw)
G = [F[0], F[1], from_triangles(bip, 3), F[3], F[4]]                 # the four-fold meeting is broken in between: no join
rows2, _ = run(G, by_segment=True)
expect('NEG: no join when the four cells do not meet in every frame between', all(s['via'] == 'direct' for s in swap_list(G, rows2)), swap_list(G, rows2))
# length filter: the flip's new contact N-S grows to 30 then 80 km; the old contact a-b was 100 km long
F = seq([0, 0, 0, 1, 1, 1, 1])
rows, _ = run(F, by_segment=True); sw = swap_list(F, rows)
Ls = [{('a', 'b'): [100.0]}] * 3 + [{('N', 'S'): [x]} for x in (10.0, 30.0, 80.0, 80.0)]
expect('length filter 50 km: passes (new contact reaches 80 km)', persistent(F, sw, 1, 50, Ls)[0] == 1)
expect('length filter 150 km: fails (new contact never reaches 150 km)', persistent(F, sw, 1, 150, Ls)[0] == 0)
Ls2 = [{('a', 'b'): [20.0]}] * 3 + Ls[3:]
expect('length filter 50 km: fails when the old contact was never 50 km long', persistent(F, sw, 1, 50, Ls2)[0] == 0)
print(f'{sum(OK)}/{len(OK)} tests passed'); sys.exit(0 if all(OK) else 1)
