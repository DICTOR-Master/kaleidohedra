# exact description of a chosen tile: faces with side lengths^2 (real metric), exact convexity (every merged face is a facet of the hull)
import sys, json
from fractions import Fraction as Fr
from tiles import tile
import exactfaces as E
from connect import shift
def desc(t, lam, tr):
    w, L = {"c": ("ABC", 1), "h": ("AB", 0)}[t]
    P = [shift(p[3], tr[i]) for i, p in enumerate(tile(w, L, lam)[0])]
    F = E.union_faces(P); V = sorted({p for f in F for lp in f["loops"] for p in lp})
    H = E.facets(V); hp = {(n, c) for n, c, _ in H}
    convex = len(H) == len(F) and all((f["n"], f["c"]) in hp for f in F)
    out = []
    for f in F:
        lp = f["loops"][0]; s = [str(E.len2(E.sub(lp[(i+1)%len(lp)], lp[i]))) for i in range(len(lp))]
        out.append((len(lp), s, len(f["loops"])-1))
    return dict(tile=t, lam=str(lam), faces=len(F), vertices=len(V), convex_exact=convex, face_sides_len2=sorted(out),
                verts=[[str(x) for x in p] for p in V])
if __name__ == "__main__":
    lam = Fr(sys.argv[1]); print(json.dumps(desc(sys.argv[2], lam, json.loads(sys.argv[3]))))
