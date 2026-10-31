# Build sheets for the HexOct c-tile and h-tile from PET-bottle-cap security rings (DICTO's idea, 2026-10-31), at the chosen
# weight lambda = -1/8 (the only weight of the walk where every face of both tiles can be laid with rings; see scan.py).
# Double scale: one ring = a triangle of side 1/2 (ball spacing 1), so a unit triangle = 4 rings, as DICTO proposed.
# For each solid of each tile: exact faces (exactfaces.py), the rings of every face, a net found by unfolding along a spanning
# tree of the faces (random trees, first rejected if two faces overlap, then the most compact kept), counts, and a 3D drawing
# (z-buffer renderer in the style of studies/2026-10-31-hexoct-plates/scripts/plates.py: solid faces, crisp edges, ring
# sides drawn thin on the faces). Ring drawing helpers rounded() and ties() are those of studies/2026-10-31-ring-nets.
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless LOGO=<dicto-logo.png> ~/geom/bin/python build.py -> ../out/*.png, counts.json
import os, sys, json, math, random
import numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get('TILES_DIR', os.path.join(HERE, '../../2026-10-29-endless-stack-cell/scripts'))); sys.path.insert(0, HERE)
from tiles import tile
import exactfaces as E
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Polygon as MPoly
from matplotlib.path import Path
from shapely.geometry import Polygon as SPoly
LOGO = os.environ.get('LOGO', os.path.join(HERE, '../../../papers/dicto-logo.png'))
OUT = os.path.join(HERE, '../out'); os.makedirs(OUT, exist_ok=True)
LAM = Fr(-1, 8)
D = (2 / 3) ** 0.5
def cart(p): return np.array([float(p[0]) + float(p[1]) / 2, float(p[1]) * 3 ** 0.5 / 2, float(p[2]) * D])
COL = {'c': '#d9a521', 'h': '#3f7fc4'}
LIGHT = {'c': '#f1d98a', 'h': '#a9c9ec'}
EDGE = '#1c1c1c'

# ---------- ring helpers (from studies/2026-10-31-ring-nets/scripts/ring_nets.py) ----------
def rounded(P, k=0.16):
    P = [np.array(p) for p in P]; verts, codes = [], []
    for n in range(3):
        a, b, c = P[n - 1], P[n], P[(n + 1) % 3]
        p1 = b + (a - b) * k; p2 = b + (c - b) * k
        verts += [p1, b, p2]
        codes += ([Path.MOVETO] if not codes else [Path.LINETO]) + [Path.CURVE3, Path.CURVE3]
    verts.append(verts[0]); codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)
def ties(P, inset=0.06):
    c = np.mean(P, 0); out = []
    for n in range(3):
        a, b = P[n], P[(n + 1) % 3]
        for t in (.25, .75):
            p = a + (b - a) * t; out.append(p + (c - p) * inset)
    return out

# ---------- exact faces, split into solids, rings per face ----------
def split_edges(faces):
    """insert every surface corner that lies inside a side, so neighbouring faces share whole sides"""
    V = sorted({p for f in faces for lp in f['loops'] for p in lp})
    for f in faces:
        new = []
        for lp in f['loops']:
            out = []
            for i in range(len(lp)):
                p, q = lp[i], lp[(i + 1) % len(lp)]; d = E.sub(q, p); dd = E.dot(d, d)
                mid = [x for x in V if x not in (p, q) and E.cross(E.sub(x, p), d) == (0, 0, 0) and 0 < E.dot(E.sub(x, p), d) < dd]
                out += [p] + sorted(mid, key=lambda x: E.dot(E.sub(x, p), d))
            new.append(out)
        f['sloops'] = new
    return faces

def rings_of(face):
    r = E.ring_test(face); assert r, 'face not ring-buildable'
    e1, e2, o, C = r['e1'], r['e2'], r['origin'], r['coords']
    poly = SPoly([tuple(float(x) for x in C[p]) for p in face['loops'][0]])
    A = [C[p][0] for p in C]; B = [C[p][1] for p in C]
    out = []
    for a in range(int(min(A)) - 1, int(max(A)) + 2):
        for b in range(int(min(B)) - 1, int(max(B)) + 2):
            for T in (((a, b), (a + 1, b), (a, b + 1)), ((a + 1, b), (a + 1, b + 1), (a, b + 1))):
                cx = sum(t[0] for t in T) / 3; cy = sum(t[1] for t in T) / 3
                if poly.contains(SPoly([(cx - 1e-3, cy - 1e-3), (cx + 1e-3, cy - 1e-3), (cx, cy + 1e-3)])):
                    out.append([E.add(o, E.add(E.mul(e1, Fr(t[0])), E.mul(e2, Fr(t[1])))) for t in T])
    assert len(out) == r['rings'], (len(out), r['rings'])
    return out

def solids(faces):
    par = list(range(len(faces)))
    def fd(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    em = {}
    for i, f in enumerate(faces):
        lp = f['sloops'][0]
        for j in range(len(lp)): em.setdefault(frozenset((lp[j], lp[(j + 1) % len(lp)])), []).append(i)
    for e, L in em.items():
        assert len(L) == 2, ('side not shared by exactly two faces', e, L)
        par[fd(L[1])] = fd(L[0])
    S = {}
    for i in range(len(faces)): S.setdefault(fd(i), []).append(i)
    return list(S.values()), em

def kind(f):
    n = len(f['loops'][0]); sides = [E.is_sq(E.len2(E.sub(f['loops'][0][(i + 1) % n], f['loops'][0][i]))) for i in range(n)]
    name = {3: 'triangle', 4: 'quadrilateral', 5: 'pentagon', 6: 'hexagon'}[n]
    if n == 6 and len(set(sides)) == 1: name = 'regular hexagon'
    if n == 3: name = 'unit triangle' if sides[0] == 1 else 'small triangle'
    if n == 4: name = 'trapezoid'
    return name, sides

# ---------- unfolding ----------
def local2d(face):
    X = [cart(p) for p in face['sloops'][0]]
    n = np.array([float(x) for x in face['n']]);
    # outward normal in Cartesian: transform the lattice-coordinate normal (a covector) by the inverse transpose of the map
    M = np.array([[1, .5, 0], [0, 3 ** .5 / 2, 0], [0, 0, D]]); nc = np.linalg.inv(M).T @ n; nc /= np.linalg.norm(nc)
    u = X[1] - X[0]; u /= np.linalg.norm(u); v = np.cross(nc, u)
    to2 = lambda Y: np.array([(Y - X[0]) @ u, (Y - X[0]) @ v])
    return to2

def unfold(fids, faces, em, tries=4000, seed=1):
    rnd = random.Random(seed)
    nb = {i: [] for i in fids}
    for e, L in em.items():
        a, b = L
        if a in nb and b in nb: nb[a].append((b, e)); nb[b].append((a, e))
    loc = {i: local2d(faces[i]) for i in fids}
    best = None
    root_order = sorted(fids, key=lambda i: -E.ring_test(faces[i])['rings'])
    for t in range(tries):
        root = root_order[0] if t % 3 == 0 else rnd.choice(fids)
        place = {root: (np.eye(2), np.zeros(2))}; tree = set(); frontier = [root]
        while frontier:
            i = frontier.pop(rnd.randrange(len(frontier)) if t else 0)
            Ni = nb[i][:]; rnd.shuffle(Ni)
            for j, e in Ni:
                if j in place: continue
                p, q = tuple(e)
                Rm, tv = place[i]; P2 = Rm @ loc[i](cart(p)) + tv; Q2 = Rm @ loc[i](cart(q)) + tv
                p1, q1 = loc[j](cart(p)), loc[j](cart(q))
                a0 = math.atan2(*(q1 - p1)[::-1]); a1 = math.atan2(*(Q2 - P2)[::-1]); th = a1 - a0
                R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
                place[j] = (R, P2 - R @ p1); tree.add(e); frontier.append(j)
        polys = {}
        for i in fids:
            Rm, tv = place[i]; polys[i] = SPoly([tuple(Rm @ loc[i](cart(p)) + tv) for p in faces[i]['sloops'][0]])
        ok = all(polys[a].intersection(polys[b]).area < 1e-9 for ai, a in enumerate(fids) for b in fids[ai + 1:])
        if not ok: continue
        U = np.array([c for P in polys.values() for c in P.exterior.coords])
        w, h = U.max(0) - U.min(0)
        # prefer a compact, landscape-friendly net
        score = max(w, h * 1.25) ** 2
        if best is None or score < best[0]: best = (score, place, tree, loc)
    assert best, 'no net found'
    return best[1:]

def draw_net(ax, fids, faces, em, place, tree, loc, col, light, letter_start=0):
    letters = 'ABCDEFGHIJKLMNPQRSTUVWXYZ'; li = letter_start; allp = []
    # a non-tree side whose two copies land on the same place in the net is tied flat like a fold line
    def pos(i, e):
        Rm, tv = place[i]; return sorted(tuple(np.round(Rm @ loc[i](cart(p)) + tv, 7)) for p in e)
    tree = set(tree) | {e for e, L in em.items() if L[0] in fids and e not in tree and pos(L[0], e) == pos(L[1], e)}
    cut = [e for e, L in em.items() if L[0] in fids and e not in tree]
    lab = {e: letters[k % len(letters)] + ('' if k < len(letters) else str(k // len(letters))) for k, e in enumerate(cut, li)}
    for i in fids:
        Rm, tv = place[i]; f2 = lambda p: Rm @ loc[i](cart(p)) + tv
        poly = [f2(p) for p in faces[i]['sloops'][0]]; allp += poly
        ax.add_patch(MPoly(poly, closed=True, facecolor=matplotlib.colors.to_rgba(light, 0.35), edgecolor='none', zorder=1))
        for T in faces[i]['rings']:
            P = [f2(p) for p in T]
            ax.add_patch(PathPatch(rounded(P), facecolor=matplotlib.colors.to_rgba(col, 0.30), edgecolor='#1d1d24', lw=1.5, zorder=2))
            for tp in ties(P): ax.plot(*tp, 'o', ms=3.0, color='#1d1d24', zorder=3)
        # face outline: fold lines dashed, cut sides solid
        L = faces[i]['sloops'][0]
        for j in range(len(L)):
            p, q = L[j], L[(j + 1) % len(L)]; e = frozenset((p, q)); a, b = f2(p), f2(q)
            if e in tree: ax.plot(*zip(a, b), color='#1f6f3f', lw=2.0, ls=(0, (3, 2)), zorder=4)
            else:
                ax.plot(*zip(a, b), color=EDGE, lw=2.6, zorder=4)
                m = (a + b) / 2; c = np.mean(poly, 0); d = c - m; d /= np.linalg.norm(d)
                ax.text(*(m + d * 0.08), lab[e], fontsize=12, ha='center', va='center', color='#b00020', weight='bold', zorder=5)
    A = np.array(allp); pad = 0.12
    ax.set_xlim(A[:, 0].min() - pad, A[:, 0].max() + pad); ax.set_ylim(A[:, 1].min() - pad, A[:, 1].max() + pad)
    ax.set_aspect('equal'); ax.axis('off')
    # ring sides tied flat (inside faces and across fold lines) and tied when closing (cut sides, counted once)
    half = lambda e: int(E.is_sq(E.len2(E.sub(*tuple(e)))) * 2)
    return sum(half(e) for e in cut), sum(half(e) for e in tree), len(cut)

# ---------- 3D drawing: z-buffer with face ids and ring ids (plates.py method) ----------
class View:
    def __init__(self, elev, azim):
        e, a = math.radians(elev), math.radians(azim)
        self.f = -np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
        self.r = np.cross(self.f, [0, 0, 1.0]); self.r /= np.linalg.norm(self.r); self.u = np.cross(self.r, self.f)
        L1 = -self.f * 0.55 + self.u * 0.65 - self.r * 0.45; self.L1 = L1 / np.linalg.norm(L1)
        L2 = -self.f * 0.6 + self.r * 0.7 - self.u * 0.2; self.L2 = L2 / np.linalg.norm(L2)
    def proj(self, P): P = np.atleast_2d(P); return np.c_[P @ self.r, P @ self.u, P @ self.f]
def hex2rgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])
def render3d(tris, view, w, h, SS=3, pad=0.06, edge_px=2.6, ring_px=1.0, scale=None):
    """tris: list of (3x3 Cartesian triangle, face id, ring id, rgb, normal)"""
    T3 = [(np.array(t), fi, ri, rgb, n) for t, fi, ri, rgb, n in tris if n @ view.f < -1e-9]
    allp = view.proj(np.vstack([t for t, *_ in tris])); lo, hi = allp[:, :2].min(0), allp[:, :2].max(0); cen = (lo + hi) / 2
    if scale is None: scale = min(w * (1 - 2 * pad) / (hi[0] - lo[0]), h * (1 - 2 * pad) / (hi[1] - lo[1]))
    sw, sh = w * SS, h * SS
    zb = np.full((sh, sw), np.inf, np.float32); fb = np.full((sh, sw), -1, np.int32); rb = np.full((sh, sw), -1, np.int32)
    cols = [np.ones(3)]
    for k, (t, fi, ri, rgb, n) in enumerate(T3):
        kk = 0.56 + 0.40 * max(0.0, float(n @ view.L1)) + 0.14 * max(0.0, float(n @ view.L2)); cols.append(np.clip(rgb * kk, 0, 1))
        X = view.proj(t); X = np.c_[(X[:, 0] - cen[0]) * scale * SS + sw / 2, sh / 2 - (X[:, 1] - cen[1]) * scale * SS, X[:, 2]]
        a, b, c = X
        x0, x1 = int(max(0, math.floor(X[:, 0].min()))), int(min(sw - 1, math.ceil(X[:, 0].max())))
        y0, y1 = int(max(0, math.floor(X[:, 1].min()))), int(min(sh - 1, math.ceil(X[:, 1].max())))
        den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if x1 < x0 or y1 < y0 or abs(den) < 1e-12: continue
        XX, YY = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        l1 = ((b[1] - c[1]) * (XX - c[0]) + (c[0] - b[0]) * (YY - c[1])) / den
        l2 = ((c[1] - a[1]) * (XX - c[0]) + (a[0] - c[0]) * (YY - c[1])) / den
        l3 = 1 - l1 - l2; m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        z = (l1 * a[2] + l2 * b[2] + l3 * c[2]).astype(np.float32)
        zs = zb[y0:y1 + 1, x0:x1 + 1]; m &= z < zs - 1e-5
        zs[m] = z[m]; fb[y0:y1 + 1, x0:x1 + 1][m] = fi; rb[y0:y1 + 1, x0:x1 + 1][m] = k + 1
    img = np.array(cols)[rb + 1 * 0].copy() if False else np.array(cols)[np.where(rb < 0, 0, rb)]
    def dil(e, px):
        r = max(1, int(round(px * SS / 2))); d = e.copy()
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(e, dy, 0), dx, 1)
        return d
    rid = np.array([-1] + [ri for t, fi, ri, rgb, n in T3])[np.where(rb < 0, 0, rb)]
    ef = np.zeros((sh, sw), bool); ef[:, 1:] |= fb[:, 1:] != fb[:, :-1]; ef[1:, :] |= fb[1:, :] != fb[:-1, :]
    er = np.zeros((sh, sw), bool); er[:, 1:] |= rid[:, 1:] != rid[:, :-1]; er[1:, :] |= rid[1:, :] != rid[:-1, :]
    img[dil(er, ring_px)] = img[dil(er, ring_px)] * 0.55
    img[dil(ef, edge_px)] = hex2rgb(EDGE)
    return img.reshape(h, SS, w, SS, 3).mean((1, 3)), scale

def cnormal(f):
    M = np.array([[1, .5, 0], [0, 3 ** .5 / 2, 0], [0, 0, D]]); nc = np.linalg.inv(M).T @ np.array([float(x) for x in f['n']])
    return nc / np.linalg.norm(nc)

def tile_tris(faces, fids, rgb, offset=np.zeros(3)):
    out = []; rid = 0
    for i in fids:
        n = cnormal(faces[i])
        for T in faces[i]['rings']:
            out.append(([cart(p) + offset for p in T], i, rid, rgb, n)); rid += 1
    return out

def save_img(img, path, label=None):
    h, w = img.shape[:2]; fig = plt.figure(figsize=(w / 200, h / 200), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(np.clip(img, 0, 1), interpolation='lanczos'); ax.axis('off')
    lg = plt.imread(LOGO); lw = 0.10 * w
    ax.imshow(lg, extent=(w - lw - 10, w - 10, h - 10, h - 10 - lw * lg.shape[0] / lg.shape[1]), zorder=6); ax.set_xlim(0, w); ax.set_ylim(h, 0)
    if label: ax.text(12, 24, label, fontsize=9, color='#333', va='top')
    fig.savefig(path, dpi=200); plt.close(fig)

# ---------- main ----------
if __name__ == '__main__':
    facts = {'lambda': str(LAM)}
    for t, w, L in (('c', 'ABC', 1), ('h', 'AB', 0)):
        P = tile(w, L, LAM)[0]; faces = split_edges(E.union_faces([p[3] for p in P]))
        for f in faces: f['rings'] = rings_of(f)
        S, em = solids(faces)
        tf = dict(solids=[], faces=len(faces), rings=0, shared_sides=0, ties=0, kinds={})
        # where the solids touch
        if len(S) > 1:
            Vs = [set(p for i in s for p in faces[i]['loops'][0]) for s in S]; common = set.intersection(*Vs)
            tf['solids_touch_at'] = [[str(x) for x in p] for p in common]
            # exact: solid 2 is solid 1 sent through the touching point (x -> -x), and solid 1 has the mirror (u, v, z) -> (v, u, z)
            # (an isometry of the lattice metric), so the two solids are congruent by a proper motion: one net, made twice
            tf['solid2_is_minus_solid1'] = Vs[1] == {tuple(-x for x in p) for p in Vs[0]}
            tf['solid1_has_mirror'] = Vs[0] == {(p[1], p[0], p[2]) for p in Vs[0]}
        for si, fids in enumerate(S):
            N = sum(len(faces[i]['rings']) for i in fids)
            perim = sum(sum(E.is_sq(E.len2(E.sub(lp[(j + 1) % len(lp)], lp[j]))) * 2 for j in range(len(lp))) for i in fids for lp in [faces[i]['loops'][0]])
            inner = sum((3 * len(faces[i]['rings']) - sum(E.is_sq(E.len2(E.sub(faces[i]['loops'][0][(j + 1) % len(faces[i]['loops'][0])], faces[i]['loops'][0][j]))) * 2
                        for j in range(len(faces[i]['loops'][0])))) / 2 for i in fids)
            along = perim / 2
            assert inner + along == Fr(3 * N, 2)
            V = len({p for i in fids for p in faces[i]['sloops'][0]}); Eg = len([e for e, Lf in em.items() if Lf[0] in fids])
            for i in fids:
                nm, sides = kind(faces[i]); k = tf['kinds'].setdefault(nm, dict(count=0, rings_each=len(faces[i]['rings']), sides=[str(s) for s in sides]))
                k["count"] += 1
            sol = dict(faces=len(fids), rings=N, shared_sides_in_faces=int(inner), shared_sides_on_edges=int(along), shared_sides=int(inner + along),
                       ties=int(2 * (inner + along)), corners=V, sides=Eg, euler=V - Eg + len(fids),
                       height=float(max(cart(p)[2] for i in fids for p in faces[i]['loops'][0]) - min(cart(p)[2] for i in fids for p in faces[i]['loops'][0])))
            # net
            if t == 'c' and si > 0: tf['solids'].append(sol); tf['rings'] += N; tf['shared_sides'] += sol['shared_sides']; tf['ties'] += sol['ties']; continue
            place, tree, loc = unfold(fids, faces, em, tries=3000 if t == 'h' else 1500, seed=7 + si)
            fig = plt.figure(figsize=(7.2, 6.0)); ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
            nclose, nfold, ncut = draw_net(ax, fids, faces, em, place, tree, loc, COL[t], LIGHT[t])
            sol['ring_sides_tied_flat'] = sol['shared_sides_in_faces'] + nfold; sol['ring_sides_tied_closing'] = nclose
            sol['cut_face_sides'] = ncut
            assert sol['ring_sides_tied_flat'] + nclose == sol['shared_sides']
            tf['solids'].append(sol); tf['rings'] += N; tf['shared_sides'] += sol['shared_sides']; tf['ties'] += sol['ties']
            lg = plt.imread(LOGO); la = fig.add_axes([0.90, 0.01, 0.09, 0.09 * 7.2 / 6.0]); la.imshow(lg); la.axis('off')
            fig.savefig(os.path.join(OUT, f'net-{t}-solid{si + 1}.png'), dpi=220, facecolor='white'); plt.close(fig)
        # 3D drawing of the finished tile (all solids in place) and, for two solids, drawn apart
        rgb = hex2rgb(COL[t]); tris = []
        for si, fids in enumerate(S): tris += tile_tris(faces, fids, rgb)
        v = View(18, -58)
        img, sc = render3d(tris, v, 1400, 1300)
        save_img(img, os.path.join(OUT, f'tile3d-{t}.png'))
        if len(S) > 1:
            tris2 = []
            for si, fids in enumerate(S):
                c = np.mean([cart(p) for i in fids for p in faces[i]['loops'][0]], 0); c[2] = 0
                tris2 += tile_tris(faces, fids, rgb, offset=c / np.linalg.norm(c) * 0.45)
            img, _ = render3d(tris2, v, 1400, 1300)
            save_img(img, os.path.join(OUT, f'tile3d-{t}-apart.png'))
        else:
            v2 = View(-20, 122); img, _ = render3d(tris, v2, 1400, 1300); save_img(img, os.path.join(OUT, f'tile3d-{t}-below.png'))
        facts[t] = tf
        print(t, json.dumps(tf, indent=1), flush=True)
    json.dump(facts, open(os.path.join(OUT, 'counts.json'), 'w'), indent=1)
