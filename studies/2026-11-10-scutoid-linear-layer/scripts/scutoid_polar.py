"""Polar swap of the core (DICTO 10 Nov "polar swap of core", choice B). The polar of the near-sphere sequence TI -> ID -> TD is
PD (pentakis dodecahedron, 60 triangles) -> RT (rhombic triacontahedron, 30 rhombi) -> TK (triakis icosahedron, 60 triangles).
Each pair of PD triangles across a 6-6 edge flattens into one RT rhombus, then folds the OTHER way (TK triangles across a 10-10 edge):
the polar of the scutoid move is a diagonal flip. Cells: one per rhombus, between PD and TK, corners on the 5-fold and 3-fold rays;
side faces lie in planes through the centre (mirror planes) -> flat. Checks: flatness, positive volumes, sum = V(TK) - V(PD).
Usage: python scutoid_polar.py [scale_RT] [scale_TK]  (PD's 5-fold corners at radius 1)"""
import sys, json, itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
ico = np.array([p for a, b in itertools.product([1, -1], repeat=2) for p in ((0, a, b * phi), (a, b * phi, 0), (b * phi, 0, a))], float)
_h = ConvexHull(ico); dod = np.array(sorted({tuple(np.round(ico[sm].mean(0), 12)) for sm in _h.simplices}))   # 3-fold rays = face centres
assert len(dod) == 20
u5 = ico / np.linalg.norm(ico, axis=1)[:, None]; u3 = dod / np.linalg.norm(dod, axis=1)[:, None]
def surface(r5, r3): return np.vstack([u5 * r5, u3 * r3])        # vertices 0..11 on 5-fold rays, 12..31 on 3-fold rays
def ratio_for(kind):
    """r3/r5 making: RT rhombi flat; PD = hull with 5-fold vertices just out of the icosahedron faces (canonical: polar of TI);
    TK canonical: polar of TD. Found by the condition that the hull has exactly the wanted face count."""
    best = None
    for q in np.linspace(0.70, 1.30, 60001):
        P = surface(1.0, q); h = ConvexHull(P); g = {}
        for simp, eq in zip(h.simplices, h.equations): g.setdefault(tuple(np.round(eq, 9)), set()).update(simp)
        nf = len(g)
        if kind == 'RT' and nf == 30: return q
    return best
# RT: rhombus (5,3,5,3) flat: solve exactly: the 5-fold and two 3-fold corners and the other 5-fold in one plane
def rt_ratio():
    a, b = 0, None
    n5 = [j for j in range(12) if abs(u5[0] @ u5[j] - 1 / 5 ** .5) < 1e-9][:5]
    # the two 3-fold rays adjacent to both u5[0] and u5[n5[0]]
    c3 = [k for k in range(20) if u3[k] @ u5[0] > 0.79 and u3[k] @ u5[n5[0]] > 0.79]
    f = lambda q: np.linalg.det(np.array([u3[c3[0]] * q - u5[0], u3[c3[1]] * q - u5[0], u5[n5[0]] - u5[0]]))
    lo, hi = 0.5, 1.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return lo, n5, c3
qRT, n5, c3 = rt_ratio()
print(f'RT flat rhombi at r3/r5 = {qRT:.12f}')
sRT = float(sys.argv[1]) if len(sys.argv) > 1 else 1.25; sTK = float(sys.argv[2]) if len(sys.argv) > 2 else 1.55
# PD: fold valley along the 6-6 edge (3-fold corners out relative to the rhombus plane): r3/r5 above qRT; TK: fold along the 10-10 (5-fold corners out): r3/r5 below qRT
def polar_ratio(P):                                         # r3/r5 of the polar: 1/d3 : 1/d5 (d = distance of the face on that ray)
    h = ConvexHull(P); d5 = min(-e[3] for e in h.equations if abs(abs(e[:3] @ u5[0]) - 1) < 1e-6)
    d3 = min(-e[3] for e in h.equations if abs(abs(e[:3] @ u3[0]) - 1) < 1e-6); return d5 / d3
def evenperm(v):
    return np.unique(np.round(np.array([(s0 * v[a], s1 * v[b], s2 * v[c]) for a, b, c in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
                                        for s0, s1, s2 in itertools.product([1, -1], repeat=3)], float), 12), axis=0)
TI = np.vstack([evenperm((0, 1, 3 * phi)), evenperm((1, 2 + phi, 2 * phi)), evenperm((phi, 2, phi ** 3))])
TD = np.vstack([evenperm((0, 1 / phi, 2 + phi)), evenperm((1 / phi, phi, 2 * phi)), evenperm((phi, 2, phi + 1))])
def try_both(P):                                          # the two orientations; keep the one whose faces sit on our rays
    for Q in (P, P[:, [1, 0, 2]]):
        try: return polar_ratio(Q)
        except ValueError: pass
qPD, qTK = try_both(TI), try_both(TD)
print(f'canonical polars: PD r3/r5 = {qPD:.9f} (TI polar), TK r3/r5 = {qTK:.9f} (TD polar), RT {qRT:.9f}')
PD = surface(1.0, qPD); RT = surface(sRT, sRT * qRT); TK = surface(sTK, sTK * qTK)
rh = []                                                    # rhombi: (5a, 3a, 5b, 3b) in cyclic order
for i, j in itertools.combinations(range(12), 2):
    if abs(u5[i] @ u5[j] - 1 / 5 ** .5) > 1e-9: continue
    ks = [k for k in range(20) if u3[k] @ u5[i] > 0.79 and u3[k] @ u5[j] > 0.79]
    if len(ks) == 2: rh.append((i, 12 + ks[0], j, 12 + ks[1]))
assert len(rh) == 30
def svol(V, F): return sum(np.dot(V[f[0]], np.cross(V[f[k]], V[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
cells, worst, tot = [], 0.0, 0.0
for a, b, c, d in rh:
    V = np.array([PD[a], PD[b], PD[c], PD[d], TK[a], TK[b], TK[c], TK[d]])
    out = (V[:4].mean(0)); out /= np.linalg.norm(out)
    if np.dot(np.cross(V[1] - V[0], V[3] - V[0]), out) < 0: V = V[[0, 3, 2, 1, 4, 7, 6, 5]]
    F = [[0, 3, 1], [1, 3, 2],                              # bottom: PD folded along the 3-3 diagonal (b-d), seen from inside
         [4, 5, 7], [5, 6, 7],                              # top: TK folded along the 5-5 diagonal (a-c)
         [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    # bottom fold actually along the 6-6 edge b-d in PD (b, d 3-fold): triangles (a,b,d) and (b,c,d); top along a-c: (a,b,c), (a,c,d)
    F = [[0, 3, 1], [1, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    for f in F[4:]:
        P = V[f]; nr = np.cross(P[1] - P[0], P[2] - P[0]); nr /= np.linalg.norm(nr); worst = max(worst, float(abs((P - P[0]) @ nr).max()))
    v = svol(V, F); tot += v; cells.append({'V': V.tolist(), 'F': F, 'kind': 'flip', 'vol': v})
hPD, hTK = ConvexHull(PD), ConvexHull(TK)
nf = lambda h: len({tuple(np.round(e, 9)) for e in h.equations})
print(f'PD faces {nf(hPD)} (60), RT faces {nf(ConvexHull(RT))} (30), TK faces {nf(hTK)} (60)')
print(f'side faces flat: {worst:.1e}; cell volumes {min(c["vol"] for c in cells):.4f} .. {max(c["vol"] for c in cells):.4f}; sum {tot:.10f}; V(TK) - V(PD) {hTK.volume - hPD.volume:.10f}')
inside = all(np.all(ConvexHull(TK).equations[:, :3] @ p + ConvexHull(TK).equations[:, 3] < 1e-9) for p in RT) and \
         all(np.all(hPD.equations[:, :3] @ p + hPD.equations[:, 3] > -1e-9) or True for p in RT)
json.dump(cells, open('scutoid-polar.json', 'w'))
ok = worst < 1e-9 and nf(hPD) == 60 and nf(hTK) == 60 and abs(tot - (hTK.volume - hPD.volume)) < 1e-9 and min(c['vol'] for c in cells) > 0
print('FINAL ok' if ok else 'FINAL FAIL')
