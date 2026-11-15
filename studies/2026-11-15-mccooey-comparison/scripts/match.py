#!/usr/bin/env python3
"""match.py (15 Nov 2026) - DICTO · dictospheres.com
Compares DICTO's solids (export_dicto.py) with David McCooey's Visual Polyhedra coordinate files (fetch_mccooey.py cache).
IDENTICAL: the corner sets are congruent up to similarity and mirror. Both sets are centred on their mean and scaled to
  mean squared radius 1; then an orthogonal map (det +1 or -1) is sought that takes three independent corners of A onto
  corners of B with the same norms and dot products and carries every corner of A onto a corner of B. Decided in double
  precision at tolerance 1e-8, then re-checked in 40 digits (mpmath) for exact builds against McCooey's 30-digit constants.
  For a non-convex entry the faces are compared too (same face sets under the map), else "corners only".
SIMILAR: no IDENTICAL entry, but a convex McCooey entry with the same combinatorics: the vertex-face incidence graphs
  (faces = merged hull facets) are isomorphic (networkx VF2, mirror allowed since incidence ignores orientation). The
  metric difference is stated by the distinct normalised edge lengths and face kinds of both.
NOT IN THE CATALOGUE: neither.
usage: match.py dicto-solids.json MCCOOEY_TXT_DIR manifest.json OUT.json [controls]"""
import sys, os, re, json, time, itertools
import numpy as np
import mpmath as mp
import networkx as nx
from networkx.algorithms import isomorphism as iso
from scipy.spatial import ConvexHull, cKDTree

mp.mp.dps = 40
DS, TXT, MAN, OUT = sys.argv[1:5]
CONTROLS = len(sys.argv) > 5 and sys.argv[5] == 'controls'
T0 = time.time()
CHECKS = []


def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok)))
    print(f'CHECK {"ok  " if ok else "FAIL"} {name} {detail}', flush=True)


# ---------------- McCooey parser
CRE = re.compile(r'^\s*(C\d+)\s*=\s*([-+0-9.eE]+)')
VRE = re.compile(r'^\s*V(\d+)\s*=\s*\(([^)]*)\)')


def parse_mc(path):
    lines = open(path, encoding='latin-1').read().splitlines()
    name = lines[0].strip() if lines else ''
    C, V, F, inf = {}, {}, [], False
    for ln in lines[1:]:
        if ln.strip().startswith('Faces'):
            inf = True
            continue
        if inf:
            m = re.match(r'^\s*\{([^}]*)\}', ln)
            if m:
                F.append([int(t) for t in m.group(1).replace(',', ' ').split()])
            continue
        m = CRE.match(ln)
        if m:
            C[m.group(1)] = mp.mpf(m.group(2))
            continue
        m = VRE.match(ln)
        if m:
            co = []
            for t in m.group(2).split(','):
                t = t.strip()
                sg = -1 if t.startswith('-') else 1
                t = t.lstrip('+-').strip()
                co.append(sg * (C[t] if t in C else mp.mpf(t)))
            V[int(m.group(1))] = co
    Vl = [V[i] for i in range(len(V))]
    return name, Vl, F


# ---------------- geometry helpers
def normalise_mp(V):
    n = len(V)
    c = [sum(v[k] for v in V) / n for k in range(3)]
    W = [[v[k] - c[k] for k in range(3)] for v in V]
    s = mp.sqrt(sum(sum(x * x for x in w) for w in W) / n)
    return [[x / s for x in w] for w in W]


def hull_faces(X, tol=1e-7):
    """merged facets of the convex hull: list of corner-index sets (corners on the facet plane)"""
    h = ConvexHull(X)
    pl = []
    for e in h.equations:
        if not any(np.allclose(e[:3], q[:3], atol=tol) and abs(e[3] - q[3]) < tol for q in pl):
            pl.append(e)
    faces = []
    for e in pl:
        on = np.where(np.abs(X @ e[:3] + e[3]) < tol)[0]
        faces.append(frozenset(int(i) for i in on))
    return faces


def is_convex_set(X, F, tol=1e-7):
    """given faces F (or None): every corner on the hull, and every face plane a hull plane"""
    try:
        h = ConvexHull(X)
    except Exception:
        return False
    if len(set(h.vertices)) != len(X):
        return False
    if not F:
        return True
    eq = h.equations
    for f in F:
        P = X[list(f)]
        if not np.any(np.all(np.abs(P @ eq[:, :3].T + eq[:, 3]) < tol, axis=0)):
            return False
    return True


class Solid:
    def __init__(s, sid, name, Vmp, F=None, hp=False, convex=None):
        s.id, s.name, s.hp = sid, name, hp
        s.Vmp = normalise_mp(Vmp) if hp else None
        X = np.array([[float(x) for x in v] for v in Vmp])
        X = X - X.mean(0)
        X = X / np.sqrt((X * X).sum(1).mean())
        s.X = X
        s.n = len(X)
        s.r = np.sort(np.sqrt((X * X).sum(1)))
        s.F = [frozenset(f) for f in F] if F else None
        s.convex = is_convex_set(X, s.F) if convex is None else convex
        s._hf = None
        s.tree = cKDTree(X)

    def hf(s):
        if s._hf is None:
            s._hf = hull_faces(s.X) if s.convex else None
        return s._hf


def basis(X):
    """three independent corners, from the rarest radius class first"""
    r = np.round(np.sqrt((X * X).sum(1)), 6)
    vals, cnt = np.unique(r, return_counts=True)
    order = sorted(range(len(X)), key=lambda i: (cnt[np.searchsorted(vals, r[i])], r[i]))
    a = [order[0]]
    for i in order[1:]:
        M = X[a + [i]]
        if np.linalg.matrix_rank(M, tol=1e-6) == len(a) + 1:
            a.append(i)
            if len(a) == 3:
                break
    return a


def congruence(A, B, tol=1e-8):
    """orthogonal Q with A.X @ Q.T ~ B.X as sets; returns (Q, perm) or None"""
    if A.n != B.n or np.max(np.abs(A.r - B.r)) > 1e-6:
        return None
    a = basis(A.X)
    if len(a) < 3:
        return None
    Pa = A.X[a]
    na = (Pa * Pa).sum(1)
    nb = (B.X * B.X).sum(1)
    cand = [np.where(np.abs(nb - na[i]) < 1e-7)[0] for i in range(3)]
    G = Pa @ Pa.T
    Pinv = np.linalg.inv(Pa)
    for b0 in cand[0]:
        for b1 in cand[1]:
            if abs(B.X[b0] @ B.X[b1] - G[0, 1]) > 1e-7:
                continue
            for b2 in cand[2]:
                if abs(B.X[b0] @ B.X[b2] - G[0, 2]) > 1e-7 or abs(B.X[b1] @ B.X[b2] - G[1, 2]) > 1e-7:
                    continue
                Pb = B.X[[b0, b1, b2]]
                M = (Pinv @ Pb).T             # M @ Pa[i] = Pb[i]
                if np.max(np.abs(M @ M.T - np.eye(3))) > 1e-7:
                    continue
                Y = A.X @ M.T
                d, idx = B.tree.query(Y)
                if np.max(d) < tol and len(set(idx)) == A.n:
                    return M, idx
    return None


def hp_confirm(A, B, M, idx):
    """40-digit re-check of a float match (both exact): refit Q from 3 basis corners in mp, max residual"""
    a = basis(A.X)
    Pa = mp.matrix([A.Vmp[i] for i in a])
    Pb = mp.matrix([B.Vmp[idx[i]] for i in a])
    Mq = (mp.inverse(Pa) * Pb).T
    worst = mp.mpf(0)
    for i in range(A.n):
        y = Mq * mp.matrix(A.Vmp[i])
        b = B.Vmp[idx[i]]
        worst = max(worst, max(abs(y[k] - b[k]) for k in range(3)))
    return worst


def faces_match(A, B, idx):
    if not A.F or not B.F:
        return None
    FA = {frozenset(int(idx[i]) for i in f) for f in A.F}
    return FA == set(B.F)


def signature(S):
    F = S.hf()
    if F is None:
        return None
    deg = [0] * S.n
    E = set()
    for f in F:
        idx = list(f)
        # order the face's corners around its centre to get its edges
        P = S.X[idx]
        c = P.mean(0)
        nrm = np.cross(P[1] - P[0], P[2] - P[0]) if len(idx) >= 3 else np.zeros(3)
        if np.linalg.norm(nrm) < 1e-12:
            for j in range(2, len(idx)):
                nrm = np.cross(P[1] - P[0], P[j] - P[0])
                if np.linalg.norm(nrm) > 1e-9:
                    break
        u = P[0] - c
        u /= np.linalg.norm(u)
        w = np.cross(nrm / np.linalg.norm(nrm), u)
        o = sorted(range(len(idx)), key=lambda k: np.arctan2((P[k] - c) @ w, (P[k] - c) @ u))
        ring = [idx[k] for k in o]
        for k in range(len(ring)):
            E.add(frozenset((ring[k], ring[(k + 1) % len(ring)])))
    for e in E:
        for v in e:
            deg[v] += 1
    fs = tuple(sorted(len(f) for f in F))
    return (S.n, len(E), len(F), fs, tuple(sorted(deg))), E


def incidence(S):
    g = nx.Graph()
    for j, f in enumerate(S.hf()):
        g.add_node(('f', j), t='f')
        for v in f:
            g.add_node(('v', v), t='v')
            g.add_edge(('v', v), ('f', j))
    return g


def edge_kinds(S, E):
    L = sorted({round(float(np.linalg.norm(S.X[a] - S.X[b])), 5) for a, b in (tuple(e) for e in E)})
    return L


# ---------------- load
dic = json.load(open(DS))['solids']
D = []
for s in dic:
    hp = s['precision'] == 'exact'
    V = [[mp.mpf(x) for x in v] for v in s['V']]
    D.append(Solid(s['id'], s['name'], V, s.get('F'), hp, s.get('convex')))
    D[-1].meta = s
if CONTROLS:     # synthetic controls from the TO file: turned + mirrored + scaled + moved (IDENTICAL), stretched (SIMILAR), cube (neither)
    _, Vto, Fto = parse_mc(os.path.join(TXT, 'TruncatedOctahedron.txt'))
    th = mp.mpf('0.7')
    Rz = [[mp.cos(th), -mp.sin(th), 0], [mp.sin(th), mp.cos(th), 0], [0, 0, 1]]
    tw = [[mp.mpf('2.5') * sum(Rz[i][j] * v[j] for j in range(3)) * (-1 if i == 0 else 1) + mp.mpf(i + 1) for i in range(3)] for v in Vto]
    st = [[v[0], v[1], v[2] * mp.mpf('1.3')] for v in Vto]
    cu = [[mp.mpf(a), mp.mpf(b), mp.mpf(c)] for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
    for sid, V, F in (('CTRL_TO_TURNED_MIRRORED', tw, Fto), ('CTRL_TO_STRETCHED', st, Fto), ('CTRL_CUBE', cu, None)):
        D.append(Solid(sid, sid, V, F, True))
        D[-1].meta = {'group': 'control'}
print(f'PROGRESS 0.10 {len(D)} DICTO solids loaded ({time.time() - T0:.0f} s)', flush=True)
man = {m['file']: m for m in json.load(open(MAN))['text_files']} if os.path.exists(MAN) else {}
MC = []
bad_parse = []
for fn in sorted(os.listdir(TXT)):
    if not fn.endswith('.txt'):
        continue
    try:
        name, V, F = parse_mc(os.path.join(TXT, fn))
        if len(V) < 4:
            raise ValueError('fewer than 4 corners')
        S = Solid(fn, name, V, F, True)
        S.url = man.get(fn, {}).get('url', 'https://dmccooey.com/polyhedra/' + fn)
        S.page = S.url[:-4] + '.html'
        MC.append(S)
    except Exception as e:
        bad_parse.append((fn, str(e)))
print(f'PROGRESS 0.20 {len(MC)} McCooey solids parsed, {len(bad_parse)} not parsed ({time.time() - T0:.0f} s)', flush=True)
byn = {}
for m in MC:
    byn.setdefault(m.n, []).append(m)

# ---------------- match
res = []
sigcache = {}
for k, A in enumerate(D):
    out = {'id': A.id, 'name': A.name, 'group': A.meta['group'], 'kind': A.meta.get('kind'), 'corners': A.n,
           'convex': bool(A.convex), 'identical': [], 'similar': []}
    for B in byn.get(A.n, []):
        r = congruence(A, B)
        if r is None:
            continue
        M, idx = r
        ent = {'mccooey': B.name, 'file': B.id, 'url': B.page, 'det': int(round(np.linalg.det(M)))}
        if A.hp and B.hp:
            ent['residual_40digit'] = mp.nstr(hp_confirm(A, B, M, idx), 3)
        if not (A.convex and B.convex):
            fm = faces_match(A, B, idx)
            ent['faces'] = 'same' if fm else ('differ' if fm is False else 'corners only')
        out['identical'].append(ent)
    if not out['identical'] and A.convex:
        sa = signature(A)
        if sa:
            ka, EA = sa
            out['combinatorics'] = {'V': ka[0], 'E': ka[1], 'F': ka[2]}
            for B in byn.get(A.n, []):
                if not B.convex:
                    continue
                if B.id not in sigcache:
                    sigcache[B.id] = signature(B)
                sb = sigcache[B.id]
                if not sb or sb[0] != ka:
                    continue
                if iso.GraphMatcher(incidence(A), incidence(B), node_match=lambda x, y: x['t'] == y['t']).is_isomorphic():
                    out['similar'].append({'mccooey': B.name, 'file': B.id, 'url': B.page,
                                           'dicto_edge_lengths': edge_kinds(A, EA), 'mccooey_edge_lengths': edge_kinds(B, sb[1])})
    out['verdict'] = 'IDENTICAL' if out['identical'] else ('SIMILAR' if out['similar'] else 'NOT IN THE CATALOGUE')
    res.append(out)
    if k % 200 == 0:
        print(f'PROGRESS {0.2 + 0.75 * k / len(D):.3f} {k}/{len(D)} matched ({time.time() - T0:.0f} s)', flush=True)

json.dump({'made': time.strftime('%Y-%m-%d'), 'mccooey_parsed': len(MC), 'not_parsed': bad_parse, 'results': res},
          open(OUT, 'w'), indent=1)
cnt = {}
for r in res:
    cnt[(r['group'], r['verdict'])] = cnt.get((r['group'], r['verdict']), 0) + 1
for k_ in sorted(cnt):
    print('COUNT', k_[0], k_[1], cnt[k_], flush=True)
if CONTROLS:
    get = {r['id']: r for r in res}
    def ver(i): return get[i]['verdict'], [e['file'] for e in get[i]['identical'] + get[i]['similar']]
    check('control +: turned, mirrored, scaled, moved TO is IDENTICAL to TruncatedOctahedron.txt',
          ver('CTRL_TO_TURNED_MIRRORED') == ('IDENTICAL', ['TruncatedOctahedron.txt']), str(ver('CTRL_TO_TURNED_MIRRORED')))
    check('control +: its 40-digit residual < 1e-25', float(get['CTRL_TO_TURNED_MIRRORED']['identical'][0]['residual_40digit']) < 1e-25,
          get['CTRL_TO_TURNED_MIRRORED']['identical'][0]['residual_40digit'])
    check('control +: registry truncated octahedron is IDENTICAL to it', ver('REG:TRUNCATED_OCTAHEDRON')[0] == 'IDENTICAL', str(ver('REG:TRUNCATED_OCTAHEDRON')))
    check('control +: A3 cone truncated octahedron (A3 Wythoff) is IDENTICAL to it',
          any(r['group'] == 'cone' and r['verdict'] == 'IDENTICAL' and r['corners'] == 24 for r in res))
    check('control sim: TO stretched 1.3 along z is SIMILAR (not IDENTICAL)', ver('CTRL_TO_STRETCHED') == ('SIMILAR', ['TruncatedOctahedron.txt']),
          str(ver('CTRL_TO_STRETCHED')))
    check('control -: cube is NOT IN THE CATALOGUE (fixture holds only the TO)', ver('CTRL_CUBE')[0] == 'NOT IN THE CATALOGUE')
    check('control -: DICTO silent zonohedron (48 corners) is not IDENTICAL to the 24-corner TO', ver('SILENT')[0] != 'IDENTICAL')
bad = [c for c in CHECKS if not c[1]]
print(f'checks {len(CHECKS) - len(bad)}/{len(CHECKS)}, {time.time() - T0:.0f} s', flush=True)
print('FINAL ok' if not bad else 'FINAL FAIL', flush=True)
