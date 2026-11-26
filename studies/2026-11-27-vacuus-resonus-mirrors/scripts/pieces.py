"""Step 2 (27 Nov 2026): how many piece shapes per mirror chamber? With Claude (Anthropic). Exact (K arithmetic).
For a solid P and its dual P*, all planes A = Vacuus and Resonus of both (through O). Any gap between two such shapes is cut by A
into pieces; adding the mirror planes M, the pieces inside ONE mirror chamber are the different shapes (every other piece is a
mirror image of one of them). On the sphere a chamber is a triangle and each plane of A that crosses it is a great-circle chord, so
pieces per chamber = 1 + L + sum over crossing points inside (m - 1) (L chords; m chords through a point). Total pieces = that x
number of chambers (2 x mirrors-group order / 2 = group order |G|: 24 T_d, 48 O_h, 120 I_h)."""
import os, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mirrors.py')).read()
exec(src[:src.index('rows = []')])
def planes_of(V):
    F = faces(V); edges = set()
    for idx, N, d in F:
        for i in range(len(idx)): edges.add(frozenset((idx[i], idx[(i + 1) % len(idx)])))
    vac, res = [], []
    for e in edges:
        a, b = tuple(e); add(vac, cross(V[a], V[b]))
    for idx, N, d in F: add(res, N)
    return vac, res
def mirrors_of(V):
    cand, mir = [], []
    R2 = [dot(v, v) for v in V]
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            if R2[i] == R2[j]: add(cand, sub(V[i], V[j]))
    return [m for m in cand if all(has(V, reflect(v, m)) for v in V)]
def sg(x): return x.sign()
def chamber_count(planes, mir, field_one):
    o = field_one
    g = (o * 1000003, o * 2000029 + o * 17 / 31, o * 3700019 + o * 5 / 7)   # generic point (rational offsets)
    gs = [sg(dot(m, g)) for m in mir]; assert 0 not in gs
    # corners of the chamber: directions on two mirrors, weakly inside all
    cor = []
    for i in range(len(mir)):
        for j in range(i + 1, len(mir)):
            d = cross(mir[i], mir[j])
            for dd in (d, scl(-1, d)):
                if all(sg(dot(m, dd)) in (0, s) for m, s in zip(mir, gs)) and not any(same_dir(dd, c) and sg(dot(dd, c)) > 0 for c in cor):
                    cor.append(dd)
    assert len(cor) == 3, len(cor)
    extra = [p for p in planes if not any(same_dir(p, m) for m in mir)]
    cut = [p for p in extra if len({sg(dot(p, c)) for c in cor} - {0}) == 2]
    pts = []   # interior crossing points with multiplicity
    for i in range(len(cut)):
        for j in range(i + 1, len(cut)):
            d = cross(cut[i], cut[j])
            for dd in (d, scl(-1, d)):
                if all(sg(dot(m, dd)) == s for m, s in zip(mir, gs)):
                    for P in pts:
                        if same_dir(P[0], dd) and sg(dot(P[0], dd)) > 0: P[1].update((i, j)); break
                    else: pts.append([dd, {i, j}])
    return 1 + len(cut) + sum(len(s) - 1 for d_, s in pts), len(cut), len(extra)
PAIRS = [('cube', 'octahedron'), ('dodecahedron', 'icosahedron'), ('tetrahedron', 'tetrahedron (dual)')] + [(a, CAT[a]) for a in ARCH]
SD = dict(SOL)
SD['tetrahedron (dual)'] = [scl(-1, v) for v in SD['tetrahedron']]
G = {6: 24, 9: 48, 15: 120}
out = []
for a, b in PAIRS:
    Va, Vb = SD[a], SD[b]; mir = mirrors_of(Va)
    pa, pb = planes_of(Va), planes_of(Vb)
    allp = []
    for p in pa[0] + pa[1] + pb[0] + pb[1]: add(allp, p)
    one = Va[0][0] * 0 + 1
    n1, L, ne = chamber_count(allp, mir, one)
    al = []
    for p in pa[0] + pa[1]: add(al, p)       # a plane can be both Vacuus and Resonus: count it once
    sa = chamber_count(al, mir, one)[0]
    out.append(dict(pair=f'{a} + {b}', planes=len(allp), mirrors=len(mir), extra_planes=ne, shapes_per_chamber=n1, pieces=n1 * G[len(mir)], first_alone=sa))
    print(f'{a} + {b}: planes {len(allp)} (mirrors {len(mir)}, others {ne}); chords in a chamber {L}; piece shapes per chamber {n1}; '
          f'pieces in all {n1 * G[len(mir)]}  (first solid alone: {sa} per chamber)', flush=True)
co = [r for r in out if r['pair'] == 'cube + octahedron'][0]
print('control (by hand): cube + octahedron -> 2 shapes per chamber, 96 pieces:', co['shapes_per_chamber'] == 2 and co['pieces'] == 96)
import json; json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pieces.json'), 'w'), indent=1)
print('alone <= pair everywhere:', all(r['first_alone'] <= r['shapes_per_chamber'] for r in out))
print('FINAL ok' if co['shapes_per_chamber'] == 2 and all(r['first_alone'] <= r['shapes_per_chamber'] for r in out) else 'FINAL FAIL (control)')
