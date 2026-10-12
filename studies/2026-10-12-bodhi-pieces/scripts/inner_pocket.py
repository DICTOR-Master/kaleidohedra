# Bodhi seed, inner pocket (2026-10-12). Claim to test: the cavity enclosed by the 12 copies (= centre RT(1/phi) + inner pocket)
# is exactly the rhombic hexecontahedron RH(1): 20 prolate golden rhombohedra of edge 1 sharing the centre as a corner, one on each
# 3-fold axis. If so the inner pocket = RH(1) minus RT(1/phi), its volume 20P - RT(1)/phi^3 = 10P + 10O = RT(1) because P = phi O.
# Then: cut each rhombohedron by the face planes of RT(1/phi) and look at the convex cells left outside the centre.
import sys, os, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bodhi_core import *
from scipy.spatial import ConvexHull

# 1. RH(1) sits in the gap: inside the outer form, clear of all 12 copies, and its 20 blocks do not overlap each other
for B in RH20:
    assert all(np.all(B @ e[:3] + e[3] <= 1e-9) for e in F_OUTER)
    assert all(sat_separated(B, C) for C in COPIES)
for A, B in itertools.combinations(RH20, 2): assert sat_separated(A, B)
print(f'RH(1): 20 blocks, each volume {P_VOL:.9f}, total {20 * P_VOL:.9f}; inside the outer form, clear of all copies, no two overlap')
# RT(1/phi) is inside RH(1): every chamber part of the centre lies in the chamber's block (checked below with the cells)

# 2. the inner pocket from the chamber BSP (as bodhi_bsp.py), then: is every inner cell inside the chamber's block?
u5, u3, u2, cone = chamber()
t = TRIANGLES[np.argmax(U20 @ u3)]; block = RH20[TRIANGLES.index(t)]; FB = planes_of(block)
cut = dedupe_planes([e for P in F_SOLIDS for e in P] + [-e for P in F_SOLIDS for e in P])
cut = [e for i, e in enumerate(cut) if not any(np.linalg.norm(e + q) < 1e-7 for q in cut[:i])]
cells = bsp([list(F_OUTER) + cone], cut)
gap = []
for H in cells:
    x, r = interior(H)
    if x is None or r < 1e-9: continue
    if any(inside_poly(x, P) for P in F_SOLIDS): continue
    W = verts(H)
    if W is not None: gap.append(W)
# pockets by shared corners
ks = [set(key(v) for v in W) for W in gap]; par = list(range(len(gap)))
def f(i):
    while par[i] != i: par[i] = par[par[i]]; i = par[i]
    return i
for i, j in itertools.combinations(range(len(gap)), 2):
    if len(ks[i] & ks[j]) >= 3: par[f(i)] = f(j)
pockets = {}
for i in range(len(gap)): pockets.setdefault(f(i), []).append(gap[i])
inner = min(pockets.values(), key=lambda L: sum(vol(W) for W in L))
outer = max(pockets.values(), key=lambda L: sum(vol(W) for W in L))
vi, vo = sum(vol(W) for W in inner), sum(vol(W) for W in outer)
print(f'chamber: {len(gap)} gap cells; inner pocket {len(inner)} cells x120 = {120 * vi:.9f}; outer {len(outer)} cells x120 = {120 * vo:.9f}')
# centre's chamber part
cc = verts(list(planes_of(CENTRE)) + cone)
ok = all(np.all(W @ e[:3] + e[3] <= 1e-7) for W in inner + [cc] for e in FB)
print(f'every inner cell and the centre part lie inside the chamber block: {ok}')
print(f'cavity volume 120 x (inner + centre part) = {120 * (vi + vol(cc)):.9f}; RH(1) = 20 P = {20 * P_VOL:.9f}; '
      f'equal: {abs(120 * (vi + vol(cc)) - 20 * P_VOL) < 1e-7}')
print(f'inner pocket = 20P - RT(1/phi) = {20 * P_VOL - vol(CENTRE):.9f}; RT(1) = {RT_VOL:.9f}; 10P+10O = {10 * (P_VOL + O_VOL):.9f}')
print(f'RH(1) face planes = RT(1/phi) face planes: offsets {sorted(set(round(abs(e[3]), 9) for B in RH20 for e in planes_of(B) if abs(e[3]) > 1e-9))}'
      f' vs RT(1/phi) inradius {RIN / PHI:.9f}')

# 3. one block minus the centre: cut by the centre's face planes, keep the cells outside the centre
FC = planes_of(CENTRE)
cells = bsp([list(FB)], FC)
out = []
for H in cells:
    x, r = interior(H)
    if x is None or r < 1e-9: continue
    if inside_poly(x, FC): continue
    out.append(verts(H))
print(f'\nblock minus centre: {len(out)} cells, volume {sum(vol(W) for W in out):.9f} = {sum(vol(W) for W in out) / P_VOL:.6f} P;'
      f' x20 = {20 * sum(vol(W) for W in out):.9f} (inner pocket {120 * vi:.9f})')
# connected components (shared face = >= 3 shared corners)
ks = [set(key(v) for v in W) for W in out]; par = list(range(len(out)))
for i, j in itertools.combinations(range(len(out)), 2):
    if len(ks[i] & ks[j]) >= 3: par[f(i)] = f(j)
comps = {}
for i in range(len(out)): comps.setdefault(f(i), []).append(out[i])
stab = stabiliser(u3)
print(f'components: {len(comps)}; 3-fold stabiliser order {len(stab)}')
for r, L in comps.items():
    U = np.vstack(L); hv = vol(hull_corners(U)); uv = sum(vol(W) for W in L)
    print(f'  component: {len(L)} cells, volume {uv:.9f} = {uv / P_VOL:.6f} P = {uv / O_VOL:.6f} O; hull {hv:.9f}; convex: {abs(hv - uv) < 1e-9}')
    if abs(hv - uv) < 1e-9: print(describe(U, '    piece'))
sigs = {}
for W in out: sigs.setdefault(congruence_sig(W), []).append(W)
print(f'cell congruence classes: {len(sigs)}')
for s, L in sigs.items(): print(f'  {len(L)} x {s[0]} corners, volume {s[1]} = {s[1] / P_VOL:.4f} P')
np.save(os.path.join(HERE, '../data/inner-block-cells.npy'), np.array(out, dtype=object), allow_pickle=True)
