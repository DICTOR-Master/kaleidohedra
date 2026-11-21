"""Scutoid approximants study (21 Nov 2026), step 3: each cubic 1/1 approximant as an amber cell, run with DICTO's combined method at
the REAL scale, then compared with the real atoms between core and mould.
For each case:
 1. core atoms = the chosen closed cluster shell around the cluster centre (radius window); if a cap shell is given, the window atoms
    are split by direction (five-fold axes -> cap, the rest -> icosidodecahedron).
 2. frame: the real directions are matched to the amber solid's vertex directions as built in the sweep (identity) or turned
    90 degrees about z (the other T_h setting); the better one is used, its largest angular deviation reported.
 3. scale k (Angstrom per amber unit): least squares of real radii against the ideal vertex radii; s_real = a / k; s0 = smallest
    lattice scale with the ideal core inside its bcc Voronoi cell (float here, exact in amber.py).  s_real < s0: the real shell does not
    fit its bcc Voronoi cell (neighbouring shells overlap); no run.
 4. run amber.py (sweep, unchanged except the Y dump of the Y-junction study) with AMBER_S = s_real rounded to 1/1000, bcc, centroid seeds.
 5. comparison (float, Angstrom): resin atoms = atoms inside the real bcc Voronoi cell of the centre and outside the scaled ideal core.
    For each Y: nearest resin atom; for each resin atom: nearest Y and nearest 2-fold axis of the core (15 lines).  Baseline: 40000
    uniform random points of the same resin (rejection sampling, fixed seed): their distance to the nearest resin atom, and to the nearest
    2-fold axis.  Percentile = share of random points closer.  The Y vertices come in T_h orbits, so the independent Y positions are few
    (counted and reported).
Usage: python approx.py  (all cases, foreground; writes ../data/approx_<case>.json, ../data/run_<case>.log, prints the summary)"""
import os, sys, json, itertools, subprocess, time
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "../data")
SWEEP = os.path.abspath(os.path.join(HERE, "../../2026-11-21-amber-cell-sweep/scripts"))
RESIN = os.path.abspath(os.path.join(HERE, "../../2026-11-21-scutoid-stand-in/tree/branch-D-resin/scripts"))
SHIM = os.path.join(HERE, "shim")
P = (1 + 5 ** 0.5) / 2
RZ = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], float)

# patched amber (Y dump), generated from the sweep's amber.py exactly as in the Y-junction study
MARK = "    Yset = {m for m in mvert.values() if m is not None}\n"
DUMP = MARK + '''    import json as _j
    _s = lambda c: [str(c.a), str(c.b)]
    _Y = []
    for _r, _m in mvert.items():
        if _m is None: continue
        _mem = clusters[_r]
        _Y.append(dict(Y=[_s(c) for c in X[_m]], I=[[_s(c) for c in X[n[1]]] for n in _mem if n[0] == "i"], O=[[_s(c) for c in X[n[1]]] for n in _mem if n[0] == "o"]))
    _j.dump(_Y, open(os.environ["YDUMP"], "w"))
'''
src = open(os.path.join(SWEEP, "amber.py")).read(); assert src.count(MARK) == 1
open(os.path.join(HERE, "_amber_patched.py"), "w").write(src.replace(MARK, DUMP))

def orbit(base):
    out = []
    for b in base:
        for sg in itertools.product((1, -1), repeat=3):
            t = [b[i] * sg[i] for i in range(3)]
            for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
                if not any(np.allclose(c, o) for o in out): out.append(c)
    return np.array(out, float)
ID_DIRS = orbit([(0, 0, P), (0.5, P / 2, P * P / 2)])            # sweep icosidodecahedron vertices = 2-fold axes of every core used here
AXES = []
for v in ID_DIRS / np.linalg.norm(ID_DIRS, axis=1, keepdims=True):
    if not any(abs(abs(v @ w) - 1) < 1e-9 for w in AXES): AXES.append(v)
AXES = np.array(AXES); assert len(AXES) == 15
FIVE = orbit([(0, P, 1)]); FIVE = FIVE / np.linalg.norm(FIVE, axis=1, keepdims=True)   # pentagon normals of the sweep icosidodecahedron

CASES = [
    # name, cif id, family, centres (fractional), core solid, window (A) for core atoms, cap?
    ("tsai_ScZn6_4101359", "4101359", "Tsai 1/1 Sc3Zn17.7 (Im-3)", [(0, 0, 0)], "icosidodecahedron", (5.5, 5.8), None),
    ("tsai_ScZn6_4101359_capped", "4101359", "Tsai 1/1 Sc3Zn17.7 (Im-3)", [(0, 0, 0)], "capped_icosidodecahedron", (5.5, 5.8), (4.8, 5.0)),
    ("tsai_YbCd6Mg_2021894", "2021894", "Tsai 1/1 Yb24Cd113.8Mg31.4 (Im-3)", [(0, 0, 0)], "icosidodecahedron", (6.40, 6.50), None),
    ("tsai_YbCd6Mg_2021894_capped", "2021894", "Tsai 1/1 Yb24Cd113.8Mg31.4 (Im-3)", [(0, 0, 0)], "capped_icosidodecahedron", (6.40, 6.50), (5.5, 5.6)),
    ("tsai_YCdMg_2108845", "2108845", "Tsai 1/1 Y24Cd109.9Mg35.3 (Im-3)", [(0, 0, 0)], "icosidodecahedron", (6.2, 6.4), None),
    ("tsai_YbCd6_1525048", "1525048", "Cd6Yb 1/1, 1971 model (I23)", [(0, 0, 0)], "icosidodecahedron", (6.3, 6.5), None),
    ("tsai_ScZn6_4101359_RTH", "4101359", "Tsai 1/1 Sc3Zn17.7 (Im-3)", [(0, 0, 0)], "rhombic_triacontahedron", None, None),
    ("bergman_LiMgZnAl_4319177", "4319177", "Bergman 1/1 Mg32(Al,Zn)49 type, Li20Mg32Zn85Al23 (Im-3)", [(0, 0, 0)], "rhombic_triacontahedron", (4.5, 5.1), None),
    ("bergman_LiMgZnAl_4319177_TI", "4319177", "Bergman 1/1 Mg32(Al,Zn)49 type, Li20Mg32Zn85Al23 (Im-3)", [(0, 0, 0)], "truncated_icosahedron", (6.6, 7.25), None),
    ("mackay_AlMnSi_2007194", "2007194", "Mackay 1/1 alpha-AlMnSi (Pm-3)", [(0, 0, 0), (.5, .5, .5)], "icosidodecahedron", (4.6, 4.9), "split"),
    ("mackay_AlMnSi_2007194_capped", "2007194", "Mackay 1/1 alpha-AlMnSi (Pm-3)", [(0, 0, 0), (.5, .5, .5)], "capped_icosidodecahedron", (4.6, 4.9), "split"),
    ("mackay_AlCuFeSi_1532186", "1532186", "Mackay 1/1 Al-Cu-Fe-Si (Im-3)", [(0, 0, 0)], "icosidodecahedron", (4.6, 4.8), "split"),
    ("mackay_AlCuFeSi_1532186_capped", "1532186", "Mackay 1/1 Al-Cu-Fe-Si (Im-3)", [(0, 0, 0)], "capped_icosidodecahedron", (4.6, 4.8), "split"),
]

def solid_float(name, lam=None):
    """vertices and face planes of the amber solid (float), built by the sweep's solids.py via the shim, in a subprocess-free import"""
    os.environ.update(RESIN_DIR=RESIN, SWEEP_DIR=SWEEP)
    if lam is not None: os.environ["CAP_LAMBDA"] = str(lam)
    sys.path[:0] = [SHIM, RESIN]
    import importlib; import solids as S; importlib.reload(S)
    C = S.build(name)
    V = np.array([[float(x) for x in v] for v in C["V"]]); planes = [(np.array([float(x) for x in n]), float(c)) for n, c in C["planes"]]
    nf = [len(f) for f, k in C["faces"]]
    return V, planes, nf

def neighbourhood(cell, centre, rmax):
    a = cell["a"]; X = np.array([t["cart"] for t in cell["atoms"]]); C = np.array(centre) * a; out = []
    for n in itertools.product((-2, -1, 0, 1, 2), repeat=3):
        Y = X + np.array(n) * a - C; d = np.linalg.norm(Y, axis=1)
        for i in np.where(d < rmax)[0]: out.append((Y[i], i))
    return out

def s0_bcc(V): return max(max(2 * np.abs(V).max(1)), max(4 / 3 * np.abs(V).sum(1)))

def in_mould(x, a): return np.all(np.abs(x) <= a / 2 + 1e-9, axis=-1) & (np.abs(x).sum(-1) <= 0.75 * a + 1e-9)

def dist_axes(x):
    """perpendicular distance of points x (n,3) to the nearest of the 15 2-fold axis lines (amber frame)"""
    pr = x @ AXES.T; d2 = (x * x).sum(1)[:, None] - pr ** 2
    return np.sqrt(np.clip(d2, 0, None)).min(1)

def run_case(case):
    name, cid, fam, centres, solid, win, cap = case
    cell = json.load(open(os.path.join(DATA, f"cells/cell_{cid}.json"))); a = cell["a"]
    R = dict(case=name, cif=cid, family=fam, a=a, space_group=cell["space_group"], solid=solid, centres=centres, doi=cell["doi"])
    if solid == "rhombic_triacontahedron" and win is None:
        # Tsai outer shell: the triacontahedron through the 12 five-fold and 20 three-fold vertex atoms of the Tsai cluster.
        # Smallest possible core = triacontahedron that still contains the icosidodecahedron shell (its face centres on the 2-fold axes).
        V, planes, nf = solid_float(solid)
        nb = neighbourhood(cell, centres[0], 9.6)
        idr = [np.linalg.norm(x) for x, i in nb if 5.5 < np.linalg.norm(x) < 5.8]
        inr = min(c / np.linalg.norm(n) for n, c in planes)
        k = max(idr) / inr * 1.0       # triacontahedron with inradius = icosidodecahedron radius (faces touching the 30 shell atoms)
        s_real = a / k; s0 = s0_bcc(V)
        R.update(k=k, s_real=s_real, s0=s0, ratio=s_real / s0, fits=bool(s_real >= s0),
                 note="lower bound: the triacontahedron with inradius equal to the icosidodecahedron-shell radius (any real outer shell is larger)")
        return R
    lo, hi = win
    per_centre = []
    for c in centres:
        nb = neighbourhood(cell, c, hi + 0.01)
        W = [(x, i) for x, i in nb if lo <= np.linalg.norm(x) <= hi]
        per_centre.append(W)
    # frame and split
    V_id = None
    def frame_dev(D, ref):
        best = None
        for fname, M in (("same", np.eye(3)), ("turned90z", RZ)):
            Rf = ref @ M.T; Rf = Rf / np.linalg.norm(Rf, axis=1, keepdims=True)
            c = np.clip(D @ Rf.T, -1, 1); dev = np.degrees(np.arccos(c.max(1)))
            if best is None or dev.max() < best[1]: best = (fname, float(dev.max()), M)
        return best
    lam = None
    if cap:
        # split each centre's window atoms: within 6 deg of a five-fold axis (either frame decided below) -> cap
        Dall = np.array([x / np.linalg.norm(x) for W in per_centre for x, i in W])
        cnt = {nm: int((np.max(np.abs(Dall @ (FIVE @ Mx.T).T), 1) > np.cos(np.radians(6))).sum()) for nm, Mx in (("same", np.eye(3)), ("turned90z", RZ))}
        M = np.eye(3) if cnt["same"] >= cnt["turned90z"] else RZ; F5 = FIVE @ M.T; R["five_fold_atoms_by_frame"] = cnt
        cores, caps = [], []
        for W in per_centre:
            cw = [(x, i) for x, i in W if np.max(np.abs((x / np.linalg.norm(x)) @ F5.T)) > np.cos(np.radians(6))]
            iw = [(x, i) for x, i in W if np.max(np.abs((x / np.linalg.norm(x)) @ F5.T)) <= np.cos(np.radians(6))]
            cores.append(iw); caps.append(cw)
        if isinstance(cap, tuple):
            caps = []
            for c in centres:
                nb = neighbourhood(cell, c, cap[1] + 0.01); caps.append([(x, i) for x, i in nb if cap[0] <= np.linalg.norm(x) <= cap[1]])
        per_centre = cores
        rid = np.mean([np.linalg.norm(x) for W in cores for x, i in W]); rcap = np.mean([np.linalg.norm(x) for W in caps for x, i in W])
        R.update(n_core_atoms=[len(W) for W in cores], n_cap_atoms=[len(W) for W in caps], r_cap_mean=float(rcap),
                 r_cap_per_centre=[float(np.mean([np.linalg.norm(x) for x, i in W])) for W in caps],
                 cap_protrusion_A=float(rcap - rid * 1.3763819 / P))   # pentagon plane distance of the icosidodecahedron = 1.37638 (edge 1)
        if solid == "capped_icosidodecahedron":
            # icosahedron (0, phi, 1)*lam has radius lam*1.902113; wanted radius = (rcap/rid)*phi
            lam = Fr(rcap / rid * P / np.sqrt(P * P + 1)).limit_denominator(200)
            R.update(cap_lambda=str(lam), cap_ratio_real=float(rcap / rid), cap_ratio_model=float(lam) * np.sqrt(P * P + 1) / P)
        else:
            R.update(caps_ignored=True)
    V, planes, nf = solid_float(solid, lam)
    R.update(n_vertices=len(V), face_sizes=dict(zip(*np.unique(nf, return_counts=True))) if False else {str(k): int(v) for k, v in zip(*np.unique(nf, return_counts=True))})
    if solid == "capped_icosidodecahedron":
        Vfit = V[np.isclose(np.linalg.norm(V, axis=1), P)]       # fit k on the 30 icosidodecahedron vertices only
    else:
        Vfit = V
    Dall = np.array([x / np.linalg.norm(x) for W in per_centre for x, i in W])
    fname, fdev, M = frame_dev(Dall, Vfit)
    R.update(frame=fname, frame_max_dev_deg=fdev, n_core_atoms=[len(W) for W in per_centre])
    # k: pair each atom with its nearest ideal vertex direction, least squares r_atom ~ k r_ideal
    Vr = Vfit @ M.T; Vu = Vr / np.linalg.norm(Vr, axis=1, keepdims=True)
    num_, den_ = 0.0, 0.0; ks = []
    for W in per_centre:
        nk, dk = 0.0, 0.0
        for x, i in W:
            j = np.argmax(Vu @ (x / np.linalg.norm(x))); ri = np.linalg.norm(Vr[j]); r = np.linalg.norm(x)
            nk += r * ri; dk += ri * ri
        ks.append(nk / dk); num_ += nk; den_ += dk
    k = num_ / den_
    radii = [np.linalg.norm(x) for W in per_centre for x, i in W]
    # how far the real atoms are from the ideal scaled vertices (Angstrom)
    devA = []
    for W in per_centre:
        for x, i in W:
            devA.append(np.min(np.linalg.norm(Vr * k - x, axis=1)))
    s0 = s0_bcc(V); s_real = a / k
    R.update(k=k, k_per_centre=ks, r_core_mean=float(np.mean(radii)), r_core_min=float(min(radii)), r_core_max=float(max(radii)),
             atom_to_ideal_vertex_max_A=float(max(devA)), atom_to_ideal_vertex_rms_A=float(np.sqrt(np.mean(np.square(devA)))),
             s_real=s_real, s0=s0, ratio=s_real / s0, fits=bool(s_real > s0))
    if not s_real > s0:
        R.update(note="real shell larger than its bcc Voronoi cell allows: neighbouring shells overlap, no amber cell at the real scale"); return R
    # amber run at the real scale
    s_rat = Fr(round(s_real * 1000), 1000)
    ydump = os.path.join(DATA, f"ydump_{name}.json")
    env = dict(os.environ, RESIN_DIR=RESIN, SWEEP_DIR=SWEEP, PYTHONPATH=SHIM + os.pathsep + SWEEP, YDUMP=ydump, AMBER_S=f"{s_rat},0")
    if lam is not None: env["CAP_LAMBDA"] = str(lam)
    t = time.time()
    p = subprocess.run([sys.executable, os.path.join(HERE, "_amber_patched.py"), solid, "bcc", "1", "cen"], env=env, capture_output=True, text=True, timeout=250)
    open(os.path.join(DATA, f"run_{name}.log"), "w").write(p.stdout + p.stderr)
    fac = "S" + str(s_rat).replace("/", "|")
    out = os.path.join(DATA, f"amber_{solid}_bcc_{fac.replace('/', '-')}_cen.json")
    res = json.load(open(out)); os.replace(out, os.path.join(DATA, f"amber_{name}.json"))
    R.update(s_run=str(s_rat), run_seconds=round(time.time() - t, 1), valid=res["valid"], why=res["why"], n_kinds=res.get("n_kinds"),
             n_scutoid_pieces=res.get("n_scutoid_pieces"), n_pieces=res.get("n_faces"), n_Y=res.get("n_Y"), contact_vertices=len(res.get("contact_vertices", [])),
             volume_gap=res.get("volume_gap"), sampling=res.get("sampling"), lambda_present=res.get("lambda_present"))
    if not res["valid"] or not os.path.exists(ydump): return R
    from fractions import Fraction as F
    Yam = np.array([[float(F(c[0])) + float(F(c[1])) * 5 ** 0.5 for c in y["Y"]] for y in json.load(open(ydump))]) if res["n_Y"] else np.zeros((0, 3))
    if len(Yam):
        R["Y_axis_dist_amber_units_max"] = float(dist_axes(Yam).max())   # amber frame: 2-fold axes = ID_DIRS lines
    Yreal = (Yam * k) @ M.T if len(Yam) else Yam                       # amber frame -> real frame, Angstrom, about the centre
    AX_real = AXES @ M.T
    def dax_real(x):
        pr = x @ AX_real.T; d2 = (x * x).sum(1)[:, None] - pr ** 2; return np.sqrt(np.clip(d2, 0, None)).min(1)
    # resin atoms of the first centre: inside the real bcc Voronoi cell, outside the scaled ideal core
    Pl = [((n @ M.T), c * k) for n, c in planes]
    def outside_core(x): return np.any(np.stack([x @ n - c for n, c in Pl], -1) > 0, axis=-1)
    comp = []
    for ci, c in enumerate(centres):
        nb = neighbourhood(cell, c, 0.75 * a / np.sqrt(3) * np.sqrt(3) + 0.1)
        X = np.array([x for x, i in nb]); idx = [i for x, i in nb]
        rcut = max(win[1], cap[1] if isinstance(cap, tuple) else 0) + 1e-6   # the core shell and cap atoms are cluster atoms, never resin
        sel = in_mould(X, a) & outside_core(X) & (np.linalg.norm(X, axis=1) > rcut)
        shell_out = int((in_mould(X, a) & outside_core(X) & (np.linalg.norm(X, axis=1) <= rcut)).sum())
        RA = X[sel]; RL = [cell["atoms"][idx[j]]["label"] for j in np.where(sel)[0]]
        RO = [cell["atoms"][idx[j]]["occ"] for j in np.where(sel)[0]]
        inside_core = int((in_mould(X, a) & ~outside_core(X)).sum())
        # all resin atoms around (any Voronoi cell): each atom reduced to its nearest cluster centre (bcc centres), outside that core
        nb2 = neighbourhood(cell, c, 0.56 * a + 4.5); X2 = np.array([x for x, i in nb2])
        cand = np.vstack([X2 - a * np.round(X2 / a), X2 - a * (np.floor(X2 / a) + 0.5)]).reshape(2, len(X2), 3)
        Yred = np.where((np.linalg.norm(cand[0], axis=1) <= np.linalg.norm(cand[1], axis=1))[:, None], cand[0], cand[1])
        RA_all = X2[outside_core(Yred) & (np.linalg.norm(Yred, axis=1) > rcut)]
        # random baseline in the same resin
        rng = np.random.default_rng(20261121 + ci); pts = []
        while sum(len(q) for q in pts) < 40000:
            q = rng.uniform(-a / 2, a / 2, (60000, 3)); q = q[in_mould(q, a) & outside_core(q)]; pts.append(q)
        Rnd = np.vstack(pts)[:40000]
        def nn(A, B): return np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)).min(1)
        rnd_nn = np.concatenate([nn(Rnd[j:j + 4000], RA_all) for j in range(0, len(Rnd), 4000)])
        rnd_ax = dax_real(Rnd)
        C = dict(centre=c, n_resin_atoms=int(len(RA)), n_resin_atoms_all_cells_near=int(len(RA_all)), n_atoms_inside_core=inside_core, n_shell_atoms_just_outside_ideal_core=shell_out, resin_atom_labels=sorted(set(RL)),
                 random_nn_median=float(np.median(rnd_nn)), random_axis_median=float(np.median(rnd_ax)))
        ax_atoms = dax_real(RA)
        on_cube = np.array([np.sum(np.abs(x) > 1e-3) == 1 for x in RA])   # on a cube axis: crystallographic special position
        C.update(atom_axis_dist=[round(float(d), 3) for d in ax_atoms], atom_on_cube_axis=[bool(b) for b in on_cube],
                 atoms_within_0p3A_of_axis=int((ax_atoms < 0.3).sum()), atoms_within_0p3A_noncube=int(((ax_atoms < 0.3) & ~on_cube).sum()),
                 random_share_within_0p3A=float((rnd_ax < 0.3).mean()),
                 expected_within_0p3A=float((rnd_ax < 0.3).mean() * len(RA)),
                 atom_axis_percentiles=[round(float((rnd_ax < d).mean()), 4) for d in ax_atoms], resin_atom_labels_each=RL, resin_atom_occ=RO,
                 resin_atom_r=[round(float(np.linalg.norm(x)), 3) for x in RA])
        if len(Yreal):
            Yc = Yreal  # same Y set at each centre (bcc mould, one core)
            dY = nn(Yc, RA_all); jY = [int(np.argmin(np.linalg.norm(RA_all - y, axis=1))) for y in Yc]
            LA = [cell["atoms"][nb2[j][1]]["label"] for j in np.where(outside_core(Yred) & (np.linalg.norm(Yred, axis=1) > rcut))[0]]
            # orbits of Y: group by (|Y|, nearest-atom distance)
            orb = {}
            for y, d, j in zip(Yc, dY, jY): orb.setdefault((round(float(np.linalg.norm(y)), 3), round(float(d), 3)), []).append(LA[j])
            C.update(Y_nn=[round(float(d), 3) for d in dY], Y_nn_label=[LA[j] for j in jY],
                     Y_nn_percentile=[round(float((rnd_nn < d).mean()), 4) for d in dY],
                     Y_orbits=[dict(r=k_[0], nn=k_[1], count=len(v), nearest_labels=sorted(set(v))) for k_, v in sorted(orb.items())],
                     atom_to_nearest_Y=[round(float(d), 3) for d in nn(RA, Yc)])
        comp.append(C)
    R["comparison"] = comp
    return R

def summary(R):
    s = f"{R['case']}: {R['family']}; a = {R['a']} A; core {R['solid']}"
    if "frame_max_dev_deg" in R: s += f" (atoms to ideal directions <= {R['frame_max_dev_deg']:.2f} deg, to ideal vertices rms {R['atom_to_ideal_vertex_rms_A']:.3f} max {R['atom_to_ideal_vertex_max_A']:.3f} A)"
    s += f"; k = {R['k']:.4f} A/unit; s_real = {R['s_real']:.4f}, s0 = {R['s0']:.4f}, s_real/s0 = {R['ratio']:.4f}"
    if "cap_protrusion_A" in R: s += f"; cap shell r = {R['r_cap_mean']:.3f} A, sticks out of the pentagon planes by {R['cap_protrusion_A']:.3f} A"
    if not R["fits"]: return s + f"; DOES NOT FIT: {R.get('note', '')}"
    s += f"\n   amber run (s = {R['s_run']}): valid {R['valid']}; kinds {R['n_kinds']}; scutoids {R['n_scutoid_pieces']}/{R.get('n_pieces')}; Y {R['n_Y']}"
    if R.get("n_Y"): s += f"; max distance of Y from a 2-fold axis {R['Y_axis_dist_amber_units_max']:.2e} (amber units)"
    for C in R.get("comparison", []):
        s += f"\n   centre {C['centre']}: resin atoms {C['n_resin_atoms']} ({','.join(C['resin_atom_labels'])[:70]}); atoms inside the ideal core {C['n_atoms_inside_core']}; core/cap shell atoms just outside the ideal core (excluded) {C['n_shell_atoms_just_outside_ideal_core']}"
        s += f"\n     atoms within 0.3 A of a 2-fold axis: {C['atoms_within_0p3A_of_axis']} (on cube axes {C['atoms_within_0p3A_of_axis'] - C['atoms_within_0p3A_noncube']}, other axes {C['atoms_within_0p3A_noncube']}); expected for random points {C['expected_within_0p3A']:.2f}"
        if "Y_orbits" in C:
            for o in C["Y_orbits"]:
                s += f"\n     Y orbit: {o['count']} Y at r = {o['r']} A, nearest resin atom {o['nn']} A ({','.join(o['nearest_labels'])}); random-point median {C['random_nn_median']:.3f} A, percentile {C['Y_nn_percentile'][C['Y_nn'].index(o['nn'])]:.3f}"
    return s

if __name__ == "__main__":
    only = sys.argv[1:]
    allR = []
    for case in CASES:
        if only and case[0] not in only: continue
        R = run_case(case); allR.append(R)
        json.dump(R, open(os.path.join(DATA, f"approx_{case[0]}.json"), "w"), indent=1, default=str)
        print(summary(R), flush=True)
