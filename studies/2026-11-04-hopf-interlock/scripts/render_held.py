#!/usr/bin/env python3
"""Figures of paper #101 (Held by Shape Alone), from out/held-data.json written by held_data.py (exact geometry and LP verdicts of the study).
A small painter's renderer (perspective or orthographic camera, faces sorted by depth, Lambert shading) drawn with matplotlib.
House look: gold #d9a520 octahedra / icosahedra, violet #7b4fa8 tetrahedra / face pyramids, blue #3f7fc4 Admiral Caps, cubes and contact faces;
neighbours as see-through glass, the piece in question solid. Writes out/fig1-octet-layer.png ... out/fig4-calibration.png."""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb

HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.join(os.path.dirname(HERE), 'out')
D = json.load(open(os.path.join(OUTD, 'held-data.json')))
GOLD, VIOLET, BLUE, INK = '#d9a520', '#7b4fa8', '#3f7fc4', '#2b2620'
LIGHT = np.array([-0.35, -0.5, 0.8]); LIGHT /= np.linalg.norm(LIGHT)
plt.rcParams['font.family'] = 'DejaVu Sans'

class Cam:
    def __init__(self, target, az, el, dist, ortho=False, fov=1.0):
        a, e = math.radians(az), math.radians(el)
        self.f = -np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)])   # view direction
        self.E = np.array(target, float) - dist*self.f
        up = np.array([0, 0, 1.0]) if abs(self.f[2]) < 0.99 else np.array([0, 1.0, 0])
        self.r = np.cross(self.f, up); self.r /= np.linalg.norm(self.r); self.u = np.cross(self.r, self.f)
        self.ortho, self.fov, self.dist = ortho, fov, dist
    def proj(self, P):
        d = np.asarray(P, float) - self.E; z = d @ self.f
        x, y = d @ self.r, d @ self.u
        s = 1.0 if self.ortho else self.dist/z
        return np.c_[x*s, y*s], z

def newell(F):
    F = np.asarray(F, float); n = np.zeros(3)
    for i in range(len(F)):
        a, b = F[i], F[(i+1) % len(F)]
        n += [(a[1] - b[1])*(a[2] + b[2]), (a[2] - b[2])*(a[0] + b[0]), (a[0] - b[0])*(a[1] + b[1])]
    return n/np.linalg.norm(n)

def shade(col, n, k=1.0):
    c = np.array(to_rgb(col)); l = 0.62 + 0.38*max(0.0, float(n @ LIGHT)); return np.clip(c*l*k + (1 - k)*1.0, 0, 1)

def items_for(piece, style, col, shift=(0, 0, 0), alpha=None, facecols=None):
    """style: 'solid' | 'glass' | 'ghost' (outline only). Returns render items (poly3d, rgba face, rgba edge, lw, cull)."""
    out = []; c = np.array(piece['centre'], float) + shift
    for k, F in enumerate(piece['faces']):
        F = np.asarray(F, float) + shift; n = newell(F)
        if n @ (F.mean(0) - c) < 0: n = -n
        fc = facecols[k] if facecols and facecols[k] else col
        if style == 'solid':
            a = 1.0 if alpha is None else alpha
            out.append((F, (*shade(fc, n), a), (*to_rgb(INK), 0.9), 0.55, alpha is None, n))
        elif style == 'glass':
            a = 0.10 if alpha is None else alpha
            out.append((F, (*shade(fc, n, 0.85), a), (*to_rgb(col), 0.45), 0.35, False, n))
        elif style == 'ghost':
            out.append((F, (1, 1, 1, 0.0), (*to_rgb(col), 0.9), 0.6, False, n))
    return out

def draw(ax, cam, items, dashed_ghost=False):
    polys, fcs, ecs, lws, depth, ls = [], [], [], [], [], []
    for F, fc, ec, lw, cull, n in items:
        if cull and n @ (F.mean(0) - cam.E) > 0: continue
        P2, z = cam.proj(F)
        polys.append(P2); fcs.append(fc); ecs.append(ec); lws.append(lw); depth.append(z.mean())
        ls.append('--' if (dashed_ghost and fc[3] == 0.0) else '-')
    order = np.argsort(depth)[::-1]
    pc = PolyCollection([polys[i] for i in order], facecolors=[fcs[i] for i in order], edgecolors=[ecs[i] for i in order],
                        linewidths=[lws[i] for i in order], linestyles=[ls[i] for i in order], joinstyle='round')
    ax.add_collection(pc)
    allp = np.vstack(polys); ax.set_xlim(allp[:, 0].min() - .05, allp[:, 0].max() + .05); ax.set_ylim(allp[:, 1].min() - .05, allp[:, 1].max() + .05)
    ax.set_aspect('equal'); ax.axis('off')

def mark(fig):
    fig.text(0.992, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=7.5, color='#8a8070')

def label(ax, cam, p, text, dx=0, dy=0, col=INK, size=10):
    (x, y), = cam.proj([p])[0]
    ax.annotate(text, (x, y), (x + dx, y + dy), fontsize=size, color=col, ha='center', va='center',
                arrowprops=dict(arrowstyle='-', color=col, lw=0.7, shrinkA=2, shrinkB=2) if (dx or dy) else None)

def arrow(ax, cam, p, q, col):
    (x0, y0), = cam.proj([p])[0]; (x1, y1), = cam.proj([q])[0]
    ax.annotate('', (x1, y1), (x0, y0), arrowprops=dict(arrowstyle='-|>', color=col, lw=1.4, mutation_scale=12, shrinkA=0, shrinkB=0))

def save(fig, name):
    p = os.path.join(OUTD, name); fig.savefig(p, dpi=220, facecolor='white'); plt.close(fig); print('wrote', p)

# ---------- Figure 1: the octet (111) layer, from above and in perspective ----------
O = D['octet']; Pc = O['pieces']; H = math.sqrt(2/3)
col = lambda pc: GOLD if pc['kind'] == 'octahedron' else VIOLET
ctr = np.array([0.5, 0.29, H/2])
disc = [k for k, pc in enumerate(Pc) if np.linalg.norm(np.array(pc['centre'][:2]) - ctr[:2]) < 3.3]
fig, axs = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw=dict(width_ratios=[1, 1.25]))
cam = Cam(ctr, -90, 89.9, 50, ortho=True)
draw(axs[0], cam, [it for k in disc for it in items_for(Pc[k], 'solid', col(Pc[k]))])
cam = Cam(ctr, -62, 24, 11)
draw(axs[1], cam, [it for k in disc for it in items_for(Pc[k], 'solid', col(Pc[k]))])
axs[0].set_title('a   from above', loc='left', fontsize=10, color=INK); axs[1].set_title('b   in perspective', loc='left', fontsize=10, color=INK)
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.04, wspace=0.03); mark(fig); save(fig, 'fig1-octet-layer.png')

# ---------- Figure 2: one tetrahedron lifted out, one octahedron that cannot move ----------
oc, tt = O['oct'], O['tet']
cont = O['oct_contacts']; cn = [np.array(c['n']) for c in cont]
fcols = []
for F in Pc[oc]['faces']:
    n = newell(F); n = n if n @ (np.mean(F, 0) - Pc[oc]['centre']) > 0 else -n
    fcols.append(BLUE if any(np.allclose(n, m, atol=1e-6) for m in cn) else None)
lift = np.array([0, 0, 1.05])
items = []
for k in disc:
    if k == oc: items += items_for(Pc[k], 'solid', GOLD, alpha=0.93, facecols=fcols)
    elif k == tt: items += items_for(Pc[k], 'ghost', VIOLET) + items_for(Pc[k], 'solid', VIOLET, shift=lift)
    elif np.linalg.norm(np.array(Pc[k]['centre'][:2]) - (np.array(Pc[oc]['centre'][:2]) + Pc[tt]['centre'][:2])/2) < 2.4: items += items_for(Pc[k], 'glass', col(Pc[k]), alpha=0.05)
fig, ax = plt.subplots(figsize=(8.4, 6.0))
cam = Cam(np.array(Pc[oc]['centre']) * 0.5 + np.array(Pc[tt]['centre']) * 0.5 + [0, 0, 0.25], -62, 40, 8)
draw(ax, cam, items, dashed_ghost=True)
tc = np.array(Pc[tt]['centre'])
arrow(ax, cam, tc + [0, 0, 0.32], tc + lift - [0, 0, 0.28], VIOLET)
label(ax, cam, tc + lift + [0, 0, 0.1], 'free: lifts straight out', dx=-0.75, dy=0.55, col=VIOLET)
label(ax, cam, np.array(Pc[oc]['centre']), 'locked: its six contact faces (blue)', dx=0.9, dy=-1.1, col='#1f4f86')
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01); mark(fig); save(fig, 'fig2-free-and-locked.png')

# ---------- Figure 3: the #47 Admiral layer ----------
A = D['admiral']; Pa = A['pieces']; z0, z1 = A['zrange']
acol = {'icosahedron': GOLD, 'Admiral Cap': BLUE, 'face pyramid': VIOLET}
free = [k for k, pc in enumerate(Pa) if pc['verdict'] == 'free']
c0 = np.mean([pc['centre'] for pc in Pa], 0)
ico = min([k for k, pc in enumerate(Pa) if pc['kind'] == 'icosahedron' and pc['verdict'] == 'locked'], key=lambda k: np.linalg.norm(np.array(Pa[k]['centre'][:2]) - c0[:2]))
fig, axs = plt.subplots(1, 2, figsize=(12, 5.6))
cam = Cam(c0, -60, 38, 16)
camb = Cam(c0 + [0, 0, 0.0], -60, 14, 16)
draw(axs[0], cam, [it for pc in Pa for it in items_for(pc, 'solid', acol[pc['kind']])])
items = []
for k, pc in enumerate(Pa):
    if k in free:
        s = np.array([0, 0, 1.4 if pc['base'] == 'high' else -1.4])
        items += items_for(pc, 'ghost', VIOLET) + items_for(pc, 'solid', VIOLET, shift=s)
    elif k == ico: items += items_for(pc, 'solid', GOLD)
    else: items += items_for(pc, 'glass', acol[pc['kind']], alpha=0.08)
draw(axs[1], camb, items, dashed_ghost=True)
for k in free:
    pc = Pa[k]; s = 1.4 if pc['base'] == 'high' else -1.4; c = np.array(pc['centre'])
    arrow(axs[1], camb, c + [0, 0, 0.1*np.sign(s)], c + [0, 0, s*0.75], VIOLET)
axs[0].set_title('a   the layer: icosahedra (gold), Admiral Caps (blue), face pyramids (violet)', loc='left', fontsize=9.5, color=INK)
axs[1].set_title('b   the four free face pyramids lifted out of the two surfaces', loc='left', fontsize=9.5, color=INK)
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.03, wspace=0.04); mark(fig); save(fig, 'fig3-admiral-layer.png')

# ---------- Figure 4: calibration, Dyskin's tetrahedra (locked) and upright cubes (free) ----------
Dy = D['dyskin']['pieces']; Cu = D['cubes']['pieces']
fig, axs = plt.subplots(1, 2, figsize=(11, 5.0))
cd = min(range(len(Dy)), key=lambda k: np.linalg.norm(Dy[k]['centre'][:2]))
cam = Cam([0, 0, 0], -58, 28, 7)
draw(axs[0], cam, [it for k, pc in enumerate(Dy) for it in (items_for(pc, 'solid', VIOLET) if k == cd else items_for(pc, 'solid', '#d8cce6', alpha=0.26) if np.linalg.norm(pc['centre'][:2]) < 1.9 else [])])
cc = min(range(len(Cu)), key=lambda k: np.linalg.norm(Cu[k]['centre'][:2]))
lift = np.array([0, 0, 1.6]); items = []
for k, pc in enumerate(Cu):
    if k == cc: items += items_for(pc, 'ghost', BLUE) + items_for(pc, 'solid', BLUE, shift=lift)
    else: items += items_for(pc, 'glass', BLUE, alpha=0.10)
cam2 = Cam([0, 0, 0.4], -58, 32, 15)
draw(axs[1], cam2, items, dashed_ghost=True)
arrow(axs[1], cam2, [0, 0, 0.55], [0, 0, 1.05], BLUE)
axs[0].set_title('a   Dyskin\'s tetrahedron layer: all 21 tested pieces locked', loc='left', fontsize=9.5, color=INK)
axs[1].set_title('b   a layer of upright cubes: every cube free', loc='left', fontsize=9.5, color=INK)
fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.03, wspace=0.05); mark(fig); save(fig, 'fig4-calibration.png')
print('OK render_held.py')
