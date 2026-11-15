#!/usr/bin/env python3
"""Arrangements of Platonic gorinto cells, EKP manner: every arrangement is scaled down until the cells first touch; the contacts
are then certified (separations by float margin >= 1e-6 on exact data, touching pairs by exact zero of the gap).

Usage: arrangements.py named OUT.json        -> all named arrangements (column, fields, BCT, up/down, rings, mandala web, EKP column)
       arrangements.py search OUT.json STARTS -> Nelder-Mead lattice search (columnar, alternating up/down, general 3D)
Prints PROGRESS <fraction> lines and ends with FINAL ok only if every control passes."""
import sys, json, math, time, signal, itertools
import numpy as np
import sympy as sp
from gorinto import *

t_start = time.time()
parts, H = platonic_gorinto()
Hf = float(H)
U = cell_pieces(parts, H / 2)
Dn = [p.transformed(INVERT, exactM=INVERT_EXACT, exactt=(0, 0, 0)) for p in U]
VOL = sum(exact_volume(SOLID[p['element']]) for p in parts)
VOLf = float(VOL)
RHO = max(np.linalg.norm(q.V, axis=1).max() for q in U)        # every cell lies in the ball of radius RHO about its axis midpoint
FAILS = []


def tables(cells):
    keys = list(cells); out = {}
    for a in keys:
        for b in keys: out[(a, b)] = PairTable(cells[a], cells[b])
    return out


CELLS = {'U': U, 'D': Dn}
PT = tables(CELLS)


def solve(entries, pts=PT, cells=CELLS):
    """entries: list of (oA, oB, p, d, pE, dE). Smallest t > 0 with no interior overlap; binding contacts; all contacts at t."""
    allint = []
    groups = {}
    for idx, e in enumerate(entries): groups.setdefault((e[0], e[1]), []).append(idx)
    for key, idxs in groups.items():
        P = np.array([entries[k][2] for k in idxs], float); Dd = np.array([entries[k][3] for k in idxs], float)
        for lo, hi, k, i, j in pts[key].forbidden(P, Dd):
            allint.append((lo, hi, idxs[k], i, j))
    t = min_feasible(allint)
    contacts = []
    for idx, (oA, oB, p, d, pE, dE) in enumerate(entries):
        x = np.asarray(p, float) + t * np.asarray(d, float)
        if np.linalg.norm(x) > 2 * RHO + 1e-6: continue
        for i in range(5):
            for j in range(5):
                g, k = gap_at(pts[(oA, oB)], i, j, x)
                if g < -1e-7: FAILS.append(f'overlap after solve: entry {idx} pair {i},{j} gap {g}')
                if abs(g) < 1e-7:
                    N, h, L = pts[(oA, oB)].data[(i, j)]
                    contacts.append(dict(entry=idx, i=i, j=j, k=k, gap=float(g), x=x.tolist(),
                                         kind=contact_kind(cells[oA][i], cells[oB][j], N[k], x),
                                         elements=f"{U[i].element}-{U[j].element}", oA=oA, oB=oB))
    return t, contacts


# ---------------------------------------------------------------- exact certification of a contact
def exact_normal(A, B, label):
    neg = label[0] == '-'
    lab = label[1:] if neg else label
    def fnorm(P, f):
        a, b, c = (sp.Matrix(P.exact[f[0]]), sp.Matrix(P.exact[f[1]]), sp.Matrix(P.exact[f[2]]))
        n = (b - a).cross(c - a)
        cen = sum((sp.Matrix(v) for v in P.exact), sp.zeros(3, 1)) / len(P.exact)
        fc = sum((sp.Matrix(P.exact[i]) for i in f), sp.zeros(3, 1)) / len(f)
        if float((fc - cen).dot(n)) < 0: n = -n
        return n
    def edir(P, k):
        d = P.dirs[k]
        for a, b in P.edges:
            e = P.V[b] - P.V[a]; e = e / np.linalg.norm(e)
            if abs(abs(e @ d) - 1) < 1e-9:
                v = sp.Matrix(P.exact[b]) - sp.Matrix(P.exact[a])
                return v if e @ d > 0 else -v
    if lab[0] == 'fA': n = fnorm(A, A.faces[lab[1]])
    elif lab[0] == 'fB': n = fnorm(B, B.faces[lab[1]])
    else: n = edir(A, lab[1]).cross(edir(B, lab[2]))
    if neg: n = -n
    nf = np.array([float(c) for c in n], float)
    return n, nf


class Timeout(Exception): pass


def _alarm(s, f): raise Timeout()


def exact_zero(expr, secs=40):
    """'exact' if the minimal polynomial is x; 'digits' if |expr| < 1e-90 at 120 digits only; 'nonzero' otherwise."""
    v = sp.N(expr, 120)
    if abs(v) > sp.Float('1e-90'): return 'nonzero', float(v)
    signal.signal(signal.SIGALRM, _alarm); signal.alarm(secs)
    try:
        mp = sp.minimal_polynomial(expr, sp.Symbol('x'))
        signal.alarm(0)
        return ('exact' if mp == sp.Symbol('x') else 'nonzero'), 0.0
    except Exception:
        signal.alarm(0)
        return 'digits', 0.0


def certify(entries, t, contacts, cells=CELLS, pts=PT, texact=None, limit=12):
    """for up to `limit` distinct contact types: rebuild the separating normal exactly, gap = n.x - h exactly, test zero."""
    out = []; seen = set()
    for c in contacts:
        key = (c['elements'], c['kind'], c['oA'], c['oB'])
        if key in seen: continue
        seen.add(key)
        if len(out) >= limit: break
        oA, oB, p, d, pE, dE = entries[c['entry']]
        A, B = cells[oA][c['i']], cells[oB][c['j']]
        N, h, L = pts[(oA, oB)].data[(c['i'], c['j'])]
        n, nf = exact_normal(A, B, L[c['k']])
        ia = int(np.argmax(A.V @ nf)); ib = int(np.argmin(B.V @ nf))
        hE = n.dot(sp.Matrix(A.exact[ia])) - n.dot(sp.Matrix(B.exact[ib]))
        tE = texact if texact is not None else sp.Float(t, 30)
        xE = sp.Matrix(pE) + tE * sp.Matrix(dE)
        g = n.dot(xE) - hE
        if texact is None:
            status, val = ('float', float(sp.N(g, 30))) if abs(float(sp.N(g, 30))) < 1e-9 else ('nonzero', float(sp.N(g, 30)))
        else:
            status, val = exact_zero(g)
        out.append(dict(elements=c['elements'], kind=c['kind'], orient=oA + oB, zero=status, value=val))
        if status == 'nonzero': FAILS.append(f'contact not exactly touching: {key} value {val}')
    return out


def texact_from_binding(entries, t, contacts, cells=CELLS, pts=PT):
    """exact t from one contact whose line actually moves (n.d != 0): t = (h - n.p)/(n.d)."""
    for c in contacts:
        oA, oB, p, d, pE, dE = entries[c['entry']]
        N, h, L = pts[(oA, oB)].data[(c['i'], c['j'])]
        if abs(N[c['k']] @ np.asarray(d, float)) < 1e-6: continue
        A, B = cells[oA][c['i']], cells[oB][c['j']]
        n, nf = exact_normal(A, B, L[c['k']])
        ia = int(np.argmax(A.V @ nf)); ib = int(np.argmin(B.V @ nf))
        hE = n.dot(sp.Matrix(A.exact[ia])) - n.dot(sp.Matrix(B.exact[ib]))
        tE = (hE - n.dot(sp.Matrix(pE))) / n.dot(sp.Matrix(dE))
        tE = sp.radsimp(sp.simplify(tE))
        if abs(float(tE) - t) < 1e-8: return tE
    return None


def summarize(contacts):
    agg = {}
    for c in contacts:
        k = (c['elements'], c['kind'], c['oA'] + c['oB']); agg[k] = agg.get(k, 0) + 1
    return [dict(elements=k[0], kind=k[1], orient=k[2], count=v) for k, v in sorted(agg.items())]


# ---------------------------------------------------------------- arrangement builders
def cs(deg):
    return math.cos(math.radians(deg)), math.sin(math.radians(deg))


def cs_exact(deg):
    a = sp.rad(deg); return sp.cos(a), sp.sin(a)


def columnar_entries(theta, gamma, rho2, s1, s2, c, parity=False, K=4, sE=(0, 0), thetaE=None, gammaE=None, rho2E=1, cE=None):
    """lattice e1 = (t u1, s1), e2 = (t rho2 u2, s2), e3 = (0, 0, c); u1 at angle theta, u2 at theta + gamma.
    parity: cells with m1 + m2 odd are inverted (up/down checkerboard on the 2D lattice)."""
    c1, n1 = cs(theta); c2, n2 = cs(theta + gamma)
    if thetaE is not None:
        c1E, n1E = cs_exact(thetaE); c2E, n2E = cs_exact(thetaE + gammaE)
    ent = []
    for origin in (['U', 'D'] if parity else ['U']):
        for m1, m2 in itertools.product(range(-K, K + 1), repeat=2):
            for m3 in range(-2, 3):
                if m1 == m2 == m3 == 0: continue
                pz = m1 * s1 + m2 * s2 + m3 * c
                if abs(pz) > 2 * RHO: continue
                d = (m1 * c1 + rho2 * m2 * c2, m1 * n1 + rho2 * m2 * n2, 0.0)
                odd = (m1 + m2) % 2 == 1
                oB = ('D' if origin == 'U' else 'U') if (parity and odd) else origin
                if thetaE is not None:
                    pE = (0, 0, m1 * sE[0] + m2 * sE[1] + m3 * cE)
                    dE = (m1 * c1E + rho2E * m2 * c2E, m1 * n1E + rho2E * m2 * n2E, 0)
                else: pE = dE = None
                ent.append((origin, oB, (0, 0, pz), d, pE, dE))
    return ent


def run_named(entries, name, texact_ok=True, extra=None):
    t, contacts = solve(entries)
    tE = texact_from_binding(entries, t, contacts) if texact_ok else None
    cert = certify(entries, t, contacts, texact=tE)
    rec = dict(name=name, t=t, t_exact=str(tE) if tE is not None else None, contacts=summarize(contacts), certified=cert)
    if extra: rec.update(extra(t))
    return rec


def ring(N, beta, centre):
    """N cells on a circle of radius r (axes vertical, all at one height), member k at angle 2 pi k/N turned by 2 pi k/N + beta
    about its own axis (each faces the centre the same way); optional central cell (beta 0)."""
    cells = {'c': U}
    ent = []
    for k in range(N):
        a = 2 * math.pi * k / N + (math.pi if beta else 0.0)
        aE = 2 * sp.pi * k / N + (sp.pi if beta else 0)
        cells[f'm{k}'] = [p.transformed(rotz(a), exactM=rotz_exact(aE), exactt=(0, 0, 0)) for p in U]
    pts = {}
    pos = lambda k: (math.cos(2 * math.pi * k / N), math.sin(2 * math.pi * k / N), 0.0)
    posE = lambda k: (sp.cos(2 * sp.pi * k / N), sp.sin(2 * sp.pi * k / N), 0)
    for k in range(1, N // 2 + 1):
        pts[('m0', f'm{k}')] = PairTable(cells['m0'], cells[f'm{k}'])
        d = tuple(np.subtract(pos(k), pos(0))); dE = tuple(sp.simplify(a - b) for a, b in zip(posE(k), posE(0)))
        ent.append(('m0', f'm{k}', (0, 0, 0), d, (0, 0, 0), dE))
    if centre:
        pts[('c', 'm0')] = PairTable(cells['c'], cells['m0'])
        ent.append(('c', 'm0', (0, 0, 0), pos(0), (0, 0, 0), posE(0)))
    t, contacts = solve(ent, pts=pts, cells=cells)
    tE = texact_from_binding(ent, t, contacts, cells=cells, pts=pts)
    cert = certify(ent, t, contacts, cells=cells, pts=pts, texact=tE)
    return dict(name=f'ring N={N} {"outward" if not beta else "inward"} {"with centre" if centre else "no centre"}',
                r=t, r_exact=str(tE) if tE is not None else None, contacts=summarize(contacts), certified=cert)


def mandala13(h, outer='U', web=False):
    """the 3D mandala web: centre + 12 at the cuboctahedral (FCC, EKP 13-node) directions, stretched along the axis:
    middle layer (+-d, +-d, 0) [the To-ji quincunx: centre and four corners], upper layer (+-d, 0, h), (0, +-d, h), lower at -h.
    outer: orientation of the upper and lower layers (U parallel, D inverted). web=True: the whole lattice spanned by these."""
    if web:
        ent = []
        for m1, m2, m3 in itertools.product(range(-4, 5), repeat=3):
            if m1 == m2 == m3 == 0: continue
            pz = m3 * h
            if abs(pz) > 2 * RHO: continue
            oB = outer if m3 % 2 else 'U'
            d = (m1 + m2 + m3, m1 - m2, 0)
            ent.append(('U', oB, (0, 0, float(pz)), d, (0, 0, m3 * H / 2 if h == Hf / 2 else None), d))
            if outer == 'D' and m3 % 2:
                ent.append(('D', 'U', (0, 0, float(pz)), d, (0, 0, m3 * H / 2), d))
            if outer == 'D' and not m3 % 2:
                ent.append(('D', 'D', (0, 0, float(pz)), d, (0, 0, m3 * H / 2), d))
        return ent
    P = [((0, 0, 0), (0, 0, 0), 'U')]
    for sx, sy in itertools.product((1, -1), repeat=2): P.append(((0, 0, 0), (sx, sy, 0), 'U'))
    for z in (1, -1):
        for dvec in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]: P.append(((0, 0, z), dvec, outer))
    ent = []
    for a, b in itertools.combinations(range(13), 2):
        (pa, da, oa), (pb, db, ob) = P[a], P[b]
        pz = (pb[2] - pa[2])
        d = tuple(np.subtract(db, da).tolist())
        ent.append((oa, ob, (0, 0, pz * h), d, (0, 0, pz * H / 2 if abs(h - Hf / 2) < 1e-12 else pz * H), d))
    return ent


def ekp_column():
    """the EKP cell's nest, one element per cell along a column of cells of edge 2 (cells centred at z = 0, 2, 4, 6, 8):
    cube (cell 0), icosahedron (cell 1), stella tetrahedron (cell 2), octahedron (cell 3), Euclid's dodecahedron (cell 4).
    Exact vertical gaps between consecutive elements (negative = overlap)."""
    ip = 1 / PHI
    cube_top = 1
    ico_lo, ico_hi = 2 - ip, 2 + ip                     # icosahedron (0, +-1/phi, +-1/phi^2) cyclic: max |z| = 1/phi
    tet_lo, tet_hi = 4 - 1, 4 + 1
    oct_lo, oct_hi = 6 - 1, 6 + 1
    dod_lo = 8 - PHI
    gaps = {'earth-water': sp.simplify(ico_lo - cube_top), 'water-fire': sp.simplify(tet_lo - ico_hi),
            'fire-wind': sp.simplify(oct_lo - tet_hi), 'wind-void': sp.simplify(dod_lo - oct_hi)}
    return {k: dict(exact=str(sp.nsimplify(v)), value=float(v)) for k, v in gaps.items()}


def density_columnar(t, gamma, rho2, c, ncells=1):
    return ncells * VOLf / (t * t * rho2 * abs(math.sin(math.radians(gamma))) * c)


# ---------------------------------------------------------------- search (numeric)
def eval_columnar(x, alt):
    theta, gamma, rho2, s1, s2 = x[:5]
    if not (20 <= gamma <= 160 and 0.5 <= rho2 <= 3): return 0.0, None
    s1, s2 = (s1 % 1) * Hf, (s2 % 1) * Hf
    ent = columnar_entries(theta, gamma, rho2, s1, s2, Hf, K=3)
    if alt:
        w1, w2, z0 = x[5], x[6], (x[7] % 1) * Hf
        c1, n1 = cs(theta); c2, n2 = cs(theta + gamma)
        base = np.array([w1 * c1 + w2 * rho2 * c2, w1 * n1 + w2 * rho2 * n2, 0.0])
        for o in ('U', 'D'):
            ob = 'D' if o == 'U' else 'U'; sg = 1 if o == 'U' else -1
            for m1, m2 in itertools.product(range(-3, 4), repeat=2):
                for m3 in range(-2, 3):
                    pz = sg * z0 + m1 * s1 + m2 * s2 + m3 * Hf
                    if abs(pz) > 2 * RHO: continue
                    d = sg * base + np.array([m1 * c1 + rho2 * m2 * c2, m1 * n1 + rho2 * m2 * n2, 0.0])
                    ent.append((o, ob, (0, 0, pz), tuple(d), None, None))
        for m1, m2 in itertools.product(range(-3, 4), repeat=2):
            for m3 in range(-2, 3):
                if m1 == m2 == m3 == 0: continue
                pz = m1 * s1 + m2 * s2 + m3 * Hf
                if abs(pz) > 2 * RHO: continue
                ent.append(('D', 'D', (0, 0, pz), (m1 * c1 + rho2 * m2 * c2, m1 * n1 + rho2 * m2 * n2, 0.0), None, None))
    allint = []
    groups = {}
    for idx, e in enumerate(ent): groups.setdefault((e[0], e[1]), []).append(idx)
    for key, idxs in groups.items():
        P = np.array([ent[k][2] for k in idxs], float); Dd = np.array([ent[k][3] for k in idxs], float)
        allint += PT[key].forbidden(P, Dd)
    t = min_feasible(allint)
    return density_columnar(t, gamma, rho2, Hf, 2 if alt else 1), t


def eval_general(x):
    """fully general lattice t * B0 (no vertical vector forced); x = 9 entries of B0."""
    B0 = np.asarray(x, float).reshape(3, 3)
    det = abs(np.linalg.det(B0))
    if det < 1e-3: return 0.0, None
    ent = []
    for m in itertools.product(range(-3, 4), repeat=3):
        if m == (0, 0, 0): continue
        ent.append(('U', 'U', (0, 0, 0), tuple(B0 @ np.array(m, float)), None, None))
    P = np.zeros((len(ent), 3)); Dd = np.array([e[3] for e in ent])
    t = min_feasible(PT[('U', 'U')].forbidden(P, Dd))
    # completeness: every lattice vector shorter than 2 RHO must be in the box
    sv = np.linalg.svd(B0, compute_uv=False).min()
    if 2 * RHO / (t * sv) > 3.0: return 0.0, None
    return VOLf / (t ** 3 * det), t


def worker(args):
    from scipy.optimize import minimize
    fam, seed = args
    rng = np.random.default_rng(seed)
    if fam == 'general':
        x0 = np.eye(3).ravel() * np.array([2, 1, 1, 1, 2, 1, 1, 1, 7.0]) ** 0 + rng.normal(0, 0.6, 9)
        x0 = (np.diag([2.0, 2.0, Hf]) + rng.normal(0, 0.8, (3, 3))).ravel()
        f = lambda x: -eval_general(x)[0]
    else:
        alt = fam == 'alternating'
        x0 = [rng.uniform(0, 180), rng.uniform(55, 125), rng.uniform(0.8, 2.0), rng.uniform(0, 1), rng.uniform(0, 1)]
        if alt: x0 += [rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0, 1)]
        f = lambda x: -eval_columnar(x, alt)[0]
    best = None
    for rnd in range(3):
        r = minimize(f, x0, method='Nelder-Mead', options=dict(maxfev=900 if fam != 'general' else 1500, xatol=1e-9, fatol=1e-12))
        x0 = r.x
        if best is None or r.fun < best[0]: best = (r.fun, r.x.tolist())
    return dict(family=fam, seed=seed, density=-best[0], x=best[1])


def main_named(out):
    R = dict(cell={}, arrangements=[], rings=[], mandala=[], ekp=None)
    # the cell
    cell = R['cell']
    cell['H_exact'] = str(H); cell['H'] = Hf
    cell['parts'] = [dict(element=p['element'], kanji=KANJI[p['element']], seed=SEED[p['element']], solid=p['solid'],
                          bottom=float(p['bottom']), top=float(p['top']), height=float(p['height']), height_exact=str(sp.nsimplify(p['height'])),
                          volume=float(exact_volume(p['solid'])), volume_exact=str(sp.nsimplify(exact_volume(p['solid'])))) for p in parts]
    cell['volume'] = VOLf; cell['volume_exact'] = str(sp.simplify(VOL))
    # contacts inside the cell
    inside = []
    for a in range(4):
        A, B = U[a], U[a + 1]
        PTab = PairTable([A], [B]); g, k = gap_at(PTab, 0, 0, np.zeros(3))
        N, h, L = PTab.data[(0, 0)]
        inside.append(dict(lower=A.element, upper=B.element, gap=float(g), kind=contact_kind(A, B, N[k], np.zeros(3))))
        if abs(g) > 1e-9: FAILS.append(f'cell pieces {A.element}/{B.element} gap {g}')
    cell['inside_contacts'] = inside
    # non-neighbouring pieces inside the cell must be separated
    for a, b in itertools.combinations(range(5), 2):
        if b == a + 1: continue
        g, k = gap_at(PairTable([U[a]], [U[b]]), 0, 0, np.zeros(3))
        if g <= 1e-9: FAILS.append(f'cell pieces {a},{b} not separated: {g}')
    print('PROGRESS 0.05 cell', flush=True)
    jobs = [
        ('column (pagoda stack)', [('U', 'U', (0, 0, 0), (0, 0, 1.0), (0, 0, 0), (0, 0, 1))], None),
        ('square field, columns, theta 0', columnar_entries(0, 90, 1, 0, 0, Hf, thetaE=0, gammaE=90, cE=H), (90, 1)),
        ('square field, columns, theta 45', columnar_entries(45, 90, 1, 0, 0, Hf, thetaE=45, gammaE=90, cE=H), (90, 1)),
        ('hexagonal field, columns, theta 0', columnar_entries(0, 60, 1, 0, 0, Hf, thetaE=0, gammaE=60, cE=H), (60, 1)),
        ('hexagonal field, columns, theta 90', columnar_entries(90, 60, 1, 0, 0, Hf, thetaE=90, gammaE=60, cE=H), (60, 1)),
        ('body-centred (BCT), columns shifted H/2, theta 0',
         columnar_entries(0, 90, 1, Hf / 2, Hf / 2, Hf, thetaE=0, gammaE=90, sE=(H / 2, H / 2), cE=H), (90, 1)),
        ('body-centred (BCT), columns shifted H/2, theta 45',
         columnar_entries(45, 90, 1, Hf / 2, Hf / 2, Hf, thetaE=45, gammaE=90, sE=(H / 2, H / 2), cE=H), (90, 1)),
        ('up/down checkerboard (stupa field), square, theta 0',
         columnar_entries(0, 90, 1, 0, 0, Hf, parity=True, thetaE=0, gammaE=90, cE=H), (90, 1)),
        ('up/down checkerboard (stupa field), square, theta 45',
         columnar_entries(45, 90, 1, 0, 0, Hf, parity=True, thetaE=45, gammaE=90, cE=H), (90, 1)),
    ]
    for q, (name, ent, geo) in enumerate(jobs):
        rec = run_named(ent, name)
        if name.startswith('column'):
            rec['period'] = rec.pop('t'); rec['period_exact'] = rec.pop('t_exact')
            if abs(rec['period'] - Hf) > 1e-9: FAILS.append(f'column period {rec["period"]} != H')
        else:
            rec['density'] = density_columnar(rec['t'], geo[0], geo[1], Hf)
        R['arrangements'].append(rec); print(f'PROGRESS {0.05 + 0.4 * (q + 1) / len(jobs):.3f} {name} t={rec.get("t", rec.get("period")):.9f}', flush=True)
        json.dump(R, open(out, 'w'), indent=1)
    for q, (N, beta, centre) in enumerate([(4, 0, True), (5, 0, True), (6, 0, True), (8, 0, True), (8, 1, True), (8, 0, False), (12, 0, True)]):
        R['rings'].append(ring(N, beta, centre)); print(f'PROGRESS {0.45 + 0.25 * (q + 1) / 7:.3f} ring {N}', flush=True)
        json.dump(R, open(out, 'w'), indent=1)
    for q, (hname, h, outer, web) in enumerate([('H/2', Hf / 2, 'U', False), ('H/2', Hf / 2, 'D', False), ('H', Hf, 'U', False),
                                                ('H/2', Hf / 2, 'U', True)]):
        ent = mandala13(h, outer, web)
        nm = f'mandala {"web lattice" if web else "13"} h={hname} outer layers {"parallel" if outer == "U" else "inverted"}'
        rec = run_named(ent, nm)
        rec['d'] = rec.pop('t'); rec['d_exact'] = rec.pop('t_exact')
        if web:   # lattice (d,d,0),(d,-d,0),(d,0,h): cell volume 2 d^2 h
            rec['density'] = VOLf / (2 * rec['d'] ** 2 * h)
        R['mandala'].append(rec); print(f'PROGRESS {0.7 + 0.25 * (q + 1) / 4:.3f} {nm} d={rec["d"]:.9f}', flush=True)
        json.dump(R, open(out, 'w'), indent=1)
    R['ekp'] = ekp_column()
    # controls
    if abs(R['ekp']['fire-wind']['value']) > 1e-12: FAILS.append('EKP fire-wind control not touching')
    R['fails'] = FAILS
    json.dump(R, open(out, 'w'), indent=1)
    print('PROGRESS 1.0 named done', flush=True)


def main_search(out, starts):
    from multiprocessing import Pool
    d0, t0 = eval_columnar([0, 90, 1, 0.5, 0.5], False)
    if abs(t0 - 1.7776700946753579) > 1e-9: FAILS.append(f'control: BCT theta 0 through the search evaluator gave {t0}')
    tasks = [(fam, s) for fam in ('columnar', 'alternating', 'general') for s in range(starts)]
    res = []
    with Pool(20) as pool:
        for q, r in enumerate(pool.imap_unordered(worker, tasks)):
            res.append(r)
            if (q + 1) % max(1, len(tasks) // 20) == 0: print(f'PROGRESS {(q + 1) / len(tasks):.3f} search', flush=True)
    res.sort(key=lambda r: -r['density'])
    best = {}
    for r in res:
        if r['family'] not in best: best[r['family']] = r
    # contacts of each family's best
    for fam, r in best.items():
        if fam == 'general':
            d, t = eval_general(r['x'])
        else:
            d, t = eval_columnar(r['x'], fam == 'alternating')
        r['t'] = t; r['density_check'] = d
    json.dump(dict(best=best, all=res[:200], fails=FAILS), open(out, 'w'), indent=1)


if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    if mode == 'named': main_named(out)
    else: main_search(out, int(sys.argv[3]))
    print(f'elapsed {time.time() - t_start:.1f} s', flush=True)
    if FAILS:
        print('FAILS:', *FAILS[:20], sep='\n'); print('FINAL FAIL'); sys.exit(1)
    else:
        print('controls: cell contacts touching, non-neighbours separated, every reported contact exactly zero or zero to 120 digits')
