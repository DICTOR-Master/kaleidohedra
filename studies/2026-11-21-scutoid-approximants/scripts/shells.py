"""Step 2: cluster shells around a cluster centre of a cubic approximant cell (cells/cell_<id>.json).
Atoms within RMAX of the centre (periodic images included) are grouped into shells (radial gap > GAP Angstrom between consecutive
distances starts a new shell).  Each shell is matched to the ideal icosahedral polyhedra in the T_h setting of the amber sweep
(solids.py: icosahedron vertices (0, 1, phi) cyclic with signs = setting A; its 90-degree turn about z (0, phi, 1) cyclic = setting B):
for each candidate vertex set (unit directions) and each setting, every atom direction is paired with the nearest ideal direction;
reported: the setting, the largest angular deviation, radial mean and spread.  Usage: python -I shells.py CELL.json CX CY CZ [RMAX]"""
import sys, json, itertools
import numpy as np
P = (1 + 5 ** 0.5) / 2
GAP = 0.25

def orbit(base):
    out = []
    for b in base:
        for sg in itertools.product((1, -1), repeat=3):
            t = [b[i] * sg[i] for i in range(3)]
            for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
                if not any(np.allclose(c, o) for o in out): out.append(c)
    return np.array(out, float)

IDEAL = {"icosahedron": orbit([(0, 1, P)]), "dodecahedron": orbit([(1, 1, 1), (0, 1 / P, P)]),
         "icosidodecahedron": orbit([(0, 0, P), (0.5, P / 2, P * P / 2)]),
         "truncated_icosahedron": orbit([(0, 1, 3 * P), (1, 2 + P, 2 * P), (P, 2, 2 * P + 1)]),
         "triacontahedron_vertices(dodeca+icosa)": None,
         "triacontahedron_edge_midpoints(=icosidodecahedron dirs)": None}
IDEAL["triacontahedron_vertices(dodeca+icosa)"] = np.vstack([IDEAL["dodecahedron"], IDEAL["icosahedron"]])
del IDEAL["triacontahedron_edge_midpoints(=icosidodecahedron dirs)"]

def unit(X): return X / np.linalg.norm(X, axis=1, keepdims=True)
def settingB(X): return X[:, [1, 0, 2]] * np.array([-1, 1, 1])   # 90 deg about z: (x, y, z) -> (-y, x, z)

def match(D, ideal):
    """D unit directions (n,3); ideal (m,3) unit; returns max angle (deg) of nearest pairing and whether it is a bijection when n == m"""
    c = np.clip(D @ ideal.T, -1, 1); j = c.argmax(1); ang = np.degrees(np.arccos(c.max(1)))
    return float(ang.max()), len(set(j.tolist())) == len(D)

def shells(cell, centre, rmax):
    a = cell["a"]; X = np.array([t["cart"] for t in cell["atoms"]]); C = np.array(centre) * a
    pts = []
    for n in itertools.product((-1, 0, 1), repeat=3):
        Y = X + np.array(n) * a - C; d = np.linalg.norm(Y, axis=1)
        for i in np.where((d < rmax) & (d > 1e-6))[0]: pts.append((d[i], i, Y[i]))
    pts.sort(key=lambda t: t[0])
    out, cur = [], [pts[0]]
    for p in pts[1:]:
        if p[0] - cur[-1][0] > GAP: out.append(cur); cur = [p]
        else: cur.append(p)
    out.append(cur)
    res = []
    for sh in out:
        r = np.array([p[0] for p in sh]); V = np.array([p[2] for p in sh]); D = unit(V)
        labs = sorted({cell["atoms"][p[1]]["label"] for p in sh})
        occ = [cell["atoms"][p[1]]["occ"] for p in sh]
        best = None
        for name, I in IDEAL.items():
            if len(I) != len(sh): continue
            for st, J in (("A", unit(I)), ("B", unit(settingB(I)))):
                m, bij = match(D, J)
                if bij and (best is None or m < best[2]): best = (name, st, m)
        res.append(dict(n=len(sh), r_mean=float(r.mean()), r_min=float(r.min()), r_max=float(r.max()), labels=labs,
                        occ_min=float(min(occ)), match=best, vectors=V.tolist()))
    return res

if __name__ == "__main__":
    cell = json.load(open(sys.argv[1])); c = [float(x) for x in sys.argv[2:5]]; rmax = float(sys.argv[5]) if len(sys.argv) > 5 else 9.0
    print(f"{cell['cif']} a={cell['a']} {cell['space_group']} centre {c}")
    for s in shells(cell, c, rmax):
        m = s["match"]
        print(f"  n={s['n']:3d} r={s['r_mean']:.3f} [{s['r_min']:.3f},{s['r_max']:.3f}] occ_min={s['occ_min']:.2f} {','.join(s['labels'])[:50]:50s} "
              + (f"{m[0]} setting {m[1]} max dev {m[2]:.2f} deg" if m else "-"))
