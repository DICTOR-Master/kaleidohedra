# DICTO 2026-10-21: first draft of the Mandala of Shells map figure (#18 style: dark ground (20,15,11), gold and purple).
# Nodes = named solids (similarity classes of exact stations, from mandala-map.json); arrows = the steps of the cycles, coloured by
# operation. Float drawing of exact relations.   usage: python3 map_figure.py   (reads mandala-map.json, writes figures/mandala-map.png)
import json, os, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, 'mandala-map.json')))
BG = (20 / 255, 15 / 255, 11 / 255); GOLD = '#e0b04a'; PURP = '#a57be0'; LIL = '#d7c3f5'; PALE = '#f3e6c8'; GREY = '#8a7f72'; CYAN = '#6fc3c9'
OPC = {'T': GOLD, 'T^n': GOLD, 'phiP': PURP, 'P': '#7a52b8', 'P^n': '#7a52b8', 'rho': CYAN, 'scale': GREY, 'T x c': '#b98b2e', 'P x c': '#7a52b8', 'rect x c': '#9c8f80', 'other': '#5e554c', 'star': '#c96f5a'}
node = {n['id']: n for n in M['nodes']}
cls = {c['class']: c for c in M['classes']}
star_ids = {n['id'] for n in M['nodes'] if n['star']}
def cname(sid):
    if sid in star_ids: return node[sid]['name']
    return cls[node[sid]['class']]['name']
# layout: classical icosahedral solids on the inner ring, DICTO's and the OG family outside, stars at the side
inner = ['I', 'ID', 'D', 'TI', 'H', 'RT', 'rTI', 'jtI', 'M', 'PD', 'OG', 'GTI', 'FPD']
outer = ['KRE', 'PHE', 'TPP', 'DPHP', 'TPH', 'TQH', 'TQP', 'TQHD', 'T H', 'T^2 H', 'T^3 H', 'T^4 H', 'P^2 H', 'P^3 H', 'P^4 H']
alias = {'jtI': 'jtI'}
names = sorted({cname(s) for s in node if not node[s]['cycle'].startswith('OTT') and not node[s]['cycle'].startswith('#33')})
pos = {}
for i, n in enumerate(inner): a = math.pi / 2 - 2 * math.pi * i / len(inner); pos[n] = (3.0 * math.cos(a), 3.0 * math.sin(a))
outer = [n for n in outer if n in names or n == 'KRE']
for i, n in enumerate(outer): a = math.pi / 2 - 2 * math.pi * (i + .5) / len(outer); pos[n] = (5.6 * math.cos(a), 5.6 * math.sin(a))
pos['Cleo star'] = (-1.3, 0.3); pos['great stellated dodecahedron'] = (0.6, 1.2); pos['small stellated dodecahedron'] = (0.4, -1.3)
label = {'great stellated dodecahedron': 'GSD', 'small stellated dodecahedron': 'SSD', 'jtI': 'jtI = KRE'}
# the KRE of #39 is the jtI shape (same similarity class): show it once
pos['KRE'] = pos['jtI']
fig, ax = plt.subplots(figsize=(13, 13), dpi=110); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
seen = {}
for e in M['edges']:
    if e['cycle'].startswith('#33') or e['cycle'].startswith('OTT'): continue
    a, b = cname(e['from']), cname(e['to'])
    if a == 'KRE': a = 'jtI'
    if b == 'KRE': b = 'jtI'
    op = e['op']; op = 'T^n' if op.startswith('T^') else 'P^n' if op.startswith('P^') else op
    if node[e['from']]['star'] or node[e['to']]['star']: op = 'star'
    k = (a, b, op); seen.setdefault(k, []).append(e['cycle'])
for (a, b, op), cyc in seen.items():
    if a not in pos or b not in pos: continue
    col = OPC.get(op, GREY); lw = 2.6 if op in ('T', 'phiP', 'P', 'rho', 'T^n', 'P^n') else 1.3
    if a == b:
        x, y = pos[a]; ax.add_patch(FancyArrowPatch((x - .18, y + .22), (x + .18, y + .22), connectionstyle='arc3,rad=-1.6', arrowstyle='-|>', mutation_scale=12, color=col, lw=lw)); continue
    rad = 0.18 if op in ('T', 'T^n', 'T x c') else -0.18 if op in ('phiP', 'P', 'P^n', 'P x c') else 0.05
    ax.add_patch(FancyArrowPatch(pos[a], pos[b], connectionstyle=f'arc3,rad={rad}', arrowstyle='-|>', mutation_scale=15, color=col, lw=lw, alpha=.92, shrinkA=22, shrinkB=22, ls='--' if op in ('other', 'rect x c') else '-'))
for n, (x, y) in pos.items():
    if n == 'KRE': continue
    if n not in names and n not in ('jtI',): continue
    dicto = n in ('H', 'OG', 'M', 'GTI', 'FPD', 'TPH', 'TQH', 'TQP', 'TQHD', 'PHE', 'TPP', 'DPHP', 'Cleo star') or n.startswith('T') and 'H' in n or n.startswith('P^')
    ax.scatter([x], [y], s=1500, color=BG, edgecolor=PURP if dicto else GOLD, lw=2.2, zorder=3)
    ax.text(x, y, label.get(n, n), color=LIL if dicto else PALE, ha='center', va='center', fontsize=9.5 if len(label.get(n, n)) < 6 else 7.2, zorder=4, family='DejaVu Sans')
ax.text(0, 6.9, 'The DICTO Mandala of Shells: the map (first draft)', color=GOLD, ha='center', fontsize=17, family='DejaVu Serif')
ax.text(0, 6.45, 'named solids (up to scale) and the steps of DICTO\'s cycles #22-#43 and the new cycles; exact in Q(sqrt5)', color=PALE, ha='center', fontsize=10)
leg = [('T  (UP step)', GOLD, '-'), ('T^n  (fused beats)', GOLD, '-'), ('phi P  (turned out)', PURP, '-'), ('P  (foot points)', '#7a52b8', '-'), ('rho  (polarity, some sphere)', CYAN, '-'),
       ('c x T, not a polarity', '#b98b2e', '-'), ('stellation / hull of a star', '#c96f5a', '-'), ('other (face-on placement, caps, Shields, loose nest)', '#5e554c', '--')]
for i, (t, c, ls) in enumerate(leg):
    y = -6.2 - 0.3 * (i % 4); x = -6.4 + 6.6 * (i // 4)
    ax.plot([x, x + .5], [y, y], color=c, lw=2.6, ls=ls); ax.text(x + .65, y, t, color=PALE, va='center', fontsize=9)
ax.text(6.9, -7.4, 'DICTO · dictospheres.com', color=GOLD, ha='right', fontsize=9)
ax.text(-6.4, -7.45, 'gold ring: classical solid   purple ring: DICTO solid   (the OTT cycles, not icosahedral, are in the README)', color=GREY, fontsize=8.5, ha='left')
ax.set_xlim(-7.2, 7.2); ax.set_ylim(-7.6, 7.3); ax.set_aspect('equal'); ax.axis('off')
os.makedirs(os.path.join(HERE, 'figures'), exist_ok=True)
fig.savefig(os.path.join(HERE, 'figures', 'mandala-map.png'), facecolor=BG, bbox_inches='tight'); print('figures/mandala-map.png')
