#!/usr/bin/env python3
"""Renders of the gorinto study: render standard (solid faces, crisp edges, painter's order, no haze), DICTO mark.
Colours: the Buddhist five colours of the rings (earth yellow, water white, fire red, wind black, void blue; ja.wikipedia 五輪塔)
for the traditional cell, the Platonic cell and every arrangement; the Kaleidohedra app's colours of the five solids only in the comparison panel.
Black reads on the white ground by itself; its edges are drawn light grey so the facets of the black octahedron stay visible.
Usage: render.py named.json search.json outdir"""
import sys, os, json, math, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-13-paradigm-expansion', 'scripts'))
import figlib as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gorinto import platonic_gorinto, faces_of, rotz, INVERT

BUD = {'earth': '#d8ae3a', 'water': '#efe7d6', 'fire': '#c83f2a', 'wind': '#2c2c30', 'void': '#2f5fae'}
BUD_EDGE = {'wind': '#b4b4b4'}
DICTO = {'earth': F.ELEM['C'], 'water': F.ELEM['I'], 'fire': F.ELEM['T'], 'wind': F.ELEM['O'], 'void': F.ELEM['D']}
named = json.load(open(sys.argv[1])); search = json.load(open(sys.argv[2])) if os.path.exists(sys.argv[2]) else None
OUT = sys.argv[3]; os.makedirs(OUT, exist_ok=True)

parts, H = platonic_gorinto(); Hf = float(H)
CELL = []
for p in parts:
    V = np.array([[float(c) for c in v] for v in p['V']]); V[:, 2] -= Hf / 2
    CELL.append((p['element'], V, [(f, None) for f in faces_of(V)]))


def add_cell(sc, M=np.eye(3), t=(0, 0, 0), pal=BUD, lw=1.1):
    for el, V, faces in CELL:
        W = V @ M.T + np.asarray(t, float)
        fs = []
        for f, _ in faces:
            n = np.cross(W[f[1]] - W[f[0]], W[f[2]] - W[f[0]]); fs.append((f, n))
        sc.solid(W, faces=fs, color=pal[el], edge=BUD_EDGE.get(el, F.INK) if pal is BUD else F.INK, lw=lw)


def finish(ax, sc, pad=0.04):
    sc.draw(ax); F.blank(ax)
    xs, ys = [], []
    for it in sc.items:
        if 'pts' in it:
            q = sc.proj(it['pts']); xs += list(q[:, 0]); ys += list(q[:, 1])
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys); dx, dy = (x1 - x0) * pad + 0.05, (y1 - y0) * pad + 0.05
    ax.set_xlim(x0 - dx, x1 + dx); ax.set_ylim(y0 - dy, y1 + dy)
    return (x0, x1, y0, y1)


# ------------------------------------------------ traditional cell (cm), from the Bōyama per-part maxima (see README)
def mesh_rev(profile, nseg=48):
    """surface of revolution about z from a profile [(r, z), ...] bottom to top: list of (pts, normal) quads/triangles."""
    out = []
    for k in range(nseg):
        a0, a1 = 2 * math.pi * k / nseg, 2 * math.pi * (k + 1) / nseg
        for (r0, z0), (r1, z1) in zip(profile, profile[1:]):
            P = [(r0 * math.cos(a0), r0 * math.sin(a0), z0), (r0 * math.cos(a1), r0 * math.sin(a1), z0),
                 (r1 * math.cos(a1), r1 * math.sin(a1), z1), (r1 * math.cos(a0), r1 * math.sin(a0), z1)]
            P = np.array(P); keep = [0, 1, 2, 3]
            if r0 < 1e-9: keep = [0, 2, 3]
            if r1 < 1e-9: keep = [0, 1, 2]
            out.append(P[keep])
    return out


def traditional():
    T = {}
    w, h = 53.3, 46.0
    T['earth'] = ('box', np.array([(x, y, z) for x in (-w / 2, w / 2) for y in (-w / 2, w / 2) for z in (0, h)]))
    R, hw = 25.0, 40.5                                  # water: sphere of diameter 50 cut to height 40.5
    c = h + hw / 2; zc = math.sqrt(R * R - (hw / 2) ** 2)
    prof = [(0, c - hw / 2)] + [(R * math.cos(math.asin(s / R)), c + s) for s in np.linspace(-hw / 2, hw / 2, 17)] + [(0, c + hw / 2)]
    T['water'] = ('rev', prof)
    z0 = h + hw; b = 53.0; hf = 32.0                    # fire: square pyramid (four-sided roof), base 53, height 32
    T['fire'] = ('pyr', np.array([(-b / 2, -b / 2, z0), (b / 2, -b / 2, z0), (b / 2, b / 2, z0), (-b / 2, b / 2, z0), (0, 0, z0 + hf)]))
    z1 = z0 + hf; rw = 13.0                             # wind: hemisphere of radius 13, flat side up, resting on the roof's apex
    prof = [(0, z1)] + [(rw * math.sin(a), z1 + rw - rw * math.cos(a)) for a in np.linspace(0, math.pi / 2, 10)][1:] + [(0, z1 + rw)]
    T['wind'] = ('rev', prof)
    z2 = z1 + rw; rj = 9.5; top = 153.0                 # void: jewel = sphere r 9.5 on the wind's top + tangent cone to 153 cm
    cz = z2 + rj; L = top - cz; ang = math.asin(rj / L)   # tangent circle
    zt = cz + rj * math.sin(ang); rt = rj * math.cos(ang)
    prof = [(0, z2)] + [(rj * math.sin(a), cz - rj * math.cos(a)) for a in np.linspace(0, math.pi / 2 + ang, 14)][1:] + [(0, top)]
    T['void'] = ('rev', prof)
    return T


def add_traditional(sc, pal=BUD, t=(0, 0, 0), s=1.0):
    off = np.asarray(t, float)
    for el, (kind, data) in traditional().items():
        ec = BUD_EDGE.get(el, F.INK)
        if kind in ('box', 'pyr'):
            V = data * s + off; fs = []
            for f in faces_of(V):
                n = np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]); fs.append((f, n))
            sc.solid(V, faces=fs, color=pal[el], edge=ec, lw=1.1)
        else:
            quads = mesh_rev(data)
            allp = np.vstack(quads) * s + off; cen = allp.mean(0)
            for Q in quads:
                Q = Q * s + off; n = np.cross(Q[1] - Q[0], Q[2] - Q[0])
                if np.linalg.norm(n) < 1e-12: continue
                if (Q.mean(0) - cen) @ n < 0: n = -n
                n = n / np.linalg.norm(n)
                if sc.R[2] @ n <= 0: continue
                sc.items.append(dict(pts=Q, n=n, col=pal[el], edge=pal[el], lw=0.25, alpha=1.0, front=True, z=0, glass=False,
                                     od=float(sc.R[2] @ cen)))


# ------------------------------------------------ figure 1: the cells
def fig_cells():
    fig, axs = plt.subplots(1, 3, figsize=(13, 7.2))
    R = F.rot(-58, 14)
    sc = F.Scene(R); add_traditional(sc, s=Hf / 153, t=(0, 0, -Hf / 2)); finish(axs[0], sc)
    axs[0].set_title('Traditional gorintō (proportions: Bōyama maxima)\nBuddhist colours', fontsize=10)
    sc = F.Scene(R); add_cell(sc); finish(axs[1], sc)
    axs[1].set_title('Platonic gorintō: five solids in one sphere\nBuddhist colours', fontsize=10)
    sc = F.Scene(R); add_cell(sc, pal=DICTO); finish(axs[2], sc)
    axs[2].set_title('Platonic gorintō, comparison:\nKaleidohedra app colours', fontsize=10)
    for ax in axs: ax.set_ylim(-3.9, 3.75)
    labels = ['空 void · kha', '風 wind · ha', '火 fire · ra', '水 water · va', '地 earth · a']
    zs = [(p['bottom'] + p['top']) / 2 - Hf / 2 for p in [dict(bottom=float(q['bottom']), top=float(q['top'])) for q in parts]][::-1]
    for lab, z in zip(labels, zs):
        axs[1].text(1.65, z * math.cos(math.radians(14)), lab, fontsize=8.5, va='center', color='#333', family=['Noto Sans CJK JP', 'DejaVu Sans'])
    for ax in axs: ax.set_xlim(-2.3, 2.3)
    F.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.05, wspace=0.02)
    fig.savefig(os.path.join(OUT, 'RENDER-gorinto-cells.png'), dpi=170, facecolor='white'); plt.close(fig)


def arr(name, key='arrangements'):
    for r in named[key]:
        if r['name'] == name: return r


# ------------------------------------------------ figure 2: a network (lattice field)
def fig_network(name, title, fname, theta=0, gamma=90, s=(0, 0), parity=False, n=(3, 3), layers=(0, 1)):
    r = arr(name); t = r['t']
    c1, n1 = math.cos(math.radians(theta)), math.sin(math.radians(theta))
    c2, n2 = math.cos(math.radians(theta + gamma)), math.sin(math.radians(theta + gamma))
    fig, ax = plt.subplots(figsize=(10, 10)); sc = F.Scene(F.rot(-35, 16))
    for m1 in range(n[0]):
        for m2 in range(n[1]):
            for m3 in layers:
                p = (t * (m1 * c1 + m2 * c2), t * (m1 * n1 + m2 * n2), m1 * s[0] + m2 * s[1] + m3 * Hf)
                M = INVERT if parity and (m1 + m2) % 2 else np.eye(3)
                add_cell(sc, M=M, t=p, lw=0.9)
    finish(ax, sc)
    ax.set_title(title, fontsize=11)
    F.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.03)
    fig.savefig(os.path.join(OUT, fname), dpi=160, facecolor='white'); plt.close(fig)


# ------------------------------------------------ figure 3: ring of eight round a centre (eight-petal lotus)
def fig_ring():
    r = [x for x in named['rings'] if x['name'] == 'ring N=8 outward with centre'][0]; rr = r['r']
    fig, axs = plt.subplots(1, 2, figsize=(15, 8.2), gridspec_kw=dict(width_ratios=[1.25, 1]))
    for ax, (az, el) in zip(axs, [(-20, 36), (-90, 89.5)]):
        sc = F.Scene(F.rot(az, el)); add_cell(sc)
        for k in range(8):
            a = 2 * math.pi * k / 8
            add_cell(sc, M=rotz(a), t=(rr * math.cos(a), rr * math.sin(a), 0))
        finish(ax, sc)
    axs[0].set_title('oblique view', fontsize=10); axs[1].set_title('from above', fontsize=10)
    fig.suptitle(f'Ring of eight round a centre (eight-petal pattern): ring radius {rr:.6f} for circumradius 1', fontsize=11.5)
    F.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.89, bottom=0.03)
    fig.savefig(os.path.join(OUT, 'RENDER-gorinto-ring.png'), dpi=160, facecolor='white'); plt.close(fig)


# ------------------------------------------------ figure 4: the 3D mandala web (centre + 12)
def fig_mandala(name, fname):
    r = [x for x in named['mandala'] if x['name'] == name][0]; d = r['d']
    h = Hf / 2 if 'h=H/2' in name else Hf
    inv = 'inverted' in name
    P = [((0, 0, 0), False)]
    for sx, sy in itertools.product((1, -1), repeat=2): P.append(((sx * d, sy * d, 0), False))
    for z in (h, -h):
        for v in [(d, 0), (-d, 0), (0, d), (0, -d)]: P.append(((v[0], v[1], z), inv))
    fig, axs = plt.subplots(1, 2, figsize=(16, 10.5), gridspec_kw=dict(width_ratios=[1.15, 1]))
    sc = F.Scene(F.rot(-27, 24))
    for p, iv in P: add_cell(sc, M=INVERT if iv else np.eye(3), t=p, lw=0.9)
    finish(axs[0], sc); axs[0].set_title('oblique view', fontsize=10)
    ax = axs[1]; w = 2 / math.sqrt(3)       # plan: the earth-cube footprint of each cell, by layer
    sty = {0: dict(fc=BUD['earth'], ec=F.INK, lw=1.4, ls='-'), 1: dict(fc='none', ec=BUD['fire'], lw=2.2, ls='-'),
           -1: dict(fc='none', ec=BUD['void'], lw=2.2, ls='--')}
    for (x, y, z), iv in P:
        lay = 0 if abs(z) < 1e-9 else (1 if z > 0 else -1)
        o = 0.07 * lay
        ax.add_patch(matplotlib.patches.Rectangle((x - w / 2 + o, y - w / 2 + o), w, w, **sty[lay]))
    ax.text(0, 0, 'centre', ha='center', va='center', fontsize=9)
    ax.set_xlim(-2.9, 2.9); ax.set_ylim(-2.9, 2.9); F.blank(ax)
    from matplotlib.lines import Line2D
    ax.legend(handles=[matplotlib.patches.Patch(fc=BUD['earth'], ec=F.INK, label='middle layer: centre + four corners (Tō-ji quincunx)'),
                       Line2D([], [], color=BUD['fire'], lw=2.2, label='upper layer, +H/2: cross of four'),
                       Line2D([], [], color=BUD['void'], lw=2.2, ls='--', label='lower layer, -H/2: cross of four')],
              loc='lower center', bbox_to_anchor=(0.5, -0.02), fontsize=9, frameon=False)
    ax.set_title('plan from above (cube footprints): 1 + 4 + 4 + 4 = 13', fontsize=10)
    fig.suptitle(f'Gorintō mandala web: centre + 12 (EKP 13-node pattern), middle layer the Tō-ji quincunx\n'
                 f'upper and lower layers at ±H/2; d = {d:.6f} for circumradius 1; axes vertical', fontsize=11.5)
    F.mark(fig); fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.03, wspace=0.03)
    fig.savefig(os.path.join(OUT, fname), dpi=160, facecolor='white'); plt.close(fig)


fig_cells(); print('cells')
fig_ring(); print('ring')
fig_mandala('mandala 13 h=H/2 outer layers parallel', 'RENDER-gorinto-mandala.png'); print('mandala')
NET = os.environ.get('NET', 'body-centred (BCT), columns shifted H/2, theta 45')
r = arr(NET)
th = 45 if 'theta 45' in NET else 0
sh = (Hf / 2, Hf / 2) if 'BCT' in NET else (0, 0)
fig_network(NET, f'Gorintō network: {NET}; spacing {r["t"]:.6f}, density {r["density"]:.4f}', 'RENDER-gorinto-network.png',
            theta=th, s=sh, parity='checkerboard' in NET, layers=(0, 1) if 'BCT' not in NET else (0,))
print('network'); print('FINAL ok render')
