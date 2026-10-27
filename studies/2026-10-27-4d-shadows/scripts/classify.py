"""Compare every all-triangle shadow / layer / slice with the 8 convex deltahedra (graph isomorphism) and with
named triangulations; test the other face patterns for an equilateral (deltahedral) realisation.

Exact parts: graph isomorphism (networkx, combinatorial), edge-length and dihedral data (from shadows.py).
Numerical part (marked so in the output): Levenberg-Marquardt search for an equilateral realisation, the method of
Tsuruta et al. 2014, started from the shadow itself, then float checks for self-intersection and flat edges.
Run on dicto-big-brother after shadows.py:  ~/geom/bin/python classify.py
"""
import json
import math
import pickle
from collections import Counter

import networkx as nx
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial import ConvexHull

PHI = (1 + 5 ** 0.5) / 2


def hull_graph(P):
    H = ConvexHull(np.asarray(P, float))
    G = nx.Graph()
    for s in H.simplices:
        for i in range(3):
            G.add_edge(int(s[i]), int(s[(i + 1) % 3]))
    return G, H


def snub_disphenoid():
    """D2d template, edges forced equal by least squares; the result is checked to be equilateral."""
    def pts(p):
        x1, z1, u, w = p
        return np.array([[x1, 0, z1], [-x1, 0, z1], [0, x1, -z1], [0, -x1, -z1],
                         [u, 0, -w], [-u, 0, -w], [0, u, w], [0, -u, w]])
    p0 = np.array([0.5, 1.0, 1.0, 0.3])
    G, _ = hull_graph(pts(p0))
    E = list(G.edges())

    def res(p):
        P = pts(p)
        L = np.array([np.linalg.norm(P[a] - P[b]) for a, b in E])
        return L - 1.0
    s = least_squares(res, p0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    P = pts(s.x)
    G2, _ = hull_graph(P)
    L = [np.linalg.norm(P[a] - P[b]) for a, b in G2.edges()]
    assert max(abs(x - 1) for x in L) < 1e-9 and nx.is_isomorphic(G, G2)
    assert sorted(d for _, d in G2.degree()) == [4, 4, 4, 4, 5, 5, 5, 5]
    return G2


def references():
    R = {}
    R["tetrahedron"] = nx.complete_graph(4)
    tri = [[math.cos(2 * math.pi * k / 3), math.sin(2 * math.pi * k / 3), 0] for k in range(3)]
    R["triangular bipyramid (J12)"] = hull_graph(tri + [[0, 0, 0.8], [0, 0, -0.8]])[0]
    R["octahedron"] = nx.octahedral_graph()
    pen = [[math.cos(2 * math.pi * k / 5), math.sin(2 * math.pi * k / 5), 0] for k in range(5)]
    R["pentagonal bipyramid (J13)"] = hull_graph(pen + [[0, 0, 0.6], [0, 0, -0.6]])[0]
    R["snub disphenoid (J84)"] = snub_disphenoid()
    pr = [[math.cos(2 * math.pi * k / 3), math.sin(2 * math.pi * k / 3), z] for k in range(3) for z in (-0.5, 0.5)]
    caps = [[1.3 * math.cos(2 * math.pi * k / 3 + math.pi / 3), 1.3 * math.sin(2 * math.pi * k / 3 + math.pi / 3), 0]
            for k in range(3)]
    R["triaugmented triangular prism (J51)"] = hull_graph(pr + caps)[0]
    sq = [[math.cos(math.pi / 2 * k + (math.pi / 4) * (z > 0)), math.sin(math.pi / 2 * k + (math.pi / 4) * (z > 0)), z]
          for k in range(4) for z in (-0.42, 0.42)]
    R["gyroelongated square bipyramid (J17)"] = hull_graph(sq + [[0, 0, 1.2], [0, 0, -1.2]])[0]
    R["icosahedron"] = nx.icosahedral_graph()
    degs = {"tetrahedron": "3333", "triangular bipyramid (J12)": "44433", "octahedron": "444444",
            "pentagonal bipyramid (J13)": "5544444", "snub disphenoid (J84)": "55554444",
            "triaugmented triangular prism (J51)": "555555444", "gyroelongated square bipyramid (J17)": "5555555544",
            "icosahedron": "555555555555"}
    for k, g in R.items():
        assert nx.check_planarity(g)[0]
        assert "".join(str(d) for d in sorted((d for _, d in g.degree()), reverse=True)) == degs[k], k
        assert g.number_of_edges() == 3 * g.number_of_nodes() - 6, k
    sizes = sorted(g.number_of_nodes() for g in R.values())
    assert sizes == [4, 5, 6, 7, 8, 9, 10, 12]
    return R


def named():
    """Named triangulations used to identify the larger patterns (built exactly as convex hulls, checked)."""
    N = {}
    for n in (6, 10):
        ring = [[math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n), 0] for k in range(n)]
        N[f"{n}-gonal bipyramid"] = hull_graph(ring + [[0, 0, 0.5], [0, 0, -0.5]])[0]
    ico = np.array([[0, s1, s2 * PHI] for s1 in (1, -1) for s2 in (1, -1)])
    ico = np.vstack([np.roll(ico, k, axis=1) for k in range(3)])
    dod = []
    for s in np.array(np.meshgrid([1, -1], [1, -1], [1, -1])).T.reshape(-1, 3):
        dod.append(s)
    for s1 in (1, -1):
        for s2 in (1, -1):
            for k in range(3):
                dod.append(np.roll([0, s1 / PHI, s2 * PHI], k))
    dod = np.array(dod, float)
    # pentakis dodecahedron: dodecahedron + 12 points over the face centres (directions of icosahedron vertices)
    # dodecahedron above has edge 2/phi and inradius 1.3764; apices on the 12 face normals at radius 1.5
    Hd = ConvexHull(dod)
    normals = np.unique(np.round(Hd.equations[:, :3], 8), axis=0)
    assert len(normals) == 12
    N["pentakis dodecahedron"] = hull_graph(np.vstack([dod, normals * 1.5]))[0]
    # pentakis icosidodecahedron (frequency-2 geodesic icosahedron): icosahedron + edge midpoints pushed out
    G0, _ = hull_graph(ico)
    mids = [(ico[a] + ico[b]) / 2 for a, b in G0.edges()]
    mids = [m / np.linalg.norm(m) * np.linalg.norm(ico[0]) for m in mids]
    N["pentakis icosidodecahedron"] = hull_graph(np.vstack([ico, mids]))[0]
    assert sorted(d for _, d in N["pentakis dodecahedron"].degree()) == [5] * 12 + [6] * 20
    assert sorted(d for _, d in N["pentakis icosidodecahedron"].degree()) == [5] * 12 + [6] * 30
    return N


# ----------------------------------------------------------------- numerical equilateral realisation (screening)
def seg_tri(p, q, a, b, c, eps=1e-9):
    n = np.cross(b - a, c - a)
    dp, dq = np.dot(n, p - a), np.dot(n, q - a)
    if dp * dq > -eps * eps:
        return False
    t = dp / (dp - dq)
    x = p + t * (q - p)
    for u, v in ((a, b), (b, c), (c, a)):
        if np.dot(np.cross(v - u, x - u), n) < eps:
            return False
    return True


def self_intersects(P, F):
    for i, f in enumerate(F):
        for j, g in enumerate(F):
            if i == j:
                continue
            for k in range(3):
                p, q = f[k], f[(k + 1) % 3]
                if p in g or q in g:
                    continue
                if seg_tri(P[p], P[q], P[g[0]], P[g[1]], P[g[2]]):
                    return True
    return False


def dihedrals(P, F):
    """interior dihedral angles (deg) of an oriented closed triangle surface (faces ccw from outside)."""
    N = {}
    for i, f in enumerate(F):
        n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]])
        N[i] = n / np.linalg.norm(n)
    ef = {}
    for i, f in enumerate(F):
        for k in range(3):
            ef.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(i)
    out = []
    for e, (i, j) in ef.items():
        r = next(v for v in F[j] if v not in e)
        a = next(iter(e))
        convex = np.dot(N[i], P[r] - P[a]) < 0
        ang = math.degrees(math.acos(max(-1, min(1, np.dot(N[i], N[j])))))
        out.append(180 - ang if convex else 180 + ang)
    return out


def signed_volume(P, F):
    return sum(np.dot(P[f[0]], np.cross(P[f[1]], P[f[2]])) for f in F) / 6


def equilateral_search(P0, F, E, tries=12, seed=1):
    rng = np.random.default_rng(seed)
    P0 = np.asarray(P0, float)
    L0 = np.mean([np.linalg.norm(P0[a] - P0[b]) for a, b in E])
    P0 = (P0 - P0.mean(0)) / L0
    found = []
    from scipy.sparse import lil_matrix
    sparsity = lil_matrix((len(E), 3 * len(P0)), dtype=int)
    for r_, (a, b) in enumerate(E):
        sparsity[r_, 3 * a:3 * a + 3] = 1
        sparsity[r_, 3 * b:3 * b + 3] = 1

    def res(x):
        P = x.reshape(-1, 3)
        return np.array([np.linalg.norm(P[a] - P[b]) - 1 for a, b in E])
    for t in range(tries):
        x0 = P0 + (0 if t == 0 else 0.15 * rng.standard_normal(P0.shape))
        s = least_squares(res, x0.ravel(), method="trf", jac_sparsity=sparsity, xtol=1e-15, ftol=1e-15, gtol=1e-15,
                          max_nfev=3000)
        P = s.x.reshape(-1, 3)
        r = np.abs(res(s.x)).max()
        if r > 1e-10:
            continue
        D = dihedrals(P, F)
        flat = min(abs(d - 180) for d in D)
        mind = min(np.linalg.norm(P[i] - P[j]) for i in range(len(P)) for j in range(i + 1, len(P)))
        if flat < 1e-4 or mind < 1e-3 or signed_volume(P, F) <= 0 or self_intersects(P, F):
            continue
        conv = max(D) < 180
        found.append({"try": t, "residual": float(r), "convex": bool(conv), "min_dihedral": min(D),
                      "max_dihedral": max(D), "reflex_edges": sum(1 for d in D if d > 180), "P": P.tolist()})
        break
    return found


def main():
    S = pickle.load(open("data/solids.pkl", "rb"))
    R = references()
    N = named()
    rows = []
    seen = {}
    for s in S:
        it = s["item"]
        if not it["all_triangles"]:
            continue
        G = nx.Graph()
        G.add_edges_from(s["E"])
        match = [k for k, g in R.items() if nx.is_isomorphic(G, g)]
        nm = [k for k, g in N.items() if nx.is_isomorphic(G, g)]
        key = (it["polytope"], tuple(sorted(it["edge_len2_exact"])), tuple(it["edge_len_count"]),
               tuple(it["dihedral_cos2_exact"]), nx.weisfeiler_lehman_graph_hash(G, iterations=4))
        row = {k: it.get(k) for k in ("polytope", "direction", "kind", "height", "central", "V", "E", "F",
                                      "degrees", "edge_len2_exact", "edge_len_count", "edge_ratio2_exact",
                                      "edge_ratio", "dihedral_cos2_exact", "dihedral_deg", "dihedral_count")}
        if not isinstance(row["degrees"], str):
            c = Counter(row["degrees"])
            row["degrees"] = " ".join(f"{d}^{m}" for d, m in sorted(c.items(), reverse=True))
        row["convex_deltahedron_graph"] = match[0] if match else None
        row["named_graph"] = nm[0] if nm else None
        row["regular"] = it["edge_ratio2_exact"] == "1"
        row["same_data_as"] = seen.get(key)
        if key not in seen:
            seen[key] = f'{it["polytope"]} {it["direction"]} {it["kind"]} {it.get("height")}'
        rows.append(row)
        if not match and row["same_data_as"] is None and row["named_graph"] is None:
            F = s["faces"]
            res = equilateral_search(np.array(s["fV"]), F, s["E"])
            row["equilateral_search_numerical"] = ({k: v for k, v in res[0].items() if k != "P"} if res
                                                   else "none found in 12 starts")
            if res:
                np.save(f'data/eqreal_{it["polytope"]}_{it["direction"]}_{it["kind"]}_{len(rows)}.npy',
                        np.array(res[0]["P"]))
        print(row["polytope"], row["direction"], row["kind"], row["height"], row["V"], row["degrees"],
              row["edge_ratio"], row["convex_deltahedron_graph"], row["named_graph"], row["same_data_as"],
              row.get("equilateral_search_numerical"), flush=True)
    json.dump(rows, open("data/all-triangle-matches.json", "w"), indent=1)


if __name__ == "__main__":
    main()
