"""Amber keyed, step 1b: the letter configurations (A/B per cell) allowed by the face-to-face rules, as a subshift on the lattice.
Every rule depends only on the face crossed and is symmetric under A<->B (cell B = R(cell A), R in O_h, T_h transitive on each face
class), so each face class allows one of: all pairs, equal letters only (eq), unequal only (neq), nothing (none).
Exact decision (proof in README): a configuration is a 2-colouring with eq/neq constraints along the constrained directions; it exists on
the infinite lattice iff it exists on the torus Lambda/4Lambda (Smith normal form of the constrained sublattice; here every constrained
class spans a sublattice of index 1 or 2, elementary divisors <= 2), and the solution set is finite (all periodic) when some class is
constrained (each T_h face orbit spans R^3, so the constrained sublattice has finite index), free (uncountable, aperiodic allowed but
not forced) only when every class allows all pairs.
Checks: (i) pysat (Glucose3) satisfiability on tori N = 2..6 for EVERY rule table (4 per class) of sc, bcc, fcc; (ii) independent parity
union-find count of configurations on the same tori; both must agree; (iii) the real rule tables read from ../data/keyed_*.json.
Mismatch controls (mismatch_controls): different real cells must be rejected, one exact identity accepted."""
import itertools, json, os, sys
from fractions import Fraction as Fr
import numpy as np
from pysat.solvers import Glucose3
HERE = os.path.dirname(os.path.abspath(__file__))
def pr(*a): print(*a, flush=True)

LAT = {   # primitive basis (rows) and neighbour vectors per face class, integer coordinates
    "sc":  (np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), {"square": [p for p in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, p)) == 1]}),
    "bcc": (np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1]]), {"square": [tuple(2*x for x in p) for p in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, p)) == 1],
                                                              "hexagon": list(itertools.product((-1, 1), repeat=3))}),
    "fcc": (np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]]), {"rhombus": [p for p in itertools.product((-1, 0, 1), repeat=3) if sum(map(abs, p)) == 2]}),
}
TYPES = ("all", "eq", "neq", "none")

def coeffs(B, w):
    c = np.linalg.solve(B.T.astype(float), np.array(w, float)); r = np.round(c).astype(int)
    assert np.allclose(c, r); return tuple(r)

def edges(lat, N, table):
    B, cls = LAT[lat]; out = []
    for cl, vecs in cls.items():
        t = table[cl]
        if t == "all": continue
        for w in vecs:
            c = coeffs(B, w)
            for p in itertools.product(range(N), repeat=3):
                q = tuple((p[i] + c[i]) % N for i in range(3)); out.append((p, q, t))
    return out

def sat(lat, N, table):
    idx = {p: i + 1 for i, p in enumerate(itertools.product(range(N), repeat=3))}
    S = Glucose3()
    for p, q, t in edges(lat, N, table):
        a, b = idx[p], idx[q]
        if t == "none": S.add_clause([a]); S.add_clause([-a])
        elif t == "eq": S.add_clause([-a, b]); S.add_clause([a, -b])
        else: S.add_clause([a, b]); S.add_clause([-a, -b])
    r = S.solve(); S.delete(); return r

def count(lat, N, table):
    """parity union-find: number of configurations = 2^components if consistent, else 0 (log2 returned)"""
    pts = list(itertools.product(range(N), repeat=3)); par = {p: p for p in pts}; par_bit = {p: 0 for p in pts}
    def fnd(p):
        b = 0
        while par[p] != p: b ^= par_bit[p]; p = par[p]
        return p, b
    for p, q, t in edges(lat, N, table):
        if t == "none": return None
        want = 0 if t == "eq" else 1
        (rp, bp), (rq, bq) = fnd(p), fnd(q)
        if rp == rq:
            if bp ^ bq != want: return None
        else: par[rp] = rq; par_bit[rp] = bp ^ bq ^ want
    return len({fnd(p)[0] for p in pts})

def real_tables():
    out = {}
    for f in sorted(os.listdir(os.path.join(HERE, "../data"))):
        if not f.startswith("keyed_") or not f.endswith(".json"): continue
        d = json.load(open(os.path.join(HERE, "../data", f)))
        for rule, R in d["rules"].items():
            tab = {}
            for cl, m in R["classes"].items():
                assert all(len(m[p]) == 1 for p in m), "rule differs within a face class"
                AA, AB, BA, BB = (m[p][0] for p in ("AA", "AB", "BA", "BB"))
                assert AA == BB and AB == BA, "A<->B symmetry of the rules"
                tab[cl] = {(True, True): "all", (True, False): "eq", (False, True): "neq", (False, False): "none"}[(AA, AB)]
            out[(d["lattice"], d["factor"], rule)] = tab
    return out

def parseQ(s):
    if s.endswith("r5"):
        a, b = s[:-2].rsplit("+", 1); return (Fr(a), Fr(b))
    return (Fr(s), Fr(0))

def polys(d, rule, mi, scale=Fr(1)):
    return {frozenset(tuple((x*scale, y*scale) for x, y in (parseQ(t) for t in p)) for p in P) for P in d["rules"][rule]["polygons_A"][mi]}

def mismatch_controls(lat):
    """real cells that are NOT the same cell must be rejected; one exact identity must be accepted.
    (1) comb: 6/5 s0 cell scaled by 5/6 vs the s0 cell (same mould faces, different real division) -> 0 faces may match;
    (2) R1 vs comb at the same scale (two real divisions of one mould) -> 0 faces may match;
    (3) positive: R1 is a central projection, so its 6/5 s0 pattern scaled by 5/6 IS the s0 pattern -> all faces match."""
    d1 = json.load(open(os.path.join(HERE, f"../data/keyed_{lat}_1.json"))); d2 = json.load(open(os.path.join(HERE, f"../data/keyed_{lat}_6-5.json")))
    F = list(d1["rules"]["comb"]["polygons_A"])
    c1 = sum(polys(d1, "comb", mi) == polys(d2, "comb", mi, Fr(5, 6)) for mi in F)
    c2 = sum(polys(d1, "R1", mi) == polys(d1, "comb", mi) for mi in F) + sum(polys(d2, "R1", mi) == polys(d2, "comb", mi) for mi in F)
    c3 = sum(polys(d1, "R1", mi) == polys(d2, "R1", mi, Fr(5, 6)) for mi in F)
    return c1, c2, c3, len(F)

def main():
    Ns = (2, 3, 4, 5, 6)
    allok = True; summary = {}
    pr("All rule tables (types per face class), tori Lambda/N Lambda, N = 2..6: SAT result and parity count must agree")
    for lat, (B, cls) in LAT.items():
        names = list(cls)
        for combo in itertools.product(TYPES, repeat=len(names)):
            table = dict(zip(names, combo))
            row = []
            for N in Ns:
                s = sat(lat, N, table); c = count(lat, N, table)
                if s != (c is not None): allok = False; pr("  DISAGREE", lat, table, N)
                row.append("-" if c is None else ("2^%d" % c))
            inf_sat = row[Ns.index(4)] != "-"
            if not inf_sat: cls_ = "(d) none"
            elif all(t == "all" for t in combo): cls_ = "(a) all (free; aperiodic allowed, not forced)"
            else: cls_ = "(b) finitely many, all periodic"
            summary[(lat, combo)] = cls_
            pr(f"  {lat} {table}: configurations on tori N={Ns}: {row}  -> {cls_}")
    pr("Real rule tables of the Fullerene-Amber Cell (from keyed_*.json):")
    for (lat, fac, rule), tab in sorted(real_tables().items()):
        combo = tuple(tab[n] for n in LAT[lat][1])
        pr(f"  {lat} {fac} s0, {rule}: {tab} -> {summary[(lat, combo)]}")
    for lat in ("sc", "bcc", "fcc"):
        if os.path.exists(os.path.join(HERE, f"../data/keyed_{lat}_1.json")):
            c1, c2, c3, n = mismatch_controls(lat)
            pr(f"  controls {lat}: comb s0 vs comb 6/5 s0 scaled: {c1}/{n} faces match (must be 0); R1 vs comb: {c2}/{2*n} (must be 0); "
               f"R1 s0 vs R1 6/5 s0 scaled (central projection, exact identity): {c3}/{n} (must be {n})")
            if c1 or c2 or c3 != n: allok = False
    pr("FINAL ok" if allok else "FINAL FAIL")

if __name__ == "__main__":
    main()
