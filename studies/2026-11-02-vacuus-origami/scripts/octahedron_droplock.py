# Drop-in tabs for DICTO's four-piece octahedron Vacuus. Two plates crossing along a line can only slide along that line, so a
# step cut into a half-lap slot cannot lock it. The lock comes from the halves of C instead: each half carries two short tabs on
# its base that drop through matching tab slots in A as the half slides onto B. Then B and C are tied to A sideways, and the
# only way apart is lifting a half straight back out (up for C1; into the floor for C2 when the piece stands on three corners).
# Usage: octahedron_droplock.py <out.pdf> [edge mm] [t mm] [clearance mm]
import sys, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = sys.argv[1]; s = float(sys.argv[2]) if len(sys.argv) > 2 else 900.0
t = float(sys.argv[3]) if len(sys.argv) > 3 else 6.0; cl = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
X = 4.0                                                    # plate thickness drawn x4 so tabs and slots show
t, cl = t * X, cl * X
a = s / 2 ** .5; w = t + cl; tl = 0.08 * s                 # half-diagonal, slot width, tab length
TABS = {'C1': (0.55, -0.55), 'C2': (0.30, -0.30)}          # tab centres along the x-diagonal, as fractions of a
INK, SLOT, TAB, GUIDE = '#1d1d24', '#c0392b', '#2bb3a3', '#9aa3b5'

def rect(ax, c, u, L, W, **kw):
    u = np.array(u, float) / np.linalg.norm(u); n = np.array([-u[1], u[0]]); c = np.array(c, float)
    P = np.array([c + u * L / 2 + n * W / 2, c - u * L / 2 + n * W / 2, c - u * L / 2 - n * W / 2, c + u * L / 2 - n * W / 2])
    ax.fill(*P.T, **kw)

fig, axs = plt.subplots(1, 3, figsize=(11.7, 4.6), gridspec_kw=dict(wspace=0.08))
# A: diamond with corners on x and y; the half-lap slot along +y; four tab slots on the x-diagonal
ax = axs[0]; P = np.array([[a, 0], [0, a], [-a, 0], [0, -a], [a, 0]]); ax.fill(*P.T, color='#e9e3dc', ec=INK, lw=0.8)
ax.plot([-a, a], [0, 0], color=GUIDE, lw=0.5, ls=(0, (3, 3)))
rect(ax, (0, a / 2), (0, 1), a, w, color='white', ec=SLOT, lw=0.8)
for k, (p, q) in TABS.items():
    for f in (p, q): rect(ax, (f * a, 0), (1, 0), tl + cl, w, color='white', ec=TAB, lw=0.9)
ax.set_title('A\nhalf-lap slot (red), four tab slots (teal)', fontsize=9)
# C1 and C2: half-triangles, base on the x-diagonal, slot along z to half-way, two tabs below the base
for ax, k, sgn in ((axs[1], 'C1', 1), (axs[2], 'C2', -1)):
    T = np.array([[-a, sgn * w / 2], [a, sgn * w / 2], [0, sgn * a]]); ax.fill(*T.T, color='#e9e3dc', ec=INK, lw=0.8)
    rect(ax, (0, sgn * (w / 2 + a / 2) / 2), (0, 1), a / 2 - w / 2, w, color='white', ec=SLOT, lw=0.8)
    for f in TABS[k]:
        rect(ax, (f * a, sgn * (w / 2 - (t + w / 2) / 2)), (1, 0), tl, t + w / 2, color=TAB, ec=INK, lw=0.6)
    ax.set_title(f'{k}: half of C\nslot to half-way, two tabs; ' + ('drops down onto A' if sgn > 0 else 'rises up onto A'), fontsize=9)
for ax in axs:
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-a * 1.05, a * 1.05); ax.set_ylim(-a * 1.05, a * 1.05)
fig.suptitle(f"DICTO's octahedron Vacuus with drop-in tabs (edge {s:.0f} mm, plate {t / X:.0f} mm; plate thickness drawn x{X:.0f})",
             fontsize=10.5, weight='bold')
fig.text(0.5, 0.03, 'C1 and C2 use different tab positions so their tabs never meet inside A. Assembled, every sideways movement is blocked; '
         'a half comes out only by lifting it straight back along B.', ha='center', fontsize=8.5)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=7, color='#555')
fig.savefig(out); print('written', out)
