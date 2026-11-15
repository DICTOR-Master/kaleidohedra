"""Event census of a 2D grain-growth run (vertex2d.py output) with the shared event logger, used unchanged
(studies/2026-11-15-event-logger/scripts/eventlog.py; md5 recorded in the output). This file is the adapter.
- logger at strides 1, 2, 4 on the same frames (pair rule and by_segment rule); torus Euler V - E + F = 0 per frame (the logger
  checks Euler on spheres only); negative control (one cell-changing event retyped as a swap must fail the balance);
- the exact event list of the simulation is the ground truth: logger swaps/deaths at stride 1 are compared with it;
- persistence (two-sided, as in the Earth stream): a swap counts when the lost contact had lasted, and the new contact lasts, while
  the mean grain area grows by a fraction q (q = 0.01, 0.05); a contact ended by a grain's death has not lasted;
- side-shedding: a swap is "shedding" when one of the two grains that lose a side is small (area < f <A>, f = 0.1, 0.2) or
  vanishes before <A> grows by 5%; "macroscopic" swaps are the rest (Rutenberg & McCurdy count macroscopic T1s);
- windows of grain number (N0/2..N0/4, N0/4..N0/8, N0/8..end) show whether the ratios have settled.
Usage: census2d.py RUNDIR OUT.json"""
import sys, os, json, hashlib, math
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
LOGDIR = os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts')
sys.path.insert(0, LOGDIR)
import eventlog as E
MD5 = hashlib.md5(open(os.path.join(LOGDIR, 'eventlog.py'), 'rb').read()).hexdigest()

run, outp = sys.argv[1], sys.argv[2]
fin = json.load(open(os.path.join(run, 'final.json')))
N0 = fin['params']['N0']
stats = [json.loads(l) for l in open(os.path.join(run, 'stats.jsonl'))]
events = [json.loads(l) for l in open(os.path.join(run, 'events.jsonl'))]

# ------------------------------------------------ logger on frames, strides 1, 2, 4
res = {}
strides = (1, 2, 4)
prev = {(s, bs): None for s in strides for bs in (False, True)}
cnt = {k: Counter() for k in prev}; clumps = {k: Counter() for k in prev}; balfail = Counter(); neg = {}
euler_fail = 0; nfr = 0; triple_fail = 0
with open(os.path.join(run, 'frames.jsonl')) as f:
    for i, line in enumerate(f):
        T = E.Tiling.from_json(line); nfr += 1
        J = len(T.junctions) if T.junctions is not None else -1
        if J - len(T.segments) + len(T.cells) != 0: euler_fail += 1
        if T.junctions is None or any(len(j) != 3 for j in T.junctions): triple_fail += 1
        c = E.check_tiling(T)
        for s in strides:
            if i % s: continue
            for bs in (False, True):
                k = (s, bs); A = prev[k]
                if A is not None:
                    ev = E.classify(A, T, by_segment=bs)
                    ok = E.balance(A, T, ev)[0]
                    if not ok: balfail[k] += 1
                    if k not in neg and any(e['net'] for e in ev):
                        bad = [dict(e) for e in ev]; j = next(j for j, e in enumerate(bad) if e['net']); bad[j]['type'] = 'swap'
                        neg[k] = not E.balance(A, T, bad)[0]
                    for e in ev:
                        cnt[k][e['type']] += 1
                        if e['type'] == 'clump': clumps[k][e['pattern']] += 1
                prev[k] = T
logger = {f'stride{s}_{"segment" if bs else "pair"}': dict(counts=dict(cnt[(s, bs)]), clumps=dict(clumps[(s, bs)].most_common(8)),
                                                           balance_failures=balfail[(s, bs)], neg_control_caught=neg.get((s, bs)))
          for s in strides for bs in (False, True)}

# ------------------------------------------------ exact events: persistence, shedding, windows
ex = Counter(e[1] for e in events)
tA = [(s['t'], s['Abar']) for s in stats]
import bisect
ts = [x[0] for x in tA]
def Abar(t):
    i = min(max(bisect.bisect_right(ts, t) - 1, 0), len(tA) - 1); return tA[i][1]
def t_grow(t, q):                    # time at which <A> has grown by fraction q since t
    a = Abar(t) * (1 + q); i = bisect.bisect_right(ts, t)
    while i < len(tA) and tA[i][1] < a: i += 1
    return tA[i][0] if i < len(tA) else float('inf')
def t_back(t, q):                    # earliest time with <A> >= Abar(t)/(1+q)
    a = Abar(t) / (1 + q); i = bisect.bisect_right(ts, t) - 1
    while i > 0 and tA[i - 1][1] >= a: i -= 1
    return tA[max(i, 0)][0]
# contact histories from the exact events: (pair) -> list of (t, +1 gained / -1 lost), death times
hist = defaultdict(list); death_t = {}
for e in events:
    t, ty = e[0], e[1]
    if ty == 'T1':
        Pg, Qg, R, S = e[2:6]; hist[tuple(sorted((Pg, Qg)))].append((t, -1)); hist[tuple(sorted((R, S)))].append((t, +1))
    elif ty == 'T2': death_t[e[2]] = t
    elif ty == 'lens': death_t[e[2]] = t
Nrun = N0; Nat = []
for e in events:
    if e[1] in ('T2', 'lens'): Nrun -= 1
    Nat.append(Nrun)
def lasted_after(pair, t, q):        # contact (gained at t) still present when <A> has grown by q, both grains alive
    tq = t_grow(t, q)
    if tq == float('inf'): return None  # censored: run ended
    for (tt, s) in hist[pair]:
        if t < tt <= tq and s == -1: return False
    if any(death_t.get(g, float('inf')) <= tq for g in pair): return False
    return True
def lasted_before(pair, t, q):       # contact (lost at t) had been present since <A> was smaller by q
    tb = t_back(t, q)
    if tb <= ts[0] + 1e-15 and Abar(t) < ts[0] + 1e9 and Abar(ts[0]) * (1 + q) > Abar(t): return None
    for (tt, s) in hist[pair]:
        if tb <= tt < t and s == +1: return False
    return True
wins = [(N0, N0 // 2), (N0 // 2, N0 // 4), (N0 // 4, N0 // 8), (N0 // 8, 0)]
def win(Nv):
    for a, b in wins:
        if b < Nv <= a: return f'{a}-{b}'
W = defaultdict(Counter)
for e, Nv in zip(events, Nat):
    w = win(Nv); ty = e[1]; t = e[0]
    if ty in ('T2', 'lens'): W[w][ty] += 1; continue
    W[w]['T1'] += 1
    Pg, Qg, R, S = e[2:6]; aP, aQ, Ab = e[6], e[7], e[8]
    for q in (0.01, 0.05):
        a = lasted_before(tuple(sorted((Pg, Qg))), t, q); b = lasted_after(tuple(sorted((R, S))), t, q)
        if a is None or b is None: W[w][f'T1 censored q{q}'] += 1
        elif a and b: W[w][f'T1 persistent q{q}'] += 1
    for fr in (0.1, 0.2):
        if min(aP, aQ) < fr * Ab: W[w][f'T1 shedding area<{fr}'] += 1
    tv = t_grow(t, 0.05)
    if death_t.get(Pg, float('inf')) <= tv or death_t.get(Qg, float('inf')) <= tv: W[w]['T1 shedding (loser dies within 5% growth)'] += 1
ratios = {}
for w, c in W.items():
    d = c['T2'] + c['lens']
    if d == 0: continue
    r = dict(vanished=d, T1=c['T1'], T1_per_vanished=c['T1'] / d)
    for k, v in c.items():
        if k.startswith('T1 '): r[k.replace('T1 ', '') + ' per vanished'] = v / d
    r['macroscopic (not shedding by area<0.1) per vanished'] = (c['T1'] - c['T1 shedding area<0.1']) / d
    r['macroscopic (loser survives 5% growth) per vanished'] = (c['T1'] - c['T1 shedding (loser dies within 5% growth)']) / d
    ratios[w] = r
# steady-state topology in the same windows
topo = {}
for a, b in wins:
    ss = [s for s in stats if b < s['N'] <= a]
    if not ss: continue
    p = [sum(s['p'][k] for s in ss) / len(ss) for k in range(16)]
    topo[f'{a}-{b}'] = dict(frames=len(ss), mu2=sum(s['mu2'] for s in ss) / len(ss), mean_n=sum(s['mean_n'] for s in ss) / len(ss),
                           p={str(k): round(p[k], 4) for k in range(2, 13) if p[k] > 0},
                           lewis={k: sum(s['lewis'].get(k, 0) for s in ss) / max(1, sum(k in s['lewis'] for s in ss)) for k in map(str, range(3, 13))},
                           aboav={k: sum(s['aboav'].get(k, 0) for s in ss) / max(1, sum(k in s['aboav'] for s in ss)) for k in map(str, range(3, 13))})
ok = euler_fail == 0 and all(v == 0 for v in balfail.values()) and all(neg.get(k, True) for k in prev)
out = dict(run=os.path.basename(run.rstrip('/')), logger_md5=MD5, params=fin['params'], status=fin['status'], frames=nfr,
           torus_euler_failures=euler_fail, frames_not_all_triple=triple_fail, sim_euler_failures=fin['euler_failures'],
           exact_events=dict(ex), anomalies=fin['anomalies'], logger=logger, windows=ratios, topology=topo,
           von_neumann=fin['von_neumann'], sides_at_small_area=fin['sides_at_small_area'], ok=ok)
json.dump(out, open(outp, 'w'), indent=1)
print('CENSUS2D_OK' if ok else 'CENSUS2D_FAIL', out['run'], json.dumps(dict(exact=dict(ex), logger1=logger['stride1_segment']['counts'],
      vn=fin['von_neumann']['slope'], last=ratios.get(f'{N0 // 8}-0'))))
