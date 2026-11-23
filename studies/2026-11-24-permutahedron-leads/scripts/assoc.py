#!/usr/bin/env python3
"""The hidden associahedra (24 Nov 2026), exact.

Construction of Hohlweg, Lange and Thomas (C. Hohlweg, C. Lange, H. Thomas, "Permutahedra and generalized
associahedra", Adv. Math. 226 (2011) 608-640; arXiv 0709.4241, 2007): for a finite reflection group W, a point a
inside the fundamental chamber, and a Coxeter element c, the c-associahedron is the intersection of those facet
half-spaces of the permutahedron Perm(a) = conv(W a) whose facet contains a vertex w a with w a c-singleton
(a prefix, up to commutations, of the c-sorting word w0(c) of the longest element; Reading 2007). The other facets
are removed. Its vertices must number the W-Catalan number (14, 20, 32 for A3, B3, H3).

All arithmetic exact (sympy number fields via vacuus_exact.Fld: Q for A3, Q(sqrt2) for B3, Q(sqrt5) for H3); floats
only to order polygon corners and to guess hull combinatorics, which analyse() then checks exactly.
Usage: python assoc.py [A3|B3|H3 ...]  -> data/assoc-<type>.json, logs printed.
"""
import sys, os, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../2026-11-24-vacuus-enumeration/scripts"))
import sympy as sp
import mpmath as mp
import numpy as np
from vacuus_exact import Fld, analyse, dot, cross, vsub, vadd, scal, vneg, vkey, fl
from perm_checks import refl_matrix, mmul, closure, apply, order

mp.mp.dps = 60
OUT = os.path.join(HERE, "../data")
def pr(*a): print(*a, flush=True)

def setup(typ):
    if typ == "A3":   # D3 = A3 coordinates: mirrors e_i +- e_j; a = (2,1,0): the uniform truncated octahedron
        F = Fld(); c = F.c
        mir = [(c(1), c(-1), c(0)), (c(1), c(1), c(0)), (c(1), c(0), c(-1)), (c(1), c(0), c(1)), (c(0), c(1), c(-1)), (c(0), c(1), c(1))]
        a = (c(2), c(1), c(0)); name = "truncated octahedron"
    elif typ == "B3":  # mirrors e_i +- e_j, e_i; a = (1+2r2, 1+r2, 1): the uniform truncated cuboctahedron
        F = Fld(sp.sqrt(2)); c = F.c; r2 = c("sqrt(2)")
        mir = [(c(1), c(-1), c(0)), (c(1), c(1), c(0)), (c(1), c(0), c(-1)), (c(1), c(0), c(1)), (c(0), c(1), c(-1)), (c(0), c(1), c(1)),
               (c(1), c(0), c(0)), (c(0), c(1), c(0)), (c(0), c(0), c(1))]
        a = (1 + 2 * r2, 1 + r2, c(1)); name = "truncated cuboctahedron"
    else:              # H3, icosahedron (0, +-1, +-phi) cyclic; mirrors: axes and cyclic (phi, +-1, +-1/phi);
        F = Fld(sp.sqrt(5)); c = F.c; phi = (1 + c("sqrt(5)")) / c(2); ip = phi - 1
        mir = [(c(1), c(0), c(0)), (c(0), c(1), c(0)), (c(0), c(0), c(1))]
        for s1, s2 in itertools.product((1, -1), repeat=2):
            t = (phi, s1 * c(1), s2 * ip)
            mir += [t, (t[2], t[0], t[1]), (t[1], t[2], t[0])]
        a = (ip, ip, 3 + phi); name = "truncated icosidodecahedron"   # a vertex of the uniform one (edge 2/phi)
    return F, mir, a, name

CATALAN = {"A3": 14, "B3": 20, "H3": 32}
PERMF = {"A3": 14, "B3": 26, "H3": 62}

def run(typ):
    t0 = time.time()
    F, mir, a, name = setup(typ)
    N = len(mir)
    assert all(F.sign(dot(m, a)) != 0 for m in mir), "a generic"
    mir = [m if F.sign(dot(m, a)) > 0 else vneg(m) for m in mir]           # positive roots w.r.t. a
    R = [refl_matrix(m) for m in mir]
    W = closure(F, R)
    pr(typ, name, "|W| =", len(W), "mirrors", N)
    mk = lambda A: tuple(F.key(x) for row in A for x in row)
    def length(A):   # number of mirrors separating a and A a
        b = apply(A, a); return sum(1 for m in mir if F.sign(dot(m, b)) < 0)
    I = tuple(tuple(F.one if i == j else F.zero for j in range(3)) for i in range(3))
    simple = [k for k in range(N) if length(R[k]) == 1]
    assert len(simple) == 3
    S = [R[k] for k in simple]; al = [mir[k] for k in simple]
    m = [[order(F, mmul(S[i], S[j])) if i != j else 1 for j in range(3)] for i in range(3)]
    # label as a path s1 - s2 - s3 (s2 the middle node; s1 the end with the larger bond)
    mid = [i for i in range(3) if all(m[i][j] > 2 for j in range(3) if j != i)][0]
    ends = sorted([i for i in range(3) if i != mid], key=lambda i: -m[i][mid])
    perm = [ends[0], mid, ends[1]]
    S = [S[i] for i in perm]; al = [al[i] for i in perm]
    M = [[order(F, mmul(S[i], S[j])) if i != j else 1 for j in range(3)] for i in range(3)]
    pr("simple roots", [fl(F, x) for x in al], "Coxeter matrix", M)
    # fundamental weight directions: omega_i orthogonal to the other two simple roots
    om = []
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        w = cross(al[j], al[k])
        if F.sign(dot(w, al[i])) < 0: w = vneg(w)
        om.append(w)
    # permutahedron vertices and facets
    Vp = [apply(A, a) for A in W]
    keyV = {vkey(F, v): i for i, v in enumerate(Vp)}
    assert len(keyV) == len(W)
    facets = {}   # key of normal -> (normal, offset, type i, sides)
    vfac = {}     # vertex index -> facet keys through it
    for A in W:
        v = vkey(F, apply(A, a))
        for i in range(3):
            n = apply(A, om[i]); k = vkey(F, n)
            j, l = [x for x in range(3) if x != i]
            facets.setdefault(k, (n, dot(a, om[i]), i, 2 * M[j][l]))
            vfac.setdefault(keyV[v], set()).add(k)
    assert len(facets) == PERMF[typ], len(facets)
    # check: each facet half-space contains every vertex, equality exactly on its face
    for k, (n, d, i, sd) in facets.items():
        on = [j for j, v in enumerate(Vp) if not (dot(n, v) - d)]
        assert all(F.sign(dot(n, v) - d) <= 0 for v in Vp) and len(on) == sd, (k, len(on), sd)
    results = {}
    # the Coxeter elements of a path diagram: 4 orientations (s1 s3 commute)
    CW = {"s1 s2 s3": [0, 1, 2], "s3 s2 s1": [2, 1, 0], "s2 s1 s3 (s2 first, bipartite)": [1, 0, 2], "s1 s3 s2 (bipartite)": [0, 2, 1]}
    for cname, cw in CW.items():
        # c-sorting word of w0: greedy leftmost reduced subword of c^infinity
        word, A = [], I
        while length(A) < N:
            for s in cw:
                B = mmul(A, S[s])
                if length(B) > length(A): word.append(s); A = B
                if length(A) == N: break
        assert len(word) == N
        # commutation class
        cls = {tuple(word)}; fr = [tuple(word)]
        while fr:
            nf = []
            for w in fr:
                for p in range(len(w) - 1):
                    if M[w[p]][w[p+1]] == 2:
                        u = w[:p] + (w[p+1], w[p]) + w[p+2:]
                        if u not in cls: cls.add(u); nf.append(u)
            fr = nf
        sing = {}
        for w in cls:
            A = I
            sing[mk(A)] = A
            for s in w:
                A = mmul(A, S[s]); sing[mk(A)] = A
        singV = {keyV[vkey(F, apply(A, a))] for A in sing.values()}
        kept = set()
        for vi in singV: kept |= vfac[vi]
        removed = [k for k in facets if k not in kept]
        # vertices of the associahedron: triples of kept planes
        KP = [facets[k] for k in kept]
        Va = {}
        for p, q, r in itertools.combinations(range(len(KP)), 3):
            n1, d1 = KP[p][0], KP[p][1]; n2, d2 = KP[q][0], KP[q][1]; n3, d3 = KP[r][0], KP[r][1]
            det = dot(n1, cross(n2, n3))
            if not det: continue
            x = scal(F.one / det, vadd(vadd(scal(d1, cross(n2, n3)), scal(d2, cross(n3, n1))), scal(d3, cross(n1, n2))))
            if all(F.sign(dot(n, x) - d) <= 0 for n, d, _, _ in KP):
                Va.setdefault(vkey(F, x), x)
        Va = list(Va.values())
        common = sum(1 for v in Va if vkey(F, v) in keyV)
        pr(f"  c = {cname}: w0(c) = {''.join(str(perm[s]+1) for s in word)} (path labels {[x+1 for x in word]}), commutation class {len(cls)} words, "
           f"c-singletons {len(sing)}, kept facets {len(kept)}, removed {len(removed)}, associahedron vertices {len(Va)} (W-Catalan {CATALAN[typ]}), shared with the permutahedron {common}")
        assert len(Va) == CATALAN[typ] and len(kept) == 3 + N
        rem_by = {}; kept_by = {}
        for k in removed: s = facets[k][3]; rem_by[s] = rem_by.get(s, 0) + 1
        for k in kept: s = facets[k][3]; kept_by[s] = kept_by.get(s, 0) + 1
        # centre at the corner centroid; Vacuus via the enumeration's own analyse()
        n = len(Va)
        cen = tuple(sum((v[i] for v in Va), F.zero) / F.c(n) for i in range(3))
        Vc = [vsub(v, cen) for v in Va]
        res, faces = analyse(f"{typ} associahedron c={cname}", F, Vc, uniform=False, check_centre=True)
        fs = {}
        for f in faces: fs[len(f["verts"])] = fs.get(len(f["verts"]), 0) + 1
        # which removed facets: list by their (exact) normals, rounded for the reader
        rem_list = sorted([[facets[k][3]] + [round(float(F.val(x)), 6) for x in facets[k][0]] for k in removed])
        sym = symmetry(F, Vc)
        fair = fairness(F, Vc, faces, sym)
        dual = dual_check(F, Vc, faces, sym)
        dist = sorted(F.key(dot(vsub(p, q), vsub(p, q))) for p, q in itertools.combinations(Vc, 2))
        results[cname] = {"w0c": [perm[s] + 1 for s in word], "commutation_class": len(cls), "c_singletons": len(sing),
                          "kept_facets": len(kept), "kept_by_sides": kept_by, "removed_facets": len(removed), "removed_by_sides": rem_by,
                          "removed_normals": rem_list, "vertices": len(Va), "shared_vertices_with_perm": common,
                          "f_vector": [res["V"], res["E"], res["F"]], "faces_by_sides": fs,
                          "centroid": [str(F.val(x))[:20] for x in cen], "vacuus": {k: res[k] for k in res if not k.startswith("_")},
                          "symmetry": sym["summary"], "fair": fair, "dual": dual, "_distkey": str(hash(tuple(map(str, dist)))),
                          "_V": [fl(F, v) for v in Vc], "_faces": [f["verts"] for f in faces],
                          "_perm_V": [fl(F, vsub(v, cen)) for v in Vp],
                          "_perm_faces_removed": [face_of(F, Vp, facets[k]) for k in removed],
                          "_perm_faces_kept": [face_of(F, Vp, facets[k]) for k in kept]}
        pr(f"    f-vector {results[cname]['f_vector']} faces {fs}; kept by sides {kept_by}, removed by sides {rem_by}")
        pr(f"    Vacuus: {res['plates']} plates, kind {res['kind']}, centrally symmetric {res['centrally_symmetric']}, classes {res['plate_classes']}")
        pr(f"    symmetry {sym['summary']}; fair: {fair['verdict']}; dual: {dual['verdict']}")
    # isometry: compare distance invariants
    keys = {c: r["_distkey"] for c, r in results.items()}
    pr("  distance invariants (equal = candidates for isometric):", keys)
    out = {"type": typ, "permutahedron": name, "W": len(W), "mirrors": N, "coxeter_matrix": M, "perm_facets": len(facets),
           "results": results, "secs": round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(OUT, f"assoc-{typ}.json"), "w"), indent=1, default=str)
    pr(typ, "done", out["secs"], "s")

def face_of(F, Vp, fc):
    n, d, i, sd = fc
    idx = [j for j, v in enumerate(Vp) if not (dot(n, v) - d)]
    P = np.array([fl(F, Vp[j]) for j in idx]); cf = P.mean(0); nf = np.array(fl(F, n)); nf /= np.linalg.norm(nf)
    u = P[0] - cf; u /= np.linalg.norm(u); w = np.cross(nf, u)
    return [idx[j] for j in sorted(range(len(idx)), key=lambda j: np.arctan2((P[j]-cf) @ w, (P[j]-cf) @ u))]

def symmetry(F, V):
    """All orthogonal maps fixing the origin (= corner centroid) that permute V, exactly."""
    n = len(V); keys = {vkey(F, v): i for i, v in enumerate(V)}
    nr = [F.key(dot(v, v)) for v in V]
    # a basis among the vertices
    b = [0]
    for j in range(1, n):
        if len(b) == 1 and any(cross(V[b[0]], V[j])): b.append(j)
        elif len(b) == 2 and dot(V[j], cross(V[b[0]], V[b[1]])): b.append(j); break
    B = [V[i] for i in b]
    G = [[dot(B[i], B[j]) for j in range(3)] for i in range(3)]
    detB = dot(B[0], cross(B[1], B[2]))
    inv = [cross(B[1], B[2]), cross(B[2], B[0]), cross(B[0], B[1])]   # rows of B^-T * det
    mats = []
    for t in itertools.product(range(n), repeat=3):
        if any(nr[t[i]] != nr[b[i]] for i in range(3)): continue
        C = [V[i] for i in t]
        if any(F.key(dot(C[i], C[j])) != F.key(G[i][j]) for i in range(3) for j in range(i+1, 3)): continue
        # A with A B_i = C_i: A = sum_i C_i (x) inv_i / detB
        A = tuple(tuple(sum((C[i][r] * inv[i][s] for i in range(3)), F.zero) / detB for s in range(3)) for r in range(3))
        if all(vkey(F, apply(A, v)) in keys for v in V): mats.append(A)
    dets = [F.sign(A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1]) - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0]) + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])) for A in mats]
    rot = sum(1 for d in dets if d > 0)
    minus = any(all(A[i][j] == (-F.one if i == j else F.zero) for i in range(3) for j in range(3)) for A in mats)
    refl = [A for A, d in zip(mats, dets) if d < 0]
    # fixed space of the group: common kernel of A - I
    fixdim = 3 - np.linalg.matrix_rank(np.vstack([np.array([[float(F.val(A[i][j])) - (i == j) for j in range(3)] for i in range(3)]) for A in mats]), tol=1e-9)
    nmir = sum(1 for A in refl if np.linalg.matrix_rank(np.array([[float(F.val(A[i][j])) - (i == j) for j in range(3)] for i in range(3)]), tol=1e-9) == 1)
    summ = f"order {len(mats)} ({rot} rotations, {nmir} mirrors, central inversion {'yes' if minus else 'no'}), fixed space of dimension {fixdim}"
    return {"mats": mats, "summary": summ, "order": len(mats), "fixdim": int(fixdim)}

def orbits(F, V, faces, mats):
    keys = {vkey(F, v): i for i, v in enumerate(V)}
    fk = {frozenset(f["verts"]): i for i, f in enumerate(faces)}
    seen = [None] * len(faces); orb = []
    for i, f in enumerate(faces):
        if seen[i] is not None: continue
        o = set()
        for A in mats:
            img = frozenset(keys[vkey(F, apply(A, V[j]))] for j in f["verts"]); o.add(fk[img])
        for j in o: seen[j] = len(orb)
        orb.append(sorted(o))
    return orb

def solid_angle(P, O):
    """Solid angle of the planar convex polygon P (mp vectors) seen from O (Van Oosterom-Strackee, fan)."""
    tot = mp.mpf(0)
    Q = [[p[i] - O[i] for i in range(3)] for p in P]
    d3 = lambda x, y: x[0]*y[0] + x[1]*y[1] + x[2]*y[2]
    cr = lambda x, y: [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]
    nn = lambda x: mp.sqrt(d3(x, x))
    for k in range(1, len(Q) - 1):
        a, b, c = Q[0], Q[k], Q[k+1]
        num = abs(d3(a, cr(b, c)))
        den = nn(a)*nn(b)*nn(c) + d3(a, b)*nn(c) + d3(a, c)*nn(b) + d3(b, c)*nn(a)
        tot += 2 * mp.atan2(num, den)
    return tot

def volume_centroid(F, V, faces):
    vol = F.zero; c = [F.zero] * 3
    for f in faces:
        p = f["verts"]
        for k in range(1, len(p) - 1):
            A, B, C = V[p[0]], V[p[k]], V[p[k+1]]
            d = dot(A, cross(B, C))
            if F.sign(d) < 0: d = -d
            vol = vol + d
            for i in range(3): c[i] = c[i] + d * (A[i] + B[i] + C[i]) / F.c(4)
    return tuple(x / vol for x in c), vol / F.c(6)

def fairness(F, V, faces, sym):
    orb = orbits(F, V, faces, sym["mats"])
    G, vol = volume_centroid(F, V, faces)
    Om = tuple(mp.mpf(0) for _ in range(3)); Gm = tuple(F.val(x) for x in G)
    Vm = [[F.val(x) for x in v] for v in V]
    rows = []
    for o in orb:
        f = faces[o[0]]["verts"]; P = [Vm[j] for j in f]
        rows.append({"faces": len(o), "sides": len(f), "solid_angle_over_4pi_corner_centroid": mp.nstr(solid_angle(P, Om) / (4*mp.pi), 15),
                     "solid_angle_over_4pi_volume_centroid": mp.nstr(solid_angle(P, Gm) / (4*mp.pi), 15),
                     "fair_share": mp.nstr(mp.mpf(1) / len(faces), 15),
                     "_gap_vol": solid_angle(P, Gm) / (4*mp.pi) - mp.mpf(1) / len(faces)})
    gap = max(abs(r["_gap_vol"]) for r in rows)
    for r in rows: r.pop("_gap_vol")
    same_centre = all(not (x) for x in G)
    if len(orb) == 1: verdict = "face-transitive: fair by symmetry"
    else:
        verdict = (f"{len(orb)} face orbits; NOT fair: largest |solid angle/4pi - 1/{len(faces)}| about the volume centroid = {mp.nstr(gap, 6)} "
                   f"(60-digit evaluation; certified unequal, gap >> 1e-50)") if gap > mp.mpf(10)**-30 else f"{len(orb)} orbits, equal to 30 digits: CHECK EXACTLY"
    return {"face_orbits": len(orb), "orbits": rows, "volume_centroid_is_corner_centroid": same_centre,
            "volume": mp.nstr(F.val(vol), 15), "verdict": verdict}

def dual_check(F, V, faces, sym):
    """Polar about the corner centroid: one face per vertex of V; face orbits = vertex orbits of V under the symmetry group."""
    keys = {vkey(F, v): i for i, v in enumerate(V)}
    seen = {}; orb = []
    for i in range(len(V)):
        if i in seen: continue
        o = {keys[vkey(F, apply(A, V[i]))] for A in sym["mats"]}
        for j in o: seen[j] = len(orb)
        orb.append(sorted(o))
    # polar faces: for vertex v, the points n_f / d_f of the faces f at v, in cyclic order around v
    pol = []
    for i in range(len(V)):
        fs = [f for f in faces if i in f["verts"]]
        pts = [scal(F.one / f["d"], f["N"]) for f in fs]
        pol.append(pts)
    # volume centroid of the polar
    allp = {}
    for pts in pol:
        for p in pts: allp.setdefault(vkey(F, p), p)
    Pl = list(allp.values())
    resd, dfaces = analyse("polar", F, Pl, uniform=False, check_centre=False)
    G, vol = volume_centroid(F, Pl, dfaces)
    Pm = [[F.val(x) for x in p] for p in Pl]; Gm = tuple(F.val(x) for x in G)
    rows = []
    fkeyset = {}
    for fi, f in enumerate(dfaces): fkeyset[fi] = f
    # map each dual face to its vertex of V by the normal direction
    for o in orb:
        v = V[o[0]]
        # dual face whose normal is parallel to v
        f = [g for g in dfaces if not any(cross(g["N"], v))][0]
        P = [Pm[j] for j in f["verts"]]
        rows.append({"faces": len(o), "sides": len(f["verts"]),
                     "solid_angle_over_4pi_volume_centroid": mp.nstr(solid_angle(P, Gm) / (4*mp.pi), 15),
                     "_g": solid_angle(P, Gm) / (4*mp.pi) - mp.mpf(1) / len(V)})
    gap = max(abs(r["_g"]) for r in rows)
    for r in rows: r.pop("_g")
    if len(orb) == 1: verdict = "face-transitive: fair by symmetry"
    else:
        verdict = (f"{len(V)} faces in {len(orb)} orbits; NOT fair: largest |solid angle/4pi - 1/{len(V)}| = {mp.nstr(gap, 6)} (60 digits)"
                   if gap > mp.mpf(10)**-30 else f"{len(orb)} orbits, equal to 30 digits: CHECK EXACTLY")
    return {"faces": len(V), "face_orbits": len(orb), "orbits": rows, "f_vector": [resd["V"], resd["E"], resd["F"]], "verdict": verdict}

if __name__ == "__main__":
    done = 0
    for typ in (sys.argv[1:] or ["A3", "B3", "H3"]):
        run(typ); done += 1      # run() asserts every check (Catalan count, n + N facets, exact face checks)
    print("FINAL ok" if done == len(sys.argv[1:] or ["A3", "B3", "H3"]) else "FINAL FAIL")
