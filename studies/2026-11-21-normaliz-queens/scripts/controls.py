"""Target 1 controls: exact hulls of the 600-cell and the 120-cell over Q(sqrt5) with Normaliz + e-antic.
Checks (all exact): vertex counts 120 / 600; facet counts 600 / 120; vertices per facet 4 / 20; f-vectors
(120,720,1200,600) and (600,1200,720,120); every facet normal of one is parallel to a vertex of the other (duality);
all points on the right side of every facet."""
import json, sys, time
from collections import Counter
from qphi import dot, QP
from polys import cell600, cell120
import nz

t0 = time.time(); ok = True; rec = {}


def check(name, V, nv, nf, per, fv):
    global ok
    C = nz.hull(V)
    Vn = nz.verts(C); F = nz.facets(C); fvec = C.FVector()
    inc = nz.incid(F, V)
    sides = all((dot(n, v) + c).sign() >= 0 for n, c in F for v in V)
    per_c = Counter(len(x) for x in inc)
    r = {"input_points": len(V), "vertices": len(Vn), "facets": len(F), "vertices_per_facet": dict(per_c),
         "f_vector": fvec, "all_points_inside": sides,
         "same_vertex_set": set(Vn) == set(V), "seconds": round(time.time() - t0, 1)}
    good = (len(Vn) == nv and len(F) == nf and dict(per_c) == {per: nf} and fvec[1:5] == fv and sides
            and set(Vn) == set(V))
    r["ok"] = good; ok &= good
    print(name, json.dumps(r), flush=True)
    return F, r


V6 = cell600(); V1 = cell120()
print("PROGRESS 0.05 vertex lists", len(V6), len(V1), flush=True)
F6, rec["600-cell"] = check("600-cell", V6, 120, 600, 4, [120, 720, 1200, 600])
print("PROGRESS 0.4 600-cell hull", flush=True)
F1, rec["120-cell"] = check("120-cell", V1, 600, 120, 20, [600, 1200, 720, 120])
print("PROGRESS 0.8 120-cell hull", flush=True)


def gram(P):
    # multiset of cosines p_i.p_j / p_i.p_i from the first point (all points on one sphere: exact in Q(phi))
    p0 = P[0]; r2 = dot(p0, p0)
    return Counter(dot(p0, q) / r2 for q in P), all(dot(q, q) == r2 for q in P)


# duality: the polar points -n/c0 of each solid's facets lie on one sphere and have the vertex cosine pattern of the other
pol6 = [tuple(x / (-c) for x in n) for n, c in F6]
pol1 = [tuple(x / (-c) for x in n) for n, c in F1]
g6, s6 = gram(pol6); g1, s1 = gram(pol1)
d1 = s6 and g6 == gram(V1)[0]   # 600 polar points of the 600-cell ~ 120-cell vertices
d2 = s1 and g1 == gram(V6)[0]   # 120 polar points of the 120-cell ~ 600-cell vertices
rec["duality"] = {"600-cell polar = 120-cell (sphere + cosine pattern)": d1,
                  "120-cell polar = 600-cell (sphere + cosine pattern)": d2}
print("duality", rec["duality"], flush=True)
ok &= d1 and d2
# facet distance for the 600-cell (radius 2): c0^2/|n|^2 = inradius^2
n, c = F6[0]; rec["600-cell inradius^2"] = (c * c / dot(n, n)).s5()
n, c = F1[0]; rec["120-cell inradius^2"] = (c * c / dot(n, n)).s5()
print("inradius^2", rec["600-cell inradius^2"], rec["120-cell inradius^2"], flush=True)
json.dump(rec, open(sys.argv[1] if len(sys.argv) > 1 else "../data/controls.json", "w"), indent=1)
print("PROGRESS 1.0 done", round(time.time() - t0, 1), "s", flush=True)
print("FINAL ok" if ok else "FINAL FAIL", flush=True)
