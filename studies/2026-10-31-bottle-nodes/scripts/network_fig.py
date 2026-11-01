# The turned node's tie network (DICTO 2026-11-01): which cap ties to which, with the clock hour at each end.
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
src = open('clocks.py').read(); src = src[:src.index('        out.append((NAMES[i], t))') + len('        out.append((NAMES[i], t))')] + '\n    return out\n'
exec(src.replace("OUT, LOGO = sys.argv[1:3]", "OUT, LOGO = 'x', 'y'"))
T = dict((n, {o: (12 if round(c) == 0 else round(c)) for c, o in t}) for n, t in ties([30, 150, 270]))
pos = {}
for i in range(6): a = np.radians(90 - 60 * i - 30); pos[f'W{i+1}'] = 1.75 * np.array([np.cos(a), np.sin(a)])
for k in range(3):
    a = np.radians(90 - 120 * k - 60); pos[f'T{k+1}'] = 0.62 * np.array([np.cos(a), np.sin(a)]); pos[f'B{k+1}'] = pos[f'T{k+1}']
COL = {'W': '#2e8b57', 'T': '#c9a227', 'B': '#3f7fc4'}
fig, axs = plt.subplots(1, 2, figsize=(14, 7.4), facecolor='white')
for ax, half, title in [(axs[0], 'T', 'Top half: waist band W1–W6 and top caps T1–T3'), (axs[1], 'B', 'Bottom half: waist band W1–W6 and bottom caps B1–B3')]:
    names = [n for n in T if n[0] in ('W', half)]
    done = set()
    for a in names:
        for b, h in T[a].items():
            if b not in names or (b, a) in done: continue
            done.add((a, b)); p, q = pos[a], pos[b]
            ax.plot(*zip(p, q), color='#555', lw=2, zorder=1)
            for x, y, hh in [(p, q, h), (q, p, T[b][a])]:
                m = x + (y - x) * 0.3; ax.text(*m, f'{hh}', ha='center', va='center', fontsize=10, fontweight='bold',
                                                  bbox=dict(boxstyle='circle,pad=0.25', fc='white', ec=COL[[k for k in names if np.allclose(pos[k], x)][0][0]], lw=1.5), zorder=3)
    for n in names:
        ax.add_patch(plt.Circle(pos[n], 0.2, color=COL[n[0]], zorder=2)); ax.text(*pos[n], n, ha='center', va='center', color='white', fontsize=12, fontweight='bold', zorder=4)
    ax.set_title(title, fontsize=13); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
fig.suptitle("Turned node (trapezo-rhombic dodecahedron): every cap's ties, with the clock hour at each end (12 = top of the node)", fontsize=13)
fig.text(0.5, 0.03, "Waist band: a closed ring at 3 and 9 o'clock, up at 12, down at 6. Top caps: a triangle at 2 and 10, down at 4 and 8. Bottom caps: a triangle at 4 and 8, up at 2 and 10.\n"
         "Each bottom cap sits directly under the top cap of the same number and holds the same waist pair (mirror through the waist). 12 caps, 24 ties.", ha='center', fontsize=10)
lg = plt.imread('dicto-logo.png'); la = fig.add_axes([0.92, 0.06, 0.06, 0.1]); la.imshow(lg); la.axis('off')
fig.savefig('trd-network.png', dpi=150); print('ok')
