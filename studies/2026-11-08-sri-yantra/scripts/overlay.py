"""Overlay plates for paper #103 Version 2 (DICTO 9 Nov 2026: "they are all in the same colours and all beautiful, it seems
unclear"). Each variant yantra is drawn DOTTED in its own colour over the DICTO Yantra (GF1) drawn solid in faint grey, in the
same circle (diameter 1), with its name in large type and its shortcomings as a red note ON the image. Every note is checked
here from the stored coordinates (corner offsets from the circle, bindu incircle centre, odd-piece count via figure.py's face
arrangement) or quoted from Table 3 / README of this study; the script stops if a measured note is not true.
Also draws the overview "Which yantra is which" (each yantra small, solid in its colour, name, EXACT or COMPUTED badge).
usage: python3 overlay.py <outdir>      (writes overlay-*.png and which-yantra.png; prints the checks and a FINAL line)"""
import json, math, os, re, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from figure import val, segments, faces, area, corners_of, inside_tri

HERE = os.path.dirname(os.path.abspath(__file__)); FIG = os.path.join(HERE, '..', 'figures'); DAT = os.path.join(HERE, '..', 'data')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
RED = (193, 18, 31); GREY = (190, 190, 190); INK = (34, 30, 25); BG = (255, 253, 247)
APEX_OF = {1: 6, 2: 9, 4: 8, 5: 7, 6: 2, 8: 1, 9: 3}   # apex of t_i lies on the base of t_j (7 apex-on-base conditions)


def from_json(path, key):
    e = json.load(open(path))[key]
    f = lambda d: {int(k): val(x) for k, x in d.items()}
    return f(e['b']), f(e['w']), f(e['apex'])


def kulaichev():
    t = open(os.path.join(DAT, 'kulaichev-numeric-data.txt')).read()
    b = {int(i): float(x) for i, x in re.findall(r'\bb(\d) = ([0-9.]+)', t)}
    w = {int(i): float(x) for i, x in re.findall(r'\bw(\d) = ([0-9.]+)', t)}
    a = {i: b[j] for i, j in APEX_OF.items()}; a[3] = 1.0; a[7] = 0.0
    return b, w, a


Y = {  # key: (label, loader, colour, exact?)
    'GF1': ('The DICTO Yantra', lambda: from_json(os.path.join(FIG, 'golden_family.json'), 'GF1'), (184, 150, 46), True),
    'KRP': ("Kulaichev's yantra", kulaichev, (199, 21, 133), True),
    'R1': ('R1, in whole-number fractions', lambda: from_json(os.path.join(DAT, 'quadratic-examples.json'), 'R1'), (29, 78, 216), True),
    'Rh345': ('Rh345, the 3-4-5 rhombus', lambda: from_json(os.path.join(DAT, 'rhombus345-coordinates.json'), 'Rh345'), (160, 82, 45), True),
    'grid': ('The grid yantra', lambda: from_json(os.path.join(FIG, 'grid.json'), 'G1'), (11, 122, 117), True),
    'K1': ('K1, the Cleo-Octangula', lambda: from_json(os.path.join(FIG, 'kites.json'), 'K1'), (31, 111, 139), False),
    'V1': ('V1, K1 from a viewpoint', lambda: from_json(os.path.join(FIG, 'viewpoint.json'), 'V1'), (125, 60, 152), False),
    'PF2': ('PF2, the stella yantra', lambda: from_json(os.path.join(FIG, 'perfect.json'), 'PF2'), (42, 127, 63), False),
    'G1': ('G1, the gnomon yantra', lambda: from_json(os.path.join(FIG, 'gnomon.json'), 'G1'), (85, 85, 85), False),
    'E1': ('E1, the most even yantra', lambda: from_json(os.path.join(FIG, 'even.json'), 'E1'), (211, 84, 0), False),
}


def measure(b, w, a):
    """corner offsets from the circle (+ outside), bindu incircle centre offset and k, odd pieces by ring, tiny third-ring pieces"""
    off = {i: math.hypot(w[i], b[i] - 0.5) - 0.5 for i in (1, 9)}
    H = a[1] - b[5]; h = w[1] * (a[1] - b[5]) / (a[1] - b[1])
    r = h * H / (h + math.hypot(h, H)); dc = b[5] + r - 0.5
    pts, fs = faces(segments(b, w, a)); odd = []
    for f in fs:
        poly = [pts[k] for k in f]; ar = area(poly)
        if ar >= -1e-14: continue
        cx = sum(p[0] for p in poly) / len(poly); cy = sum(p[1] for p in poly) / len(poly)
        cnt = sum(inside_tri((cx, cy), b, w, a, i) for i in range(1, 10))
        if cnt % 2: odd.append((corners_of(poly), cnt, -ar, (cx, cy)))
    rings = [sum(1 for o in odd if o[1] == c) for c in (1, 3, 5, 7, 9)]
    third = sorted([o for o in odd if o[1] == 5], key=lambda o: o[2])
    return dict(off=off, bindu=dc, k=r / 0.5, rings=rings, n=len(odd), tiny=third[:2] if rings[2] > 10 else [],
                t3tip=a[3], tri=sum(1 for o in odd if len(o[0]) == 3))


def font(p, s): return ImageFont.truetype(p, s)


def draw_lines(dr, b, w, a, X, Yd, col, width, dotted=False, dot=11.0):
    for (p, q, i) in segments(b, w, a):
        P, Q = (X(p[0]), Yd(p[1])), (X(q[0]), Yd(q[1]))
        if not dotted:
            dr.line([P, Q], fill=col, width=width); continue
        L = math.hypot(Q[0] - P[0], Q[1] - P[1]); n = max(1, int(L / dot))
        for k in range(n + 1):
            x, y = P[0] + (Q[0] - P[0]) * k / n, P[1] + (Q[1] - P[1]) * k / n
            dr.ellipse([x - width, y - width, x + width, y + width], fill=col)


def circle(dr, X, Yd, col, width):
    dr.ellipse([X(-0.5), Yd(0), X(0.5), Yd(1)], outline=col, width=width)


def wrap(dr, text, f, maxw):
    out, line = [], ''
    for word in text.split(' '):
        t = (line + ' ' + word).strip()
        if dr.textlength(t, font=f) <= maxw: line = t
        else: out.append(line); line = word
    return out + [line]


def plate(key, notes, rings_marks, out):
    """one overlay plate, drawn at 2x and reduced (anti-aliasing)"""
    s = 2; Wd = 1200 * s; D = 1000 * s; top = 190 * s; side = (Wd - D) // 2
    label, load, col, exact = Y[key]
    b0, w0, a0 = Y['GF1'][1](); b, w, a = load()
    lo = min(0.0, min(a.values())); hi = max(1.0, max(a.values()))
    X = lambda x: side + (x + 0.5) * D; Yd = lambda d: top + (d - lo) * D
    fn = font(FONT, 40 * s); fb = font(BOLD, 64 * s); fs_ = font(FONT, 30 * s)
    probe = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    lines = [l for n in notes for l in wrap(probe, n, fn, Wd - 2 * side - 40 * s)]
    H = int(top + (hi - lo) * D + 60 * s + 56 * s * len(lines) + 70 * s)
    im = Image.new('RGB', (Wd, H), BG); dr = ImageDraw.Draw(im)
    bx = Wd - side - 230 * s; sz = 64
    while dr.textlength(label, font=font(BOLD, sz * s)) > bx - side - 30 * s: sz -= 2
    dr.text((side, 30 * s + (64 - sz) * s // 2), label, font=font(BOLD, sz * s), fill=INK)
    dr.rounded_rectangle([bx, 44 * s, bx + 230 * s, 90 * s], radius=8 * s, fill=(201, 152, 26) if exact else (140, 140, 150))
    dr.text((bx + 115 * s, 67 * s), 'EXACT' if exact else 'COMPUTED', font=font(BOLD, 28 * s), fill='white', anchor='mm')
    short = label.split(',')[0]; short = short[0].lower() + short[1:] if short.startswith('The ') else short
    dr.text((side, 122 * s), 'solid grey: the DICTO Yantra;   dotted, in colour: ' + short, font=fs_, fill=(80, 80, 80))
    circle(dr, X, Yd, (90, 90, 90), 3 * s)
    draw_lines(dr, b0, w0, a0, X, Yd, GREY, 4 * s)
    draw_lines(dr, b, w, a, X, Yd, col, 3 * s, dotted=True, dot=12 * s)
    for (x, d, rr) in rings_marks:
        R = rr * D
        dr.ellipse([X(x) - R, Yd(d) - R, X(x) + R, Yd(d) + R], outline=RED, width=4 * s)
    y = Yd(hi) + 40 * s
    for l in lines:
        dr.text((side, y), l, font=fn, fill=RED); y += 56 * s
    dr.text((Wd - side, H - 50 * s), 'DICTO · dictospheres.com', font=fs_, fill=(110, 110, 110), anchor='ra')
    im.resize((Wd // s, H // s), Image.LANCZOS).save(out)


def overview(out):
    s = 2; cols, rows = 5, 2; tw, th = 520 * s, 700 * s; D = 440 * s; head = 130 * s
    im = Image.new('RGB', (cols * tw + 40 * s, head + rows * th), BG); dr = ImageDraw.Draw(im)
    dr.text((30 * s, 30 * s), 'Which yantra is which', font=font(BOLD, 66 * s), fill=INK)
    dr.text((im.width - 30 * s, 50 * s), 'DICTO · dictospheres.com', font=font(FONT, 30 * s), fill=(150, 110, 20), anchor='ra')
    order = ['GF1', 'KRP', 'R1', 'Rh345', 'grid', 'K1', 'V1', 'PF2', 'G1', 'E1']
    sub = {'GF1': 'Cleo-Antonius; 43 pieces', 'KRP': 'equal great triangles; 45', 'R1': 'every corner a fraction',
           'Rh345': "DICTO's rhombus, 3-4-5; 45", 'grid': 'one slope; 37 pieces', 'K1': 'Cleo-Icos over stella',
           'V1': 'every condition met', 'PF2': 'stella exact below', 'G1': 'repeats in its own bindu',
           'E1': 'pieces most even; 43'}
    for n, key in enumerate(order):
        label, load, col, exact = Y[key]; b, w, a = load()
        c, r = n % cols, n // cols; ox, oy = 20 * s + c * tw, head + r * th
        if key == 'GF1': dr.rectangle([ox + 6 * s, oy, ox + tw - 6 * s, oy + th - 20 * s], outline=(201, 152, 26), width=8 * s)
        lo = min(0.0, min(a.values())); hi = max(1.0, max(a.values())); sc = D / (hi - lo)
        X = lambda x: ox + tw / 2 + x * sc; Yd = lambda d: oy + 30 * s + (d - lo) * sc
        circle(dr, X, Yd, (90, 90, 90), 2 * s)
        draw_lines(dr, b, w, a, X, Yd, col, 3 * s)
        ty = oy + 30 * s + D + 22 * s
        for l in wrap(dr, label, font(BOLD, 34 * s), tw - 50 * s):
            dr.text((ox + 25 * s, ty), l, font=font(BOLD, 34 * s), fill=INK); ty += 42 * s
        dr.text((ox + 25 * s, ty + 4 * s), sub[key], font=font(FONT, 27 * s), fill=(70, 70, 70)); ty += 46 * s
        dr.rounded_rectangle([ox + 25 * s, ty, ox + 25 * s + 190 * s, ty + 40 * s], radius=8 * s,
                             fill=(201, 152, 26) if exact else (140, 140, 150))
        dr.text((ox + 25 * s + 95 * s, ty + 20 * s), 'EXACT' if exact else 'COMPUTED', font=font(BOLD, 26 * s), fill='white', anchor='mm')
    im.resize((im.width // s, im.height // s), Image.LANCZOS).save(out)


def main(outdir):
    os.makedirs(outdir, exist_ok=True); M = {}
    for k in Y:
        M[k] = measure(*Y[k][1]())
        m = M[k]
        print(f"{k:6s} odd pieces {m['n']} rings {m['rings']} (triangles {m['tri']}); t1/t9 corner offset "
              f"{m['off'][1]:+.4f} {m['off'][9]:+.4f}; bindu centre offset {m['bindu']:+.2e}; k {m['k']:.5f}; t3 tip {m['t3tip']:.4f}"
              + (f"; two smallest third-ring areas {[round(t[2], 7) for t in m['tiny']]}" if m['tiny'] else ''))
    ok = True
    def need(c, why):
        nonlocal ok
        if not c: ok = False; print('NOTE NOT TRUE:', why)
    g = M['GF1']; need(g['n'] == 43 and abs(g['bindu']) < 1e-12 and max(map(abs, g['off'].values())) < 1e-12, 'GF1 reference')
    corner_rings = lambda b, w: [(s_ * w[i], b[i], 0.03) for i in (1, 9) for s_ in (1, -1)]
    tiny_rings = lambda m: [(sx * abs(t[3][0]), t[3][1], 0.03) for t in m['tiny'] for sx in (1,)] + \
                           [(-t[3][0], t[3][1], 0.03) for t in m['tiny']]
    P = {}
    m = M['KRP']; need(m['n'] == 45 and m['rings'][2] == 12, 'KRP 45')
    P['KRP'] = (['45 pieces, not 43 (ringed: the third ring\'s two smallest pieces); 28 sandhis, not 24'], [])
    m = M['R1']; need(m['off'][1] < -1e-3 and m['off'][9] < -1e-3 and abs(m['bindu']) > 1e-3, 'R1')
    P['R1'] = ([f"small corners inside the circle (t1 by {-m['off'][1]:.3f}, t9 by {-m['off'][9]:.3f}); bindu not centred "
                f"(off by {abs(m['bindu']):.3f})", "t1's base at 3.3/48, not 6/48 as traditionally drawn"], corner_rings(*Y['R1'][1]()[:2]))
    m = M['Rh345']; need(m['n'] == 45 and abs(abs(m['bindu']) - 2.36e-5) < 0.01e-5, 'Rh345')
    P['Rh345'] = (['45 pieces, not 43 (ringed: the third ring\'s two smallest pieces); 28 sandhis', 'bindu off centre by 2.36·10⁻⁵'], [])
    m = M['grid']; need(m['t3tip'] > 1 and m['n'] == 37, 'grid')
    P['grid'] = ([f"t3's tip outside the circle (depth {m['t3tip']:.3f}); 37 pieces, not 43; no corner touches (Theorem 7)"],
                 [(0.0, m['t3tip'], 0.035)])
    m = M['K1']; need(m['n'] == 43 and abs(m['bindu']) > 1e-4, 'K1')
    P['K1'] = ([f"bindu not centred (off by {abs(m['bindu']):.3f} of the diameter)", 'COMPUTED: exact form not found'], [])
    m = M['V1']; need(m['n'] == 43 and abs(m['bindu']) < 1e-9, 'V1')
    P['V1'] = (['COMPUTED: exact form not found', 'slopes 0.7336 / 0.7364: no longer the solids\' own (2/φ², 1/√2)'], [])
    m = M['PF2']; need(m['n'] == 43 and abs(m['bindu']) < 1e-9, 'PF2')
    P['PF2'] = (['COMPUTED: exact form not found', 'upper slope 0.6959 has no parent solid (Proposition 8)'], [])
    m = M['E1']; need(m['n'] == 43 and m['off'][1] < 0 and m['off'][9] < 0 and abs(m['bindu']) > 1e-3, 'E1')
    P['E1'] = ([f"small corners inside the circle (t1 by {-m['off'][1]:.3f}, t9 by {-m['off'][9]:.3f}); 28 sandhis, not 24",
                f"bindu not centred (off by {abs(m['bindu']):.3f}); COMPUTED: exact form not found"], corner_rings(*Y['E1'][1]()[:2]))
    for k in ('KRP', 'Rh345'):
        P[k] = (P[k][0], tiny_rings(M[k]))
    for k, (notes, marks) in P.items():
        plate(k, notes, marks, os.path.join(outdir, f'overlay-{k}.png')); print('wrote', f'overlay-{k}.png:', ' | '.join(notes))
    overview(os.path.join(outdir, 'which-yantra.png')); print('wrote which-yantra.png')
    print('FINAL ok' if ok else 'FINAL FAIL: a note is not true')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(FIG, 'overlays'))
