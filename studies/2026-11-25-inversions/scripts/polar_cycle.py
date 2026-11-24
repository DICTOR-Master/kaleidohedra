"""Items 2-4 of study 2026-11-25-inversions, exact in Q(sqrt5) (pure Python, q5.py).
(2) star-polyhedron polarity on the stellation cycle: which polyhedron is the polar, at which phi-scale; Vacuus, Resonus, corner planes.
(3) the faceting ladder (corners of I0 / D0 fixed): chord classes, plane classes, their Vacuus/Resonus axes; the compounds.
(4) sphere inversion about O: face spheres, edge circles, their crossings (Sphericus of the inverted bodies).
Prints FINAL ok only when every assert passed. Writes data/polar-cycle.json."""
import os, sys, json, itertools, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from q5 import Q, PHI, IPHI, phipow, log_phi_exact, dot, cross, vsub, vadd, vsc, det3, iszero, vkey, pkey, cyclic_signs
T0 = time.time(); RES = {}; LOG = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
P2 = PHI * PHI
I0 = cyclic_signs([(0, PHI, 1)]); D0 = cyclic_signs([(1, 1, 1), (0, IPHI, PHI)])
def r2(v): return dot(v, v)
A5 = {pkey(v) for v in I0}; A3 = {pkey(v) for v in D0}
e2I = min((r2(vsub(a, b)) for a, b in itertools.combinations(I0, 2)), key=lambda q: q.f())
A2 = {pkey(vadd(a, b)) for a, b in itertools.combinations(I0, 2) if r2(vsub(a, b)) == e2I}
assert (len(A5), len(A3), len(A2)) == (6, 10, 15)
def axis(v):
    k = pkey(v); return "5" if k in A5 else "3" if k in A3 else "2" if k in A2 else "other"

# ---------------- polyhedra as (vertices, planes (n, h): n.x = h, edges) ----------------
class Poly:
    def __init__(s, name, V, planes, E):
        s.name, s.V, s.planes, s.E = name, V, planes, E
    def key(s):
        return (frozenset(vkey(v) for v in s.V),
                frozenset(vkey(vsc(Q(1) / h, n)) for n, h in s.planes),
                frozenset(frozenset((vkey(a), vkey(b))) for a, b in s.E))
    def scaled(s, k, name=None):
        f = phipow(k)
        return Poly(name or s.name, [vsc(f, v) for v in s.V], [(n, h * f) for n, h in s.planes], [(vsc(f, a), vsc(f, b)) for a, b in s.E])

def build(name, normals, h, V, long_edges):
    planes = [(n, h) for n in normals]; E = {}
    for n, _ in planes:
        F = [v for v in V if dot(n, v) == h]
        ds = sorted({r2(vsub(a, b)) for a, b in itertools.combinations(F, 2)}, key=lambda q: q.f())
        want = ds[-1] if long_edges else ds[0]
        for a, b in itertools.combinations(F, 2):
            if r2(vsub(a, b)) == want: E[frozenset((vkey(a), vkey(b)))] = (a, b)
    E = list(E.values())
    for a, b in E: assert sum(1 for n, hh in planes if dot(n, a) == hh and dot(n, b) == hh) == 2, name
    return Poly(name, V, planes, E)

def sc(V, k): f = phipow(k); return [vsc(f, v) for v in V]
BASE = {   # at k = 0; X(k) = BASE[X].scaled(k)
    "I": build("icosahedron", D0, P2, I0, False),
    "D": build("dodecahedron", I0, P2, D0, False),
    "SSD": build("small stellated dodecahedron {5/2,5}", I0, P2, sc(I0, 1), True),
    "GD": build("great dodecahedron {5,5/2}", I0, P2, sc(I0, 1), False),
    "GSD": build("great stellated dodecahedron {5/2,3}", I0, P2, sc(D0, 3), True),
    "GI": build("great icosahedron {3,5/2}", D0, P2, sc(I0, 3), False)}
for X, P in BASE.items(): assert len(P.E) == 30, (X, len(P.E))
def ladder(X, k): return BASE[X].scaled(k, "%s(%d)" % (X, k))
KEYS = {}
for X in BASE:
    for k in range(-14, 15): KEYS[ladder(X, k).key()] = (X, k)
def ident(P): return KEYS.get(P.key())

def polar(P, R):
    """reciprocal in the sphere |x|^2 = R about O: plane n.x = h -> pole (R/h) n; corner v -> plane v.x = R; edge (F, G) -> (pole F, pole G)"""
    pole = lambda n, h: vsc(R / h, n)
    V = {vkey(pole(n, h)): pole(n, h) for n, h in P.planes}
    planes = [(v, R) for v in P.V]; E = []
    for a, b in P.E:
        F = [(n, h) for n, h in P.planes if dot(n, a) == h and dot(n, b) == h]; assert len(F) == 2
        E.append((pole(*F[0]), pole(*F[1])))
    return Poly("polar of " + P.name, list(V.values()), planes, E)

def vac(P): return {pkey(cross(a, b)) for a, b in P.E}            # plane through O and the edge: normal a x b
def res(P): return {pkey(n) for n, h in P.planes}
def cpl(P): return {pkey(v) for v in P.V}                          # corner planes: through O at right angles to a corner direction
def edir(P): return {pkey(vsub(b, a)) for a, b in P.E}
def axes(S): return sorted({axis(tuple(Q(*c) for c in k)) for k in S})
def midr2(P):
    s = set()
    for a, b in P.E:
        d = vsub(b, a); t = -dot(a, d) / dot(d, d); f = vadd(a, vsc(t, d)); s.add(r2(f))
    return s

# ---------------- (2) polarity on the cycle ----------------
FORM = {"I": ("D", -2), "D": ("I", -2), "SSD": ("GD", -3), "GD": ("SSD", -3), "GSD": ("GI", -5), "GI": ("GSD", -5)}   # X(k) -> Y(m + c - k)
rows = []
for m in range(-3, 6):
    R = phipow(m)
    for X in BASE:
        for k in range(-3, 4):
            P = ladder(X, k); Ps = polar(P, R); idn = ident(Ps)
            Y, c = FORM[X]; assert idn == (Y, m + c - k), (X, k, m, idn)
            assert vac(Ps) == edir(P) and vac(P) == edir(Ps), "Vacuus of the polar = planes at right angles to the edges"
            assert res(Ps) == cpl(P) and cpl(Ps) == res(P), "Resonus of the polar = corner planes"
            assert vac(Ps) == vac(P) == A2, "Vacuus kept: the 15 mirrors"
            assert ident(polar(Ps, R)) == (X, k), "involution"
    rows.append(m)
say("(2) formula X(k) -> Y(m+c-k) holds for all six members, k in -3..3, sphere radius^2 phi^m, m in", rows)
# the midsphere (proper reciprocal) of each member
mid = {}
for X in BASE:
    P = ladder(X, 0); s = midr2(P); assert len(s) == 1; R = s.pop(); m = log_phi_exact(R)
    Ps = polar(P, R); idn = ident(Ps)
    out = dict(member=BASE[X].name, midradius2=repr(R), midradius2_is_phi_power=m, polar_in_midsphere=idn,
               corner_scale_of_reciprocal=None, vacuus=len(vac(P)), resonus=len(res(P)), resonus_axes=axes(res(P)),
               corner_planes=len(cpl(P)), corner_axes=axes(cpl(P)), polar_resonus_axes=axes(res(Ps)), polar_corner_axes=axes(cpl(Ps)))
    assert m is not None
    # compare circumradii of the pair
    out["circumradius2_ratio_polar_over_member"] = repr(r2(Ps.V[0]) / r2(P.V[0]))
    lr = log_phi_exact(r2(Ps.V[0]) / r2(P.V[0])); out["circumradius_ratio_phi_power_x2"] = lr
    assert midr2(Ps) == {R}, "reciprocal pair shares the midsphere"
    mid[X] = out; say("(2) midsphere:", json.dumps(out, ensure_ascii=False))
RES["polarity_midsphere"] = mid
# off the ladder: radius^2 not a power of phi
R3 = Q(3); Ps = polar(ladder("I", 0), R3); assert ident(Ps) is None
f = r2(Ps.V[0]) / r2(ladder("D", 0).V[0]); say("(2) sphere radius^2 3: polar of I0 = c.D0 with c^2 =", f, "phi-power?", log_phi_exact(f))
RES["off_ladder_example"] = dict(R2="3", polar_of_I0_is="(3/phi^2) D0", on_ladder=False)
# a counterexample to 'Vacuus kept' outside the regular members: compound of five cubes (faceting of D0) and its polar
cubes = {}
for v in D0:
    nb = [w for w in D0 if r2(vsub(w, v)) == 4]
    for a, b, c in itertools.combinations(nb, 3):
        if all(r2(vsub(x, y)) == 8 for x, y in ((a, b), (b, c), (a, c))):
            ea, eb, ec = vsub(a, v), vsub(b, v), vsub(c, v)
            Cv = [vadd(v, vadd(vsc(i, ea), vadd(vsc(j, eb), vsc(l, ec)))) for i in (0, 1) for j in (0, 1) for l in (0, 1)]
            if all(vkey(x) in {vkey(y) for y in D0} for x in Cv): cubes[frozenset(vkey(x) for x in Cv)] = Cv
assert len(cubes) == 5
def cube_poly(Cv):
    cen = vsc(Q(Fr(1, 8)), [sum((x[i] for x in Cv), Q(0)) for i in range(3)]); assert iszero(cen)
    E = [(a, b) for a, b in itertools.combinations(Cv, 2) if r2(vsub(a, b)) == 4]
    planes = {}
    for a, b in E:
        n = vsub(b, a)            # face normals of a cube are its edge directions
        for s in (1, -1):
            nn = vsc(Q(s), n); h = max((dot(nn, x) for x in Cv), key=lambda q: q.f()); planes[vkey(vsc(Q(1) / h, nn))] = (nn, h)
    return Poly("cube", Cv, list(planes.values()), E)
comp = [cube_poly(Cv) for Cv in cubes.values()]
C5 = Poly("compound of five cubes", D0, [p for c in comp for p in c.planes], [e for c in comp for e in c.E])
O5 = Poly("compound of five octahedra", [], [], [])
O5parts = [polar(c, P2) for c in comp]
O5 = Poly("compound of five octahedra (polar of five cubes, sphere phi^2)", [v for p in O5parts for v in p.V], [p for q in O5parts for p in q.planes], [e for q in O5parts for e in q.E])
RES["compound_counterexample"] = dict(five_cubes=dict(vacuus=len(vac(C5)), vacuus_axes=axes(vac(C5)), resonus=len(res(C5)), resonus_axes=axes(res(C5))),
                                      five_octahedra=dict(vacuus=len(vac(O5)), vacuus_axes=axes(vac(O5)), resonus=len(res(O5)), resonus_axes=axes(res(O5)),
                                                          corners=len({vkey(v) for v in O5.V}), corner_axes=sorted({axis(v) for v in O5.V}), corner_radius2=sorted({repr(r2(v)) for v in O5.V})))
assert vac(O5) == edir(C5) and vac(C5) == edir(O5)
say("(2) five cubes vs five octahedra:", json.dumps(RES["compound_counterexample"], ensure_ascii=False))

# ---------------- (3) faceting ladder ----------------
def chord_classes(V, name):
    out = []
    cl = {}
    for a, b in itertools.combinations(V, 2):
        if iszero(vadd(a, b)): continue                         # antipodal chords pass through O: no Vacuus plate
        cl.setdefault(r2(vsub(a, b)), []).append((a, b))
    for L, prs in sorted(cl.items(), key=lambda kv: kv[0].f()):
        out.append(dict(chord2=repr(L), chords=len(prs), vacuus_axes=sorted({axis(cross(a, b)) for a, b in prs}),
                        vacuus_planes=len({pkey(cross(a, b)) for a, b in prs}), direction_axes=sorted({axis(vsub(a, b)) for a, b in prs})))
    return out
def plane_classes(V):
    pl = {}
    for a, b, c in itertools.combinations(V, 3):
        n = cross(vsub(b, a), vsub(c, a))
        if iszero(n): continue
        h = dot(n, a)
        if h.sign() == 0: continue                              # through O
        if h.sign() < 0: n, h = vsc(Q(-1), n), -h
        pl[vkey(vsc(Q(1) / h, n))] = (n, h)
    cls = {}
    for n, h in pl.values():
        on = sum(1 for v in V if dot(n, v) == h); d2 = h * h / r2(n)
        cls.setdefault((axis(n), d2, on), []).append(n)
    return [dict(axis=a, dist2=repr(d), corners_on_plane=o, planes=len(L)) for (a, d, o), L in sorted(cls.items(), key=lambda kv: (kv[0][1].f(), kv[0][0]))]
fac = dict(I0=dict(chords=chord_classes(I0, "I0"), planes=plane_classes(I0)), D0=dict(chords=chord_classes(D0, "D0"), planes=plane_classes(D0)))
RES["faceting_classes"] = fac
for k, v in fac.items():
    say("(3) facetings of", k, "chords:", json.dumps(v["chords"], ensure_ascii=False)); say("(3) facetings of", k, "planes:", json.dumps(v["planes"], ensure_ascii=False))
# the regular facetings with corners fixed, and their phi-scales (face planes as ladder planes)
regs = []
for X, Vk in (("SSD", "I"), ("GD", "I"), ("GI", "I"), ("GSD", "D")):
    for k in range(-2, 3):
        Vset = {vkey(v) for v in ladder(Vk, k).V}
        hits = [ (Y, j) for (Y, j) in [(X, j) for j in range(-12, 13)] if {vkey(v) for v in ladder(Y, j).V} == Vset]
        assert len(hits) == 1
        regs.append(dict(corners="%s_%d" % (Vk, k), faceting=X, as_stellation_of=("D_%d" if X != "GI" else "I_%d") % hits[0][1], step=hits[0][1] - k))
RES["faceting_ladder"] = regs
say("(3) faceting ladder:", sorted({(r["faceting"], r["step"]) for r in regs}))

# ---------------- (4) sphere inversion about O ----------------
def invert_report(P, R):
    """faces -> spheres through O: centre (R/2h) n = half the pole; edges -> circles through O in the Vacuus plate"""
    sph = []
    for n, h in P.planes:
        c = vsc(R / (2 * h), n); sph.append((c, r2(c)))
    pole_half = all(vkey(vsc(Q(2), c)) in {vkey(vsc(R / h, n)) for n, h in P.planes} for c, _ in sph)
    circ = {}
    for a, b in P.E:
        d = vsub(b, a); t = -dot(a, d) / dot(d, d); f = vadd(a, vsc(t, d))
        c = vsc(R / (2 * r2(f)), f)                              # circle centre; diameter from O to R f/|f|^2
        plane = pkey(cross(a, b)); circ[(plane, vkey(c))] = dict(c=c, d=d, a=a, b=b, plane=plane)
    # crossings other than O: images of the meeting points of edge lines
    pts = {}
    L = list(circ.values())
    for e1, e2 in itertools.combinations(L, 2):
        a1, d1, a2, d2 = e1["a"], e1["d"], e2["a"], e2["d"]
        nn = cross(d1, d2)
        if iszero(nn): continue                                  # parallel lines: circles kiss at O
        if det3(vsub(a2, a1), d1, d2).sign() != 0: continue      # skew: circles meet only at O
        # a1 + s d1 = a2 + t d2
        s = dot(cross(vsub(a2, a1), d2), nn) / dot(nn, nn)
        x = vadd(a1, vsc(s, d1)); t = dot(vsub(x, a2), d2) / dot(d2, d2)
        inside = (Q(0) <= s <= Q(1)) and (Q(0) <= t <= Q(1))
        y = vsc(R / r2(x), x); k = vkey(y)
        e = pts.setdefault(k, dict(y=y, circles=set(), at_vertex=any(vkey(x) == vkey(v) for v in P.V), arcs=set(), cos2=set()))
        e["circles"].update({id(e1), id(e2)})
        if inside: e["arcs"].update({id(e1), id(e2)})
        e["cos2"].add(dot(d1, d2) * dot(d1, d2) / (dot(d1, d1) * dot(d2, d2)))
    tang = {}
    for e in L: tang.setdefault(pkey(e["d"]), 0); tang[pkey(e["d"])] += 1
    mult = {}
    for p in pts.values():
        kk = ("vertex" if p["at_vertex"] else "other", len(p["circles"]), len(p["arcs"]))
        mult[kk] = mult.get(kk, 0) + 1
    dih = set()
    for (n1, h1), (n2, h2) in itertools.combinations(P.planes, 2):
        if any(dot(n1, a) == h1 and dot(n1, b) == h1 and dot(n2, a) == h2 and dot(n2, b) == h2 for a, b in P.E):
            cs = dot(n1, n2); dih.add((repr(cs * cs / (r2(n1) * r2(n2))), cs.sign()))
    return dict(R2=repr(R), face_spheres=len(sph), sphere_radius2=sorted({repr(x) for _, x in sph}), centres_are_half_poles=pole_half,
                tangent_planes_at_O_are_resonus=len({pkey(c) for c, _ in sph}) == len(res(P)),
                edge_circles=len(circ), circle_planes=len({e["plane"] for e in L}), circle_planes_are_vacuus={e["plane"] for e in L} == vac(P),
                circle_diameter2=sorted({repr(R * R / r2(vadd(e["a"], vsc(-dot(e["a"], e["d"]) / dot(e["d"], e["d"]), e["d"])))) for e in L}),
                tangent_lines_at_O=len(tang), circles_per_tangent_line=sorted(set(tang.values())),
                crossings_besides_O={"%s, %d circles, %d arcs" % k: v for k, v in sorted(mult.items())},
                crossing_angle_cos2=sorted({repr(c) for p in pts.values() for c in p["cos2"]}),
                face_sphere_angles_cos2_sign=sorted(dih))
CUBE = [(Q(a), Q(b), Q(c)) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
OCT = cyclic_signs([(1, 0, 0)])
cube = Poly("cube", CUBE, [(v, Q(1)) for v in OCT], [(a, b) for a, b in itertools.combinations(CUBE, 2) if r2(vsub(a, b)) == 4])
octa = Poly("octahedron", OCT, [(v, Q(1)) for v in CUBE], [(a, b) for a, b in itertools.combinations(OCT, 2) if r2(vsub(a, b)) == 2])
TET = [v for v in CUBE if (v[0] * v[1] * v[2]).sign() > 0]
tet = Poly("tetrahedron", TET, [(vsc(Q(-1), v), Q(1)) for v in TET], [(a, b) for a, b in itertools.combinations(TET, 2)])
INV = {}
for P in [tet, cube, octa, BASE["I"], BASE["D"], BASE["SSD"], BASE["GD"], BASE["GSD"], BASE["GI"]]:
    s = midr2(P); assert len(s) == 1; R = s.pop()
    rep = invert_report(P, R); rep["sphere"] = "midsphere"
    assert rep["centres_are_half_poles"] and rep["circle_planes_are_vacuus"] and rep["tangent_planes_at_O_are_resonus"]
    INV[P.name] = rep; say("(4)", P.name, json.dumps(rep, ensure_ascii=False))
RES["inversion"] = INV
# pedal check for the convex ones: radial function of the inverse = support function of the polar, at every corner direction
for P in [tet, cube, octa, BASE["I"], BASE["D"]]:
    R = midr2(P).pop(); Ps = polar(P, R)
    for v in P.V:
        img2 = (R / r2(v)) * (R / r2(v)) * r2(v)               # |inverse of v|^2
        hs = max((dot(p, v) for p in Ps.V), key=lambda q: q.f())  # support of the polar in direction v, times |v|
        assert hs * hs / r2(v) == img2
say("(4) pedal identity checked exactly at every corner direction of T, C, O, I, D")
RES["seconds"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "..", "data", "polar-cycle.json"), "w"), indent=1, ensure_ascii=False)
say("FINAL ok")
