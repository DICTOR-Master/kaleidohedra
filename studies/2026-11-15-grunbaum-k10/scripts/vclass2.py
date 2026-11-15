#!/usr/bin/env python3
"""Sharpened face-pair test for class C(n) (n = 4, 5, 6): which rank-3 lattices could carry a FACE-TO-FACE lattice tiling?

Zone words. Walk once round zone a. Each face of the zone is crossed from one a-edge to the opposite one, a step +-e_c (its other
direction c). The walk closes and e_1..e_n are independent in Z^n, so the two c-faces of the zone carry opposite signs. Write the zone
as a cyclic word of 2(n-1) signed letters. The vector lambda_ac between the two (a,c) faces is the sum of the signed letters strictly
between the two c's: a letter b counts +-1 when exactly one b lies between, and 0 when both or neither do (their signs cancel). So:
  every lambda_ac has entries in {0, +-1}, zero at a and c, and is nonzero (two faces cannot coincide);
  in a face-to-face lattice tiling all lambda_ac lie in the rank-3 lattice L (lifted to Z^n), V = L (x) Q.
Enumeration. Some Plucker coordinate of V is nonzero; relabel it p_123 and write V = rowspace [I | X]. lambda_12 is a multiple of
(p_12c)_c whose entry at c = 3 is 1, so the third row of X lies in {0, +-1}; likewise the other rows. So X in {0, +-1}^(3 x (n-3)):
3^(3(n-3)) subspaces (19,683 for n = 6), complete up to relabelling. For each V and each zone a we ask: is there a cyclic signed word
whose between-sums equal, up to sign, vectors of V (in {0,+-1}^n, zero at a and c) for all five c? The words are enumerated once
(n = 6: 362,880 per zone, first letter fixed). Survivors are printed with the realising words. Prints PROGRESS and FINAL."""
import sys, json, itertools, time
t0 = time.time()
OUT = sys.argv[1]; NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6

def norm(v):
    for x in v:
        if x: return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

def word_table(m):
    """m letters 0..m-1 each twice with opposite signs, cyclic, first letter 0 with sign +; key = tuple of normalised lambda_c"""
    table = {}
    rest = [0] + [x for c in range(1, m) for x in (c, c)]
    perms = set(itertools.permutations(rest))
    for perm in perms:
        word = (0,) + perm
        for signs in itertools.product((1, -1), repeat=m - 1):
            sg = (1,) + signs; seen = set(); w = []
            for c in word:
                s = sg[c] if c not in seen else -sg[c]; seen.add(c); w.append((c, s))
            lam = []
            ok = True
            for c in range(m):
                i, j = [k for k, (x, _) in enumerate(w) if x == c]
                v = [0]*m
                for k in range(i + 1, j): v[w[k][0]] += w[k][1]
                if not any(v): ok = False; break
                lam.append(norm(v))
            if ok: table.setdefault(tuple(lam), w)
    return table

def run(n):
    m = n - 1; tab = word_table(m)
    print(f'n={n}: {len(tab)} distinct lambda-tuples from zone words t={time.time()-t0:.0f}s', flush=True)
    cells = 3*(n - 3); total = 3**cells; surv = []
    allv = [v for v in itertools.product((0, 1, -1), repeat=n) if any(v)]
    for idx in range(total):
        d = [(idx // 3**j) % 3 for j in range(cells)]; X = [[(0, 1, -1)[d[r*(n-3) + c]] for c in range(n - 3)] for r in range(3)]
        inV = [v for v in allv if all(v[3 + c] == sum(v[r]*X[r][c] for r in range(3)) for c in range(n - 3))]
        ok = True; words = {}
        for a in range(n):
            others = [b for b in range(n) if b != a]
            allowed = []
            for c in others:
                A = set()
                for v in inV:
                    if v[a] == 0 and v[c] == 0: A.add(norm([v[b] for b in others]))
                allowed.append(sorted(A))
                if not A: ok = False; break
            if not ok: break
            hit = None
            for combo in itertools.product(*allowed):
                if combo in tab: hit = tab[combo]; break
            if hit is None: ok = False; break
            words[a] = [(others[c], s) for c, s in hit]
        if ok: surv.append({'X': X, 'zone_words': {str(a): w for a, w in words.items()}})
        if idx % max(1, total//20) == 0: print(f'PROGRESS {idx/total:.3f} n={n} survivors={len(surv)} t={time.time()-t0:.0f}s', flush=True)
    return {'n': n, 'subspaces': total, 'word_tuples': len(tab), 'survivors': len(surv), 'list': surv[:500]}

res = {n: run(n) for n in range(4, NMAX + 1)}
for n, r in res.items(): print(f'n={n}: subspaces {r["subspaces"]}, survivors {r["survivors"]}')
# control: Grunbaum-type D1/D2 lattice (from the n=5 flip search) must survive
D1 = [(1, 0, 0, -1, 1), (0, -1, 0, 0, 1), (0, 0, 1, 1, 0)]
ctrl = None
if NMAX >= 5:
    import fractions
    def rref_key(rows):
        A = [[fractions.Fraction(x) for x in r] for r in rows]; rk = 0
        for c in range(len(A[0])):
            p = next((i for i in range(rk, len(A)) if A[i][c] != 0), None)
            if p is None: continue
            A[rk], A[p] = A[p], A[rk]; A[rk] = [x/A[rk][c] for x in A[rk]]
            for i in range(len(A)):
                if i != rk and A[i][c] != 0: f = A[i][c]; A[i] = [x - f*y for x, y in zip(A[i], A[rk])]
            rk += 1
        return A
    R = rref_key(D1)
    Xd = [[int(R[r][3 + c]) for c in range(2)] for r in range(3)] if all(R[r][r] == 1 for r in range(3)) else None
    ctrl = any(s['X'] == Xd for s in res[5]['list']) if Xd else None
    print('CONTROL D1/D2 lattice', D1, 'RREF X', Xd, 'among n=5 survivors:', ctrl)
json.dump({str(k): v for k, v in res.items()}, open(OUT, 'w'), indent=0)
print('RESULT survivors', {k: v['survivors'] for k, v in res.items()}, f'| {time.time()-t0:.0f}s')
print('FINAL ok' if ctrl and res[4]['survivors'] > 0 else 'FINAL FAIL: positive control (D1/D2 lattice at n = 5, Bilinski at n = 4) not met')
