# Face data of the 163 catalogue polyhedra (study 2026-11-24-vacuus-resonus-catalogue): 5 Platonic, 13 Archimedean,
# 13 Catalan, prisms/antiprisms 3..12 with duals (40), 92 Johnson. Reuses that study's exact builders unchanged
# (exact fields; faces from VX.analyse); writes corner-centred float vertices, faces and unit normals.
# Run with the venv holding sympy + python-flint:  python extract_polyhedra.py OUT.json [names...]
import os, sys, json, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CATS = os.path.normpath(os.path.join(HERE, "../../2026-11-24-vacuus-resonus-catalogue/scripts"))
sys.path.insert(0, CATS)
spec = importlib.util.spec_from_file_location("cat", os.path.join(CATS, "catalogue.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
VX, JX, sp = C.VX, C.JX, C.sp
out_path = os.path.abspath(sys.argv[1]); only = set(sys.argv[2:])

def rec(name, family, F, V, faces, group=None):
    P = np.array([VX.fl(F, v) for v in V])
    N = []
    for f in faces:
        n = np.array(VX.fl(F, f["N"])); N.append((n / np.linalg.norm(n)).tolist())
    return {"name": name, "family": family, "group": group, "verts": P.tolist(), "faces": [f["verts"] for f in faces], "normals": N}

rows = []
def want(nm): return not only or nm in only or nm.split("_")[0] in only
S = VX.uniform_solids(); C.S = S
for nm in S:
    F, gen, grp = S[nm]
    if not (want(nm) or want(C.CATALAN.get(nm, ""))): continue
    if nm == "snub dodecahedron":
        V = None
        for cand in gen:
            Vc = VX.build_set(F, cand)
            try:
                if len(Vc) == 60: VX.analyse("probe", F, Vc, True); V = Vc; break
            except AssertionError: pass
    else: V = VX.build_set(F, gen)
    r, faces = VX.analyse(nm, F, V, True)
    rows.append(rec(nm, "Platonic" if nm in C.PLATONIC else "Archimedean", F, V, faces, grp))
    if nm in C.CATALAN:          # polars of the Platonic polyhedra are Platonic again: not repeated (163 = 168 - 5)
        D = VX.dual_vertices(F, faces); r2, f2 = VX.analyse(C.CATALAN[nm], F, D, False)
        rows.append(rec(C.CATALAN[nm], "Catalan", F, D, f2, grp))
    print("done", nm, flush=True)
for n in range(3, 13):
    if only and str(n) not in only: continue
    F, pr, ap = VX.prism_family(n)
    for nm, V0, fam, dn, dfam in ((f"{n}-gonal prism", pr, "prism", f"{n}-gonal bipyramid", "bipyramid"),
                                  (f"{n}-gonal antiprism", ap, "antiprism", f"{n}-gonal trapezohedron", "trapezohedron")):
        V = VX.build_set(F, V0); r, faces = VX.analyse(nm, F, V, True); rows.append(rec(nm, fam, F, V, faces))
        D = VX.dual_vertices(F, faces); r2, f2 = VX.analyse(dn, F, D, False); rows.append(rec(dn, dfam, F, D, f2))
    print("done prisms", n, flush=True)
os.chdir(C.VE)
for m in (3, 4, 5, 6, 8, 10): JX.axial(m)
JX.prisms_augmented(); JX.gyrobifastigium(); JX.platonic_archimedean_based()
JX.recognise("J91_BILUNABIROTUNDA", [sp.sqrt(5)], [sp.Integer(1), sp.sqrt(5)])
JX.recognise("J92_TRIANGULAR_HEBESPHENOROTUNDA", [sp.sqrt(3), sp.sqrt(5)], [sp.Integer(1), sp.sqrt(3), sp.sqrt(5), sp.sqrt(15)])
os.chdir(HERE)
C.J8X.update(json.load(open(os.path.join(C.STUDY, "data/j84_90_exact.json"))))
names = sorted(set(JX.BUILT) | {k for k in JX.REG if k.split("_")[0] in C.J8X}, key=lambda s: int(s.split("_")[0][1:]))
assert len(names) == 92
for nm in names:
    if not want(nm): continue
    F, V, recipe = C.johnson_solid(nm)
    Oc, Ov = JX.centroids(F, V)
    W = [C.vsub(v, Oc) for v in V]
    r, faces = VX.analyse(nm, F, W, True, None, check_centre=False)
    rows.append(rec(nm, "Johnson", F, W, faces)); print("done", nm, flush=True)
json.dump(rows, open(out_path, "w"))
print("polyhedra", len(rows))
print("FINAL ok" if (only or len(rows) == 163) else "FINAL FAIL count")
