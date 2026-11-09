"""02: DICTO's Escher stepped hexagon, named versions, with every 'matching bottom'; screw-consistency facts.

Tops (heights in units H/12; ccw = climbing direction; plate s spans rim corners D_s -> D_{s+1}):
  E1  helical ramp: six plates climbing 2 each (rise per turn 12 = one layer), ONE riser of 12 at D_0,
      centre of each plate at the mean of its rim ends (plates tilted round the axis only).
  E3  three flights (C3): plates climb 2 each, riser of 4 at every D_even; rise per turn 12.
  E3p E3 with an RD-like peak (all plate centres at 9).
  E6  six risers (C6): every plate climbs 2, riser 2 at every corner; rise per turn 12.
  RDE RD cap with the descending plates turned to climb (C3): even (9,3,6), odd (9,6,9); rise per turn 18,
      riser 6 at every D_even.
  RDE2 RD cap, odd plates (9,0,3): riser 6 at every D_odd; rise per turn 18.
Bottoms: every reassembly of the tops of 3 upright lower cells (lean below 1/2, turns k*60 deg) and the C2 turned top.
Battery: patch SAT (4 layers, R=2, every lean word), then periodic tilings with in-plane period lattice of index <= 3
(any vertical period, any skew) via the finite layer graph.  Proper motions; then with mirror copies.
"""
import sys, time, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from escher import *

t0 = time.time()
NAMED = {
    'E1': top_from([(2 * s + 2, 2 * s + 1, 2 * s + 3) for s in range(6)]),
    'E3': c3_top(2, 1, 3, 4, 3, 5),
    'E3p': c3_top(9, 1, 3, 9, 3, 5),
    'E6': top_from([(6, 5, 7)] * 6),
    'RDE': c3_top(9, 3, 6, 9, 6, 9),
    'RDE2': c3_top(9, 3, 6, 9, 0, 3),
}
ok = True
summary = {}


def around(top_rel_by_cell, V):
    """values at V of the 6 triangles around V (ccw) in a layer whose cell at X has relief top_rel_by_cell(X)."""
    seq = []
    for k in range(6):
        T = [V, add(V, D[k]), add(V, D[(k + 1) % 6])]
        X = [p for p in T if coset(p) == 0][0]
        top = top_rel_by_cell(X)
        seq.append(dict(top[sec([sub(p, X) for p in T])])[sub(V, X)])
    return seq


def monotone_one_drop(seq):
    jumps = [seq[(k + 1) % 6] - seq[k] for k in range(6)]
    ups = [j for j in jumps if j > 0]
    downs = [j for j in jumps if j < 0]
    return len(ups) == 5 and len(downs) == 1


for name, top in NAMED.items():
    rim, cen = risers(top)
    print(f'== {name}: rise per turn (rim) {rim_climb(top)}, rim risers {rim} (sum {sum(rim)}), centre jumps {cen}')
    ok &= rim_climb(top) + sum(rim) == 0        # single-valuedness: climb is always paid back by risers
    # uniform layer (all cells translates): what the interface does round the corners (Y=coset 1, Z=coset 2)
    for V, lab in (((1, 0), 'corner coset 1'), ((0, 1), 'corner coset 2')):
        seq = around(lambda X: top, V)
        print(f'   uniform layer, values round a {lab}: {seq}  monotone staircase: {monotone_one_drop(seq)}')
    # shared staircase round a corner: which turn patterns of the 3 cells give a monotone climb round it
    for V, lab in (((1, 0), 'coset 1'), ((0, 1), 'coset 2')):
        cells = sorted({[p for p in [V, add(V, D[k]), add(V, D[(k + 1) % 6])] if coset(p) == 0][0] for k in range(6)})
        hits = []
        for rots in itertools.product(range(6), repeat=3):
            tops = {X: map_relief(top, planar(r, 0)) for X, r in zip(cells, rots)}
            if monotone_one_drop(around(lambda X: tops[X], V)):
                hits.append(rots)
        print(f'   shared staircase round a {lab} corner: {len(hits)} of 216 turn patterns of its 3 cells'
              + (f' (e.g. {hits[0]}; uniform among them: {any(len(set(h))==1 for h in hits)})' if hits else ''))
    bts = bottoms_for(top)
    summary[name] = {}
    for b, info in bts.items():
        P = (top, b)
        for mirrors in (False, True):
            r = battery([P], mirrors=mirrors)
            key = f"{info[0]} {info[1:3]} {info[3]}{' +mirrors' if mirrors else ''}"
            summary[name][key] = r['verdict']
            if r['verdict'] != 'INVALID':
                print(f'   bottom {key}: {r["verdict"]}  states {r.get("states")}  patch c/h words {r.get("patch_words")}'
                      f'  periodic words {r.get("periodic_words", "")}')
    cnt = {}
    for v in summary[name].values():
        cnt[v] = cnt.get(v, 0) + 1
    print(f'   verdict counts for {name}: {cnt}', flush=True)
    if any(v == 'CANDIDATE' for v in summary[name].values()):
        print(f'   >>> CANDIDATE present for {name}')
json.dump(summary, open(sys.argv[1] if len(sys.argv) > 1 else 'data/02_named.json', 'w'), indent=1)
print(f'time {time.time()-t0:.1f}s')
print('FINAL ok' if ok else 'FINAL FAIL: a top violates climb + risers = 0')
