"""Football scutoid study, step 3d (DICTO 11-07: "all three picks go ahead" — PARI/GP): the exact algebraic degree of the closest
stacking (h, b) and of the scutoid corner (distance d, height z). corner_exact.py recomputes everything at DPS digits (default here
1500); PARI's algdep then looks for the minimal polynomial with degrees 2..64. A polynomial is ACCEPTED only if (i) it is irreducible,
(ii) it vanishes at the value to within 10^-(DPS-100), and (iii) its coefficients are small enough that the fit is meaningful
(sum of log10|coeffs| < DPS/2). Run: python3 tools/runjob.py <this> <data file>   (DPS from env, default 1500)"""
import os, sys, io, contextlib
os.environ.setdefault('DPS', '1500'); DPS = int(os.environ['DPS'])
sys.argv = [sys.argv[0]]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    src = open('corner_exact.py').read().split('# integer relations')[0]
    exec(src)
print(f"recomputed at {DPS} digits; corner checks {'OK' if all(r[0] for r in results) else 'FAIL'}")
import cypari2, math
pari = cypari2.Pari(); pari.set_real_precision(DPS); pari.allocatemem(2 * 10**9)
vals = {'h (layer spacing)': hM, 'b (shift)': bM, 'd (corner distance)': results[0][1], 'z (corner height)': results[0][2]}
found = {}
for name, v in vals.items():
    x = pari(mp.nstr(v, DPS - 10)); ok = None
    for k in (2, 4, 6, 8, 12, 16, 24, 32, 48, 64):
        P = pari.algdep(x, k)
        if P.poldegree() < 1: continue
        res = abs(pari.subst(P, 'x', x)); size = sum(math.log10(abs(int(c)) + 1) for c in P.Vec())
        if pari.polisirreducible(P) and res < pari(f'1e-{DPS - 100}') and size < DPS / 2:
            ok = (k, P, size); break
    if ok:
        k, P, size = ok
        print(f"{name}: minimal polynomial of degree {P.poldegree()} (found with algdep(x,{k}); coefficient digits {size:.0f} of {DPS}):\n   {P}")
        found[name] = P
    else:
        print(f"{name}: no integer polynomial of degree <= 64 with coefficients small enough to be meaningful at {DPS} digits")
# the fields: a reduced defining polynomial and the subfields (which square roots the numbers live over)
for name, P in found.items():
    R = pari.polredabs(P); subs = pari.nfsubfields(R)
    print(f"{name}: reduced field polynomial {R}; discriminant of the field {pari.nfdisc(R)}")
    print("   subfields of degree 2 and 4:", [str(sf[0]) for sf in subs if pari.poldegree(sf[0]) in (2, 4)])
print("FINAL ok" if all(r[0] for r in results) else "FINAL FAIL (corner checks failed at high precision)")
