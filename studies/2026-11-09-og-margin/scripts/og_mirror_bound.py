# og_mirror_bound.py, DICTO 11 Nov 2026 ("yes prove M"). Exact lemma (§38): every mirror face (normal in a mirror plane P of I_h) is
# symmetric across P, so it crosses P along an edge of the section polygon D_k ∩ P and its cap of directions meets the great circle of P;
# caps are disjoint, so the mirror faces of P fill at most the band of half-width 2*gamma_M (gamma_M = largest cap radius of a mirror face):
#   mu_k  <=  15 * sin(2 gamma_M) * (mean solid angle of all faces / mean solid angle of mirror faces)  +  62 / n_k     (axis faces <= 62).
# Per level: n, mirror faces M, actual mu, gamma_M, the size ratio, the bound; (M) needs bound < 1/4 (with generic death share <= 1/3).
# Control: solid angles add to 4*pi; actual mu <= bound at every level.
# usage: python -u og_mirror_bound.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); KM = int(sys.argv[2]); OUTJ = os.path.abspath(sys.argv[3])
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(open(os.path.join(here, 'og_sweep.py')).read().split('rows_out = []')[0])
from scipy.spatial import ConvexHull, cKDTree
GH = np.concatenate([Gf, -Gf])
def face_polys(V):
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
        m = E[fs, :3].mean(0); m /= np.linalg.norm(m)
        pts = V[sorted(set(int(j) for f in fs for j in h.simplices[f]))]
        c0 = pts.mean(0); B = np.linalg.svd(pts - c0)[2][:2]; Q = (pts - c0) @ B.T
        out.append((m, pts[np.argsort(np.arctan2(Q[:, 1], Q[:, 0]))]))
    return out
def solid_angle_and_cap(P):
    U = P / np.linalg.norm(P, axis=1)[:, None]; c = U.mean(0); c /= np.linalg.norm(c)
    om = 0.0
    for a, b in zip(U, np.roll(U, -1, 0)):
        num = np.dot(c, np.cross(a, b)); den = 1 + c @ a + c @ b + a @ b; om += 2 * np.arctan2(num, den)
    return abs(om), float(np.arccos(np.clip(U @ c, -1, 1)).max())
rows = []; ok = True; V = OGf
for k in range(KM + 1):
    FP = face_polys(V); n = len(FP)
    Nn = np.array([m for m, _ in FP]); tr = cKDTree(Nn)
    stab = np.array([sum(1 for g in GH if np.linalg.norm(g @ m - m) < 1e-9) for m in Nn])   # stabiliser size in I_h
    mirror = stab == 2; axis = stab > 2
    om_cap = [solid_angle_and_cap(P) for _, P in FP]; om = np.array([x[0] for x in om_cap]); cap = np.array([x[1] for x in om_cap])
    tot_ok = abs(om.sum() - 4 * np.pi) < 1e-6; ok &= tot_ok
    M = int(mirror.sum()); mu = (M + int(axis.sum())) / n
    gM = float(cap[mirror].max()) if M else 0.0; ratio = float(om.mean() / om[mirror].mean()) if M else 0.0
    bound = 15 * np.sin(min(2 * gM, np.pi / 2)) * ratio + 62 / n
    ok &= mu <= bound + 1e-12
    rows.append(dict(k=k, n=n, mirror=M, axis=int(axis.sum()), mu=mu, gamma_M_deg=np.degrees(gM), size_ratio=ratio, bound=float(bound), mean_cap_deg=float(np.degrees(cap.mean()))))
    print(f'PROGRESS {(k + 1) / (KM + 1):.3f}', flush=True)
    print(f'k {k:2d}: n {n:6d} mirror faces {M:5d} axis {int(axis.sum()):3d} | mu {mu:.3f} | gamma_M {np.degrees(gM):6.3f} deg (mean cap {np.degrees(cap.mean()):.3f}) | size ratio {ratio:.3f} | BOUND {bound:.3f} {"< 1/4" if bound < .25 else ""} | sum omega = 4pi {tot_ok}', flush=True)
    M_, Dd = Nn, np.array([np.max(P @ m) for m, P in FP])
    V = symmetrise(M_ * Dd[:, None])
json.dump(rows, open(OUTJ, 'w'), indent=1)
print('levels where the bound proves mu < 1/4:', [r['k'] for r in rows if r['bound'] < .25])
print('FINAL ok' if ok else 'FINAL FAIL: solid angles do not add to 4 pi, or mu above its bound')
