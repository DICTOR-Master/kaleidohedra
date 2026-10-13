# Builds src/krp-core/src/polyhedra/kits13.js (DICTO 2026-10-13, docs/PLAN-13.md stage 3): every 13 kit as Polyhedraverse pieces
# plus placements, from the centre out. A kit shape reuses a catalogue piece when exactly congruent (same size); otherwise it is
# a new DICTO piece (mirror twins as their own piece). Also the RD 13 centres at four thicknesses as a graded set.
# Usage: python3 scripts/build-kits13.py thirteens-raw.json catalogue.json <free-centre jsons for the graded set: 0.08 0.25 0.35 ...>
import sys, json, numpy as np
sys.path.insert(0, 'scripts')
from importlib import import_module
ks = import_module('kit-shapes')
raw, cat = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
# More kits from other worlds (OCTET_RAW: the DICTO Icosahedral Octet's, scripts/dump-octet-kits.mjs), in their own group.
import os
GROUP = {k: '13' for k in raw}
if os.environ.get('OCTET_RAW'):
    extra = json.load(open(os.environ['OCTET_RAW'])); raw.update(extra); GROUP.update({k: 'octet' for k in extra})
D = np.diag([-1.0, 1, 1])
NAMES = {'axe': 'AXE', 'fuji': 'FUJI', 'cleo': 'Cleo', 'hasu': 'Hasu', 'vajra': 'VAJRA', 'j11': 'J11', 'B1': 'Vajra (fine)', 'B2': 'Chatra',
         'B3': 'Mudra', 'B4': 'Crown Jewel', 'B5L': 'Diadem', 'wedge': 'Dodeca-13 wedge', 'needle': 'Dodeca-13 needle', 'unit': 'Dodeca-13 unit',
         'star': 'Dodeca-13 star', 'ico': 'Icosahedron', 'dodeca': 'Dodecahedron', 'idd': 'Icosidodecahedron', 'j63': 'J63',
         'copy': 'Rhombic triacontahedron', 'centre': 'Centre', 'admiral': 'Admiral Cap', 'icoSmall': 'Icosahedron', 'weirdstone': 'Weirdstone', 'tadpole': 'Tadpole', 'tet': 'Octet tetrahedron',
         'bilinski13Centre': 'Bilinski dodecahedron', 'bilinski13Cell': 'Bilinski dodecahedron',
         'rd': 'Rhombic dodecahedron', 'rdCentre': 'Spheroid-13 RD centre', 'rdA': 'Spheroid-13 RD outer A', 'rdB': 'Spheroid-13 RD outer B'}
def quat(R):
    # Shepperd's method: build from the largest of w, x, y, z, so half-turns (w = 0) come out right.
    tr = np.trace(R)
    m = max(range(4), key=lambda i: [tr, R[0, 0], R[1, 1], R[2, 2]][i])
    if m == 0:
        w = np.sqrt(1 + tr) / 2; x, y, z = (R[2, 1] - R[1, 2]) / (4 * w), (R[0, 2] - R[2, 0]) / (4 * w), (R[1, 0] - R[0, 1]) / (4 * w)
    elif m == 1:
        x = np.sqrt(1 + 2 * R[0, 0] - tr) / 2; w, y, z = (R[2, 1] - R[1, 2]) / (4 * x), (R[0, 1] + R[1, 0]) / (4 * x), (R[0, 2] + R[2, 0]) / (4 * x)
    elif m == 2:
        y = np.sqrt(1 + 2 * R[1, 1] - tr) / 2; w, x, z = (R[0, 2] - R[2, 0]) / (4 * y), (R[0, 1] + R[1, 0]) / (4 * y), (R[1, 2] + R[2, 1]) / (4 * y)
    else:
        z = np.sqrt(1 + 2 * R[2, 2] - tr) / 2; w, x, y = (R[1, 0] - R[0, 1]) / (4 * z), (R[0, 2] + R[2, 0]) / (4 * z), (R[1, 2] + R[2, 1]) / (4 * z)
    q = np.array([x, y, z, w]); return (q / np.linalg.norm(q)).tolist()
def edge(V, F):
    return np.mean([np.linalg.norm(np.array(V[f[i]]) - np.array(V[f[(i + 1) % len(f)]])) for f in F for i in range(len(f))])
new = {}            # id -> {name, vertices, faces}
# Shapes compared by corner count and distances from the middle, with a small tolerance (exact rounding split equal shapes, 2026-10-13).
def same_sig(a, b): return a[0] == b[0] and max(abs(x - y) for x, y in zip(a[1], b[1])) < 1e-3
def find(V, F, role, kind, thick):
    """A piece id and A, b with V = A @ S + b for that piece's vertices S (A a rotation)."""
    for cid, c in list(cat.items()) + [(k, {'vertices': v['vertices']}) for k, v in new.items()]:
        S = np.array(c['vertices'], float)
        if not same_sig(ks.signature(S), ks.signature(V)): continue
        m = ks.match(S, V)
        if m: return cid, m[0], m[1]
    # a mirror image of a piece already made is that piece's mirror twin, not a new piece
    for nid, nv in list(new.items()):
        if nid.endswith('_M'): continue
        Sm = np.array(nv['vertices'], float) @ D
        if not same_sig(ks.signature(Sm), ks.signature(V)): continue
        m = ks.match(Sm, V)
        if m: return mirror_id(nid), m[0], m[1]
    base = f"KIT13_{kind.upper()}_{role.upper()}" + (f"_{thick}" if thick else '')
    while base in new: base += 'X'      # never overwrite a piece already made (its placements depend on it)
    tag = {'T15': '0.15, exact RD centre', 'T35': '0.35, exact RD centre', 'T15F': '0.15, free centre'}.get(thick, thick.replace('T', '0.') if thick else '')
    name = NAMES.get(role, role) + (f' ({tag})' if thick else '')
    if role in ('ico', 'dodeca', 'idd', 'copy', 'centre', 'icoSmall', 'tet'): name += f' (edge {edge(V, F):.3f})'
    c = V.mean(0); new[base] = {'name': name, 'vertices': (V - c).tolist(), 'faces': F}
    return base, np.eye(3), c
def mirror_id(pid):
    if pid.endswith('_M') and (pid[:-2] in new or pid[:-2] in cat): return pid[:-2]   # the twin of a twin is the piece itself
    mid = pid + '_M'
    if mid not in new:
        src = new[pid] if pid in new else cat[pid]
        nm = src['name'].replace('Diadem', 'Diadem R') if 'Diadem' in src['name'] else src['name'] + ' (mirror)'
        if pid in new and 'Diadem' in new[pid]['name'] and 'Diadem L' not in new[pid]['name']: new[pid]['name'] = new[pid]['name'].replace('Diadem', 'Diadem L')
        new[mid] = {'name': nm, 'vertices': (np.array(src['vertices']) @ D).tolist(), 'faces': [list(reversed(f)) for f in (src.get('faces') or new[pid]['faces'])]}
    return mid
LABEL = {'octet': 'DICTO Icosahedral Octet', 'icosa13': 'DICTO Icosa-13', 'dodeca13': 'DICTO Dodeca-13', 'bodhi': 'The Bodhi Seed', 'unity': 'UNITY', 'dictoStar': 'DICTO-Star', 'deshi': 'DESHI', 'rd13': 'RD 13', 'hexed': 'Regular-hexagon ED 13', 'to13': 'Truncated octahedron 13', 'skewedRd13': 'DICTO skewed RD 13', 'bainRd13': 'Bain RD 13', 'bilinski13': 'Bilinski 13', 'jewel13': 'DICTO Jewel 13'}
KITLABEL = {'octahedron': 'octahedron cell', 'tetrahedron': 'tetrahedron cell', 'octetBlock': 'octet block', 'allIcoBlock': 'all-icosahedral block', 'pieces': 'pieces', 'build': '63-piece build', 'units': 'units', 'stars': 'stars', 'seed': '13 triacontahedra', 'kitA': 'Kit A', 'kitB': 'Kit B',
            'open': 'open', 'venus': 'VENUS', 'star': '', 'deshi': '', 'cluster': 'centre and twelve', 'withStellas': 'with the 6 stella octangulas', 'plain': 'plain', 'rounded': 'DICTO Spheroid-13 RD (0.15)', 'fattest': 'Spheroid-13 RD, fattest (0.35)', 'roundedFree': 'Spheroid-13 RD, free centre (0.15)'}
kits = {}
for kind, views in raw.items():
    for view, pieces in views.items():
        if view == 'blocks': continue
        thick = {'rounded': 'T15', 'fattest': 'T35', 'roundedFree': 'T15F'}.get(view, '')
        shapes, entries = ks.classify(pieces)
        ids = []
        for s in shapes: ids.append(find(s['V'], s['F'], s['role'], kind, thick))
        allV = np.array([v for _, V, _ in pieces for v in V], float)
        cen = np.array(pieces[0][1], float).mean(0)       # the first piece is the centre of every 13
        out = []
        for e in entries:
            pid, A, b = ids[e['shape']]
            R, t = e['R'], e['t']
            if e['mirror']:
                # R already includes the mirror: v = R (A s + b) + t = (R A D)(D s) + R b + t, D s being the mirror piece's corners
                pid = mirror_id(pid); rot = R @ A @ D; pos = R @ b + t
            else:
                rot = R @ A; pos = R @ b + t
            out.append({'shape': pid, 'position': (pos - cen).round(9).tolist(), 'quaternion': quat(rot)})
        out.sort(key=lambda o: np.linalg.norm(o['position']))
        kits[f'{kind}.{view}'] = {'label': ' · '.join(x for x in [LABEL[kind], KITLABEL.get(view, view)] if x), 'group': GROUP[kind], 'entries': out}
# The graded set (DICTO 2026-10-13): the free centres at each thickness given (the exact centres are plain rhombic dodecahedra).
for fn in sys.argv[3:]:
    R = json.load(open(fn)); faces = R['cells'][0]; tag = 'T%02d' % round(R['margin'] * 100)
    V, F = [], []
    for f in faces:
        idx = []
        for p in f:
            k = next((i for i, w in enumerate(V) if np.allclose(w, p, atol=1e-7)), None)
            if k is None: V.append(p); k = len(V) - 1
            idx.append(k)
        F.append(idx)
    V = np.array(V)
    pid, _, _ = find(V, F, 'rdCentre', 'rd13', tag + 'F')
    new[pid]['name'] = f'Spheroid-13 RD free centre ({R["margin"]})' if pid in new and pid.startswith('KIT13') else new.get(pid, {}).get('name')
print(len(new), 'new pieces;', sum(1 for k in kits.values() for e in k['entries'] if e['shape'] in cat), 'placements reuse catalogue pieces')
for k, v in kits.items():
    from collections import Counter
    print(f"{k:18s} {len(v['entries']):4d}  " + ', '.join(f'{n}×{c}' for c, n in Counter(e['shape'] for e in v['entries']).items()))
js = ['// Generated by scripts/build-kits13.py (the 13s kits, docs/PLAN-13.md stage 3). Do not edit.',
      "import { specOf } from './stellaJewel.js';",
      'const RAW = ' + json.dumps({k: v for k, v in new.items()}, separators=(',', ':')) + ';',
      'export const KIT13_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, specOf(id, p.name, p.vertices, p.faces, false, 1)]));',
      'export const KIT13_ADDITION_IDS = Object.keys(KIT13_ADDITIONS);',
      '/** kit id -> { label, entries: [{ shape, position, quaternion }] }, from the centre out. */',
      'export const KITS13 = ' + json.dumps(kits, separators=(',', ':')) + ';', '']
open('src/krp-core/src/polyhedra/kits13.js', 'w').write('\n'.join(js))
