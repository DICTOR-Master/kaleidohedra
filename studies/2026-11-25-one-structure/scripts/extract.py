"""Skeleton data for Part B (one-structure study, 25 Nov 2026): exact corners, edges and faces of
- the 5 Platonic and 13 Archimedean polyhedra, built with the exact builders of study 2026-11-24-vacuus-resonus-catalogue
  (its scripts/catalogue.py, which reuses 2026-11-24-vacuus-enumeration), unchanged;
- the stellation-cycle polyhedra of study 2026-11-25-stellation-cycle: the four Kepler-Poinsot stars with their 30 true edges
  (the star() rule of cycle.py), the Dogstar and the Sunstar (visible-surface edge pieces from cycle.py's surface_report).
The H3 permutahedron (hub) is the truncated icosidodecahedron of the first list.
Writes data/skeletons.json: per polyhedron the field (minimal polynomial low -> high, real root), corners as coefficient
lists in the field generator, edges as index pairs (or as segments for surface pieces), faces as index lists when known."""
import os, sys, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
CAT = os.path.normpath(os.path.join(HERE, "../../2026-11-24-vacuus-resonus-catalogue"))
SC = os.path.normpath(os.path.join(HERE, "../../2026-11-25-stellation-cycle/scripts"))
sys.path.insert(0, os.path.join(CAT, "scripts"))
import catalogue as C
import sympy as sp
VX = C.VX


def field_of(F):
    if isinstance(F, C.NF):
        return {"g": [str(c) for c in F.g.coeffs()], "eta": F.eta_str}
    K = F.K
    return {"g": [str(c) for c in K.mod.to_list()][::-1], "eta": str(sp.N(K.ext.as_expr(), 120))}


def el(F, a):
    if isinstance(F, C.NF): return [str(c) for c in a.p.coeffs()] or ["0"]
    return [str(c) for c in a.to_list()][::-1] or ["0"]


def uniform(nm):
    F, gen, grp = C.S[nm]
    if nm == "snub dodecahedron":
        V = None
        for cand in gen:
            Vc = VX.build_set(F, cand)
            try:
                if len(Vc) == 60: VX.analyse("probe", F, Vc, True); V = Vc; break
            except AssertionError:
                pass
    else:
        V = VX.build_set(F, gen)
    r, faces = VX.analyse(nm, F, V, True)
    E = sorted({tuple(sorted((f["verts"][j], f["verts"][(j + 1) % len(f["verts"])]))) for f in faces for j in range(len(f["verts"]))})
    assert len(V) - len(E) + len(faces) == 2, nm
    return {"name": nm, "family": "Platonic" if nm in C.PLATONIC else "Archimedean", "group": grp, "field": field_of(F),
            "V": [[el(F, x) for x in v] for v in V], "E": E, "faces": [list(f["verts"]) for f in faces]}


def cycle_rows():
    src = open(os.path.join(SC, "cycle.py")).read().split("# ---------- 6.")[0]
    g = {"__file__": os.path.join(SC, "cycle.py"), "__name__": "cycle_partial"}
    cwd = os.getcwd(); os.chdir(SC)
    exec(compile(src, os.path.join(SC, "cycle.py"), "exec"), g)
    os.chdir(cwd)
    Q, dot, r2, vsub, vkey, scaled, I0, D0, P2 = (g[k] for k in ("Q", "dot", "r2", "vsub", "vkey", "scaled", "I0", "D0", "P2"))
    fld = {"g": ["-5", "0", "1"], "eta": "2.2360679774997896964091736687312762354406183596115"}
    cv = lambda x: [str(x.a), str(x.b)]
    rows = []

    def star(name, normals, V, long_edges):
        faces, E = [], set()
        for n in normals:
            Fc = [i for i, v in enumerate(V) if dot(n, v) == P2]
            faces.append(Fc)
            ds = sorted({r2(vsub(V[a], V[b])).key() for a, b in itertools.combinations(Fc, 2)}, key=lambda q: Q(*q).f())
            want = ds[-1] if long_edges else ds[0]
            for a, b in itertools.combinations(Fc, 2):
                if r2(vsub(V[a], V[b])).key() == want: E.add((a, b))
        assert len(E) == 30, (name, len(E))
        rows.append({"name": name, "family": "Kepler-Poinsot star", "group": "Ih", "field": fld,
                     "V": [[cv(x) for x in v] for v in V], "E": sorted(E), "faces": faces})
    star("small stellated dodecahedron", I0, scaled(I0, 1), True)
    star("great dodecahedron", I0, scaled(I0, 1), False)
    star("great stellated dodecahedron", I0, scaled(D0, 3), True)
    star("great icosahedron", D0, scaled(I0, 3), False)

    def surface(name, out, verts, pieces):
        vk = {}
        V = []
        for x in verts.values():
            vk[vkey(x)] = len(V); V.append(x)
        segs = []
        for lk, p, u, t0, t1, fp in pieces:
            a = g["vadd"](p, g["vsc"](t0, u)); b = g["vadd"](p, g["vsc"](t1, u))
            segs.append([[cv(x) for x in a], [cv(x) for x in b]])
        rows.append({"name": name, "family": "stellation cycle", "group": "Th", "field": fld, "V": [[cv(x) for x in v] for v in V],
                     "segments": segs, "check": {"vertices": out["vertices"], "edges": out["edges"]}})
    surface("Dogstar", g["dog"], g["dogV"], g["dogP"])
    out, verts, pieces = g["surface_report"]("Sunstar (for its skeleton)", g["Spl"], g["sun_member"], keep=g["near"])
    assert out["vertices"] == 92 and out["edges"] == 150
    surface("Sunstar", out, verts, pieces)
    return rows


if __name__ == "__main__":
    t0 = time.time()
    C.S = VX.uniform_solids()
    names = [n for n in C.S]
    rows = []
    for nm in names:
        C._SIGN.clear(); C._ALPHA.clear()
        rows.append(uniform(nm)); print(f"PROGRESS {len(rows) / (len(names) + 6):.2f} {nm} V={len(rows[-1]['V'])} E={len(rows[-1]['E'])}", flush=True)
    rows += cycle_rows()
    print("cycle rows:", [(r["name"], len(r["V"])) for r in rows[-6:]], flush=True)
    json.dump(rows, open(os.path.join(STUDY, "data/skeletons.json"), "w"))
    ok = len(rows) == 24 and sum(1 for r in rows if r["family"] in ("Platonic", "Archimedean")) == 18
    print(f"rows {len(rows)} in {time.time() - t0:.0f} s", flush=True)
    if ok: print("FINAL ok extract", flush=True)
