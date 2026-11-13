# Small renderer for the figures of The Permutohedron Paradigm (expanded version, 13 Nov 2026).
# House look (gold standard #43 v3): solid faces with light shading, crisp dark edges (>= 1.5 px at the output size), no haze,
# see-through glass for shells and helpers, the DICTO mark and emblem on every figure. Painter's algorithm on convex pieces:
# for an opaque convex solid only its front faces are drawn; glass draws back faces faintly, then front faces.
import os, math
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, '..', 'data', 'dicto-logo.png')
OUT = os.path.join(HERE, '..', 'figures')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.linewidth': 0.8})
# colours: the book's gold and violet; one red for the swapping pair in every figure (Fire, #cd3e28); element colours D I C T O
GOLD = '#e0b43c'; GOLD_D = '#9a7b2f'; VIOLET = '#8a5cc4'; RED = '#cd3e28'; BLUE = '#6b9ddb'; TEAL = '#3aa6a0'; INK = '#1c1c1c'; GREY = '#9a9a9a'
GLASS = '#cfd8e3'; IVORY = '#f3ead2'
ELEM = {'D': '#8a5cc4', 'I': '#3a70cd', 'C': '#488e48', 'T': '#cd3e28', 'O': '#e8c852'}
PHI = (1 + 5 ** .5) / 2
LIGHT = np.array([-0.4, 0.55, 0.75]); LIGHT /= np.linalg.norm(LIGHT)

def rot(az, el):
    """camera rotation: azimuth about z, then elevation; returns R with rows = screen x, screen y, depth (towards viewer)."""
    a, e = math.radians(az), math.radians(el)
    Rz = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, math.cos(e), -math.sin(e)], [0, math.sin(e), math.cos(e)]])
    M = Rx @ Rz
    return np.array([M[0], M[2], -M[1]])   # x right, y up (old z), depth = towards viewer

def hull_faces(P, tol=1e-7):
    """faces of the convex hull of points P (n,3): list of index lists in cyclic order, coplanar triangles merged; normals outward."""
    P = np.asarray(P, float); h = ConvexHull(P)
    planes = []
    for eq in h.equations:
        if not any(np.allclose(eq, q, atol=1e-6) for q in planes): planes.append(eq)
    faces = []
    for eq in planes:
        idx = [i for i in sorted(set(h.vertices)) if abs(P[i] @ eq[:3] + eq[3]) < 1e-6]
        c0 = P[idx].mean(0); n = eq[:3]; u = P[idx[0]] - c0; u /= np.linalg.norm(u); v = np.cross(n, u)
        idx.sort(key=lambda i: math.atan2((P[i] - c0) @ v, (P[i] - c0) @ u))
        # drop collinear corners
        k = 0
        while k < len(idx) and len(idx) > 3:
            a, b, c = P[idx[k - 1]], P[idx[k]], P[idx[(k + 1) % len(idx)]]
            if np.linalg.norm(np.cross(b - a, c - b)) < 1e-9: idx.pop(k)
            else: k += 1
        faces.append((idx, n))
    return faces

def halfspace_vertices(A, b):
    """vertices of {x : A x <= b} in R^3 (bounded), by brute force over triples (small systems)."""
    A = np.asarray(A, float); b = np.asarray(b, float); V = []
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                M = A[[i, j, k]]
                if abs(np.linalg.det(M)) < 1e-12: continue
                x = np.linalg.solve(M, b[[i, j, k]])
                if np.all(A @ x <= b + 1e-9) and not any(np.allclose(x, y, atol=1e-8) for y in V): V.append(x)
    return np.array(V)

def shade(col, n):
    c = np.array(matplotlib.colors.to_rgb(col)); f = 0.80 + 0.20 * max(-0.3, float(n @ LIGHT))
    return tuple(np.clip(c * f + (1 - f) * 0.30, 0, 1))

class Scene:
    """collects polygons in 3D with style; draw() sorts by depth and paints."""
    def __init__(self, R, byobject=True): self.R = R; self.items = []; self.byobject = byobject
    def solid(self, P, faces=None, color=GOLD, edge=INK, lw=1.0, alpha=1.0, glass=False, facecolors=None, offset=(0, 0, 0), z=0, edgecolors=None, shell=False):
        P = np.asarray(P, float) + np.asarray(offset, float)
        if faces is None: faces = hull_faces(P)
        c = P.mean(0); od = float(self.R[2] @ c); self.nobj = getattr(self, 'nobj', 0) + 1
        for fi, (f, n) in enumerate(faces):
            n = np.asarray(n, float); n = n / np.linalg.norm(n)
            if (P[f].mean(0) - c) @ n < 0: n = -n
            col = facecolors[fi] if facecolors else color
            ec = edgecolors[fi] if edgecolors else edge
            front = (self.R[2] @ n) > 0
            if glass:
                zz = z + (1 if front else -1) if shell else z
                self.items.append(dict(pts=P[f], n=n, col=col, edge=ec, lw=lw * (1.0 if front else 0.55), alpha=alpha if front else alpha * 0.5, front=front, z=zz, glass=True, od=od + (1e-6 if front else -1e-6)))
            elif front:
                self.items.append(dict(pts=P[f], n=n, col=col, edge=ec, lw=lw, alpha=alpha, front=True, z=z, glass=False, od=od))
    def poly(self, pts, color, edge=INK, lw=1.0, alpha=1.0, z=0, shade_it=True):
        pts = np.asarray(pts, float)
        n = np.cross(pts[1] - pts[0], pts[2] - pts[0]); nn = np.linalg.norm(n); n = n / nn if nn > 0 else np.array([0, 0, 1.0])
        if self.R[2] @ n < 0: n = -n
        self.items.append(dict(pts=pts, n=n, col=color, edge=edge, lw=lw, alpha=alpha, front=True, z=z, glass=not shade_it))
    def line(self, a, b, color=RED, lw=2.0, z=0, ls='-'):
        self.items.append(dict(line=(np.asarray(a, float), np.asarray(b, float)), col=color, lw=lw, z=z, ls=ls))
    def dot(self, p, color=INK, s=12, z=0, label=None, fs=7, dx=0, dy=0, lc=INK):
        self.items.append(dict(dot=np.asarray(p, float), col=color, s=s, z=z, label=label, fs=fs, dx=dx, dy=dy, lc=lc))
    def proj(self, p): return (self.R @ np.asarray(p, float).T).T
    def draw(self, ax, scale=1.0, shift=(0, 0)):
        def depth(it):
            if 'line' in it: return float((self.R[2] @ ((it['line'][0] + it['line'][1]) / 2))) + 1e-3
            if 'dot' in it: return float(self.R[2] @ it['dot']) + 2e-3
            return float((self.R[2] @ it['pts'].T).mean())
        for kk, it in enumerate(sorted(self.items, key=lambda it: (it['z'], it.get('od', depth(it)) if self.byobject else depth(it), depth(it)))):
            zo = 2 + kk * 1e-4
            if 'line' in it:
                a, b = self.proj(it['line'][0]) * scale, self.proj(it['line'][1]) * scale
                ax.plot([a[0] + shift[0], b[0] + shift[0]], [a[1] + shift[1], b[1] + shift[1]], color=it['col'], lw=it['lw'], solid_capstyle='round', ls=it['ls'], zorder=zo)
            elif 'dot' in it:
                p = self.proj(it['dot']) * scale
                ax.scatter([p[0] + shift[0]], [p[1] + shift[1]], s=it['s'], color=it['col'], zorder=zo, edgecolors='none')
                if it['label']: ax.text(p[0] + shift[0] + it['dx'], p[1] + shift[1] + it['dy'], it['label'], fontsize=it['fs'], color=it['lc'], ha='center', va='center', zorder=50,
                                        bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.75))
            else:
                q = self.proj(it['pts'])[:, :2] * scale + np.asarray(shift)
                fc = it['col'] if it['glass'] else shade(it['col'], it['n'])
                ax.add_patch(MPoly(q, closed=True, facecolor=fc, alpha=it['alpha'], edgecolor='none', zorder=zo))
                if it['edge'] is not None and it['lw'] > 0:
                    ax.add_patch(MPoly(q, closed=True, facecolor='none', edgecolor=it['edge'], lw=it['lw'], joinstyle='round', zorder=zo + 5e-5, alpha=1.0 if it['front'] else 0.55))

def mark(fig, dark=False):
    """the DICTO mark and the gold emblem, lower right of every figure."""
    w, h = fig.get_size_inches(); e = 0.30; sx, sy = e / w, e / h
    fig.text(0.992 - sx - 0.006, 0.006 + sy / 2, 'DICTO · dictospheres.com', ha='right', va='center', fontsize=7.5, color='#9a7b2f')
    try:
        ax = fig.add_axes([0.992 - sx, 0.006, sx, sy]); ax.imshow(plt.imread(LOGO)); ax.axis('off')
    except Exception as ex:
        print('logo not drawn:', ex)

def blank(ax):
    ax.set_aspect('equal'); ax.axis('off')

def save(fig, name, dpi=220):
    os.makedirs(OUT, exist_ok=True); p = os.path.join(OUT, name)
    fig.savefig(p, dpi=dpi, facecolor='white'); plt.close(fig); print('wrote', name, flush=True); return p

def perms(vals):
    import itertools
    return [tuple(p) for p in itertools.permutations(vals)]

def basis_sum0(n):
    """orthonormal basis of {x in R^n : sum x = 0} (rows)."""
    M = np.eye(n) - 1.0 / n; Q, _ = np.linalg.qr(M[:, :n - 1]); return Q.T

def basis_perp(n, extra):
    """orthonormal basis of {x : sum x = 0, x.e = 0 for e in extra} (rows)."""
    C = np.vstack([np.ones(n)] + [np.asarray(e, float) for e in extra])
    _, s, Vt = np.linalg.svd(C); r = int((s > 1e-10).sum()); return Vt[r:]
