"""Mock-up pages for the proposed "Dual-Pair Cycles" world (PROPOSAL ONLY, nothing is built): writes paper.html that composes the
real renders of mockup_render.py with UI drawn in HTML/CSS to match Polyhedraverse (colours sampled from the Golden Cut screenshots,
the ∞ player's own SVG and CSS from src/app/infinity-player.js, tokens from src/app/tokens.css). Printed with
~/work/cw-print/print.mjs (footer "mock-up, not built").
usage: python mockup_page.py <render dir (mockup-data.json, r-*.png)> <out folder> <logo png>
DICTO · dictospheres.com
"""
import os, sys, json, shutil, html
RD, OUT, LOGO = sys.argv[1:4]
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
for f in os.listdir(RD):
    if f.endswith('.png'): shutil.copy(os.path.join(RD, f), os.path.join(OUT, 'img', f))
shutil.copy(LOGO, os.path.join(OUT, 'img', 'dicto-logo.png'))
D = json.load(open(os.path.join(RD, 'mockup-data.json')))
E = html.escape

GOLDT, PALE = '#f4cb6a', '#b6f8a6'
INF_PATH = 'M100 45C126 9 186 9 186 45S126 81 100 45 14 9 14 45 74 81 100 45Z'

CSS = r"""
@page { size: A4; }
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, sans-serif; color: #1d1d24; background: #fff; }
.page { page-break-after: always; break-after: page; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 22px; margin: 0 0 2px; }
.sub { color: #555; font-size: 12.5px; margin: 0 0 8px; }
.meta { border-top: 2px solid #d4af37; border-bottom: 1px solid #d4af37; padding: 5px 0; font-size: 11px; color: #444; margin-bottom: 10px; }
.status { border: 1.5px solid #d4af37; background: #fffaf0; border-radius: 6px; padding: 7px 10px; font-size: 11.5px; margin-bottom: 12px; }
.hdr { display: flex; align-items: center; gap: 12px; }
.hdr img { height: 54px; }
table.ch { width: 100%; border-collapse: collapse; font-size: 12px; }
table.ch td, table.ch th { border-bottom: 1px solid #e3e0d6; padding: 4px 5px; vertical-align: top; text-align: left; }
table.ch th { font-size: 10.5px; color: #6b5a1e; }
.box { display: inline-block; width: 11px; height: 11px; border: 1.3px solid #555; border-radius: 2px; vertical-align: -1px; margin-right: 3px; }
.ac { white-space: nowrap; font-size: 10.5px; }
.ftitle { font-size: 14px; font-weight: 700; margin: 0 0 6px; }
.cap { font-size: 12px; margin-top: 8px; line-height: 1.4; }
.cap b { color: #6b5a1e; }
.mark { font-size: 9.5px; color: #8a6a00; text-align: right; margin-top: 3px; }
.frame { background: #1b1b20; border: 1px solid #444; border-radius: 22px; padding: 6px; width: fit-content; margin: 6px auto 0; }
.frame.flat { border-radius: 8px; padding: 2px; }
.devwrap { position: relative; overflow: hidden; contain: strict; border-radius: 16px; }   /* strict: no print shrink from the clipped screen */
.dev { position: absolute; left: 0; top: 0; background: #05050a; color: #a9f795; overflow: hidden; }
.dev .r3d { position: absolute; }
.wm { position: absolute; left: 24px; top: 30px; font-weight: 700; letter-spacing: 2.2px; font-size: 14px; color: #d8ffcc; }
.wm span { color: #5ee233; }
.btn { border: 1px solid rgba(169,247,149,.35); background: #07070d; color: #a9f795; border-radius: 6px; font-size: 13px; display: inline-flex;
       align-items: center; justify-content: center; padding: 0 14px; height: 44px; white-space: nowrap; font-weight: 600; }
.btn.gold { border-color: #e2b23a; }
.btn.on { background: #4f3d11; border-color: #e8c060; color: #fff3cf; }
.btn.gon { background: #4f3d11; border-color: #e8c060; color: #fff3cf; }
.btn.g { border-color: rgba(169,247,149,.35); }
.btn.on.green { background: #1d3a14; border-color: #5ee233; color: #d8ffcc; }
.seg { display: inline-flex; border: 1px solid rgba(169,247,149,.35); border-radius: 8px; overflow: hidden; height: 36px; }
.seg span { padding: 0 12px; display: flex; align-items: center; font-size: 12px; color: #a9f795; }
.seg span.on { background: #1d3a14; color: #d8ffcc; font-weight: 700; }
.side { position: absolute; right: 28px; top: 30px; display: flex; flex-direction: column; gap: 6px; }
.side div { width: 46px; height: 44px; border: 1px solid rgba(94,226,51,.45); border-radius: 7px; display: grid; place-items: center; font-size: 17px; color: #a9f795; background: #08080f; }
.side div.inuse { border-color: #5ee233; background: #1d3a14; }
.panel { position: absolute; left: 0; right: 0; bottom: 0; text-align: center; }
.chev { display: inline-grid; place-items: center; width: 44px; height: 26px; border: 1px solid rgba(169,247,149,.35); border-radius: 5px; color: #a9f795; font-size: 13px; }
.head { color: #e8c060; font-weight: 700; font-size: 15px; margin-top: 7px; }
.capl { color: #a9f795; font-size: 13px; margin-top: 4px; }
.row { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.lab { color: #a9f795; font-size: 13px; font-weight: 600; }
.sl { position: relative; }
.track { position: absolute; height: 14px; border-radius: 7px; background: #2d2d31; border: 1.5px solid rgba(94,226,51,.55); }
.tick { position: absolute; width: 5px; border-radius: 2px; }
.tl { position: absolute; font-size: 12px; white-space: nowrap; transform: translateX(-50%); }
.thumb { position: absolute; width: 42px; height: 42px; border-radius: 50%; background: #5ee233; border: 3px solid #fff; transform: translate(-50%, -50%); box-shadow: 0 0 8px rgba(0,0,0,.6); }
.ogm { position: absolute; width: 10px; height: 10px; background: #e8c060; transform: translate(-50%, -50%) rotate(45deg); border: 1px solid #fff3cf; }
.inf { position: relative; width: 184px; height: 83px; flex: 0 0 184px; }
.inf svg.l { position: absolute; inset: 0; width: 100%; height: 100%; fill: none; stroke: #e8c060; stroke-width: 3; opacity: .6; }
.lobe { position: absolute; top: 12px; width: 60px; height: 60px; display: grid; place-items: center; color: #d8cfb8; }
.lobe svg { width: 24px; height: 24px; fill: currentColor; }
.pause { width: 46px; height: 46px; border-radius: 10px; border: 1px solid rgba(169,247,149,.35); display: grid; place-items: center; color: #d8cfb8; }
.pause svg { width: 20px; height: 20px; fill: currentColor; }
.corner { position: absolute; bottom: 14px; display: flex; gap: 8px; }
.corner div { width: 36px; height: 36px; border: 1px solid rgba(169,247,149,.3); border-radius: 7px; display: grid; place-items: center; font-size: 15px; color: #a9f795; }
.devmark { position: absolute; display: flex; align-items: center; gap: 6px; color: #b89a4a; font-size: 11px; }
.devmark img { height: 22px; }
.inset { position: absolute; border: 1px solid rgba(232,192,96,.55); border-radius: 10px; background: rgba(12,10,6,.85); text-align: center; color: #e8c060; font-size: 12px; }
.chip { display: inline-flex; align-items: center; height: 36px; padding: 0 12px; border-radius: 18px; border: 1px solid rgba(169,247,149,.35); font-size: 12.5px; color: #a9f795; }
.chip.gon { background: #4f3d11; border-color: #e8c060; color: #fff3cf; font-weight: 700; }
.strip { position: absolute; }
.stn { position: absolute; transform: translateX(-50%); text-align: center; font-size: 12px; }
.dot { width: 22px; height: 22px; border-radius: 50%; margin: 0 auto 4px; border: 2px solid #a9f795; background: #07070d; }
.dot.cur { background: #e8c060; border-color: #fff3cf; width: 34px; height: 34px; margin-top: -6px; }
.link { position: absolute; height: 4px; }
.diag { position: absolute; border: 1px solid rgba(169,247,149,.35); border-radius: 10px; background: rgba(8,8,15,.9); color: #a9f795; font-size: 11.5px; text-align: center; }
"""


def inf_player():
    lobe = lambda side, d: (f'<div class="lobe" style="{side}:21px"><svg viewBox="0 0 20 20">'
                            + ('<path d="M6 3l11 7-11 7z"/>' if d == 'unwrap' else '<path d="M14 3L3 10l11 7z"/>') + '</svg></div>')
    return (f'<div class="inf"><svg class="l" viewBox="0 0 200 90"><path d="{INF_PATH}"/></svg>{lobe("left", "wrap")}{lobe("right", "unwrap")}</div>'
            '<div class="pause"><svg viewBox="0 0 20 20"><rect x="4" y="3" width="4" height="14" rx="1"/><rect x="12" y="3" width="4" height="14" rx="1"/></svg></div>')


def header(title, phone=False):
    s = 1.0
    return (f'<div class="wm">POLYHEDRA<span>VERSE</span></div>'
            f'<div style="position:absolute;left:24px;top:56px;display:flex;align-items:center;gap:12px"><span class="btn" style="height:34px;font-size:12px;font-weight:400">DICTO</span>'
            f'<span style="font-size:30px;font-weight:800;color:#5ee233">3D+</span></div>'
            f'<div style="position:absolute;left:24px;top:98px;display:flex;align-items:center;gap:12px"><span class="btn" style="height:34px;font-size:12px;font-weight:400">← Back</span>'
            f'<span style="color:#e8c060;font-weight:700;font-size:13px">{E(title)}</span></div>')


def sidebar(inuse='∞'):
    icons = ['🌐', '⚙', '3D', '◎', '⛶', '◯', '▢', '⊘', '↻', '📖']
    return '<div class="side">' + ''.join(f'<div>{i}</div>' for i in icons) + '</div>'


def corners():
    return ('<div class="corner" style="left:16px"><div>⬡</div><div>⬢</div><div style="margin-left:40px">🖌</div></div>'
            '<div class="corner" style="right:16px"><div>↶</div><div style="border-radius:50%">🕘</div><div style="border-radius:50%">i</div></div>')


def place_labels(xs, widths, gap=10):
    """stagger labels into rows (0 = nearest the track) so none overlap"""
    rows, ends = [], []
    for x, w in zip(xs, widths):
        a = x - w / 2
        for r in range(4):
            if r >= len(ends): ends.append(-1e9)
            if a > ends[r] + gap: ends[r] = x + w / 2; rows.append(r); break
        else: rows.append(3)
    return rows


def slider(width, lo, hi, stations, cur, labels=True, og=None, label_of=None, fs=12):
    """the big bottom slider: stations as ticks (golden gold), labels staggered above, thumb at `cur` (a value)"""
    X = lambda v: 21 + (v - lo) / (hi - lo) * (width - 42)
    top = 72 if labels else 22
    h = top + 44
    out = [f'<div class="sl" style="width:{width}px;height:{h}px">',
           f'<div class="track" style="left:0;right:0;top:{top - 7}px"></div>']
    xs = [X(s['v']) for s in stations]
    names = [label_of(s) if label_of else s['label'] for s in stations]
    rows = place_labels(xs, [len(n) * fs * 0.56 + 4 for n in names]) if labels else [0] * len(xs)
    for s, x, n, r in zip(stations, xs, names, rows):
        col = GOLDT if s['golden'] else PALE
        out.append(f'<div class="tick" style="left:{x - 2.5:.1f}px;top:{top - 15}px;height:30px;background:{col}"></div>')
        if labels:
            iscur = abs(s['v'] - cur) < 1e-9
            out.append(f'<div class="tl" style="left:{x:.1f}px;top:{top - 40 - 17 * r}px;color:{col};'
                       f'font-weight:{800 if iscur else (600 if s["golden"] else 400)};font-size:{fs + (1 if iscur else 0)}px">{E(n)}</div>')
    for m in (og or []):
        out.append(f'<div class="ogm" style="left:{X(m["v"]):.1f}px;top:{top + 22}px"></div>')
    out.append(f'<div class="thumb" style="left:{X(cur):.1f}px;top:{top}px"></div></div>')
    return ''.join(out), h


def devmark(pos):
    return f'<div class="devmark" style="{pos}"><img src="img/dicto-logo.png">DICTO · dictospheres.com</div>'


def detail(inner, w, h, x0, y0, cw, ch, label):
    """the same screen at 1:1 CSS scale (about real iPad size on paper), cropped to the controls"""
    return (f'<div style="font-size:11px;color:#6b5a1e;margin:8px 0 0">{E(label)}</div><div class="frame flat"><div class="devwrap" style="width:{cw}px;height:{ch}px;border-radius:6px">'
            f'<div class="dev" style="width:{w}px;height:{h}px;left:{-x0}px;top:{-y0}px">{inner}</div></div></div>')


def device(inner, w, h, scale):
    # zoom (not a transform) so the print layout sees the scaled size
    return (f'<div class="frame"><div class="devwrap" style="width:{w * scale:.1f}px;height:{h * scale:.1f}px">'
            f'<div class="dev" style="width:{w}px;height:{h}px;zoom:{scale}">{inner}</div></div></div>')


def figpage(n, title, dev, caption, approve):
    return (f'<div class="page"><div class="ftitle">Figure {n}. {E(title)}</div>{dev}'
            f'<div class="cap">{caption}<br><b>To approve:</b> {approve}</div>'
            f'<div class="mark">mock-up, not built · DICTO · dictospheres.com</div></div>')


def pair_buttons(cur, phone=False):
    names = [('di', 'Dodecahedron–Icosahedron', 'Dodeca–Icosa'), ('co', 'Cube–Octahedron', 'Cube–Octa'), ('tt', 'Tetrahedron', 'Tetra')]
    return ''.join(f'<span class="btn {"on green" if k == cur else ""}" style="{"height:40px;padding:0 10px" if phone else ""}">'
                   f'{E(s if phone else l)}</span>' for k, l, s in names)


def views(cur):
    return '<span class="seg">' + ''.join(f'<span class="{"on" if v == cur else ""}">{v}</span>' for v in ('Sweep', 'Nested cycle', '4D slice')) + '</span>'


def cutwrap(cur):
    return '<span class="seg" style="height:30px">' + ''.join(f'<span class="{"on" if v == cur else ""}" style="font-size:11.5px;padding:0 9px">{v}</span>' for v in ('cut', 'wrap')) + '</span>'


def stations_of(k):
    return [{'v': s['mu_float'], 'golden': s['golden'], 'label': s['name'], 'tick': s['tick']} for s in D['pairs'][k]['stations']]


CO_LABEL = {'Octahedron': 'Octahedron', 'Unborn Axes': 'Unborn Axes', 'Truncated octahedron (TO)': 'TO', 'Icosaxes': 'Icosaxes',
            'Cuboctahedron': 'Cuboctahedron', 'Greater Golden Cut Cube': 'Greater GC Cube', 'Truncated cube': 'Truncated cube',
            'Lesser Golden Cut Cube': 'Lesser GC Cube', 'Cube': 'Cube'}


# ------------------------------------------------------------------ figure 1 and 2: iPad landscape, C·O sweep
def ipad_sweep(cur_i, head, capl, img, x0=300):
    W, H = 1366, 1024
    st = stations_of('co'); co = D['pairs']['co']
    sl, sh = slider(1366 - 48 - 250, co['r2'], co['R2'], st, st[cur_i]['v'], label_of=lambda s: CO_LABEL[s['label']])
    panel = (f'<div class="panel" style="bottom:66px"><span class="chev">⌄</span><div class="head">{E(head)}</div><div class="capl">{capl}</div>'
             f'<div class="row">{views("Sweep")}{cutwrap("cut")}<span style="width:14px"></span>{pair_buttons("co")}<span class="btn">✕ Close</span></div>'
             f'<div class="row" style="margin-top:4px;align-items:flex-end;gap:14px">{inf_player()}{sl}</div></div>')
    inner = (header('Dual-Pair Cycles') + sidebar() + f'<img class="r3d" src="img/{img}" style="left:{(W - 760) // 2}px;top:40px;width:760px;height:640px">'
             + panel + corners() + devmark('left:150px;bottom:20px'))
    return device(inner, W, H, 666 / W) + detail(inner, W, H, x0, 700, 676, 272, 'Detail at 1:1 (about real iPad size): the controls')


mu_phi = 'μ = φ = (1 + √5)/2 ≈ 1.6180 · ν = φ (the one golden station with ν a power of φ) · cube ∩ φ·octahedron · 24 corners'
f1 = ipad_sweep(3, 'Icosaxes', mu_phi, 'r-co-icosaxes.png')
g = D['pairs']['co']['stations'][5]
mu_g = f'μ = 4 + 3√2/2 − √5 − √10/2 ≈ {g["mu_float"]:.4f} · cube ∩ μ·octahedron · 24 corners'
f2 = ipad_sweep(5, 'Greater Golden Cut Cube', mu_g, 'r-co-ggc-cube.png', x0=560)


# ------------------------------------------------------------------ figure 3: iPad nested cycle, D·I polar Dharma, OG highlighted
def ipad_nested():
    W, H = 1366, 1024
    names = ['Dodecahedron', 'Icosidodecahedron', 'OG', 'Pentakis dodecahedron', 'Icosahedron', 'Rhombic triacontahedron', 'φ³·Dodecahedron']
    touch = [False, True, True, True, True, False]       # s4 chain links: the middle four touch (factor 1)
    sw = 1366 - 48 - 250
    xs = [60 + i * (sw - 140) / 6 for i in range(7)]
    strip = [f'<div class="strip" style="position:relative;width:{sw}px;height:86px">']
    for i in range(6):
        col = '#e8c060' if touch[i] else 'rgba(169,247,149,.45)'
        dash = '' if touch[i] else 'background:repeating-linear-gradient(90deg,rgba(169,247,149,.6) 0 8px,transparent 8px 14px);'
        strip.append(f'<div class="link" style="left:{xs[i]}px;width:{xs[i + 1] - xs[i]}px;top:30px;background:{col};{dash}"></div>')
        strip.append(f'<div style="position:absolute;left:{(xs[i] + xs[i + 1]) / 2}px;top:6px;transform:translateX(-50%);font-size:11px;'
                     f'color:{"#e8c060" if touch[i] else "#8bcc7c"}">{"touch" if touch[i] else "gap"}</div>')
    for i, (x, n) in enumerate(zip(xs, names)):
        cur = i == 2
        strip.append(f'<div class="stn" style="left:{x}px;top:{14 if not cur else 14}px;color:{"#e8c060" if cur else "#a9f795"};font-weight:{800 if cur else 400};'
                     f'font-size:{14 if cur else 12}px"><div class="dot {"cur" if cur else ""}"></div>{E(n)}</div>')
    strip.append(f'<div style="position:absolute;left:{xs[6]}px;top:64px;transform:translateX(-50%);color:#e8c060;font-size:12px;font-weight:700;white-space:nowrap">closes at φ³</div></div>')
    panel = (f'<div class="panel" style="bottom:66px"><span class="chev">⌄</span><div class="head">OG · polar Dharma cycle</div>'
             f'<div class="capl">OG = H(μ_TI) ∩ φ²·icosahedron · ID, OG, pentakis, icosahedron and RT touch (factor 1) · inner 3√5 − 6 ≈ 0.708 · closes at φ³</div>'
             f'<div class="row">{views("Nested cycle")}<span style="width:8px"></span><span class="chip gon">Polar Dharma · φ³</span><span class="chip">Golden · φ</span>'
             f'<span style="width:14px"></span>{pair_buttons("di")}<span class="btn">✕ Close</span></div>'
             f'<div class="row" style="margin-top:6px;align-items:flex-end;gap:14px">{inf_player()}{"".join(strip)}</div></div>')
    inset = ('<div class="inset" style="left:40px;top:250px;width:230px;height:276px"><img src="img/r-lesser-golden-og.png" style="width:220px;height:220px;margin-top:6px">'
             '<div style="font-weight:700">Lesser Golden OG</div><div style="color:#d8cfb8;font-size:11px">μ = √5 · same faces as OG</div></div>')
    inner = (header('Dual-Pair Cycles') + sidebar() + f'<img class="r3d" src="img/r-di-dharma-nested.png" style="left:{(W - 720) // 2}px;top:52px;width:720px;height:640px">'
             + inset + panel + corners() + devmark('left:150px;bottom:20px'))
    return device(inner, W, H, 666 / W) + detail(inner, W, H, 300, 700, 676, 272, 'Detail at 1:1 (about real iPad size): the controls')


f3 = ipad_nested()


# ------------------------------------------------------------------ figure 4: phone portrait, D·I sweep at the Lesser GCI
def phone_sweep():
    W, H = 390, 844
    di = D['pairs']['di']; st = stations_of('di')
    og = [{'v': m['mu_float']} for m in di['og_marks']]
    sl, sh = slider(366, di['r2'], di['R2'], st, st[1]['v'], labels=False, og=og)
    side = ('<div class="side" style="right:10px;top:22px;gap:5px">' + ''.join(f'<div style="width:40px;height:38px;font-size:14px">{i}</div>'
            for i in ['🌐', '⚙', '3D', '◎', '⛶', '◯', '▢', '⊘', '↻', '📖']) + '</div>')
    hdr = ('<div class="wm" style="left:14px;top:18px;font-size:12px;letter-spacing:1.6px">POLYHEDRA<span>VERSE</span></div>'
           '<div style="position:absolute;left:14px;top:40px;display:flex;align-items:center;gap:9px"><span class="btn" style="height:30px;font-size:11px;padding:0 9px;font-weight:400">DICTO</span>'
           '<span style="font-size:24px;font-weight:800;color:#5ee233">3D+</span></div>'
           '<div style="position:absolute;left:14px;top:78px;display:flex;align-items:center;gap:9px"><span class="btn" style="height:30px;font-size:11px;padding:0 9px;font-weight:400">← Back</span>'
           '<span style="color:#e8c060;font-weight:700;font-size:12px">Dual-Pair Cycles</span></div>')
    panel = (f'<div class="panel" style="bottom:52px;padding:0 12px"><span class="chev">⌄</span><div class="head" style="font-size:15px">Lesser Golden Cut Icosahedron</div>'
             f'<div class="capl" style="font-size:12px">μ = √5 ≈ 2.2361 · dodecahedron ∩ √5·icosahedron · 60 corners</div>'
             f'<div class="row" style="gap:6px">{views("Sweep")}{cutwrap("cut")}</div>'
             f'<div class="row" style="gap:6px;margin-top:6px">{pair_buttons("di", phone=True)}<span class="btn" style="height:40px;padding:0 10px">✕</span></div>'
             f'<div class="row" style="margin-top:2px;transform:scale(.8);margin-bottom:-14px">{inf_player()}</div>'
             f'<div class="row" style="margin-top:0">{sl}</div></div>')
    corner = ('<div class="corner" style="left:10px;bottom:8px"><div style="width:32px;height:32px">⬡</div><div style="width:32px;height:32px">⬢</div></div>'
              '<div class="corner" style="right:10px;bottom:8px"><div style="width:32px;height:32px">↶</div><div style="width:32px;height:32px;border-radius:50%">i</div></div>')
    inner = (hdr + side + '<img class="r3d" src="img/r-di-lgci.png" style="left:6px;top:118px;width:330px;height:330px">' + panel + corner
             + devmark('left:100px;bottom:14px;font-size:9.5px'))
    return device(inner, W, H, 1.0)


f4 = phone_sweep()


# ------------------------------------------------------------------ figure 5: iPad 4D slice, C·O, rectified tesseractic honeycomb
def ipad_slice():
    W, H = 1366, 1024
    sd = D['slice']
    st = [{'v': s['h'], 'golden': s['golden'], 'label': s['name']} for s in sd['stations']]
    short = {'Cube (simple cubic)': 'Cubes', 'Lesser Golden Cut Cube + octahedra': 'Lesser GC Cube', 'Truncated cube + octahedra': 'Truncated cube',
             'Greater Golden Cut Cube + octahedra': 'Greater GC Cube', 'Cuboctahedron + octahedra': 'Cuboctahedron'}
    sl, sh = slider(1366 - 48 - 250, 0, 1, st, sd['h_float'], label_of=lambda s: short[s['label']])
    panel = (f'<div class="panel" style="bottom:66px"><span class="chev">⌄</span><div class="head">Greater Golden Cut Cube + octahedra</div>'
             f'<div class="capl">rectified tesseractic honeycomb · slice x₄ = h = 3 − μ ≈ {sd["h_float"]:.4f} · tiles cube ∩ (3 − h)·octahedron at 2ℤ³, octahedra of radius h at (2ℤ+1)³</div>'
             f'<div class="row">{views("4D slice")}<span style="width:14px"></span>{pair_buttons("co")}<span class="btn">✕ Close</span></div>'
             f'<div class="row" style="margin-top:4px;align-items:flex-end;gap:14px">{inf_player()}{sl}</div></div>')
    diag = ('<div class="diag" style="left:30px;top:150px;width:350px;height:300px"><div style="margin:6px 0 0;font-weight:700;color:#d8ffcc">where the slice sits</div>'
            '<img src="img/r-slice-diagram.png" style="width:340px;height:250px">'
            '<div style="font-size:10.5px;color:#8bcc7c;margin-top:-6px">plane (t,t,t, x₄): rectified tesseracts green, 16-cells violet, slice gold</div></div>')
    inner = (header('Dual-Pair Cycles') + sidebar() + f'<img class="r3d" src="img/r-co-slice.png" style="left:{(W - 640) // 2 + 60}px;top:80px;width:640px;height:560px">'
             + diag + panel + corners() + devmark('left:150px;bottom:20px'))
    return device(inner, W, H, 666 / W) + detail(inner, W, H, 560, 700, 676, 272, 'Detail at 1:1 (about real iPad size): the controls')


f5 = ipad_slice()

# ------------------------------------------------------------------ page 1: design choices
CHOICES = [
    ('Place', 'A new world in Polyhedraverse, in the 3D+ wizard next to ✂ Golden Cut.'),
    ('Pair buttons', 'Dodecahedron–Icosahedron · Cube–Octahedron · Tetrahedron, in D·I·C·T·O order. No arrows anywhere.'),
    ('Three views', 'Sweep · Nested cycle · 4D slice, as one segmented button row; each view shows only its own controls.'),
    ('Sweep slider', 'One long slider at the bottom (as Golden Cut: 42 px thumb), linear in μ from the dual end (left) to P (right); every station a tick; dragging near a tick lands on it.'),
    ('Golden stations', 'Ticks and names in gold: Golden Cut solids, Icosaxes, Unborn Axes. Others pale green.'),
    ('Tick labels', 'iPad: names above the ticks, staggered in rows. Phone: ticks only; the station name is the gold heading.'),
    ('∞ player', 'The app\'s ∞ player (Wrap ◀ / Unwrap ▶ in the ∞, VHS pause) plays the sweep station to station, pausing at each.'),
    ('cut / wrap', 'A small toggle: cut = S(μ) = P ∩ μP*; wrap = H(μ) = conv(P ∪ μP*). Tick labels follow it (cut: Cuboctahedron, TO; wrap: RD).'),
    ('Colours', 'Faces on P\'s planes green (the app piece colour), on μP*\'s planes violet; edges 2 px dark; app background.'),
    ('Frame', 'The camera stays framed on P (as Golden Cut), so the cut is seen eating into a still solid.'),
    ('Numbers line', 'μ exact and to 4 places, the solid as P ∩ μ·P*, corner count (as the Golden Cut caption).'),
    ('OG marks', 'On the D·I line, gold diamonds under the track at OG and the Lesser / Greater Golden OG (they are Q(μ, φ²), not S(μ)).'),
    ('Nested cycle', 'Each station inside the next, innermost solid, outer shells see-through crystal, the current station gold; a station strip shows which links touch and the closing factor.'),
    ('Cycles offered', 'D·I polar Dharma (φ³) and golden (φ); C·O cube ⊂ RD ⊂ 2 TO ⊂ 2 cube (2) and golden (φ); T golden (φ⁶). As chips.'),
    ('4D slice', 'Second build: the slice moving through a 4D honeycomb (C·O cube side: rectified tesseractic; octahedron side: 24-cell; T: tesseractic), tiles pulled apart 10 %, with a small 2D diagram of where the slice sits.'),
    ('Language', 'All words through the app\'s 7-language keys; English shown here.'),
]
rows = ''.join(f'<tr><td>{i + 1}</td><td><b>{E(a)}</b></td><td>{E(b)}</td><td class="ac"><span class="box"></span>approve&nbsp; <span class="box"></span>change</td></tr>'
               for i, (a, b) in enumerate(CHOICES))
p1 = (f'<div class="page"><div class="hdr"><img src="img/dicto-logo.png"><div><h1>Dual-Pair Cycles: a new world, mock-up</h1>'
      f'<div class="sub">Polyhedraverse · 3D+ wizard · beside Golden Cut · from the study "Dual pairs through the dimensions" (2026-11-03)</div></div></div>'
      f'<div class="meta">DICTO (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com · mock-up · 2026-11-03</div>'
      f'<div class="status"><b>Status:</b> mock-up, not built. The solids are real renders of the exact study geometry (dp_lib, s1, s4, s7); '
      f'the buttons, slider and panels are drawn to match the app. Nothing has changed in the app. Please mark each choice; '
      f'pages 2–7 show them.</div>'
      f'<table class="ch"><tr><th>#</th><th>Choice</th><th>Default shown in the figures</th><th>Your answer</th></tr>{rows}</table>'
      f'<div class="cap" style="margin-top:10px"><b>Pages:</b> 2 iPad sweep, C·O at Icosaxes · 3 the same at the Greater Golden Cut Cube · '
      f'4 iPad nested cycle, D·I polar Dharma, OG highlighted · 5 phone sweep, D·I · 6 iPad 4D slice, C·O · 7 the three sweeps as station films.</div>'
      f'<div class="mark">DICTO · dictospheres.com</div></div>')

pages = [p1,
         figpage(1, 'iPad landscape · Sweep · Cube–Octahedron at Icosaxes (μ = φ)', f1,
                 'The cube ∩ φ·octahedron (8 golden hexagons violet, 6 squares green), framed on the cube. The slider runs from the octahedron (μ = 1) '
                 'to the cube (μ = 3); its four golden ticks (Unborn Axes, Icosaxes, Greater and Lesser GC Cube) are gold, the thumb sits on Icosaxes.',
                 'the bottom panel layout (views, cut/wrap, pair buttons, Close; ∞ player left of the slider), labels above ticks, gold for golden.'),
         figpage(2, 'iPad landscape · Sweep · Cube–Octahedron at the Greater Golden Cut Cube', f2,
                 'The same view with the thumb moved right to μ ≈ 2.3041: the cube with its corners cut by octahedron planes (violet triangles), '
                 'octagons green. Heading and numbers line follow the station.',
                 'that the frame stays on the cube while the solid changes, and the numbers line.'),
         figpage(3, 'iPad landscape · Nested cycle · D–I polar Dharma cycle, OG highlighted', f3,
                 'The cycle, exact from the study (s4): inner dodecahedron ⊂ icosidodecahedron ⊂ OG ⊂ pentakis dodecahedron ⊂ icosahedron ⊂ rhombic triacontahedron '
                 '⊂ φ³ × the inner dodecahedron. The film is paused at OG and zoomed on its turn: OG solid (kites gold, hexagons violet), the pentakis dodecahedron, '
                 'icosahedron and RT round it as crystal; the two stations inside OG and the closing dodecahedron (2.4 × wider than the RT) '
                 'are on the strip (gold links touch). Inset: the Lesser Golden OG (μ = √5).',
                 'crystal shells round a solid core, the gold highlight of the current station, the station strip, the cycle chips, the inset.'),
         figpage(4, 'Phone portrait · Sweep · D–I at the Lesser Golden Cut Icosahedron (μ = √5)', f4,
                 'The dodecahedron ∩ √5·icosahedron. On a phone the ticks carry no names (the D·I stations lie only about 13 px apart); the gold heading names '
                 'the station. Gold diamonds under the track mark OG and the Golden OGs. Short pair names on the buttons.',
                 'ticks-only on phones, the short pair names, the ∞ player on its own row.'),
         figpage(5, 'iPad landscape · 4D slice · C–O, rectified tesseractic honeycomb, golden height', f5,
                 f'The slice x₄ = h ≈ {D["slice"]["h_float"]:.4f} gives Greater Golden Cut Cube tiles with octahedra at their shared corners (study s7 A, #89 '
                 'Corollary D), pulled apart 10 %. The slider is h through one period (cubes at 0, cuboctahedra + octahedra at 1). '
                 'The diagram (left) cuts the 4D honeycomb along the plane (t, t, t, x₄) and shows the slice as a gold line.',
                 'the 2D "where the slice sits" diagram, and h as the slider.'),
         (f'<div class="page"><div class="ftitle">Figure 6. Overview: the three dual-pair sweeps as station films</div>'
          f'<img src="img/fig6-filmstrips.png" style="width:100%;border:1px solid #ddd">'
          f'<div class="cap">Every station of the three sweeps S(μ) = P ∩ μP*, rendered from the exact study geometry, golden stations framed gold with their exact μ. '
          f'These are the ticks of the Sweep slider. Also proposed as a figure for paper #91 (white background).<br><b>To approve:</b> the station set and names per pair, '
          f'and use in #91.</div><div class="mark">mock-up, not built · DICTO · dictospheres.com</div></div>')]
doc = (f'<!doctype html><html><head><meta charset="utf-8"><title>Dual-Pair Cycles mock-up</title><style>{CSS}</style></head><body>'
       + ''.join(pages) + '</body></html>')
open(os.path.join(OUT, 'paper.html'), 'w').write(doc)
print('wrote', os.path.join(OUT, 'paper.html'))
