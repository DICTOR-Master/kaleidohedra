# Builds src/app/octet-data.js for the DICTO Icosahedral Octet world (DICTO 2026-10-13; DISCOVERIES F21, studies
# 2026-10-10-icosa-networks-2/-3): the cells (octahedron = icosahedron + 6 Admiral Caps; tetrahedron plain, or icosahedron(1/2) +
# 4 Weirdstones + 6 Tadpoles; the Frog Chorus gap star; the Lotus Jewel and its void dodecahedron; the Unborn, the 8 Tricaps of an
# icosahedron and the AXE of the gap, study 2026-10-23-axe-gap), each in its own frame. The world repeats them on their lattices at run
# time (a size slider). Names by DICTO. Usage: python3 scripts/build-octet-data.py
import json, numpy as np
S2, S3 = 'studies/2026-10-10-icosa-networks-2/data/', 'studies/2026-10-10-icosa-networks-3/data/'
S4 = 'studies/2026-10-23-axe-gap/data/'
PHI = (1 + 5 ** 0.5) / 2; A = PHI ** 2
def load(f): return json.load(open(f))
def merge_pairs(parts):
    """Join pieces that share a whole face into one solid (the shared face drops out)."""
    pieces = [(np.array(p['vertices'], float), [list(f) for f in p['faces']]) for p in parts]
    used, out = set(), []
    def key(V, f): return tuple(sorted(tuple(np.round(V[i], 6)) for i in f))
    for i, (Vi, Fi) in enumerate(pieces):
        if i in used: continue
        ki = {key(Vi, f): f for f in Fi}
        for j in range(i + 1, len(pieces)):
            if j in used: continue
            Vj, Fj = pieces[j]; kj = {key(Vj, f): f for f in Fj}
            shared = set(ki) & set(kj)
            if not shared: continue
            V = [tuple(np.round(v, 9)) for v in Vi]
            idx = lambda p: V.index(p) if p in V else (V.append(p) or len(V) - 1)
            F = [f for k, f in ki.items() if k not in shared]
            F += [[idx(tuple(np.round(Vj[t], 9))) for t in f] for k, f in kj.items() if k not in shared]
            used |= {i, j}; out.append((np.array(V), F)); break
        else:
            used.add(i); out.append((Vi, Fi))
    return out
def part(role, V, F, centre): return [role, (np.asarray(V) - centre).round(7).tolist(), [list(map(int, f)) for f in F]]
cells = {}
# octahedron cell: centred at the origin already
oc = load(S2 + 'octahedron-ico-parts-unit.json')['parts']
cells['oct'] = [part('ico', p['vertices'], p['faces'], 0) for p in oc if p['role'] == 'ico'] + \
               [part('admiral', V, F, 0) for V, F in merge_pairs([p for p in oc if p['role'] == 'roof'])]
# tetrahedron cells, centred, in the orientation of the site a/4 (1,1,1)
tc = load(S3 + 'tet-ico-parts-unit.json')['parts']
ct = np.array([v for p in tc for v in p['vertices']]).mean(0)
cells['tetIco'] = [part('icoSmall', p['vertices'], p['faces'], ct) for p in tc if p['role'] == 'ico-small'] + \
                  [part('weirdstone', p['vertices'], p['faces'], ct) for p in tc if p['role'] == 'corner-cap'] + \
                  [part('tadpole', V, F, ct) for V, F in merge_pairs([p for p in tc if p['role'] == 'edge-cap'])]
blk = load(S2 + 'octet-ico-parts-unit.json')['parts']
tet = next(p for p in blk if p['role'] == 'tet' and np.allclose(np.array(p['vertices']).mean(0), np.array([-1, -1, 1]) * A / 4, atol=1e-5))
# that tetrahedron has the same orientation class as a/4 (1,1,1) (sum of signs 3 mod 4); move it to the origin
cells['tet'] = [part('tet', tet['vertices'], tet['faces'], np.array(tet['vertices']).mean(0))]
g = load(S3 + 'octet-gap-star-unit.json')
cells['frog'] = [part('frog', g['vertices'], g['faces'], np.array([A / 2, 0, 0]))]
# Lotus Jewel network: clawed icosahedra on the simple cubic lattice (spacing phi), void dodecahedra at the cube centres
cl = load(S3 + 'clawed-icosahedron-unit.json')
cells['lotusJewel'] = [part('lotusJewel', cl['vertices'], cl['faces'], np.array(cl['vertices']).mean(0))]
sc = load(S2 + 'sc-clawed-parts-unit.json')['parts'] if False else load(S3 + 'sc-clawed-parts-unit.json')['parts']
dod = next(p for p in sc if p['role'] == 'dodeca'); dc = np.array(dod['vertices']).mean(0)
cells['voidDodeca'] = [part('voidDodeca', dod['vertices'], dod['faces'], dc)]
print('void dodecahedron centre / (phi/2):', np.round(dc / (PHI / 2), 4))
# The AXE gap (DICTO 2026-10-23, study 2026-10-23-axe-gap): the Unborn (the void dodecahedron minus its 8 Tricaps), the 8 Tricaps of the
# icosahedron at the origin (in its frame), and the cell's 6 AXE as three pairs, one per cell face, each pair in the frame of its face's
# centre (the face between the voids at -/+ (phi/2) along that axis: x for axeX, ...). Icosahedron + Unborn + 6 AXE, or Lotus Jewel +
# dodecahedron + 6 AXE, or Lotus Jewel + 8 Tricaps + Unborn + 6 AXE, fill each cell of the simple cubic lattice (point tests in the study).
ax = load(S4 + 'axe-cell-parts-unit.json')['parts']
un = next(p for p in ax if p['role'] == 'unborn'); uc = np.array(un['vertices']).mean(0)
cells['unborn'] = [part('unborn', un['vertices'], un['faces'], uc)]
cells['tricap'] = [part('tricap', p['vertices'], p['faces'], 0) for p in ax if p['role'] == 'tricap']
for a, name in enumerate(['axeX', 'axeY', 'axeZ']):
    fc = np.full(3, PHI / 2); fc[a] = 0
    cells[name] = [part('axe', p['vertices'], p['faces'], fc) for p in ax if p['role'] == 'axe' and p['faceAxis'] == a]
# checks: the Unborn's corners are the void dodecahedron's 12 non-cube corners; each Tricap's apex is a cube corner of a void dodecahedron
# and its base a face of the icosahedron; the Lotus Jewel's corners are the icosahedron's 12 and the 8 apexes; two AXE per face.
rk = lambda P: {tuple(np.round(p, 5)) for p in np.asarray(P)}
D = rk(np.array(dod['vertices']) - dc); Uc = rk(cells['unborn'][0][1]); ico = rk(cells['oct'][0][1])
assert len(Uc) == 12 and Uc <= D and len(D - Uc) == 8, 'Unborn = void dodecahedron minus its cube corners'
apex = [min(t[1], key=lambda v: np.linalg.norm(v)) for t in cells['tricap']]
assert len(cells['tricap']) == 8 and all(rk([np.array(a) - np.sign(a) * PHI / 2]) <= D for a in apex), 'Tricap apexes on the dodecahedra'
assert all(rk(t[1]) - rk([a]) <= ico for t, a in zip(cells['tricap'], apex)), 'Tricap bases on the icosahedron'
lj = cells['lotusJewel'][0]
assert rk([lj[1][i] for i in {i for f in lj[2] for i in f}]) == ico | rk(apex), 'Lotus Jewel = icosahedron minus its 8 Tricaps (corners)'
assert all(len(cells[n]) == 2 for n in ['axeX', 'axeY', 'axeZ']), 'two AXE per face'
print('AXE gap checks passed: Unborn 12 corners of the dodecahedron, 8 Tricaps, Lotus Jewel corners, 2 AXE per face')
for k, v in cells.items(): print(k, [(p[0], len(p[1]), len(p[2])) for p in v][:8], len(v))
data = {'a': A, 'phi': PHI, 'cells': cells}
open('src/app/octet-data.js', 'w').write('// Generated by scripts/build-octet-data.py (DICTO Icosahedral Octet, DISCOVERIES F21). Do not edit.\nexport default ' + json.dumps(data, separators=(',', ':')) + ';\n')
