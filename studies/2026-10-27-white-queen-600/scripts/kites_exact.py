"""Why the kites (DICTO 2026-10-27). Exact, in Q(√5). A cut through a cell's four edges (two corners below, two above) is a
four-sided face. Claim tested here at every atlas height: the face is a kite exactly when the cell's corner heights, measured
from the cut, are -p, -q, +q, +p with p ≠ q (the cell sits symmetrically across the cut, turned so its four corners are at
four different heights); with p = q it is the square of a mid-cut (squares_midcuts.py). Reason: the cell's symmetry that
swaps the corners at -p and +p and those at -q and +q reverses the heights, so it maps the cut onto itself; on the face it
fixes the two corners on the edges p–p and q–q and swaps the other two: a mirror along a diagonal, which makes a kite.
Run:  python3 scripts/kites_exact.py data/600cell-source.json data/atlas600.json   (uses check63_exact.py's arithmetic)
"""
import sys
src = open(__file__.replace("kites_exact.py", "check63_exact.py")).read().split("# ---- 1.")[0]
exec(src.replace('print("atlas entries:"', 'pass  #').replace('if "face_sizes" not in o: print', 'if False: print'))
kites = sym = both = 0
for lab, d in dirs.items():
    h = [dot(v, d) for v in V]; hs = sorted(set(h), key=float)
    samples = [x for x in hs if x.sign() >= 0] + [(a + b) / Q(2) for a, b in zip(hs, hs[1:]) if (a + b).sign() >= 0]
    for hv in samples:
        for c in cells:
            below = [i for i in c if (h[i] - hv).sign() < 0]; above = [i for i in c if (h[i] - hv).sign() > 0]
            if len(below) != 2 or len(above) != 2:
                continue
            def pt(bi, ai):
                t = (hv - h[bi]) / (h[ai] - h[bi]); return tuple(V[bi][k] + t * (V[ai][k] - V[bi][k]) for k in range(4))
            P00, P01, P10, P11 = pt(below[0], above[0]), pt(below[0], above[1]), pt(below[1], above[0]), pt(below[1], above[1])
            s = [sq(sub(P10, P00)), sq(sub(P11, P10)), sq(sub(P01, P11)), sq(sub(P00, P01))]
            kite = ((s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0])) and not (s[0] == s[2] and s[1] == s[3])
            lo = [h[i] - hv for i in below]; hi = [h[i] - hv for i in above]
            symmetric = any(lo[0] + hi[x] == Z and lo[1] + hi[1 - x] == Z for x in (0, 1)) and lo[0] != lo[1]
            kites += kite; sym += symmetric; both += kite and symmetric
print(f"kites {kites}; cells cut symmetrically with four different heights {sym}; both {both}")
print("CLAIM HOLDS" if kites == sym == both else "CLAIM FAILS")
