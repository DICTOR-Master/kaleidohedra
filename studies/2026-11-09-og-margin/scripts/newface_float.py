# DICTO #43, 9 Nov ("proceed"): data for the NEW-FACE LEMMA. Float iteration of the pedal step D_{k+1} = hull of foot points of D_k.
# Per level: surviving faces (normal of a face of D_k) vs NEW faces; for each new face F: nu_F = its distance, rho_F = smallest radius
# of its spanning foot points, gamma_F = largest angle between its normal and those foot points. Bound: nu_F >= rho_F cos gamma_F.
# Prints min nu_new / r_prev, max gamma_new, the product prod cos(gamma_max) from K, and the m-step ratios min nu_new(D_{j+m}) / r(D_j).
# usage: python -u newface_float.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, time, itertools, math
import numpy as np
from scipy.spatial import ConvexHull, cKDTree
OUT = os.path.abspath(sys.argv[3]); sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])
KMAX = int(sys.argv[2])
# DICTO 9 Nov ('faces getting smaller ~ whole getting bigger'; 'make it so'): WHERE is the largest new face? angle of its normal to the
# nearest 5-, 3-, 2-fold axis; and the largest new face AWAY from every axis (> AXTOL deg): generic faces vs axis faces.
q5 = lambda x: float(x.a) + float(x.b) * 5 ** .5
Gf = np.array([[[q5(x) for x in row] for row in M] for M in G])
AX = {5: [], 3: [], 2: []}
for g in Gf:
    c = (np.trace(g) - 1) / 2
    if c > 1 - 1e-9: continue
    ang = np.degrees(np.arccos(np.clip(c, -1, 1)))
    o = 5 if min(abs(ang - 72), abs(ang - 144)) < 1e-4 else 3 if abs(ang - 120) < 1e-4 else 2
    w, v = np.linalg.eig(g); a = np.real(v[:, np.argmin(np.abs(w - 1))]); a /= np.linalg.norm(a); AX[o] += [a, -a]
for o in AX: AX[o] = np.unique(np.round(np.array(AX[o]), 9), axis=0)
assert {o: len(AX[o]) for o in AX} == {5: 12, 3: 20, 2: 30}
ax_angle = lambda u: {o: float(np.degrees(np.arccos(np.clip(np.abs(AX[o] @ u).max(), -1, 1)))) for o in AX}
AXTOL = 3.0
W = np.array([[float(x.a) + float(x.b) * 5 ** .5 for x in v] for v in OG])
def faces(W, tol=1e-9):
    h = ConvexHull(W); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    G = {}
    for f in range(n): G.setdefault(find(f), []).append(f)
    out = []
    for g in G.values():
        nrm = h.equations[g[0], :3]; d = -h.equations[g[0], 3]
        mem = sorted(set(int(j) for f in g for j in h.simplices[f])); out.append((nrm, d, mem))
    return out
rows = []; prevN = None; prev_r = None; t0 = time.time()
for k in range(KMAX + 1):
    F = faces(W); N = np.array([f[0] for f in F]); D = np.array([f[1] for f in F]); r = D.min(); R = np.linalg.norm(W, axis=1).max()
    row = {'k': k, 'faces': len(F), 'r': float(r), 'R': float(R)}
    if prevN is not None:
        surv = cKDTree(prevN).query(N, k=1)[0] < 1e-6        # same normal as a face of D_k (memory-light)
        nu = D[~surv]; rad = np.linalg.norm(W, axis=1); gam = []; rho = []
        for (n, d, mem), s in zip(F, surv):
            if s: continue
            P = W[mem]; rr = np.linalg.norm(P, axis=1); rho.append(rr.min()); gam.append(np.arccos(np.clip((P @ n) / rr, -1, 1)).max())
        gam = np.array(gam); rho = np.array(rho)
        newN = N[~surv]; jmax = int(np.argmax(gam)); aa = ax_angle(newN[jmax]); near = min(aa, key=aa.get)
        offax = np.array([min(ax_angle(n).values()) > AXTOL for n in newN]) if len(newN) < 4000 else None
        if offax is None:                                # vectorised for large levels
            m = np.full(len(newN), np.inf)
            for o in AX: m = np.minimum(m, np.degrees(np.arccos(np.clip(np.abs(newN @ AX[o].T).max(1), -1, 1))))
            offax = m > AXTOL
        gen = float(np.degrees(gam[offax].max())) if offax.any() else float('nan')
        row.update(gamma_max_axis=near, gamma_max_axis_angle=aa[near], gamma_generic_max_deg=gen,
                   avg_ang_rad_deg=float(np.degrees(2 / np.sqrt(len(F)))))
        row.update(new=int((~surv).sum()), surviving=int(surv.sum()), nu_new_min=float(nu.min()), nu_new_over_rprev=float(nu.min() / prev_r),
                   gamma_new_max_deg=float(np.degrees(gam.max())), rho_over_rprev_min=float(rho.min() / prev_r),
                   bound_slack=float((nu - rho * np.cos(gam)).min()), surv_min=float(D[surv].min()) if surv.any() else None)
        print(f"k {k:2d} F {len(F):6d} r {r:.6f} R {R:.6f} new {row['new']:6d} surv {row['surviving']:4d} nu_new/r_prev {row['nu_new_over_rprev']:.6f} "
              f"gamma_new_max {row['gamma_new_max_deg']:.3f} deg at {row['gamma_max_axis']}-fold +{row['gamma_max_axis_angle']:.2f} | off-axis max {row['gamma_generic_max_deg']:.3f} | avg {row['avg_ang_rad_deg']:.3f} | rho_min/r_prev {row['rho_over_rprev_min']:.6f} bound slack {row['bound_slack']:.1e} ({time.time()-t0:.0f} s)", flush=True)
    rows.append(row); prevN = N; prev_r = r
    if k == KMAX: break
    W = N * D[:, None]                                   # foot points (unit normals from qhull)
for m in (1, 2, 3, 4):
    vals = [rows[j + m]['nu_new_min'] / rows[j]['r'] for j in range(len(rows) - m) if 'nu_new_min' in rows[j + m]]
    print(f'm-step: min over j of nu_new(D_(j+m)) / r(D_j), m = {m}: {min(vals):.6f}  (j >= 13 only: {min(vals[13:]) if vals[13:] else float("nan"):.6f})')
for K in (13, 18, 22):
    if K + 1 >= len(rows): continue
    p = np.prod([math.cos(math.radians(x['gamma_new_max_deg'])) for x in rows[K + 1:]]); print(f'prod cos(gamma_new_max) over k > {K}: {p:.6f}')
json.dump({'mark': 'DICTO #43 New-Face Lemma data, 2026-11-09 · DICTO · dictospheres.com', 'k': rows}, open(OUT, 'w'), indent=1)
print('FINAL ok' if all(r.get('bound_slack', 0) > -1e-9 for r in rows) and len(rows) == KMAX + 1 else 'FINAL FAIL: plane bound violated or run incomplete')
