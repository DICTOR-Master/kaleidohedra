"""Extract the exact Vacuus plates and Resonus planes (as normals) of the 163 catalogue polyhedra, reusing the builders of
study 2026-11-24-vacuus-resonus-catalogue unchanged (its scripts/catalogue.py, which reuses 2026-11-24-vacuus-enumeration).
Vacuus: one plane through O and each edge (normal V_a x V_b); Resonus: one plane through O parallel to each face (the face
normal). Johnson polyhedra: Vacuus about the corner centroid and about the volume centroid (the Resonus is the same).
The plane counts are checked against the catalogue table (data/catalogue-all.json there).
Writes data/catalogue-normals.json: field (minimal polynomial low -> high, real root) and normals as coefficient lists."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
CAT = os.path.normpath(os.path.join(HERE, "../../2026-11-24-vacuus-resonus-catalogue"))
sys.path.insert(0, os.path.join(CAT, "scripts"))
import catalogue as C
import multiprocessing as mpr
import sympy as sp

VX, JX = C.VX, C.JX


def field_of(F):
    if isinstance(F, C.NF):
        return {"g": [str(c) for c in F.g.coeffs()], "eta": F.eta_str}
    K = F.K
    mod = [str(c) for c in K.mod.to_list()][::-1]
    return {"g": mod, "eta": str(sp.N(K.ext.as_expr(), 120))}


def el(F, a):
    if isinstance(F, C.NF): return [str(c) for c in a.p.coeffs()] or ["0"]
    return [str(c) for c in a.to_list()][::-1] or ["0"]


def planes(F, V, faces):
    edges = sorted({(min(f["verts"][j], f["verts"][(j + 1) % len(f["verts"])]), max(f["verts"][j], f["verts"][(j + 1) % len(f["verts"])]))
                    for f in faces for j in range(len(f["verts"]))})
    vac = {}
    for a, b in edges:
        m = C.canon(F, C.cross(V[a], V[b])); vac.setdefault(C.vkey(F, m), m)
    res = {}
    for f in faces:
        m = C.canon(F, f["N"]); res.setdefault(C.vkey(F, m), m)
    return [[el(F, x) for x in m] for m in vac.values()], [[el(F, x) for x in m] for m in res.values()]


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
    D = VX.dual_vertices(F, faces)
    dn = {"cube": "octahedron (polar of the cube)", "octahedron": "cube (polar of the octahedron)", "tetrahedron": "tetrahedron (polar)",
          "dodecahedron": "icosahedron (polar of the dodecahedron)", "icosahedron": "dodecahedron (polar of the icosahedron)"}.get(nm, C.CATALAN.get(nm))
    r2, faces2 = VX.analyse(dn, F, D, False)
    out = []
    for name, VV, ff, fam in ((nm, V, faces, "Platonic" if nm in C.PLATONIC else "Archimedean"),
                              (dn, D, faces2, "Catalan" if nm in C.CATALAN else "Platonic polar")):
        v, rr = planes(F, VV, ff)
        out.append({"name": name, "family": fam, "field": field_of(F), "vacuus": v, "resonus": rr})
    return out


def prisms(n):
    F, pr, ap = VX.prism_family(n)
    out = []
    for nm, V0, fam, dn, dfam in ((f"{n}-gonal prism", pr, "prism", f"{n}-gonal bipyramid", "bipyramid"),
                                  (f"{n}-gonal antiprism", ap, "antiprism", f"{n}-gonal trapezohedron", "trapezohedron")):
        V = VX.build_set(F, V0)
        r, faces = VX.analyse(nm, F, V, True)
        D = VX.dual_vertices(F, faces)
        r2, faces2 = VX.analyse(dn, F, D, False)
        for name, VV, ff, fm in ((nm, V, faces, fam), (dn, D, faces2, dfam)):
            v, rr = planes(F, VV, ff)
            out.append({"name": name, "family": fm, "field": field_of(F), "vacuus": v, "resonus": rr})
    return out


def johnson(nm):
    F, V, recipe = C.johnson_solid(nm)
    Oc, Ov = JX.centroids(F, V)
    row = {"name": nm, "family": "Johnson", "field": field_of(F)}
    for lab, O in (("corner", Oc), ("volume", Ov)):
        W = [C.vsub(v, O) for v in V]
        r, faces = VX.analyse(nm, F, W, True, None, check_centre=False)
        v, rr = planes(F, W, faces)
        row["vacuus" if lab == "corner" else "vacuus_volume"] = v
        row["resonus"] = rr
    return [row]


def run(task):
    kind, arg = task
    t0 = time.time()
    C._SIGN.clear(); C._ALPHA.clear()   # these caches are keyed by id(field); a later field can reuse a freed id
    try:
        rows = {"uniform": uniform, "prism": prisms, "johnson": johnson}[kind](arg)
    except Exception as e:
        import traceback
        return {"task": task, "error": repr(e), "tb": traceback.format_exc()}
    return {"task": task, "rows": rows, "secs": round(time.time() - t0, 1)}


if __name__ == "__main__":
    procs = int(os.environ.get("PROCS", "8"))
    C.S = VX.uniform_solids()
    tasks = [("uniform", nm) for nm in C.S] + [("prism", n) for n in range(3, 13)]
    os.chdir(C.VE)
    for m in (3, 4, 5, 6, 8, 10): JX.axial(m)
    JX.prisms_augmented(); JX.gyrobifastigium(); JX.platonic_archimedean_based()
    JX.recognise("J91_BILUNABIROTUNDA", [sp.sqrt(5)], [sp.Integer(1), sp.sqrt(5)])
    JX.recognise("J92_TRIANGULAR_HEBESPHENOROTUNDA", [sp.sqrt(3), sp.sqrt(5)], [sp.Integer(1), sp.sqrt(3), sp.sqrt(5), sp.sqrt(15)])
    os.chdir(STUDY)
    C.J8X.update(json.load(open(os.path.join(CAT, "data/j84_90_exact.json"))))
    names = sorted(set(JX.BUILT) | {k for k in JX.REG if k.split("_")[0] in C.J8X}, key=lambda s: int(s.split("_")[0][1:]))
    assert len(names) == 92
    tasks += [("johnson", nm) for nm in names]
    heavy = ("snub dodecahedron", "truncated icosidodecahedron", "rhombicosidodecahedron", "snub cube")
    tasks.sort(key=lambda t: (t[1] not in heavy, str(t)))
    print("tasks", len(tasks), flush=True)
    ref = {r["name"]: r for r in json.load(open(os.path.join(CAT, "data/catalogue-all.json")))}
    out, bad = [], 0
    with mpr.get_context("fork").Pool(procs) as pool:
        for i, res in enumerate(pool.imap_unordered(run, tasks)):
            if "error" in res:
                bad += 1; print("ERROR", res["task"], res["error"], res["tb"], flush=True); continue
            for r in res["rows"]:
                c = ref[r["name"]]
                a = c.get("corner", c)
                assert len(r["vacuus"]) == a["vacuus_plates"] and len(r["resonus"]) == a["resonus_planes"], r["name"]
                if "vacuus_volume" in r: assert len(r["vacuus_volume"]) == c["volume"]["vacuus_plates"], r["name"]
                out.append(r)
            print(f"PROGRESS {(i + 1) / len(tasks):.3f} {res['task'][1]} ({res['secs']} s)", flush=True)
    json.dump(out, open(os.path.join(STUDY, "data/catalogue-normals.json"), "w"))
    print("rows", len(out), "errors", bad, flush=True)
    if bad == 0 and len(out) == 168:
        print("FINAL ok extract", len(out), flush=True)
