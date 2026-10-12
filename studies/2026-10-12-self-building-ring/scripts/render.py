# Renders (2026-10-12): the two rings (band, hole, forced corner pieces) and any solution found by ring_search.py.
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_core as rc
from kit_exact import KIT
rc.KIT.update(KIT); PHI = rc.PHI
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT = os.path.join(rc.HERE, '../renders'); os.makedirs(OUT, exist_ok=True)
COL = {'J2': '#d9a441', 'FUJI': '#c4473d', 'AXE': '#3f8fbf', 'CLEO': '#8a5cc2', 't1': '#5aa469', 't2': '#7fb3a5', 't3': '#9ccc65',
       't4': '#b39ddb', 't5': '#4db6ac', 't6': '#64b5f6', 'T2': '#90a4ae', 'I': '#8bc34a', 'J11': '#5aa469', 'axe': '#3f8fbf', 'fuji': '#c4473d'}
def faces(V):
    E = rc.planes(V); out = []
    for e in E:
        idx = np.where(np.abs(V @ e[:3] + e[3]) < 1e-7)[0]; c = V[idx].mean(0); n = e[:3]
        a = V[idx[0]] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out.append(V[idx[np.argsort([np.arctan2((V[i] - c) @ b, (V[i] - c) @ a) for i in idx])]])
    return out
def frame(r):
    """coordinates with the ring axis vertical, floor at z=0"""
    z = r['apex'] - r['c1']; z /= np.linalg.norm(z); x = r['floor'][0] - r['floor'].mean(0); x -= (x @ z) * z; x /= np.linalg.norm(x)
    y = np.cross(z, x); o = r['floor'].mean(0); return lambda V: (np.asarray(V) - o) @ np.array([x, y, z]).T
def draw(ax, V, col, a=1.0, lw=0.5):
    ax.add_collection3d(Poly3DCollection(faces(V), facecolor=col, edgecolor='k', linewidths=lw, alpha=a))
def setup(ax, s=1.0, elev=28, azim=-60):
    ax.set_xlim(-s, s); ax.set_ylim(-s, s); ax.set_zlim(-s * .6, s * 1.4); ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.set_axis_off()
fig = plt.figure(figsize=(14, 7))
for i, nm in enumerate(('J2', 'FUJI')):
    r = rc.ring(nm); T = frame(r)
    ax = fig.add_subplot(1, 2, i + 1, projection='3d')
    tip = T(np.vstack([r['top'], r['apex'][None]]))
    draw(ax, tip, COL[nm], 0.35, 0.3)
    draw(ax, T(r['hole']), '#9e9e9e', 0.95)
    for V in faces(T(r['band'])): ax.add_collection3d(Poly3DCollection([V], facecolor='#cfe3f0', edgecolor='k', linewidths=0.6, alpha=0.25))
    setup(ax, 1.0 if nm == 'J2' else 1.2)
    ax.set_title(f'DICTO\'s rule for {nm}: φ·{nm} = tip {nm}(1) (colour) + {nm}(1/φ) point-mirrored (grey)\n+ side ring (pale blue band minus the grey hole), volume 3 × {nm}', fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'rings.png'), dpi=140); plt.close()
# the cap rule: J2(phi^2) = J11 + 5 J2 + 5 AXE + 5 FUJI
cr = os.path.join(rc.HERE, '../data/cap-rule-J2-raw.json')
if os.path.exists(cr):
    d = json.load(open(cr)); A = np.array(d['target_corners'])
    apex = A[0]; z = apex - A[1:].mean(0); z /= np.linalg.norm(z); x = A[1] - A[1:].mean(0); x -= (x @ z) * z; x /= np.linalg.norm(x); y = np.cross(z, x)
    Tc = lambda V: (np.asarray(V) - A[1:].mean(0)) @ np.array([x, y, z]).T
    fig = plt.figure(figsize=(14, 7))
    for j, ex in enumerate((0.0, 0.6)):
        ax = fig.add_subplot(1, 2, j + 1, projection='3d')
        for q in d['parts']:
            W = Tc(q['vertices']); c = W.mean(0); dd = c - np.array([0, 0, 0.6])
            draw(ax, W + ex * dd, COL.get(q['is'].split('@')[0], '#cccccc'), 0.95, 0.4)
        setup(ax, 2.2 if ex else 1.8, elev=22)
        ax.set_title(('J2(φ²) assembled' if not ex else 'exploded') + ': J11 (green) + 5 J2 (gold) + 5 AXE (blue) + 5 FUJI (red)', fontsize=10)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, 'cap-rule-J2.png'), dpi=140); plt.close()
for f in sorted(glob.glob(os.path.join(rc.HERE, '../data/ring-*-solution.json'))):
    nm = 'J2' if 'ring-J2' in f else 'FUJI'; r = rc.ring(nm); T = frame(r); sol = json.load(open(f))
    fig = plt.figure(figsize=(14, 7))
    for j, ex in enumerate((0.0, 0.35)):
        ax = fig.add_subplot(1, 2, j + 1, projection='3d'); draw(ax, T(r['hole']), '#9e9e9e', 0.9)
        for p in sol:
            W = T(np.array(p['vertices'])); c = W.mean(0); d = np.r_[c[:2], 0]
            draw(ax, W + ex * d / (np.linalg.norm(d) + 1e-9) * (1 + 2 * abs(c[2])), COL.get(p['name'].split('@')[0], '#cccccc'), 0.95, 0.3)
        setup(ax, 1.3 if ex else 1.0); ax.set_title(('assembled' if not ex else 'exploded') + f': {len(sol)} pieces', fontsize=10)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, os.path.basename(f).replace('.json', '.png')), dpi=140); plt.close()
print('renders:', sorted(os.listdir(OUT)))
