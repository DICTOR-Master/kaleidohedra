# The Golden Ladder, chapter 1 (DICTO 11-04): the three kaleidoscopes (2,3,p), p = 3, 4, 5, on the sphere, and the flat one, p = 6.
# Mirror great circles; one triangle shaded gold, its corners marked; counts 24, 48, 120 checked from the angle sum.
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, itertools, math
phi = (1 + 5 ** .5) / 2
def uniq(vs):
    out = []
    for v in vs:
        v = np.array(v, float); v /= np.linalg.norm(v)
        if not any(abs(abs(v @ w) - 1) < 1e-9 for w in out): out.append(v)
    return out
mir = {3: uniq([p for a in [(1, 1, 0), (1, -1, 0)] for p in set(itertools.permutations(a))]),
       4: uniq([p for a in [(1, 0, 0), (1, 1, 0), (1, -1, 0)] for p in set(itertools.permutations(a))]),
       5: uniq([(1, 0, 0), (0, 1, 0), (0, 0, 1)] + [np.roll((sx * phi, sy * 1, 1 / phi), k) for k in range(3) for sx in (1, -1) for sy in (1, -1)])}
assert [len(mir[p]) for p in (3, 4, 5)] == [6, 9, 15]
for p in (3, 4, 5):   # the angle sum: area of one triangle = π(1/2 + 1/3 + 1/p − 1); 4π / area triangles
    assert round(4 / (1 / 2 + 1 / 3 + 1 / p - 1)) == {3: 24, 4: 48, 5: 120}[p]
# one fundamental triangle: corners on the p-fold, 3-fold and 2-fold axes
tri = {3: [(1, 1, 1), (1, 1, -1), (1, 1, 0)],          # 3-fold, 3-fold' (the dual tetrahedron), 2-fold... use T_d triangle below
       4: [(0, 0, 1), (1, 1, 1), (0, 1, 1)],
       5: [(0, 1, phi), (1 / phi, 0, phi), (0, 0, 1)]}
tri[3] = [(1, 1, 1), (1, -1, -1), (1, 0, 0)]              # two 3-fold corners (tetrahedron and its dual) and a 2-fold, T_d triangle (2,3,3)
tri[3] = [(1, 1, 1), (1, 0, 0), (1, 1, -1)]   # the region x >= y >= |z|: mirrors x=y, y=z, y=-z
R = None
ROT = np.eye(3)
def face(c):   # turn the sphere so that direction c (tilted a little) faces the viewer
    global ROT
    c = np.array(c, float); c /= np.linalg.norm(c)
    t = np.array([0.25, 0.18, 0.95]); t /= np.linalg.norm(t)      # where c should land: slightly off centre, so the sphere reads as round
    def frame(z):
        x = np.cross([0.13, 0.91, 0.39], z); x /= np.linalg.norm(x); y = np.cross(z, x); return np.array([x, y, z])
    ROT = frame(t).T @ frame(c)
def view(v): return ROT @ v
def circle(n):
    n = n / np.linalg.norm(n); u = np.cross(n, [0.3, 0.5, 0.8]); u /= np.linalg.norm(u); w = np.cross(n, u)
    t = np.linspace(0, 2 * np.pi, 400); return np.array([np.cos(a) * u + np.sin(a) * w for a in t])
def fund(p):
    # the triangle of the group's mirrors that contains the centroid of the listed corners (exact, from the mirror arrangement)
    c = sum(np.array(v, float) / np.linalg.norm(v) for v in tri[p]); c /= np.linalg.norm(c)
    sg = [np.sign(m @ c) for m in mir[p]]
    pts = []
    for x in np.linspace(-1, 1, 260):
        for y in np.linspace(-1, 1, 260):
            q = np.array([x, y, 0.]); 
            if x * x + y * y > 1: continue
            # sample on the sphere around c: q in the tangent plane at c
            u = np.cross(c, [0.1, 0.7, 0.3]); u /= np.linalg.norm(u); w = np.cross(c, u)
            v = c + 1.6 * (x * u + y * w); v /= np.linalg.norm(v)
            if all(np.sign(m @ v) == s or abs(m @ v) < 1e-12 for m, s in zip(mir[p], sg)): pts.append(v)
    return np.array(pts)
GOLD, INK, GREY = '#c9a24a', '#2a2a2a', '#9a9a9a'
fig, axs = plt.subplots(1, 4, figsize=(12, 3.6), dpi=200)
names = {3: ('p = 3', 'tetrahedron\n24 triangles · 2cos 60° = 1'), 4: ('p = 4', 'cube · octahedron\n48 triangles · 2cos 45° = √2'),
         5: ('p = 5', 'dodecahedron · icosahedron\n120 triangles · 2cos 36° = φ')}
for ax, p in zip(axs, (3, 4, 5)):
    ax.add_patch(plt.Circle((0, 0), 1, fc='#fbf7ee', ec=INK, lw=0.8))
    face(sum(np.array(v, float) / np.linalg.norm(v) for v in tri[p]))
    F = fund(p); W = np.array([view(v) for v in F]); W = W[W[:, 2] > 0]
    ax.scatter(W[:, 0], W[:, 1], s=2.2, c=GOLD, lw=0)
    for n in mir[p]:
        C = np.array([view(v) for v in circle(n)])
        front = C[:, 2] >= 0
        for seg_mask, st in ((front, '-'), (~front, ':')):
            pts = np.where(seg_mask, 1, np.nan)
            ax.plot(C[:, 0] * pts, C[:, 1] * pts, st, color=INK if st == '-' else GREY, lw=0.7 if st == '-' else 0.4)
    for v, lab in zip(tri[p], ('p', '3', '2') if p != 3 else ('3', '2', "3'")):
        w = view(np.array(v, float) / np.linalg.norm(v))
        if w[2] > 0: ax.plot(w[0], w[1], 'o', ms=3, color='#7a1f1f')
    ax.set_title(names[p][0], fontsize=11, fontweight='bold'); ax.text(0, -1.32, names[p][1], ha='center', va='top', fontsize=8.5)
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.75, 1.15); ax.set_aspect('equal'); ax.axis('off')
# p = 6: the flat kaleidoscope (30°-60°-90° triangles of the triangular lattice)
ax = axs[3]; s3 = 3 ** .5
for k in range(-6, 7):
    for ang in (0, 60, 120):
        a = math.radians(ang); d = np.array([math.cos(a), math.sin(a)]); nrm = np.array([-d[1], d[0]])
        for off in (k * s3 / 2,):
            P0 = nrm * off; ax.plot(*np.array([P0 - 3 * d, P0 + 3 * d]).T, color=INK, lw=0.7)
        a2 = math.radians(ang + 30); d2 = np.array([math.cos(a2), math.sin(a2)]); n2 = np.array([-d2[1], d2[0]])
        P0 = n2 * k * 0.5; ax.plot(*np.array([P0 - 3 * d2, P0 + 3 * d2]).T, color=GREY, lw=0.45)
ax.add_patch(plt.Polygon([(0, 0), (0.5, 0), (0.5, 0.5 / s3)], fc=GOLD, ec='none'))
for (x, y) in [(i + j / 2, j * s3 / 2) for i in range(-3, 4) for j in range(-3, 4)]:
    ax.add_patch(plt.Circle((x, y), 0.5, fc='none', ec='#7a9ab8', lw=0.5))
from matplotlib.patches import Rectangle
clip = Rectangle((-1.1, -1.05), 2.2, 2.15, transform=ax.transData)
for art in ax.lines + ax.patches: art.set_clip_path(clip)
ax.add_patch(Rectangle((-1.1, -1.05), 2.2, 2.15, fc='none', ec=INK, lw=0.8))
ax.set_title('p = 6', fontsize=11, fontweight='bold'); ax.text(0, -1.32, 'flat: the close-packed layer\nangles add to exactly 180°', ha='center', va='top', fontsize=8.5)
ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.75, 1.15); ax.set_aspect('equal'); ax.axis('off')
fig.text(0.985, 0.03, 'DICTO', ha='right', fontsize=7, color=GOLD, fontweight='bold')
plt.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.02, wspace=0.05)
plt.savefig('fig1-kaleidoscopes.png'); print('fig1 ok')
