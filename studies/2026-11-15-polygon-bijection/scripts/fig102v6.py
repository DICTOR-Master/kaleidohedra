"""Paper #102 v6, Figure 4: the half-turn twist of Theorem A on one polygon (study 2026-11-15-polygon-bijection).
Usage: python3 fig102v6.py OUT.png [L]
Builds diamond (3C) near the lower atom v of bilayer 0, enumerates the polygons of length L (default 10) through v that cross the
vertical bonds of bilayer 0 exactly twice, picks the one whose far arc moves most under the twist, and draws it before and after.
Checks first (exit 1 on failure): for EVERY such polygon the image under the half-turn about the midpoint of the two crossing
points is a polygon of the same length through v in the network with bilayer 0 flipped (c -> h), the map is one-to-one, and the
number of these polygons is the same in both networks (Theorem A, Corollary A on this window).
Integer plane coordinates as in halves.py: the point (x, y) is (x a1 + y a2)/3, letter of (x, y) = x mod 3 with x = y mod 3.
"""
import sys, math, itertools
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Poly, FancyArrowPatch
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
GOLD, VIOL, RED, GREY, FAINT = '#b8962e', '#7b4fa0', '#c0392b', '#8a8070', '#cfc8bc'
OUT = sys.argv[1]; L = int(sys.argv[2]) if len(sys.argv) > 2 else 10
D1 = ((1, 1), (-2, 1), (1, -2)); D2 = ((-1, -1), (2, -1), (-1, 2))
KMIN, KMAX = -4, 4
S3C = {k: k % 3 for k in range(KMIN - 1, KMAX + 2)}
def flipped(s, K):
    a = s[K]; o = [x for x in (0, 1, 2) if x != a]; sw = {a: a, o[0]: o[1], o[1]: o[0]}
    return {k: (sw[v] if k > K else v) for k, v in s.items()}
S2 = flipped(S3C, 0)
def nbrs(s, a):
    k, x, y, u = a
    if u == 0:
        res = [(k, x, y, 1)]
        if k - 1 >= KMIN:
            dd = D1 if (s[k] - s[k - 1]) % 3 == 1 else D2   # from the upper atom of k-1 to here
            res += [(k - 1, x - dx, y - dy, 1) for dx, dy in dd]
    else:
        res = [(k, x, y, 0)]
        if k + 1 <= KMAX:
            dd = D1 if (s[k + 1] - s[k]) % 3 == 1 else D2
            res += [(k + 1, x + dx, y + dy, 0) for dx, dy in dd]
    return res
V = (0, 0, 0, 0)
def polygons(s, L):
    out = set(); path = [V]; on = {V}
    def rec(a):
        if len(path) - 1 > L: return
        for b in nbrs(s, a):
            if b == V and len(path) == L: out.add(tuple(path)); continue
            if b in on or len(path) >= L: continue
            on.add(b); path.append(b); rec(b); path.pop(); on.discard(b)
    rec(V)
    canon = set()
    for p in out:
        r = (p[0],) + tuple(reversed(p[1:])); canon.add(min(p, r))
    return sorted(canon)
far = lambda a: a[0] > 0 or (a[0] == 0 and a[3] == 1)
def edges(p): return [(p[i], p[(i + 1) % len(p)]) for i in range(len(p))]
def crossings(p):
    return sorted({(a[1], a[2]) for a, b in edges(p) if a[0] == b[0] == 0 and a[3] != b[3]})
def twist(p, P):
    """the surgery on the edge set: root edges kept, far edges turned, the vertical bonds at P kept; returns the cycle from V."""
    (px, py), (qx, qy) = P
    g = lambda a: (a[0], px + qx - a[1], py + qy - a[2], a[3]) if far(a) else a
    E = [(g(a), g(b)) if far(a) and far(b) else (a, b) for a, b in edges(p)]
    adj = {}
    for a, b in E: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    if any(len(v) != 2 for v in adj.values()): return tuple(adj)   # not 2-regular: is_polygon will reject it
    cyc = [V, adj[V][0]]
    while len(cyc) < len(E):
        nx = [c for c in adj[cyc[-1]] if c != cyc[-2]][0]
        if nx == V: break
        cyc.append(nx)
    return tuple(cyc)
def is_polygon(s, p):
    return len(set(p)) == len(p) and all(b in nbrs(s, a) for a, b in edges(p))
def canon(p):
    i = p.index(V); q = p[i:] + p[:i]; r = (q[0],) + tuple(reversed(q[1:])); return min(q, r)
ok = True
P1, P2 = polygons(S3C, L), polygons(S2, L)
two1 = [p for p in P1 if len(crossings(p)) == 2]; two2 = {p for p in P2 if len(crossings(p)) == 2}
imgs = []
for p in two1:
    q = twist(p, crossings(p))
    if not is_polygon(S2, q) or crossings(q) != crossings(p): ok = False; print('BAD image', p)
    imgs.append(canon(q))
if len(set(imgs)) != len(imgs) or set(imgs) != two2: ok = False
print(f'L={L}: polygons through v 3C {len(P1)} flipped {len(P2)}; crossing bilayer 0 twice: {len(two1)} and {len(two2)}; '
      f'images valid, distinct and onto: {ok}')
if not ok: print('FINAL FAIL'); sys.exit(1)
# choose: far arc and root arc of at least 3 bonds each, and the largest in-plane move of the far atoms
def pos(a):
    k, x, y, u = a; b = 0.6124
    return ((x + 0.5 * y) / 3, (math.sqrt(3) / 2 * y) / 3, k * 4 * b / 3 + u * b)
def score(p):
    q = twist(p, crossings(p)); nf = sum(far(a) for a in p)
    if nf < 4 or len(p) - nf < 4: return (-1, 0)
    moved = len(set(p) - set(q))
    return moved, -sum(abs(a[0]) for a in p)
C = max(two1, key=score); Pc = crossings(C); C2 = twist(C, Pc)
print('chosen', C, 'crossings', Pc)
# projection: turn the plane by AZ, look from ELEV above the horizon
AZ, ELEV = math.radians(-28), math.radians(24)
def proj(a):
    X, Y, Z = pos(a); xr = X * math.cos(AZ) - Y * math.sin(AZ); yr = X * math.sin(AZ) + Y * math.cos(AZ)
    return xr, yr * math.sin(ELEV) + Z * math.cos(ELEV)
cx = sum(pos(a)[0] for a in C) / len(C); cy = sum(pos(a)[1] for a in C) / len(C)
ks = [a[0] for a in C + C2]; k0, k1 = min(ks), max(ks)
def background(s):
    atoms = [(k, x, y, u) for k in range(k0, k1 + 1) for u in (0, 1) for x in range(-15, 16) for y in range(-15, 16)
             if (x - s[k]) % 3 == 0 and (y - s[k]) % 3 == 0 and math.dist(pos((k, x, y, u))[:2], (cx, cy)) < 1.2]
    A = set(atoms); return [(a, b) for a in atoms for b in nbrs(s, a) if b in A and a < b]
fig, axs = plt.subplots(1, 2, figsize=(7.2, 4.1))
mx, my = (Pc[0][0] + Pc[1][0]) / 2, (Pc[0][1] + Pc[1][1]) / 2
for ax, s, p, title in ((axs[0], S3C, C, '(a) In diamond: the polygon crosses the cut twice'),
                        (axs[1], S2, C2, '(b) After the half-turn: bilayer 0 is now h')):
    for a, b in background(s):
        (x1, y1), (x2, y2) = proj(a), proj(b); ax.plot([x1, x2], [y1, y2], color=FAINT, lw=0.7, zorder=1, solid_capstyle='round')
    # the cut: a horizontal plane halfway up the vertical bonds of bilayer 0
    zc = 0.6124 / 2; R = 1.25
    corners = []
    for t in range(0, 360, 10):
        X, Y = cx + R * math.cos(math.radians(t)), cy + R * math.sin(math.radians(t))
        xr = X * math.cos(AZ) - Y * math.sin(AZ); yr = X * math.sin(AZ) + Y * math.cos(AZ)
        corners.append((xr, yr * math.sin(ELEV) + zc * math.cos(ELEV)))
    ax.add_patch(Poly(corners, closed=True, facecolor=GOLD, alpha=0.10, edgecolor=GOLD, lw=0.8, zorder=2))
    for a, b in edges(p):
        (x1, y1), (x2, y2) = proj(a), proj(b)
        cross = a[0] == b[0] == 0 and a[3] != b[3]
        col = RED if cross else (VIOL if far(a) and far(b) else GOLD)
        ax.plot([x1, x2], [y1, y2], color=col, lw=3.2 if cross else 2.2, zorder=4, solid_capstyle='round')
    for a in p:
        x, y = proj(a); ax.scatter([x], [y], s=11, color='#333333', zorder=5)
    x, y = proj(V); ax.scatter([x], [y], s=70, facecolor='none', edgecolor='#222222', lw=1.4, zorder=6)
    ax.annotate('site v', (x, y), xytext=(9, -13), textcoords='offset points', fontsize=7.5)
    # the axis of the half-turn: vertical line through the midpoint of the two crossing points
    zlo, zhi = 0.0, max(pos(a)[2] for a in C + C2) + 0.25
    A0 = proj((0, mx, my, 0)); xa = A0[0]
    def pz(z):
        X, Y = (mx + 0.5 * my) / 3, (math.sqrt(3) / 2 * my) / 3
        xr = X * math.cos(AZ) - Y * math.sin(AZ); yr = X * math.sin(AZ) + Y * math.cos(AZ)
        return xr, yr * math.sin(ELEV) + z * math.cos(ELEV)
    (xa1, ya1), (xa2, ya2) = pz(zlo), pz(zhi)
    ax.plot([xa1, xa2], [ya1, ya2], color='#444444', lw=1.0, ls=(0, (4, 3)), zorder=3)
    ax.add_patch(FancyArrowPatch((xa2 - 0.22, ya2 - 0.02), (xa2 + 0.22, ya2 - 0.02), connectionstyle='arc3,rad=0.9',
                                 arrowstyle='-|>', mutation_scale=9, color='#444444', lw=1.0, zorder=3))
    ax.text(xa2 + 0.27, ya2 + 0.02, 'half-turn', fontsize=7.2, color='#444444', va='bottom')
    ax.set_aspect('equal'); ax.axis('off')
lo = [min(ax.get_xlim()[0] for ax in axs), min(ax.get_ylim()[0] for ax in axs)]
hi = [max(ax.get_xlim()[1] for ax in axs), max(ax.get_ylim()[1] for ax in axs)]
for ax in axs: ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1])
h = [plt.Line2D([], [], color=GOLD, lw=2.2), plt.Line2D([], [], color=VIOL, lw=2.2), plt.Line2D([], [], color=RED, lw=3.2),
     Poly([(0, 0)], facecolor=GOLD, alpha=0.2, edgecolor=GOLD)]
fig.legend(h, ['root arc (unchanged)', 'far arc (turned)', 'the two crossing bonds', 'the cut'], loc='lower center', ncol=4,
           fontsize=7.4, frameon=False, bbox_to_anchor=(0.5, 0.045))
fig.tight_layout(rect=(0, 0.11, 1, 0.92))
fig.text(0.01, 0.975, '(a) In diamond: the polygon crosses the cut twice', fontsize=8.6, va='top')
fig.text(0.51, 0.975, '(b) After the half-turn: bilayer 0 is now h', fontsize=8.6, va='top')
fig.text(0.992, 0.008, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=7.5, color=GREY)
fig.savefig(OUT, dpi=300); print('wrote', OUT); print('FINAL ok')
