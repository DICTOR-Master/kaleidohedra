"""Prolate-oblate walls share no region (24 Nov 2026; reproduces the referee report of 24 Nov, section 4 (a)).  Exact in Q(sqrt5).

For each of the 8 common-scale settings of the paper's wall table (the settings of logs/wall_configs.log), and for each of the 120
prolate-oblate wall configurations (enumerated from geometry exactly as wall_configs.py), the outer patterns of the two sides are
taken relative to the face centre with the pattern code of facematch_exact.py (unchanged) and compared polygon by polygon:
the number of polygons common to both sides is counted exactly.
Pass: in every setting, all 120 prolate-oblate configurations have 0 common polygons.
Control (shows the comparison detects agreement): the 30 + 30 same-type mirror configurations (two different cells) have equal
patterns, every polygon common.
Usage: python wall_disjoint.py   (runs the 8 settings on 8 processes).  Last line FINAL ok only if every check holds."""
import os, sys, io, itertools, runpy, contextlib
from collections import Counter
from fractions import Fraction as Fr
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SETTINGS = [("C1", "S0", "cproj"), ("C1", "S65", "cproj"), ("C2", "S0", "cen"), ("C2", "S65", "cen"), ("dodecahedron", "S0", "cen"),
            ("icosahedron", "S0", "cen"), ("icosahedron", "S0", "cproj"), ("icosidodecahedron", "S65", "cen")]

def run(setting):
    sys.argv = ["facematch_exact.py", *setting]
    with contextlib.redirect_stdout(io.StringIO()):
        fm = runpy.run_path(os.path.join(HERE, "facematch_exact.py"), run_name="facematch_exact")
    from ammann_cell import cross, dot, vsub, vsc
    from tiling import E, TRIPLES, tvol
    def key(v): return tuple(x.key() for x in v)
    def absq(x): return x if x.sign() >= 0 else -x
    vP = max((absq(tvol(A)) for A in TRIPLES), key=float)
    kind = {A: ("P" if (absq(tvol(A)) - vP).sign() == 0 else "O") for A in TRIPLES}
    halves = {}
    for A in TRIPLES:
        for l in A:
            i, j = [a for a in A if a != l]
            for s in (0, 1):
                sig = -(2*s - 1)*dot(cross(E[i], E[j]), E[l]).sign()
                halves.setdefault((i, j), []).append((A, l, s, sig))
    configs = set()
    for pr, H in halves.items():
        for h1, h2 in itertools.combinations(H, 2):
            if h1[3] == -h2[3]: configs.add((pr, frozenset((h1[:3], h2[:3]))))
    def rel(A, l, s):
        fc = vsc(Fr(1, 2) if s else Fr(-1, 2), E[l])
        return frozenset(frozenset(key(vsub(p, fc)) for p in Pg) for Pg in fm["pat"](list(A), l, s))
    po = []; mirror_agree = Counter(); mirror_tot = Counter()
    for c in configs:
        h1, h2 = tuple(c[1]); k = "".join(sorted(kind[h[0]] for h in c[1]))
        r1, r2 = rel(*h1), rel(*h2)
        if k == "OP":
            p1, p2 = (r1, r2) if kind[h1[0]] == "P" else (r2, r1)
            po.append((len(p1 & p2), len(p1), len(p2)))
        elif h1[0] != h2[0]:
            mirror_tot[k] += 1; mirror_agree[k] += (r1 == r2)
    common = Counter(x[0] for x in po)
    nP = sorted({x[1] for x in po}); nO = sorted({x[2] for x in po})
    good = len(po) == 120 and set(common) == {0} and mirror_tot == Counter({"OO": 30, "PP": 30}) and mirror_agree == mirror_tot
    line = (f"{' '.join(setting)}: prolate-oblate configurations {len(po)}, common polygons per configuration {dict(common)}; "
            f"regions prolate side {nP}, oblate side {nO}; control mirror same-type configurations equal: "
            f"OO {mirror_agree['OO']}/{mirror_tot['OO']}, PP {mirror_agree['PP']}/{mirror_tot['PP']}; {'ok' if good else 'FAILED'}")
    return line, good

if __name__ == "__main__":
    with Pool(len(SETTINGS)) as p: res = p.map(run, SETTINGS)
    for line, _ in res: print(line, flush=True)
    ok = len(res) == 8 and all(g for _, g in res)
    print(f"settings passing: {sum(g for _, g in res)}/8")
    print("RESULT: in all 8 settings the two sides of every prolate-oblate wall share no region" if ok else "RESULT: check failed")
    print("FINAL ok" if ok else "FINAL FAILED")
