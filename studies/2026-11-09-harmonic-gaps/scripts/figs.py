# DICTO 2026-11-09 harmonic-gaps study: figures (float copies of the exact pieces; runs on the big machine, writes ../figures/).
#  fig-b1-maps.png      Mollweide maps: r of the great star, outer r and equivalent radius (3m)^(1/3) of the small Sunstar, gap mass m(u)
#  fig-b2-spectrum.png  power of the gap mass by degree l, icosahedral vs pyritohedral part
#  fig-b3-filler.png    the great star (see-through), the small Sunstar, and the 1/phi^3 lattice pieces cut by the great star (the filler)
#  fig-a1-reciprocal.png  GD(D1) = D1 + spires + valley tetrahedra inside I2; GI(I) piercing D1
import os, sys, json, itertools, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import manifold3d as m3
from scipy.spatial import ConvexHull
from radial import real_Y, LMAX
DATA = os.path.join(HERE, '..', 'data'); FIG = os.path.join(HERE, '..', 'figures'); os.makedirs(FIG, exist_ok=True)
MARK = 'DICTO · dictospheres.com'; phi = (1 + 5 ** .5) / 2; s = phi ** -3
GOLD, PURPLE, PALE, BG, INK = '#d9a334', '#a77be0', '#f0d48a', '#15131a', '#ece6d8'
ORBCOL = ['#5fb3d9', '#7fc97f', '#e07b7b', '#f2a65a', '#c9a0dc', '#8dd3c7', '#fb8072', '#bebada', '#ffffb3']
fails = []
# ---------- maps ----------
V = pickle.load(open(os.path.join(DATA, 'b_visible.pkl'), 'rb'))
def ray_mass(bnd, U):
    """m(u) = sum over boundary crossings sign * t^3/3, and the outer radius, by ray casting on the boundary triangles"""
    m = np.zeros(len(U)); rmax = np.zeros(len(U))
    for n, d, tris in bnd:
        cos = U @ n; okc = np.abs(cos) > 1e-12; t = np.where(okc, d / np.where(okc, cos, 1), -1)
        for A, B, C in tris:
            X = U * t[:, None]; v0, v1, v2 = B - A, C - A, X - A
            d00, d01, d11 = v0 @ v0, v0 @ v1, v1 @ v1; d20, d21 = v2 @ v0, v2 @ v1; den = d00 * d11 - d01 * d01
            bb = (d11 * d20 - d01 * d21) / den; cc = (d00 * d21 - d01 * d20) / den
            hit = okc & (t > 0) & (bb >= 0) & (cc >= 0) & (bb + cc <= 1)
            m += np.where(hit, np.sign(d) * t ** 3 / 3, 0); rmax = np.where(hit & (t > rmax), t, rmax)
    return m, rmax
nlon, nlat = 720, 360
lon = (np.arange(nlon) + .5) / nlon * 2 * np.pi - np.pi; lat = (np.arange(nlat) + .5) / nlat * np.pi - np.pi / 2
LO, LA = np.meshgrid(lon, lat); U = np.c_[(np.cos(LA) * np.cos(LO)).ravel(), (np.cos(LA) * np.sin(LO)).ravel(), np.sin(LA).ravel()]
U = U + 1e-9 * np.array([0.3, 0.7, 0.11]); U /= np.linalg.norm(U, axis=1)[:, None]      # avoid rays exactly along edges
mG, rG = ray_mass(V['bndG'], U); mS, rS = ray_mass(V['bndS'], U)
# check the maps against the harmonic series (smooth parts agree on average: compare the l = 0 moments)
w = np.cos(LA).ravel() * (2 * np.pi / nlon) * (np.pi / nlat)
volG, volS = (w * mG).sum(), (w * mS).sum()
if abs(volG - (70 - 30 * 5 ** .5)) > 2e-3 or abs(volS - (-2598 + 1162 * 5 ** .5)) > 2e-3: fails.append(f'map volumes {volG:.5f} {volS:.5f}')
print(f'map check: ∫ m dΩ on the grid: GSD {volG:.5f}, Sunstar {volS:.5f}', flush=True)
mgap = mG - mS; rhoS = np.cbrt(3 * mS)
fig, axs = plt.subplots(2, 2, figsize=(13, 7.6), subplot_kw={'projection': 'mollweide'}, facecolor=BG)
panels = [(rG, 'great star: r(u)', 'magma'), (rS, 'small Sunstar: outer r(u)', 'magma'),
          (rhoS, 'small Sunstar: equivalent radius (3m)$^{1/3}$\n(below outer r where rays leave and re-enter)', 'magma'), (mgap, 'the gap: angular mass m(u) = m$_G$ − m$_S$', 'viridis')]
for ax, (f, title, cm) in zip(axs.ravel(), panels):
    im = ax.pcolormesh(LO, LA, f.reshape(nlat, nlon), cmap=cm, shading='auto', rasterized=True)
    ax.set_title(title, color=INK, fontsize=10); ax.grid(True, color='#ffffff30', lw=.4); ax.set_xticklabels([]); ax.set_yticklabels([])
    cb = fig.colorbar(im, ax=ax, shrink=.7, pad=.02); cb.ax.tick_params(colors=INK, labelsize=7); ax.set_facecolor(BG)
fig.suptitle('#42 gap, by 3D waves: the great star and the small Sunstar seen from their common centre (cells of edge 2)', color=INK, fontsize=12)
fig.text(.99, .01, MARK, ha='right', color=INK, fontsize=8, alpha=.8)
fig.savefig(os.path.join(FIG, 'fig-b1-maps.png'), dpi=150, facecolor=BG); plt.close(fig)
# ---------- spectrum ----------
J = json.load(open(os.path.join(DATA, 'b_harmonic.json'))); Pm = np.array(J['spectra']['m_gap']); share = J['m_nonicosahedral_share']
ls = np.arange(1, LMAX + 1); cub = np.array([Pm[l] * share.get(str(l), 0) for l in ls]); ico = np.array([Pm[l] for l in ls]) - cub
fig, ax = plt.subplots(figsize=(10, 4.2), facecolor=BG); ax.set_facecolor(BG)
ax.bar(ls - .2, np.maximum(ico, 1e-30), .4, color=PALE, label='icosahedral part (the great star\'s)')
ax.bar(ls + .2, np.maximum(cub, 1e-30), .4, color=PURPLE, label='pyritohedral part (the Sunstar\'s cube)')
ax.set_yscale('log'); ax.set_ylim(1e-8, 1); ax.set_xlabel('degree l', color=INK); ax.set_ylabel('power of m(u) at degree l', color=INK)
ax.tick_params(colors=INK); [sp.set_color(INK) for sp in ax.spines.values()]; ax.legend(facecolor=BG, labelcolor=INK, fontsize=9)
ax.set_title(f'The gap\'s angular mass: {1 - J["gap_mass_anisotropy"]["non_icosahedral_share_of_l>0_power"]:.1%} of its variation is icosahedral; l = 4, 8, 14 come from the cube alone', color=INK, fontsize=10)
fig.text(.99, .01, MARK, ha='right', color=INK, fontsize=8, alpha=.8); fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig-b2-spectrum.png'), dpi=150, facecolor=BG); plt.close(fig)
# ---------- filler render ----------
S = json.load(open(os.path.join(DATA, 'sunstar-exact.json'))); cells = [np.array(c) for c in S['gsd_cells_float']]; dogc = [cells[i] for i in S['dogstar_cells']]
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def union(ms):
    while len(ms) > 1: ms = [ms[i] + ms[i + 1] if i + 1 < len(ms) else ms[i] for i in range(0, len(ms), 2)]
    return ms[0]
GSD = union([hull(c) for c in cells])
C8 = np.array(list(itertools.product((1, -1), repeat=3)), float)
RID = np.array([r for a in (1, -1) for b in (1, -1) for r in ([0, a / phi, b * phi], [a / phi, b * phi, 0], [b * phi, 0, a / phi])], float)
DOD = np.vstack([C8, RID])
dod_at = lambda k: hull(DOD * s + 2 * s * np.array(k, float))
dog_at = lambda k: union([hull(c * s + 2 * s * np.array(k, float)) for c in dogc])
B = json.load(open(os.path.join(DATA, 'b_exact.json')))['B4']
def canon(k): return min(tuple(sg * x for sg, x in zip(sgs, k[i:] + k[:i])) for i in range(3) for sgs in itertools.product((1, -1), repeat=3))
orb_keys = [eval(r) for r, v in B.items() if 0 < v['float'] < 1]
parts = []; legend = []
for oi, rk in enumerate(sorted(orb_keys, key=lambda k: -B[str(k)]['float'])):
    ks = [k for k in itertools.product(range(-5, 6), repeat=3) if canon(k) == rk]
    pieces = [(dod_at(k) if sum(k) % 2 == 0 else dog_at(k)) ^ GSD for k in ks]
    parts.append((union(pieces), ORBCOL[oi % len(ORBCOL)], .55)); legend.append((ORBCOL[oi % len(ORBCOL)], f'{len(ks)} {"dodecahedra" if sum(rk) % 2 == 0 else "Dogstars"} {rk}: {B[str(rk)]["float"]:.3f} inside'))
sun_core = dod_at((0, 0, 0)); sun_dogs = union([dog_at(e) for e in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))])
vg = sum(p[0].volume() for p in parts); gap_exact = 2668 - 1192 * 5 ** .5
print(f'render check: the cut lattice pieces fill {vg:.6f} (exact gap {gap_exact:.6f})', flush=True)
if abs(vg - gap_exact) > 1e-6: fails.append('cut pieces volume != gap')
def mesh(mf):
    me = mf.to_mesh(); return np.asarray(me.vert_properties[:, :3]), np.asarray(me.tri_verts)
def draw(ax, mf, col, alpha, ex=0.0, ec='none'):
    P, T = mesh(mf)
    if len(T) == 0: return
    tri = P[T]; c = tri.mean(1); off = c / np.maximum(np.linalg.norm(c, axis=1)[:, None], 1e-9) * ex
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1)[:, None], 1e-12)
    light = np.clip(.45 + .55 * (n @ np.array([.4, -.5, .75]) / np.linalg.norm([.4, -.5, .75])), .15, 1)
    rgb = np.array(matplotlib.colors.to_rgb(col)); fc = np.c_[light[:, None] * rgb, np.full(len(T), alpha)]
    ax.add_collection3d(Poly3DCollection(tri + off[:, None, :], facecolors=fc, edgecolors=ec, linewidths=.1))
def frame(ax, R=1.85):
    ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_zlim(-R, R); ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_facecolor(BG); ax.view_init(22, 32)
fig = plt.figure(figsize=(15, 5.6), facecolor=BG)
ax = fig.add_subplot(131, projection='3d'); frame(ax); draw(ax, GSD, PALE, .22); draw(ax, sun_core, GOLD, 1); draw(ax, sun_dogs, PURPLE, 1)
ax.set_title('the great star (see-through) and the small Sunstar\ninside it: 10.7% of its volume', color=INK, fontsize=10)
half = m3.Manifold.cube([4, 4, 4]).translate([-2, -2, 0])                                   # cut away the upper half (z > 0)
ax = fig.add_subplot(132, projection='3d'); frame(ax)
for mf, col, a in parts: draw(ax, mf - half, col, 1)
draw(ax, sun_core - half, GOLD, 1); draw(ax, sun_dogs - half, PURPLE, 1)
ax.set_title('the filler, cut open (lower half): the neighbouring 1/φ³\nSunstar Lattice pieces, each trimmed by the great star', color=INK, fontsize=10)
ax = fig.add_subplot(133, projection='3d'); frame(ax, 2.3)
for mf, col, a in parts: draw(ax, mf, col, 1, ex=.35)
draw(ax, sun_core, GOLD, 1); draw(ax, sun_dogs, PURPLE, 1)
ax.set_title('drawn apart: 118 trimmed pieces in 9 kinds,\nno piece whole (exact)', color=INK, fontsize=10)
for i, (c, t) in enumerate(legend): fig.text(.70, .26 - i * .026, '■ ' + t, color=c, fontsize=8)
fig.text(.99, .01, MARK, ha='right', color=INK, fontsize=8, alpha=.8)
fig.suptitle('#42: what fills between the great star and the Sunstar inside it', color=INK, fontsize=12)
fig.savefig(os.path.join(FIG, 'fig-b3-filler.png'), dpi=150, facecolor=BG); plt.close(fig)
# ---------- part A render ----------
def cycp(v):
    out = set()
    for k in range(3):
        p = v[k:] + v[:k]
        for sg in itertools.product((1, -1), repeat=3): out.add(tuple(round(a * b, 12) for a, b in zip(p, sg)))
    return np.array(sorted(out))
I = cycp([0, .5, phi / 2]); hI = ConvexHull(I)
D1 = np.unique(np.round([3 * I[list(t)].mean(0) for t in hI.simplices], 9), axis=0); I2 = I * phi ** 3
hD = ConvexHull(D1); facesD = {}
for simp, eq in zip(hD.simplices, hD.equations): facesD.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
spires = [hull(np.vstack([D1[list(ix)], [5 ** .5 * D1[list(ix)].mean(0)]])) for ix in facesD.values()]
eqI = np.unique(np.round(hI.equations, 9), axis=0)
GIf = []                                                     # GI(I): 20 big triangles in I's planes; as a solid: union of cones from O
for e in eqI:
    G = I2[np.abs(I2 @ e[:3] + e[3]) < 1e-6]; GIf.append(G)
pv = pickle.load(open(os.path.join(DATA, 'a_visible.pkl'), 'rb')) if os.path.exists(os.path.join(DATA, 'a_visible.pkl')) else None
fig = plt.figure(figsize=(11, 5.6), facecolor=BG)
ax = fig.add_subplot(121, projection='3d'); frame(ax, 4.6)
hI2 = ConvexHull(I2); fI2 = {}
for simp, eq in zip(hI2.simplices, hI2.equations): fI2.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
inward = [hull(np.vstack([I2[list(ix)], [D1[np.argmax(D1 @ np.array(eq[:3]))]]])) for eq, ix in fI2.items()]
GDm = hull(I2) - union(inward)
draw(ax, hull(I2), PALE, .12); draw(ax, GDm, '#e07b7b', 1)
ax.set_title('reciprocal of the small stellated shell: the great dodecahedron\n= D1 + 12 spires + 30 valley tetrahedra, in hull I2 (exact)', color=INK, fontsize=9)
ax = fig.add_subplot(122, projection='3d'); frame(ax, 4.6)
if pv is not None:
    tris = np.array([t for _, _, T in pv['visGI'] for t in T])
    GIm = union([hull(np.vstack([[0, 0, 0], t])) for t in tris])
    draw(ax, GIm - hull(D1), '#5fb3d9', 1); draw(ax, hull(D1), GOLD, .35)
ax.set_title('reciprocal of the great stellated shell: the great icosahedron\nbreaks through D1 (gold); its 12 points stand over I\'s corners', color=INK, fontsize=9)
fig.text(.99, .01, MARK, ha='right', color=INK, fontsize=8, alpha=.8)
fig.savefig(os.path.join(FIG, 'fig-a1-reciprocal.png'), dpi=150, facecolor=BG); plt.close(fig)
print('FINAL ok' if not fails else 'FINAL FAIL: ' + '; '.join(fails))
