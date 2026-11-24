"""The stellation cycle (DICTO, 25 Nov 2026), exact in Q(sqrt5). -> data/cycle.json, printed log.
Frame (as the Aequi frame): icosahedron I0 = cyclic (0, +-phi, +-1) (Pacioli's three golden rectangles, 2 x 2phi), dodecahedron
D0 = (+-1, +-1, +-1) and cyclic (0, +-1/phi, +-phi). I0 and D0 share the midsphere (radius phi) and are polar in it:
I0 = {x : w.x <= phi^2 for w in D0}, D0 = {x : n.x <= phi^2 for n in I0} (checked below)."""
import json, os, sys, time, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from q5 import Q, PHI, IPHI, phipow, log_phi_exact, dot, cross, vsub, vadd, vsc, iszero, vkey, pkey, solve3, cyclic_signs
from arrangement import Arrangement

T0 = time.time(); LOG = []; RES = {}
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

P2 = PHI * PHI
I0 = cyclic_signs([(0, PHI, 1)]); D0 = cyclic_signs([(1, 1, 1), (0, IPHI, PHI)])
assert len(I0) == 12 and len(D0) == 20
def scaled(V, k): f = phipow(k); return [vsc(f, v) for v in V]
def setkey(V): return frozenset(vkey(v) for v in V)
def r2(v): return dot(v, v)

# axes: 5-fold = I0 corners, 3-fold = D0 corners, 2-fold = I0 edge midpoints
A5 = {pkey(v) for v in I0}; A3 = {pkey(v) for v in D0}
e2I = min((r2(vsub(a, b)) for a, b in itertools.combinations(I0, 2)), key=lambda q: q.f())
EI = [(a, b) for a, b in itertools.combinations(I0, 2) if r2(vsub(a, b)) == e2I]
A2 = {pkey(vadd(a, b)) for a, b in EI}
assert (len(A5), len(A3), len(A2), len(EI)) == (6, 10, 15, 30)
def axis(v):
    k = pkey(v)
    return "5" if k in A5 else "3" if k in A3 else "2" if k in A2 else "other"
MIRRORS = A2                       # an Ih mirror is the plane at right angles to a 2-fold axis

def is_mirror(n, V):
    keys = setkey(V); nn = dot(n, n)
    return all(vkey(vsub(p, vsc(dot(n, p) / nn * 2, n))) in keys for p in V)
assert all(is_mirror(tuple(Q(Fr(a), Fr(b)) for a, b in k), I0) for k in A2), "the 15 planes at right angles to 2-fold axes are mirrors"

# polarity and midsphere
assert all(dot(w, v) <= P2 for w in D0 for v in I0)
assert all(sum(1 for v in I0 if dot(w, v) == P2) == 3 for w in D0)       # each D0 corner gives one face plane of I0 (3 corners)
assert all(sum(1 for w in D0 if dot(w, v) == P2) == 5 for v in I0)       # each I0 corner gives one face plane of D0 (5 corners)
e2D = min((r2(vsub(a, b)) for a, b in itertools.combinations(D0, 2)), key=lambda q: q.f())
ED = [(a, b) for a, b in itertools.combinations(D0, 2) if r2(vsub(a, b)) == e2D]
mid_I = {r2(vsc(Q(Fr(1, 2)), vadd(a, b))) for a, b in EI}; mid_D = {r2(vsc(Q(Fr(1, 2)), vadd(a, b))) for a, b in ED}
assert mid_I == mid_D == {P2}
say("frame: I0 edge^2", e2I, "D0 edge^2", e2D, "| midsphere^2 of both", P2, "| circumradius^2 I0", r2(I0[0]), "D0", r2(D0[0]))
rI2 = P2 * P2 / 3                  # inradius^2 of I0: face plane w.x = phi^2 with |w|^2 = 3
rD2 = P2 * P2 / r2(I0[0])          # inradius^2 of D0: face plane n.x = phi^2 with |n|^2 = phi + 2
RES["frame"] = dict(I0_edge2=repr(e2I), D0_edge2=repr(e2D), midsphere2=repr(P2), I0_circum2=repr(r2(I0[0])), D0_circum2=repr(r2(D0[0])),
                    I0_in2=repr(rI2), D0_in2=repr(rD2))

def ident(V):
    """name V as phi^k I0 or phi^k D0 (exact set equality), else None"""
    s = setkey(V)
    for k in range(-9, 10):
        if s == setkey(scaled(I0, k)): return f"phi^{k} I0"
        if s == setkey(scaled(D0, k)): return f"phi^{k} D0"
    return None

# ---------- 1. stellation points: every triple of face planes ----------
def triple_points(normals, d):
    pts = {}
    for a, b, c in itertools.combinations(normals, 3):
        x = solve3(a, d, b, d, c, d)
        if x is not None: pts[vkey(x)] = x
    shells = {}
    for x in pts.values():
        shells.setdefault((r2(x).key(), axis(x)), []).append(x)
    return shells
for nm, normals in (("D0 planes", I0), ("I0 planes", D0)):
    sh = triple_points(normals, P2)
    rows = []
    for (rk, ax), V in sorted(sh.items(), key=lambda kv: Q(*kv[0][0]).f()):
        rows.append(dict(radius2=repr(Q(*rk)), axis=ax, count=len(V), is_=ident(V)))
    RES["triple_points " + nm] = rows
    say("triple points of", nm, ":", "; ".join(f"r^2={r['radius2']} axis {r['axis']} x{r['count']} {r['is_'] or ''}" for r in rows))

# ---------- 2. the four Kepler-Poinsot stars as face complexes (true edges) ----------
def star(name, planes_normals, V, long_edges):
    """faces = corners of V on each face plane n.x = phi^2; star polygon sides = the longest (pentagram) or shortest pairs"""
    faces = []
    for n in planes_normals:
        F = [v for v in V if dot(n, v) == P2]
        faces.append((n, F))
    k = {len(F) for n, F in faces}; assert len(k) == 1, (name, k)
    E = set()
    for n, F in faces:
        ds = sorted({r2(vsub(a, b)).key() for a, b in itertools.combinations(F, 2)}, key=lambda q: Q(*q).f())
        want = ds[-1] if long_edges else ds[0]
        for a, b in itertools.combinations(F, 2):
            if r2(vsub(a, b)).key() == want: E.add(frozenset((vkey(a), vkey(b))))
    # each edge in exactly two faces
    for e in E:
        a, b = [tuple(Q(*c) for c in x) for x in e]
        cnt = sum(1 for n, F in faces if dot(n, a) == P2 and dot(n, b) == P2)
        assert cnt == 2, (name, cnt)
    deg = {}
    for e in E:
        for x in e: deg[x] = deg.get(x, 0) + 1
    vac = {}
    for e in E:
        a, b = [tuple(Q(*c) for c in x) for x in e]
        c = cross(a, b); assert not iszero(c)
        vac[pkey(c)] = c
    res = {pkey(n) for n, F in faces}
    out = dict(V=len(V), E=len(E), F=len(faces), euler=len(V) - len(E) + len(faces), face_corners=k.pop(), vertex_degree=sorted(set(deg.values())),
               vertices_are=ident(V), edge2=repr(Q(*next(iter({r2(vsub(*[tuple(Q(*c) for c in x) for x in e])).key() for e in E})))),
               vacuus_planes=len(vac), vacuus_all_Ih_mirrors=all(k in MIRRORS for k in vac), vacuus_equals_15_mirrors=set(vac) == MIRRORS,
               resonus_planes=len(res), resonus_axes=sorted({axis(tuple(Q(*c) for c in k)) for k in res}),
               resonus_equals_core=(res == {pkey(n) for n in planes_normals}))
    say(name, json.dumps(out)); RES["star " + name] = out
star("small stellated dodecahedron {5/2,5} on D0", I0, scaled(I0, 1), True)
star("great dodecahedron {5,5/2} on D0", I0, scaled(I0, 1), False)
star("great stellated dodecahedron {5/2,3} on D0", I0, scaled(D0, 3), True)
star("great icosahedron {3,5/2} on I0", D0, scaled(I0, 3), False)
# the cores themselves
star("dodecahedron D0", I0, D0, False)
star("icosahedron I0", D0, I0, False)

# ---------- 3. the stars as filled polyhedra (visible surface), from the cells of D0's 12 face planes ----------
def nadj(a, b): return dot(a, b) == PHI          # neighbouring faces of D0 (normals = neighbouring corners of I0)
def dstell_member(kind, normals, cube=None):
    """membership in a stellation of the dodecahedron with face normals `normals` (input planes in this order).
    B = planes the point lies beyond. core: B empty; pyramid |B| = 1; wedge B = 2 neighbours; spike B = 3 mutual neighbours."""
    def member(sg):
        B = [i for i in range(len(normals)) if sg(i) > 0]
        if len(B) == 0: return True
        if len(B) == 1: return kind in ("ssd", "gd", "gsd", "dogstar")
        if len(B) == 2:
            if not nadj(normals[B[0]], normals[B[1]]): return False
            if kind in ("gd", "gsd"): return True
            if kind == "dogstar":
                s = vadd(normals[B[0]], normals[B[1]])
                return sum(1 for x in s if x.sign() == 0) != 2           # leave out the 6 wedges on the cube axes
            return False
        if len(B) == 3:
            a, b, c = [normals[i] for i in B]
            if not (nadj(a, b) and nadj(b, c) and nadj(a, c)): return False
            if kind == "gsd": return True
            if kind == "dogstar":
                s = vadd(vadd(a, b), c)
                return all(x.sign() != 0 for x in s) and abs(s[0].f()) - abs(s[1].f()) < 1e-9 and abs(s[1].f()) - abs(s[2].f()) < 1e-9 and \
                    s[0] * s[0] == s[1] * s[1] == s[2] * s[2]                 # the 8 spikes whose tips are the cube corners
            return False
        return False
    return member

def surface_report(name, planes, member, keep=None, sym_vertices=None):
    t = time.time()
    A = Arrangement(planes); pieces = A.edges(member, keep)
    # split into edges at vertices; vertices = piece ends met by >= 2 lines or ending a run
    ends = {}
    for lk, p, u, t0, t1, fp in pieces:
        for tt, side in ((t0, 0), (t1, 1)):
            x = vadd(p, vsc(tt, u)); ends.setdefault(vkey(x), [x, set(), []])[1].add(lk); ends[vkey(x)][2].append((lk, side))
    verts = {}
    for k, (x, lines, inc) in ends.items():
        if len(lines) >= 2 or len(inc) == 1: verts[k] = x
    nE = sum(1 for lk, p, u, t0, t1, fp in pieces if vkey(vadd(p, vsc(t0, u))) in verts) if pieces else 0
    vac = {}
    through_O = 0
    for lk, p, u, t0, t1, fp in pieces:
        c = cross(p, u)
        if iszero(c): through_O += 1; continue
        vac[pkey(c)] = c
    res = {}
    for lk, p, u, t0, t1, fp in pieces:
        for k in fp: res[pkey(A.P[k][0])] = A.P[k][0]
    shells = {}
    for x in verts.values(): shells.setdefault((r2(x).key(), axis(x)), []).append(x)
    vshell = [dict(radius2=repr(Q(*rk)), axis=ax, count=len(V), is_=ident(V)) for (rk, ax), V in sorted(shells.items(), key=lambda kv: Q(*kv[0][0]).f())]
    SV = sym_vertices if sym_vertices is not None else list(verts.values())
    own = [k for k, n in vac.items() if is_mirror(n, SV)]
    out = dict(pieces=len(pieces), vertices=len(verts), edges=nE, vertex_shells=vshell,
               vacuus_planes=len(vac), vacuus_lines_through_O=through_O, vacuus_in_Ih_mirrors=sum(1 for k in vac if k in MIRRORS),
               vacuus_equals_15_mirrors=set(vac) == MIRRORS, vacuus_planes_that_are_own_mirrors=len(own),
               vacuus_other_axes=sorted({axis(n) for k, n in vac.items() if k not in MIRRORS}),
               resonus_planes=len(res), resonus_axes=sorted({axis(n) for n in res.values()}), seconds=round(time.time() - t, 1))
    say(name, json.dumps(out)); RES["surface " + name] = out
    return out, verts, pieces

Dpl = [(n, P2) for n in I0]
surface_report("dodecahedron D0 (check)", Dpl, dstell_member("core", I0))
surface_report("small stellated dodecahedron, visible surface", Dpl, dstell_member("ssd", I0))
surface_report("great dodecahedron, visible surface", Dpl, dstell_member("gd", I0))
surface_report("great stellated dodecahedron, visible surface", Dpl, dstell_member("gsd", I0))

# ---------- 4. the Dogstar (Hart's stellation 8): core = phi^-3 D0, cell cube [-1, 1]^3 ----------
dcore = P2 * phipow(-3)                          # face planes n.x = phi^2 phi^-3 = 1/phi
Cpl = [(n, dcore) for n in I0]
dog, dogV, dogP = surface_report("Dogstar (cells: core, 12 pyramids, 24 wedges, 8 spikes)", Cpl, dstell_member("dogstar", I0))
# cross-check: the cube [-1,1]^3 minus the six neighbouring dodecahedra D0 + 2e (Hart's tiling)
E3 = [(Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1))]
cubepl = [(e, Q(1)) for e in E3] + [(vsc(Q(-1), e), Q(1)) for e in E3]
centres = [vsc(Q(2), e) for e in E3] + [vsc(Q(-2), e) for e in E3]
nbpl = [(n, P2 + dot(n, c)) for c in centres for n in I0]
def csg_member(sg):
    if any(sg(12 + i) > 0 for i in range(6)): return False                       # outside the cube
    for c in range(6):
        if all(sg(18 + 12 * c + i) < 0 for i in range(12)): return False         # strictly inside a neighbour dodecahedron
    return True
def in_cube(m): return all(abs(x.f()) <= 1 + 1e-9 for x in m)
dog2, dogV2, dogP2 = surface_report("Dogstar as cube minus six roofs (cross-check)", Cpl + cubepl + nbpl, csg_member, keep=in_cube)
same = setkey(dogV.values()) == setkey(dogV2.values())
say("Dogstar: the two constructions have the same corners:", same); RES["dogstar_cross_check_same_corners"] = same
assert same and dog["vacuus_planes"] == dog2["vacuus_planes"]

# ---------- 5. the Sunstar: D0 with the Dogstars of its six face-neighbour cells (centres +-2e) ----------
Spl = list(Dpl)
for c in centres: Spl += [(n, dcore + dot(n, c)) for n in I0]
dogm = dstell_member("dogstar", I0)
def sun_member(sg):
    if all(sg(i) < 0 for i in range(12)): return True
    for c in range(6):
        if dogm(lambda i, c=c: sg(12 + 12 * c + i)): return True
    return False
def near(m): return r2(m).f() <= 11 + 1e-9                                       # Dogstar tips reach (3, 1, 1): radius^2 11
surface_report("Sunstar (D0 + six Dogstars)", Spl, sun_member, keep=near)

# ---------- 6. the great icosahedron's kernel and scale steps ----------
steps = [("I0", ident(I0)), ("D0", ident(D0))]
RES["scale_ladder"] = dict(
    ssd_and_gd_of_Dk_vertices="phi^(k+1) I0", gsd_of_Dk_vertices="phi^(k+3) D0", gi_of_Ik_vertices="phi^(k+3) I0",
    note="I_k = phi^k I0 and D_k = phi^k D0 share the midsphere phi^(k+1); see the stars above (k = 0) and scale invariance")

# ---------- 7. the H3 permutahedron (uniform truncated icosidodecahedron, edge 2/phi; coordinates as study 2026-11-24-permutahedron-leads) ----------
ip = IPHI
TID = cyclic_signs([(ip, ip, 3 + PHI), (2 * ip, PHI, 1 + 2 * PHI), (ip, PHI + 1, 3 * PHI - 1), (2 * PHI - 1, Q(2), 2 + PHI), (PHI, Q(3), 2 * PHI)])
assert len(TID) == 120
def support(V, n):
    h = max((dot(n, v) for v in V), key=lambda q: q.f()); h = max([dot(n, v) for v in V if (dot(n, v) - h).f() > -1e-9])
    return h, [v for v in V if dot(n, v) == h]
n5 = I0[0]
if len(support(TID, n5)[1]) != 10:
    TID = [(v[1], v[0], v[2]) for v in TID]                                       # the other Ih frame: swap x, y
    say("H3 permutahedron: coordinates swapped x <-> y to match the frame")
axes_all = {"5": [tuple(Q(*c) for c in k) for k in A5], "3": [tuple(Q(*c) for c in k) for k in A3], "2": [tuple(Q(*c) for c in k) for k in A2]}
faces = []; depth2 = {}
for t, AX in axes_all.items():
    for a in AX:
        for s in (1, -1):
            n = vsc(Q(s), a); h, F = support(TID, n); faces.append((n, h, F))
            depth2.setdefault(t, set()).add((h * h / dot(n, n)).key())
assert len(faces) == 62 and sorted(len(F) for n, h, F in faces) == [4] * 30 + [6] * 20 + [10] * 12
e2T = min((r2(vsub(a, b)) for a, b in itertools.combinations(TID, 2)), key=lambda q: q.f())
ET = [(a, b) for a, b in itertools.combinations(TID, 2) if r2(vsub(a, b)) == e2T]
assert len(ET) == 180
for a, b in ET:
    assert sum(1 for n, h, F in faces if dot(n, a) == h and dot(n, b) == h) == 2
assert all(len(v) == 1 for v in depth2.values())
d2 = {t: Q(*next(iter(v))) for t, v in depth2.items()}
res31 = {pkey(n) for n, h, F in faces}
assert res31 == (A5 | A3 | A2) and len(res31) == 31
R2T = r2(TID[0]); assert all(r2(v) == R2T for v in TID)
def ratio_report(x2):
    k = None
    for j in range(-12, 13):
        if x2 == phipow(j): k = j
    return dict(square_ratio=repr(x2), approx=round(x2.f() ** 0.5, 9), ratio_is_phi_power=(None if k is None else f"phi^{Fr(k, 2)}"))
H = dict(edge2=repr(e2T), circumradius2=repr(R2T), square_depth2=repr(d2["2"]), hexagon_depth2=repr(d2["3"]), decagon_depth2=repr(d2["5"]),
         resonus_31_is_union=True,
         decagon_depth_over_D0_inradius=ratio_report(d2["5"] / rD2), hexagon_depth_over_I0_inradius=ratio_report(d2["3"] / rI2),
         square_depth_over_midsphere=ratio_report(d2["2"] / P2), circumradius_over_I0=ratio_report(R2T / r2(I0[0])),
         circumradius_over_D0=ratio_report(R2T / r2(D0[0])),
         hexagon_over_decagon_depth=ratio_report(d2["3"] / d2["5"]), I0_in_over_D0_in=ratio_report(rI2 / rD2))
say("H3 permutahedron:", json.dumps(H)); RES["H3_permutahedron"] = H
# which cycle polyhedra nest exactly in it at a phi-power scale: least scale s with X inside the permutahedron, as s^2
def least_scale2(X, faces):
    best = None
    for v in X:
        for n, h, F in faces:
            q = dot(n, v) / h
            if best is None or q > best: best = q
    return best
nest = {}
for nm, X in (("I0", I0), ("D0", D0), ("ID0 (I0 edge midpoints)", [vsc(Q(Fr(1, 2)), vadd(a, b)) for a, b in EI])):
    s = least_scale2(X, faces)       # X * s touches the permutahedron from inside  <=> X inside (1/s) permutahedron
    k = log_phi_exact(s)
    nest[nm] = dict(scale_of_X_inside_permutahedron=repr(Q(1) / s), approx=round(1 / s.f(), 9), phi_power=(None if k is None else f"phi^{-k}"))
say("least-scale nestings in the H3 permutahedron:", json.dumps(nest)); RES["H3_nestings"] = nest

# ---------- 8. the earlier cycles: exact numbers ----------
G = {}
w0 = D0[0]; nb = [w for w in D0 if r2(vsub(w, w0)) == e2D]
tip_ratio = r2(w0) / dot(nb[0], w0)               # first stellation of I0: tip radius / face distance = |w0|^2 / (w . w0)
G["first_stellation_of_I_tip_over_face_distance"] = repr(tip_ratio) + " (squared: " + repr(tip_ratio * tip_ratio) + ")"
G["first_stellation_is_3_over_sqrt5"] = (tip_ratio * tip_ratio == Q(Fr(9, 5)))
G["R(phi^2 D0) over r(I0), squared"] = repr(r2(D0[0]) * phipow(4) / rI2)
G["three_times_I0_inradius_is_phi^2_D0_circumradius"] = (r2(D0[0]) * phipow(4) == 9 * rI2)
G["(R(D0)/r(I0))^2"] = repr(r2(D0[0]) / rI2)
G["equals_9_over_phi^4"] = (r2(D0[0]) / rI2 == 9 / phipow(4))
# lemma for every stellation: the plane through O and the line {n_i.x = d, n_j.x = d} is (n_i - n_j).x = 0
lem = {}
for nm, N in (("D0 planes (normals I0)", I0), ("I0 planes (normals D0)", D0)):
    cls = {}
    for a, b in itertools.combinations(N, 2):
        if iszero(vadd(a, b)): continue
        c = r2(vsub(a, b)).key(); cls.setdefault(c, set()).add(axis(vsub(a, b)))
    lem[nm] = {repr(Q(*c)): sorted(v) for c, v in sorted(cls.items(), key=lambda kv: Q(*kv[0]).f())}
say("pair classes of face normals (squared distance -> axis of n_i - n_j):", json.dumps(lem)); RES["stellation_lemma"] = lem
say("earlier-cycle numbers:", json.dumps(G)); RES["earlier_cycles"] = G

RES["seconds"] = round(time.time() - T0, 1)
os.makedirs(os.path.join(HERE, "../data"), exist_ok=True)
json.dump(RES, open(os.path.join(HERE, "../data/cycle.json"), "w"), indent=1)
open(os.path.join(HERE, "../data/cycle.log"), "w").write("\n".join(LOG) + "\n")
print("FINAL ok" if all([same]) else "FINAL check failed", RES["seconds"], "s")
