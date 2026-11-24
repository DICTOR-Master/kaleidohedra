# Post-processing of the Aequi census: which beyond-symmetry silences are COMPOSITE, i.e. the die's face set (odd k) or its
# multiset of face axes (even k; even harmonics do not see the sign of a direction) splits into blocks, each a full orbit of
# some subgroup H of a frame group (Ih in either icosahedron placement, or Oh) that has no invariant harmonic of degree k?
# Such a silence is a sum of symmetry-forced silences of the pieces (exact: index sets + group theory). The rest are ACCIDENTAL.
# Accidental ones, and every die-degree pair with 0 < e_k < 1e-5, are then checked EXACTLY (exact_check.py).
# Usage: python post.py OUT.json   (env PROCS)
import os, sys, json, importlib.util, itertools
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tacitus as T
spec = importlib.util.spec_from_file_location("g", os.path.join(T.ST, "2026-11-24-aequi-certify-extend/scripts/groups.py"))
gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm)
DIRS = gm.DIRS; n = len(DIRS)
NEG = [gm.DKEY[tuple(np.round(-v, 6))] for v in DIRS]
AX = [min(i, NEG[i]) for i in range(n)]
Rz = gm.rot((0, 0, 1), np.pi / 2)
FRAMES = [gm.OH, gm.IH, [Rz @ g @ Rz.T for g in gm.IH]]

def subgroups(F):
    keys = {gm.key(g): g for g in F}; out = {}
    E = list(keys.values())
    for a, b in itertools.combinations_with_replacement(range(len(E)), 2):
        for extra in ([], [-np.eye(3)]):
            H = gm.closure([E[a], E[b]] + extra); k = frozenset(gm.key(h) for h in H)
            if k not in out: out[k] = H
    return list(out.values())

def blocks_for(H, k):
    """orbits of H on directions (odd k) or axes (even k), restricted to orbits staying inside DIRS."""
    perms = [gm.dperm(h) for h in H]; seen = set(); out = []
    for i in range(n):
        if i in seen: continue
        orb = {p[i] for p in perms}; seen |= orb
        if -1 in orb: continue
        if k % 2 == 0: orb = {AX[j] for j in orb}
        out.append(frozenset(orb))
    return out

def build_blocks():
    allH = {}
    for F in FRAMES:
        for H in subgroups(F): allH[frozenset(gm.key(h) for h in H)] = H
    B = {k: set() for k in range(1, T.KMAX + 1)}
    for H in allH.values():
        d = T.char_dims(H)
        for k in range(1, T.KMAX + 1):
            if d[k] == 0: B[k] |= set(blocks_for(H, k))
    return len(allH), {k: [sorted(b) for b in v] for k, v in B.items()}

def cover(need, blocks):
    """exact cover of the multiset need (dict id -> count) by blocks (sets), blocks reusable."""
    if not need: return []
    e = min(need, key=lambda x: sum(1 for b in blocks if x in b))
    for b in blocks:
        if e in b and all(need.get(x, 0) > 0 for x in b):
            nn = dict(need)
            for x in b:
                nn[x] -= 1
                if not nn[x]: del nn[x]
            r = cover(nn, blocks)
            if r is not None: return [b] + r
    return None

BL = None
def work(r):
    idx = r["idx"]; res = {}
    for k in r["i"]["beyond"]:
        if k % 2 == 0:
            need = {}
            for i in idx: need[AX[i]] = need.get(AX[i], 0) + 1
        else: need = {i: 1 for i in idx}
        cand = [set(b) for b in BL[k] if set(b) <= set(need)]
        c = cover(need, cand)
        res[k] = None if c is None else [sorted(b) for b in c]
    P = DIRS[idx]; e = T.energies(P, np.ones(len(P)), 3)
    small = [(k, e[k]) for k in range(1, T.KMAX + 1) if T.ZERO < e[k] < 1e-5]
    return dict(name=r["name"], label=r["label"], group=r["group"], tags=r["tags"], idx=idx, beyond=r["i"]["beyond"], covers=res, small=small)

if __name__ == "__main__":
    nH, BL = build_blocks()
    print("frame subgroups", nH, "| forced blocks per degree", {k: len(v) for k, v in BL.items()}, flush=True)
    # face index lists in the same order as the census
    sets = T.aequi_sets(); D = os.path.join(HERE, "..", "data")
    res = {}
    for i in range(3):
        for j, l in enumerate(open(os.path.join(D, "aequi-%d.jsonl" % i))):
            r = json.loads(l); res[r["name"]] = r
    key = {tuple(np.round(v, 6)): t for t, v in enumerate(DIRS)}
    todo = []
    for s in sets:
        r = res[s["name"]]; r["idx"] = [key[tuple(np.round(v, 6))] for v in np.array(s["normals"])]
        todo.append(r)
    import multiprocessing as mpc
    with mpc.get_context("fork").Pool(int(os.environ.get("PROCS", "4"))) as pool:
        out = list(pool.map(work, todo, chunksize=20))
    keep = [o for o in out if o["beyond"] or o["small"]]
    json.dump(keep, open(sys.argv[1], "w"))
    comp = sum(1 for o in keep for k, c in o["covers"].items() if c is not None)
    acc = [(o["name"], o["label"], k) for o in keep for k, c in o["covers"].items() if c is None]
    print("beyond pairs: composite", comp, "accidental", len(acc)); print("accidental:", acc[:60])
    print("near misses 1e-11 < e < 1e-5:", sum(len(o["small"]) for o in keep))
    nb = sum(len(o["beyond"]) for o in keep)
    print("FINAL ok" if comp + len(acc) == nb and nb > 0 else "FINAL FAIL pair count")
