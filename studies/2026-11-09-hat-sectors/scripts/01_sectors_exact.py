# Task 1: exact geometry of the RD (cubic stacking c) and TRD (hexagonal stacking h) about the stacking axis.
# RD: vertices (+-1,0,0) perms and (+-1/2,+-1/2,+-1/2) (Voronoi cell of fcc (+-1,+-1,0), volume 2).
# Frame: z along [111]; heights h = (x+y+z)/sqrt3 lie in Q(sqrt3); horizontal coords in Q(sqrt2, sqrt3).
# TRD: hull of the RD's upper half-cell and its mirror in h = 0 (hcp Voronoi cell, layer with B above and below).
import itertools, sympy as sp
S3, S2, S6 = sp.sqrt(3), sp.sqrt(2), sp.sqrt(6)
ez = sp.Matrix([1, 1, 1]) / S3
ex = sp.Matrix([2, -1, -1]) / S6
ey = sp.Matrix([0, 1, -1]) / S2
R = lambda v: sp.Matrix([sp.nsimplify(ex.dot(v)), sp.nsimplify(ey.dot(v)), sp.nsimplify(ez.dot(v))]).applyfunc(sp.radsimp)
H = sp.Rational(1, 2)
RDv = [sp.Matrix(p) for p in set(itertools.permutations([1, 0, 0])) | set(itertools.permutations([-1, 0, 0]))]
RDv += [sp.Matrix([a, b, c]) for a in (H, -H) for b in (H, -H) for c in (H, -H)]
RD = [R(v) for v in RDv]
up = [v for v in RD if v[2] >= 0]
TRD = list({tuple(v) for v in up} | {(v[0], v[1], -v[2]) for v in up})
TRD = [sp.Matrix(v) for v in TRD]
checks = []
def ok(name, cond):
    checks.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

def faces(V):
    out = {}
    for a, b, c in itertools.combinations(range(len(V)), 3):
        n = (V[b] - V[a]).cross(V[c] - V[a]).applyfunc(sp.radsimp)
        if n.norm() == 0: continue
        d = sp.radsimp(n.dot(V[a]))
        s = [sp.sign(sp.radsimp(n.dot(v) - d)) for v in V]
        if all(x <= 0 for x in s) or all(x >= 0 for x in s):
            if all(x >= 0 for x in s): n, d = -n, -d
            k = n / n.norm(); kd = sp.radsimp(d / n.norm())
            key = tuple(sp.nsimplify(sp.radsimp(t)) for t in list(k) + [kd])
            out[key] = (k.applyfunc(sp.radsimp), kd)
    return list(out.values())

def top(F, x, y):
    return sp.radsimp(min((kd - k[0] * x - k[1] * y) / k[2] for k, kd in F if sp.simplify(k[2]) > 0))
def bot(F, x, y):
    return sp.radsimp(max((kd - k[0] * x - k[1] * y) / k[2] for k, kd in F if sp.simplify(k[2]) < 0))

rho = S6 / 3                       # hexagon circumradius
apo = S2 / 2                       # apothem
ang = lambda k: sp.pi * k / 3
Vpt = [(rho * sp.cos(ang(k)), rho * sp.sin(ang(k))) for k in range(6)]
Mpt = [(apo * sp.cos(ang(k) + sp.pi / 6), apo * sp.sin(ang(k) + sp.pi / 6)) for k in range(6)]
res = {}
for name, V in (('RD', RD), ('TRD', TRD)):
    F = faces(V)
    ok(f'{name}: 14 corners, 12 faces', len(V) == 14 and len(F) == 12)
    vert = [f for f in F if sp.simplify(f[0][2]) == 0]
    ok(f'{name}: exactly 6 faces vertical (normal perpendicular to the stacking axis)', len(vert) == 6)
    rad = sorted({sp.radsimp(sp.sqrt(v[0] ** 2 + v[1] ** 2)) for v in V})
    ok(f'{name}: horizontal radii of corners = {{0, sqrt6/3}} -> projection is the regular hexagon', rad == [0, rho])
    # corner directions: 12 non-axial corners over the 6 hexagon vertices, 2 per vertex
    over = {}
    for v in V:
        if v[0] == 0 and v[1] == 0: continue
        k = [kk for kk in range(6) if sp.simplify(v[0] - Vpt[kk][0]) == 0 and sp.simplify(v[1] - Vpt[kk][1]) == 0]
        ok(f'{name}: corner {list(v)} lies over a hexagon vertex', len(k) == 1)
        over.setdefault(k[0], []).append(v[2])
    # mid-section h = 0: on the walls, the section is the hexagon itself (walls are vertical over its edges)
    midT = [top(F, *p) for p in Vpt]; midB = [bot(F, *p) for p in Vpt]
    ok(f'{name}: mid-section h=0 is the full hexagon (T>0>B at all 6 vertices)', all(t > 0 for t in midT) and all(b < 0 for b in midB))
    TC, BC = top(F, 0, 0), bot(F, 0, 0)
    TM = [top(F, *p) for p in Mpt]; BM = [bot(F, *p) for p in Mpt]
    print(f'  {name} relief  C: [{BC}, {TC}]   M: ' + ', '.join(f'[{b},{t}]' for b, t in zip(BM, TM)))
    print(f'  {name} relief  V: ' + ', '.join(f'k{k}:[{b},{t}]' for k, (b, t) in enumerate(zip(midB, midT))))
    # piecewise linearity: each kite (C, M_{k-1}, V_k, M_k) split by C-V into two triangles; T and B linear on each
    lin = True; vols = []
    for k in range(6):
        Mp, Mn = Mpt[(k - 1) % 6], Mpt[k]
        tri = [((0, 0), Mp, Vpt[k]), ((0, 0), Vpt[k], Mn)]
        vol = 0
        for t3 in tri:
            for wts in [(sp.Rational(1, 3),) * 3, (H, H, 0), (0, H, H), (H, 0, H), (sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 4))]:
                x = sum(w * p[0] for w, p in zip(wts, t3)); y = sum(w * p[1] for w, p in zip(wts, t3))
                for f in (top, bot):
                    val = f(F, x, y); interp = sum(w * f(F, *p) for w, p in zip(wts, t3))
                    if sp.simplify(val - interp) != 0: lin = False
            area = sp.Abs(((t3[1][0] - t3[0][0]) * (t3[2][1] - t3[0][1]) - (t3[2][0] - t3[0][0]) * (t3[1][1] - t3[0][1])) / 2)
            vol += area * sum(top(F, *p) - bot(F, *p) for p in t3) / 3
        vols.append(sp.nsimplify(sp.radsimp(sp.simplify(vol))))
    ok(f'{name}: relief linear on the two triangles of every kite (crease only along C-V)', lin)
    ok(f'{name}: 6 sector volumes sum to the cell volume 2', sp.simplify(sum(vols) - 2) == 0)
    print(f'  {name} sector volumes k0..k5: {vols}  (fractions of the cell: {[v / 2 for v in vols]})')
    res[name] = dict(TC=TC, BC=BC, TM=TM, BM=BM, TV=midT, BV=midB, vols=vols)

rd, trd = res['RD'], res['TRD']
ok('RD: walls at every M run from -sqrt3/4 to sqrt3/4; at C from -sqrt3/2 to sqrt3/2',
   all(sp.simplify(t - S3 / 4) == 0 for t in rd['TM']) and all(sp.simplify(b + S3 / 4) == 0 for b in rd['BM']) and sp.simplify(rd['TC'] - S3 / 2) == 0)
hi, lo = 1 / S3, 1 / (2 * S3)
ok('RD: sector V-relief alternates (top 1/sqrt3, bottom -1/(2sqrt3)) and (top 1/(2sqrt3), bottom -1/sqrt3)',
   all(sp.simplify(rd['TV'][k] - (hi if k % 2 == 0 else lo)) == 0 and sp.simplify(rd['BV'][k] + (lo if k % 2 == 0 else hi)) == 0 for k in range(6)))
ok('RD: alternate sectors are each other turned upside down (h -> -h swaps the two reliefs); all 6 volumes 1/3',
   all(v == sp.Rational(1, 3) for v in rd['vols']))
ok('TRD: sector V-relief alternates fat [-1/sqrt3, 1/sqrt3] and thin [-1/(2sqrt3), 1/(2sqrt3)] (each sector is its own mirror in h=0)',
   all(sp.simplify(trd['TV'][k] - (hi if k % 2 == 0 else lo)) == 0 and sp.simplify(trd['BV'][k] + (hi if k % 2 == 0 else lo)) == 0 for k in range(6)))
ok('TRD: the two sector kinds are NOT congruent (volumes 13/36 and 11/36)',
   sorted(set(trd['vols'])) == [sp.Rational(11, 36), sp.Rational(13, 36)])
ok('RD and TRD: upper halves identical relief (the shared half-cell)',
   all(sp.simplify(a - b) == 0 for a, b in zip(rd['TV'], trd['TV'])) and all(sp.simplify(a - b) == 0 for a, b in zip(rd['TM'], trd['TM'])))
bad = [n for n, c in checks if not c]
print('FINAL ok' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
