# DICTO · Tacitus, second step (25 Nov 2026). With Claude (Anthropic).
# (A) Variant (iii): each face direction weighted by its FACE AREA (Steinhardt's q_l with Mickel et al.'s Minkowski area weights,
#     outside-clues lead 2). Degree 1 is silent for every closed polyhedron (Minkowski: sum A_f n_f = 0) - a built-in control.
#     Sets: the 163 polyhedra (corners and faces as in poly.jsonl's source) and the 15 126 Aequi rebuilt from their depths
#     (fairness re-checked to 1e-9 before use: guards the face order).
# (B) Fingerprint of the 286 accidental silences of variant (i) (post.json: beyond symmetry, no exact cover): for each die-degree
#     pair, the degree-k moment of each face orbit, M_k(O) in the harmonic space; Gram matrix <M(A), M(B)> = sum P_k(a.b);
#     which orbits carry a moment, and how they cancel (rank, sign pattern).
# Usage: python tacitus_iii.py OUTDIR [PROCS]
import os, sys, json, gzip, csv, math
import numpy as np
from multiprocessing import Pool
from scipy.spatial import HalfspaceIntersection
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tacitus as T
ST = T.ST; OUT = sys.argv[1]; NP = int(sys.argv[2]) if len(sys.argv) > 2 else 20
os.makedirs(OUT, exist_ok=True)
import importlib.util
spec = importlib.util.spec_from_file_location("g", os.path.join(ST, "2026-11-24-aequi-certify-extend/scripts/groups.py")); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
DIRS = np.array(g.DIRS, float); DIRS /= np.linalg.norm(DIRS, axis=1)[:, None]

def faces_of(idx, dep):
    H = np.hstack([DIRS[idx], -np.array(dep)[:, None]]); V = HalfspaceIntersection(H, np.zeros(3)).intersections
    V = np.unique(np.round(V, 12), axis=0); areas, om = [], []
    for k, i in enumerate(idx):
        on = V[np.abs(V @ DIRS[i] - dep[k]) < 1e-9]; c = on.mean(0); u = on[0] - c; u /= np.linalg.norm(u); w = np.cross(DIRS[i], u)
        on = on[np.argsort(np.arctan2((on - c) @ w, (on - c) @ u))]
        areas.append(0.5 * abs(sum(np.dot(np.cross(a - c, b - c), DIRS[i]) for a, b in zip(on, np.roll(on, -1, 0)))))
        s = 0.0
        for a, b in zip(on, np.roll(on, -1, 0)):
            num = np.dot(c, np.cross(a, b)); den = np.linalg.norm(c) * np.linalg.norm(a) * np.linalg.norm(b) + np.dot(c, a) * np.linalg.norm(b) + np.dot(c, b) * np.linalg.norm(a) + np.dot(a, b) * np.linalg.norm(c)
            s += 2 * math.atan2(num, den)
        om.append(abs(s))
    return np.array(areas), np.array(om)

def aequi_records():
    """every Aequus: name, idx, per-face depths, per-face orbit id."""
    recs = []
    for study in ("2026-11-19-aequi-complete", "2026-11-20-aequi-two-placements"):
        dd = os.path.join(ST, study, "data/dice")
        for f in sorted(os.listdir(dd)):
            d = json.load(open(os.path.join(dd, f))); idx = d["face_directions"]; idx = json.loads(idx) if isinstance(idx, str) else idx
            sz = d["orbit_sizes"]; sz = json.loads(sz) if isinstance(sz, str) else sz
            dp = d["depths_60_digits"]; dp = json.loads(dp.replace("'", '"')) if isinstance(dp, str) else dp
            dep = [float(dp[j]) for j, s in enumerate(sz) for _ in range(s)]; orb = [j for j, s in enumerate(sz) for _ in range(s)]
            recs.append(dict(name="%s:%d" % (study[:10], int(d["sid"])), group=d["group"], idx=idx, dep=dep, orb=orb))
    app = {r["no"]: r for r in json.load(open(os.path.join(ST, "2026-11-24-aequi-catalogue-2/app_dice.json")))}
    for no, r in sorted(app.items()):
        idx = [d for o in r["orbits"] for d in o]; dep = [r["depths"][j] for j, o in enumerate(r["orbits"]) for _ in o]
        orb = [j for j, o in enumerate(r["orbits"]) for _ in o]
        recs.append(dict(name="No.%d" % no, group=r["group"], idx=idx, dep=dep, orb=orb))
    return recs

def area_census(rec):
    try: A, om = faces_of(rec["idx"], rec["dep"])
    except Exception as ex: return dict(name=rec["name"], err=str(ex)[:80])
    fair = float(np.abs(om - 4 * np.pi / len(om)).max())
    if fair > 1e-9: return dict(name=rec["name"], err="not fair with these depths (%.1e): face order" % fair)
    P = DIRS[rec["idx"]]; w = A / A.sum()
    Rs = T.sym_group(P, T.labels(w)); dims = T.char_dims(Rs); c = T.classify(T.energies(P, w, 3), dims)
    c["beyond"] = [k for k in c["beyond"] if k != 1]   # degree 1 is forced by Minkowski (sum A_f n_f = 0), not by symmetry
    return dict(name=rec["name"], group=rec["group"], G=len(Rs), **c)

def poly_census(r):
    V = np.array(r["verts"], float); P = np.array(r["normals"], float); P /= np.linalg.norm(P, axis=1)[:, None]; A = []
    for f, n in zip(r["faces"], P):
        Q = V[f]; c = Q.mean(0); A.append(0.5 * abs(sum(np.dot(np.cross(a - c, b - c), n) for a, b in zip(Q, np.roll(Q, -1, 0)))))
    A = np.array(A); w = A / A.sum()
    Rs = T.sym_group(P, T.labels(w)); dims = T.char_dims(Rs); c = T.classify(T.energies(P, w, 3), dims)
    c["beyond"] = [k for k in c["beyond"] if k != 1]   # Minkowski
    return dict(name=r["name"], family=r.get("family"), G=len(Rs), **c)

def fingerprint(args):
    rec, k = args
    P = DIRS[rec["idx"]]; orb = np.array(rec["orb"]); m = orb.max() + 1
    Z = T.zonal(P @ P.T, 3)[k]
    Gm = np.array([[Z[np.ix_(orb == a, orb == b)].sum() for b in range(m)] for a in range(m)])
    norms = np.sqrt(np.clip(np.diag(Gm), 0, None)); carry = [int(a) for a in range(m) if norms[a] > 1e-6 * norms.max()] if norms.max() > 1e-9 else []
    rank = int(np.linalg.matrix_rank(Gm[np.ix_(carry, carry)], tol=1e-9 * norms.max() ** 2)) if carry else 0
    cos = [[round(float(Gm[a, b] / (norms[a] * norms[b])), 6) for b in carry] for a in carry]
    pattern = ("none" if not carry else "two opposed" if len(carry) == 2 and abs(cos[0][1] + 1) < 1e-6 else
               "%d orbits, rank %d" % (len(carry), rank))
    return dict(name=rec["name"], group=rec["group"], k=k, m=int(m), sizes=[int((orb == a).sum()) for a in range(m)],
                carrying=carry, rank=rank, cos=cos, pattern=pattern, total=float(Gm.sum()))

if __name__ == "__main__":
    recs = aequi_records(); byname = {r["name"]: r for r in recs}
    LIM = os.environ.get("LIMIT")
    if LIM: recs = recs[:int(LIM)]
    polys = json.load(open(os.path.join(HERE, "../data/polyhedra.json")))
    print("PROGRESS 0.05 sets: polyhedra %d, Aequi %d" % (len(polys), len(recs)), flush=True)
    with Pool(NP) as Pp:
        pa = Pp.map(poly_census, polys)
        print("PROGRESS 0.15 polyhedra done", flush=True)
        aa = []
        for i, r in enumerate(Pp.imap_unordered(area_census, recs, chunksize=16)):
            aa.append(r)
            if i % 1000 == 0: print("PROGRESS %.3f Aequi %d" % (0.15 + 0.7 * i / len(recs), i), flush=True)
    json.dump(pa, open(os.path.join(OUT, "area-poly.json"), "w")); json.dump(aa, open(os.path.join(OUT, "area-aequi.json"), "w"))
    # (B) the accidental pairs of variant (i)
    post = json.load(open(os.path.join(HERE, "../data/post.json")))
    acc = [(p["name"], int(k)) for p in post for k, c in p["covers"].items() if c is None]   # accidental: no exact cover (post.py)
    fp = [fingerprint((byname[n], k)) for n, k in acc if n in byname]
    json.dump(fp, open(os.path.join(OUT, "fingerprint.json"), "w"))
    from collections import Counter
    err = [r for r in aa if "err" in r]
    deg1 = all(1 in r["silent"] for r in pa) and all(1 in r["silent"] for r in aa if "err" not in r)
    beyond_p = [(r["name"], r["beyond"]) for r in pa if r["beyond"]]
    beyond_a = sum(1 for r in aa if "err" not in r and r["beyond"])
    print("(A) polyhedra beyond symmetry (area weights):", beyond_p)
    print("(A) Aequi rebuilt %d, errors %d, beyond symmetry %d" % (len(aa) - len(err), len(err), beyond_a))
    print("(A) control: degree 1 silent for every set (Minkowski):", deg1)
    print("(B) accidental pairs found %d (README: 286)" % len(acc))
    print("(B) patterns by degree:", {k: dict(Counter(f["pattern"] for f in fp if f["k"] == k)) for k in sorted({f["k"] for f in fp})})
    full = not os.environ.get("LIMIT")
    print("FINAL ok" if deg1 and not err and len(acc) == 286 and (len(fp) == 286 or not full) else "FINAL FAIL (control, errors or count)")
