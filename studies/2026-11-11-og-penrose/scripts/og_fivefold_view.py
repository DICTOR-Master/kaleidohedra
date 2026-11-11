# og_fivefold_view.py, DICTO 11 Nov 2026 ("the penrose and the icosahedral are mixed" -> "b": the OG family is icosahedral (6D side) but its
# views perpendicular to a five-fold axis may carry five-fold, Penrose-type order, as icosahedral quasicrystals do on five-fold planes).
# Per level k of the OG downward family D_k (float, as og_sweep.py):
#  (1) the central section perpendicular to a five-fold axis: edges, distinct edge lengths, ratios of consecutive lengths vs powers of phi;
#  (2) the CAP: faces whose normal is within CAP degrees of the axis, projected onto the plane: distinct tile shapes (congruence by sorted
#      side lengths and angles, 1e-6), the counts of the two commonest, their ratio vs phi, and the edge directions mod 36 degrees
#      (Penrose tilings use 5 edge directions: all edges at multiples of 36 degrees).
# Control: central section has 10-fold dihedral symmetry (five-fold axis x central symmetry): edge count divisible by 10.
# usage: python -u og_fivefold_view.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, numpy as np
from collections import Counter
KM = int(sys.argv[2]); OUTJ = os.path.abspath(sys.argv[3])
SW = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts/og_sweep.py')
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(open(SW).read().split('rows_out = []')[0])
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2; CAP = 20.0
ax = None
for g in Gf:
    if abs(np.trace(g) - (1 + 2 * np.cos(2 * np.pi / 5))) < 1e-9:
        w, v = np.linalg.eig(g); ax = np.real(v[:, np.argmin(abs(w - 1))]); ax /= np.linalg.norm(ax); break
B = np.linalg.svd(np.eye(3) - np.outer(ax, ax))[0][:, :2]
def faces_polys(V):
    h = ConvexHull(V); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(E[f] - E[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), []).append(f)
    out = []
    for fs in grp.values():
        m = E[fs, :3].mean(0); m /= np.linalg.norm(m)
        P = V[sorted(set(int(j) for f in fs for j in h.simplices[f]))]
        c0 = P.mean(0); Bb = np.linalg.svd(P - c0)[2][:2]; Q = (P - c0) @ Bb.T
        out.append((m, P[np.argsort(np.arctan2(Q[:, 1], Q[:, 0]))]))
    return out, h
def section(V, h):
    s = V @ ax; pts = []
    for simp in h.simplices:
        for a, b in ((simp[0], simp[1]), (simp[1], simp[2]), (simp[0], simp[2])):
            if s[a] * s[b] < 0: t = s[a] / (s[a] - s[b]); pts.append(V[a] + t * (V[b] - V[a]))
            elif abs(s[a]) < 1e-12: pts.append(V[a])
    Q = np.unique(np.round(np.array(pts) @ B, 10), axis=0); hh = ConvexHull(Q); vq = Q[hh.vertices]; keep = []
    for i in range(len(vq)):
        a, b_, c = vq[i - 1], vq[i], vq[(i + 1) % len(vq)]
        if abs((b_[0] - a[0]) * (c[1] - b_[1]) - (b_[1] - a[1]) * (c[0] - b_[0])) > 1e-10 * np.linalg.norm(b_ - a) * np.linalg.norm(c - b_): keep.append(i)
    vq = vq[keep]; L = np.linalg.norm(np.roll(vq, -1, 0) - vq, axis=1); return vq, L
rows = []; ok = True; V = OGf
for k in range(KM + 1):
    FP, h = faces_polys(V)
    vq, L = section(V, h); e = len(vq); ok &= e % 10 == 0 or e % 5 == 0
    Ls = np.unique(np.round(L / L.max(), 7))[::-1]; ratios = [float(Ls[i] / Ls[i + 1]) for i in range(len(Ls) - 1)]
    near_phi = [r for r in ratios if min(abs(np.log(r) / np.log(phi) - n_) for n_ in range(1, 6)) < 1e-4]
    cap = [(m, P) for m, P in FP if m @ ax > np.cos(np.radians(CAP))]
    shapes = Counter(); dirs = []
    for m, P in cap:
        Q = P @ B; L2 = np.linalg.norm(np.roll(Q, -1, 0) - Q, axis=1); e1 = np.roll(Q, -1, 0) - Q; e0 = Q - np.roll(Q, 1, 0)
        an = np.degrees(np.arccos(np.clip((-e0 * e1).sum(1) / (np.linalg.norm(e0, axis=1) * np.linalg.norm(e1, axis=1)), -1, 1)))
        key = (len(Q), tuple(np.round(sorted(L2 / L2.max()), 5)), tuple(np.round(sorted(an), 3)))
        shapes[key] += 1; dirs += list(np.mod(np.degrees(np.arctan2(e1[:, 1], e1[:, 0])), 36.0))
    dirs = np.array(dirs); lock = float(np.mean(np.minimum(dirs, 36 - dirs) < 0.5)) if len(dirs) else 0.0
    top = shapes.most_common(2); r2 = top[0][1] / top[1][1] if len(top) > 1 else float('nan')
    rows.append(dict(k=k, section_edges=e, section_lengths=len(Ls), golden_ratios_between_lengths=len(near_phi), cap_faces=len(cap), cap_shapes=len(shapes), top2=[t[1] for t in top], top2_ratio=r2, edge_dirs_on_36deg=lock))
    print(f'PROGRESS {(k + 1) / (KM + 1):.3f}', flush=True)
    print(f'k {k:2d}: central 5-fold section {e} edges, {len(Ls)} lengths, {len(near_phi)} consecutive ratios = powers of phi | cap ({CAP:.0f} deg) {len(cap)} faces, {len(shapes)} shapes, top2 {[t[1] for t in top]} ratio {r2:.3f} (phi {phi:.3f}) | edge directions on multiples of 36 deg: {lock:.2f}', flush=True)
    W = symmetrise(np.array([m * (m @ P[0]) for m, P in FP])); V = W
json.dump(rows, open(OUTJ, 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL: a central section without five-fold symmetry')
