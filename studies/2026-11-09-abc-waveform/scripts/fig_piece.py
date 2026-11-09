"""Figure: Narcissus with DICTO's ABC wave (crest planes of one design drawn as crest lines on the faces), top view of the
hexagon with the seat points A, B, C, and (optional) a decorated stack from a SAT model. Runs on dicto-big-brother.
Usage: fig_piece.py design_json_index out.png  (design taken from data/figure-design.json written by forced.py)"""
import sys, os, json, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave_lib as W
from n_slabs import coset
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
deco = [(np.array(n), d, c) for n, d, c in spec['planes']]
COL = ['#b07800', '#1f5fc8']          # crest colours: wave 1 dark gold, wave 2 blue
def face_poly(P, idx, n):
    V = P[sorted(idx)]; c = V.mean(0); u = V[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    return V[np.argsort(np.arctan2((V - c) @ w, (V - c) @ u))]
def crest_segments(P, faces, deco, R=np.eye(3), t=np.zeros(3)):
    segs = []
    for n0, d0, col in deco:
        n = R @ n0; d = d0 + n @ t
        for fn, fo, idx in faces:
            V = face_poly(P, idx, fn); s = V @ n - d
            if s.min() > -1e-7 or s.max() < 1e-7: continue
            pts = []
            for i in range(len(V)):
                a, b, sa, sb = V[i], V[(i + 1) % len(V)], s[i], s[(i + 1) % len(V)]
                if (sa < 0) != (sb < 0) and abs(sa - sb) > 1e-12: pts.append(a + sa / (sa - sb) * (b - a))
            if len(pts) >= 2: segs.append((pts[0], pts[1], col))
    return segs
fig = plt.figure(figsize=(13, 6.2))
# panel 1: the decorated piece
ax = fig.add_subplot(1, 3, 1, projection='3d'); P = W.P0
polys = [face_poly(P, idx, n) for n, o, idx in W.BF]
fc = ['#e8e1f5' if len(p) == 6 else '#dcebdc' if len(p) == 4 else '#f3e6d6' for p in polys]
ax.add_collection3d(Poly3DCollection(polys, facecolors=fc, edgecolors='#555', linewidths=.8, alpha=.55))
for a, b, c in crest_segments(P, W.BF, deco): ax.plot(*np.c_[a, b], color=COL[c], lw=3)
ax.set_title('Narcissus with the crest lines\n(gold/blue = the two waves)', fontsize=10)
ax.view_init(22, -60); ax.set_box_aspect((1, 1, .9)); ax.set_axis_off()
# panel 2: top view, hexagon with seats
ax2 = fig.add_subplot(1, 3, 2)
hexv = P[:6, :2]; ax2.fill(*np.r_[hexv, hexv[:1]].T, color='#e8e1f5', ec='#555')
for a, b, c in crest_segments(P, [f for f in W.BF if len(f[2]) == 6], deco): ax2.plot([a[0], b[0]], [a[1], b[1]], color=COL[c], lw=3)
ax2.plot(0, 0, 'ko'); ax2.text(.03, .03, 'A (own seat)', fontsize=9)
for i, v in enumerate(hexv):
    lab = 'B' if coset(v) == 'B' else 'C'
    ax2.plot(*v, 'o', color='#333' if lab == 'B' else '#999'); ax2.text(v[0] * 1.12, v[1] * 1.12, lab, ha='center', va='center')
ax2.set_aspect('equal'); ax2.set_axis_off(); ax2.set_title('top face (hexagon): crests and seats', fontsize=10, pad=22)
# panel 3: stack (if a model is given)
ax3 = fig.add_subplot(1, 3, 3, projection='3d')
if spec.get('stack'):
    st = spec['stack']; S = W.Structure(st['word'], st['n']); model = st['model']
    keep = [i for i, Q in enumerate(S.Ps) if np.linalg.norm(Q[:, :2].mean(0)) < st.get('radius', 1.3)]
    for i in keep:
        Q = S.Ps[i]; R, t, det, inv = S.pl[i][model[i]]
        ax3.add_collection3d(Poly3DCollection([face_poly(Q, idx, n) for n, o, idx in S.wf[i]], facecolors='#e9e4f2', edgecolors='#888', linewidths=.3, alpha=.18))
        for a, b, c in crest_segments(W.P0, W.BF, deco):
            ax3.plot(*np.c_[R @ a + t, R @ b + t], color=COL[c], lw=1.6)
    ax3.set_title(f"stack {st['word']} (S = straight, T = turned)", fontsize=10)
    allp = np.vstack([S.Ps[i] for i in keep]); ax3.set_xlim(allp[:,0].min(), allp[:,0].max()); ax3.set_ylim(allp[:,1].min(), allp[:,1].max()); ax3.set_zlim(allp[:,2].min(), allp[:,2].max())
    ax3.set_box_aspect(np.ptp(allp, axis=0)); ax3.view_init(12, -75); ax3.set_axis_off()
else: ax3.set_axis_off()
fig.text(.99, .01, 'DICTO', ha='right', va='bottom', fontsize=12, fontweight='bold', color='#6a4c9c')
fig.suptitle(spec.get('title', 'ABC waveform on Narcissus'), fontsize=12)
plt.tight_layout(); plt.savefig(out, dpi=150)
print('FINAL ok' if os.path.getsize(out) > 10000 else 'FINAL FAIL: empty figure')
