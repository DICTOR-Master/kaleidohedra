# Five pyramids study, question 2 (DICTO, 2026-10-27): classify the equilateral-surfaced gluings found by enum_glue.py.
# Each distinct solid (corner matching, mirror images identified) is compared with the 8 convex deltahedra:
#  (a) congruent to one of them; (b) VARIANT: same face pattern (isomorphic edge graph) but a different shape;
#  (c) a face pattern none of the 8 convex deltahedra has (then checked against prior art by hand, see prior-art.md).
import json, itertools, sys, os
import numpy as np, networkx as nx
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enum_glue import match_sets

PHI = (1 + 5 ** 0.5) / 2

def hull_graph(P):
    H = ConvexHull(P); G = nx.Graph()
    groups = {}
    for s, e in zip(H.simplices, H.equations): groups.setdefault(tuple(np.round(e, 6)), []).append(s)
    assert all(len(v) == 1 for v in groups.values()), 'coplanar hull faces'
    for s in H.simplices:
        for a, b in itertools.combinations(s, 2): G.add_edge(int(a), int(b))
    L = [np.linalg.norm(P[a] - P[b]) for a, b in G.edges]
    assert max(L) - min(L) < 1e-6, ('not equilateral', min(L), max(L))
    return G

def convex_deltahedra():
    D = {}
    T = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float); D['tetrahedron (4)'] = T
    D['triangular bipyramid J12 (6)'] = np.vstack([T, [-T[0] * 5 / 3]])
    D['octahedron (8)'] = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float)
    a = np.arange(5) * 2 * np.pi / 5; R5 = 1 / (2 * np.sin(np.pi / 5)); h = np.sqrt(1 - R5 ** 2)
    D['pentagonal bipyramid J13 (10)'] = np.vstack([np.c_[R5 * np.cos(a), R5 * np.sin(a), 0 * a], [(0, 0, h), (0, 0, -h)]])
    # snub disphenoid J84: (+-t, r, 0), (0, -r, +-t), (+-1, -s, 0), (0, s, +-1); q real root of 2x^3 + 11x^2 + 4x - 1
    q = [x.real for x in np.roots([2, 11, 4, -1]) if abs(x.imag) < 1e-12 and 0 < x.real < 1][0]
    r, s, t = np.sqrt(q), np.sqrt((1 - q) / (2 * q)), np.sqrt(2 - 2 * q)
    D['snub disphenoid J84 (12)'] = np.array([(t, r, 0), (-t, r, 0), (0, -r, t), (0, -r, -t), (1, -s, 0), (-1, -s, 0), (0, s, 1), (0, s, -1)])
    pr = np.array([(0, 0, 0), (1, 0, 0), (0.5, np.sqrt(3) / 2, 0)]); c = pr.mean(0); hp = np.sqrt(0.5 - 1 / 12 * 0)  # placeholder
    # triaugmented triangular prism J51: unit prism + a square pyramid (height 1/sqrt2) on each square
    P = np.vstack([pr, pr + [0, 0, 1]]); cen = P.mean(0); apx = []
    for i in range(3):
        m = (pr[i] + pr[(i + 1) % 3]) / 2; out = m - c; out[2] = 0; out /= np.linalg.norm(out)
        apx.append(m + [0, 0, 0.5] + out / np.sqrt(2))
    D['triaugmented triangular prism J51 (14)'] = np.vstack([P, apx])
    # gyroelongated square bipyramid J17: unit square antiprism + two square pyramids
    R4 = 1 / np.sqrt(2); b = np.arange(4) * np.pi / 2
    ha = np.sqrt(1 - (2 * R4 * np.sin(np.pi / 8)) ** 2)  # antiprism height for unit lateral edges
    top = np.c_[R4 * np.cos(b), R4 * np.sin(b), np.full(4, ha / 2)]; bot = np.c_[R4 * np.cos(b + np.pi / 4), R4 * np.sin(b + np.pi / 4), np.full(4, -ha / 2)]
    hp = np.sqrt(1 - R4 ** 2)
    D['gyroelongated square bipyramid J17 (16)'] = np.vstack([top, bot, [(0, 0, ha / 2 + hp), (0, 0, -ha / 2 - hp)]])
    V = []
    for s1, s2 in itertools.product((1, -1), repeat=2): V += [(0, s1, s2 * PHI), (s1, s2 * PHI, 0), (s2 * PHI, 0, s1)]
    D['icosahedron (20)'] = np.array(V, float)
    G = {}
    for k, P in D.items():
        P = P / min(np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)); G[k] = (P, hull_graph(P))
    return G

def solid_of(r):
    faces = [np.array(f) for f in r['merged_faces']]
    pts = []
    def vid(p):
        for i, q in enumerate(pts):
            if np.linalg.norm(p - q) < 1e-6: return i
        pts.append(p); return len(pts) - 1
    F = [[vid(p) for p in f] for f in faces]
    G = nx.Graph()
    for f in F:
        for a, b in zip(f, f[1:] + f[:1]): G.add_edge(a, b)
    P = np.array(pts); P = P / np.mean([np.linalg.norm(P[a] - P[b]) for a, b in G.edges])
    H = ConvexHull(P); vol = sum(np.dot(P[f[0]], np.cross(P[f[k]], P[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
    convex = abs(H.volume - vol) < 1e-7
    return P, F, G, convex, vol

def run(files):
    CD = convex_deltahedra(); solids = []
    for fn in files:
        for r in json.load(open(fn))['results']:
            if r['cls'] != 'strict': continue
            P, F, G, convex, vol = solid_of(r)
            for s in solids:
                if len(s['P']) == len(P) and abs(s['vol'] - vol) < 1e-7 and (match_sets(s['P'], P) or match_sets(s['P'], P * [-1, 1, 1])):
                    s['builds'].append(r['pieces']); break
            else:
                solids.append(dict(P=P, F=F, G=G, convex=convex, vol=vol, builds=[r['pieces']], src=fn))
    out = []
    for s in solids:
        cls, ref = 'c', None
        for k, (Q, H) in CD.items():
            if len(Q) == len(s['P']) and nx.is_isomorphic(H, s['G']):
                cong = match_sets(Q - Q.mean(0), s['P'] - s['P'].mean(0)) or match_sets(Q - Q.mean(0), (s['P'] - s['P'].mean(0)) * [-1, 1, 1])
                cls, ref = ('a' if cong else 'b'), k
        degs = sorted((d for _, d in s['G'].degree()), reverse=True)
        out.append(dict(cls=cls, ref=ref, faces=len(s['F']), vertices=len(s['P']), convex=bool(s['convex']), volume_edge1=s['vol'],
                        degrees=degs, builds=sorted({' + '.join(sorted(b)) for b in s['builds']}), n_builds=len(s['builds']),
                        corners=s['P'].tolist(), face_list=s['F']))
    out.sort(key=lambda d: (d['cls'], d['faces'], d['builds'][0]))
    json.dump(out, open('data/q2-deltahedra.json', 'w'), indent=0)
    for d in out:
        print(d['cls'], d['ref'] or '', '| F', d['faces'], 'V', d['vertices'], '| convex' if d['convex'] else '| non-convex', '| vol %.6f' % d['volume_edge1'],
              '| deg', ''.join(map(str, d['degrees'])), '|', d['builds'][0], '(%d builds)' % d['n_builds'])
    print(len(out), 'distinct solids')

if __name__ == '__main__':
    run(sys.argv[1:])
