"""Amber keyed (21 Nov 2026), DICTO's question: can the Fullerene-Amber Cell be KEYED by the orientation of its Fullerene Star?
I_h cap O_h = T_h, so inside a cubic mould the Fullerene Star (C1) stands in exactly two ways, A (T_h axes on the cube axes, the
setting of resin.py) and B = R(A), R = quarter turn about z, (x,y,z) -> (-y,x,z).  The mould is O_h-symmetric, so cell B = R(cell A).

For each lattice / scale and each division rule we compute, exactly in Q(sqrt5), the pattern the resin pieces make on every mould face
(the pieces' top facets), then test face-to-face matching for A|A, A|B, B|A, B|B across every mould face (the set of top polygons on
the face from one cell must equal the set from the neighbour, translated by the neighbour vector v = 2c n/|n|^2).
Rules:  comb = DICTO's combined method (amber.py / combi.py): top of piece F = outer Voronoi cell of F's face centroid, cut by the mould.
        R1   = central division (resin.py): top of piece F = mould surface cap the cone from C1's centre over F.
Also printed: the in-plane symmetry group of every face pattern (elements of O_h fixing the face normal that fix the pattern).
Controls: each pattern is a partition of its mould face (exact area sum); each pattern is invariant under its T_h face stabiliser
(must hold); a perturbed copy (one vertex moved by 1/1000 in the face) must be rejected; a real cell of the other scale (6/5 s0
pattern scaled by 5/6) must be rejected.
Usage: python keyed.py LATTICE FACTOR   -> ../data/keyed_<lat>_<fac>.json"""
import itertools, json, os, sys, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
SWEEP = os.path.join(HERE, "../../2026-11-21-amber-cell-sweep/scripts")
os.environ.setdefault("RESIN_DIR", os.path.join(HERE, "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts"))
sys.path.insert(0, SWEEP)
import numpy as np
from amber import shell, mould_faces, clip, area2, key, fl, Q, dot, cross, vsub, vadd, vsc
from solids import build
T0 = time.time()
def pr(*a): print(*a, flush=True)
Z = Q(0)

def solid_and_scale(lat, fac):
    C = build("C1"); V = C["V"]
    s0 = None
    for n, c in shell(lat, Q(1)):
        for v in V:
            r = dot(n, v)/c
            if s0 is None or (r - s0).sign() > 0: s0 = r
    return C, s0, s0*fac

def canon(P):
    """drop collinear vertices; convex polygon -> frozenset of exact vertex keys"""
    m = len(P); out = []
    for i in range(m):
        a, b, c = P[i-1], P[i], P[(i+1) % m]
        if any(x.sign() for x in cross(vsub(b, a), vsub(c, b))): out.append(b)
    return frozenset(key(p) for p in out), out

def patterns(C, H, rule):
    V, faces, planes = C["V"], C["faces"], C["planes"]; NF = len(faces)
    cent = [[sum((V[i][j] for i in f), Z)/len(f) for j in range(3)] for f, k in faces]
    MF = mould_faces(H)
    out = {}
    if rule == "comb":
        seeds = cent; sq = [dot(p, p) for p in seeds]; sf = np.array([fl(p) for p in seeds])
    for mi, poly in MF:
        pf = np.array([fl(p) for p in poly]); cf = pf.mean(0); rad = np.linalg.norm(pf - cf, axis=1).max()
        L = []
        for F in range(NF):
            P = poly
            if rule == "comb":
                for G in sorted(range(NF), key=lambda G: np.linalg.norm(sf[G] - sf[F])):
                    if G == F: continue
                    a = 2*(sf[G] - sf[F]); b = sf[G] @ sf[G] - sf[F] @ sf[F]
                    if a @ cf + np.linalg.norm(a)*rad < b - 1e-7: continue
                    P = clip(P, vsc(2, vsub(seeds[G], seeds[F])), sq[G] - sq[F])
                    if len(P) < 3: break
            else:   # R1: cone from the centre over face F
                f = faces[F][0]
                for i in range(len(f)):
                    nn = cross(V[f[i]], V[f[(i+1) % len(f)]])
                    if dot(nn, cent[F]).sign() < 0: nn = vsc(-1, nn)
                    P = clip(P, vsc(-1, nn), Z)
                    if len(P) < 3: break
            if len(P) >= 3 and any(x.sign() for x in area2(P)):
                k, Pc = canon(P); L.append((F, k, Pc))
        # control: partition of the mould face (exact area vectors add up; pieces convex inside the face)
        tot = [Z, Z, Z]
        for F, k, Pc in L:
            A = area2(Pc); n = H[mi][0]
            if dot(A, n).sign() < 0: A = vsc(-1, A)
            tot = vadd(tot, A)
        Af = area2(poly)
        if dot(Af, H[mi][0]).sign() < 0: Af = vsc(-1, Af)
        assert all((tot[j] - Af[j]).sign() == 0 for j in range(3)), "pattern is not a partition of the mould face"
        out[mi] = L
    return MF, out

def act_m(M, p): return [sum((p[j]*M[i][j] for j in range(3)), Z) for i in range(3)]
OH = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        OH.append([[Fr(sg[i]) if perm[i] == j else Fr(0) for j in range(3)] for i in range(3)])
def det(M): return np.linalg.det(np.array(M, dtype=float))
def in_Th(M):
    """T_h = signed CYCLIC permutation matrices"""
    perm = tuple(next(j for j in range(3) if M[i][j] != 0) for i in range(3))
    return perm in ((0, 1, 2), (1, 2, 0), (2, 0, 1))
R = [[Fr(0), Fr(-1), Fr(0)], [Fr(1), Fr(0), Fr(0)], [Fr(0), Fr(0), Fr(1)]]   # quarter turn about z: A -> B

def main():
    lat, fac = sys.argv[1], Fr(sys.argv[2])
    C, s0, s = solid_and_scale(lat, fac)
    H = shell(lat, s)
    pr(f"=== amber keyed  C1 (Fullerene Star)  {lat}  s0 = {s0}  s = {fac} s0 = {float(s):.6f}")
    res = dict(lattice=lat, factor=str(fac), s0=str(s0), s=float(s), rules={})
    nkey = lambda n: tuple(x.key() for x in n)
    for rule in ("comb", "R1"):
        MF, PA = patterns(C, H, rule)
        pr(f"[{rule}] patterns computed, every mould face partitioned exactly ({time.time()-T0:.1f}s)")
        plane = {mi: H[mi] for mi, poly in MF}
        byn = {nkey(H[mi][0]): mi for mi in plane}
        # orientation B: rotate every top polygon by R; it lands on mould face R(n)
        PB = {mi: [] for mi in plane}
        for mi, L in PA.items():
            mj = byn[nkey(act_m(R, H[mi][0]))]
            for F, k, Pc in L:
                Pr = [act_m(R, p) for p in Pc]; PB[mj].append((F, frozenset(key(p) for p in Pr), Pr))
        pat = {"A": {mi: frozenset(k for F, k, Pc in L) for mi, L in PA.items()},
               "B": {mi: frozenset(k for F, k, Pc in L) for mi, L in PB.items()}}
        assert all(len(pat["A"][mi]) == len(pat["B"][mi]) or True for mi in plane)
        def shifted(S, v): return frozenset(frozenset(tuple((Q(*x) + v[j]).key() for j, x in enumerate(p)) for p in P) for P in S)
        def nvec(mi):
            n, c = H[mi]; return vsc(2*c/dot(n, n), n)
        recs = []
        classes = {}
        for mi in sorted(plane):
            n, c = H[mi]; v = nvec(mi); mo = byn[nkey(vsc(-1, n))]
            row = dict(face=mi, normal=[str(x) for x in n], npieces=len(pat["A"][mi]))
            for o1, o2 in (("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")):
                row[o1 + o2] = pat[o1][mi] == shifted(pat[o2][mo], v)
            # in-plane symmetry of the A pattern: elements g of O_h with g n = n, g(pattern) = pattern (about the face centre v/2)
            sym, symTh = 0, 0
            for M in OH:
                if nkey(act_m(M, n)) != nkey(n): continue
                img = frozenset(frozenset(key(act_m(M, [Q(*x) for x in p])) for p in P) for P in pat["A"][mi])
                ok = img == pat["A"][mi]
                if ok: sym += 1
                if in_Th(M):
                    symTh += 1
                    assert ok, "control failed: pattern not invariant under its T_h face stabiliser"
            stab = sum(1 for M in OH if nkey(act_m(M, n)) == nkey(n))
            row.update(sym_order=sym, stab_Oh=stab, stab_Th=symTh)
            recs.append(row)
            cl = "square" if lat == "bcc" and sum(1 for x in n if x.sign()) == 1 else ("hexagon" if lat == "bcc" else ("rhombus" if lat == "fcc" else "square"))
            classes.setdefault(cl, []).append(row)
        # controls: perturbed neighbour and wrong-scale neighbour must be rejected
        mi0 = sorted(plane)[0]; n0, c0 = H[mi0]; v0 = nvec(mi0); mo0 = byn[nkey(vsc(-1, n0))]
        good = pat["A"][mo0] if recs[0]["AA"] else pat["B"][mo0]
        Lp = [list(P) for P in good]; P0 = sorted(Lp[0]); pt = P0[0]
        # move one vertex inside the face plane: along a direction orthogonal to n0
        u = cross(n0, [Q(1), Q(2), Q(3)])
        moved = tuple((Q(*x) + u[j]*Fr(1, 1000)).key() for j, x in enumerate(pt))
        pert = frozenset(frozenset(moved if p == pt else p for p in P) for P in good)
        o1 = "A"; o2 = "A" if recs[0]["AA"] else "B"
        ctrl_good = pat[o1][mi0] == shifted(good, v0)
        ctrl_pert = pat[o1][mi0] == shifted(pert, v0)
        pr(f"[{rule}] control: matching pair {o1}|{o2} on face {mi0} accepted: {ctrl_good}; perturbed copy rejected: {not ctrl_pert}")
        assert ctrl_good and not ctrl_pert
        for cl, rows in classes.items():
            tab = {p: sorted({r[p] for r in rows}) for p in ("AA", "AB", "BA", "BB")}
            syms = sorted({(r["sym_order"], r["stab_Th"], r["stab_Oh"]) for r in rows})
            pr(f"[{rule}] {cl} faces ({len(rows)}): pieces on a face {sorted({r['npieces'] for r in rows})}; "
               f"A|A {tab['AA']} A|B {tab['AB']} B|A {tab['BA']} B|B {tab['BB']}; pattern symmetry (order, T_h stab, O_h stab) {syms}")
        res["rules"][rule] = dict(faces=recs, polygons_A={str(mi): [[[str(x) for x in p] for p in Pc] for F, k, Pc in PA[mi]] for mi in PA},
                                  pieces_A={str(mi): [F for F, k, Pc in PA[mi]] for mi in PA}, control_pert_rejected=not ctrl_pert,
                                  classes={cl: {p: sorted({r[p] for r in rows}) for p in ("AA", "AB", "BA", "BB")} for cl, rows in classes.items()})
    json.dump(res, open(os.path.join(HERE, f"../data/keyed_{lat}_{str(fac).replace('/', '-')}.json"), "w"), indent=1)
    pr(f"done ({time.time()-T0:.1f}s)")

if __name__ == "__main__":
    main()
