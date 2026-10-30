# Figures for paper A of the Star Cores book, "Star Cores of DICTO's Solids" (2026-10-31).
#   polar-fill.png   the polar-spike fill (tip of face n.x = c at rho^2 n / c, rho^2 = phi R^2): star | layer pieces apart | halo,
#                    top row DICTO GTI (D40), bottom row DICTO OCD Stella (D29, pyritohedral Th)
#   star-gallery.png 3 x 4 stars (polar rule, rho^2 = phi R^2) inside their halos (see-through shell)
#   valley.png       the valley rule of star_valley.py (t = 2): FPD freezes, Lahdeli keeps building, steps 1-3
# Rendering: own orthographic painter (each convex piece back-face culled, faces sorted far to near), Lambert shading, white
# background, dark edges >= 1.5 px at 300 dpi; only the halo shell is see-through. Construction code from star_core.py,
# polar_spikes.py and star_valley.py (imported, not copied). Usage: [FIGS=polar,gallery,valley] figs_paper_a.py <dataset dir> <out dir> <logo png>
import json, os, sys, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_core import faces_info, polyvol, vol, load
import star_valley as SV

phi = (1 + 5 ** .5) / 2
DS, OUT, LOGO = sys.argv[1:4]
os.chdir(DS); os.makedirs(OUT, exist_ok=True)
GOLD, VIOLET, TEAL, LILAC, EDGE, HALO = '#d4af37', '#8e5bd6', '#2bb3a3', '#c4a6ee', '#1d1d24', '#9aa3b5'
EW = 0.5                                     # points: 0.5 pt = 2.1 px at 300 dpi
LIGHT = np.array([-0.35, 0.55, 0.76]); LIGHT /= np.linalg.norm(LIGHT)
logo = plt.imread(LOGO)

def rot(elev, azim):
    a, e = np.radians(azim), np.radians(elev)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    # world z up -> screen y; view along -z after rotation
    M = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    return Rx @ M @ Rz
def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); k = 0.50 + 0.50 * max(0.0, float(n @ LIGHT))
    return tuple(np.clip(c * k + 0.06 * (1 - k), 0, 1))
def hull_faces(Q):
    """faces of the convex hull of Q as ordered polygons (coplanar triangles merged), with outward normals"""
    h = ConvexHull(Q); out = {}
    for eq in h.equations:
        k = tuple(np.round(eq, 6))
        if k in out: continue
        ids = [i for i, p in enumerate(Q) if abs(eq[:3] @ p + eq[3]) < 1e-7 * (1 + np.abs(Q).max())]
        R = Q[ids]; c = R.mean(0); n = eq[:3]; a = R[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out[k] = (R[np.argsort(np.arctan2((R - c) @ b, (R - c) @ a))], n)
    return list(out.values())
class Scene:
    def __init__(s, M): s.M = M; s.items = []          # (depth, poly2d, face rgba, edge rgba, lw, z-order layer)
    def convex(s, Q, col, layer=1, lw=EW):
        d0 = float((Q.mean(0) @ s.M.T)[2])             # whole piece at its centroid depth (pieces are disjoint convex)
        for P, n in hull_faces(Q):
            nn = s.M @ n
            if nn[2] <= 1e-9: continue
            W = P @ s.M.T; s.items.append((layer, d0 + 1e-6 * W[:, 2].mean(), W[:, :2], shade(col, nn), EDGE, lw))
    def tris(s, V, F, cols, layer=1, lw=EW):
        """an oriented (outward ccw) polygon surface, not necessarily convex: cull back faces, sort by depth"""
        W = V @ s.M.T
        for f, col in zip(F, cols):
            P = W[f]; n = np.zeros(3)
            for i in range(len(f)): n += np.cross(P[i], P[(i + 1) % len(f)])
            if n[2] <= 0.03 * np.linalg.norm(n): continue      # back-facing or edge-on slivers (no visible area; they mis-sort)
            s.items.append((layer, P[:, 2].mean(), P[:, :2], shade(col, n / np.linalg.norm(n)), EDGE, lw))
    def shell(s, Q):
        """see-through halo: back faces first (layer 0), front faces last (layer 2)"""
        for P, n in hull_faces(Q):
            W = P @ s.M.T; front = (s.M @ n)[2] > 0
            s.items.append((2 if front else 0, W[:, 2].mean(), W[:, :2], (0.62, 0.68, 0.80, 0.13 if front else 0.10),
                            (0.30, 0.34, 0.44, 0.85 if front else 0.35), 0.40 if front else 0.25))
    def draw(s, ax, lim):
        s.items.sort(key=lambda t: (t[0], t[1]))
        ax.add_collection(PolyCollection([t[2] for t in s.items], facecolors=[t[3] for t in s.items], edgecolors=[t[4] for t in s.items],
                                         linewidths=[t[5] for t in s.items], joinstyle='round', antialiased=True))
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal'); ax.axis('off')
def mark(fig):
    a = fig.add_axes([0.925, 0.008, 0.065, 0.065 * fig.get_figwidth() / fig.get_figheight()]); a.imshow(logo); a.axis('off')

def polar(fn, t=phi):
    d, V, F = load(fn); V = V - V.mean(0); FI = faces_info(V, F); R2 = float((np.linalg.norm(V, axis=1) ** 2).max()); rho2 = t * R2
    tips = np.array([rho2 * n / c for _, n, c in FI])
    spikes = [np.vstack([V[f], tp]) for (f, _, _), tp in zip(FI, tips)]
    fa = {v: [i for i, (f, _, _) in enumerate(FI) if v in f] for v in range(len(V))}
    E = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f, _, _ in FI for i in range(len(f))})
    corner = [np.vstack([V[v]] + [tips[i] for i in fa[v]]) for v in range(len(V))]
    edge = [np.vstack([V[a], V[b]] + [tips[i] for i in fa[a] if i in fa[b]]) for a, b in E]
    VS = polyvol(V, F); VH = vol(tips); star = VS + sum(map(vol, spikes)); lay = sum(map(vol, corner + edge))
    assert abs(lay - (VH - star)) < 1e-7 * VH, (fn, lay, VH - star)
    return dict(V=V, F=F, FI=FI, tips=tips, spikes=spikes, corner=corner, edge=edge, rho2=rho2, R=R2 ** .5, VS=VS, VH=VH, star=star)
def spike_cols(FI):
    """spikes violet / teal by face family (sides, distance): largest family violet, the rest teal"""
    keys = [(len(f), round(c, 6)) for f, _, c in FI]; cnt = {}
    for k in keys: cnt[k] = cnt.get(k, 0) + 1
    order = sorted(cnt, key=lambda k: (-k[0], k[1])); first = order[0]
    return [VIOLET if k == first else TEAL for k in keys]
VIEW = (20, 24)

# ---------------- figure 1: polar fill ----------------
def fig_polar():
    rows = [('dicto-gti.json', 'GTI (D40)'), ('dicto-ocd-stella.json', 'OCD Stella (D29)')]
    fig, axs = plt.subplots(2, 3, figsize=(8, 5.6), gridspec_kw=dict(wspace=0.02, hspace=0.16))
    M = rot(*VIEW); info = []
    for r, (fn, nm) in enumerate(rows):
        g = polar('solids/' + fn); cols = spike_cols(g['FI']); lim = 1.04 * np.linalg.norm(g['tips'], axis=1).max()
        S = Scene(M)
        for Q, c in zip(g['spikes'], cols): S.convex(Q, c)
        S.draw(axs[r, 0], lim)
        S = Scene(M); k = 0.45                     # explode: each piece moved out along its centroid
        for Q, c in [(Q, GOLD) for Q in g['corner']] + [(Q, TEAL) for Q in g['edge']]:
            if vol(Q) <= 1e-12: continue
            S.convex(Q + k * Q.mean(0), c)
        S.draw(axs[r, 1], lim * (1 + k))
        S = Scene(M); S.convex(g['tips'], '#e9e4f4'); S.draw(axs[r, 2], lim)
        nc, ne = len(g['corner']), len(g['edge'])
        axs[r, 0].set_title(f'{nm}: star\n{len(g["spikes"])} polar spikes', fontsize=7.8)
        axs[r, 1].set_title(f'layer, drawn apart: {nc} corner\npyramids (gold), {ne} edge tetrahedra (teal)', fontsize=7.8)
        axs[r, 2].set_title(f'halo: hull of the {len(g["tips"])} tips\n(one facet over each corner)', fontsize=7.8)
        info.append(dict(shape=nm, rho2_over_R2=phi, R=g['R'], rho=g['rho2'] ** .5, star_over_solid=g['star'] / g['VS'], halo_over_solid=g['VH'] / g['VS'],
                         corner_pieces=nc, edge_pieces=ne))
    fig.text(0.5, 0.015, 'polar spikes: tip of face n·x = c at ρ²n/c, ρ² = φR²;  star + layer = halo', ha='center', fontsize=8.5)
    mark(fig); fig.savefig(os.path.join(OUT, 'polar-fill.png'), dpi=300, facecolor='white'); plt.close(fig); return info

# ---------------- figure 2: gallery ----------------
GAL = [('dicto-gti.json', 'GTI', 'D40'), ('dicto-fpd.json', 'FPD', 'D41'), ('dicto-ogdoecontahedron.json', 'OG', 'D28'),
       ('dicto-ocd-stella.json', 'OCD Stella', 'D29'), ('dicto-dbt.json', 'DBT', 'D37'), ('dicto-ott.json', 'OTT', 'D38'),
       ('dicto-hecatodihedron.json', 'TI Hecatodihedron', 'D22'), ('dicto-red-king.json', 'Red King', 'D98'),
       ('dicto-tweedledum.json', 'Tweedledum', 'D89'), ('dicto-lion.json', 'Lion', 'D87'), ('dicto-star-halo.json', 'Star Halo', 'D104'),
       ('dicto-ti-star-core.json', 'TI Star core', 'D105')]
def fig_gallery():
    fig, axs = plt.subplots(3, 4, figsize=(8, 6.5), gridspec_kw=dict(wspace=0.02, hspace=0.12)); M = rot(*VIEW); info = []
    for ax, (fn, nm, D) in zip(axs.flat, GAL):
        g = polar('solids/' + fn); cols = spike_cols(g['FI']); lim = 1.03 * np.linalg.norm(g['tips'], axis=1).max()
        S = Scene(M); S.shell(g['tips'])
        for Q, c in zip(g['spikes'], cols): S.convex(Q, c)
        S.draw(ax, lim); ax.set_title(f'{nm} ({D})', fontsize=8.5)
        info.append(dict(shape=nm, D=D, faces=len(g['F']), halo_over_solid=g['VH'] / g['VS'], star_over_solid=g['star'] / g['VS']))
    fig.text(0.5, 0.012, 'stars with polar spikes (ρ² = φR²) inside their halos (see-through)', ha='center', fontsize=8.5)
    mark(fig); fig.savefig(os.path.join(OUT, 'star-gallery.png'), dpi=300, facecolor='white'); plt.close(fig); return info

# ---------------- figure 3: valley rule ----------------
def valley_build(fn, t, steps=3):
    """star_valley.run, keeping the surface after each step; each face tagged with the step that made it"""
    clash, geo = SV.clash, SV.geo
    d, V, F = load(fn); V = V - V.mean(0); F = [list(f) for f in F]
    old = [np.vstack([V[f], np.zeros(3)]) for f in F]; OG = [geo(Q) for Q in old]; below = list(old); tag = [0] * len(F); out = []
    for k in range(1, steps + 1):
        FI = faces_info(V, F); base = []
        for (f, n, c), P in zip(FI, below):
            h = (P - V[f[0]]) @ n; A = P[np.abs(h - h.min()) < 1e-9].mean(0); foot = A + (c - A @ n) * n; base.append((f, A, foot))
        spike = lambda i, s: np.vstack([V[base[i][0]], base[i][1] + s * (base[i][2] - base[i][1])])
        def free_old(i, s):
            Q = spike(i, s); g = geo(Q); return not any(clash(Q, g, P, G) for P, G in zip(old, OG))
        S = []
        for i in range(len(base)):
            if free_old(i, t): S.append(t); continue
            lo, hi = 1.0, t
            for _ in range(30):
                mid = (lo + hi) / 2
                if free_old(i, mid): lo = mid
                else: hi = mid
            S.append(lo)
        for _ in range(12):
            Qs = [spike(i, s) for i, s in enumerate(S)]; Gs = [geo(Q) if s > 1 + 1e-9 else None for Q, s in zip(Qs, S)]
            pairs = [(i, j) for i in range(len(S)) for j in range(i + 1, len(S)) if Gs[i] and Gs[j] and clash(Qs[i], Gs[i], Qs[j], Gs[j])]
            if not pairs: break
            for i, j in pairs:
                lo, hi = 1.0, min(S[i], S[j])
                for _ in range(30):
                    mid = (lo + hi) / 2; A_, B_ = spike(i, min(S[i], mid)), spike(j, min(S[j], mid))
                    if clash(A_, geo(A_), B_, geo(B_)): hi = mid
                    else: lo = mid
                S[i] = min(S[i], lo); S[j] = min(S[j], lo)
        V2 = list(V); F2 = []; B2 = []; T2 = []
        for i, (f, A, foot) in enumerate(base):
            if S[i] <= 1 + 1e-9: F2.append(list(f)); B2.append(below[i]); T2.append(tag[i]); continue
            tip = A + S[i] * (foot - A); ti = len(V2); V2.append(tip); Q = np.vstack([V[f], tip]); old.append(Q); OG.append(geo(Q))
            for a in range(len(f)): F2.append([f[a], f[(a + 1) % len(f)], ti]); B2.append(Q); T2.append(k)
        fr = [(s - 1) / (t - 1) for s in S]
        V, F, below, tag = np.array(V2), F2, B2, T2
        out.append(dict(V=V, F=F, tag=tag, full=sum(1 for x in fr if x > 1 - 1e-9), flat=sum(1 for x in fr if x < 1e-9), spikes=len(fr),
                        R=float(np.linalg.norm(V, axis=1).max()), vol=polyvol(V, F)))
    return out
def fig_valley(t=2.0):
    rows = [('dicto-fpd.json', 'FPD (D41)'), ('dicto-lahdeli.json', 'Lahdeli (D77)')]
    fig, axs = plt.subplots(3, 2, figsize=(8, 10.6), gridspec_kw=dict(wspace=0.02, hspace=0.2)); M = rot(*VIEW); info = []   # portrait, a full page (DICTO 10-31)
    STEPC = {0: GOLD, 1: VIOLET, 2: TEAL, 3: LILAC}
    for r, (fn, nm) in enumerate(rows):
        st = valley_build('solids/' + fn, t); lim = 1.04 * max(s['R'] for s in st); _, V0_, F0_ = load('solids/' + fn); V0_ = V0_ - V0_.mean(0); R0 = np.linalg.norm(V0_, axis=1).max(); V0 = polyvol(V0_, F0_)
        for k, s in enumerate(st):
            S = Scene(M); S.tris(s['V'], s['F'], [STEPC[x] for x in s['tag']]); S.draw(axs[k, r], lim)
            prev = st[k - 1]['R'] if k else R0; pv = st[k - 1]['vol'] if k else V0
            axs[k, r].set_title(f'{nm}, step {k + 1}: {len(s["F"])} triangles\n{s["full"]} of {s["spikes"]} spikes full height\nradius ×{s["R"] / prev:.3f}, volume ×{s["vol"] / pv:.3f}', fontsize=7.8)
            info.append(dict(shape=nm, step=k + 1, triangles=len(s['F']), full=s['full'], flat=s['flat'], spikes=s['spikes'], radius_over_last=s['R'] / prev, volume_over_last=s['vol'] / pv))
    fig.text(0.5, 0.012, 'valley rule, t = 2: spikes shortened until they clear the pieces already built and each other\n'
             'spikes of step 1 violet, step 2 teal, step 3 lilac (a face whose spike shrinks to nothing keeps its colour)', ha='center', fontsize=8.5)
    mark(fig); fig.savefig(os.path.join(OUT, 'valley.png'), dpi=300, facecolor='white'); plt.close(fig); return info

if __name__ == '__main__':
    which = os.environ.get('FIGS', 'polar,gallery,valley').split(','); rep = {}
    if 'polar' in which: rep['polar-fill'] = fig_polar()
    if 'gallery' in which: rep['star-gallery'] = fig_gallery()
    if 'valley' in which: rep['valley'] = fig_valley()
    json.dump(rep, open(os.path.join(OUT, 'figs-info-' + '-'.join(which) + '.json'), 'w'), indent=1, default=float); print(json.dumps(rep, indent=1, default=float))
