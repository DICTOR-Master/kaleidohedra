"""Vacuus cut of an amber cell (26 Nov 2026; idea proposed by Claude, tested at DICTO's "yes test the vacuus cut"). With Claude (Anthropic).
The resin between a fair die (centre O inside) and its mould is cut along the die's own Vacuus planes: for every die edge (u, v), the
plane through O, u, v. The piece over die face F is  cone(O, F) ∩ mould ∩ {beyond F's plane}: an intersection of half-spaces, so it is
CONVEX by construction, its neighbours are exactly the die's face neighbours (no Y vertex can occur), and it has one lateral face per
edge of F, lying in a Vacuus plane. What is left to compute: its outer end, the part of the mould surface inside cone(O, F): one mould
face (a flat end: a true frustum of a pyramid, ends not parallel in general) or several (a bent end, across mould edges).
Exact in Q(sqrt5) (same solids and moulds as amber_aequus.py). Check: piece volumes add to mould - die exactly; every outer end nonempty.
Usage: python vacuus_cut.py SOLID LATTICE FACTOR   (e.g. aequus-61 sc 6/5)."""
import os, sys, json
from collections import Counter
from fractions import Fraction as Fr
sys.argv_saved = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = sys.argv_saved
from resin import Q, dot, cross, vsub, det3

def main():
    solid, lat, fac = sys.argv[1], sys.argv[2], Fr(sys.argv[3])
    C = A.build(solid); V, faces = C["V"], C["faces"]
    s0 = None
    for n, c in A.shell(lat, Q(1)):
        for v in V:
            r = dot(n, v) / c
            if s0 is None or (r - s0).sign() > 0: s0 = r
    s = s0 * fac; H = A.shell(lat, s); MF = A.mould_faces(H)
    Z = Q(0)
    def pyr(P):   # 6 x volume of the pyramid O-P (P a convex polygon, any orientation)
        t = Z
        for q in range(1, len(P) - 1): t = t + det3(P[0], P[q], P[q + 1])
        return t if t.sign() >= 0 else -t
    vol_die = Z; vol_pieces = Z; ends = []; lat_sides = []
    for f, kind in faces:
        P = [V[i] for i in f]; vol_die = vol_die + pyr(P)
        cen = [sum((p[j] for p in P), Z) / len(P) for j in range(3)]
        cone = []
        for i in range(len(P)):
            n = cross(P[i], P[(i + 1) % len(P)])
            if dot(n, cen).sign() < 0: n = [-x for x in n]
            cone.append(n)                                 # keep n.x >= 0, i.e. clip(-n . x <= 0)
        outer = []
        for mi, poly in MF:
            R = poly
            for n in cone:
                R = A.clip(R, [-x for x in n], Z)
                if len(R) < 3: break
            if len(R) >= 3 and any(x.sign() != 0 for x in A.area2(R)): outer.append((mi, R))
        assert outer, f"empty outer end for face {f}"
        vp = sum((pyr(R) for _, R in outer), Z) - pyr(P); assert vp.sign() > 0
        vol_pieces = vol_pieces + vp
        corners = len({A.key(p) for _, R in outer for p in R})
        ends.append((len(P), len(outer), corners))
    vol_die = vol_die / 6; vol_pieces = vol_pieces / 6; vol_res = s * s * s * A.CELLVOL[lat] - vol_die
    gap = vol_pieces - vol_res
    flat = sum(1 for k, m, c in ends if m == 1)
    kinds = Counter((k, m, c) for k, m, c in ends)
    print(f"VACUUS CUT {solid} {lat} {fac}: {len(ends)} pieces, all convex, Y vertices 0; flat outer end {flat}, bent {len(ends) - flat};"
          f" (die-face sides, mould faces met, outer-end corners): {dict(sorted(kinds.items()))}; volume gap {gap}", flush=True)
    print("RESULT", "valid=True" if gap.sign() == 0 else "valid=False", flush=True)

if __name__ == "__main__":
    main()
