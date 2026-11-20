# Where does the rhombic triacontahedron (RT) meet four dimensions?  Gap study 2026-11-21, grid cell "RT x 4D" (empty).
# Float SCREEN (numpy/scipy): for the 600-cell, the 120-cell, their rectifications, and controls (tesseract, 24-cell),
# along the vertex, edge, 2-face and cell axes, list the shapes of
#   (a) the orthogonal projection (shadow) onto the 3-space perpendicular to the axis,
#   (b) the central section by that 3-space,
#   (c) every layer of corners at one height (hull of the corners at that height).
# A shape is reported by (corners, faces by number of sides). An RT is (32 corners; 30 four-sided faces, all rhombi).
# Every RT hit is then confirmed exactly by rt_4d_exact.py.  Controls: tesseract corner-first shadow = RD (classical);
# 24-cell central section perpendicular to a corner = cuboctahedron (classical).
import itertools, sys
import numpy as np
from scipy.spatial import ConvexHull

phi = (1 + 5 ** .5) / 2

def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0: out.append([v[i] for i in p])
    return out

def signs(v):
    out = []
    for s in itertools.product([1, -1], repeat=len(v)):
        w = [a * b for a, b in zip(s, v)]
        out.append(w)
    return out

def uniq(P, tol=1e-9):
    P = np.array(P, float); keep = []
    for p in P:
        if not any(np.linalg.norm(p - q) < tol for q in keep): keep.append(p)
    return np.array(keep)

def c600():
    V = [s for v in itertools.permutations([1, 0, 0, 0]) for s in signs(v)]
    V += signs([.5, .5, .5, .5])
    V += [p for s in signs([phi / 2, .5, 1 / (2 * phi), 0]) for p in even_perms(s)]
    return uniq(V)

def edges(V):
    D = np.linalg.norm(V[:, None] - V[None], axis=2); e = np.min(D[D > 1e-9])
    return [(i, j) for i in range(len(V)) for j in range(i + 1, len(V)) if abs(D[i, j] - e) < 1e-7], e

def polar_vertices(V):
    h = ConvexHull(V); out = []
    for eq in h.equations:
        n, d = eq[:4], eq[4]; out.append(n / (-d))
    return uniq(out)

def shape3(P):
    P = uniq(P, 1e-7)
    if len(P) < 4: return None
    h = ConvexHull(P); planes = {}
    for eq in h.equations:
        key = tuple(np.round(eq, 7)); planes.setdefault(key, eq)
    faces = []
    for eq in planes.values():
        S = [i for i in range(len(P)) if abs(P[i] @ eq[:3] + eq[3]) < 1e-7]; faces.append(S)
    verts = sorted(set(h.vertices))
    hist = {}
    for f in faces: hist[len(f)] = hist.get(len(f), 0) + 1
    return len(verts), dict(sorted(hist.items())), faces, P

def is_rt(sh):
    if sh is None: return False
    nv, hist, faces, P = sh
    if nv != 32 or hist != {4: 30}: return False
    for f in faces:  # rhombus with diagonals in ratio phi
        Q = P[f]; c = Q.mean(0); d = sorted(np.linalg.norm(Q - c, axis=1))
        sides = [np.linalg.norm(Q[i] - Q[j]) for i in range(4) for j in range(i + 1, 4)]
        if abs(d[3] / d[0] - phi) > 1e-6: return False
    return True

def basis_perp(u):
    u = u / np.linalg.norm(u); M = np.linalg.svd(np.eye(4) - np.outer(u, u))[0][:, :3]
    return u, M

def screen(name, V, axes, report):
    E, elen = edges(V)
    for an, u in axes.items():
        u, M = basis_perp(np.array(u, float))
        h = V @ u
        proj = V @ M
        sh = shape3(proj)
        report.append((name, an, 'shadow', sh[0], sh[1], is_rt(sh)))
        cuts = [V[i] for i in range(len(V)) if abs(h[i]) < 1e-9]
        for i, j in E:
            if h[i] * h[j] < -1e-18:
                t = h[i] / (h[i] - h[j]); cuts.append(V[i] + t * (V[j] - V[i]))
        if len(cuts) >= 4:
            sh = shape3(np.array(cuts) @ M); report.append((name, an, 'central section', sh[0], sh[1], is_rt(sh)))
        for lev in sorted(set(np.round(h, 9))):
            L = V[np.abs(h - lev) < 1e-8] @ M
            if len(L) >= 4 and np.linalg.matrix_rank(L - L.mean(0), tol=1e-8) == 3:
                sh = shape3(L); report.append((name, an, f'corner layer h={lev:+.6f}', sh[0], sh[1], is_rt(sh)))

def axes_of(V):
    E, _ = edges(V); V = np.array(V)
    ax = {'corner': V[0], 'edge': V[E[0][0]] + V[E[0][1]]}
    h = ConvexHull(V); eq = h.equations[0]; ax['cell'] = -eq[:4]
    # a 2-face: three or more corners of one cell sharing a plane with the axis of the ridge; take the centre of the face
    # common to two adjacent cells
    n0 = eq[:4]; d0 = eq[4]
    on0 = set(i for i in range(len(V)) if abs(V[i] @ n0 + d0) < 1e-9)
    for eq2 in h.equations[1:]:
        on2 = set(i for i in range(len(V)) if abs(V[i] @ eq2[:4] + eq2[4]) < 1e-9)
        common = on0 & on2
        if len(common) >= 3 and not np.allclose(eq2, eq):
            ax['2-face'] = V[list(common)].mean(0); break
    return ax

report = []
V600 = c600(); assert len(V600) == 120
V120 = polar_vertices(V600); assert len(V120) == 600, len(V120)
E600, _ = edges(V600); R600 = uniq([(V600[i] + V600[j]) / 2 for i, j in E600]); assert len(R600) == 720
E120, _ = edges(V120); R120 = uniq([(V120[i] + V120[j]) / 2 for i, j in E120]); assert len(R120) == 1200
T4 = uniq(signs([1, 1, 1, 1]))
C24 = uniq([s for v in set(itertools.permutations([1, 1, 0, 0])) for s in signs(v)])
for name, V in [('tesseract (control)', T4), ('24-cell (control)', C24), ('600-cell', V600), ('120-cell', V120),
                ('rectified 600-cell', R600), ('rectified 120-cell', R120)]:
    base = V600 if '600' in name else (V120 if '120' in name else V)
    ax = axes_of(base if 'rectified' in name else V)
    if 'rectified' in name:  # also use the axes of the other regular one (dual directions)
        ax2 = axes_of(V120 if '600' in name else V600); ax.update({k + ' (dual)': v for k, v in ax2.items()})
    screen(name, V, ax, report)
    print(f'{name}: {len(V)} corners screened along {list(ax)}'); sys.stdout.flush()

ok_rd = any(r[0].startswith('tesseract') and r[2] == 'shadow' and r[3] == 14 and r[4] == {4: 12} for r in report)
ok_co = any(r[0].startswith('24-cell') and r[2] == 'central section' and r[3] == 12 and r[4] == {3: 8, 4: 6} for r in report)
print(('ok   ' if ok_rd else 'FAIL ') + 'control: tesseract corner-first shadow is the RD (14 corners, 12 four-sided faces)')
print(('ok   ' if ok_co else 'FAIL ') + 'control: 24-cell central section perpendicular to a corner is the cuboctahedron')
for r in report:
    print(('RT  ' if r[5] else '    ') + f'{r[0]:22s} {r[1]:14s} {r[2]:28s} corners {r[3]:4d} faces {r[4]}')
hits = [r for r in report if r[5]]
print('RT HITS:', len(hits))
for r in hits: print('   ', r[:3])
print('FINAL ok' if ok_rd and ok_co else 'FINAL FAIL (controls)')
