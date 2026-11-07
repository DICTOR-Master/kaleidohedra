#!/usr/bin/env python3
"""Two figures of the Admiral Cap network for Space-Fillers and Lattice Moves, Chapter (Admiral network) — 7 Nov 2026.
Geometry exactly as build_admiral_octet.py / twin_ground_state.py: the octet with corners at even-sum points of Z^3 (edge sqrt2),
octahedra |x - c|_1 <= 1 at odd-sum c, each = Pacioli icosahedron (corners on the 12 edges, golden division, twin 0 or 1)
+ six Admiral Caps (each two tetrahedra over an icosahedron edge, a dent between; #47, edgeRoof.js).
fig-admiral-caps.png  (a) one octahedron = icosahedron + six Admiral Caps, drawn apart; (b) the six Admiral Caps and eight tetrahedra
                      round one octet corner, drawn apart, one cap solid, the rest glass.
fig-twin-layers.png   (a) a block of the ground state twin(c) = parity(c_x), layers along x drawn apart, matched shared edges blue;
                      (b) one octet corner: 8 of its 12 shared edges matched, 4 carry a T-junction.
Painter's renderer and house look copied from studies/2026-11-04-hopf-interlock/scripts/render_held.py.
Checks: volume I + 6 caps = octahedron (4/3); every interior octet corner of the ground state has exactly 8 of 12 shared edges matched.
Usage: render_admiral_figs.py OUTDIR"""
import os, sys, math, itertools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.colors import to_rgb

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)
GOLD, VIOLET, BLUE, INK, GREY = '#d9a520', '#7b4fa8', '#3f7fc4', '#2b2620', '#9a9288'
LIGHT = np.array([-0.35, -0.5, 0.8]); LIGHT /= np.linalg.norm(LIGHT)
plt.rcParams['font.family'] = 'DejaVu Sans'
phi = (1 + 5**.5)/2; a, b = 1/phi**2, 1/phi

# ---------------- geometry ----------------
def ico(t, c=(0, 0, 0)):
    p, q = (a, b) if t == 0 else (b, a); out = []
    for k in range(3):
        for s1, s2 in itertools.product((1, -1), repeat=2):
            v = [0, 0, 0]; v[(k+1) % 3] = s1*p; v[(k+2) % 3] = s2*q; out.append(v)
    return np.array(out, float) + np.asarray(c, float)

def ico_faces(V):
    e = 2*a; F = []
    for i, j, k in itertools.combinations(range(12), 3):
        if all(abs(np.linalg.norm(V[x] - V[y]) - e) < 1e-9 for x, y in ((i, j), (j, k), (i, k))): F.append([V[i], V[j], V[k]])
    assert len(F) == 20; return F

def tet_faces(P): return [[P[i] for i in f] for f in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))]

def octa_faces(c):
    c = np.asarray(c, float); F = []
    for s in itertools.product((1, -1), repeat=3):
        F.append([c + [s[0], 0, 0], c + [0, s[1], 0], c + [0, 0, s[2]]])
    return F

def octa_edges(c):
    c = np.asarray(c, float); E = []
    for i, j in itertools.combinations(range(3), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            u = c.copy(); u[i] += si; w = c.copy(); w[j] += sj; E.append((u, w))
    return E

def cap_tets(c, t, e):
    """The Admiral Cap of octahedron c (twin t) at its corner c + e: two tetrahedra (as build_admiral_octet.py)."""
    c = np.asarray(c, float); e = np.asarray(e, float); I = ico(t, c); corner = c + e
    near = [v for v in I if abs(np.abs(v - c).sum() - 1) < 1e-9 and (v - c) @ e > 1e-9]
    pr = [(i1, i2) for i1, i2 in itertools.combinations(range(4), 2)
          if abs(np.linalg.norm(near[i1] - near[i2]) - 2*a) < 1e-9 and abs((near[i1] - near[i2]) @ e) < 1e-9]
    assert len(near) == 4 and len(pr) == 1
    e0, e1 = near[pr[0][0]], near[pr[0][1]]
    return [np.array([corner, e0, e1, near[k]]) for k in range(4) if k not in pr[0]]

def cap_faces(c, t, e):
    """Outer boundary of the non-convex cap: the 6 triangles of its two tetrahedra other than the shared one, with outward normals."""
    T = cap_tets(c, t, e); out = []
    for P in T:
        g = P.mean(0)
        for F in tet_faces(P):
            F = np.array(F)
            shared = all(any(np.allclose(x, y) for y in T[0]) for x in F) and all(any(np.allclose(x, y) for y in T[1]) for x in F)
            if shared: continue
            n = np.cross(F[1] - F[0], F[2] - F[0]); n /= np.linalg.norm(n)
            if n @ (F.mean(0) - g) < 0: n = -n
            out.append((F, n))
    assert len(out) == 6; return out

def tvol(P): return abs(np.linalg.det(np.array([P[1] - P[0], P[2] - P[0], P[3] - P[0]])))/6

def ico_vol(V):
    g = V.mean(0); return sum(tvol(np.array([g, *F])) for F in ico_faces(V))

def corner_on(c, t, u, w):
    for v in ico(t, c):
        if abs(np.linalg.norm(v - u) + np.linalg.norm(v - w) - np.linalg.norm(u - w)) < 1e-9: return v
    raise ValueError

# check 1: I + 6 caps = octahedron
I0 = ico(0); vol = ico_vol(I0) + sum(tvol(P) for i in range(3) for s in (1, -1) for P in cap_tets((0, 0, 0), 0, np.eye(3)[i]*s))
assert abs(vol - 4/3) < 1e-12, vol
print('check: icosahedron + 6 Admiral Caps =', round(vol, 12), '= 4/3 (octahedron)')

# ---------------- renderer (render_held.py) ----------------
class Cam:
    def __init__(self, target, az, el, dist, ortho=False):
        A, E = math.radians(az), math.radians(el)
        self.f = -np.array([math.cos(E)*math.cos(A), math.cos(E)*math.sin(A), math.sin(E)])
        self.E = np.array(target, float) - dist*self.f
        up = np.array([0, 0, 1.0]) if abs(self.f[2]) < 0.99 else np.array([0, 1.0, 0])
        self.r = np.cross(self.f, up); self.r /= np.linalg.norm(self.r); self.u = np.cross(self.r, self.f)
        self.ortho, self.dist = ortho, dist
    def proj(self, P):
        d = np.asarray(P, float) - self.E; z = d @ self.f
        s = 1.0 if self.ortho else self.dist/z
        return np.c_[(d @ self.r)*s, (d @ self.u)*s], z

def shade(col, n, k=1.0):
    c = np.array(to_rgb(col)); l = 0.62 + 0.38*max(0.0, float(n @ LIGHT)); return np.clip(c*l*k + (1 - k), 0, 1)

def items(faces, style, col, shift=(0, 0, 0), alpha=None, centre=None, lw=None):
    """faces: list of (F, n) or plain F (normal oriented away from centre)."""
    out = []; shift = np.asarray(shift, float)
    for f in faces:
        if isinstance(f, tuple): F, n = np.asarray(f[0], float), f[1]
        else:
            F = np.asarray(f, float); n = np.cross(F[1] - F[0], F[2] - F[0]); n /= np.linalg.norm(n)
            if centre is not None and n @ (F.mean(0) - centre) < 0: n = -n
        F = F + shift
        if style == 'solid':
            out.append((F, (*shade(col, n), 1.0 if alpha is None else alpha), (*to_rgb(INK), 0.9), lw or 0.55, alpha is None, n))
        elif style == 'glass':
            out.append((F, (*shade(col, n, 0.85), 0.10 if alpha is None else alpha), (*to_rgb(col), 0.55), lw or 0.4, False, n))
        elif style == 'ghost':
            out.append((F, (1, 1, 1, 0.0), (*to_rgb(col), 0.7), lw or 0.5, False, n))
    return out

def draw(ax, cam, its, lines=(), dots=(), pad=0.06):
    polys, fcs, ecs, lws, depth, ls = [], [], [], [], [], []
    for F, fc, ec, lw, cull, n in its:
        if cull and n @ (F.mean(0) - cam.E) > 0: continue
        P2, z = cam.proj(F)
        polys.append(P2); fcs.append(fc); ecs.append(ec); lws.append(lw); depth.append(z.mean())
        ls.append('--' if fc[3] == 0.0 else '-')
    order = np.argsort(depth)[::-1]
    ax.add_collection(PolyCollection([polys[i] for i in order], facecolors=[fcs[i] for i in order], edgecolors=[ecs[i] for i in order],
                                     linewidths=[lws[i] for i in order], linestyles=[ls[i] for i in order], joinstyle='round'))
    allp = [np.vstack(polys)]
    for (p, q, col, lw, style) in lines:
        P2, _ = cam.proj([p, q]); allp.append(P2)
        ax.plot(P2[:, 0], P2[:, 1], color=col, lw=lw, ls=style, solid_capstyle='round', zorder=3)
    for (p, col, size, mk) in dots:
        P2, _ = cam.proj([p]); ax.plot(P2[0, 0], P2[0, 1], mk, color=col, ms=size, mfc=col if mk == 'o' else 'white', mew=1.0, zorder=4)
    allp = np.vstack(allp)
    ax.set_xlim(allp[:, 0].min() - pad, allp[:, 0].max() + pad); ax.set_ylim(allp[:, 1].min() - pad, allp[:, 1].max() + pad)
    ax.set_aspect('equal'); ax.axis('off')

def mark(fig): fig.text(0.992, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=7.5, color='#8a8070')
def save(fig, name):
    p = os.path.join(OUT, name); fig.savefig(p, dpi=220, facecolor='white'); plt.close(fig); print('wrote', p)

E6 = [np.eye(3)[i]*s for i in range(3) for s in (1, -1)]

# ================= Figure A: the Admiral Caps =================
fig, axs = plt.subplots(1, 2, figsize=(12, 5.6), gridspec_kw=dict(width_ratios=[1, 1.15]))
# (a) one octahedron, its icosahedron and six caps drawn apart
its = items(ico_faces(I0), 'solid', GOLD, centre=np.zeros(3))
its += items(octa_faces((0, 0, 0)), 'ghost', GREY, centre=np.zeros(3), lw=0.6)
for e in E6: its += items(cap_faces((0, 0, 0), 0, e), 'solid', BLUE, shift=0.62*e)
cam = Cam((0, 0, 0), -57, 24, 9)
draw(axs[0], cam, its)
axs[0].set_title('a   one octahedron: icosahedron + six Admiral Caps', loc='left', fontsize=10.5, color=INK)
# (b) round one octet corner O: six caps (one solid), eight tetrahedra, icosahedra as glass further out
s_cap, s_tet = 0.62, 1.3
its = []; solid_e = np.array([0, -1.0, 0])
for c in E6:
    e = -c; t = int(abs(c[0]) == 1)                     # ground-state twins twin(c) = parity(c_x)
    sh = s_cap*c
    style = 'solid' if np.allclose(c, -solid_e) else 'glass'
    its += items(cap_faces(c, t, e), style, BLUE, shift=sh, alpha=None if style == 'solid' else 0.50)
for lo in itertools.product((-1, 0), repeat=3):
    cs = [np.array(lo) + np.array(d) for d in itertools.product((0, 1), repeat=3)]
    P = np.array([x for x in cs if x.sum() % 2 == 0], float)
    d = np.array(lo) + 0.5; d /= np.linalg.norm(d)
    its += items(tet_faces(P), 'glass', VIOLET, shift=s_tet*d, alpha=0.05, centre=P.mean(0))
cam = Cam((0, 0, 0), -38, 30, 13)
draw(axs[1], cam, its, dots=[((0, 0, 0), INK, 4.5, 'o')])
axs[1].set_title('b   round one octet corner: six Admiral Caps, eight tetrahedra', loc='left', fontsize=10.5, color=INK)
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.03, wspace=0.04); mark(fig); save(fig, 'fig-admiral-caps.png')

# ================= Figure B: twin layers, matched edges =================
def twin(c): return int(c[0]) % 2                     # twin(c) = parity(c_x) XOR f(c_y), here f = 0
def shared_edges(cs):
    """All octahedron edges shared by two octahedra of the set cs, with match flag and the two icosahedron corners on them."""
    S = {tuple(c) for c in cs}; out = []
    for c in cs:
        for d in [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)]:
            c2 = tuple(np.add(c, d))
            if c2 not in S: continue
            nz = [i for i in range(3) if d[i]]
            u = np.array(c, float); u[nz[0]] += d[nz[0]]; w = np.array(c, float); w[nz[1]] += d[nz[1]]
            p1, p2 = corner_on(c, twin(c), u, w), corner_on(c2, twin(c2), u, w)
            out.append((tuple(c), c2, u, w, np.allclose(p1, p2), p1, p2))
    return out

# check 2: every octet corner inside a big box has exactly 8 of 12 shared edges matched
big = [c for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2 == 1]
SE = shared_edges(big); cnt = {}
for c1, c2, u, w, m, p1, p2 in SE:
    for v in (u, w):
        k = tuple(v.astype(int)); cnt.setdefault(k, [0, 0]); cnt[k][0] += 1; cnt[k][1] += int(m)
full = {k: v for k, v in cnt.items() if v[0] == 12}
assert full and all(v[1] == 8 for v in full.values()), {v[1] for v in full.values()}
print(f'check: {len(full)} interior octet corners, each with 8 of 12 shared edges matched (ground state twin = parity(c_x))')

fig, axs = plt.subplots(1, 2, figsize=(12.4, 5.8), gridspec_kw=dict(width_ratios=[1.15, 1]))
# (a) one layer of octahedra (centres at z = 0) seen from above: twins alternate along x; every shared edge marked
blk = [c for c in itertools.product(range(0, 5), range(0, 4), (0,)) if sum(c) % 2 == 1]
its = []; lines = []; dots = []
for c in blk:
    t = twin(c); col = GOLD if t == 0 else VIOLET; cc = np.array(c, float)
    its += items(ico_faces(ico(t, c)), 'solid', col, centre=cc)
    its += items(octa_faces(c), 'ghost', GREY, centre=cc, lw=0.5)
for c1, c2, u, w, m, p1, p2 in shared_edges(blk):
    lines.append((u + [0, 0, .01], w + [0, 0, .01], BLUE if m else INK, 3.0 if m else 1.1, '-' if m else (0, (2, 2))))
    if m: dots.append((p1, BLUE, 5.0, 'o'))
    else: dots += [(p1, INK, 4.6, 's'), (p2, INK, 4.6, 's')]
cam = Cam((2, 1.5, 0), -90, 89.9, 50, ortho=True)
draw(axs[0], cam, its, lines=lines, dots=dots)
axs[0].set_title('a   one layer from above: twins alternate along x', loc='left', fontsize=10.5, color=INK)
# (b) one octet corner O = (0,0,0)? use an even-sum interior point; six octahedra round it
O = np.array([2, 1, 1]); six = [tuple(O + e.astype(int)) for e in E6]
its = []; lines = []; dots = [(O, INK, 4.5, 'o')]
for c in six:
    t = twin(c); col = GOLD if t == 0 else VIOLET; cc = np.array(c, float)
    its += items(ico_faces(ico(t, c)), 'solid', col, alpha=0.22, centre=cc, lw=0.25)
    its += items(octa_faces(c), 'glass', GREY, alpha=0.03, centre=cc, lw=0.3)
nm = 0; nt = 0
for c1, c2, u, w, m, p1, p2 in shared_edges(six):
    if not (np.allclose(u, O) or np.allclose(w, O)): continue
    nt += 1; nm += int(m)
    lines.append((u, w, BLUE if m else INK, 2.6 if m else 1.0, '-' if m else (0, (2, 2))))
    if m: dots.append((p1, BLUE, 4.0, 'o'))
    else: dots += [(p1, INK, 4.2, 's'), (p2, INK, 4.2, 's')]
assert (nt, nm) == (12, 8), (nt, nm)
cam = Cam(O, -50, 28, 13)
draw(axs[1], cam, its, lines=lines, dots=dots)
axs[1].set_title(f'b   one octet corner: {nm} of {nt} shared edges matched', loc='left', fontsize=10.5, color=INK)
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.03, wspace=0.04); mark(fig); save(fig, 'fig-twin-layers.png')
print('OK render_admiral_figs.py')
