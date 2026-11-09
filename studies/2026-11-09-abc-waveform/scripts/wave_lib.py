"""ABC waveform on Narcissus (DICTO 9 Nov 2026): shared library.

Carrier: the Narcissus slab stacking of #97 (n_slabs.py, copied from studies/2026-11-05-one-piece-any-stacking).
Each slab = down-N on X sites (hexagon on top) + up-N on Y sites (hexagon below); each interface between slabs is
S (straight: mirror in the interface plane) or T (turned: mirror + 60 deg). SSS... is the hcp h-tiling, TTT... the Covenant pairs.

Decoration (Ammann-style wave): a finite set of PLANES fixed in the reference piece P0 (wave crests). In a tiling every piece
carries the planes moved by its own placement (3 turns, plus 3 mirror placements if mirror copies are allowed), so different
placements show different crest phases/directions on the same face. Every face of N touches exactly one neighbour face to face
(edge census, 11-06), so the matching rule is a rule per contact:
   STRICT  - the set of planes cutting the shared face is the same on both sides (crests continue straight through the face);
   BEND    - only the crest LINES on the shared face agree (a crest may change direction at the face: 'lean back').
Planes carry a colour (wave component); colours must agree too.
"""
import itertools, numpy as np
from scipy.spatial import ConvexHull
from n_slabs import narc, build, SITE, H

PHI = (1 + 5 ** .5) / 2
a1 = np.array([1, 0.]); a2 = np.array([.5, np.sqrt(3) / 2])
P0 = narc(SITE['A'], H, 0, 'C')
D0 = np.linalg.norm(P0[:, None] - P0[None], axis=2)

def faces_idx(P):
    h = ConvexHull(P); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 7)), set()).update(int(x) for x in sp)
    return [(np.array(k[:3]), -k[3], frozenset(v)) for k, v in F.items()]   # (normal, offset, corner set)
BF = faces_idx(P0); assert len(BF) == 10
BFI = {f[2]: i for i, f in enumerate(BF)}
FKIND = ['hex' if len(f[2]) == 6 else 'quad' if len(f[2]) == 4 else 'tri' for f in BF]

def perms_matching(Da, Db):
    out = []
    def rec(m):
        k = len(m)
        if k == 10: out.append(tuple(m)); return
        for j in range(10):
            if j in m: continue
            if all(abs(Da[k, i] - Db[j, m[i]]) < 1e-6 for i in range(k)): rec(m + [j])
    rec([]); return out
SYM = perms_matching(D0, D0); assert len(SYM) == 6

def affine(P, Q, p):
    """R, t with Q[p[i]] = R P[i] + t"""
    A = np.c_[P, np.ones(10)]; B = Q[list(p)]
    M = np.linalg.lstsq(A, B, rcond=None)[0]; R = M[:3].T; t = M[3]
    assert np.allclose(A @ M, B, atol=1e-7) and np.allclose(R @ R.T, np.eye(3), atol=1e-7)
    return R, t

class Structure:
    """pieces of a word, their 6 placements (alignments of P0), and all face contacts"""
    def __init__(self, word, n):
        self.word = word; self.Ps = build(word, n=n); self.pl = []; self.wf = []
        for Q in self.Ps:
            Dq = np.linalg.norm(Q[:, None] - Q[None], axis=2)
            al = []
            for p in perms_matching(D0, Dq):
                R, t = affine(P0, Q, p); inv = {p[i]: i for i in range(10)}
                al.append((R, t, int(round(np.linalg.det(R))), inv))
            self.pl.append(al)
            self.wf.append(faces_idx(Q))
        cen = {}
        for i, (Q, F) in enumerate(zip(self.Ps, self.wf)):
            for fi, (nrm, off, idx) in enumerate(F):
                c = Q[sorted(idx)].mean(0); cen.setdefault(tuple(np.round(c, 5)), []).append((i, fi))
        self.contacts = []
        for k, v in cen.items():
            if len(v) == 2:
                (i, fi), (j, fj) = v
                assert np.allclose(self.wf[i][fi][0], -self.wf[j][fj][0], atol=1e-6)
                self.contacts.append((i, fi, j, fj))
            else: assert len(v) == 1
    def base_face(self, i, k, fi):
        inv = self.pl[i][k][3]; return BFI[frozenset(inv[x] for x in self.wf[i][fi][2])]

def cuts(plane, fidx):
    n, d, col = plane; s = P0[sorted(fidx)] @ n - d
    return s.min() < -1e-7 and s.max() > 1e-7

def canon_vec(v, c):
    for x in v:
        if abs(x) > 1e-6:
            if x < 0: v, c = -v, -c
            break
    return tuple(np.round(v, 5) + 0.0) + (round(float(c), 5) + 0.0,)

def signatures(S, deco, mode):
    """sig[i][k][fi] = frozenset of crest keys on world face fi of piece i in placement k"""
    cut = [[pl for pl in deco if cuts(pl, f[2])] for f in BF]
    sig = []
    for i in range(len(S.Ps)):
        si = []
        for k, (R, t, det, inv) in enumerate(S.pl[i]):
            sk = []
            for fi, (u, c, idx) in enumerate(S.wf[i]):
                bf = BFI[frozenset(inv[x] for x in idx)]; keys = []
                for n, d, col in cut[bf]:
                    nw = R @ n; dw = d + nw @ t
                    if mode == 'STRICT': keys.append((col,) + canon_vec(nw, dw))
                    else:
                        m = nw - (nw @ u) * u; L = np.linalg.norm(m)
                        keys.append((col,) + canon_vec(m / L, (dw - (nw @ u) * c) / L))
                sk.append(frozenset(keys))
            si.append(sk)
        sig.append(si)
    return sig

def solve(S, sig, mirror_ok, classes=None, want_model=False):
    from pysat.solvers import Cadical153
    s = Cadical153(); X = {}; nv = [0]
    def var(c, k):
        if (c, k) not in X: nv[0] += 1; X[(c, k)] = nv[0]
        return X[(c, k)]
    cl = classes if classes is not None else list(range(len(S.Ps)))
    ok = [[k for k in range(6) if mirror_ok or S.pl[i][k][2] > 0] for i in range(len(S.Ps))]
    done = set()
    for i in range(len(S.Ps)):
        c = cl[i]
        if c in done: continue
        done.add(c)
        s.add_clause([var(c, k) for k in ok[i]])
        for k in range(6):
            if k not in ok[i]: s.add_clause([-var(c, k)])
        for k1, k2 in itertools.combinations(range(6), 2): s.add_clause([-var(c, k1), -var(c, k2)])
    for (i, fi, j, fj) in S.contacts:
        for (a, fa, b, fb) in ((i, fi, j, fj), (j, fj, i, fi)):
            for k in ok[a]:
                allowed = [l for l in ok[b] if sig[b][l][fb] == sig[a][k][fa]]
                s.add_clause([-var(cl[a], k)] + [var(cl[b], l) for l in allowed])
    r = s.solve(); model = None
    if r and want_model:
        M = set(x for x in s.get_model() if x > 0)
        model = [next(k for k in range(6) if X.get((cl[i], k)) in M) for i in range(len(S.Ps))]
    s.delete()
    return (r, model) if want_model else r

# ---------- tori (copied from spiral_keys.py classes_for, with every skew representative: the 11-06 review fix)
def classes_for(Ps, word_unit, reps, m, skew=np.zeros(2)):
    ha, hb, hd = m; ML = np.array([ha * a1, hb * a1 + hd * a2]).T
    p = len(word_unit); nl = p * reps + 1; per_layer = len(Ps) // nl
    layer = [i // per_layer for i in range(len(Ps))]; cen = [P.mean(0) for P in Ps]
    L0 = [cen[i] for i in range(len(Ps)) if layer[i] == 0]; Lp = [cen[i] for i in range(len(Ps)) if layer[i] == p]
    tz = p * H
    def red(x):
        cc = np.linalg.solve(ML, x[:2]); f = cc - np.floor(cc + 1e-7); f = np.where(f > 1 - 1e-6, 0, f); return tuple(np.round(f, 4))
    SP = {red(z) + (round(z[2] % (2 * H), 4),) for z in Lp}
    cand = None
    for y in Lp:
        t = y[:2] - L0[0][:2]
        if all((red(np.r_[x[:2] + t, 0]) + (round((x[2] + tz) % (2 * H), 4),)) in SP for x in L0): cand = t; break
    if cand is None: return None
    cand = cand + skew; key = {}; cls = []
    for i in range(len(Ps)):
        q, r = divmod(layer[i], p); x = cen[i] - np.r_[q * cand, q * tz]
        cls.append(key.setdefault((r,) + red(x) + (round(x[2], 4),), len(key)))
    rep = {}
    for i, k in enumerate(cls):
        off = np.round(Ps[i] - cen[i], 5)
        if k in rep:
            if not np.allclose(rep[k], off): return None
        else: rep[k] = off
    return cls

def periodic_words(pmax):
    out = set()
    for p in range(1, pmax + 1):
        for w in itertools.product('ST', repeat=p):
            w = ''.join(w)
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)): continue
            out.add(min(w[i:] + w[:i] for i in range(p)))
    return sorted(out, key=lambda w: (len(w), w))

def torus_instances(pmax, imax, n):
    """(label, Structure, classes) for every primitive periodic word up to pmax (repeated so that the period lattice exists),
    every in-plane sublattice of index <= imax (Hermite normal forms) and every skew representative"""
    out = []
    MS = [(ha, hb, hd) for ha in range(1, imax + 1) for hd in range(1, imax + 1) if ha * hd <= imax for hb in range(ha)]
    for wu in periodic_words(pmax):
        for mult in range(1, 7):
            if len(wu) * mult > 12: break
            u = wu * mult; S = Structure(u * 2, n); got = False
            for m in MS:
                for p_ in range(m[0]):
                    for q_ in range(m[2]):
                        cl = classes_for(S.Ps, u, 2, m, skew=p_ * a1 + q_ * a2)
                        if cl is not None: out.append((f"{u}/{m}+skew({p_},{q_})", S, cl)); got = True
            if got: break
    return out

# ---------- the menu of crest planes
def lean_normals():
    """the 3 tilted close-packed plane families for each lean sense (B-ward t, C-ward t'), and the horizontal family"""
    A1 = np.r_[a1, 0]; A2 = np.r_[a2, 0]; t = np.r_[(a1 + a2) / 3, H]; tp = np.r_[-(a1 + a2) / 3, H]
    out = {}
    for name, (v, w) in {'b1': (A1, t), 'b2': (A2, t), 'b3': (A2 - A1, t - A1),
                         'c1': (A1, tp), 'c2': (A2, tp), 'c3': (A2 - A1, tp - A1)}.items():
        n = np.cross(v, w); n /= np.linalg.norm(n)
        if n[2] < 0: n = -n
        out[name] = n
    out['z'] = np.array([0, 0, 1.])
    return out
