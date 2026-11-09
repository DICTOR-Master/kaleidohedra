"""Close-up of Kulaichev's yantra (DICTO 10 Nov 2026: 'draw the close-up' of the 41 triangles): which of the 45 odd pieces are
not triangles, and where the two tiny extra pieces lie. Uses figure.py's face arrangement on the stored 60-digit values.
usage: python3 kulaichev_closeup.py <out.png>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from figure import segments, faces, area, corners_of, inside_tri
from overlay import kulaichev
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle
b, w, a = kulaichev(); segs = segments(b, w, a); pts, fs = faces(segs)
odd = []
for f in fs:
    poly = [pts[k] for k in f]; ar = area(poly)
    if ar >= -1e-14: continue
    cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
    cnt = sum(inside_tri((cx, cy), b, w, a, i) for i in range(1, 10))
    if cnt % 2: odd.append(dict(poly=poly, n=len(corners_of(poly)), depth=cnt, A=-ar, c=(cx, cy)))
non = [o for o in odd if o['n'] != 3]; tiny = sorted(odd, key=lambda o: o['A'])[:2]
print(f"odd pieces {len(odd)}, triangles {sum(o['n']==3 for o in odd)}; non-triangles: " +
      ', '.join(f"{o['n']} corners, ring depth {o['depth']}, area {o['A']:.2e}, centre ({o['c'][0]:+.4f}, {o['c'][1]:.4f})" for o in non))
print('two smallest: ' + ', '.join(f"{o['n']} corners, area {o['A']:.2e}, centre ({o['c'][0]:+.4f}, {o['c'][1]:.4f})" for o in tiny))
# zoom box round the right-hand tiny piece and its neighbours
t = max(tiny, key=lambda o: o['c'][0]); cx, cy = t['c']
GOLD, MAG, BLUE, INK = '#e8d9a8', '#c7158a', '#1d4ed8', '#221e19'
fig, axs = plt.subplots(1, 3, figsize=(15, 5.6), facecolor='#fffdf7')
def draw(ax, box, lw):
    for o in odd:
        col = MAG if o in tiny else (BLUE if o['n'] != 3 else GOLD)
        ax.add_patch(Polygon([(p[0], -p[1]) for p in o['poly']], fc=col, ec='none', alpha=0.85 if col != GOLD else 0.55))
    for s in segs: ax.plot([s[0][0], s[1][0]], [-s[0][1], -s[1][1]], color=INK, lw=lw)
    ax.add_patch(Circle((0, -0.5), 0.5, fill=False, ec=INK, lw=lw))
    ax.set_xlim(box[0], box[1]); ax.set_ylim(-box[3], -box[2]); ax.set_aspect('equal'); ax.axis('off')
non_r = [o for o in non if o['c'][0] > 0] or non
xs = [p[0] for o in non_r + [t] for p in o['poly']]; ys = [p[1] for o in non_r + [t] for p in o['poly']]
m1 = 0.15 * max(max(xs) - min(xs), max(ys) - min(ys)); B1 = (min(xs) - m1, max(xs) + m1, min(ys) - m1, max(ys) + m1)
r2 = 4 * math.sqrt(t['A']); B2 = (cx - r2, cx + r2, cy - r2, cy + r2)
draw(axs[0], (-0.52, 0.52, -0.02, 1.02), 0.6)
for ax, B, c in ((axs[0], B1, '#c1121f'), (axs[1], B2, '#c1121f')):
    ax.add_patch(Rectangle((B[0], -B[3]), B[1] - B[0], B[3] - B[2], fill=False, ec=c, lw=1.4))
draw(axs[1], B1, 0.8); draw(axs[2], B2, 0.8)
axs[0].set_title("Kulaichev's yantra: 45 odd pieces", fontsize=12)
axs[1].set_title(f"Magnified ×{1.04/(B1[1]-B1[0]):.0f}: the {len(non_r)} four-sided pieces on this side (blue)", fontsize=11)
axs[2].set_title(f"Magnified ×{1.04/(B2[1]-B2[0]):.0f}: the tiny extra triangle (magenta)", fontsize=11)
fig.text(0.5, 0.02, f"Gold: the 41 triangles. Blue: the {len(non)} pieces that are not triangles. Magenta: the two tiny extra pieces "
         f"(area {tiny[0]['A']:.1e} of a circle of diameter 1). Mirror image on the left side.  DICTO · dictospheres.com",
         ha='center', fontsize=10)
plt.savefig(sys.argv[1], dpi=150, bbox_inches='tight', facecolor='#fffdf7')
ok = len(odd) == 45 and sum(o['n'] == 3 for o in odd) == 41
print('FINAL ok' if ok else 'FINAL FAIL: counts differ from the certified 45 / 41')
