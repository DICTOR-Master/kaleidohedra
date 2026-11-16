#!/usr/bin/env python3
"""Method A: intersection lattice, Moebius values and characteristic polynomial of a central
arrangement in R^4, exact in Z[phi] (written from scratch for the #110 check).

usage: lattice.py walls.npz NAME MODE OUT.json      MODE = orbit | all
  rank 1: the walls.
  rank 2: for every wall a, the other walls are grouped by the plane H_a ∩ H_b, using the exact
          projective key of p_b = (n_a.n_a) n_b - (n_a.n_b) n_a.  hpair[a,b] = number of walls
          through H_a ∩ H_b.  #flats with h walls = #{ordered pairs with hpair = h} / (h(h-1)).
          mu(X) = h - 1.
  rank 3: lines.  For a wall H (all walls in MODE=all, W-orbit representatives weighted by orbit
          size in MODE=orbit) every line in H is H ∩ X_A ∩ X_B for two planes X_A, X_B in H; its
          exact direction is cross3(n_H, n_A, n_B).  For each line L: S(L) = walls through L
          (exact n.d = 0), h = |S|, mu(L) = -1 + h - sum_{X > L} (h_X - 1), with
          sum_{X > L}(h_X - 1) = sum_{a<b in S} 2/h_X(a,b).  #lines of a type =
          sum_H weight(H) * #(lines of that type in H) / h.
  rank 4: mu(0) from chi(1) = 0.  Regions = |chi(-1)| (Zaslavsky).
"""
import sys, os, json, time
from fractions import Fraction
from math import comb, lcm
from collections import Counter, defaultdict
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import zphi as Z

NPZ, NAME, MODE, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
NPROC = int(os.environ.get('NPROC', '24'))
D = np.load(NPZ)
N = D[NAME]; GENS = D[NAME + '_gens']; n = len(N)
t0 = time.time()
def say(*a): print(f'[{time.time() - t0:7.1f}s]', *a, flush=True)

# ---------- rank 2 ----------
def classes_through(a):
    """exact grouping of the other walls by the plane H_a ∩ H_b.  returns (others, inverse)"""
    others = np.array([b for b in range(n) if b != a])
    na = N[a]
    p = Z.mul(Z.dot(na, na)[None, None, :], N[others]) - Z.mul(Z.dot(N[others], na)[:, None, :], na[None])
    keys = Z.canon(p)
    _, inv = np.unique(keys, axis=0, return_inverse=True)
    return others, inv.ravel()

def hrow(a):
    others, inv = classes_through(a)
    sizes = np.bincount(inv)
    row = np.zeros(n, np.int32)
    row[others] = sizes[inv] + 1
    return row

# ---------- rank 3 ----------
HP = None
def lines_in(H, lo, hi, reps):
    """canonical keys of the lines H ∩ X_A ∩ X_B for class pairs with first index in [lo, hi)"""
    K = len(reps)
    ia, ib = [], []
    for A in range(lo, hi):
        ia.append(np.full(K - A - 1, A)); ib.append(np.arange(A + 1, K))
    ia = np.concatenate(ia); ib = np.concatenate(ib)
    d = Z.reduce(Z.cross3(N[H][None], N[reps[ia]], N[reps[ib]]))
    return Z.canon(d), d

def line_types(H, d):
    """for exact line directions d, compute S(L) and the type (h, flats-by-size) exactly."""
    inc = (Z.dot(N[None, :, :, :], d[:, None, :, :]) == 0).all(-1)   # [U, n]
    assert inc[:, H].all(), 'line not in its wall'
    out = Counter(); kcheck = []
    hs = inc.sum(1)
    for h in np.unique(hs):
        sel = np.nonzero(hs == h)[0]
        S = np.nonzero(inc[sel])[1].reshape(len(sel), h)
        iu, ju = np.triu_indices(h, 1)
        hx = HP[S[:, iu], S[:, ju]]                                   # [m, pairs]
        assert (hx >= 2).all()
        L = 1
        for v in np.unique(hx): L = lcm(L, int(v))
        sx = (2 * L // hx).sum(1)                                     # L * sum 2/h_X
        assert (sx % L == 0).all()
        sumX = sx // L
        mu = -1 + h - sumX
        # flats by size: count of pairs with h_X = k is C(k,2) * #flats of size k
        ks = np.unique(hx)
        cnts = np.stack([(hx == k).sum(1) for k in ks], 1)
        for j, k in enumerate(ks):
            assert (cnts[:, j] % comb(int(k), 2) == 0).all()
        nflats = cnts // np.array([comb(int(k), 2) for k in ks])[None, :]
        # k(H, L) = number of planes X in H through L = #distinct flats through (H, b), b in S\{H}
        hb = HP[H, S].astype(np.int64)                                 # hpair with H (H itself -> 0)
        L2 = 1
        for v in np.unique(hb[hb > 0] - 1): L2 = lcm(L2, int(v))
        sk = np.where(hb > 0, L2 // np.maximum(hb - 1, 1), 0).sum(1)
        assert (sk % L2 == 0).all()
        kcheck.append((sel, sk // L2))
        rows = np.concatenate([np.full((len(sel), 1), h), mu[:, None], nflats], 1)
        for r_, c_ in Counter(map(tuple, rows.tolist())).items():
            out[(int(h), int(r_[1]), tuple((int(k), int(r_[2 + j])) for j, k in enumerate(ks) if r_[2 + j]))] += c_
    return out, kcheck

def worker_lines(args):
    H, lo, hi, reps = args
    return lines_in(H, lo, hi, reps)

def worker_types(args):
    H, d = args
    out, kcheck = line_types(H, d)
    # return k values (planes in H through L) per line for the pair-count check
    kvals = np.zeros(len(d), dtype=np.int64)
    for sel, inv_sum in kcheck: kvals[sel] = inv_sum
    return out, kvals

def main():
    global HP
    say(f'{NAME}: {n} walls, mode {MODE}')
    # wall orbits
    parent = list(range(n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for g in GENS:
        for i in range(n):
            a, b = find(i), find(int(g[i]))
            if a != b: parent[a] = b
    orb = defaultdict(list)
    for i in range(n): orb[find(i)].append(i)
    orbits = sorted(orb.values(), key=lambda o: (-len(o), o[0]))
    say('wall orbits under W(H4):', [len(o) for o in orbits])
    # rank 2 (all walls, exact)
    with Pool(NPROC) as pool:
        HP = np.array(pool.map(hrow, range(n), chunksize=4))
    assert (HP == HP.T).all(), 'hpair not symmetric'
    hv = Counter(HP[np.triu_indices(n, 1)].tolist())          # unordered pairs by h
    N2 = {}
    for h, c in sorted(hv.items()):
        assert c % comb(h, 2) == 0
        N2[h] = c // comb(h, 2)
    assert sum(c * comb(h, 2) for h, c in N2.items()) == comb(n, 2)
    c2 = sum((h - 1) * c for h, c in N2.items())
    say('rank 2 flats by walls through them:', N2, ' sum mu =', c2)
    # rank 3
    reps = [(o[0], len(o)) for o in orbits] if MODE == 'orbit' else [(i, 1) for i in range(n)]
    N3w = defaultdict(Fraction)
    total_lines_in_reps = 0
    with Pool(NPROC) as pool:
        for H, w in reps:
            others, inv = classes_through(H)
            K = inv.max() + 1
            creps = np.array([others[np.nonzero(inv == c)[0][0]] for c in range(K)])
            # split pair ranges evenly
            tot = K * (K - 1) // 2; nchunks = max(1, min(4 * NPROC, tot // 20000 + 1))
            bounds = [0]; acc = 0; target = tot / nchunks
            for A in range(K):
                acc += K - A - 1
                if acc >= target * len(bounds) and A + 1 < K: bounds.append(A + 1)
            bounds.append(K)
            tasks = [(H, bounds[i], bounds[i + 1], creps) for i in range(len(bounds) - 1) if bounds[i] < bounds[i + 1]]
            parts = pool.map(worker_lines, tasks)
            keys = np.concatenate([p[0] for p in parts]); dirs = np.concatenate([p[1] for p in parts])
            ukeys, first, cnt = np.unique(keys, axis=0, return_index=True, return_counts=True)
            udirs = dirs[first]; del keys, dirs
            U = len(ukeys); total_lines_in_reps += U
            ch = np.array_split(np.arange(U), max(1, min(8 * NPROC, U // 500 + 1)))
            res = pool.map(worker_types, [(H, udirs[c]) for c in ch])
            cntH = Counter(); kv = np.zeros(U, dtype=np.int64)
            for c, (o, kvals) in zip(ch, res):
                cntH.update(o); kv[c] = kvals
            # completeness check: each line arises from exactly C(k,2) class pairs
            bad = int((kv * (kv - 1) // 2 != cnt).sum())
            assert bad == 0, f'pair-count check failed on {bad} lines'
            for t, c in cntH.items():
                N3w[t] += Fraction(w * c, t[0])
            say(f'wall {H} (weight {w}): {K} planes, {tot} plane pairs, {U} lines; types {len(cntH)}')
    N3 = {}
    for t, v in N3w.items():
        assert v.denominator == 1, ('non-integral line count', t, v)
        N3[t] = int(v)
    for t in N3:
        assert t[1] < 0, ('mu(L) not negative', t)
    c3 = sum(t[1] * c for t, c in N3.items())
    nlines = sum(N3.values())
    c4 = -(1 - n + c2 + c3)
    chi = [1, -n, c2, c3, c4]       # coefficients of t^4 .. t^0
    regions = sum(abs(x) for x in chi)
    chim1 = sum(c * (-1) ** (4 - i) for i, c in enumerate(chi))
    say('lines:', nlines, ' sum mu(lines) =', c3, ' mu(0) =', c4)
    say('chi(t) = t^4 %+d t^3 %+d t^2 %+d t %+d' % tuple(chi[1:]), ' |chi(-1)| =', abs(chim1), '=', regions)
    # divide by (t - 1)
    q = [chi[0]]
    for c in chi[1:]: q.append(c + q[-1])
    say('chi(t)/(t-1) = t^3 %+d t^2 %+d t %+d, remainder %d' % (q[1], q[2], q[3], q[4]))
    out = dict(arrangement=NAME, walls=n, mode=MODE, wall_orbits=[len(o) for o in orbits],
               rank2={str(h): dict(flats=c, mu=h - 1) for h, c in N2.items()},
               rank3=[dict(walls=t[0], mu=t[1], planes_by_size={str(k): m for k, m in t[2]}, lines=c)
                      for t, c in sorted(N3.items())],
               coefficients=dict(t4=1, t3=-n, t2=c2, t1=c3, t0=c4),
               chi_over_t_minus_1=q[:4], remainder=q[4], regions=regions,
               regions_over_14400=Fraction(regions, 14400).__str__(),
               lines_found_in_representative_walls=total_lines_in_reps)
    json.dump(out, open(OUT, 'w'), indent=1)
    say('rank-3 types (h, mu, planes through L by size): lines')
    for t, c in sorted(N3.items()): say('   ', t, c)
    return out

if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('fork')   # workers inherit the wall data and hpair table
    try:
        out = main()
        print('FINAL ok' if out['remainder'] == 0 else 'FINAL FAIL chi(1) != 0')
    except Exception as e:
        import traceback; traceback.print_exc()
        print('FINAL FAIL', repr(e))
