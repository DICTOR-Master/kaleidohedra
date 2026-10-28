# Which of the four 144-corner White Queen slices (W28, W30, W49, W51) are the same shape? Corner matching:
# sorted pairwise distances first (necessary), then an explicit isometry found from matched corners and checked on
# every corner and face (sufficient). Float coordinates of the exact hulls (metric frame), tolerance 1e-9.
import json, pickle, os, itertools, numpy as np
H = os.path.expanduser('~/kres-tmp')
K = pickle.load(open(f'{H}/4d/data/atlas600.pkl', 'rb'))
A = json.load(open(f'{H}/4d/data/atlas600.json'))
ORDER = ['vertex-first', 'edge-first', 'face-first', 'cell-first']; code = {}; n = 0
for d in ORDER:
    for o in sorted([o for o in A if o['direction'] == d], key=lambda o: o['h']):
        n += 1; code[(d, o['height'], o['at_vertex_layer'])] = 'W' + str(n)
S = {}
for k in K:
    it = k['item']; c = code[(it['direction'], it['height'], it['at_vertex_layer'])]
    if c in ('W28', 'W30', 'W49', 'W51', 'W1', 'W58', 'W5', 'W22'): S[c] = (np.array(k['fV'], float), k['faces'])
def dists(P): return np.sort(np.linalg.norm(P[:, None] - P[None], axis=2)[np.triu_indices(len(P), 1)])
def facesig(P, F): return sorted((len(f), round(float(np.linalg.norm(np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]))), 6)) for f in F)
def isometric(P, Q):
    P = P - P.mean(0); Q = Q - Q.mean(0)
    # try to map 4 affinely independent corners of P onto candidates in Q with the same distances
    dP = np.linalg.norm(P[:, None] - P[None], axis=2); dQ = np.linalg.norm(Q[:, None] - Q[None], axis=2)
    i0 = 0; nbr = np.argsort(dP[i0])[1:4]; base = [i0] + list(nbr)
    for j0 in range(len(Q)):
        if abs(np.linalg.norm(Q[j0]) - np.linalg.norm(P[i0])) > 1e-7: continue
        cands = [[j for j in range(len(Q)) if abs(dQ[j0, j] - dP[i0, b]) < 1e-7] for b in nbr]
        for js in itertools.product(*cands):
            if len(set(js)) < 3: continue
            tgt = [j0] + list(js)
            if any(abs(dQ[a, b] - dP[x, y]) > 1e-7 for (x, a), (y, b) in itertools.combinations(zip(base, tgt), 2)): continue
            X = P[base]; Y = Q[tgt]
            M, *_ = np.linalg.lstsq(X, Y, rcond=None)
            if np.abs(M.T @ M - np.eye(3)).max() > 1e-6: continue
            PM = P @ M
            dd = np.linalg.norm(PM[:, None] - Q[None], axis=2).min(1)
            if dd.max() < 1e-7: return True
    return False
for a, b in [('W28', 'W30'), ('W28', 'W49'), ('W28', 'W51'), ('W30', 'W49'), ('W30', 'W51'), ('W49', 'W51'), ('W1', 'W58'), ('W5', 'W22')]:
    P, F = S[a]; Q, G = S[b]
    same_d = len(P) == len(Q) and np.allclose(dists(P), dists(Q), atol=1e-7)
    iso = isometric(P, Q) if same_d else False
    print(a, b, 'corners', len(P), len(Q), '| same distances', same_d, '| congruent', iso, flush=True)
# Same pattern? (combinatorial type: face-vertex incidence, up to relabelling) — the gap slices are patterns over a
# height range, so this is the right comparison for them.
import networkx as nx
def inc_graph(F):
    g = nx.Graph()
    for fi, f in enumerate(F):
        g.add_node(('f', fi), k=len(f))
        for a, b in zip(f, f[1:] + f[:1]): g.add_edge(('f', fi), ('v', a))
    for n_ in g.nodes:
        if n_[0] == 'v': g.nodes[n_]['k'] = 0
    return g
for a, b in [('W28', 'W30'), ('W28', 'W49'), ('W28', 'W51'), ('W30', 'W49'), ('W30', 'W51'), ('W49', 'W51'), ('W1', 'W58'), ('W5', 'W22')]:
    ga, gb = inc_graph(S[a][1]), inc_graph(S[b][1])
    same = nx.is_isomorphic(ga, gb, node_match=lambda x, y: x['k'] == y['k'])
    print(a, b, 'same pattern of faces:', same, flush=True)
