"""Figures for the change-ringing chapter: tours on the truncated octahedron (the permutohedron of four values) and rhythm strips.
Reads data/ring.json, writes figures/*.svg. DICTO · dictospheres.com - study 2026-11-12-change-ringing.
Usage: python3 figs.py <study dir>.  Float drawing of exact combinatorial data (rows and changes are exact)."""
import sys, os, json, math, itertools

STUDY = sys.argv[1]; D = json.load(open(os.path.join(STUDY, 'data', 'ring.json'))); FIG = os.path.join(STUDY, 'figures')
os.makedirs(FIG, exist_ok=True)
SQ_FILL, HEX_FILL, EDGE, PATH = '#e8cf8a', '#a9c6ea', '#555', '#b0302a'
MARK = 'DICTO · dictospheres.com'
OK = True

def sub(a, b): return [x - y for x, y in zip(a, b)]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def norm(a): l = math.sqrt(dot(a, a)); return [x / l for x in a]

ROWS = [''.join(p) for p in itertools.permutations('1234')]
def point4(row):  # x_b = position of bell b (1-based), centred
    x = [0] * 4
    for pos, b in enumerate(row): x[int(b) - 1] = pos + 1 - 2.5
    return x
B3 = [norm([1, -1, 0, 0]), norm([1, 1, -2, 0]), norm([1, 1, 1, -3])]
def point3(row): x = point4(row); return [dot(x, e) for e in B3]

def view(theta, phi):
    """screen basis: h along rounds - backrounds, v turned by theta about h, w = view direction; phi tilts h"""
    h = norm(sub(point3('1234'), point3('4321')))
    a = [0, 0, 1]; a = norm(sub(a, [dot(a, h) * c for c in h])); b = cross(h, a)
    v = [math.cos(theta) * x + math.sin(theta) * y for x, y in zip(a, b)]
    w = cross(h, v)
    # tilt about v by phi
    h2 = [math.cos(phi) * x + math.sin(phi) * y for x, y in zip(h, w)]; w2 = cross(h2, v)
    return h2, v, w2

def faces():
    out = []
    swaps = {(0,): None}
    seen = set()
    for r in ROWS:
        for gens in ((0, 1), (1, 2), (0, 2)):
            # rows reachable from r by swaps at the generator positions
            orb = {r}; frontier = [r]
            while frontier:
                s = frontier.pop();
                for g in gens:
                    t = list(s); t[g], t[g + 1] = t[g + 1], t[g]; t = ''.join(t)
                    if t not in orb: orb.add(t); frontier.append(t)
            key = frozenset(orb)
            if key in seen: continue
            seen.add(key); out.append(('S' if gens == (0, 2) else 'H', sorted(orb)))
    return out
FACES = faces()
def is_edge(a, b): return sum(x != y for x, y in zip(a, b)) == 2 and any(a[i] == b[i + 1] and a[i + 1] == b[i] for i in range(3))
EDGES = [(a, b) for a, b in itertools.combinations(ROWS, 2) if is_edge(a, b)]
assert len(FACES) == 14 and len(EDGES) == 36

def solid(svg, ox, oy, scale, theta, phi, tour, title, labels=True, sub_title='', k=1.0):
    h, v, w = view(theta, phi)
    P = {r: point3(r) for r in ROWS}
    S = {r: (ox + scale * dot(P[r], h), oy - scale * dot(P[r], v)) for r in ROWS}
    depth = {r: dot(P[r], w) for r in ROWS}
    fdata = []
    for kind, rows in FACES:
        c = [sum(P[r][i] for r in rows) / len(rows) for i in range(3)]
        nrm = norm(c)  # faces of a centred convex solid: outward normal along the centroid
        e1 = norm(sub(P[rows[0]], c)); e2 = cross(nrm, e1)
        order = sorted(rows, key=lambda r: math.atan2(dot(sub(P[r], c), e2), dot(sub(P[r], c), e1)))
        fdata.append((dot(c, w), kind, order, dot(nrm, w) > 0, set(rows)))
    fdata.sort()
    def poly(order): return ' '.join(f'{S[r][0]:.1f},{S[r][1]:.1f}' for r in order)
    # back faces, back edges
    for d, kind, order, front, rs in fdata:
        if not front: svg.append(f'<polygon points="{poly(order)}" fill="{SQ_FILL if kind == "S" else HEX_FILL}" fill-opacity="0.18" stroke="none"/>')
    def edge_front(a, b): return any(front and a in rs and b in rs for d, k, o, front, rs in fdata)
    for a, b in EDGES:
        if not edge_front(a, b): svg.append(f'<line x1="{S[a][0]:.1f}" y1="{S[a][1]:.1f}" x2="{S[b][0]:.1f}" y2="{S[b][1]:.1f}" stroke="#999" stroke-width="{0.8 * k:.2f}" stroke-dasharray="{3 * k:.1f},{3 * k:.1f}"/>')
    # hidden part of the tour
    T = tour + [tour[0]]
    def seg_front(a, b):
        if is_edge(a, b): return edge_front(a, b)
        return any(front and a in rs and b in rs for d, k, o, front, rs in fdata)
    for a, b in zip(T, T[1:]):
        if not seg_front(a, b):
            svg.append(f'<line x1="{S[a][0]:.1f}" y1="{S[a][1]:.1f}" x2="{S[b][0]:.1f}" y2="{S[b][1]:.1f}" stroke="{PATH}" stroke-opacity="0.45" stroke-width="{2.2 * k:.2f}" stroke-dasharray="{5 * k:.1f},{3 * k:.1f}"/>')
    for d, kind, order, front, rs in fdata:
        if front: svg.append(f'<polygon points="{poly(order)}" fill="{SQ_FILL if kind == "S" else HEX_FILL}" fill-opacity="0.42" stroke="none"/>')
    for a, b in EDGES:
        if edge_front(a, b): svg.append(f'<line x1="{S[a][0]:.1f}" y1="{S[a][1]:.1f}" x2="{S[b][0]:.1f}" y2="{S[b][1]:.1f}" stroke="{EDGE}" stroke-width="{1.2 * k:.2f}"/>')
    for a, b in zip(T, T[1:]):
        if seg_front(a, b):
            svg.append(f'<line x1="{S[a][0]:.1f}" y1="{S[a][1]:.1f}" x2="{S[b][0]:.1f}" y2="{S[b][1]:.1f}" stroke="{PATH}" stroke-width="{3.2 * k:.2f}" stroke-linecap="round"/>')
    # direction: a small arrow on the first step
    a, b = T[0], T[1]; mx, my = (S[a][0] * 0.4 + S[b][0] * 0.6), (S[a][1] * 0.4 + S[b][1] * 0.6)
    ang = math.atan2(S[b][1] - S[a][1], S[b][0] - S[a][0])
    pts = [(mx + 9 * k * math.cos(ang), my + 9 * k * math.sin(ang)), (mx + 6 * k * math.cos(ang + 2.5), my + 6 * k * math.sin(ang + 2.5)), (mx + 6 * k * math.cos(ang - 2.5), my + 6 * k * math.sin(ang - 2.5))]
    svg.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{PATH}"/>')
    cx = sum(S[r][0] for r in ROWS) / 24; cy = sum(S[r][1] for r in ROWS) / 24
    for r in ROWS:
        x, y = S[r]; vis = depth[r] > -0.9
        rad = (4.5 if r in ('1234', '4321') else 2.4) * k
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{"#7a5c00" if r in ("1234", "4321") else ("#222" if vis else "#888")}"/>')
        if labels or r in ('1234', '4321'):
            dx, dy = x - cx, y - cy; l = math.hypot(dx, dy) or 1
            off = (26 if r in ('1234', '4321') else 15) * k   # 13 Nov: rounds and backrounds sit further out, clear of their larger dots
            tx, ty = x + off * dx / l, y + off * dy / l + 3.5 * k
            wt = 'bold' if r in ('1234', '4321') else 'normal'
            svg.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="{(12.5 if r in ("1234", "4321") else 10.5) * k:.1f}" font-weight="{wt}" text-anchor="middle" fill="{"#222" if vis else "#8a8a8a"}" font-family="Helvetica, Arial, sans-serif">{r}</text>')
    svg.append(f'<text x="{ox}" y="{oy - 2.24 * scale - 42 * k:.1f}" font-size="{15 * k:.1f}" font-weight="bold" text-anchor="middle" font-family="Helvetica, Arial, sans-serif">{title}</text>')
    if sub_title: svg.append(f'<text x="{ox}" y="{oy - 2.24 * scale - 24 * k:.1f}" font-size="{12 * k:.1f}" text-anchor="middle" fill="#444" font-family="Helvetica, Arial, sans-serif">{sub_title}</text>')

def write(name, W, H, body):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" fill="white"/>'] + body
    s.append(f'<text x="{W - 10}" y="{H - 10}" font-size="{max(11, W / 90):.0f}" text-anchor="end" fill="#9a7b2f" font-family="Helvetica, Arial, sans-serif">{MARK}</text></svg>')
    open(os.path.join(FIG, name), 'w').write('\n'.join(s)); print('wrote', name)

F = D['figures']
TH, PH = 0.62, 0.18
# Figure 1: Plain Bob Minimus
b = []; solid(b, 330, 330, 108, TH, PH, F['Plain Bob Minimus'][:24], 'Plain Bob Minimus', sub_title='x.14.x.14.x.14.x.12, three leads: 12 edges, 12 square diagonals')
write('fig-plain-bob-minimus.svg', 660, 620, b)
# Figure 2: the three most symmetric extents (order 12): plain changes, Double Court, Double Bob
b = []
solid(b, 300, 400, 100, TH, PH, F['Plain changes on 4'][:24], 'Plain changes on four', sub_title='edges only', labels=False, k=2.0)
solid(b, 900, 400, 100, TH, PH, F['CCCBR Double Court Place Minimus'][:24], 'Double Court Place', sub_title='edges only', labels=False, k=2.0)
solid(b, 1500, 400, 100, TH, PH, F['CCCBR Double Bob Minimus'][:24], 'Double Bob', sub_title='12 edges, 12 diagonals', labels=False, k=2.0)
write('fig-most-symmetric.svg', 1800, 690, b)
# Figure 3: plain hunt on four, a closed geodesic loop through rounds and backrounds
b = []; solid(b, 330, 330, 108, TH, PH, F['Plain hunt on 4'][:8], 'Plain hunt on four', sub_title='x.14 four times: rounds to backrounds in 4 changes and back')
write('fig-plain-hunt.svg', 660, 620, b)

# Figure 4: rhythm strips
order = ['Plain Bob Minimus', 'Plain changes on 4', 'Plain Bob Doubles', 'Grandsire Doubles', 'Stedman Doubles', 'Plain changes on 5']
ST = F['strips']; W = 1000; left = 250; y = 30; body = []
COL = {1: '#3f6fb5', 2: '#c9a23a', 3: '#7a4fa0'}
for nm in order:
    if nm not in ST: continue
    chs = ST[nm]; N = len(chs); n = 4 if ('Minimus' in nm or 'on 4' in nm) else 5
    cw = (W - left - 20) / N; ch = 14
    body.append(f'<text x="10" y="{y + (n - 1) * ch / 2 + 4}" font-size="17" font-family="Helvetica, Arial, sans-serif">{nm} ({N})</text>')
    for t, c in enumerate(chs):
        for i in c:
            body.append(f'<rect x="{left + t * cw:.2f}" y="{y + i * ch}" width="{max(cw - 0.4, 0.6):.2f}" height="{ch - 1}" fill="{COL[min(len(c), 3)]}"/>')
    body.append(f'<rect x="{left}" y="{y}" width="{N * cw:.1f}" height="{(n - 1) * ch}" fill="none" stroke="#bbb" stroke-width="0.5"/>')
    y += (n - 1) * ch + 26
body.append(f'<text x="10" y="{y + 8}" font-size="16" fill="#444" font-family="Helvetica, Arial, sans-serif">blue: one swap (an edge); gold: two swaps (a square crossed)</text>')
write('fig-rhythm.svg', W, y + 40, body)
print('FINAL ok' if OK else 'FINAL FAIL')
