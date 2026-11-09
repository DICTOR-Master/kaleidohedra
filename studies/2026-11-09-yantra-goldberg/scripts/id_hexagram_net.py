# DICTO 11-09: "can the known hexagonal yantra make a network of a Goldberg sphere ... as small as possible, maybe an icosidodecahedron".
# Smallest base: the icosidodecahedron (ID). On each of its 20 triangles: a hexagram (Satkona) = the ID triangle (up) + the same
# triangle turned 60 deg about the face centre (down), both on the triangle's circumcircle (angular radius 20.905 deg = the Cleo-sphere
# circle). The turned tips point at the 12 pentagon centres; the 5 tips round each pentagon are joined as a pentagram.
# All sides are great-circle arcs. Panels: A hexagrams only, B hexagrams + pentagrams (the network). Checks printed, FINAL ok.
import numpy as np, itertools, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
phi = (1 + 5 ** .5) / 2
V = np.array([p for a in (-1, 1) for b in (-phi, phi) for p in ((0, a, b), (a, b, 0), (b, 0, a))], float); V /= np.linalg.norm(V[0])
E = [(i, j) for i, j in itertools.combinations(range(12), 2) if np.dot(V[i], V[j]) > .4]
F = [f for f in itertools.combinations(range(12), 3) if all((min(a, b), max(a, b)) in E for a, b in itertools.combinations(f, 2))]
assert len(E) == 30 and len(F) == 20
nrm = lambda x: x / np.linalg.norm(x)
def rot(v, ax, ang):
    ax = nrm(ax); return v * np.cos(ang) + np.cross(ax, v) * np.sin(ang) + ax * np.dot(ax, v) * (1 - np.cos(ang))
up, down, tips = [], [], {i: [] for i in range(12)}
for f in F:
    c = nrm(V[list(f)].sum(0)); mids = [nrm(V[a] + V[b]) for a, b in itertools.combinations(f, 2)]
    d = [rot(m, c, np.pi / 3) for m in mids]; up.append(mids); down.append(d)
    for p in d:
        k = int(np.argmax(V @ p)); tips[k].append(p)
rad = np.degrees(np.arccos(np.dot(nrm(V[list(F[0])].sum(0)), up[0][0])))
print(f'circumcircle angular radius {rad:.4f} deg (Cleo circle 20.9052)')
assert all(len(t) == 5 for t in tips.values())
tipd = np.degrees(np.arccos(np.dot(V[0], tips[0][0]))); print(f'turned tips: 5 round each pentagon centre, at {tipd:.4f} deg from it')
pent = []
for k, t in tips.items():
    ax = V[k]; e1 = nrm(np.cross(ax, [0.3, 0.1, 0.9])); e2 = np.cross(ax, e1)
    t = sorted(t, key=lambda p: np.arctan2(np.dot(p, e2), np.dot(p, e1))); pent.append([t[(2 * i) % 5] for i in range(5)])
def arc(a, b, n=40):
    w = np.arccos(np.clip(np.dot(a, b), -1, 1)); s = np.linspace(0, 1, n)[:, None]
    return (np.sin((1 - s) * w) * a + np.sin(s * w) * b) / np.sin(w)
Rv = np.array(rot(np.eye(3).T, [1, .3, 0], .35).T if False else np.eye(3))
def view(P):
    th, ph = .45, .3
    Rz = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]]); Rx = np.array([[1, 0, 0], [0, np.cos(ph), -np.sin(ph)], [0, np.sin(ph), np.cos(ph)]])
    return P @ (Rx @ Rz).T
def poly(ax, pts, col, lw):
    for a, b in zip(pts, pts[1:] + pts[:1]):
        P = view(arc(a, b)); front = P[:, 2] >= 0
        for m, al, l in ((front, 1, lw), (~front, .15, lw * .6)):
            Q = np.where(m[:, None], P, np.nan); ax.plot(Q[:, 0], Q[:, 1], color=col, alpha=al, lw=l, solid_capstyle='round')
fig, axs = plt.subplots(1, 2, figsize=(12, 6.4), facecolor='white')
for ax, withp, title in ((axs[0], False, 'A  20 hexagrams on the icosidodecahedron'), (axs[1], True, 'B  + 12 pentagrams: one network')):
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color='#999', lw=.8)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.08, 1.08); ax.set_ylim(-1.08, 1.08)
    for u in up: poly(ax, u, '#d62828', 1.6)          # fire red: upward (the ID triangles)
    for d in down: poly(ax, d, '#1d4ed8', 1.6)        # water blue: turned 60 deg
    if withp:
        for p in pent: poly(ax, p, '#7b2cbf', 1.6)    # aether violet: pentagrams
    ax.set_title(title, fontsize=12)
fig.text(.5, .02, 'Hexagram (Ṣaṭkoṇa) in each icosidodecahedron triangle, on its Cleo-sphere circle (20.905°); turned tips 5 round each pentagon · DICTO · dictospheres.com', ha='center', fontsize=9, color='#444')
out = '../figures/id-hexagram-network.png'; fig.savefig(out, dpi=150, bbox_inches='tight'); print('saved', out); print('FINAL ok')
