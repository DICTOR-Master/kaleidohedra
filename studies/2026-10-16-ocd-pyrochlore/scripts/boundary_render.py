# Step 23 render: the boundary vacancies of the exact five-fold chorus (float readout of exactly verified sites).
import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = json.load(open('data/chorus-exact-r10.json')); A = np.array(D['all']); S = np.array(D['silenced']); K = np.array(D['sites'])
a5, e1, e2, th0, R = (np.array(D[k]) for k in ('a5', 'e1', 'e2')), None, None, D['th0'], D['RAD']
a5, e1, e2 = (np.array(D[k]) for k in ('a5', 'e1', 'e2'))
def cyl(X):
    z = X @ a5; x = X @ e1; y = X @ e2; th = np.arctan2(y, x); rho = np.hypot(x, y)
    k = np.round(((th - th0) % (2 * np.pi)) / (2 * np.pi / 5)) % 5; dth = ((th - th0 - k * 2 * np.pi / 5 + np.pi) % (2 * np.pi)) - np.pi
    return x, y, z, rho * np.cos(dth), rho * np.sin(dth), k
bg, fg, mute = '#f4f1ea', '#2b2620', '#6d6556'; cols = ['#e07a2e', '#3b8ea5', '#7a5aa6', '#4f9a4a', '#c0455a']
fig, ax = plt.subplots(1, 3, figsize=(18, 6.4), facecolor=bg)
for a in ax: a.set_facecolor(bg); [s.set_color(mute) for s in a.spines.values()]; a.tick_params(colors=mute)
# 1: down the axis, a slab |z| < 1.2
x, y, z, u, off, k = cyl(K); kx, ky, kz = x, y, z
w = ((np.arctan2(ky, kx) - th0) % (2 * np.pi)) // (2 * np.pi / 5)
m = np.abs(kz) < 1.2
for j in range(5): ax[0].scatter(kx[m & (w == j)], ky[m & (w == j)], s=26, c=cols[j], alpha=.85, lw=0)
sx, sy, sz, *_ = cyl(S); ms = np.abs(sz) < 1.2
ax[0].scatter(sx[ms], sy[ms], s=60, facecolors='none', edgecolors=fg, lw=1.4, label='silent (vacancy)')
for j in range(5):
    t = th0 + j * 2 * np.pi / 5; ax[0].plot([0, R * np.cos(t)], [0, R * np.sin(t)], color=mute, lw=.8, ls='--')
ax[0].set_aspect('equal'); ax[0].set_title('Down the five-fold axis (slab |z| < 1.2): five voices, vacancies circled', color=fg, fontsize=11)
ax[0].legend(loc='lower left', frameon=False, labelcolor=fg, fontsize=9)
# 2: all vacancies unrolled onto the boundary half-plane (five orbits fold onto one)
_, _, z, u, off, k = cyl(S); core = np.hypot(u, off) < 1.05
ax[1].scatter(u[~core], z[~core], s=34, c=np.abs(off[~core]), cmap='viridis', vmin=0, vmax=.7, lw=0)
ax[1].scatter(u[core], z[core], s=34, marker='x', c=fg, lw=1)
ax[1].axvline(0, color=mute, lw=.8); ax[1].set_xlabel('distance out from the axis along the boundary', color=mute); ax[1].set_ylabel('height along the axis', color=mute)
ax[1].set_aspect('equal'); ax[1].set_title('All vacancies folded onto one boundary half-plane\n(colour: offset off the plane, 0 to 0.7; x: core)', color=fg, fontsize=11)
# 3: growth
for tag, fn, c in (('R = 5', 'data/chorus-exact-big.json', cols[1]), ('R = 8', 'data/chorus-exact-r8.json', cols[2]), ('R = 10', 'data/chorus-exact-r10.json', cols[0])):
    try: d = json.load(open(fn))
    except FileNotFoundError: continue
    s = np.array(d['silenced']); r = np.sort(np.linalg.norm(s, axis=1)); r = r[r < d['RAD'] - 1]
    ax[2].step(r, np.arange(1, len(r) + 1), where='post', color=c, label=f'{tag} (to r = {d["RAD"] - 1:g})')
rr = np.linspace(0, R - 1, 100); r_, n_ = r, np.arange(1, len(r) + 1)
c2 = np.sum(n_ * r_ ** 2) / np.sum(r_ ** 4); c1 = np.sum(n_ * r_) / np.sum(r_ ** 2)
ax[2].plot(rr, c2 * rr ** 2, color=fg, ls=':', label='best fit ~ r² (area)'); ax[2].plot(rr, c1 * rr, color=mute, ls='--', label='best fit ~ r (line)')
ax[2].set_xlabel('distance from the centre', color=mute); ax[2].set_ylabel('vacancies inside', color=mute)
ax[2].set_title('How the vacancies grow', color=fg, fontsize=11); ax[2].legend(frameon=False, labelcolor=fg, fontsize=9)
fig.suptitle('DICTO Ogdoecontahedron five-fold chorus, exact to radius 10: the boundary vacancies', color=fg, fontsize=14, y=.99)
fig.text(.995, .01, 'DICTO · dictospheres.com', ha='right', color=mute, fontsize=9)
fig.tight_layout(rect=(0, .02, 1, .96)); fig.savefig('renders/chorus-boundary.png', dpi=110, facecolor=bg); print('saved')
