# og_vacuus_lean.py, DICTO 11 Nov 2026 ("we did vacuus survey earlier of all the shapes", #87 DICTO Vacuus Solids): in D_k's Vacuus each
# face i has its centre pyramid (apex O); the foot point d_i n_i lies on the pyramid's axis, INSIDE its own face (upright pyramid) or
# OUTSIDE it (leaning pyramid). Test: cut at hop k  <=>  leaning?  (and how far outside: lean = distance of the foot point from its face
# polygon, relative to the face size). Control: cut counts match cut_lemma / og_sweep.
# usage: python -u og_vacuus_lean.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); KM = int(sys.argv[2]); OUTJ = os.path.abspath(sys.argv[3])
src = open(os.path.join(here, 'og_sweep.py')).read().split('rows_out = []')[0]
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(src)
from scipy.spatial import ConvexHull, cKDTree
KNOWN = {5: 60, 6: 60, 7: 90, 8: 0, 9: 252, 10: 192, 11: 132, 12: 252, 13: 192, 14: 552}
def face_polys(V):
    """face planes (merged) with their corner polygons."""
    h = ConvexHull(V); E = h.equations; n = len(E); par = np.arange(n)
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), []).append(f)
    out = []
    for fs in grp.values():
        m = E[fs, :3].mean(0); m /= np.linalg.norm(m); d = -E[fs, 3].mean()
        pts = sorted(set(int(j) for f in fs for j in h.simplices[f])); out.append((m, d, V[pts]))
    return out
def inside_poly(p, m, P):
    """signed lean: >0 = foot point outside the face polygon by that distance (relative to face size); <=0 inside."""
    c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]; Q = (P - c0) @ B.T; q = B @ (p - c0)
    hh = ConvexHull(Q); E = hh.equations; size = np.linalg.norm(Q, axis=1).max()
    return float((E[:, :2] @ q + E[:, 2]).max() / size)
rows = []; ok = True; V = OGf
for k in range(KM + 1):
    FP = face_polys(V)
    W = np.array([m * d for m, d, _ in FP]); FN = faces(W); act = np.zeros(len(W), bool); act[FN[2]] = True
    lean = np.array([inside_poly(m * d, m, P) for m, d, P in FP]); leaning = lean > 1e-9
    cut = ~act; both = int((cut & leaning).sum()); cut_up = int((cut & ~leaning).sum()); act_lean = int((~cut & leaning).sum())
    if k in KNOWN: ok &= int(cut.sum()) == KNOWN[k]
    rows.append(dict(k=k, faces=len(W), cut=int(cut.sum()), leaning=int(leaning.sum()), cut_and_leaning=both, cut_upright=cut_up, active_leaning=act_lean,
                     lean_cut_min=float(lean[cut].min()) if cut.any() else None, lean_active_max=float(lean[~cut].max())))
    print(f"k {k:2d}: faces {len(W):5d} | cut {int(cut.sum()):4d} | leaning {int(leaning.sum()):4d} | cut&leaning {both:4d}, cut but upright {cut_up:4d}, survive though leaning {act_lean:4d} "
          f"| lean of cut faces min {rows[-1]['lean_cut_min'] if cut.any() else float('nan'):+.4f}, of survivors max {rows[-1]['lean_active_max']:+.4f}", flush=True)
    V = symmetrise(W)
json.dump(rows, open(OUTJ, 'w'), indent=1)
print('cut <=> leaning at every level:', all(r['cut_upright'] == 0 and r['active_leaning'] == 0 for r in rows))
print('FINAL ok' if ok else 'FINAL FAIL: cut counts differ from cut_lemma / og_sweep')
