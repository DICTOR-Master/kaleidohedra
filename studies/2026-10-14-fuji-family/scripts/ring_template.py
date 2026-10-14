# Cutting template for the six slotted rings (DICTO, 2026-10-14): one ring, cut six. A4 PDF at full size: outer diameter 180 mm,
# band 14 mm, for sheet 2 mm thick (slot width = 1.118 x thickness + 0.3 mm clearance, depth = half the band), 10 slots every 36°,
# alternating from the outside and the inside. DICTO · dictospheres.com
import math, os, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'paper', 'figures')
D, BAND, TH = 180.0, 14.0, 2.0
RO, RI = D / 2, D / 2 - BAND; RM = (RO + RI) / 2
SW = TH / math.sin(math.radians(63.4349)) + 0.3
def arc(r, t0, t1, n=200): return [(r * math.cos(t0 + (t1 - t0) * k / n), r * math.sin(t0 + (t1 - t0) * k / n)) for k in range(n + 1)]
fig = plt.figure(figsize=(8.27, 11.69)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-105, 105); ax.set_ylim(-148.5, 148.5); ax.set_aspect('equal'); ax.axis('off')
for r, kind in ((RO, 'out'), (RI, 'in')):
    pts = []
    for k in range(10):
        c = 2 * math.pi * k / 10; half = (SW / 2) / r
        slot_here = (kind == 'out') == (k % 2 == 0)
        nxt = 2 * math.pi * (k + 1) / 10
        if slot_here:
            depth_r = RM
            pts += [(r * math.cos(c - half), r * math.sin(c - half))]
            # slot: go in to the middle radius and back out (parallel sides, width SW)
            ux, uy = math.cos(c), math.sin(c); vx, vy = -uy, ux
            pts += [(depth_r * ux - SW / 2 * vx, depth_r * uy - SW / 2 * vy), (depth_r * ux + SW / 2 * vx, depth_r * uy + SW / 2 * vy)]
            pts += arc(r, c + half, nxt - (SW / 2) / r if ((kind == 'out') == ((k + 1) % 2 == 0)) else nxt)
        else:
            pts += arc(r, c, nxt - (SW / 2) / r if ((kind == 'out') == ((k + 1) % 2 == 0)) else nxt)
    xs, ys = zip(*(pts + pts[:1])); ax.plot(xs, ys, color='black', lw=0.6)
ax.plot([0], [0], marker='+', color='#999', ms=8)
ax.text(0, 112, 'Six slotted rings: cut 6', ha='center', fontsize=14, weight='bold')
ax.text(0, 104, f'Outer diameter {D:.0f} mm, band {BAND:.0f} mm, for sheet {TH:.0f} mm thick. Slots {SW:.2f} mm wide, {BAND/2:.0f} mm deep,', ha='center', fontsize=8.5)
ax.text(0, 98, 'every 36°, alternately from the outside and the inside. Slot each ring onto the others, outside slot into inside slot;', ha='center', fontsize=8.5)
ax.text(0, 92, 'the planes cross at 63.4°, so card or thin PET sheet will flex enough to close the last rings.', ha='center', fontsize=8.5)
ax.plot([-50, 50], [-110, -110], color='black', lw=0.6); ax.text(0, -116, 'check: this line is 100 mm', ha='center', fontsize=8)
ax.text(-100, -143, 'DICTO · dictospheres.com · FUJI family study, 2026-10-14', fontsize=7.5, color='#555')
fig.savefig(os.path.join(OUT, 'six-rings-template.pdf')); fig.savefig(os.path.join(OUT, 'six-rings-template.png'), dpi=80)
print('ok', round(SW, 3))
