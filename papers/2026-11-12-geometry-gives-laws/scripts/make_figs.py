"""Figures for the draft "Geometry Gives Laws" (aim 2). DICTO · dictospheres.com
Every figure is drawn from the study data or the study formulas (studies/2026-11-10-canonical-sweep, 2026-11-12-solids-canonical,
2026-11-12-pds-hopscotch-line, 2026-11-12-yantra-regions-canonical); each figure checks its numbers against the study values first.
Run with Python 3 (numpy, scipy, matplotlib, mpmath, sympy) from the k-research checkout: python make_figs.py"""
import sys, os, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial import HalfspaceIntersection

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'figures')
ST = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'studies'))
MARK = 'DICTO · dictospheres.com'
GOLD, DARK, RED, BLUE, GREY = '#b8962e', '#6b5310', '#b02020', '#1f5fa8', '#777777'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.titlesize': 9, 'axes.labelsize': 8.5})
fails = 0


def check(c, msg):
    global fails
    fails += 0 if c else 1
    print(('ok   ' if c else 'FAIL ') + msg, flush=True)


def mark(fig):
    fig.text(0.995, 0.004, MARK, ha='right', va='bottom', fontsize=6.5, color='#8a7a50')


def save(fig, name):
    mark(fig)
    fig.savefig(os.path.join(OUT, name), dpi=220)
    plt.close(fig)
    print('wrote', name, flush=True)


# ------------------------------------------------------------------ 3D helpers
def solid_faces(H, b):
    """H x <= b, origin inside. Returns vertices and faces (ordered polygons)."""
    hs = HalfspaceIntersection(np.hstack([H, -b[:, None]]), np.zeros(H.shape[1]))
    V = []
    for p in hs.intersections:
        if not any(np.linalg.norm(p - q) < 1e-9 for q in V): V.append(p)
    V = np.array(V); F = []
    for n, c in zip(H, b):
        on = [v for v in V if abs(n @ v - c) < 1e-9]
        if len(on) < 3: continue
        on = np.array(on); cen = on.mean(0); nn = n / np.linalg.norm(n)
        e1 = on[0] - cen; e1 /= np.linalg.norm(e1); e2 = np.cross(nn, e1)
        ang = np.arctan2((on - cen) @ e2, (on - cen) @ e1)
        F.append((on[np.argsort(ang)], nn))
    return V, F


def draw(ax, F, colour, alpha=1.0, shift=np.zeros(3), edge=DARK, lw=0.6):
    light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    base = np.array(matplotlib.colors.to_rgb(colour))
    polys, cols = [], []
    for P, n in F:
        polys.append(P + shift)
        s = 0.55 + 0.45 * max(0.0, n @ light)
        cols.append((*np.clip(base * s + 0.08, 0, 1), alpha))
    pc = Poly3DCollection(polys, facecolors=cols, edgecolors=edge, linewidths=lw)
    ax.add_collection3d(pc)


def tidy3d(ax, lim, elev=18, azim=32):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.set_axis_off()


# ------------------------------------------------------------------ Figure 1: the cube-octahedron line
def fig_line():
    import sympy as sp
    mu = sp.symbols('mu', positive=True)
    pieces = [(0, 1, 48 / mu ** 3), (1, 2, 48 / mu ** 2), (2, 3, 24 / mu), (3, sp.oo, sp.Integer(8))]
    for (a, b, f), (_, _, g) in zip(pieces, pieces[1:]):
        same = sp.simplify(f.subs(mu, b) - g.subs(mu, b)) == 0
        kink = sp.simplify(sp.diff(f, mu).subs(mu, b) - sp.diff(g, mu).subs(mu, b)) != 0
        check(same and kink, f'Fig 1: Omega(S;0) continuous at the wall mu = {b} with a kink (slopes {sp.diff(f, mu).subs(mu, b)}, {sp.diff(g, mu).subs(mu, b)})')
    # chunk 2 bridge, numerically: 3! vol(polar of S(mu)) at the centre equals the piece, at mu = 0.7, 1.5, 2.5, 3.5
    H = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]] +
                 [[sx, sy, sz] for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)], float)
    fig = plt.figure(figsize=(7.4, 5.0))
    samples = [(0.7, 'μ = 0.7: octahedron μ·P*'), (1.5, 'μ = 1.5'), (2.5, 'μ = 2.5'), (3.5, 'μ = 3.5: cube P')]
    for k, (m, lab) in enumerate(samples):
        b = np.array([1.0] * 6 + [m] * 8)
        V, F = solid_faces(H, b)
        from scipy.spatial import ConvexHull
        pol = ConvexHull(np.array([n / c for n, c in zip(H, b)]))          # polar about the centre: hull of the normals over distances
        val = 6 * pol.volume
        expect = float([p for p in pieces if p[0] <= m < (p[1] if p[1] != sp.oo else 1e9)][0][2].subs(mu, m))
        check(abs(val - expect) < 1e-9, f'Fig 1: bridge at mu = {m}: 3! vol(polar) = {val:.10f} = {expect:.10f}')
        ax = fig.add_axes([0.02 + k * 0.245, 0.50, 0.23, 0.46], projection='3d')
        draw(ax, F, GOLD if m > 1 else '#8a8fbf')
        tidy3d(ax, 1.25)
        ax.set_title(lab, fontsize=8, pad=-4)
    ax = fig.add_axes([0.09, 0.09, 0.86, 0.38])
    xs = np.linspace(0.62, 4.2, 800)
    f = sp.lambdify(mu, sp.Piecewise(*[(p[2], mu < (p[1] if p[1] != sp.oo else 1e9)) for p in pieces]))
    ax.semilogy(xs, [f(x) for x in xs], color=DARK, lw=1.6)
    for w in (1, 2, 3):
        ax.axvline(w, color=GREY, ls='--', lw=0.8)
        ax.text(w, 260, f'wall {w}', ha='center', va='bottom', fontsize=7, color=GREY)
    ax.axvline(math.sqrt(3), color=GOLD, lw=1.2)
    ax.text(math.sqrt(3) + 0.03, 120, 'turn fixed point √3', color=DARK, fontsize=7.5)
    for x0, txt in [(0.78, '48/μ³'), (1.25, '48/μ²'), (2.45, '24/μ'), (3.55, '8')]:
        ax.text(x0, f(x0) * 1.25, txt, fontsize=8, color='k')
    ax.set_xlim(0.62, 4.2); ax.set_ylim(5, 400)
    ax.set_xlabel('μ (slider)'); ax.set_ylabel('Ω(S(μ); centre) = 3!·vol(polar)')
    save(fig, 'fig1-cube-line.png')


# ------------------------------------------------------------------ Figure 2: Cleo-Icos + Antonius + Cleo-Icos
def fig_join():
    phi = (1 + 5 ** 0.5) / 2
    a, b, c = np.array([0, 1, phi]), np.array([0, -1, phi]), np.array([phi, 0, 1])
    check(all(abs(np.linalg.norm(p - q) - 2) < 1e-12 for p, q in [(a, b), (a, c), (b, c)]), 'Fig 2: a, b, c are the corners of one icosahedron face (edges 2)')
    M = np.array([a, b, c]).T; Mi = np.linalg.inv(M)
    def piece(lo, hi):                       # rhombohedron points s a + t b + u c with 0 <= s, t, u <= 1 and lo <= s + t + u <= hi
        Hs = [Mi[i] for i in range(3)] + [-Mi[i] for i in range(3)]
        bs = [1, 1, 1, 0, 0, 0]
        s = Mi.sum(0)
        Hs += [s, -s]; bs += [hi, -lo]
        H = np.array(Hs); bb = np.array(bs, float)
        cen = M @ np.array([(lo + hi) / 6] * 3)
        V, F = solid_faces(H, bb - H @ cen)
        return V + cen, [(P + cen, n) for P, n in F]
    det = abs(np.linalg.det(M))
    vols = []
    for lo, hi in [(0, 1), (1, 2), (2, 3)]:
        from scipy.spatial import ConvexHull
        V, F = piece(lo, hi); vols.append(ConvexHull(V).volume)
    check(abs(vols[0] - det / 6) < 1e-9 and abs(vols[1] - 4 * det / 6) < 1e-9 and abs(vols[2] - det / 6) < 1e-9,
          f'Fig 2: volumes Cleo-Icos, Antonius, Cleo-Icos = 1/6, 4/6, 1/6 of the rhombohedron ({vols[0]:.6f}, {vols[1]:.6f}, {vols[2]:.6f})')
    check(len(piece(1, 2)[1]) == 8 and len(piece(1, 2)[0]) == 6, 'Fig 2: Antonius has 6 corners and 8 faces')
    d = (a + b + c) / np.linalg.norm(a + b + c); mid = (a + b + c) / 2
    fig = plt.figure(figsize=(7.4, 3.6))
    ax = fig.add_axes([0.0, 0.02, 0.48, 0.92], projection='3d'); ax.computed_zorder = False
    for (lo, hi), col in zip([(0, 1), (1, 2), (2, 3)], ['#c9a74a', '#6f8fc8', '#c9a74a']):
        V, F = piece(lo, hi); draw(ax, F, col, alpha=0.55, shift=-mid, lw=0.5)
    for tri in ([a, b, c], [a + b, b + c, a + c]):
        T = np.array(tri + [tri[0]]) - mid
        ax.plot(T[:, 0], T[:, 1], T[:, 2], color=RED, lw=2.2, zorder=20)
    tidy3d(ax, 2.0, elev=14, azim=-58)
    ax.set_title('golden prolate rhombohedron: two inner planes (red)', fontsize=8)
    ax = fig.add_axes([0.5, 0.02, 0.48, 0.92], projection='3d')
    for (lo, hi), col, sh in zip([(0, 1), (1, 2), (2, 3)], ['#c9a74a', '#6f8fc8', '#c9a74a'], [-1.1, 0, 1.1]):
        V, F = piece(lo, hi); draw(ax, F, col, alpha=0.95, shift=-mid + sh * d, lw=0.6)
    tidy3d(ax, 2.4, elev=14, azim=-58)
    ax.set_title('Cleo-Icos + Antonius + Cleo-Icos', fontsize=8)
    save(fig, 'fig2-join.png')


# ------------------------------------------------------------------ Figure 3: three lines, three near misses
def fig_near():
    import sympy as sp
    mu = sp.symbols('mu', positive=True); r5 = sp.sqrt(5)
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.75))
    plt.subplots_adjust(left=0.07, right=0.985, bottom=0.2, top=0.86, wspace=0.42)
    # (a) cube line: order-4 anisotropy / c0 on (1, 2) and (2, 3); Mahler product on (1, 2), (2, 3)
    an = [(1, 2, 2 * (mu ** 4 + 2 * mu ** 3 + mu ** 2 - 4 * mu - 14) / (9 * mu ** 4)), (2, 3, (3 * mu ** 4 + 2 * mu ** 3 - 2 * mu ** 2 - 8 * mu - 12) / (9 * mu ** 4))]
    Mh = [(1, 2, 32 * (-2 * mu ** 3 + 9 * mu ** 2 - 9 * mu + 3) / (3 * mu ** 2)), (2, 3, 16 * (mu ** 3 - 9 * mu ** 2 + 27 * mu - 21) / (3 * mu))]
    z = sp.nsolve(mu ** 4 + 2 * mu ** 3 + mu ** 2 - 4 * mu - 14, mu, 1.7)
    m_max = sp.nsolve(2 * mu ** 3 - 9 * mu + 6, mu, 1.6)
    check(abs(z - 1.692590) < 1e-6 and abs(m_max - 1.631223) < 1e-6, f'Fig 3a: roundest point {float(z):.6f}, Mahler maximum {float(m_max):.6f} (study: 1.692590, 1.631223)')
    check(sp.simplify(an[0][2].subs(mu, sp.sqrt(3)) - 4 * (sp.sqrt(3) - 1) / 81) == 0, 'Fig 3a: anisotropy at sqrt3 = 4(sqrt3 - 1)/81 (study)')
    ax = axs[0]
    for lo, hi, e in an:
        xs = np.linspace(max(lo, 1.45), min(hi, 2.05), 300); ax.plot(xs, [float(e.subs(mu, x)) for x in xs], color=DARK, lw=1.5)
    ax.axhline(0, color='k', lw=0.5)
    ax.axvline(math.sqrt(3), color=GOLD, lw=1.2); ax.plot([float(z)], [0], 'o', color=RED, ms=4)
    ax.axvline(float(m_max), color=GREY, ls=':', lw=1)
    ax.text(float(z) - 0.012, -0.02, 'roundest\n1.6926', ha='right', fontsize=6.5, color=RED)
    ax.text(math.sqrt(3) + 0.015, -0.065, '√3 = 1.7321', fontsize=6.5, color=DARK)
    ax.text(float(m_max) - 0.012, 0.075, 'Mahler max\n1.6312', ha='right', fontsize=6.5, color=GREY)
    ax.set_xlim(1.45, 2.05); ax.set_ylim(-0.08, 0.11)
    ax.set_title('(a) cube line: 4th-order anisotropy', fontsize=7.8); ax.set_xlabel('μ')
    # (b) icosahedral line, chamber (phi^2, (5+sqrt5)/2): order-6 anisotropy / c0 = k Q(nu)
    nu = sp.symbols('nu')
    Q = (nu ** 6 + (1 - r5 / 5) * nu ** 5 + (-sp.Rational(17, 5) + 8 * r5 / 5) * nu ** 4 + (-sp.Rational(58, 5) + 26 * r5 / 5) * nu ** 3
         + (sp.Rational(114, 5) - 51 * r5 / 5) * nu ** 2 + (-sp.Rational(47, 5) + 21 * r5 / 5) * nu - sp.Rational(4698, 5) + 2101 * r5 / 5)
    k = (640 - 128 * r5) / 9 / (420 - 180 * r5)
    g = sp.lambdify(mu, (k * Q).subs(nu, 1 / mu), 'mpmath')
    fp = sp.sqrt((25 + 11 * r5) / 6)
    zi = sp.nsolve((k * Q).subs(nu, 1 / mu), mu, 2.89, prec=30)
    check(abs(float(g(float(fp))) - 0.000431717368330967) < 1e-12 and abs(zi - sp.Float('2.891792659030825043', 30)) < 1e-15,
          f'Fig 3b: anisotropy/c0 at the fixed point {float(g(float(fp))):.15f}; zero at {float(zi):.12f} (study: 0.000431717368330967, 2.891792659030825043)')
    ax = axs[1]
    xs = np.linspace(2.80, 2.97, 300); ax.plot(xs, [float(g(x)) * 1e3 for x in xs], color=DARK, lw=1.5)
    ax.axhline(0, color='k', lw=0.5); ax.axvline(float(fp), color=GOLD, lw=1.2); ax.plot([float(zi)], [0], 'o', color=RED, ms=4)
    ax.text(float(zi) + 0.004, -0.75, 'roundest\n2.8918', fontsize=6.5, color=RED)
    ax.text(float(fp) - 0.004, -1.6, 'fixed point\n2.8751', ha='right', fontsize=6.5, color=DARK)
    ax.set_title('(b) icosahedral line: 6th order (×10³)', fontsize=7.8); ax.set_xlabel('μ')
    # (c) PDS line, truncated 600-cell hop: B(mu), the order-12 tone of Omega
    d = json.load(open(os.path.join(ST, '2026-11-12-pds-hopscotch-line', 'data', 'pds-line.json')))
    hop = d['hops']['truncated 600-cell hop']
    B = sp.sympify(hop['B'], locals={'mu': mu})
    Bf = sp.lambdify(mu, B, 'mpmath')
    import mpmath as mp
    mp.mp.dps = 40
    r = mp.sqrt((7 + 3 * mp.sqrt(5)) / 16)
    mO = mp.mpf('0.921449634428905791812131090257'); ms = mp.mpf('0.924138673238867458601238076667')
    check(abs(Bf(r) - mp.mpf(hop['B_at_fixed_point'])) < 1e-20 and abs(Bf(mO)) < 1e-15 * abs(Bf(r)),
          f'Fig 3c: B(r) = {mp.nstr(Bf(r), 12)} (study -4.29713341975); B(mu_Omega) = {mp.nstr(Bf(mO), 3)}')
    ax = axs[2]
    xs = np.linspace(0.9055, 0.945, 300); ax.plot(xs, [float(Bf(x)) for x in xs], color=DARK, lw=1.5)
    ax.axhline(0, color='k', lw=0.5); ax.axvline(float(r), color=GOLD, lw=1.2)
    ax.plot([float(mO)], [0], 'o', color=RED, ms=4); ax.plot([float(ms)], [0], 's', color=BLUE, ms=4)
    ax.axvline(float(r ** 2 / ms), color=GREY, ls=':', lw=1)
    yl = ax.get_ylim()
    ax.text(float(mO) - 0.001, yl[0] + 0.12 * (yl[1] - yl[0]), 'silent Ω\n0.92145', ha='right', fontsize=6.5, color=RED)
    ax.text(float(ms) + 0.0006, yl[0] + 0.55 * (yl[1] - yl[0]), '19-design\n0.92414', fontsize=6.5, color=BLUE)
    ax.text(float(r) + 0.0035, yl[0] + 0.82 * (yl[1] - yl[0]), 'r = 0.92561\n(dotted: r²/μ*)', fontsize=6.5, color=DARK)
    ax.set_title('(c) 600-cell line: tone B(μ) of Ω', fontsize=7.8); ax.set_xlabel('μ')
    save(fig, 'fig3-near-misses.png')


# ------------------------------------------------------------------ Figure 4: the DICTO Yantra's form: marmas and sandhis
def fig_yantra():
    sys.path.insert(0, os.path.join(ST, '2026-11-12-yantra-regions-canonical', 'scripts'))
    import yantra_regions as yr
    logs = []
    K = yr.Ctx(80)
    Y, ok0 = yr.load_gf1(K, logs.append)
    check(ok0, 'Fig 4: DICTO Yantra rebuilt from its degree-160 polynomial at 80 digits')
    ok, res = yr.analyse(K, Y, 'GF1', logs.append)
    A = yr.arrangement(K, Y)
    odd = [f for f in A['faces'] if f['c'] % 2]
    rows = res['rows']
    marmas = [r[4] for r in rows if r[0] == 'marma']; sandhis = [r[4] for r in rows if r[0] == 'sandhi']
    centre = float(res['bindu'][1])
    check(len(odd) == 43 and all(len(f['V']) == 3 for f in odd) and len(marmas) == 18 and len(sandhis) == 24 and abs(centre + 86.08) < 0.01,
          f'Fig 4: 43 regions, all triangles; {len(marmas)} marmas, {len(sandhis)} sandhis; Omega_Y(0, 1/2) = {centre:.4f} (study -86.08)')
    tri = [[(float(p[0]), float(p[1])) for p in f['V']] for f in odd]
    lines = [tuple(float(v) for v in l) for l in A['lines']]
    def omega_Y(x, y):
        tot = 0.0
        for (a, b, c) in tri:
            D = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            d0 = (b[0] - x) * (c[1] - y) - (b[1] - y) * (c[0] - x)
            d1 = (x - a[0]) * (c[1] - a[1]) - (y - a[1]) * (c[0] - a[0])
            d2 = (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0])
            tot = tot + np.sign(D) * D * D / (d0 * d1 * d2)
        return tot
    check(abs(omega_Y(0.0, 0.5) - centre) < 1e-6, f'Fig 4: float form at the centre {omega_Y(0.0, 0.5):.6f} agrees with the 80-digit value')
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.85))
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.03, top=0.92, wspace=0.03)
    th = np.linspace(0, 2 * np.pi, 400)
    for ax in axs:
        ax.plot(0.5 * np.cos(th), 0.5 + 0.5 * np.sin(th), color=GREY, lw=0.7)
        for s in A['S']:
            ax.plot([float(s[0][0]), float(s[1][0])], [float(s[0][1]), float(s[1][1])], color='k', lw=0.45)
        ax.set_aspect('equal'); ax.set_xlim(-0.53, 0.53); ax.set_ylim(-0.03, 1.03); ax.set_axis_off()
    ax = axs[0]
    for t in tri:
        ax.fill([p[0] for p in t], [p[1] for p in t], color='#e8d49a', lw=0)
    ax.scatter([p[0] for p in sandhis], [p[1] for p in sandhis], s=9, color=BLUE, zorder=5, label='24 sandhis: residue 2')
    ax.scatter([p[0] for p in marmas], [p[1] for p in marmas], s=34, facecolors='none', edgecolors=RED, linewidths=1.1, zorder=6,
               label='18 marmas: double zeros')
    ax.plot([0], [0.5], '+', color='k', ms=7)
    ax.annotate('centre (+): Ω$_Y$ = −86.08', xy=(0, 0.5), xytext=(-0.52, 0.97), fontsize=7, arrowprops=dict(arrowstyle='-', color=GREY, lw=0.6))
    ax.legend(loc='lower center', fontsize=6.8, frameon=False, ncol=2, bbox_to_anchor=(0.5, -0.04))
    ax.set_title('(a) 43 regions (gold), marmas and sandhis', fontsize=8)
    ax = axs[1]
    n = 520
    X, Yg = np.meshgrid(np.linspace(-0.53, 0.53, n), np.linspace(-0.03, 1.03, n))
    with np.errstate(all='ignore'):
        Om = omega_Y(X, Yg)
        P = np.ones_like(X)
        for l in lines: P = P * (l[0] * X + l[1] * Yg + l[2])
        N = Om * P
    ax.contour(X, Yg, np.sign(N), levels=[0], colors=['#2a7a3a'], linewidths=0.8)
    ax.scatter([p[0] for p in marmas], [p[1] for p in marmas], s=34, facecolors='none', edgecolors=RED, linewidths=1.1, zorder=6)
    ax.set_title('(b) the zero curve N = 0 (green; numerical sketch)', fontsize=8)
    save(fig, 'fig4-yantra-form.png')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ['line', 'join', 'near', 'yantra']
    for k, w in enumerate(which):
        {'line': fig_line, 'join': fig_join, 'near': fig_near, 'yantra': fig_yantra}[w]()
        print(f'PROGRESS {(k + 1) / len(which):.2f} {w}', flush=True)
    print('FINAL ok' if fails == 0 else f'FINAL FAIL ({fails} checks failed)')
