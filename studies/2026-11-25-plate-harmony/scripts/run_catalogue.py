"""Harmony tests on the Vacuus and Resonus of the 163 catalogue polyhedra (data/catalogue-normals.json).
Identical arrangements (same field, same plane set) are computed once. Cross-checks against the catalogue study: number of
regions and the simplicial flag must agree for every arrangement. Writes data/catalogue-harmony.json."""
import os, sys, json, time
import multiprocessing as mpr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from nf import NF
from harmony import analyse
CAT = os.path.normpath(os.path.join(HERE, "../../2026-11-24-vacuus-resonus-catalogue"))
_F = {}


def field(fd):
    k = (tuple(fd["g"]), fd["eta"][:40])
    if k not in _F: _F[k] = NF(fd["g"], fd["eta"])
    return _F[k]


def job(arg):
    key, fd, normals = arg
    t0 = time.time()
    try:
        F = field(fd)
        N = [tuple(F.from_coeffs(c) for c in v) for v in normals]
        return key, analyse(F, N), None
    except Exception as e:
        import traceback
        return key, None, traceback.format_exc()


if __name__ == "__main__":
    rows = json.load(open(os.path.join(STUDY, "data/catalogue-normals.json")))
    ref = {r["name"]: r for r in json.load(open(os.path.join(CAT, "data/catalogue-all.json")))}
    only = sys.argv[1:]
    if only: rows = [r for r in rows if any(o == r["name"] or r["name"].startswith(o + "_") for o in only)]
    uniq = {}; use = []
    for r in rows:
        for kind in ("vacuus", "resonus", "vacuus_volume"):
            if kind not in r: continue
            k = json.dumps([r["field"]["g"], sorted(json.dumps(v) for v in r[kind])])
            uniq.setdefault(k, (k, r["field"], r[kind]))
            use.append((r["name"], r["family"], kind, k))
    print("arrangements", len(use), "distinct", len(uniq), flush=True)
    procs = int(os.environ.get("PROCS", "8"))
    res = {}; bad = 0
    order = sorted(uniq.values(), key=lambda a: -len(a[2]))
    with mpr.get_context("fork").Pool(procs) as pool:
        for i, (k, o, err) in enumerate(pool.imap_unordered(job, order)):
            if err: bad += 1; print("ERROR", err, flush=True); continue
            res[k] = o
            print(f"PROGRESS {(i + 1) / len(order):.3f} planes {o['planes']} ({o['secs']} s)", flush=True)
    out = []; mism = 0
    for name, fam, kind, k in use:
        if k not in res: continue
        o = dict(res[k]); o["name"] = name; o["family"] = fam; o["arrangement"] = kind
        c = ref[name]; a = c.get("volume" if kind == "vacuus_volume" else "corner", c)
        arr = a["vacuus_arr" if kind.startswith("vacuus") else "resonus_arr"]
        if arr.get("regions") != o.get("regions") or bool(arr.get("simplicial")) != bool(o.get("simplicial")):
            mism += 1; print("MISMATCH", name, kind, arr.get("regions"), o.get("regions"), arr.get("simplicial"), o.get("simplicial"), flush=True)
        out.append(o)
    tag = "-pilot" if only else ""
    json.dump(out, open(os.path.join(STUDY, f"data/catalogue-harmony{tag}.json"), "w"), indent=0, default=str)
    print("rows", len(out), "errors", bad, "mismatches", mism, flush=True)
    if bad == 0 and mism == 0 and (only or len(out) == len(use) == 168 * 2 + 92):
        print("FINAL ok catalogue harmony", len(out), flush=True)
