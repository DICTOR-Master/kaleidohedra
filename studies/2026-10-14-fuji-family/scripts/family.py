# The FUJI family (DICTO, 2026-10-14): hexagonal pyramids with all six side edges 1 on a flat-ended triangle (an equiangular
# hexagon with sides 1 and r alternating, 0 <= r <= 1). r = 0: regular tetrahedron; r = 1/phi: FUJI; r = 1: flat (regular hexagon).
# Computes height, volume and dihedral angles across r, and checks FUJI against the Icosa-13 study data. DICTO · dictospheres.com
import json, math, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2

def pyramid(r):
    # flat-ended triangle: big triangle of side 1 + 2r with corners of side r cut off; long sides 1, short sides r
    R2 = (1 + r + r * r) / 3; R = math.sqrt(R2); h = math.sqrt(max(0.0, 1 - R2))
    # corners on the circle: long side subtends angle a, short side b, 3a + 3b = 2 pi, chord 2R sin(a/2) = 1
    a = 2 * math.asin(min(1.0, 1 / (2 * R))); b = 2 * math.pi / 3 - a
    ang, P = 0.0, []
    for i in range(3):
        P.append((R * math.cos(ang), R * math.sin(ang), 0.0)); ang += a
        P.append((R * math.cos(ang), R * math.sin(ang), 0.0)); ang += b
    V = np.array(P + [(0.0, 0.0, h)])
    F = [[0, 1, 2, 3, 4, 5][::-1]] + [[i, (i + 1) % 6, 6] for i in range(6)]
    return V, F, h

def dihedral(V, F, e):
    fs = [f for f in F if e[0] in f and e[1] in f and (abs(f.index(e[0]) - f.index(e[1])) in (1, len(f) - 1))]
    def n(f):
        c = V[f].mean(0); m = sum(np.cross(V[f[i]] - c, V[f[(i + 1) % len(f)]] - c) for i in range(len(f))); return m / np.linalg.norm(m)
    return math.degrees(math.pi - math.acos(np.clip(n(fs[0]) @ n(fs[1]), -1, 1)))

def facts(r):
    V, F, h = pyramid(r)
    area = math.sqrt(3) / 4 * (1 + 4 * r + r * r)
    out = dict(r=r, height=h, volume=area * h / 3, baseArea=area)
    if h > 1e-12:
        out['baseLong'] = dihedral(V, F, (0, 1)); out['baseShort'] = dihedral(V, F, (1, 2))
        out['sideAtLong'] = dihedral(V, F, (0, 6)); out['apexAngles'] = [math.degrees(math.acos(np.clip((V[i] - V[6]) @ (V[(i + 1) % 6] - V[6]), -1, 1))) for i in (0, 1)]
    return out

rows = [facts(r) for r in (0, 0.25, 1 / phi ** 2, 0.5, 1 / phi, 0.75, 1)]
fuji = facts(1 / phi)
chk = dict(
    tetrahedron_r0=abs(rows[0]['height'] - math.sqrt(2 / 3)) < 1e-12 and abs(rows[0]['baseLong'] - math.degrees(math.acos(1 / 3))) < 1e-9,
    fuji_height=abs(fuji['height'] - 1 / math.sqrt(3)) < 1e-12,
    fuji_volume=abs(fuji['volume'] - (1 + 3 * 5 ** .5) / 24) < 1e-12,
    fuji_base_long_alpha=abs(fuji['baseLong'] - math.degrees(math.acos(5 ** .5 / 3))) < 1e-9,
    fuji_base_short_delta=abs(fuji['baseShort'] - 37.3774) < 1e-3,
    flat_r1=rows[-1]['height'] < 1e-12)
# against the study's FUJI
D = json.load(open(os.path.join(ROOT, '..', '2026-10-10-icosa-13', 'data', 'ico13-hex-pyramid-unit.json')))
E = sorted(round(float(np.linalg.norm(np.array(D['vertices'][f[i]]) - np.array(D['vertices'][f[(i + 1) % len(f)]]))), 6) for f in D['faces'] for i in range(len(f)))
V, F, h = pyramid(1 / phi)
E2 = sorted(round(float(np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]])), 6) for f in F for i in range(len(f)))
chk['matches_study_FUJI_edges'] = E == E2
json.dump(dict(credit='DICTO · dictospheres.com', rows=rows, checks=chk), open(os.path.join(ROOT, 'family.json'), 'w'), indent=1)
for x in rows: print({k: (round(v, 5) if isinstance(v, float) else [round(t, 4) for t in v] if isinstance(v, list) else v) for k, v in x.items()})
print(chk)
