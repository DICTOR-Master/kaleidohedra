"""Harmony tests for the stellation-cycle arrangements and DICTO's root forms (CLEO, AXE, FUJI, Cleo-Icos, Antonius), exact in
Q(sqrt5), in the frame of study 2026-11-25-stellation-cycle: I0 = cyclic (0, +-phi, +-1), D0 = (+-1, +-1, +-1) and cyclic
(0, +-1/phi, +-phi).

Arrangements of the cycle (from that study, Theorems 4-6): the 15 mirror planes M15 (the Vacuus of I0, D0, the four
Kepler-Poinsot stars and the Dogstar); R6 (planes at right angles to the 6 five-fold axes: Resonus of D0, its stars, the
Dogstar, the Sunstar); R10 (at right angles to the 10 three-fold axes: Resonus of I0 and the great icosahedron); the hub H31 =
M15 + R6 + R10 (Resonus of the H3 permutahedron); the Sunstar's Vacuus S69, recomputed here with that study's own code
(cycle.py executed up to its section 6, then the Sunstar surface rebuilt and its 69 plates read off).

Root forms. CLEO (Mosseri-Sadoc t4 scaled by 1/tau), AXE (t6 scaled by 1/tau) and FUJI: corners from study
2026-10-14-axe-cleo-fuji (nets/pieces.json, copied to inputs/), identified exactly as (a + b phi)/2 and scaled by 2/phi into this
frame (their dodecahedron becomes D0). Cleo-Icos: O and one face of I0 (the icosahedron's face pyramid; Mackay's unit
tetrahedron). Antonius: the middle of the golden rhombohedron spanned by the corners a, b, c of that face (golden rhombohedron =
Cleo-Icos + Antonius + Cleo-Icos, as the app's definition says): corners a, b, c, a+b, b+c, c+a; its shape is checked against the
app's floats. Faces and edges come from an exact hull. Vacuus about the corner centroid and the volume centroid; Resonus.
For each: the harmony tests, whether each plate is one of the 31 hub planes (as a direction), and where each corner sits on the
phi-ladder (I_k = phi^k I0, D_k = phi^k D0, -8 <= k <= 8)."""
import os, sys, json, itertools, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from nf import NF
from harmony import analyse, canon, vkey, cross, dot, dedupe
SC = os.path.normpath(os.path.join(HERE, "../../2026-11-25-stellation-cycle/scripts"))

F = NF([-5, 0, 1], "2.2360679774997896964091736687312762354406183596115")
s5 = F.gen(); o = F.one; z = F.zero
phi = (s5 + 1) / 2; ip = phi - 1
LOG = []
def say(*a):
    t = " ".join(str(x) for x in a); print(t, flush=True); LOG.append(t)


def cyc_signs(pts):
    out = {}
    for p in pts:
        for sg in itertools.product((1, -1), repeat=3):
            q = tuple(F.c(0) + c * sgn if not isinstance(c, int) else F.c(c * sgn) for c, sgn in zip(p, sg))
            for r in (q, (q[2], q[0], q[1]), (q[1], q[2], q[0])):
                out[vkey(r)] = r
    return list(out.values())


I0 = cyc_signs([(z, phi, o)]); D0 = cyc_signs([(o, o, o), (z, ip, phi)])
assert len(I0) == 12 and len(D0) == 20
A5 = dedupe(I0); A3 = dedupe(D0)
mids = [tuple((a + b) / 2 for a, b in zip(p, q)) for p, q in itertools.combinations(I0, 2) if dot(*(tuple(x - y for x, y in zip(p, q)),) * 2) == 4]
A2 = dedupe(mids)
assert (len(A5), len(A3), len(A2)) == (6, 10, 15)
HUB = {vkey(canon(n)) for n in A5 + A3 + A2}
assert len(HUB) == 31
ARR = {"M15 (15 mirror planes)": A2, "R6 (5-fold Resonus)": A5, "R10 (3-fold Resonus)": A3, "H31 (the hub)": A5 + A3 + A2}

# ---------------------------------------------------------------- the Sunstar's Vacuus, with the stellation study's own code
def sunstar_plates():
    src = open(os.path.join(SC, "cycle.py")).read()
    src = src.split("# ---------- 6.")[0]
    g = {"__file__": os.path.join(SC, "cycle.py"), "__name__": "cycle_partial"}
    cwd = os.getcwd(); os.chdir(SC)
    exec(compile(src, os.path.join(SC, "cycle.py"), "exec"), g)
    os.chdir(cwd)
    out, verts, pieces = g["surface_report"]("Sunstar (again, for its plates)", g["Spl"], g["sun_member"], keep=g["near"])
    vac = {}
    for lk, p, u, t0, t1, fp in pieces:
        c = g["cross"](p, u)
        if g["iszero"](c): continue
        vac[g["pkey"](c)] = c
    assert len(vac) == 69 and out["vertices"] == 92 and out["edges"] == 150
    conv = lambda x: F.c(Fr(x.a)) + s5 * F.c(Fr(x.b))
    return [tuple(conv(x) for x in c) for c in vac.values()]


# ---------------------------------------------------------------- exact hull of a small point set
def hull(V):
    n = len(V); faces = {}
    for i, j, k in itertools.combinations(range(n), 3):
        nn = cross(tuple(a - b for a, b in zip(V[j], V[i])), tuple(a - b for a, b in zip(V[k], V[i])))
        if not any(nn): continue
        d = dot(nn, V[i])
        sg = [(dot(nn, V[m]) - d).sign() for m in range(n)]
        if all(x <= 0 for x in sg) or all(x >= 0 for x in sg):
            if any(x > 0 for x in sg): nn = tuple(-x for x in nn); d = -d
            key = vkey(canon(nn)) + (d / [x for x in nn if x][0]).key()
            faces[key] = (nn, d, frozenset(m for m in range(n) if sg[m] == 0))
    edges = set()
    for nn, d, on in faces.values():
        on = sorted(on)
        for a, b in itertools.combinations(on, 2):
            e = tuple(x - y for x, y in zip(V[b], V[a])); m = cross(nn, e)       # in-plane normal of the line ab
            sg = [dot(m, tuple(x - y for x, y in zip(V[c], V[a]))).sign() for c in on if c not in (a, b)]
            if all(x >= 0 for x in sg) or all(x <= 0 for x in sg): edges.add((a, b))
    fl = list(faces.values())
    assert len(V) - len(edges) + len(fl) == 2, "Euler"
    return fl, sorted(edges)


def centroids(V, faces):
    n = len(V)
    Oc = tuple(sum((v[i] for v in V), z) / n for i in range(3))
    vol = z; mom = [z, z, z]
    for nn, d, on in faces:
        on = sorted(on)
        # order the face's corners around its normal, then fan-triangulate from Oc
        c0 = tuple(sum((V[m][i] for m in on), z) / len(on) for i in range(3))
        e1 = tuple(a - b for a, b in zip(V[on[0]], c0)); e2 = cross(nn, e1)
        from flint import arb
        def ang(m):
            w = tuple(a - b for a, b in zip(V[m], c0)); x = dot(w, e1).ball(); y = dot(w, e2).ball()
            a = arb.atan2(y, x); return float(a.mid()) % 6.283185307179586 if m != on[0] else 0.0
        cyc = sorted(on, key=ang)
        for a, b in zip(cyc[1:-1], cyc[2:]):
            P = [V[cyc[0]], V[a], V[b]]
            u = [tuple(x - y for x, y in zip(p, Oc)) for p in P]
            v6 = dot(u[0], cross(u[1], u[2]))
            vol = vol + v6
            for i in range(3): mom[i] = mom[i] + v6 * (Oc[i] + P[0][i] + P[1][i] + P[2][i])
    Ov = tuple(m / (vol * 4) for m in mom)
    return Oc, Ov, vol / 6


def ladder(v):
    """station of a corner: 'I_k' / 'D_k' if v is a corner of phi^k I0 / phi^k D0 (-8 <= k <= 8), 'O' for the centre"""
    if not any(v): return "O"
    for k in range(-8, 9):
        f = o
        for _ in range(abs(k)): f = f * (phi if k > 0 else ip)
        w = tuple(x / f for x in v); kw = vkey(w)
        if kw in IK: return f"I_{k}"
        if kw in DK: return f"D_{k}"
    return "-"


IK = {vkey(v) for v in I0}; DK = {vkey(v) for v in D0}


def ident(x):
    """exact (a + b phi)/2, small integers, from a 9-digit float"""
    best = None
    for a in range(-12, 13):
        for b in range(-12, 13):
            val = (a + b * 1.6180339887498949) / 2
            if abs(val - x) < 2e-8:
                assert best is None, "ambiguous"
                best = (a, b)
    assert best is not None, f"no exact form for {x}"
    return (F.c(best[0]) + phi * best[1]) / 2


def root_forms():
    pcs = json.load(open(os.path.join(STUDY, "inputs/axe-cleo-fuji-pieces.json")))
    out = {}
    sc = 2 / phi
    for nm in ("CLEO", "AXE", "FUJI"):
        out[nm] = [tuple(ident(x) * sc for x in v) for v in pcs[nm]["vertices"]]
    # the pieces' dodecahedron is D0 after scaling (frame check)
    Dp = {vkey(tuple(ident(x) * sc for x in v)) for v in pcs["dodecahedron"]["vertices"]}
    assert Dp == DK, "pieces frame differs from the stellation frame"
    face = next(t for t in itertools.combinations(I0, 3) if all(dot(*(tuple(x - y for x, y in zip(p, q)),) * 2) == 4 for p, q in itertools.combinations(t, 2)))
    a, b, c = face
    out["Cleo-Icos"] = [(z, z, z), a, b, c]
    add = lambda p, q: tuple(x + y for x, y in zip(p, q))
    out["Antonius"] = [a, b, c, add(a, b), add(b, c), add(c, a)]
    # shape check of Antonius against the app's floats (k-mix cleo-sphere.js ANTONIUS): sorted squared edge ratios
    app = [[0.500000003144, -0.36180340115, 0.0], [0.223606799156, 0.36180340115, 0.447213598312], [0.223606799156, 0.36180340115, -0.447213598312],
           [-0.223606799156, -0.36180340115, 0.447213598312], [-0.500000003144, 0.36180340115, 0.0], [-0.223606799156, -0.36180340115, -0.447213598312]]
    d2 = lambda p, q: sum((x - y) ** 2 for x, y in zip(p, q))
    A = sorted(d2(p, q) for p, q in itertools.combinations(app, 2))
    Bv = [[float(x.ball().mid()) for x in v] for v in out["Antonius"]]
    B = sorted(d2(p, q) for p, q in itertools.combinations(Bv, 2))
    assert max(abs(x / A[0] - y / B[0]) for x, y in zip(A, B)) < 1e-6, "Antonius shape differs from the app's"
    return out


def plate_sets(V, O):
    fl, edges = hull(V)
    W = [tuple(x - y for x, y in zip(v, O)) for v in V]
    vac = dedupe([cross(W[a], W[b]) for a, b in edges])
    res = dedupe([nn for nn, d, on in fl])
    return vac, res, fl, edges


if __name__ == "__main__":
    t0 = time.time()
    RES = {"cycle": {}, "roots": {}}
    # positive controls for the exact area routine: H3 and the hub's 15 (reflection: all regions equal) via tracing
    from harmony import pencil_order
    say("control: region areas by tracing on M15 (H3):")
    o15 = analyse(F, A2, "M15")
    sp = o15["sphericus"]
    assert sp["area_values"] == 1 and sp["area_values_over_pi"] == ["1/30"] and sp["region_sides"] == {"3": 120}, "control failed"
    say("  120 regions, each pi/30: ok")
    S69 = sunstar_plates()
    ARR["S69 (Sunstar Vacuus)"] = S69
    for nm, N in ARR.items():
        r = analyse(F, N, nm)
        r["inside_hub"] = sum(1 for n in dedupe(N) if vkey(canon(n)) in HUB)
        RES["cycle"][nm] = r
        say(nm, json.dumps(r, default=str))
    forms = root_forms()
    for nm, V in forms.items():
        fl, edges = hull(V)
        Oc, Ov, vol = centroids(V, fl)
        rr = {"corners": len(V), "edges": len(edges), "faces": len(fl), "face_sizes": sorted(len(f[2]) for f in fl),
              "volume": str(abs(vol.ball()).mid())[:14], "centroids_equal": vkey(Oc) == vkey(Ov),
              "ladder": [ladder(v) for v in V]}
        for lab, O in (("corner centroid", Oc), ("volume centroid", Ov)):
            if lab == "volume centroid" and rr["centroids_equal"]: continue
            vac, res, _, _ = plate_sets(V, O)
            a = analyse(F, vac, f"{nm} Vacuus ({lab})")
            a["inside_hub"] = sum(1 for n in vac if vkey(canon(n)) in HUB)
            rr[f"vacuus ({lab})"] = a
            rr["resonus"] = analyse(F, res, f"{nm} Resonus")
            rr["resonus"]["inside_hub"] = sum(1 for n in res if vkey(canon(n)) in HUB)
        RES["roots"][nm] = rr
        say(nm, json.dumps(rr, default=str))
    json.dump(RES, open(os.path.join(STUDY, "data/stellation-roots.json"), "w"), indent=1, default=str)
    say("seconds", round(time.time() - t0, 1))
    print("FINAL ok stellation and root forms", flush=True)
