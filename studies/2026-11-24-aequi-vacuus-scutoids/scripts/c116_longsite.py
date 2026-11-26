"""Sectored attack (26 Nov 2026; DICTO: "sector the study so it is only having to solve a part which can actually be multiplied once
successful"). With Claude (Anthropic). After floor 1 (the 24 independent swaps, 132/174), the 6 long changes are one problem repeated:
their T_h orbit has 6 members (pairs about the 3 two-fold axes). Solve ONE long change locally: guided (beam) search of short sequences
of single swaps and divide/rejoin moves restricted to the neighbourhood of that pair (faces within 2 steps), ending with the pair
touching, no copy left, and no Minana pair lost in the neighbourhood. Then copy the sequence to the 5 other sites by T_h and check the
copies do not collide (disjoint supports, or the combined result still holds). Combinatorics only."""
import os, sys, itertools, json
os.environ.setdefault('PAIRFILE', 'pairing_local.json'); os.environ['DEPTH'] = '1'
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'c116_stages.py')).read().split("sc, T, path = best")[0]
exec(src)                                   # T0, target, E, gimg, flip1, moves..., best = floor 1 state
T1st = best[1]; cur = E(T1st)
missing = sorted(target - cur, key=lambda e: sorted(e))
nbr = {k: set() for k in range(60)}
for e in cur:
    a, b = tuple(e); nbr[a].add(b); nbr[b].add(a)
def dist(a, b, lim=8):
    fr, seen, k = {a}, {a}, 0
    while fr and k <= lim:
        if b in fr: return k
        fr = {y for x in fr for y in nbr[x]} - seen; seen |= fr; k += 1
    return 99
long_ = [e for e in missing if dist(*tuple(e)) > 2]
print('after floor 1: missing', len(missing), '; long ones (distance > 2):', [(sorted(e), dist(*tuple(e))) for e in long_], flush=True)
site = long_[0]; c, d = tuple(site)
hood = {c, d} | nbr[c] | nbr[d] | {y for x in nbr[c] | nbr[d] for y in nbr[x]}
print('site', sorted(site), 'neighbourhood faces', len(hood), flush=True)
want = {e for e in target if e <= hood}           # Minana pairs inside the neighbourhood
def local_ok(T): return {e for e in E(T) if e <= hood} >= want and site in E(T)
def lflips(T):
    for e in E(T):
        if e <= hood:
            r = flip1(T, e)
            if r is not None and all(x <= hood or not (x - e) for x in [frozenset()]): yield ('swap', tuple(sorted(e))), r
MAXD, BW = int(os.environ.get('MAXD', 12)), int(os.environ.get('BW', 3000))
def gap(T):   # steps between the two faces of the long change in the current neighbour graph
    nb = {}
    for e in E(T):
        a_, b_ = tuple(e); nb.setdefault(a_, set()).add(b_); nb.setdefault(b_, set()).add(a_)
    fr, seen, k = {c}, {c}, 0
    while fr:
        if d in fr: return k
        fr = {y for x in fr for y in nb[x]} - seen; seen |= fr; k += 1
    return 99
def lscore(T): return (gap(T), -len({e for e in E(T) if e <= hood} & want))
found = None; beam = [(lscore(T1st), T1st, [])]; seen = {T1st}
for depth in range(1, MAXD + 1):
    nxt = []
    for _, T, path in beam:
        for mv, T2 in lflips(T):
            if T2 in seen: continue
            seen.add(T2); p2 = path + [mv]
            if site in E(T2) and local_ok(T2): found = p2; break
            nxt.append((lscore(T2), T2, p2))
        if found: break
    if found or not nxt: break
    nxt.sort(key=lambda x: x[0]); beam = nxt[:BW]
    print(f'local depth {depth}: best (gap, -local pairs) {beam[0][0]}, candidates {len(nxt)}', flush=True); print(f'PROGRESS {depth / MAXD:.3f}', flush=True)
print('local solution (swaps only):', found, flush=True)
if found:
    # multiply: apply the sequence's T_h images at all sites, in order, and check
    T = T1st
    for g in range(24):
        for kind, e in found:
            eg = frozenset(gface[g][x] for x in e)
            if eg in E(T):
                r = flip1(T, eg)
                if r is not None: T = r
    sym = symmetric(T); sc = len(E(T) & target)
    print(f'multiplied by T_h: symmetric {sym}; Minana pairs {sc} / 174 (was {len(cur & target)})', flush=True)
    json.dump(dict(site=sorted(site), path=[[k, list(e)] for k, e in found], symmetric=sym, score=sc),
              open(os.path.join(HERE, '../data/c116/longsite.json'), 'w'))
    print('FINAL ok' if sym and sc > len(cur & target) else 'FINAL FAIL (copies collide or no gain)')
else:
    print('FINAL FAIL (no local swap sequence within depth; next: allow divided faces locally)')
