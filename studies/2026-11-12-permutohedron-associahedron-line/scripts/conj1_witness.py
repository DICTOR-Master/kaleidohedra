"""Check of the witness point in the proof of Conjecture 1 (equal-speed line B: facet S present exactly for s < D_S), n = 3..N.
DICTO · dictospheres.com - study 2026-11-12-permutohedron-associahedron-line, 13 Nov 2026.  Exact integers, stdlib only.

For a non-interval S with blocks b_1 < ... < b_m (sizes k_1..k_m, K = sum k), the proof's point x is:
  on each block b: the values 1, 2, ..., k_b (in increasing order);
  on the complement G (size n - K): the values K+1, ..., n in increasing order, plus E_p = k_p (k_{p+1} + ... + k_m) added to the
  first element of the gap between b_p and b_{p+1} (p = 1..m-1).
The proof needs: x(S) = z_L(S) (so x lies on the hyperplane of S at s = D_S), x([n]) = C(n+1, 2), x(I) >= C(|I|+1, 2) for every
interval I, x(U) >= C(|U|+1, 2) - D_S for every other nonempty proper U.  Then concavity of the facet margin in s gives the claim.
This script checks those conditions for every non-interval S, n = 3..N, by subset sums over all 2^n subsets.
Negative control: the same point with all the extras on the last complement element must fail for some S at every n >= 4.
Usage: python3 conj1_witness.py N   Prints PROGRESS lines and 'WITNESS ok' / 'WITNESS FAIL'."""
import sys, time
from math import comb
NMAX = int(sys.argv[1]); T0 = time.time(); OK = True; tot = 0
for n in range(3, NMAX + 1):
    FULLM = (1 << n) - 1
    def blocks(m):
        out = []; i = 0
        while i < n:
            if (m >> i) & 1:
                j = i
                while j < n and (m >> j) & 1: j += 1
                out.append((i, j)); i = j
            else: i += 1
        return out
    isint = [False] + [len(blocks(m)) == 1 for m in range(1, FULLM + 1)]
    pc = [bin(m).count('1') for m in range(FULLM + 1)]
    bad = 0; cnt = 0; negfail = 0
    for S in range(1, FULLM):
        if isint[S]: continue
        bl = blocks(S); ks = [j - i for i, j in bl]; K = sum(ks); DS = sum(ks[p] * ks[q] for p in range(len(ks)) for q in range(p + 1, len(ks)))
        x = [0] * n
        for (i, j) in bl:
            for t in range(i, j): x[t] = t - i + 1
        G = [t for t in range(n) if not (S >> t) & 1]
        for r, t in enumerate(G): x[t] = K + 1 + r
        zL_S = sum(k * (k + 1) // 2 for k in ks)
        def valid(x):
            xs = [0] * (FULLM + 1)
            for m in range(1, FULLM + 1):
                low = m & -m; xs[m] = xs[m ^ low] + x[low.bit_length() - 1]
            return xs[S] == zL_S and xs[FULLM] == comb(n + 1, 2) and all(
                xs[U] >= comb(pc[U] + 1, 2) - (0 if isint[U] else DS) for U in range(1, FULLM))
        xneg = list(x); xneg[G[-1]] += DS          # negative control: all extras on the last complement element
        for p in range(len(bl) - 1):
            x[bl[p][1]] += ks[p] * sum(ks[p + 1:])     # first element of the gap after block p
        good = valid(x); cnt += 1; bad += not good; negfail += not valid(xneg)
        if not good and bad <= 3: print(f'FAIL n={n} S={[t + 1 for t in range(n) if (S >> t) & 1]} x={x}', flush=True)
    tot += cnt; OK = OK and bad == 0 and (negfail > 0 or n == 3)   # n = 3: the only gap element is the last one
    print(f'PROGRESS {n - 2}/{NMAX - 2} n={n}: {cnt} non-interval facets, witness valid for {cnt - bad}; negative control (extras off the gaps) fails for {negfail}  ({time.time() - T0:.1f} s)', flush=True)
print(f'{tot} non-interval facets checked, n = 3..{NMAX}', flush=True)
print('WITNESS ok' if OK else 'WITNESS FAIL', flush=True); sys.exit(0 if OK else 1)
