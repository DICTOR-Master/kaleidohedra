"""Exact form of the stella yantra: Q and S to 1500 digits, then PARI algdep (degree <= 64), accepted only if stable at 2/3
precision and residual < 10^-700."""
import mpmath as mp, cypari2, stella_yantra as Y
mp.mp.dps = 1540; pari = cypari2.Pari(); pari.set_real_precision(1560); pari.allocatemem(2*10**9)
Y.u = 1/mp.sqrt(2)
Q, S = mp.findroot(Y.eqs, (mp.mpf(Y.Q), mp.mpf(Y.S)), tol=mp.mpf(10)**-1520)
found = {}
for name, x in (("Q", Q), ("S", S)):
    s = mp.nstr(x, 1520)
    for d in range(2, 65):
        p = pari(f"algdep({s}, {d})"); p2 = pari(f"algdep({mp.nstr(x, 1000)}, {d})")
        if p == p2 and p.poldegree() == d and abs(complex(pari(f"subst({p}, x, {s})"))) < 1e-700:
            found[name] = str(p); print(name, "degree", d, ":", p, flush=True); break
    else: print(name, "none up to degree 64", flush=True)
print("FINAL ok" if len(found) == 2 else "FINAL FAIL: exact form not found up to degree 64")
