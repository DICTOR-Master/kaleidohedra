"""Route (a)(ii) split B: the DOWN piece holds the whole tile (shows n, takes carry w, chooses s and e); it passes (s, e, z=(n==0)) to its UP
piece, which shows s, gives carry e to the next down piece, passes z to the next up piece and checks 'not (z_prev and z)' (x1/2 rows).
Counts the states each piece needs, from real rows (Beatty, many x)."""
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
    D = {(n, s, w, e) for n, s, w, e, z in R}
    U = {(s, e, int(n == 0), z) if flag else (s, e) for n, s, w, e, z in R}
    U0 = {(s, e, int(n == 0)) if flag else (s, e) for n, s, w, e, z in R}
    print(f"x{q}: down {len(D)}, up {len(U)} (without the left flag {len(U0)})" + (f"  up list {sorted(U)}" if flag else ''))
