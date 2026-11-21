"""print the run list (args TMIN TMAX [GP = insphere form, GPc = canonical form]): GP(m,n), m >= n >= 0, m >= 1, Tmin <= T <= Tmax, ordered by T then m; bcc at s0 and 6/5 s0"""
import sys
lo, hi = int(sys.argv[1]), int(sys.argv[2]); pre = sys.argv[3] if len(sys.argv) > 3 else "GP"
L = sorted(((m*m+m*n+n*n, m, n) for m in range(1, 40) for n in range(0, m+1) if lo <= m*m+m*n+n*n <= hi))
for T, m, n in L:
    for f in ("1", "6/5"): print(f"{pre}_{m}_{n} bcc {f}")
