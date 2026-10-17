# DICTO 2026-10-17 night: "start with a dome construction shape of pents and hexagons, Goldberg polyhedra, as the top mesh and the opposite
# pattern at the bottom; then every scutoid has a clear path and a place in the group — flattened out". Step 1 (to check the vision): the two
# patterns only. Top = the truncated icosahedron (Goldberg GP(1,1)) as a dome about a hexagon (axis (1,1,1), 3-fold symmetric); bottom = the
# opposite pattern: the 6 axis edge flips (one Th orbit) turn its 12 pentagons into hexagons and 12 hexagons into pentagons, same cells.
# Flattened by azimuthal-equidistant projection about the axis. -> renders/dome-patterns.svg
import itertools, json, numpy as np
from scipy.spatial import HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
ICO = np.array([c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1, s2 * phi])], float)
DOD = np.array([[a, b, c] for a in (1, -1) for b in (1, -1) for c in (1, -1)] + [c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1 * phi, s2 / phi])], float)
diag = np.array([abs(abs(v[0]) - abs(v[1])) < 1e-9 and abs(abs(v[1]) - abs(v[2])) < 1e-9 for v in DOD])
N = np.vstack([ICO, DOD[diag], DOD[~diag]]); G = ['P'] * 12 + ['Hd'] * 8 + ['Ho'] * 12
TI = []
for b in ([0, 1, 3 * phi], [1, 2 + phi, 2 * phi], [phi, 2, phi ** 3]):
    for c in cyc(b):
        for s in itertools.product((1, -1), repeat=3): TI.append([c[k] * s[k] for k in range(3)])
TI = np.unique(np.round(TI, 9), axis=0); dA = (TI @ N.T).max(0)
def faces(d):
    V = HalfspaceIntersection(np.c_[N, -d], np.zeros(3)).intersections; V = np.unique(np.round(V, 9), axis=0); F = []
    for i in range(32):
        P = V[np.abs(V @ N[i] - d[i]) < 1e-7]; n = N[i] / np.linalg.norm(N[i]); o = P.mean(0)
        u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
        F.append(P[np.argsort(np.arctan2((P - o) @ w, (P - o) @ u))])
    return F
top = faces(dA); bot = faces(np.array([dA[i] * (1.2 if G[i] == 'Ho' else 1) for i in range(32)]))   # Ho pushed past the flip (k > (5-φ)/3)
ax = np.ones(3) / 3 ** .5; e1 = np.array([1, -1, 0]) / 2 ** .5; e2 = np.cross(ax, e1)
def flat(v):
    v = v / np.linalg.norm(v); th = np.arccos(np.clip(v @ ax, -1, 1)); a = np.arctan2(v @ e2, v @ e1); return th * np.array([np.cos(a), -np.sin(a)])
cen = [np.degrees(np.arccos(np.clip(N[i] @ ax / np.linalg.norm(N[i]), -1, 1))) for i in range(32)]
keep = [i for i in range(32) if cen[i] < 95]
print('cells in the dome:', len(keep), {g: sum(G[i] == g for i in keep) for g in ('P', 'Hd', 'Ho')})
print('sides top / bottom:', [(i, G[i], len(top[i]), len(bot[i])) for i in keep])
order = sorted(keep, key=lambda i: (round(cen[i]), np.arctan2(*flat(N[i])[::-1]))); num = {i: k + 1 for k, i in enumerate(order)}
S = 120; W = 2 * 2.0 * S
def panel(F, ox, title):
    out = [f'<g transform="translate({ox + W / 2},{W / 2 + 40})">', f'<text x="0" y="{-W / 2 + 6}" text-anchor="middle" class="t">{title}</text>']
    for i in keep:
        pts = np.array([flat(v) for v in F[i]]) * S; n = len(F[i])
        col = '#e8b84a' if n == 5 else '#7fd6cb' if n == 6 else '#e57373'
        chg = len(top[i]) != len(bot[i])
        out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{col}" stroke="#2a2218" stroke-width="{2.2 if chg else 1.2}"/>')
        c = pts.mean(0); out.append(f'<text x="{c[0]:.1f}" y="{c[1] + 5:.1f}" text-anchor="middle" class="n">{num[i]}</text>')
    out.append('</g>'); return '\n'.join(out)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {2 * W + 40} {W + 110}" font-family="Georgia, serif">',
       '<style>.t{font-size:22px;font-weight:600;fill:#2a2218}.n{font-size:13px;fill:#2a2218}.m{font-size:14px;fill:#6b604f}</style>',
       f'<rect width="100%" height="100%" fill="#f4f1ea"/>', panel(top, 0, 'Top: Goldberg dome (pentagons gold)'), panel(bot, W + 40, 'Bottom: the opposite pattern'),
       f'<text x="{2 * W + 30}" y="{W + 100}" text-anchor="end" class="m">DICTO · dictospheres.com — same number = same scutoid, top and bottom; bold outline = changes 5↔6</text></svg>']
open('renders/dome-patterns.svg', 'w').write('\n'.join(svg))
