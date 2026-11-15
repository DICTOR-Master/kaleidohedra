"""Tests of rm_count.py (Rutenberg-McCurdy macroscopic count, rules SS and RM) on hand-built sphere maps with known answers.
Map as in test_macro.py: octahedron (cells x X y Y z Z) with a three-sided cell w inside the corner x-y-z.
Sequence S1 (frame index = time, 31 frames):
  A  t = 2   flip X-Y -> z-Z;  B  t = 10  flip x-y -> w-Z (w GAINS a side);  C  t = 21  flip w-Z -> x-y (w SHEDS it);
  D  t = 22  w vanishes;      Ar t = 23  flip z-Z -> X-Y.
  Known: swaps 4; side-shedding (SS) = C only; macroscopic (SS) 3. B has w in its GAINED pair: not side-shedding (negative).
Sequence S2 (regain): w-Z gained at 4, lost at 8, gained again at 12, lost at 21; w vanishes at 22; A and Ar as in S1.
  Known: swaps 6; the loss at 8 is followed by a regain, so SS = 1 (the loss at 21); SS_any = 2; macroscopic 5.
Areas (rule RM): every cell 100, w 50 for t <= 15 and 1 for t >= 16; box 700, 7 cells -> <A> = 100, l^2 = rc * 10.
  rc = 1: l^2 = 10: C (w = 1) microscopic, B (w = 50) macroscopic: macroscopic 3; w passes l^2 at t = 16 with 4 sides.
  rc = 10: l^2 = 100: w is always below: B and C microscopic: macroscopic 2."""
from eventlog import from_triangles, check_tiling
import pairing as PR
from rm_count import rm_count, side_shedding

OK = []
def expect(name, cond, info=''):
    OK.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (f'  [{info}]' if info else ''))

x, X, y, Y, z, Z, w = 'x', 'X', 'y', 'Y', 'z', 'Z', 'w'

def tris(xy=True, XY=True, alive=True):
    faces = [(p, q, r) for p in (x, X) for q in (y, Y) for r in (z, Z)]
    if not XY:
        faces = [f for f in faces if f not in ((X, Y, z), (X, Y, Z))] + [(X, z, Z), (Y, z, Z)]
    faces.remove((x, y, z))
    wf = [(w, x, y), (w, y, z), (w, x, z)]
    if not alive:
        return faces + [(x, y, z)]
    if not xy:
        faces.remove((x, y, Z)); wf.remove((w, x, y)); wf += [(w, x, Z), (w, y, Z)]
    return faces + wf

def s1(t): return from_triangles(tris(not (10 <= t < 21), not (2 <= t < 23), t < 22), float(t))
def s2(t): return from_triangles(tris(not (4 <= t < 8 or 12 <= t < 21), not (2 <= t < 23), t < 22), float(t))

S1 = [s1(t) for t in range(31)]; S2 = [s2(t) for t in range(31)]
expect('all frames pass Euler', all(check_tiling(F)['ok'] for F in S1 + S2))

r1 = rm_count(S1, PR.collect(S1), W=0, P=1)
expect('S1: swaps 4, side-shedding 1, macroscopic 3', r1['swaps'] == 4 and r1['SS']['side_shedding'] == 1 and r1['SS']['macroscopic'] == 3, r1['SS'])
expect('S1: one vanished cell; total per vanished 4, macroscopic per vanished 3',
       r1['vanished'] == 1 and r1['per_vanished']['total'] == 4 and r1['per_vanished']['SS_macroscopic'] == 3, r1['per_vanished'])
sw, _ = PR.apply_rules(PR.collect(S1), 0, 1, keep_events=True)
fl, delays, _ = side_shedding(sw, S1)
byt = {s['t']: f[0] for s, f in zip(sw, fl)}
expect('S1: the flagged swap is C (t = 21), shed-to-vanish delay 1', byt == {2.0: False, 10.0: False, 21.0: True, 23.0: False} and delays == [1.0], (byt, delays))
expect('NEGATIVE S1: B (w in the gained pair, w vanishes later) is not side-shedding', byt[10.0] is False)

r2 = rm_count(S2, PR.collect(S2), W=0, P=1)
expect('S2 (regain): swaps 6, side-shedding 1, SS_any 2, macroscopic 5',
       r2['swaps'] == 6 and r2['SS']['side_shedding'] == 1 and r2['SS']['side_shedding_any'] == 2 and r2['SS']['macroscopic'] == 5, r2['SS'])

co = S1[::2]
rc = rm_count(co, PR.collect(co), W=0, P=2)
expect('step 2: C absorbed into the vanishing; swaps 3, side-shedding 0, macroscopic 3 (unchanged)',
       rc['swaps'] == 3 and rc['SS']['side_shedding'] == 0 and rc['SS']['macroscopic'] == 3, rc['SS'])

areas = [{c: (100.0 if c != w else (50.0 if F.t <= 15 else 1.0)) for c in F.cells} for F in S1]
for F, a in zip(S1, areas):
    if w not in F.cells: a.clear(); a.update({c: 700.0 / 6 for c in F.cells})
ra = rm_count(S1, PR.collect(S1), W=0, P=1, areas=areas, box=700.0, rcs=(1.0, 10.0))
a1, a10 = ra['RM']['1.0'], ra['RM']['10.0']
expect('RM rc = 1 (l^2 = 10): microscopic 1 (C), macroscopic 3', a1['microscopic'] == 1 and a1['macroscopic'] == 3 and a1['microscopic_and_SS'] == 1, a1)
expect('RM rc = 1: w shrinks past l^2 with 4 sides', a1['sides_at_ell2'] == {4: 1}, a1['sides_at_ell2'])
expect('RM rc = 10 (l^2 = 100): microscopic 2 (B and C), macroscopic 2', a10['microscopic'] == 2 and a10['macroscopic'] == 2, a10)

nv = [from_triangles(tris(True, not (5 <= t < 12), True), float(t)) for t in range(20)]
rn = rm_count(nv, PR.collect(nv), W=0, P=1)
expect('NEGATIVE: no vanishing -> no side-shedding; every swap macroscopic (2 of 2)',
       rn['swaps'] == 2 and rn['SS']['side_shedding'] == 0 and rn['SS']['macroscopic'] == 2 and rn['vanished'] == 0, rn['SS'])
expect('parameters logged', r1['params']['W'] == 0 and r1['params']['P'] == 1)
print(f'{sum(OK)}/{len(OK)} pass')
raise SystemExit(0 if all(OK) else 1)
