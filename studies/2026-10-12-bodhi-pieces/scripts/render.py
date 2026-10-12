# Renders for the Bodhi seed gap pieces (matplotlib, 2026-10-12): each piece type, the inner cavity (RH(1) = centre + 60 B1), and
# kits A and B assembled (cut-away) and exploded. Also a chirality check: is each piece congruent to its own mirror image?
import sys, os, json, itertools, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bodhi_core import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
D = os.path.join(HERE, '../data'); OUT = os.path.join(HERE, '../renders'); os.makedirs(OUT, exist_ok=True)
kits = {k: json.load(open(os.path.join(D, f'bodhi-kit-{k}-all-pieces.json'))) for k in 'AB'}
P = {lab: [np.array(W) for W in Ws] for k in 'AB' for lab, Ws in kits[k].items()}
COL = {'B1': '#d9a441', 'B2': '#3f8fbf', 'B3': '#c4473d', 'B4': '#5aa469', 'B5': '#8a5cc2', 'copy': '#cfd8dc', 'centre': '#9e9e9e'}

def achiral(V):
    """True if some rigid motion with det -1 maps the corner set to itself up to a permutation (i.e. the piece equals its mirror image)."""
    V = V - V.mean(0); n = len(V); Dm = np.linalg.norm(V[:, None] - V[None], axis=2)
    for perm in itertools.permutations(range(n)):
        if not np.allclose(Dm[np.ix_(perm, perm)], Dm, atol=1e-7): continue
        R, *_ = np.linalg.lstsq(V, V[list(perm)], rcond=None)
        if np.allclose(V @ R, V[list(perm)], atol=1e-7) and np.linalg.det(R) < 0: return True
    return False
for lab in ('B1', 'B2', 'B3', 'B4', 'B5'):
    V = hull_corners(P[lab][0]); ok = achiral(V) if len(V) <= 9 else 'mirror in stabiliser'
    print(f'{lab}: equals its mirror image: {ok}')
if len(hull_corners(P['B4'][0])) > 9:
    print('B4: has a mirror symmetry (its stabiliser in the group contains a mirror, logs/verify_kit_B.log)')

def faces(V):
    return [V[f] for _, f in faces_of(hull_corners(V))]
def draw(ax, polys, color, alpha=1.0, lw=0.4, ec='k'):
    pc = Poly3DCollection(polys, facecolor=color, edgecolor=ec, linewidths=lw, alpha=alpha); ax.add_collection3d(pc)
def setup(ax, r, elev=18, azim=35):
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.set_axis_off()

# 1. piece types
fig = plt.figure(figsize=(15, 3.6))
for i, lab in enumerate(['B1', 'B2', 'B3', 'B4', 'B5']):
    ax = fig.add_subplot(1, 5, i + 1, projection='3d'); V = hull_corners(P[lab][0]); c = V.mean(0); V = V - c
    draw(ax, faces(V), COL[lab], 0.85, 0.8); r = np.abs(V).max() * 1.05; setup(ax, r)
    ax.set_title(f'{lab} ×{len(P[lab])}\n{len(V)} corners, vol {vol(V):.6f}', fontsize=9)
fig.suptitle('Bodhi seed gap pieces (kit A: B1, B2, B3; kit B: B1, B4, B5); each panel scaled to fit', fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'piece-types.png'), dpi=140); plt.close()

# 2. inner cavity: RH(1) = RT(1/phi) + 60 B1
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 2, 1, projection='3d'); draw(ax, faces(CENTRE), COL['centre'], 1.0)
for W in P['B1']:
    if W.mean(0) @ np.array([0.3, -1, 0.4]) < 0: draw(ax, faces(W), COL['B1'], 0.9)
setup(ax, 2.0); ax.set_title('inner cavity cut open: centre RT(1/φ) + B1 (half shown)', fontsize=9)
ax = fig.add_subplot(1, 2, 2, projection='3d'); draw(ax, faces(CENTRE), COL['centre'], 1.0)
for W in P['B1']:
    d = W.mean(0); draw(ax, faces(W + 0.9 * d / np.linalg.norm(d)), COL['B1'], 0.95)
setup(ax, 2.9); ax.set_title('exploded: 60 B1 round the centre = rhombic hexecontahedron RH(1)', fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'inner-cavity.png'), dpi=140); plt.close()

# 3. kits assembled (cut away) and exploded
cut = np.array([0.35, -1.0, 0.25]); cut /= np.linalg.norm(cut)
for k, labs in (('A', ['B1', 'B2', 'B3']), ('B', ['B1', 'B4', 'B5'])):
    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    draw(ax, faces(CENTRE), COL['centre'])
    for C in COPIES:
        if C.mean(0) @ cut < -0.5: draw(ax, faces(C), COL['copy'], 0.35, 0.3)
    for lab in labs:
        for W in P[lab]:
            if W.mean(0) @ cut < 0: draw(ax, faces(W), COL[lab], 0.95, 0.3)
    setup(ax, 4.0); ax.set_title(f'kit {k} assembled, front half removed (copies faint)', fontsize=10)
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    draw(ax, faces(CENTRE), COL['centre'])
    for lab in labs:
        for W in P[lab]:
            d = W.mean(0); s = {'B1': 0.6, 'B2': 2.2, 'B3': 2.6, 'B4': 2.2, 'B5': 2.6}[lab]
            draw(ax, faces(W + s * d / np.linalg.norm(d)), COL[lab], 0.95, 0.25)
    setup(ax, 6.0); ax.set_title(f'kit {k} exploded (12 copies hidden): ' + ', '.join(f'{l} ×{len(P[l])}' for l in labs), fontsize=10)
    plt.tight_layout(); plt.savefig(os.path.join(OUT, f'kit-{k}.png'), dpi=140); plt.close()

# 4. the outer pocket round one 3-fold axis, both kits (three copies faint)
u3 = U20[0]; near = [C for C in COPIES if (C.mean(0) / np.linalg.norm(C.mean(0))) @ u3 > 0.75]
fig = plt.figure(figsize=(12, 6))
for i, (k, labs) in enumerate((('A', ['B2', 'B3']), ('B', ['B4', 'B5']))):
    ax = fig.add_subplot(1, 2, i + 1, projection='3d')
    for C in near: draw(ax, faces(C), COL['copy'], 0.25, 0.2)
    for lab in labs:
        for W in P[lab]:
            if (W.mean(0) / np.linalg.norm(W.mean(0))) @ u3 > 0.85: draw(ax, faces(W), COL[lab], 0.95, 0.4)
    c = 3.2 * u3; ax.set_xlim(c[0] - 2, c[0] + 2); ax.set_ylim(c[1] - 2, c[1] + 2); ax.set_zlim(c[2] - 2, c[2] + 2); ax.set_box_aspect((1, 1, 1))
    ax.view_init(*np.degrees([np.arcsin(u3[2]), np.arctan2(u3[1], u3[0])])); ax.set_axis_off()
    ax.set_title(f'kit {k}: outer pocket round one 3-fold axis (' + ', '.join(labs) + ')', fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'outer-pocket-3fold.png'), dpi=140); plt.close()
print('renders written:', sorted(os.listdir(OUT)))
