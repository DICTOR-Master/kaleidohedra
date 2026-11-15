"""Tests of macro.py (free / attached swaps) on a hand-built sphere map whose swaps and cell events are known, with negative cases.
Map: octahedron (cells x X y Y z Z) with a three-sided cell w inside the corner x-y-z. Events (frame index = time):
  A  t = 2   flip X-Y -> z-Z      (cells X Y z Z; w not involved)
  B  t = 10  flip x-y -> w-Z      (w gains a side; far from w's vanishing)
  C  t = 21  flip w-Z -> x-y      (w sheds the side again, 1 before it vanishes)
  Ar t = 23  flip z-Z -> X-Y      (reverse of A; z is a neighbour of w, but none of X Y z Z vanishes)
  D  t = 22  w vanishes (death)
Known answer, tau = 3: free = A, B, Ar (3); attached = C (1, to the death of w; one side shed). Ring variant: Ar is attached too
(z is w's neighbour), free 2. tau = 15: B is attached too (primary free 2)."""
from eventlog import from_triangles, check_tiling
from macro import macro_census, cell_events

OK = []
def expect(name, cond, info=''):
    OK.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (f'  [{info}]' if info else ''))

x, X, y, Y, z, Z, w = 'x', 'X', 'y', 'Y', 'z', 'Z', 'w'

def tris(xy=True, XY=True, alive=True):
    """xy: edge x-y present (else w-Z, needs alive); XY: edge X-Y present (else z-Z)."""
    T = []
    # faces round X (X with y/Y and z/Z), edge X-Y vs z-Z inside quad X? no: quad X-Y with z, Z on the X side
    # octahedron faces (p, q, r), p in {x, X}, q in {y, Y}, r in {z, Z}
    faces = [(p, q, r) for p in (x, X) for q in (y, Y) for r in (z, Z)]
    # flip region 1: faces (X, Y, z), (X, Y, Z) share X-Y? they share edge X-Y. Flip -> (X, z, Z), (Y, z, Z)
    if not XY:
        faces = [f for f in faces if f not in ((X, Y, z), (X, Y, Z))] + [(X, z, Z), (Y, z, Z)]
    # w inside face (x, y, z)
    faces.remove((x, y, z))
    wf = [(w, x, y), (w, y, z), (w, x, z)]
    if not alive:
        return faces + [(x, y, z)]
    if not xy:   # faces (w, x, y) and (x, y, Z) share x-y; flip -> (w, x, Z), (w, y, Z)
        faces.remove((x, y, Z)); wf.remove((w, x, y)); wf += [(w, x, Z), (w, y, Z)]
    return faces + wf

def frame(t, n_end=30):
    xy = not (10 <= t < 21); XY = not (2 <= t < 23); alive = t < 22
    return from_triangles(tris(xy, XY, alive), float(t))

seq = [frame(t) for t in range(31)]
expect('all frames pass Euler', all(check_tiling(F)['ok'] for F in seq))
_, ev = cell_events(seq)
expect('one cell event: death of w at t = 22', len(ev) == 1 and ev[0]['type'] == 'death' and ev[0]['died'] == [w] and ev[0]['t'] == 22,
       [(e['type'], e['died'], e['t']) for e in ev])

r = macro_census(seq, W=0, P=1, taus=[3, 15])
p3, p15 = r[3], r[15]
expect('swaps 4 (A, B, C, Ar)', p3['swaps'] == 4, p3['swaps'])
expect('tau = 3: free 3, attached 1', p3['primary']['free'] == 3 and p3['primary']['attached'] == 1, p3['primary'])
d = p3['primary']['per_type'].get('death', {})
expect('tau = 3: the attached swap belongs to the death, one side shed before vanishing',
       d.get('events') == 1 and d.get('attached_swaps') == 1 and d.get('sides_shed_before_vanishing') == 1, d)
expect('tau = 3 ring variant: free 2 (Ar attached through neighbour z)', p3['ring']['free'] == 2 and p3['ring']['attached'] == 2, p3['ring'])
expect('tau = 15: free 2 (B attached too)', p15['primary']['free'] == 2 and p15['primary']['attached'] == 2, p15['primary'])
expect('identity free + attached = swaps', all(v[k]['identity_ok'] for v in r.values() for k in ('primary', 'ring')))

# coarse step: frames at even times; C (t = 21) and D (t = 22) fall in one interval and are logged as one event (no swap).
# The free count must not change, because C was attached.
co = seq[::2]
rc = macro_census(co, W=0, P=2, taus=[3])[3]
expect('step 2: swap C absorbed (swaps 3)', rc['swaps'] == 3, rc['swaps'])
expect('step 2: free count unchanged (3), attached 0', rc['primary']['free'] == 3 and rc['primary']['attached'] == 0, rc['primary'])
_, evc = cell_events(co)
expect('step 2: the absorbed swap and the vanishing are one event with w', len(evc) == 1 and evc[0]['died'] == [w],
       [(e['type'], e['died']) for e in evc])

# NEGATIVE: with no cell event every swap is free, at any tau
nv = [from_triangles(tris(True, not (5 <= t < 12), True), float(t)) for t in range(20)]
rn = macro_census(nv, W=0, P=1, taus=[0, 100])
expect('NEGATIVE: no cell event -> all swaps free (2 of 2) at tau 0 and 100',
       all(v['swaps'] == 2 and v['primary']['free'] == 2 and v['primary']['attached'] == 0 for v in rn.values()), rn)
# NEGATIVE: tau = 0 attaches only swaps in the very interval of the event
r0 = macro_census(seq, W=0, P=1, taus=[0])[0]
expect('NEGATIVE: tau = 0 attaches nothing here (C is 1 before D)', r0['primary']['free'] == 4, r0['primary'])
# lineage: w is absorbed by z (heir share 1.0) -> a merge whose participants are w and z; Ar (cells X Y z Z, 1 after) is attached
lin = [F if F.t != 21 else from_triangles(tris(True, False, True), 21.0, heirs={w: {z: 1.0}}) for F in seq]
_, evl = cell_events(lin)
rl = macro_census(lin, W=0, P=1, taus=[3])[3]
expect('lineage merge: participants {w, z}; free 2 (A, B), attached 2 (C, Ar) to the merge',
       evl[0]['type'] == 'merge' and evl[0]['cells'] == {w, z} and rl['primary']['free'] == 2
       and rl['primary']['per_type']['merge']['attached_swaps'] == 2, (evl, rl['primary']))
expect('parameters logged', p3['params']['tau'] == 3 and p3['params']['W'] == 0 and p3['params']['P'] == 1)
print(f'{sum(OK)}/{len(OK)} pass')
raise SystemExit(0 if all(OK) else 1)
