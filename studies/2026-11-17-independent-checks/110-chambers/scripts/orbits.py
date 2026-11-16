#!/usr/bin/env python3
"""W(H4)-orbits of the flats of an arrangement (exact).  usage: orbits.py walls.npz NAME OUT.json [lines]
rank 2: every plane as the sorted tuple of the walls through it; W acts by the generator
permutations of the walls.  rank 3 (with 'lines'): every line by its exact projective key;
W acts by the simple reflections on directions.  Orbits by union-find; for each orbit its size,
the walls through it and mu.  (written from scratch)"""
import sys, os, json, time
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(__file__))
import zphi as Z

NPZ, NAME, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
DO_LINES = len(sys.argv) > 4 and sys.argv[4] == 'lines'
D = np.load(NPZ); N = D[NAME]; GENS = D[NAME + '_gens']; alpha = D['alpha']; n = len(N)
t0 = time.time()
def say(*a): print(f'[{time.time() - t0:7.1f}s]', *a, flush=True)

def classes(a):
    others = np.array([b for b in range(n) if b != a]); na = N[a]
    p = Z.mul(Z.dot(na, na)[None, None, :], N[others]) - Z.mul(Z.dot(N[others], na)[:, None, :], na[None])
    _, inv = np.unique(Z.canon(p), axis=0, return_inverse=True)
    return others, inv.ravel()

def planes_of(a):
    others, inv = classes(a)
    out = []
    for c in range(inv.max() + 1):
        mem = others[inv == c]
        if mem.min() > a:                      # record each plane once, from its smallest wall
            out.append(tuple([a] + mem.tolist()))
    return out, others, inv

class UF:
    def __init__(s, k): s.p = np.arange(k)
    def find(s, x):
        p = s.p
        r = x
        while p[r] != r: r = p[r]
        while p[x] != r: p[x], x = r, p[x]
        return r
    def union(s, a, b):
        a, b = s.find(a), s.find(b)
        if a != b: s.p[a] = b

def lines_of(a):
    others, inv = classes(a)
    K = inv.max() + 1
    reps = np.array([others[np.nonzero(inv == c)[0][0]] for c in range(K)])
    ia, ib = np.triu_indices(K, 1)
    d = Z.reduce(Z.cross3(N[a][None], N[reps[ia]], N[reps[ib]]))
    k, f = np.unique(Z.canon(d), axis=0, return_index=True)
    return k, d[f]

def main():
    mp.set_start_method('fork')
    res = {}
    with mp.Pool(24) as pool:
        out = pool.map(planes_of, range(n))
    planes = [p for o in out for p in o[0]]
    idx = {p: i for i, p in enumerate(planes)}
    hp = np.zeros((n, n), np.int64)
    for a, (_, others, inv) in enumerate(out): hp[a, others] = np.bincount(inv)[inv] + 1
    uf = UF(len(planes))
    for g in GENS:
        for i, p in enumerate(planes):
            uf.union(i, idx[tuple(sorted(int(g[x]) for x in p))])
    orb = defaultdict(list)
    for i in range(len(planes)): orb[uf.find(i)].append(i)
    t2 = Counter()
    for o in orb.values():
        t2[(len(planes[o[0]]), len(o))] += 1
    say(f'rank 2: {len(planes)} planes in {len(orb)} orbits; (walls through, orbit size): #orbits')
    for k, v in sorted(t2.items()): say('   ', k, v)
    res['rank2_orbits'] = [dict(walls=k[0], mu=k[0] - 1, orbit_size=k[1], orbits=v) for k, v in sorted(t2.items())]
    if DO_LINES:
        with mp.Pool(24) as pool:
            parts = pool.map(lines_of, range(n))
        K = np.concatenate([p[0] for p in parts]); Dd = np.concatenate([p[1] for p in parts])
        K, f = np.unique(K, axis=0, return_index=True); Dd = Dd[f]
        L = len(K); say('lines:', L)
        Kv = np.ascontiguousarray(K).view([('', K.dtype)] * K.shape[1]).ravel()
        uf = UF(L)
        for a in alpha:
            rr = Z.dot(a, a)
            img = Z.mul(Dd, rr[None, :]) - 2 * Z.mul(Z.dot(Dd, a)[:, None, :], a)
            ki = np.ascontiguousarray(Z.canon(img)).view(Kv.dtype).ravel()
            j = np.searchsorted(Kv, ki); assert (Kv[j] == ki).all()
            for x, y in zip(range(L), j): uf.union(x, int(y))
        roots = np.array([uf.find(i) for i in range(L)])
        ur, first, sizes = np.unique(roots, return_index=True, return_counts=True)
        rep = Dd[first]
        inc = (Z.dot(N[None], rep[:, None]) == 0).all(-1)
        t3 = Counter()
        for r in range(len(rep)):
            S = np.nonzero(inc[r])[0]; h = len(S)
            iu, ju = np.triu_indices(h, 1)
            hx = hp[S[iu], S[ju]]
            sx = sum(Fraction(2, int(x)) for x in hx); assert sx.denominator == 1
            mu = -1 + h - int(sx)
            t3[(h, mu, int(sizes[r]))] += 1
        say(f'rank 3: {L} lines in {len(rep)} orbits; (walls through, mu, orbit size): #orbits')
        for k, v in sorted(t3.items()): say('   ', k, v)
        res['rank3_check'] = bool(sum(k[2] * v for k, v in t3.items()) == L)
        res['rank3_orbits'] = [dict(walls=k[0], mu=k[1], orbit_size=k[2], orbits=v) for k, v in sorted(t3.items())]
    json.dump(res, open(OUT, 'w'), indent=1)
    ok = res.get('rank3_check', True)
    print('FINAL ok' if ok else 'FINAL FAIL line orbit sizes do not add up to the line count')

if __name__ == '__main__':
    try: main()
    except Exception as e:
        import traceback; traceback.print_exc(); print('FINAL FAIL', repr(e))
