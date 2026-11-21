"""Exact follow-up (22 Nov 2026, DICTO: every step behind #118's claims exact). Writes exact_cell.py, seams_exact.py and
facematch_exact.py from ammann_cell.py, seams_cell.py and facematch.py by these replacements ONLY (each asserted to apply once):
 1. Voronoi pattern: the floating-point cull of seeds whose bisector "cannot cut the face" is removed; every seed's bisector is clipped
    exactly in Q(sqrt5) (clipping by a halfspace that contains the polygon leaves it unchanged, so the result is the exact Voronoi cell).
 2. Embedding test: no floating-point stage.  Every pair of triangles of a piece is tested with exact orientation signs; coordinates
    are scaled by one positive common denominator to Z[sqrt5] (integer pairs; signs and comparisons unchanged), bounding boxes compared
    exactly, coplanar cases by the exact separating-axis test as before.
 3. The floating-point sampling cross-check is not run (it was a cross-check only; validity rests on (1)-(4) of the docstring).
 4. Each piece record gets its exact boundary signature 'sig': per facet (coplanar adjacent triangles merged, exact), the set of its
    boundary edges as pairs of exact point keys.  exact_summary.py compares pieces by these signatures under exact group elements.
Run: python make_exact.py (in scripts/)."""
import os, re
H = os.path.dirname(os.path.abspath(__file__))
def rep(src, old, new, name):
    assert src.count(old) == 1, (name, old[:60], src.count(old)); return src.replace(old, new)
CULL = """                # skip G whose bisector cannot cut the face disc (float test with margin)
                a = 2*(sf[G] - sf[F]); b = sf[G] @ sf[G] - sf[F] @ sf[F]
                if a @ cen_f + np.linalg.norm(a)*rad < b - 1e-7: continue
"""
EMB_OLD = """        Fl = {i: fl(X[i]) for t in tris for i in t}
        bb = [(np.min([Fl[i] for i in t], 0) - 1e-9, np.max([Fl[i] for i in t], 0) + 1e-9) for t in tris]
        emb = True
        for i, j in itertools.combinations(range(len(tris)), 2):
            if np.any(bb[i][1] < bb[j][0]) or np.any(bb[j][1] < bb[i][0]): continue
            if not tri_pair_ok(tris[i], tris[j], X, Fl): emb = False; break
"""
EMB_NEW = """        XI = zscale({i: X[i] for t in tris for i in t})
        bb = [zbox([XI[i] for i in t]) for t in tris]
        emb = True
        for i, j in itertools.combinations(range(len(tris)), 2):
            if any((bb[i][1][c] - bb[j][0][c]).sign() < 0 or (bb[j][1][c] - bb[i][0][c]).sign() < 0 for c in range(3)): continue
            if not tri_pair_ok(tris[i], tris[j], XI, None): emb = False; break
"""
ZDEF = '''
# ---------- exact integer Z[sqrt5] arithmetic for the embedding test (make_exact.py) ----------
from math import lcm as _lcm
class Z5:
    __slots__ = ("a", "b")
    def __init__(s, a, b): s.a = a; s.b = b
    def __add__(s, o): return Z5(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Z5(s.a - o.a, s.b - o.b)
    def __neg__(s): return Z5(-s.a, -s.b)
    def __mul__(s, o): return Z5(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a)
    def sign(s):
        a, b = s.a, s.b
        if a >= 0 and b >= 0: return 0 if (a == 0 and b == 0) else 1
        if a <= 0 and b <= 0: return -1
        d = a*a - 5*b*b
        return (1 if d > 0 else -1 if d < 0 else 0) * (1 if a > 0 else -1)
def zscale(D):
    L = 1
    for v in D.values():
        for x in v: L = _lcm(L, x.a.denominator, x.b.denominator)
    return {i: [Z5(int(x.a*L), int(x.b*L)) for x in v] for i, v in D.items()}
def zbox(P):
    lo, hi = list(P[0]), list(P[0])
    for p in P[1:]:
        for c in range(3):
            if (p[c] - lo[c]).sign() < 0: lo[c] = p[c]
            if (p[c] - hi[c]).sign() > 0: hi[c] = p[c]
    return lo, hi
'''
SAMP_OLD = "    mc = None\n    if allok:\n        rng = np.random.default_rng(1)"
SAMP_NEW = "    mc = None\n    if allok and os.environ.get('FLOAT_SAMPLING'):\n        rng = np.random.default_rng(1)"
SIG_OLD = "        facets = {}\n        for i in range(len(tris)): facets.setdefault(fd(i), []).append(i)\n"
SIG_NEW = SIG_OLD + """        _sig = []
        for _fl in facets.values():
            _ce = Counter(frozenset((tris[i][k], tris[i][(k+1) % 3])) for i in _fl for k in range(3))
            _sig.append(sorted(sorted(",".join(map(str, X[v])) for v in e) for e, c in _ce.items() if c == 1))
        pc["sig"] = sorted(_sig)
"""
REC_OLD = "        recs.append(dict(F=F, kind=pc[\"kind\"],"
REC_NEW = "        recs.append(dict(F=F, sig=pc[\"sig\"], kind=pc[\"kind\"],"
def exactify(src, name, cell=True):
    src = rep(src, CULL, "", name)
    if not cell: return src
    src = rep(src, "    for fast in (True, False):\n", "    for fast in (False,):\n", name)
    src = rep(src, "# ---------- triangle intersection", ZDEF + "# ---------- triangle intersection", name)
    src = rep(src, EMB_OLD, EMB_NEW, name)
    src = rep(src, SAMP_OLD, SAMP_NEW, name)
    if "recs.append" in src:
        src = rep(src, SIG_OLD, SIG_NEW, name); src = rep(src, REC_OLD, REC_NEW, name)
    return src
HEAD = '"""EXACT VERSION written by make_exact.py (22 Nov 2026) from {0}; see make_exact.py for the four changes. Data to ../data/exact/."""\n'
for srcf, dst, cell in (("ammann_cell.py", "exact_cell.py", True), ("seams_cell.py", "seams_exact.py", True)):
    s = open(os.path.join(H, srcf)).read()
    s = exactify(s, srcf, cell)
    s = s.replace('"../data/ammann_', '"../data/exact/ammann_').replace("f\"../data/ammann_", "f\"../data/exact/ammann_")
    open(os.path.join(H, dst), "w").write(HEAD.format(srcf) + s)
s = open(os.path.join(H, "facematch.py")).read()
FM_OLD = "            if a @ cen_f + np.linalg.norm(a)*rad < b - 1e-7: continue\n"
s = rep(s, FM_OLD, "", "facematch.py")
open(os.path.join(H, "facematch_exact.py"), "w").write(HEAD.format("facematch.py") + s)
print("written exact_cell.py, seams_exact.py, facematch_exact.py")
