# Fable 2026-10-17 — pieces, checks and SVG renders for DICTO's flat-cut scutoid group (from fable_build.py parameters). FLOAT.
import json, sys, itertools, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
sys.argv = sys.argv[:1] + sys.argv[1:]
import fable_build as FB
P = np.array(json.load(open(sys.argv[1]))['p']); OUT = sys.argv[2]; H = float(sys.argv[3]) if len(sys.argv) > 3 else 0
X, L, c, t = FB.unpack(P); n = FB.n; bits = FB.bits
MARK = 'DICTO · dictospheres.com'
BG = '#f4f1ea'; INK = '#2a2218'; GOLD = '#e8b84a'; BLUE = '#7fb3d5'
COLS = ['#e07a5f', '#81b29a', '#f2cc8f', '#3d85c6', '#c77dff', '#90be6d', '#f9844a', '#4d908e']
# ---------- group: one image of each cell, chosen compact ----------
def img(k, m, q): return X[k] + m * L[0] + q * L[1]
cen = X.mean(0); grp = []
for k in range(n):
    best = min(((np.linalg.norm(img(k, m, q) - cen), m, q) for m in range(-3, 4) for q in range(-3, 4)))
    grp.append((k, best[1], best[2]))
_ord = sorted(range(n), key=lambda k: (-bits[k], k)); NUM = {_ord[i]: i + 1 for i in range(n)}
def cell3d(k, m, q, Hh):
    xi = img(k, m, q); A = []; B = []
    for kk in range(n):
        for mm in range(m - 3, m + 4):
            for qq in range(q - 3, q + 4):
                if kk == k and mm == m and qq == q: continue
                xj = img(kk, mm, qq)
                if np.linalg.norm(xj - xi) > 3.5: continue
                # 2x.(xj-xi) + z(t_i - t_j) <= |xj|^2-|xi|^2 + c_j - c_i   (z in [-1,1] model units; physical z = z*Hh/2)
                A.append([2 * (xj - xi)[0], 2 * (xj - xi)[1], (t[k] - t[kk]) * 2 / Hh]); B.append(xj @ xj - xi @ xi + c[kk] - c[k])
    A += [[0, 0, 1], [0, 0, -1]]; B += [Hh / 2, Hh / 2]
    A = np.array(A); B = np.array(B)
    hs = HalfspaceIntersection(np.c_[A, -B], np.r_[xi, 0]); V = hs.intersections
    V = np.unique(np.round(V, 10), axis=0); hull = ConvexHull(V)
    faces = []
    for i in range(len(A)):
        on = np.abs(V @ A[i] - B[i]) < 1e-7
        if on.sum() < 3: continue
        Q = V[on]; nrm = A[i] / np.linalg.norm(A[i]); o = Q.mean(0)
        u = np.cross(nrm, [1, 0, 0] if abs(nrm[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(nrm, u)
        Q = Q[np.argsort(np.arctan2((Q - o) @ w, (Q - o) @ u))]
        # drop duplicate points
        keep = [Q[0]]
        for v in Q[1:]:
            if np.linalg.norm(v - keep[-1]) > 1e-8: keep.append(v)
        if np.linalg.norm(keep[0] - keep[-1]) < 1e-8: keep.pop()
        if len(keep) >= 3: faces.append((nrm, np.array(keep)))
    area = sum(np.linalg.norm(sum(np.cross(F[j], F[(j + 1) % len(F)]) for j in range(len(F)))) / 2 for _, F in faces)
    vol = hull.volume; psi = np.pi ** (1 / 3) * (6 * vol) ** (2 / 3) / area
    return dict(faces=faces, vol=vol, area=area, psi=psi, V=V)
def end_poly(cell, top):
    for nrm, F in cell['faces']:
        if abs(nrm[2] - (1 if top else -1)) < 1e-9: return F
def angles2(F):
    m = len(F); out = []
    for j in range(m):
        u = F[j - 1] - F[j]; w = F[(j + 1) % m] - F[j]; out.append(np.degrees(np.arccos(np.clip(u @ w / np.linalg.norm(u) / np.linalg.norm(w), -1, 1))))
    return np.array(out)
def scan_H():
    res = []
    for Hh in np.arange(0.6, 2.61, 0.05):
        ps = [cell3d(*g, Hh)['psi'] for g in grp]; res.append((min(ps), Hh))
    return max(res)
if __name__ == '__main__':
    if not H:
        mp, H = scan_H(); print('best H (layer height, seed spacing ~1)', round(H, 3), 'min psi', round(mp, 4))
    cells = [cell3d(*g, H) for g in grp]
    rep = []
    for i, (g, C) in enumerate(zip(grp, cells)):
        T = end_poly(C, True); Bt = end_poly(C, False)
        nt, nb = len(T), len(Bt); at, ab = angles2(T[:, :2]), angles2(Bt[:, :2])
        kinds = sorted(len(F) for _, F in C['faces'])
        rep.append(dict(piece=NUM[g[0]], top=nt, bottom=nb, psi=round(C['psi'], 4), vol=round(C['vol'], 4), faces=len(C['faces']), face_sizes=kinds,
                        top_angles=[round(x, 1) for x in at], bottom_angles=[round(x, 1) for x in ab]))
        print(rep[-1])
    sig = [np.round(sorted(np.linalg.norm(F[(j + 1) % len(F)] - F[j]) for _, F in C['faces'] for j in range(len(F))), 5) for C in cells]
    for i in range(n):
        for j in range(i + 1, n):
            if np.allclose(sig[i], sig[j], atol=1e-4): print('same edge lengths (congruent or mirror): pieces', NUM[grp[i][0]], NUM[grp[j][0]])
    vt = sum(C['vol'] for C in cells); cellarea = abs(np.linalg.det(L)); print('group volume', vt, 'period prism volume', cellarea * H)
    json.dump(dict(H=H, pieces=rep, group=[list(map(int, g)) for g in grp], group_volume=vt, period_volume=cellarea * H,
                   note='FLOAT: Laguerre cells of tuned float parameters; faces planar by construction'), open(OUT + '.json', 'w'), indent=1)

# ---------------- drawing ----------------
def svg_head(w, h, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="Georgia, serif">',
            f'<style>.t{{font-size:24px;font-weight:600;fill:{INK}}}.s{{font-size:15px;fill:#5b5040}}.n{{font-size:15px;font-weight:700;fill:{INK}}}.m{{font-size:15px;fill:#6b604f;font-style:italic}}</style>',
            f'<rect width="100%" height="100%" fill="{BG}"/>', f'<text x="24" y="38" class="t">{title}</text>']
def svg_tail(w, h, L_):
    return L_ + [f'<text x="{w - 20}" y="{h - 16}" text-anchor="end" class="m">{MARK}</text>', '</svg>']
def merge(Pp):
    Q = [Pp[0]]
    for v in Pp[1:]:
        if np.linalg.norm(v - Q[-1]) > 1e-7: Q.append(v)
    if np.linalg.norm(Q[0] - Q[-1]) < 1e-7: Q.pop()
    return np.array(Q)
def latt(k, m, q):
    j0, i0 = divmod(k, FB.a); return (i0 + m * FB.a + q * FB.b, j0 + q * FB.d)
def shade(col, f):
    r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)
    return '#%02x%02x%02x' % tuple(int(min(255, max(0, v * f))) for v in (r, g, b))
def patterns(fn):
    W, Hs = 1500, 640; out = svg_head(W, Hs, 'DICTO scutoid group — the two flat cuts (and the middle)')
    panels = [(1, 'TOP cut: pieces 1–4 are pentagons'), (0, 'MIDDLE: every piece a hexagon'), (-1, 'BOTTOM cut: pieces 5–8 are pentagons')]
    order = sorted(range(n), key=lambda k: (-bits[k], k))   # numbers: T cells 1-4, B cells 5-8
    num = {order[i]: i + 1 for i in range(n)}
    sc = 62; cen2 = np.mean([img(*g) for g in grp], 0)
    for pi, (z, ttl) in enumerate(panels):
        ox, oy = 250 + pi * 500, 340
        out.append(f'<text x="{ox}" y="92" text-anchor="middle" class="t" style="font-size:19px">{ttl}</text>')
        out.append(f'<clipPath id="c{pi}"><rect x="{ox - 235}" y="110" width="470" height="470" rx="14"/></clipPath><g clip-path="url(#c{pi})">')
        for k in range(n):
            for m in range(-3, 4):
                for q in range(-2, 3):
                    ingrp = (k, m, q) in [tuple(g) for g in grp]
                    Pp = merge(FB.polygon(latt(k, m, q), P, z)); S = (Pp - cen2) * sc
                    if np.abs(S).max() > 330: continue
                    five = len(Pp) == 5
                    col = GOLD if five else ('#cfe0ec' if not ingrp else '#9cc3dd')
                    if not ingrp: col = shade(col, 1.0) if not five else '#f0d9a2'
                    pts = ' '.join(f'{ox + x:.1f},{oy - y:.1f}' for x, y in S)
                    out.append(f'<polygon points="{pts}" fill="{col}" stroke="{INK}" stroke-width="{2.4 if ingrp else 1.1}" opacity="{1 if ingrp else .55}"/>')
                    if ingrp:
                        cx, cy = S.mean(0); out.append(f'<text x="{ox + cx:.1f}" y="{oy - cy + 5:.1f}" text-anchor="middle" class="n">{num[k]}</text>')
        # four-piece corners
        for zz in (z,):
            if zz == 0: continue
            for e in FB.M[zz]:
                for m in range(-2, 3):
                    for q in range(-2, 3):
                        A_ = e[0]; sh = (A_[0] + m * FB.a + q * FB.b, A_[1] + q * FB.d)
                        v = FB.vert([sh, (e[1][0] + m * FB.a + q * FB.b, e[1][1] + q * FB.d), (e[2][0] + m * FB.a + q * FB.b, e[2][1] + q * FB.d)], X, L, c, t, zz)
                        S = (v - cen2) * sc
                        if np.abs(S).max() < 330: out.append(f'<circle cx="{ox + S[0]:.1f}" cy="{oy - S[1]:.1f}" r="5" fill="#c0392b"/>')
        out.append('</g>')
    out.append(f'<text x="24" y="{Hs - 46}" class="s">Same number = same piece. Gold = pentagon, blue = hexagon. Red dot = corner where 4 pieces meet (the scutoid’s Y lies exactly on the cut).</text>')
    out.append(f'<text x="24" y="{Hs - 24}" class="s">Bold = one group of 8 pieces; faint = neighbouring groups (the same group repeated). Pieces 1–4: pentagon on top, hexagon below; 5–8 the other way round.</text>')
    open(fn, 'w').write('\n'.join(svg_tail(W, Hs, out))); return num
VIEW = None
def proj(p, el=28, az=-35, s=90):
    a_, e_ = np.radians(az), np.radians(el)
    Rz = np.array([[np.cos(a_), -np.sin(a_), 0], [np.sin(a_), np.cos(a_), 0], [0, 0, 1]])
    q = Rz @ p; y2 = q[1] * np.sin(e_) + q[2] * np.cos(e_); dep = q[1] * np.cos(e_) - q[2] * np.sin(e_)
    return np.array([q[0] * s, -y2 * s]), dep
def viewdir(el=28, az=-35):
    a_, e_ = np.radians(az), np.radians(el); Rz = np.array([[np.cos(a_), -np.sin(a_), 0], [np.sin(a_), np.cos(a_), 0], [0, 0, 1]])
    return Rz.T @ np.array([0, -np.cos(e_), np.sin(e_)])   # direction toward viewer
def draw_solids(items, ox, oy, s, el=28, az=-35, sw=1.6):
    vd = viewdir(el, az); light = np.array([-.4, -.5, .8]); light /= np.linalg.norm(light); polys = []
    for C, col, off in items:
        cen_ = np.mean([F.mean(0) for _, F in C['faces']], 0) + off; dep = proj(cen_, el, az, s)[1]
        for nrm, F in C['faces']:
            if nrm @ vd <= 1e-9: continue
            G = F + off; sp = [proj(v, el, az, s) for v in G]
            muted = col.startswith('#') and col not in COLS
            fc = GOLD if (abs(nrm[2]) > .999 and len(F) == 5) else (BLUE if abs(nrm[2]) > .999 else col)
            if muted and abs(nrm[2]) > .999: fc = '#ecd9a8' if len(F) == 5 else '#c9dbe7'
            if len(F) == 3: fc = '#c0392b'
            f = .62 + .45 * max(0, nrm @ light) if el > 0 else .62 + .45 * max(0, nrm @ (light * [1, 1, -1]))
            polys.append((dep, ' '.join(f'{ox + x:.1f},{oy + y:.1f}' for (x, y), _ in sp), shade(fc, f)))
    polys.sort(key=lambda r: -r[0])
    return [f'<polygon points="{p}" fill="{f}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>' for _, p, f in polys]
def piece_col(k, num): return COLS[num[k] - 1]

def draw_all(prefix, H, cells, rep):
    num = patterns(prefix + '-cuts.svg')
    gc = np.mean([img(*g) for g in grp], 0); gc3 = np.r_[gc, 0]
    # whole group, assembled and exploded
    W, Hs = 1500, 720; out = svg_head(W, Hs, f'One DICTO scutoid group: 8 pieces, flat top and bottom (layer height {H:.2f}, seed spacing 1)')
    it = [(C, piece_col(g[0], num), -gc3) for g, C in zip(grp, cells)]
    out += draw_solids(it, 380, 420, 135)
    it2 = []
    for g, C in zip(grp, cells):
        cc = C['V'].mean(0); dlt = np.r_[(cc[:2] - gc) * 0.55, 0]; it2.append((C, piece_col(g[0], num), -gc3 + dlt))
    out += draw_solids(it2, 1110, 420, 108)
    for g, C in zip(grp, cells):
        cc = C['V'].mean(0) + np.r_[(C['V'].mean(0)[:2] - gc) * 0.55, 0] - gc3 + np.array([0, 0, H / 2 + .25]); (x, y), _ = proj(cc, s=108)
        out.append(f'<text x="{1110 + x:.0f}" y="{420 + y:.0f}" text-anchor="middle" class="n" style="font-size:20px">{num[g[0]]}</text>')
    out.append(f'<text x="380" y="{Hs - 60}" text-anchor="middle" class="s">assembled</text><text x="1110" y="{Hs - 60}" text-anchor="middle" class="s">pulled apart sideways</text>')
    out.append(f'<text x="24" y="{Hs - 24}" class="s">Gold = pentagon end, blue = hexagon end, red = the small triangle face (the scutoid face) whose tip is the Y on the cut.</text>')
    open(prefix + '-group.svg', 'w').write('\n'.join(svg_tail(W, Hs, out)))
    # tiling: 3x3 groups per layer, 2 layers stacked straight, layers lifted apart a little
    W, Hs = 1500, 900; out = svg_head(W, Hs, 'Groups fill space: side by side in a layer, layers stacked straight up')
    it = []
    for m in (-1, 0, 1):
        for q in (-1, 0, 1):
            sh = m * L[0] + q * L[1]
            for g, C in zip(grp, cells):
                col = piece_col(g[0], num) if (m, q) == (0, 0) else '#%02x%02x%02x' % tuple(int(.35 * int(piece_col(g[0], num)[1 + 2 * i:3 + 2 * i], 16) + .65 * (0xd9, 0xd2, 0xc4)[i]) for i in range(3))
                it.append((C, col, np.r_[sh - gc, 0]))
    out += draw_solids(it, 520, 470, 58, sw=1.0)
    it = []
    for lay in (0, 1, 2):
        for g, C in zip(grp, cells): it.append((C, piece_col(g[0], num), np.r_[-gc, lay * (H + 0.7)]))
    out += draw_solids(it, 1210, 560, 70, sw=1.2)
    out.append(f'<text x="520" y="{Hs - 70}" text-anchor="middle" class="s">one layer: 9 groups (centre group in full colour)</text>')
    out.append(f'<text x="1210" y="{Hs - 70}" text-anchor="middle" class="s">one group, three layers (lifted apart to show the flat joins)</text>')
    out.append(f'<text x="24" y="{Hs - 24}" class="s">Every group is the same 8 pieces, moved without turning. The top of one layer sits flat on the bottom of the next; nothing crosses between layers.</text>')
    open(prefix + '-tiling.svg', 'w').write('\n'.join(svg_tail(W, Hs, out)))
    # pieces
    W, Hs = 1500, 900; out = svg_head(W, Hs, 'The 8 pieces (each: pentagon at one end, hexagon at the other)')
    out.append(f'<text x="24" y="66" class="s">Pieces 1–4 seen from above (pentagon on top), pieces 5–8 seen from below (pentagon underneath). Each view faces the red triangle.</text>')
    order = sorted(range(n), key=lambda k: num[grp[k][0]])
    for slot, gi in enumerate(order):
        g = grp[gi]; C = cells[gi]; r = rep[gi]; cx = 190 + (slot % 4) * 370; cy = 260 + (slot // 4) * 370
        flip = bits[g[0]] == 0
        Cc = dict(faces=[(nn, F - C['V'].mean(0)) for nn, F in C['faces']])
        el = 24 if not flip else -24; tri = [nn for nn, F in C['faces'] if len(F) == 3][0]
        az = max(range(0, 360, 3), key=lambda a_: tri @ viewdir(el, a_) + .35 * viewdir(el, a_) @ np.array([-.5, 0, 0]))
        out += draw_solids([(Cc, piece_col(g[0], num), np.zeros(3))], cx, cy, 125, el=el, az=az)
        out.append(f'<text x="{cx}" y="{cy + 150}" text-anchor="middle" class="n">piece {num[g[0]]}: top {r["top"]}, bottom {r["bottom"]}</text>')
        out.append(f'<text x="{cx}" y="{cy + 172}" text-anchor="middle" class="s">ψ = {r["psi"]:.3f} · {r["faces"]} faces</text>')
    out.append(f'<text x="24" y="{Hs - 24}" class="s">ψ = sphericity, a yardstick only (cube 0.806, regular hexagonal prism of best height ≈ 0.85). Gold = pentagon end, blue = hexagon end, red = triangle face.</text>')
    open(prefix + '-pieces.svg', 'w').write('\n'.join(svg_tail(W, Hs, out)))

if __name__ == '__main__':
    draw_all(OUT, H, cells, [r for r in rep])
