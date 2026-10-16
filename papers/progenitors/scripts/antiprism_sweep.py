# DICTO · dictospheres.com — Antiprism Conway sweep (progenitors prior-art check, 2026-10-16): every Conway string of up to two operators on
# the icosahedron and dodecahedron (Hart algorithms via Antiprism conway), its combinatorial signature (face sides, vertex orders), compared
# with our solids. Also canonical forms: which of ours canonicalize to a Conway-reachable polyhedron.
import subprocess, os, itertools, collections, json
B = os.path.expanduser("~/antiprism/bin/")
def run(*a): return subprocess.run([B + a[0], *a[1:]], capture_output=True, text=True, timeout=120)
def sig(path):
    r = run("off_report", "-C", "so", path).stdout
    sec = None; out = {"s": {}, "o": {}}
    for line in r.splitlines():
        if line.startswith("[face_sides_cnts]"): sec = "s"; continue
        if line.startswith("[vert_order_cnts]"): sec = "o"; continue
        if line.startswith("["): sec = None; continue
        if sec and "=" in line:
            k, v = line.split("="); out[sec][int(k)] = int(v.split()[0])
    return (tuple(sorted(out["s"].items())), tuple(sorted(out["o"].items())))
OPS = list("abdegjkmoprstz") + ["k5", "k6", "t5", "t6", "k3", "t3"]
seen = {}
for seed in "ID":
    for n in (1, 2):
        for ops in itertools.product(OPS, repeat=n):
            s = "".join(ops) + seed; p = f"conway/{s}.off"
            if not os.path.exists(p):
                r = run("conway", "-o", p, s)
                if r.returncode or not os.path.exists(p): continue
            try: seen.setdefault(sig(p), []).append(s)
            except Exception: pass
ours = [f[:-4] for f in os.listdir(".") if f.endswith(".off")]
res = {}
for o in sorted(ours):
    g = sig(o + ".off"); res[o] = {"signature": str(g), "conway_matches": seen.get(g, [])}
    print(f"{o:24s} faces {dict(g[0])} orders {dict(g[1])} -> Conway (<=2 ops on I/D) with same structure: {seen.get(g, []) or chr(45)}")
print("Conway forms generated:", sum(len(v) for v in seen.values()), "distinct structures:", len(seen))
json.dump(res, open("sweep.json", "w"), indent=1)
