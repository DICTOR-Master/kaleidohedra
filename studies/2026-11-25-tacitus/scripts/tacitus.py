# Tacitus census: in which degrees k does a weighted set of face directions on the sphere fall silent?
# Silent in degree k  <=>  sum_f w_f h(n_f) = 0 for every harmonic h of degree k
#                     <=>  e_k = (1/W^2) sum_{f,g} w_f w_g Z_k(n_f.n_g) = 0,
# Z_k the zonal kernel (Legendre P_k on S^2, Gegenbauer C_k^(1) = U_k/(k+1) on S^3), positive definite (Schoenberg;
# zonal test of Delsarte-Goethals-Seidel 1977). Forced degrees: the symmetry group G of the WEIGHTED set has no invariant
# harmonic of degree k (dim H_k^G = 0, by the character average; Sobolev's invariant-harmonic test). "Beyond" = silent, not forced.
# Usage: python tacitus.py poly POLY.json OUT.jsonl | aequi SHARD NSHARDS OUT.jsonl [LIMIT] | 4d OUT.jsonl     (env PROCS)
import os, sys, json, gzip, csv, math, importlib.util
import numpy as np
from multiprocessing import Pool
KMAX = 20; ZERO, NONZERO = 1e-11, 1e-8
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, "../.."))

def zonal(G, dim, kmax=KMAX):
    """list of matrices Z_k(G), Z_k(1) = 1."""
    G = np.clip(G, -1, 1); out = [np.ones_like(G), G.copy()]
    if dim == 3:
        for k in range(1, kmax): out.append(((2 * k + 1) * G * out[k] - k * out[k - 1]) / (k + 1))
        return out
    U = [np.ones_like(G), 2 * G]                      # Chebyshev U_k, U_k(1) = k+1
    for k in range(1, kmax): U.append(2 * G * U[k] - U[k - 1])
    return [u / (k + 1) for k, u in enumerate(U)]

def energies(P, w, dim):
    G = P @ P.T; W = w.sum(); Z = zonal(G, dim)
    return [float(w @ Z[k] @ w) / W ** 2 for k in range(KMAX + 1)]

def sym_group(P, lab, tol=1e-7):
    """all orthogonal maps (3D) permuting the labelled point set; numerical, tolerance tol."""
    key = lambda X: {(tuple(np.rint(x * 1e6).astype(int)), l) for x, l in zip(X, lab)}
    K = key(P); a = P[0]
    j = next(i for i in range(len(P)) if abs(P[i] @ a) < 1 - 1e-6)
    b = P[j]; ab = a @ b
    A = np.column_stack([a, b, np.cross(a, b)]); Ai = np.linalg.inv(A)
    Rs = []
    for c in np.where(lab == lab[0])[0]:
        for d in np.where(lab == lab[j])[0]:
            if abs(P[c] @ P[d] - ab) > tol: continue
            cr = np.cross(P[c], P[d])
            for s in (1, -1):
                R = np.column_stack([P[c], P[d], s * cr]) @ Ai
                if np.abs(R @ R.T - np.eye(3)).max() > 1e-6: continue
                X = P @ R.T
                if key(X) == K: Rs.append(R)
    return Rs

def char_dims(Rs, kmax=KMAX):
    dims = []
    for k in range(kmax + 1):
        s = 0.0
        for R in Rs:
            det = np.linalg.det(R); Q = R if det > 0 else -R
            c = max(-1.0, min(1.0, (np.trace(Q) - 1) / 2)); th = math.acos(c)
            chi = 1 + 2 * sum(math.cos(m * th) for m in range(1, k + 1))
            s += chi if det > 0 else (-1) ** k * chi
        dims.append(s / len(Rs))
    assert all(abs(d - round(d)) < 1e-6 for d in dims), dims
    return [int(round(d)) for d in dims]

def classify(e, dims):
    silent = [k for k in range(1, KMAX + 1) if e[k] < ZERO]
    grey = [k for k in range(1, KMAX + 1) if ZERO <= e[k] <= NONZERO]
    forced = [k for k in range(1, KMAX + 1) if dims[k] == 0]
    beyond = [k for k in silent if dims[k] > 0]
    assert set(forced) <= set(silent), ("forced but not silent?", forced, silent)
    return dict(silent=silent, forced=forced, beyond=beyond, grey=grey,
                min_nonzero=min([e[k] for k in range(1, KMAX + 1) if e[k] > NONZERO] or [None]))

def group_dims(P, lab):
    """dims of G-invariant harmonics; rank-1 sets ({a} or {a,-a}) handled directly (infinite group)."""
    if np.abs(np.abs(P @ P[0]) - 1).max() < 1e-9:
        anti = len(P) > 1 and (P @ P[0]).min() < 0
        return None, [1 if (k % 2 == 0 or not anti) else 0 for k in range(KMAX + 1)]
    Rs = sym_group(P, lab); return Rs, char_dims(Rs)

def orbits(P, Rs):
    key = {tuple(np.rint(x * 1e6).astype(int)): i for i, x in enumerate(P)}; seen = set(); out = []
    for i in range(len(P)):
        if i in seen: continue
        o = sorted({key[tuple(np.rint(R @ P[i] * 1e6).astype(int))] for R in Rs}); seen |= set(o); out.append(o)
    return out

def explain(P, w, Rs, beyond):
    """why each beyond-symmetry silent degree k holds:
    E  even k, forced by the symmetry group of the centrally symmetrised multiset X + (-X) (same even moments up to factor 2);
    P  every orbit piece (symmetrised for even k) is forced silent by its own group;
    S  every orbit piece is silent, not all forced;   C  the pieces cancel (some piece is not silent)."""
    why = {}
    PP = np.vstack([P, -P]); ww = np.concatenate([w, w])
    # the symmetrised multiset: merge antipodal coincidences into weights
    keys = {}
    for x, a in zip(PP, ww):
        kx = tuple(np.rint(x * 1e6).astype(int)); keys.setdefault(kx, [x, 0.0]); keys[kx][1] += a
    Ps = np.array([v[0] for v in keys.values()]); ws = np.array([v[1] for v in keys.values()])
    _, dsym = group_dims(Ps, labels(ws))
    obs = orbits(P, Rs)
    for k in beyond:
        if k % 2 == 0 and dsym[k] == 0: why[k] = "E"; continue
        forced, silent = True, True
        for o in obs:
            Q, wq = P[o], w[o]
            if k % 2 == 0: Q, wq = np.vstack([Q, -Q]), np.concatenate([wq, wq])
            ek = energies(Q, wq, 3)[k]
            if ek > ZERO: silent = False; forced = False; break
            _, dq = group_dims(Q, labels(wq))
            if dq[k] != 0: forced = False
        why[k] = "P" if forced else ("S" if silent else "C")
    return why

def labels(w):
    _, lab = np.unique(np.rint(np.asarray(w) / max(w) * 1e7), return_inverse=True); return lab

def analyse_set(s):
    P = np.array(s["normals"], float); P /= np.linalg.norm(P, axis=1)[:, None]
    out = {k: s[k] for k in s if k not in ("normals", "verts", "faces", "w2")}
    out["N"] = len(P)
    for var, w in (("i", np.ones(len(P))), ("ii", s.get("w2"))):
        if w is None: continue
        w = np.asarray(w, float); Rs = sym_group(P, labels(w)); dims = char_dims(Rs)
        c = classify(energies(P, w, 3), dims)
        if c["beyond"]: c["why"] = explain(P, w, Rs, c["beyond"])
        out[var] = dict(G=len(Rs), **c)
    return out

def solid_angles(V, faces):
    V = np.asarray(V); om = []
    for f in faces:
        t = 0.0; a = V[f[0]]
        for i in range(1, len(f) - 1):
            b, c = V[f[i]], V[f[i + 1]]; la, lb, lc = map(np.linalg.norm, (a, b, c))
            num = a @ np.cross(b, c); den = la * lb * lc + (a @ b) * lc + (a @ c) * lb + (b @ c) * la
            t += 2 * math.atan2(abs(num), den)
        om.append(t)
    assert abs(sum(om) - 4 * math.pi) < 1e-9, sum(om)
    return om

def poly_sets(path):
    sets = []
    for r in json.load(open(path)):
        r = dict(r); r["w2"] = solid_angles(r["verts"], r["faces"]); sets.append(r)
    return sets

def aequi_sets():
    spec = importlib.util.spec_from_file_location("groups_ext", os.path.join(ST, "2026-11-24-aequi-certify-extend/scripts/groups.py"))
    gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm); DIRS = gm.DIRS
    s1232 = {(d["study"], int(d["sid"])) for d in map(json.loads, open(os.path.join(ST, "2026-11-24-aequi-certify-extend/data/certify-pass1.jsonl")))}
    s4404 = {int(d["sid"]) for d in json.load(open(os.path.join(ST, "2026-11-24-aequi-certify-4404/data/dice4404.json")))}
    co = {(c["src"], int(c["id"])) for c in json.load(open(os.path.join(ST, "2026-11-25-stellation-cycle/data/aequi.json")))["coincidences"]}
    assert len(s1232) == 1232 and len(s4404) == 4404
    sets = []
    for study, src in (("2026-11-19-aequi-complete", "4553"), ("2026-11-20-aequi-two-placements", None)):
        dd = os.path.join(ST, study, "data/dice")
        for f in sorted(os.listdir(dd)):
            d = json.load(open(os.path.join(dd, f))); sid = int(d["sid"])
            idx = json.loads(d["face_directions"]) if isinstance(d["face_directions"], str) else d["face_directions"]
            tags = [t for t, ok in (("1232", (study, sid) in s1232), ("4404", src and sid in s4404), ("cycle", (src, sid) in co)) if ok]
            sets.append(dict(name="%s:%d" % (study[:10], sid), family="Aequi " + study[:10], label=d["label"], group=d["group"],
                             tags=tags, normals=DIRS[idx].tolist()))
    assert len(sets) == 4553 + 1083, len(sets)
    batches = {}
    for row in csv.DictReader(open(os.path.join(ST, "2026-11-24-aequi-catalogue-2/catalogue.csv"))):
        b = row["source_batch"]
        if b == "reserved": continue
        if b not in batches: batches[b] = json.load(gzip.open(os.path.join(ST, "2026-11-24-aequi-certify-extend/data/aequi%s.json.gz" % b)))["new"]
        d = batches[b][int(row["source_id"])]
        sets.append(dict(name="No.%s" % row["No"], family="Aequi catalogue-2", label=row["name_shown"], group=row["group"],
                         tags=["cycle"] if ("ext " + b, int(row["source_id"])) in co else [], normals=DIRS[d["idx"]].tolist()))
    assert len(sets) == 4553 + 1083 + 9490
    assert sum("cycle" in s["tags"] for s in sets) == len(co), "cycle tags"
    return sets

# ---- 4D regular polytopes: facet normals = corners of the polar polytope; forced degrees from the Coxeter degrees
def molien_harm(degs, kmax=KMAX):
    ser = [1] + [0] * kmax
    for d in degs:
        for k in range(d, kmax + 1): ser[k] += ser[k - d]
    return [ser[k] - (ser[k - 2] if k >= 2 else 0) for k in range(kmax + 1)]   # harmonic invariants = (1 - t^2) * invariants

def four_d():
    import itertools
    ph = (1 + 5 ** 0.5) / 2
    def sgn(v):
        return {tuple(s * x for s, x in zip(ss, v)) for ss in itertools.product((1, -1), repeat=len(v))}
    def perms(v, even=False):
        out = set()
        for p in itertools.permutations(range(4)):
            par = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2
            if even and par: continue
            for s in sgn(v): out.add(tuple(s[i] for i in p))
        return out
    c16 = sorted(perms((1, 0, 0, 0))); c8 = sorted(sgn((1, 1, 1, 1)))
    c24d = sorted(perms((1, 1, 0, 0)))                       # polar of the 24-cell (1,0,0,0)+(1/2,..)
    c600 = sorted(perms((1, 0, 0, 0)) | sgn((.5, .5, .5, .5)) | perms((ph / 2, .5, 1 / (2 * ph), 0), even=True))
    assert len(c600) == 120
    A = np.array(c600); G = A @ A.T; nb = [set(np.where(np.abs(G[i] - ph / 2) < 1e-9)[0]) for i in range(120)]
    cells = {tuple(sorted((i, j, k, l))) for i in range(120) for j in nb[i] for k in nb[i] & nb[j] for l in nb[i] & nb[j] & nb[k]}
    assert len(cells) == 600
    c120 = np.array([A[list(c)].sum(0) for c in cells])
    E = np.eye(5) - 0.2; B = np.linalg.svd(E)[2][:4]; c5 = (E @ B.T)               # 5 corners of a regular simplex
    S = [("5-cell", -c5, (2, 3, 4, 5)), ("tesseract (8 normals)", np.array(c16, float), (2, 4, 6, 8)),
         ("16-cell (16 normals)", np.array(c8, float), (2, 4, 6, 8)), ("24-cell (24 normals)", np.array(c24d, float), (2, 6, 8, 12)),
         ("120-cell (120 normals)", A, (2, 12, 20, 30)), ("600-cell (600 normals)", c120, (2, 12, 20, 30))]
    out = []
    for nm, P, degs in S:
        P = P / np.linalg.norm(P, axis=1)[:, None]; e = energies(P, np.ones(len(P)), 4)
        out.append(dict(name=nm, family="4D regular", N=len(P), i=dict(G="W(degrees %s)" % (degs,), **classify(e, molien_harm(degs)))))
    return out

def run(mode, args):
    procs = int(os.environ.get("PROCS", "4"))
    if mode == "4d":
        res = four_d(); outp = args[0]
    elif mode == "poly":
        sets = poly_sets(args[0]); outp = args[1]
    else:
        sh, ns, outp = int(args[0]), int(args[1]), args[2]
        sets = aequi_sets()[sh::ns]
        if len(args) > 3: sets = sets[:int(args[3])]
    if mode != "4d":
        res = []
        with Pool(procs) as pool:
            for i, r in enumerate(pool.imap(analyse_set, sets, chunksize=8)):
                res.append(r)
                if i % 500 == 0: print("PROGRESS %.3f %s" % ((i + 1) / len(sets), r["name"]), flush=True)
    with open(outp, "w") as fo:
        for r in res: fo.write(json.dumps(r) + "\n")
    grey = sum(bool(r[v]["grey"]) for r in res for v in ("i", "ii") if v in r)
    beyond = sum(bool(r[v]["beyond"]) for r in res for v in ("i", "ii") if v in r)
    print("sets", len(res), "with beyond-symmetry silence", beyond, "with grey energies", grey)
    print("grey (set, variant, degrees) for the exact check:", [(r["name"], v, r[v]["grey"]) for r in res for v in ("i", "ii") if v in r and r[v]["grey"]])
    ok = all(set(r[v]["forced"]) <= set(r[v]["silent"]) for r in res for v in ("i", "ii") if v in r) and len(res) > 0
    print("FINAL ok" if ok else "FINAL FAIL forced degree not silent")

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2:])
