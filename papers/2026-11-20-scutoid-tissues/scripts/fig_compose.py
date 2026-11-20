# DICTO · dictospheres.com — compose Figures 1 to 5 from the shots of fig_scenes.py (renders/<fig>/p<i>.png) and its labels
# and sections (renders/<fig>.json), in the house look of paper #43 (the fig_compose.py of the Dehn Canon paper: dark warm
# ground, bold title and grey subtitle inside the image, bold label and grey second line under each panel, the DICTO mark).
# Graphs only as small strips (Matplotlib). Usage: python3 fig_compose.py SWEEP_JSON      (sweep.json of the null-model study)
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'renders'); OUT = os.path.join(H, '..', 'figures')
DATA = os.path.join(H, '..', 'data')
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans'; f = lambda s, b=False: ImageFont.truetype(F + ('-Bold' if b else '') + '.ttf', int(s))
INK, MUTE, BG, RULE = (238, 230, 214), (176, 165, 148), (20, 15, 11), (92, 82, 68)
K = 2; PX = 1600
MARK = 'DICTO · dictospheres.com'
hexc = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
CREAM, TAUPE, AMBER = '#d2c3a0', '#7c6d5a', '#c99a45'
EV = {'birth': '#f2ead8', 'swap': AMBER, 'death': '#76869c', 'neighbour': '#4a4239'}
BORN, DIES, BOTH = '#d6c69e', '#6c7d93', '#b9b2a3'
OTHER = '#3b342c'


def fit(d, txt, fo, w):
    while d.textlength(txt, font=fo) > w and fo.size > 14 * K: fo = ImageFont.truetype(fo.path, fo.size - 2)
    return fo


def ctext(d, x, y, txt, fo, col, w):
    fo = fit(d, txt, fo, w); d.text((x - d.textlength(txt, font=fo) / 2, y), txt, font=fo, fill=col); return fo


def paste(im, path, x, y, cell, crop=None):
    p = Image.open(path).convert('RGBA'); bb = p.getbbox()
    assert bb and bb[0] > 2 and bb[1] > 2 and bb[2] < PX - 2 and bb[3] < PX - 2, f'{path}: solid touches the shot edge {bb}'
    p = p.resize((cell, cell), Image.LANCZOS); im.paste(p, (x, y), p)


def head(d, W, title, sub):
    d.text((80 * K, 46 * K), title, font=f(60 * K, True), fill=INK); d.text((80 * K, 122 * K), sub, font=fit(d, sub, f(30 * K), W - 160 * K), fill=MUTE)


def mark(d, W, Hh):
    d.text((W - 80 * K - d.textlength(MARK, font=f(24 * K)), Hh - 56 * K), MARK, font=f(24 * K), fill=MUTE)


def save(im, name):
    im.save(os.path.join(OUT, name), optimize=True); print(name, im.size)


def swatch(d, x, y, col, txt, fo, outline=None, ball=False):
    if ball: d.ellipse((x + 14 * K, y + 2 * K, x + 40 * K, y + 28 * K), fill=col, outline=outline, width=2 * K)
    else: d.rounded_rectangle((x, y + 6 * K, x + 54 * K, y + 26 * K), radius=5 * K, fill=col, outline=outline, width=2 * K)
    d.text((x + 66 * K, y), txt, font=fo, fill=INK); return x + 66 * K + d.textlength(txt, font=fo) + 44 * K


def tiling(im, polys, x, y, side, edge_hi=None):
    """2D sections (coordinates in [-1, 1]², y up) drawn in a square of side px at (x, y); polys = [(poly, fill, outline, width)].
    edge_hi: segments drawn on top in amber."""
    d = ImageDraw.Draw(im); s = side / 2
    T = lambda P: [(x + s + p[0] * s, y + s - p[1] * s) for p in P]
    for P, fill, ol, w in polys: d.polygon(T(P), fill=hexc(fill), outline=None)
    for P, fill, ol, w in sorted(polys, key=lambda q: q[3]):
        Q = T(P); d.line(Q + Q[:1], fill=hexc(ol), width=w, joint='curve')
    for a, b in (edge_hi or []): d.line(T([a, b]), fill=hexc(AMBER), width=7 * K)
    d.rectangle((x, y, x + side, y + side), outline=RULE, width=2 * K)


def shared(P1, P2):
    P1, P2 = np.array(P1), np.array(P2)
    sh = [p for p in P1 if np.min(np.linalg.norm(P2 - p, axis=1)) < 1e-6]
    assert len(sh) == 2, 'two cells share one edge'
    return sh


# ---------- Figure 1: a scutoid ----------
def scutoid():
    J = json.load(open(os.path.join(R, 'scutoid.json'))); nb, nt = J['sides']
    cell, sl, gap = 760 * K, 560 * K, 70 * K
    W = cell + 2 * sl + 2 * gap + 160 * K; top = 230 * K; Hh = top + cell + 250 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'A scutoid', 'A cell between two planes whose top and bottom have different numbers of sides · Gómez-Gálvez et al. 2018')
    paste(im, f'{R}/scutoid/p0.png', 80 * K, top, cell)
    s = cell / PX; L = J['labels']; bb = Image.open(f'{R}/scutoid/p0.png').getbbox()
    for key, txt, yy in (('top', f'top: {nt} sides', top + bb[1] * s - 52 * K), ('bottom', f'bottom: {nb} sides', top + bb[3] * s + 14 * K)):
        px, py = L[key]; fo = f(27 * K, True); w = d.textlength(txt, font=fo)
        d.text((80 * K + px * s - w / 2, yy), txt, font=fo, fill=INK)
    px, py = L['corner']; d.text((80 * K + px * s + 26 * K, top + py * s - 2 * K), 'the swap corner', font=f(25 * K), fill=hexc(AMBER))
    ctext(d, 80 * K + cell / 2, top + cell + 10 * K, f'A scutoid: {nb} sides below, {nt} above', f(34 * K, True), INK, cell)
    ctext(d, 80 * K + cell / 2, top + cell + 56 * K, 'amber: the wall it gains, a triangle from the corner up', f(26 * K), MUTE, cell)
    ROLE = {'scutoid': CREAM, 'meet': '#a8966f', 'part': TAUPE, 'other': OTHER}
    for i, (nm, title, sub) in enumerate((('bottom', 'The bottom plane', 'the pair that parts still touches'),
                                          ('top', 'The top plane', 'the scutoid and its partner now touch'))):
        x = 80 * K + cell + gap + i * (sl + gap); y = top + (cell - sl) / 2
        polys = [(P['poly'], ROLE[P['role']], '#efe6d2' if P['role'] == 'scutoid' else '#15100c', (6 if P['role'] == 'scutoid' else 3) * K)
                 for P in J['slices'][nm]]
        pair = ('part', 'part') if nm == 'bottom' else ('scutoid', 'meet')
        A = [P['poly'] for P in J['slices'][nm] if P['role'] == pair[0]]; B = [P['poly'] for P in J['slices'][nm] if P['role'] == pair[1]]
        hi = [shared(A[0], B[0])] if nm == 'top' else [shared(A[0], A[1])]
        tiling(im, polys, int(x), int(y), sl, edge_hi=hi)
        ctext(d, x + sl / 2, top + cell + 10 * K, title, f(34 * K, True), INK, sl + gap)
        ctext(d, x + sl / 2, top + cell + 56 * K, sub, f(26 * K), MUTE, sl + gap)
    fo = f(25 * K); x = 80 * K; y = Hh - 120 * K
    for col, txt in ((CREAM, 'the scutoid'), ('#a8966f', 'its partner: they meet at the swap'), (TAUPE, 'the pair that parts'), (AMBER, 'the contact that changes')):
        x = swatch(d, x, y, hexc(col), txt, fo)
    mark(d, W, Hh); save(im, 'fig-scutoid.png')


# ---------- Figure 2: a block of the moving tiling ----------
def block():
    FS = json.load(open(os.path.join(DATA, 'fig-scenes.json')))['figures']['fig2']
    cell = 1000 * K; side = 760 * K
    W = cell + side + 120 * K; top = 220 * K; Hh = top + cell + 120 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'A moving tiling in space-time', 'Each cell a tube, time upward · the block cut into three spans of time and pulled apart, so its sections show')
    paste(im, f'{R}/block/p0.png', 80 * K, top, cell)
    x0 = 80 * K + cell - 40 * K; y = top + 60 * K
    d.text((x0, y), 'Cells by their fate in the block', font=f(36 * K, True), fill=INK); y += 70 * K
    fo = f(27 * K)
    for col, txt in ((BORN, f'born in the block: {FS["born"]}'), (DIES, f'dying in the block: {FS["dies"]}'),
                     (BOTH, f'born and dying in it: {FS["both"]}'), ('#7d6f5c', f'passing through: {FS["through"]}')):
        swatch(d, x0, y, hexc(col), txt, fo); y += 54 * K
    y += 40 * K; d.text((x0, y), 'Corners by their event', font=f(36 * K, True), fill=INK); y += 70 * K
    for k, txt in (('birth', f'birth (index 1): {FS["births"]}'), ('swap', f'swap (index 2): {FS["swaps"]}'), ('death', f'death (index 3): {FS["deaths"]}')):
        swatch(d, x0, y, hexc(EV[k]), txt, fo, ball=True); y += 54 * K
    y += 40 * K; d.text((x0, y), 'Theorem 1(b), cell by cell', font=f(36 * K, True), fill=INK); y += 64 * K
    for t in (f'{FS["births"]} births = {FS["births"]} cells with their', 'lowest corner in the block',
              f'{FS["deaths"]} deaths = {FS["deaths"]} highest corners',
              f'{FS["swaps"]} swaps = {FS["corners"]} corners − {FS["births"]} − {FS["deaths"]}'):
        d.text((x0, y), t, font=f(27 * K), fill=MUTE); y += 42 * K
    # the time arrow
    ax = 80 * K + 30 * K; d.line((ax, top + cell - 120 * K, ax, top + 120 * K), fill=MUTE, width=3 * K)
    d.polygon([(ax, top + 100 * K), (ax - 12 * K, top + 130 * K), (ax + 12 * K, top + 130 * K)], fill=MUTE)
    tim = Image.new('RGBA', (300 * K, 40 * K), (0, 0, 0, 0)); ImageDraw.Draw(tim).text((0, 0), 'time', font=f(28 * K), fill=MUTE)
    tim = tim.rotate(90, expand=True); im.paste(tim, (int(ax - 50 * K), int(top + cell / 2 - 150 * K)), tim)
    mark(d, W, Hh); save(im, 'fig-block.png')


# ---------- Figure 3: birth, swap, death ----------
def corners():
    J = json.load(open(os.path.join(R, 'corners.json'))); cell, gap, ins = 640 * K, 60 * K, 290 * K
    W = 3 * cell + 2 * gap + 160 * K; top = 220 * K; Hh = top + cell + 140 * K + ins + 130 * K + 160 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'Birth, swap and death at a corner', 'The four cells round one corner of space-time, cut out by a small box · time upward · the plane just before and just after')
    TXT = {'birth': ('Birth: index 1', 'one edge goes down; a three-sided cell appears'),
           'swap': ('Swap: index 2', 'two edges go down; one pair parts, the other meets'),
           'death': ('Death: index 3', 'three edges go down; a three-sided cell vanishes')}
    for i, c in enumerate(J):
        x = 80 * K + i * (cell + gap); paste(im, f'{R}/corners/p{i}.png', x, top, cell)
        ctext(d, x + cell / 2, top + cell + 6 * K, TXT[c['kind']][0], f(34 * K, True), INK, cell + gap)
        ctext(d, x + cell / 2, top + cell + 52 * K, TXT[c['kind']][1], f(25 * K), MUTE, cell + gap)
        y = top + cell + 120 * K
        for j, nm in enumerate(('before', 'after')):
            xx = x + cell / 2 - ins - 20 * K + j * (ins + 40 * K)
            polys = [(P['poly'], P['col'], '#15100c', 3 * K) for P in c['secs'][nm]]
            hi = []
            if c['kind'] == 'swap':
                pairs = {}
                for P in c['secs'][nm]: pairs.setdefault(P['col'], []).append(P['poly'])
                hi = [shared(*pairs[CREAM if nm == 'after' else TAUPE])]
            tiling(im, polys, int(xx), int(y), ins, edge_hi=hi)
            ctext(d, xx + ins / 2, y + ins + 8 * K, 'just before' if nm == 'before' else 'just after', f(25 * K), MUTE, ins + 40 * K)
    fo = f(25 * K)
    for row, items in enumerate((((BORN, 'the cell born'), (DIES, 'the cell dying'), ('#a8967a', 'other cells, see-through in 3D')),
                                 ((CREAM, 'the pair that meets'), (TAUPE, 'the pair that parts'), (AMBER, 'the wall of the meeting pair; the contact that changes')))):
        x = 80 * K; y = Hh - 190 * K + row * 50 * K
        for col, txt in items: x = swatch(d, x, y, hexc(col), txt, fo)
    mark(d, W, Hh); save(im, 'fig-corners.png')


# ---------- Figure 4: one cell, swept in two directions ----------
def tube():
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    FT = json.load(open(os.path.join(DATA, 'fig-tube.json'))); L = json.load(open(os.path.join(R, 'tube.json')))
    cell, gap, ph = 820 * K, 120 * K, 300 * K
    W = 2 * cell + gap + 160 * K; top = 290 * K; Hh = top + cell + ph + 230 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'One cell, swept in two directions', 'A dodecahedral cell of the 120-cell as a tube in space-time: born at its lowest corner, dead at its highest, its section changing at every corner between')
    fo = f(26 * K); x = 80 * K; y = 186 * K
    for col, txt in ((EV['birth'], 'birth (lowest corner)'), (AMBER, 'swap'), (EV['neighbour'], 'a neighbour born or dying'), (EV['death'], 'death (highest corner)')):
        x = swatch(d, x, y, hexc(col), txt, fo, outline=(150, 140, 125) if col == EV['neighbour'] else None, ball=True)
    MC = {'birth': EV['birth'], 'death': EV['death'], 'swap': AMBER, 'neighbour born': EV['neighbour'], 'neighbour dies': EV['neighbour']}
    for k, dd in enumerate(FT['directions']):
        x0 = 80 * K + k * (cell + gap); cs = int(cell * 0.80); ys = top + (cell - cs) // 2
        paste(im, f'{R}/tube/p{k}.png', x0, ys, cs); s = cs / PX; lx = x0 + cs + 24 * K
        for n, px, py in L[k]['sections']:
            d.line((x0 + px * s + 10 * K, ys + py * s, lx - 12 * K, ys + py * s), fill=RULE, width=2 * K)
            d.text((lx, ys + py * s - 16 * K), f'{n} sides', font=f(26 * K), fill=hexc('#d9c7a3'))
        # the strip: sides against time
        fig = plt.figure(figsize=(cell / 200, ph / 200), dpi=200); fig.patch.set_alpha(0)
        ax = fig.add_axes([0.13, 0.30, 0.84, 0.66]); ax.set_facecolor('none')
        T, seq = dd['time'], dd['sides']; xs, ys = [], []
        for i in range(len(seq)): xs += [T[i], T[i + 1]]; ys += [seq[i], seq[i]]
        ax.plot(xs, ys, color='#d9c7a3', lw=3)
        for fr in dd['levels']: ax.axvline(fr, color='#5c5244', lw=1.5, ls='--', zorder=0)
        for v, t in zip(dd['order'], T):
            kd = dd['kind'][v]; ax.plot(t, 1.7, 'o', ms=13 if kd in ('birth', 'death') else 10, color=MC[kd], mec='#a09684' if 'neighbour' in kd else '#140f0b', mew=1.2, clip_on=False)
        ax.set_ylim(1.0, 10.2); ax.set_xlim(-0.02, 1.02); ax.set_yticks([3, 5, 7, 9]); ax.set_xticks([])
        ax.tick_params(colors='#b0a594', labelsize=22, width=1.5)
        for s_ in ax.spines.values(): s_.set_color('#5c5244'); s_.set_linewidth(1.5)
        ax.set_ylabel('sides', color='#b0a594', fontsize=24); ax.set_xlabel('time, from birth to death', color='#b0a594', fontsize=24)
        tmp = os.path.join(R, f'tube-strip{k}.png'); fig.savefig(tmp, transparent=True); plt.close(fig)
        g = Image.open(tmp).convert('RGBA'); im.paste(g, (x0, top + cell + 10 * K), g)
        c = dd['counts']
        ctext(d, x0 + cell / 2, top + cell + ph + 30 * K, f'Direction {k + 1}', f(34 * K, True), INK, cell)
        ctext(d, x0 + cell / 2, top + cell + ph + 76 * K, f"1 birth, {c['swap']} swaps, {c['neighbour born']} neighbours born, {c['neighbour dies']} dying, 1 death", f(26 * K), MUTE, cell)
    mark(d, W, Hh); save(im, 'fig-tube.png')


# ---------- Figure 5: the law at a glance ----------
def law(sweep):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    SW = json.load(open(sweep)); RP = SW['random_simple_polytopes']
    chk = {c[0]: c[1] for c in SW['checks']}
    assert chk.get('PV 3D contact changes per birth 4.7669 +- 0.0006 vs 24pi^2/35 - 2 = 4.7677') is True
    FS = json.load(open(os.path.join(DATA, 'fig-scenes.json')))['figures']['fig5']
    cell, gap, gw = 600 * K, 40 * K, 820 * K
    W = 2 * cell + gap + 70 * K + gw + 160 * K; top = 220 * K; Hh = top + cell + 230 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, 'The law at a glance: swaps per birth = ⟨F⟩/2 − 3', 'Two space-filling tilings by convex cells, a corner cut away · F, the number of walls of a cell')
    for i, (t, sub) in enumerate((('Poisson–Voronoi', '⟨F⟩ = 2 + 48π²/35 ≈ 15.54 · 24π²/35 − 2 ≈ 4.7677'),
                                  ('bcc: truncated octahedra', 'F = 14 · 14/2 − 3 = 4'))):
        x = 80 * K + i * (cell + gap); paste(im, f'{R}/law/p{i}.png', x, top, cell)
        ctext(d, x + cell / 2, top + cell + 6 * K, t, f(34 * K, True), INK, cell + gap)
        ctext(d, x + cell / 2, top + cell + 52 * K, sub, f(25 * K), MUTE, cell + gap)
    pv = 24 * np.pi ** 2 / 35 - 2
    fig = plt.figure(figsize=(gw / 200, cell / 200), dpi=200); fig.patch.set_alpha(0)
    ax = fig.add_axes([0.20, 0.17, 0.77, 0.78]); ax.set_facecolor('none'); mc = '#b0a594'
    n = [r['cells'] for r in RP]; v = [r['h2_over_h1'] for r in RP]; e = [r['err'] for r in RP]
    ax.axhline(pv, color='#eee6d6', lw=2); ax.axhline(4, color='#5c5244', lw=2, ls='--')
    ax.errorbar(n, v, yerr=e, fmt='o', ms=13, color='#cdc3b0', mec='#140f0b', ecolor='#cdc3b0', capsize=4)
    xo = 3e6; ax.errorbar([xo], [4.7669], yerr=[0.0006], fmt='D', ms=16, color=AMBER, mec='#140f0b')
    ax.set_xscale('log'); ax.set_xlim(50, 1e7); ax.set_ylim(3.9, 4.88)
    ax.set_xticks([1e2, 1e3, 1e4, 1e5, xo]); ax.set_xticklabels(['10²', '10³', '10⁴', '10⁵', 'open'])
    ax.minorticks_off()
    ax.text(70, pv + 0.025, '24π²/35 − 2', color='#eee6d6', fontsize=24)
    ax.text(70, 4.02, 'bcc: 4', color=mc, fontsize=24)
    ax.annotate('space-time\nsimulation', (xo, 4.7669), (1.6e5, 4.42), color=AMBER, fontsize=22, ha='center', arrowprops=dict(arrowstyle='-', color=AMBER))
    ax.text(700, 4.14, 'random simple\n4-polytopes,\nby cells', color=mc, fontsize=22)
    ax.tick_params(colors=mc, labelsize=22, width=1.5)
    for s_ in ax.spines.values(): s_.set_color('#5c5244'); s_.set_linewidth(1.5)
    ax.set_ylabel('swaps per birth', color=mc, fontsize=24)
    tmp = os.path.join(R, 'law-strip.png'); fig.savefig(tmp, transparent=True); plt.close(fig)
    g = Image.open(tmp).convert('RGBA'); x = 80 * K + 2 * cell + gap + 70 * K; im.paste(g, (x, top), g)
    ctext(d, x + gw / 2, top + cell + 6 * K, 'Poisson–Voronoi, closed and open', f(34 * K, True), INK, gw)
    ctext(d, x + gw / 2, top + cell + 52 * K, 'simulated 4.7669 ± 0.0006 against 24π²/35 − 2 = 4.7677', f(25 * K), MUTE, gw)
    mark(d, W, Hh); save(im, 'fig-law.png')


# ---------- Figure 6: the Sun's granules in space-time (study data) ----------
def sun():
    Z = np.load(os.path.join(DATA, 'sun-faces.npz')); up = float(Z['up']); dx, dt = float(Z['dx']), float(Z['dt'])
    N = int(Z['crop'][2]); T = Z['front'].shape[0]
    assert Z['top'].shape == (N, N) and Z['front'].shape == (T, N) and Z['side'].shape == (T, N) and T == 242
    allv = np.concatenate([Z[k].astype(np.float32).ravel() for k in ('top', 'mid', 'front', 'side')]) * up
    lo, hi = np.percentile(allv, 2), np.percentile(allv, 98)
    C0, C1, C2 = np.array(hexc('#2a1f17'), float), np.array(hexc('#806b50'), float), np.array(hexc('#f0e3c4'), float)
    def colour(a, shade=1.0):                              # downflow dark, zero mid, upflow light (a warm neutral ramp)
        v = a.astype(np.float32) * up; u = np.where(v < 0, -np.clip(v / lo, 0, 1), np.clip(v / hi, 0, 1))
        rgb = np.where(u[..., None] < 0, C1 + (C1 - C0) * u[..., None], C1 + (C2 - C1) * u[..., None]) * shade
        return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert('RGBA')
    cell, gap = 1000 * K, 140 * K
    W = 2 * cell + gap + 160 * K; top = 230 * K; Hh = top + cell + 230 * K
    im = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(im)
    head(d, W, "The Sun's granules in space-time", 'Vertical velocity 0.1 Mm below the surface in the Bifrost run en024048_hion (Carlsson et al. 2016) · rising gas light, sinking gas dark')
    m = colour(Z['mid']).resize((int(cell * 0.86), int(cell * 0.86)), Image.LANCZOS); mx, my = 80 * K + int(cell * 0.07), top + int(cell * 0.07)
    im.paste(m, (mx, my)); d.rectangle((mx, my, mx + m.size[0], my + m.size[1]), outline=RULE, width=2 * K)
    ctext(d, 80 * K + cell / 2, top + cell + 6 * K, 'One moment', f(34 * K, True), INK, cell)
    ctext(d, 80 * K + cell / 2, top + cell + 52 * K, f'{N * dx:.0f} Mm square, the middle of the run · each light patch a granule', f(25 * K), MUTE, cell)
    # the block: x to the right and down, y to the left and down, time up (an isometric drawing, three faces as affine images)
    c30, s30 = np.cos(np.radians(30)), 0.5; sc = cell * 0.40 / (N * c30); hT = cell * 0.46 / T
    X0 = 80 * K + cell + gap + cell / 2; Y0 = top + cell * 0.04
    P = lambda x, y, t: np.array([X0 + (x - (N - y)) * c30 * sc, Y0 + (x + (N - y)) * s30 * sc - t * hT + T * hT])
    def face(img, O, U, V):
        M = np.array([[U[0], V[0]], [U[1], V[1]]]); Mi = np.linalg.inv(M)
        a, b = Mi[0]; d_, e = Mi[1]; c = -(a * O[0] + b * O[1]); f_ = -(d_ * O[0] + e * O[1])
        out = img.transform((W, Hh), Image.AFFINE, (a, b, c, d_, e, f_), resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
        im.paste(out, (0, 0), out)
    Tf = np.flipud(Z['front'])                             # rows: last frame first, so time runs up the page
    Ts = np.flipud(Z['side'])
    face(colour(Tf, 0.80), P(0, 0, T), P(1, 0, T) - P(0, 0, T), P(0, 0, T - 1) - P(0, 0, T))
    face(colour(Ts, 0.62), P(N, 0, T), P(N, 1, T) - P(N, 0, T), P(N, 0, T - 1) - P(N, 0, T))
    face(colour(Z['top'], 1.0), P(0, 0, T), P(1, 0, T) - P(0, 0, T), P(0, 1, T) - P(0, 0, T))
    for a_, b_ in [((0, 0, T), (N, 0, T)), ((N, 0, T), (N, N, T)), ((N, N, T), (0, N, T)), ((0, N, T), (0, 0, T)),
                   ((0, 0, 0), (N, 0, 0)), ((N, 0, 0), (N, N, 0)), ((0, 0, 0), (0, 0, T)), ((N, 0, 0), (N, 0, T)), ((N, N, 0), (N, N, T))]:
        d.line([tuple(P(*a_)), tuple(P(*b_))], fill=(26, 20, 15), width=3 * K)
    pa, pb = P(0, 0, 0), P(0, 0, T); ax = pa[0] - 40 * K
    d.line((ax, pa[1], ax, pb[1] + 20 * K), fill=MUTE, width=3 * K); d.polygon([(ax, pb[1]), (ax - 11 * K, pb[1] + 28 * K), (ax + 11 * K, pb[1] + 28 * K)], fill=MUTE)
    lab = f'{(T - 1) * dt / 60:.0f} minutes'; tim = Image.new('RGBA', (int(d.textlength(lab, font=f(26 * K))) + 4, 36 * K), (0, 0, 0, 0))
    ImageDraw.Draw(tim).text((0, 0), lab, font=f(26 * K), fill=MUTE); tim = tim.rotate(90, expand=True)
    im.paste(tim, (int(ax - 48 * K), int((pa[1] + pb[1]) / 2 - tim.size[1] / 2)), tim)
    xc = P(N / 2, 0, 0); d.text((xc[0] - 110 * K, xc[1] + 10 * K), f'{N * dx:.0f} Mm', font=f(26 * K), fill=MUTE)
    ctext(d, X0, top + cell + 6 * K, f'{(T - 1) * dt / 60:.0f} minutes of space-time', f(34 * K, True), INK, cell)
    ctext(d, X0, top + cell + 52 * K, 'top: the last moment · sides: two cuts through time · each granule a tube, not convex', f(25 * K), MUTE, cell + gap)
    mark(d, W, Hh); save(im, 'fig-sun.png')


if __name__ == '__main__':
    scutoid(); block(); corners(); tube(); law(sys.argv[1]); sun()
    print('FINAL ok')
