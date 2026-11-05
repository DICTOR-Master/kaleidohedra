"""Route (a)(ii) variant: Culik a=1/3 + key 'no two side-by-side n=0 in x1/2 rows', with the key's flag carried by the UP pieces.
D (down) shows n, takes carry w, passes m = qn + w and z = (n == 0) to its U; U shows s, gives carry e to the next D, and passes z to the
next U through their side contact; U checks 'not (z_prev and z)'. Counts the states each piece needs, from real rows (Beatty, many x)."""
from fractions import Fraction as Fr
from math import floor
def rows(q, lo, hi):
    out = set()
    for den in (97, 101, 103, 107, 211, 307):
        for a in range(int(lo * den), int(hi * den) + 1):
            x = Fr(a, den)
            if not (lo <= x <= hi): continue
            zp = None
            for k in range(1, 400):
                n = floor(k * x) - floor((k - 1) * x); s = floor(k * q * x) - floor((k - 1) * q * x)
                w = q * floor((k - 1) * x) - floor((k - 1) * q * x); e = q * floor(k * x) - floor(k * q * x)
                if zp is not None: out.add((n, s, w, e, zp))
                zp = int(n == 0)
    return out
for q, lo, hi in ((Fr(3), Fr(1, 3), Fr(2, 3)), (Fr(1, 2), Fr(2, 3), Fr(2))):
    R = rows(q, lo, hi); flag = q == Fr(1, 2)
    D = {(n, w) for n, s, w, e, z in R}
    U = {(q * n + w, s, int(n == 0), z) if flag else (q * n + w, s) for n, s, w, e, z in R}
    print(f"x{q}: D states {len(D)}, U states {len(U)}" + (f"  U list {sorted(U)}" if flag else ''))
