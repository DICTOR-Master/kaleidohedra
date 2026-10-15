# Step 13 (DICTO: "slice up the 102-faced partner, see if any resonance in quadrants, like the relation between dodeca and icosa").
# Exploratory, float. The Hecatodihedron (Heca) is the OCD's dual. Scale it so its 90 tangent faces pass through the OCD's 90
# corners on the sphere r = 2/3 (the dual nesting, as an icosahedron sits in a dodecahedron with corners on face centres).
# Then: Heca against the bcc cell V and its neighbours; the shell Heca - OCD sliced into octants by the three cube planes.
import json, itertools, numpy as np, sys, io, os, contextlib
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T']); R = json.load(open('data/network-render.json'))
cube = np.array(R['cube']); G = json.load(open('data/gaps.json')); V = np.array(G['V'])
# the Hecatodihedron as the polar of the OCD in the unit sphere: face plane n.x = d of the OCD -> corner n/d
EO = ConvexHull(O).equations; pl = []
for e in EO:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
H = np.array([e[:3] / -e[3] for e in pl])                          # polar corners (OCD faces -> Heca corners)
hH = ConvexHull(H); EH = []
for e in hH.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in EH): EH.append(e)
EH = np.array(EH); dH = -EH[:, 3]
tang = sorted(set(np.round(dH, 6)))                                # face distances: the 90 tangent faces are at the smallest
from collections import Counter
common = Counter(np.round(dH, 6)).most_common(1)[0][0]           # the 90 tangent faces (the 12 pentagons sit slightly inside)
s = (2 / 3) / common; H = H * s; hH = ConvexHull(H); EHs = hH.equations
on = sum(np.min(np.abs(O @ e[:3] + e[3])) < 1e-7 for e in EHs)
cnt = len({tuple(np.round(e, 6)) for e in EHs if np.min(np.abs(O @ e[:3] + e[3])) < 1e-7})
out = [f'Hecatodihedron scaled x{s:.6f}: {len(H)} corners, {len({tuple(np.round(e, 6)) for e in EHs})} faces; faces through OCD corners: {cnt}; volume {hH.volume:.6f} (OCD {ConvexHull(O).volume:.6f}, cell {ConvexHull(V).volume:.6f})']
EV = ConvexHull(V).equations
inside = all(np.all(EV[:, :3] @ v + EV[:, 3] <= 1e-9) for v in H)
out.append(f'Heca inside the bcc cell: {inside}; furthest Heca corner outside the cell by {max(0, max((EV[:, :3] @ v + EV[:, 3]).max() for v in H)):.6f}')
def overlap(E1, E2):
    A = np.vstack([E1, E2]); nrm = np.linalg.norm(A[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A[:, :3], nrm], b_ub=-A[:, 3], bounds=[(None, None)] * 3 + [(0, None)]); return r.status == 0 and r.x[3] > 1e-8
nb = [t for t in np.vstack([T, -T])] + [T[a] + T[b] for a, b in itertools.combinations(range(4), 2)] + [-(T[a] + T[b]) for a, b in itertools.combinations(range(4), 2)]
hits = sum(overlap(EHs, EHs - np.c_[np.zeros((len(EHs), 3)), EHs[:, :3] @ c]) for c in nb)
out.append(f'Hecas around neighbouring copies overlap: {hits} of {len(nb)} neighbours')
# the shell Heca - OCD in octants: cone pieces (over OCD faces, out to the Heca) cut by the three cube planes
def clip(P, n):     # keep the part of convex P with n.x >= 0
    E = np.vstack([ConvexHull(P).equations, np.r_[-n, 0.0]]); nrm = np.linalg.norm(E[:, :3], axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[E[:, :3], nrm], b_ub=-E[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if r.status != 0 or r.x[3] < 1e-9: return None
    return np.unique(np.round(HalfspaceIntersection(E, r.x[:3]).intersections, 10), axis=0)
shell = []
for e in pl:
    idx = np.abs(O @ e[:3] + e[3]) < 1e-7; Fv = O[idx]; c = Fv.mean(0); u = c / np.linalg.norm(c)
    Hs = [np.r_[e[:3], e[3]] * -1]                                   # beyond the OCD face
    hs = [np.r_[-e[:3], -e[3] * -1]] if False else [np.r_[-e[:3], -(-e[3])]]
    hs = [np.r_[-e[:3], e[3] * -1 * -1]]
    hs = [np.r_[-e[:3], -e[3]]]                                      # -n.x - d <= 0  <=> n.x + d >= 0 ... outside the OCD face
    ring = Fv[np.argsort(np.arctan2((Fv - c) @ np.cross(u, Fv[0] - c), (Fv - c) @ (Fv[0] - c)))]
    for i in range(len(ring)):
        m = np.cross(ring[i], ring[(i + 1) % len(ring)]); m = m if m @ c > 0 else -m; hs.append(np.r_[-m, 0.0])
    hs += list(EHs)
    nu = EHs[:, :3] @ u; r1 = np.min(-EHs[nu > 1e-12, 3] / nu[nu > 1e-12]); r0 = np.linalg.norm(c)
    if r1 - r0 < 1e-9: continue
    X = np.unique(np.round(HalfspaceIntersection(np.array(hs), u * (r0 + r1) / 2).intersections, 10), axis=0); shell.append(X)
oct_vol = {}
for P in shell:
    for sg in itertools.product((1, -1), repeat=3):
        Q = P
        for k in range(3):
            if Q is None: break
            Q = clip(Q, sg[k] * cube[k])
        if Q is not None and len(Q) >= 4:
            try: oct_vol[sg] = oct_vol.get(sg, 0) + ConvexHull(Q).volume
            except Exception: pass
vs = ConvexHull(H).volume - ConvexHull(O).volume
out.append(f'shell Heca - OCD = {vs:.6f}, in {len(shell)} cone pieces; octant volumes: {sorted(round(v, 6) for v in oct_vol.values())} (sum {sum(oct_vol.values()):.6f})')
phi = (1 + 5 ** .5) / 2; ratios = {'Heca/OCD': hH.volume / ConvexHull(O).volume, 'shell/OCD': vs / ConvexHull(O).volume, 'cell/Heca': ConvexHull(V).volume / hH.volume}
out.append('ratios: ' + ', '.join(f'{k} = {v:.6f} (log_phi {np.log(v) / np.log(phi):.4f})' for k, v in ratios.items()))
print('\n'.join(out)); open('data/heca-partner.txt', 'w').write('\n'.join(out) + '\n')
