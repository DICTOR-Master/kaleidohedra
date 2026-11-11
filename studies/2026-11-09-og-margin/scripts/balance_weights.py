# balance_weights.py, DICTO 11 Nov 2026 ("check all the different balance laws for all the 4D polytopes and figure out if this may be
# an expression of a new law"). The metric balance laws that carry WEIGHTS, split over the hop's cut vs active candidates.
# Candidate = face F of D_k (= corner v = m/d of X_k = polar D_k). Cut iff its foot point d*m is not a corner of D_{k+1}.
# Per candidate:  A    = area of F                                  (Minkowski: sum A m = 0)
#                 om   = solid angle F subtends at O                (= Descartes defect of X_k at v; sum = 4 pi)
#                 tau  = interior solid angle of X_k at v = 2 pi - sum of arcs between consecutive corner directions of F
#                                                               (Gram: sum tau/4pi - sum dihedral/2pi + F/2 - 1 = 0)
#                 vol  = cone volume d A / 3                         (sum = vol D_k)
#                 d    = face distance
# Checks (each level): sum om = 4 pi; Minkowski |sum A m| small; sum vol = hull volume; Gram relation for X_k; foot points of the
# merged faces = the listed candidates (count). Prints cut/active shares of each weight, and max(cut) vs min(active) per weight.
# usage: python -u balance_weights.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json
import numpy as np
from scipy.spatial import cKDTree, ConvexHull
OUT = os.path.abspath(sys.argv[3]); here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, 'og_sweep.py')).read().split('def death(')[0])

def tri_solid(a, b, c):
    """solid angle of the triangle abc seen from O (Van Oosterom-Strackee)."""
    na, nb, nc = np.linalg.norm(a), np.linalg.norm(b), np.linalg.norm(c)
    num = abs(np.dot(a, np.cross(b, c)))
    den = na * nb * nc + np.dot(a, b) * nc + np.dot(a, c) * nb + np.dot(b, c) * na
    return 2 * np.arctan2(num, den)

def face_data(V, M, Dd):
    """per merged face, from the hull's triangles grouped by plane (robust to near-coplanar corners): area, subtended solid angle,
    polar interior angle (2 pi - arcs along the face's boundary edges), cone volume, distance, corner count; plus D_k's edges."""
    h = ConvexHull(V); nrm = h.equations[:, :3]
    _, gid = cKDTree(M).query(nrm)                       # merged face each hull triangle belongs to
    F = len(M); area = np.zeros(F); om = np.zeros(F); ecount = [dict() for _ in range(F)]
    for t, (i, j, l) in enumerate(h.simplices):
        a, b, c = V[i], V[j], V[l]; g = gid[t]
        area[g] += 0.5 * np.linalg.norm(np.cross(b - a, c - a)); om[g] += tri_solid(a, b, c)
        for p, q in ((i, j), (j, l), (l, i)):
            e = (min(p, q), max(p, q)); ecount[g][e] = ecount[g].get(e, 0) + 1
    Vu = V / np.linalg.norm(V, axis=1)[:, None]; tau = np.zeros(F); nv = np.zeros(F); edges = set()
    for g in range(F):
        bd = [e for e, c in ecount[g].items() if c == 1]; edges.update(bd)
        tau[g] = 2 * np.pi - sum(np.arccos(np.clip(Vu[p] @ Vu[q], -1, 1)) for p, q in bd); nv[g] = len(bd)
    return np.array([area, om, tau, Dd * area / 3, Dd, nv]).T, edges

rows = []; ok = True
V = OGf; FF = faces(V)
for k in range(KMAX + 1):
    M, Dd, cor = FF
    Vc = V[cor]
    FD, edges = face_data(Vc, M, Dd)
    if k == 0: assert len(edges) == len(Vc) + len(M) - 2, 'Euler edge count'
    A, om, tau, vol, d, nv = FD.T
    W = symmetrise(M * Dd[:, None]); FN = faces(W); M2, D2, cor2 = FN
    dist, _ = cKDTree(W[cor2]).query(M * Dd[:, None]); act = dist < 1e-7
    # checks
    c1 = abs(om.sum() - 4 * np.pi) < 1e-6
    c2 = np.linalg.norm((A[:, None] * M).sum(0)) < 1e-6 * A.sum()
    c3 = abs(vol.sum() - ConvexHull(Vc).volume) < 1e-6 * vol.sum()
    Vu = Vc / np.linalg.norm(Vc, axis=1)[:, None]
    dih = sum(np.pi - np.arccos(np.clip(Vu[i] @ Vu[j], -1, 1)) for i, j in edges)   # dihedral of X_k at the edge dual to D_k's edge ij
    gram = tau.sum() / (4 * np.pi) - dih / (2 * np.pi) + len(Vc) / 2 - 1
    c4 = abs(gram) < 1e-6
    c5 = len(W) == len(M)
    ok &= c1 and c2 and c3 and c4 and c5
    cut = ~act; nc = int(cut.sum()); F = len(M)
    def share(w): return float(w[cut].sum() / w.sum())
    def mx(w, s): return float(w[s].max()) if s.any() else float('nan')
    def mn(w, s): return float(w[s].min()) if s.any() else float('nan')
    r = dict(k=k, F=F, cut=nc, frac=nc / F, checks=[bool(c1), bool(c2), bool(c3), bool(c4), bool(c5)], gram=float(gram))
    for name, w in (('area', A), ('omega', om), ('tau', tau), ('vol', vol), ('d', d), ('nv', nv)):
        r[name] = dict(share=share(w), cut_max=mx(w, cut), cut_mean=float(w[cut].mean()) if nc else float('nan'),
                       act_min=mn(w, act), act_mean=float(w[act].mean()))
    rows.append(r)
    print(f'PROGRESS {(k + 1) / (KMAX + 1):.3f}', flush=True)
    print(f"k {k:2d} F {F:5d} cut {nc:5d} frac {nc / F:.3f} | shares cut: area {r['area']['share']:.3f} omega {r['omega']['share']:.3f}"
          f" tau {r['tau']['share']:.3f} vol {r['vol']['share']:.3f} | mean ratio cut/act: area {r['area']['cut_mean'] / r['area']['act_mean']:.3f}"
          f" omega {r['omega']['cut_mean'] / r['omega']['act_mean']:.3f} tau {r['tau']['cut_mean'] / r['tau']['act_mean']:.3f}"
          f" d {r['d']['cut_mean'] / r['d']['act_mean']:.4f} | omega cut max {r['omega']['cut_max']:.2e} act min {r['omega']['act_min']:.2e}"
          f" | d cut max {r['d']['cut_max']:.5f} act min {r['d']['act_min']:.5f} | nv cut mean {r['nv']['cut_mean']:.2f} act {r['nv']['act_mean']:.2f}"
          f" | checks {r['checks']} gram {gram:.1e}", flush=True)
    V, FF = W, FN
json.dump(rows, open(OUT, 'w'), indent=0)
print('FINAL ok' if ok else 'FINAL FAIL: a balance check (4pi, Minkowski, volume, Gram, count) failed')
