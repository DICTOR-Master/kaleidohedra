#!/usr/bin/env python3
"""Batch for Concordance 6.1 empty cells (queued 4 Nov, DICTO "keep onto next as queuing"): isoperimetric IQ = 36πV²/A³, Mahler V·V° (about the corner centroid;
Santaló point = centroid for these symmetric sets) and Q4/Q6 for: Delian walk O(t) scan; CO–RD sweep Q6 scan; OG family; Admiral kinds; centre pyramids T, C6, R12, RT;
HexOct fixed h-piece (λ ≥ 3/8). Lindelöf check: for each scan, is the IQ maximum where all facets are equidistant from the centre?"""
import sys, os, json, math, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
sys.path.insert(0, os.path.expanduser('~/study-runs/2026-11-04-tetra-sweep/scripts/_lib')); import methods as M
def meas(P):
    P = np.asarray(P, float); h = ConvexHull(P); c = P[h.vertices].mean(0); Q = P - c; h = ConvexHull(Q)
    pol = np.array([eq[:3]/(-eq[3]) for eq in h.equations]); Vp = ConvexHull(pol).volume
    return {'IQ': 36*math.pi*h.volume**2/h.area**3, 'Mahler': h.volume*Vp, 'Q4': float(M.Q3d(Q[h.vertices], 4)), 'Q6': float(M.Q3d(Q[h.vertices], 6))}
out = {}
RDn = [np.array(p, float) for p in {tuple(s*v for s, v in zip(sg, q)) for q in itertools.permutations((1, 1, 0)) for sg in itertools.product((1, -1), repeat=3)}]
def O_t(t):
    Hs = [[*n, -1.0] for n in RDn] + [[*s, -1.5*(1 - t)] for s in itertools.product((1., -1.), repeat=3)]
    return HalfspaceIntersection(np.array(Hs), np.zeros(3)).intersections
ts = np.linspace(0.0005, 1/3 - 1e-4, 600); rows = [(t, meas(O_t(t))) for t in ts]
iq = max(rows, key=lambda r: r[1]['IQ']); ma = max(rows, key=lambda r: r[1]['Mahler'])
# Lindelöf point: rhombus faces at distance 1/√2, triangles at 1.5(1-t)/√3 -> equal at t = 1 - √2/√3·... solve
tL = 1 - (2/3)*math.sqrt(3)/math.sqrt(2)
out['Delian O(t)'] = {'IQ_max_t': iq[0], 'IQ_max': iq[1]['IQ'], 'Lindelof_t': tL, 'Mahler_max_t': ma[0], 'Mahler_max': ma[1]['Mahler'],
                      'Q6_sign_changes': [round((a[0] + b[0])/2, 4) for a, b in zip(rows, rows[1:]) if (a[1]['Q6'] - 0) * (b[1]['Q6']) < 0]}
# CO–RD sweep: CO ∩ μRD, RD at 1 .. CO at 2 (CO = {|x|+|y|+|z| <= 2, |x_i| <= 1}·?, use cube+octa normals for CO)
CO = [[*e, -1.0] for i in range(3) for e in [np.eye(3)[i], -np.eye(3)[i]]] + [[*s, -2.0] for s in itertools.product((1., -1.), repeat=3)]
def S(mu): return HalfspaceIntersection(np.array(CO + [[*n, -mu] for n in RDn]), np.zeros(3)).intersections
mus = np.linspace(1.001, 1.999, 500); q6 = []
from scipy.special import sph_harm_y
for m in mus:
    P = S(m); u = P/np.linalg.norm(P, axis=1)[:, None]; q6.append(float(sph_harm_y(6, 0, np.arccos(np.clip(u[:, 2], -1, 1)), np.arctan2(u[:, 1], u[:, 0])).mean().real))
out['CO-RD sweep'] = {'Q6_sign_changes': [round((mus[i] + mus[i+1])/2, 4) for i in range(len(mus) - 1) if q6[i]*q6[i+1] < 0]}
d = json.load(open('data/og-family-solids.json'))
out['OG family'] = {nm: meas(d['solids'][nm]['v']) for nm in d['order']}
A = json.load(open('data/admiral-network-pieces.json')); seen = {}
for p in A:
    if p['kind'] not in seen: seen[p['kind']] = meas(np.array([v for f in p['faces'] for v in f]))
out['Admiral kinds'] = seen
phi = (1 + 5**.5)/2
pyr = {'T': [(0,0,0),(1,1,1),(1,-1,-1),(-1,1,-1)], 'C6': [(0,0,0),(.5,.5,.5),(.5,-.5,.5),(.5,-.5,-.5),(.5,.5,-.5)], 'R12': [(0,0,0),(1,0,0),(.5,.5,.5),(0,1,0),(.5,.5,-.5)]}
out['Centre pyramids'] = {k: meas(v) for k, v in pyr.items()}
H = math.sqrt(2/3); hp = [[0,0,0],[0,0.57735027,-H/2],[0,0.57735027,0],[0.5,-0.28867513,-H/2],[0.5,-0.28867513,0],[0.5,0.28867513,-H],[0.5,0.8660254,0],[1,0,0],[1,0.57735027,-H/2],[1,0.57735027,0]]
out['HexOct fixed h-piece'] = meas(hp)
print(json.dumps(out, indent=1)); json.dump(out, open('data/batch-iq-mahler.json', 'w'), indent=1)
