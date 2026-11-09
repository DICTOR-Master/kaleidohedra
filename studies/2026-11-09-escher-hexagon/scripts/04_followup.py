"""04: follow-up on the helical-ramp pieces (family C1) that tile: which stackings survive on larger patches,
explicit periodic stack (built from a cycle of the layer graph and checked exactly, column by column),
and why the C2-turned bottoms fail.  Writes data/04_stack.json for the figure."""
import sys, time, json, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from escher import *
sys.argv = [sys.argv[0], 'C1', '0', '1']
import importlib.util
spec = importlib.util.spec_from_file_location('scan', __file__.rsplit('/', 1)[0] + '/03_scan.py')
scan = importlib.util.module_from_spec(spec); spec.loader.exec_module(scan)

t0 = time.time()
ok = True


def words(P, K, R, mirrors=False):
    sts, _ = states([P], mirrors)
    C = compat_table(sts)
    adm = []
    for w in itertools.product((1, 2), repeat=K - 1):
        if w[0] != 1:
            continue
        cells, con = patch_contacts(w, R)
        if sat_solve(len(cells), len(sts), con, C)[0]:
            adm.append(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    return adm


def cycle_stack(P, M, nlayers):
    sts, _ = states([P])
    C = compat_table(sts)
    alive, edges, conf = periodic_alive(C, len(sts), M)
    adj = {}
    for a, l, b in edges:
        adj.setdefault(a, []).append((l, b))
    a = min(alive)
    seq = [(a, None)]
    for _ in range(nlayers - 1):
        l, b = adj[a][0]
        seq.append((b, l))
        a = b
    return sts, C, conf, seq


# 1. the periodic C1 pieces: words on 6-layer patches of radius 3, mirrors too, larger tori
per = []
for tag, top in scan.tops_c1():
    for b, info in bottoms_for(top).items():
        if info[3] == 'uniform':
            continue
        P = (top, b)
        if not valid(P) or thickness_sum(P) != 216:
            continue
        r = battery([P])
        if r['verdict'].startswith('PERIODIC'):
            per.append((tag, info, P, r))
print(f'periodic (non-uniform bottom) ramp pieces: {len(per)}', flush=True)
wsets = {}
for tag, info, P, r in per[:: max(1, len(per) // 60)]:
    w6 = words(P, 6, 3)
    wm = words(P, 6, 3, True)
    wsets[(tuple(w6), tuple(wm))] = wsets.get((tuple(w6), tuple(wm)), 0) + 1
print('sampled pieces: c/h words on 6-layer patches R=3 (proper | with mirror copies): count')
for (a, b), v in wsets.items():
    print(f'   {list(a)} | {list(b)} : {v}')
ok &= all(set(a) <= {'hhhh'} for (a, b) in wsets)

# 2. the most literal piece: E1 (six plates climbing 2, rise 12 = one layer per turn, one riser), forced-h bottom
E1 = top_from([(2 * s + 2, 2 * s + 1, 2 * s + 3) for s in range(6)])
pick = None
for b, info in bottoms_for(E1).items():
    P = (E1, b)
    if info[3] != 'uniform' and valid(P) and thickness_sum(P) == 216:
        r = battery([P])
        print(f'E1 bottom {info}: {r["verdict"]} {r.get("periodic_words","")}')
        if r['verdict'].startswith('PERIODIC') and pick is None:
            pick = (info, P, r)
info, P, r = pick
print('figure piece: E1 with bottom', info, 'words K=7 R=3:', words(P, 7, 3))
for M in hnf(4):
    alive, edges, conf = periodic_alive(compat_table(states([P])[0]), len(states([P])[0]), M)
    print(f'   index {M[0]*M[2]} lattice {M}: periodic tilings {"yes" if alive else "no"}'
          + (f', c/h words {ch_words_from_edges(edges, 4)}' if alive else ''))
M = r['M']
sts, C, conf, seq = cycle_stack(P, M, 5)
# build the explicit stack and check it exactly, column by column
anchor = [(0, 0)]
for (_, l) in seq[1:]:
    anchor.append(add(anchor[-1], ORIG[l]))
cells = {}
for k, (cid, l) in enumerate(seq):
    a = anchor[k]
    for i in range(-9, 10):
        for j in range(-9, 10):
            p = (i, j)
            if coset(p) == coset(a) and cart2(p) <= 7:
                q = reduce_mod(coarse(sub(p, a)), M)
                cells[(k, p)] = sts[conf[cid][reps(M).index(q)]]
good = bad = 0
for (k, X), Pc in cells.items():
    for s in range(6):
        T = [add(X, v) for v in TRI[s]]
        nxt = [(k + 1, Y) for Y in T if (k + 1, Y) in cells]
        if not nxt:
            continue
        Y = nxt[0][1]
        top = dict(Pc[0][s]); bot = dict(cells[(k + 1, Y)][1][sec([sub(p, Y) for p in T])])
        if all(top[sub(p, X)] == bot[sub(p, Y)] + H for p in T):
            good += 1
        else:
            bad += 1
print(f'explicit stack: leans {[l for _, l in seq[1:]]}, {len(cells)} cells, exact column contacts {good}, mismatches {bad}')
ok &= bad == 0 and good > 0
json.dump({'piece': [list(map(list, P[0])), list(map(list, P[1]))],
           'cells': [[k, list(p), [list(map(list, c[0])), list(map(list, c[1]))]] for (k, p), c in cells.items()],
           'leans': [l for _, l in seq[1:]]}, open('data/04_stack.json', 'w'), default=list)

# 3. C2-turned bottoms of E1: minimum thickness
st = sum(dict(E1[s])[v] for s in range(6) for v in dict(E1[s]))
d = (2 * st - 216) // 18
for rr in range(6):
    b = map_relief(E1, planar(rr, 1), True)
    th = min(dict(E1[s])[v] - (dict(b[s])[v] + d) for s in range(6) for v in dict(E1[s]))
    print(f'E1 turned end over end (reflection {rr}, offset {d}): minimum thickness {th}, valid {valid((E1, tuple(tuple(sorted((v, x + d) for v, x in s)) for s in b)))}')
print(f'time {time.time()-t0:.0f}s')
print('FINAL ok' if ok else 'FINAL FAIL: a ramp piece admits a non-h word or the stack check failed')
