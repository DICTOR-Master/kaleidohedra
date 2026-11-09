"""The crossing (DICTO 10 Nov 2026: 'the crossing of the line should illustrate it'). True-scale views centred on t5's corner,
where t5's base, t5's right leg and t6's right leg meet exactly (the corner touch (5,5,6)). Left, the DICTO Yantra: t4's right
leg passes on one side of that corner and every region is a triangle. Right, Kulaichev's yantra: t4's right leg has crossed to the
other side; it cuts the tip off region A (where t4's and t6's legs would meet) and region B (whose tip was t5's corner), leaving the
pink and white triangles. Dashed: the cut-off tips. Checks the side of the corner the leg passes on, and the corner counts.
usage: python yantra_crossing.py <out.png>"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from figure import segments, faces, area, corners_of, inside_tri
from overlay import Y
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
GOLD, BLUE, PINK, INK, RED = '#e8d9a8', '#3f6fdc', '#c7158a', '#221e19', '#c1121f'
def meet(p, q, r, s):
    d = (q[0]-p[0])*(s[1]-r[1]) - (q[1]-p[1])*(s[0]-r[0]); t = ((r[0]-p[0])*(s[1]-r[1]) - (r[1]-p[1])*(s[0]-r[0])) / d
    return (p[0] + t*(q[0]-p[0]), p[1] + t*(q[1]-p[1]))
fig, axs = plt.subplots(1, 3, figsize=(20, 7.6), facecolor='#fffdf7'); ok = True
for ax, key, title, h in ((axs[0], 'GF1', 'The DICTO Yantra', 0.0042), (axs[1], 'KRP', "Kulaichev's yantra", 0.0042), (axs[2], 'KRP', "Kulaichev's yantra, closer", 0.0010)):
    b, w, a = Y[key][1]()[:3]; segs = segments(b, w, a); pts, fs = faces(segs)
    C5 = (w[5], b[5]); L = {'t4 right leg': ((w[4], b[4]), (0, a[4])), 't5 base': ((-w[5], b[5]), (w[5], b[5])),
                           't5 right leg': ((w[5], b[5]), (0, a[5])), 't6 right leg': ((w[6], b[6]), (0, a[6]))}
    p, q = L['t4 right leg']; dist = ((q[0]-p[0])*(C5[1]-p[1]) - (q[1]-p[1])*(C5[0]-p[0])) / math.hypot(q[0]-p[0], q[1]-p[1])
    close = h < 0.002
    if close:
        P1 = meet(*L['t4 right leg'], *L['t5 base']); P2 = meet(*L['t4 right leg'], *L['t5 right leg']); P3 = meet(*L['t4 right leg'], *L['t6 right leg'])
        cx0 = (min(P1[0], P2[0], P3[0], C5[0]) + max(P1[0], P2[0], P3[0], C5[0])) / 2; cy0 = (min(P1[1], P2[1], P3[1], C5[1]) + max(P1[1], P2[1], P3[1], C5[1])) / 2
        box = (cx0-h, cx0+h, cy0-h, cy0+h)
    else:
        box = (C5[0]-h, C5[0]+h, C5[1]-h, C5[1]+h)
    four = 0
    for f in fs:
        poly = [pts[i] for i in f]; ar = area(poly)
        if ar >= -1e-14: continue
        cx = sum(x for x, _ in poly)/len(poly); cy = sum(y for _, y in poly)/len(poly)
        if not any(box[0]-0.1 < x < box[1]+0.1 and box[2]-0.1 < y < box[3]+0.1 for x, y in poly): continue
        odd = sum(inside_tri((cx, cy), b, w, a, i) for i in range(1, 10)) % 2 == 1; c = corners_of(poly)
        if not odd: continue
        isf = len(c) == 4; four += isf and cx > 0 and min(math.dist(v, C5) for v in c) < 0.003
        col = BLUE if isf else PINK if -ar < 1e-6 else GOLD
        ax.add_patch(Polygon([(x, -y) for x, y in poly], fc=col, ec='none', alpha=0.85 if col != GOLD else 0.55))
    for s in segs: ax.plot([s[0][0], s[1][0]], [-s[0][1], -s[1][1]], color='#999', lw=0.4)
    for name, (u0, u1) in L.items():
        col = RED if name == 't4 right leg' else INK
        ax.plot([u0[0], u1[0]], [-u0[1], -u1[1]], color=col, lw=0.9 if col == RED else 0.7, zorder=4)
        # label at the box edge along the line
        tt = [((box[0]+0.0004)-u0[0])/(u1[0]-u0[0]) if u1[0] != u0[0] else None]
        for t in (0.0, 1.0):
            pass
        X = [u0[0] + t*(u1[0]-u0[0]) for t in [i/400 for i in range(401)]]; Yv = [u0[1] + t*(u1[1]-u0[1]) for t in [i/400 for i in range(401)]]
        ins = [(x, y) for x, y in zip(X, Yv) if box[0]+0.0003 < x < box[1]-0.0003 and box[2]+0.0003 < y < box[3]-0.0003]
        if ins:
            x, y = ins[0] if name == 't5 base' else ins[len(ins)//4] if name == 't4 right leg' else ins[-1]
            ax.text(x, -y, ' ' + name, color=col, fontsize=10, weight='bold', zorder=6, ha='left' if name != 't5 base' else 'left', va='bottom')
    ax.plot(C5[0], -C5[1], 'o', ms=4.5, mfc='white', mec=INK, mew=0.9, zorder=7)
    if not (key == 'KRP' and close): ax.annotate("t5's corner", (C5[0], -C5[1]), xytext=(8, -16), textcoords='offset points', fontsize=10, zorder=7)
    if key == 'KRP' and not close:
        ax.text(C5[0] + 0.35*h, -(C5[1] + 0.55*h), 'A', fontsize=16, weight='bold', color=INK, ha='center', zorder=8)
        ax.text(C5[0] - 0.55*h, -(C5[1] + 0.35*h), 'B', fontsize=16, weight='bold', color=INK, ha='center', zorder=8)
    if key == 'KRP' and close:
        D = '#0b2a8a'
        ax.plot([P2[0], C5[0]], [-P2[1], -C5[1]], color='#ff7a00', lw=1.6, zorder=5)
        ax.plot([P1[0], P2[0]], [-P1[1], -P2[1]], color='#ff7a00', lw=1.6, zorder=5)
        for P, lab, off in ((C5, "t5's corner", (10, 6)), (P1, '', (0, 0)), (P2, '', (0, 0)), (P3, '', (0, 0))):
            ax.plot(P[0], -P[1], 'o', ms=4.5, mfc='white', mec=INK, mew=0.9, zorder=7)
        ax.annotate("A's short fourth side\n(on t5's right leg)", ((P2[0]+C5[0])/2, -(P2[1]+C5[1])/2), xytext=(60, -95), textcoords='offset points', fontsize=10, color=D, weight='bold', arrowprops=dict(arrowstyle='->', color=D), zorder=9)
        ax.annotate("B's short fourth side\n(on t4's right leg)", ((P1[0]+P2[0])/2, -(P1[1]+P2[1])/2), xytext=(-215, -150), textcoords='offset points', fontsize=10, color=D, weight='bold', arrowprops=dict(arrowstyle='->', color=D), zorder=9)
        ax.annotate("A's cut-off tip:\nt4's and t6's legs meet here", (P3[0], -P3[1]), xytext=(-200, 30), textcoords='offset points', fontsize=10, color=D, weight='bold', arrowprops=dict(arrowstyle='->', color=D), zorder=9)
        ax.annotate("B's cut-off tip: t5's base and\nright leg meet at t5's corner", (C5[0], -C5[1]), xytext=(20, 50), textcoords='offset points', fontsize=10, color=D, weight='bold', arrowprops=dict(arrowstyle='->', color=D), zorder=9)
        ax.text(box[1] - 0.2*h, -(box[2] + 0.9*h), 'A', fontsize=22, weight='bold', color=INK, ha='center', zorder=8)
        ax.text(box[0] + 0.2*h, -(box[2] + 0.75*h), 'B', fontsize=22, weight='bold', color=INK, ha='center', zorder=8)
        ok &= dist < 0 and four == 2
    elif key == 'KRP':
        ok &= dist < 0 and four == 2
    else:
        ok &= dist > 0 and four == 0
    ax.set_xlim(box[0], box[1]); ax.set_ylim(-box[3], -box[2]); ax.set_aspect('equal'); ax.axis('off')
    side = 'passes beside t5\'s corner' if key == 'GF1' else 'has crossed over t5\'s corner'
    ax.set_title(f"{title} (×{1.0/(2*h):.0f})\nt4's right leg {side}\nby {abs(dist):.5f} of the diameter" + ('' if close else f"; four-sided regions: {four}"), fontsize=11)
fig.text(0.5, 0.03, "Fine lines; true scale, centred on t5's corner (where t5's base, t5's right leg and t6's right leg meet). Gold: triangles. Blue: four-sided regions A and B; orange: their short fourth sides. Pink: the tiny extra triangle; "
         "the white sliver beside it is an even region. Mirror image on the left.  DICTO · dictospheres.com", ha='center', fontsize=9)
plt.savefig(sys.argv[1], dpi=160, bbox_inches='tight', facecolor='#fffdf7')
print('FINAL ok' if ok else 'FINAL FAIL: side of the corner or the count is not as stated')
