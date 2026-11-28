# #125 Figure 2: Lemma 19 on one crossing set of diamond's far half. With Claude (Anthropic).
# (a) S = {a, b, e, f}, paired a b | e f: the 4-edge arc from a to b passes through the crossing atom of e, so it meets
# the 2-edge arc from e to f (a meeting pair: not a linkage). (b) The half-turn gS: the arcs between the same pairs exist
# (single arcs are half-turn symmetric) but no pair meets. The far asymmetry of S at this pairing is 0 - 1 = -1.
import json, math, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
SV = [(1,1),(-2,1),(1,-2),(-1,-1),(2,-1),(-1,2)]
u1, u2 = (0.0, 1.0), (-math.sqrt(3)/2, -0.5)
e1 = ((u1[0]-u2[0])/3, (u1[1]-u2[1])/3); e2 = ((2*u1[0]+u2[0])/3, (2*u1[1]+u2[1])/3)
def xy(p): return (p[0]*e1[0] + p[1]*e2[0], p[0]*e1[1] + p[1]*e2[1])
letters = [0, 1, 2]
def site(p, s): return p[0] % 3 == s % 3 and p[1] % 3 == s % 3
def nbrs(a):
    j, p, u = a; out = [(j, p, 1-u)] + [(j+1, (p[0]+d[0], p[1]+d[1]), 0) for d in SV] + [(j-1, (p[0]-d[0], p[1]-d[1]), 1) for d in SV]
    res = []
    for b in out:
        if not (0 <= b[0] < 3 and 0 <= a[0] < 3): continue
        if not (site(a[1], letters[a[0]]) and site(b[1], letters[b[0]])): continue
        jb, pb, ub = b
        if jb == j and pb == p and ub != u: res.append(b)
        elif jb == j+1 and u == 1 and ub == 0 and (pb[0]-p[0], pb[1]-p[1]) in SV: res.append(b)
        elif j == jb+1 and ub == 1 and u == 0 and (p[0]-pb[0], p[1]-pb[1]) in SV: res.append(b)
    return res
far = lambda a: a[0] > 0 or (a[0] == 0 and a[2] == 1)
def arcs(p, q, n):
    out = []
    def rec(path):
        if len(path) - 1 == n:
            if path[-1] == (0, q, 1): out.append(list(path))
            return
        for b in nbrs(path[-1]):
            if far(b) and b not in path: path.append(b); rec(path); path.pop()
    rec([(0, p, 1)]); return out
a, b, e, f = (-6, -3), (-3, -6), (-3, -3), (-3, 0)
g = lambda p: (-p[0], -p[1])
GOLD, VIOLET, RED, GREY = '#b8922e', '#7b4ea3', '#c0392b', '#cbbfae'
def panel(ax, P, title, find_meet):
    pa, pb, pe, pf = P
    # the honeycomb of the two sublayers next to the cut
    for x in range(-12, 13):
        for y in range(-12, 13):
            if site((x, y), 0):
                for d in SV[:3]:
                    q = (x + d[0], y + d[1])
                    X0, Y0 = xy((x, y)); X1, Y1 = xy(q)
                    ax.plot([X0, X1], [Y0, Y1], color=GREY, lw=0.8, zorder=1)
    L, S2 = [], []
    lens = []
    for i in (4, 2):
        for A in arcs(pa, pb, i):
            for B in arcs(pe, pf, 6 - i):
                if bool(set(A) & set(B)) == find_meet:
                    L, S2 = A, B
                    break
            if L: break
        if L: break
    for path in (L, S2):
        col, lw = (VIOLET if len(path) - 1 == 4 else GOLD), 3.2
        pts = [xy(t[1]) for t in path]
        lens.append(len(path) - 1)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, lw=lw, zorder=3, solid_capstyle='round')
    for name, p in zip('abef', P):
        X, Y = xy(p)
        ax.scatter([X], [Y], s=70, color=RED, zorder=5, edgecolor='black', linewidth=0.6)
        ax.annotate(name if title.startswith('(a)') else 'g' + name, (X, Y), xytext=(6, 6), textcoords='offset points', fontsize=11)
    shared = set(L) & set(S2)
    for t in shared:
        X, Y = xy(t[1])
        ax.scatter([X], [Y], s=260, facecolor='none', edgecolor='black', linewidth=1.4, zorder=6)
    ax.set_title(title, fontsize=11, loc='left')
    allpts = [xy(t[1]) for t in L + S2]
    x0, x1 = min(p[0] for p in allpts), max(p[0] for p in allpts)
    y0, y1 = min(p[1] for p in allpts), max(p[1] for p in allpts)
    cx, cy, h = (x0 + x1) / 2, (y0 + y1) / 2, max(y1 - y0, (x1 - x0) / 1.25) / 2 + 0.7
    ax.set_xlim(cx - 1.25 * h, cx + 1.25 * h); ax.set_ylim(cy - h, cy + h)
    ax.set_aspect('equal'); ax.axis('off')
    return len(shared), lens
fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.6))
(n1, l1) = panel(axs[0], (a, b, e, f), '(a) S, paired a b | e f: the two arcs meet', True)
(n2, l2) = panel(axs[1], (g(a), g(b), g(e), g(f)), '(b) the half-turn gS: the arcs do not meet', False)
from matplotlib.lines import Line2D
fig.legend([Line2D([0], [0], color=VIOLET, lw=3), Line2D([0], [0], color=GOLD, lw=3),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=RED, markeredgecolor='black', markersize=8),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='none', markeredgecolor='black', markersize=12)],
           ['arc of 4 bonds', 'arc of 2 bonds', 'crossing points', 'the shared atom'], loc='lower center', ncol=4, frameon=False, fontsize=10)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=8, color='#7a705f')
plt.subplots_adjust(bottom=0.14, top=0.92, left=0.02, right=0.98, wspace=0.05)
out = sys.argv[1] if len(sys.argv) > 1 else 'fig2-meeting.png'
fig.savefig(out, dpi=200)
print('shared atoms', n1, n2, 'lengths (a b, e f)', l1, l2)
ok = n1 >= 1 and n2 == 0 and l1 == [4, 2] and l2 == [4, 2]
print('FINAL ok' if ok else 'FINAL FAIL (panel content does not match the caption)')
