# Keyed W as wallpaper (DICTO 2026-10-19 brief, started 2026-10-20 03:00): the keys on W's flat faces should GIVE THE IMPRESSION that the
# OG's own surface pattern (60 kites, 20 hexagons) carries on across the joins. Impression, not exactness.
# W_star (#37) = the octahedral Voronoi cell of an octahedron-edge midpoint minus its two OGs (the two sockets = W's two sides). Its 8 flat
# faces are triangles (OG centre A, octet vertex E, tetrahedron centre T) with the OG's section bitten out at A; each meets a copy of W.
# Face 1 = (A0, E0, T+) in the plane z = x (#37 frame, Fable review 4): this W lies on its n-negative side, the neighbouring W on the other.
# Drawing method (2D, one plane):
#   inside the socket rim: the socket as seen face-on (orthographic view of the OG half on this W's side);
#   outside the rim, on the flat face: the OG half on the far side, ROLLED OUT across the rim (direction kept, radius |x|(1 + elevation)),
#   so every OG edge that crosses the joint plane carries straight on from the socket onto the face. That rolled-out pattern is the key:
#   raised on this W, sunk the same in the neighbouring W, whose face is drawn opened out like a book about the edge A-E.
import json, math, sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, '..', 'data', 'step1-ocd-exact.json')))
num = lambda s: (lambda a, b: float(eval(a)) + float(eval(b)) * 5 ** .5)(*s.split('|'))
V = np.array([[num(c) for c in v] for v in D['V']]); F = D['faces']; R = num(D['R']) if isinstance(D['R'], str) else 2 * (1 + 5 ** .5) / 6
u = np.array([0, 1, 0.]); w = np.array([1, 0, 1.]) / 2 ** .5; n = np.array([1, 0, -1.]) / 2 ** .5
A, E, T = np.zeros(3), np.array([0, R, 0]), np.array([R / 2, R / 2, R / 2]); tri = np.array([[x @ u, x @ w] for x in (A, E, T)])
log = open(os.path.join(HERE, '..', 'data', 'wallpaper-face.log'), 'w')
def say(*a): print(*a); print(*a, file=log); log.flush()
say('OG corners', len(V), 'faces', len(F), '| R', round(R, 6), '| face triangle uv', tri.round(4).tolist())
SIDE = -1                                    # this W is on the n-negative side; the neighbour on the positive side
def mapped(x, inside_side):
    p = np.array([x @ u, x @ w]); h = x @ n
    if np.sign(h) == inside_side or abs(h) < 1e-12: return p                         # socket: seen face-on
    r = np.linalg.norm(x); phi = math.atan2(abs(h), np.linalg.norm(p)); d = p / max(np.linalg.norm(p), 1e-12)
    return d * r * (1 + phi)                                                           # far half rolled out across the rim
def face_path(f, side, k=24):
    pts = []
    for i in range(len(f)):
        a, b = V[f[i]], V[f[(i + 1) % len(f)]]
        for t in np.linspace(0, 1, k, endpoint=False): pts.append(mapped(a + t * (b - a), side))
    return np.array(pts)
# the section (socket rim) in the joint plane
cr = []
for f in F:
    for i in range(len(f)):
        a, b = V[f[i]], V[f[(i + 1) % len(f)]]; ha, hb = a @ n, b @ n
        if ha * hb < 0: x = a + ha / (ha - hb) * (b - a); cr.append([x @ u, x @ w])
cr = np.unique(np.round(np.array(cr), 9), axis=0); c0 = cr.mean(0); cr = cr[np.argsort(np.arctan2(cr[:, 1] - c0[1], cr[:, 0] - c0[0]))]
say('socket rim: OG edges crossing the joint plane', len(cr))
kinds = ['hex' if len(f) == 6 else 'kite' for f in F]
# drawing (SVG), panel 1 = this W's face (key raised), panel 2 = the neighbour's face (key sunk), mirrored about the edge A-E
S = 520; pad = 90; ox, oy = pad, pad + S * 0.80
P = lambda q, mirror=False: (ox + q[0] * S, oy - (-q[1] if mirror else q[1]) * S)
def poly(pts, mirror=False): return ' '.join(f'{P(q, mirror)[0]:.2f},{P(q, mirror)[1]:.2f}' for q in pts)
inset = 0.035                                 # clearance from the cell edges (Fable review 4: about 1.4 mm)
cen = tri.mean(0); tri_in = cen + (tri - cen) * (1 - inset / (np.linalg.norm(tri - cen, axis=1).min() * 0.5))
C = dict(bg='#f6f4ef', ink='#1f2430', muted='#6b7280', hexS='#9db7dc', kiteS='#c9d8ee', hexK='#d9a93c', kiteK='#efd08a', hexD='#a8781f', kiteD='#cfa95a', line='#2b3445')
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {2 * pad + S * 1.45:.0f} {2 * pad + S * 1.62:.0f}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif">',
       f'<rect width="100%" height="100%" fill="{C["bg"]}"/>', '<defs>']
for tag, mir in (('a', False), ('b', True)):
    out.append(f'<clipPath id="tri{tag}"><polygon points="{poly(tri, mir)}"/></clipPath>')
    out.append(f'<clipPath id="sock{tag}"><polygon points="{poly(cr, mir)}"/></clipPath>')
    out.append(f'<clipPath id="in{tag}"><polygon points="{poly(tri_in, mir)}"/></clipPath>')
    big = np.array([[-3, -3], [3, -3], [3, 3], [-3, 3]])
    out.append(f'<clipPath id="key{tag}"><path clip-rule="evenodd" d="M{poly(big, mir)}Z M{poly(cr * 1.012, mir)}Z"/></clipPath>')
out.append('</defs>')
for tag, mir, side, fill in (('a', False, SIDE, ('hexK', 'kiteK')), ('b', True, -SIDE, ('hexD', 'kiteD'))):
    # flat face ground, then the key tiles, then the socket view, then the rim and the face outline
    out.append(f'<polygon points="{poly(tri, mir)}" fill="#ffffff" stroke="none"/>')
    paths_key = [face_path(f, SIDE) for f in F]                                           # the key = the neighbour-side half rolled out (same footprint on both faces)
    out.append(f'<g clip-path="url(#in{tag})"><g clip-path="url(#key{tag})">')
    for f, pth, k in zip(F, paths_key, kinds):
        if not any(np.sign(V[i] @ n) == -SIDE for i in f): continue
        out.append(f'<polygon points="{poly(pth, mir)}" fill="{C[fill[0] if k == "hex" else fill[1]]}" stroke="{C["line"]}" stroke-width="2.2" stroke-linejoin="round"/>')
    out.append('</g></g>')
    out.append(f'<g clip-path="url(#tri{tag})"><g clip-path="url(#sock{tag})">')
    for f, k in zip(F, kinds):
        if not any(np.sign(V[i] @ n) == side for i in f): continue
        out.append(f'<polygon points="{poly(face_path(f, side), mir)}" fill="{C["hexS"] if k == "hex" else C["kiteS"]}" stroke="{C["line"]}" stroke-width="1.4" stroke-linejoin="round"/>')
    out.append('</g></g>')
    out.append(f'<polygon points="{poly(cr, mir)}" fill="none" stroke="{C["ink"]}" stroke-width="2.4" clip-path="url(#tri{tag})"/>')
    out.append(f'<polygon points="{poly(tri, mir)}" fill="none" stroke="{C["ink"]}" stroke-width="2.6"/>')
    out.append(f'<polygon points="{poly(tri_in, mir)}" fill="none" stroke="{C["muted"]}" stroke-width="1" stroke-dasharray="5 5"/>')
# labels
def txt(q, s, size=17, mir=False, anchor='start', weight=400, col=None):
    x, y = P(q, mir); out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{col or C["ink"]}">{s}</text>')
txt((-0.02, 0.86), 'Keyed W as wallpaper: one keyed face and its neighbouring copy', 22, weight=600)
txt((-0.02, 0.815), 'The OG pattern runs from the socket across the rim onto the flat face, and on into the neighbour W', 15, col=C['muted'])
txt(tri[2] + np.array([0.02, -0.03]), 'T (tetrahedron centre)', 14); txt(tri[1] + np.array([0.03, -0.008]), 'E (octet vertex)', 14)
txt(np.array([-0.025, -0.008]), 'A', 16, anchor='end', weight=600); txt(np.array([-0.025, -0.045]), 'OG centre', 12, anchor='end', col=C['muted'])
txt(np.array([0.80, 0.50]), 'this W: key raised', 16, weight=600); txt(np.array([0.80, 0.50]), 'neighbouring W: key sunk', 16, mir=True, weight=600)
txt(np.array([0.08, 0.20]), 'socket', 14, col=C['muted']); txt(np.array([0.08, 0.20]), 'socket', 14, mir=True, col=C['muted'])
txt(np.array([R + 0.03, -0.05]), 'join (fold line,', 13, col=C['muted']); txt(np.array([R + 0.03, -0.085]), 'opened like a book)', 13, col=C['muted'])
out.append(f'<line x1="{P((0, 0))[0] - 20}" y1="{P((0, 0))[1]}" x2="{P((R, 0))[0] + 20}" y2="{P((R, 0))[1]}" stroke="{C["muted"]}" stroke-dasharray="2 6" stroke-width="1.5"/>')
mm = 39.331442200393894; bar = 10 / mm; bx, by = P((0.0, -0.80))
out.append(f'<line x1="{bx}" y1="{by}" x2="{bx + bar * S}" y2="{by}" stroke="{C["ink"]}" stroke-width="3"/>'); txt((bar + 0.02, -0.807), '10 mm at the print scale (OG kite long edge 9.4 mm)', 13, col=C['muted'])
txt((-0.02, -0.87), 'DICTO · dictospheres.com · keyed-W wallpaper sketch 2026-10-20 · impression, not exact', 13, col=C['muted'])
out.append('</svg>')
svg = '\n'.join(out); open(os.path.join(HERE, '..', 'renders', 'keyed-w-wallpaper.svg'), 'w').write(svg)
key_tiles = sum(1 for f in F if any(np.sign(V[i] @ n) == -SIDE for i in f))
say('drawn: socket faces + rolled-out key tiles from', key_tiles, 'OG faces on the far side; svg bytes', len(svg))
