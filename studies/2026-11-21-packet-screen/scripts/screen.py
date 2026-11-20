# Packet screen 2026-11-21, step 4: packets and the screen.
# Packet of a piece = its Dehn invariant written in the angle basis B of relations.json:
#     D = sum_b c_b (x) beta_b,  c_b = sum over edges of q_{e,b} * length_e   (q from the proved relations; rational angles drop).
# Each c_b is kept EXACTLY as an element of the formal radical ring of the piece's field (lengths are square roots of field elements).
# Since the beta_b are Q-independent mod Q pi (numerically: PSLQ found no further relation, see relations.json), D = 0 iff every c_b = 0.
# Cancellation n P + sum m_i (lambda_i H_i) = 0 with free scales lambda_i > 0 is the condition c(P) = -sum a_i c(H_i), a_i > 0.
# A cancellation claim needs only the proved relations and exact identities in the radical ring (no independence assumption);
# a "none" claim relies on the basis being independent (numerical: PSLQ bound) and is marked so.
import sys, os, json, itertools, time
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
sys.path.insert(0, os.path.dirname(__file__))
from nf import fields, Radicals

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mp.mp.dps = 120
F = fields()
FAIL = []
def check(label, ok):
    print(('ok   ' if ok else 'FAIL ') + label, flush=True)
    if not ok: FAIL.append(label)
def el(K, s): return K.el([Fr(t) for t in s])

pieces = json.load(open(os.path.join(HERE, 'data', 'pieces.json')))
angles = json.load(open(os.path.join(HERE, 'data', 'angles.json')))
rel = json.load(open(os.path.join(HERE, 'data', 'relations.json')))
B = rel['basis']; Bi = {b: j for j, b in enumerate(B)}
akey = {}
for a in angles:
    for o in a['occurs']: akey[(o[0], o[1], tuple(o[2]))] = a['id']
# express every irrational angle in the basis (mod Q pi)
expr = {b: {b: Fr(1)} for b in B}
for r in rel['relations']:
    R = {int(k) if k != 'pi' else k: v for k, v in r['relation'].items()}; a = r['angle']; k0 = R[a]
    expr[a] = {b: Fr(-v, k0) for b, v in R.items() if b not in ('pi', a)}
    if not r['proved_exact']: print('note: relation for th', a, 'not proved exactly; pieces using it are marked')
unproved = {r['angle'] for r in rel['relations'] if not r['proved_exact']}
RAD = {k: Radicals(K, full=8) for k, K in F.items()}

def packet(p):
    K = F[p['field']]; R = RAD[p['field']]; c = {}; uses_unproved = False
    for kind, L2, sg, c2 in p['edges']:
        aid = akey[(p['field'], sg, tuple(c2))]
        if angles[aid]['rational']: continue
        if aid in unproved: uses_unproved = True
        L = R.register(el(K, L2))
        for b, q in expr[aid].items():
            c[b] = R.add(c.get(b, {}), R.scal(K.q(q), L))
    c = {b: v for b, v in c.items() if not R.iszero(v)}
    num = np.zeros(len(B)); mpv = {}
    for b, v in c.items():
        z = R.num(v); assert abs(z.imag) < 1e-100
        mpv[b] = z.real; num[Bi[b]] = float(z.real)
    for b, v in mpv.items(): assert abs(v) > mp.mpf(10) ** -60, f'formally nonzero but numerically zero: {p["id"]} beta{b}'
    return {'exact': c, 'mp': mpv, 'num': num, 'unproved': uses_unproved}

def lengths(p):
    K = F[p['field']]; s = []
    for e in p['edges']:
        if tuple(e[1]) not in s: s.append(tuple(e[1]))
    return [el(K, t) for t in s]

t0 = time.time()
P = {}
for p in pieces:
    P[p['id']] = dict(p, **packet(p))
print(f'packets built [{time.time() - t0:.1f}s]', flush=True)

def same_field(*ids): return len(set(P[i]['field'] for i in ids)) == 1

def verify1(pid, hid):
    """exact proof that c(P) = -mu c(H) for one real mu > 0 (same field)"""
    p, h = P[pid], P[hid]; R = RAD[p['field']]
    if set(p['exact']) != set(h['exact']): return False
    j0 = max(p['mp'], key=lambda b: abs(p['mp'][b]))
    for b in p['exact']:
        if not R.iszero(R.sub(R.mul(p['exact'][b], h['exact'][j0]), R.mul(p['exact'][j0], h['exact'][b]))): return False
    return p['mp'][j0] / h['mp'][j0] < 0

def mu_of(pid, hid):
    p, h = P[pid], P[hid]; j0 = max(p['mp'], key=lambda b: abs(p['mp'][b])); return -p['mp'][j0] / h['mp'][j0], j0

def proportions(pid, hid, maxden=48):
    """edge-matched integer proportions n:m (helper scaled so that one of its edges equals one edge of the pyramid), proved exactly"""
    p, h = P[pid], P[hid]; K = F[p['field']]; R = RAD[p['field']]; mu, j0 = mu_of(pid, hid); out = []
    for lp in lengths(p):
        for lh in lengths(h):
            x = mu * mp.sqrt(K.num(lh)) / mp.sqrt(K.num(lp))
            q = Fr(str(mp.nstr(x, 50))).limit_denominator(maxden)
            if abs(x - mp.mpf(q.numerator) / q.denominator) > mp.mpf(10) ** -50: continue
            # n lh c_P + m lp c_H = 0 at j0 with m/n = q
            LP = R.register(lp); LH = R.register(lh)
            ok = R.iszero(R.add(R.scal(K.q(q.denominator), R.mul(LH, p['exact'][j0])), R.scal(K.q(q.numerator), R.mul(LP, h['exact'][j0]))))
            if ok: out.append({'n': q.denominator, 'm': q.numerator, 'P_edge2': [str(t) for t in lp], 'H_edge2': [str(t) for t in lh],
                               'P_edge': float(mp.sqrt(K.num(lp))), 'H_edge': float(mp.sqrt(K.num(lh)))})
    out.sort(key=lambda d: d['n'] + d['m'])
    return out

def det3(R, a, b, c):
    return R.sub(R.add(R.add(R.mul(a[0], R.mul(b[1], c[2])), R.mul(a[1], R.mul(b[2], c[0]))), R.mul(a[2], R.mul(b[0], c[1]))),
                 R.add(R.add(R.mul(a[2], R.mul(b[1], c[0])), R.mul(a[0], R.mul(b[2], c[1]))), R.mul(a[1], R.mul(b[0], c[2]))))

def verify2(pid, h1, h2):
    p = P[pid]; R = RAD[p['field']]; ex = [P[i]['exact'] for i in (pid, h1, h2)]
    sup = sorted(set().union(*[set(e) for e in ex]))
    g = lambda e, b: e.get(b, {})
    pairs = [(j, k) for j, k in itertools.combinations(sup, 2) if not R.iszero(R.sub(R.mul(g(ex[1], j), g(ex[2], k)), R.mul(g(ex[1], k), g(ex[2], j))))]
    if not pairs: return False
    j, k = pairs[0]
    for l in sup:
        if l in (j, k): continue
        if not R.iszero(det3(R, [g(ex[0], j), g(ex[0], k), g(ex[0], l)], [g(ex[1], j), g(ex[1], k), g(ex[1], l)], [g(ex[2], j), g(ex[2], k), g(ex[2], l)])): return False
    return True

def proportion2(pid, h1, h2, maxden=48):
    """at the canonical scales (edge 1; Catalan = dual of the edge-1 Archimedean): integers n:m1:m2 with n P + m1 H1 + m2 H2 = 0, proved exactly; None if a ratio is irrational"""
    p = P[pid]; K = F[p['field']]; R = RAD[p['field']]; sup = sorted(set(p['mp']) | set(P[h1]['mp']) | set(P[h2]['mp']))
    g = lambda i, b: P[i]['mp'].get(b, mp.mpf(0))
    for j, k in itertools.combinations(sup, 2):
        det = g(h1, j) * g(h2, k) - g(h1, k) * g(h2, j)
        if abs(det) < mp.mpf(10) ** -50: continue
        a1 = (-g(pid, j) * g(h2, k) + g(pid, k) * g(h2, j)) / det; a2 = (-g(h1, j) * g(pid, k) + g(h1, k) * g(pid, j)) / det
        q = [Fr(str(mp.nstr(a, 50))).limit_denominator(maxden) for a in (a1, a2)]
        if any(abs(a - mp.mpf(x.numerator) / x.denominator) > mp.mpf(10) ** -50 for a, x in zip((a1, a2), q)): return None
        L = 1
        for x in q: L = L * x.denominator // __import__('math').gcd(L, x.denominator)
        n, m1, m2 = L, int(q[0] * L), int(q[1] * L)
        for b in sup:
            t = R.add(R.add(R.scal(K.q(n), P[pid]['exact'].get(b, {})), R.scal(K.q(m1), P[h1]['exact'].get(b, {}))), R.scal(K.q(m2), P[h2]['exact'].get(b, {})))
            if not R.iszero(t): return None
        return [n, m1, m2]
    return None

# ---------------- controls
cz = [pid for pid in P if not P[pid]['exact']]
check('control: cube centre pyramid packet is exactly zero', 'P[cube|4]' in cz)
check('control: rhombic dodecahedron centre pyramid packet is exactly zero', 'P[rhombic_dodecahedron|4]' in cz)
check('control: rhombic triacontahedron centre pyramid packet is exactly zero', 'P[rhombic_triacontahedron|4]' in cz)
check('control: dodecahedron centre pyramid packet is nonzero', 'P[dodecahedron|5]' not in cz)
ok = verify1('tetrahedron', 'octahedron'); pr = proportions('tetrahedron', 'octahedron')
check('control: tetrahedron + octahedron cancel, 2:1 at equal edges (octet)', ok and any(d['n'] == 2 and d['m'] == 1 and d['P_edge'] == d['H_edge'] for d in pr))
ok = verify1('P[cuboctahedron|3]', 'P[cuboctahedron|4]'); pr = proportions('P[cuboctahedron|3]', 'P[cuboctahedron|4]')
check('control: CO triangle pyramid + CO square pyramid cancel 1:1 (the octet again)', ok and any(d['n'] == 1 and d['m'] == 1 for d in pr))
mu, _ = mu_of('P[icosidodecahedron|3]', 'P[icosidodecahedron|5]')
check('control: ID triangle pyramid + ID pentagon pyramid do NOT cancel (gap study theorem)', not verify1('P[icosidodecahedron|3]', 'P[icosidodecahedron|5]'))
check('control: tetrahedron + cube do NOT cancel (cube is zero, tetrahedron is not)', 'tetrahedron' not in cz and 'cube' in cz)
# additivity: the pyramids of a solid add up to the solid (exact)
for s in [p for p in pieces if p['kind'] == 'solid' and p['family'] != 'antiprism']:
    R = RAD[s['field']]; K = F[s['field']]; tot = {}
    for q in pieces:
        if q['kind'] == 'pyramid' and q['solid'] == s['id']:
            for b, v in P[q['id']]['exact'].items(): tot[b] = R.add(tot.get(b, {}), R.scal(K.q(q['face_count']), v))
    okk = set(b for b in tot if not R.iszero(tot[b])) == set(P[s['id']]['exact']) and all(R.iszero(R.sub(tot.get(b, {}), P[s['id']]['exact'].get(b, {}))) for b in set(tot) | set(P[s['id']]['exact']))
    check(f"additivity: sum of the centre pyramids of {s['id']} = the solid's packet (exact)", okk)

# ---------------- the screen
NZ = [pid for pid in P if P[pid]['exact']]
lib = NZ
res = {}
for pid in [q['id'] for q in pieces if q['kind'] == 'pyramid']:
    p = P[pid]
    if not p['exact']:
        res[pid] = {'zero': True}; continue
    v = p['num']; nv = np.linalg.norm(v); one = []
    for hid in lib:
        if hid == pid: continue
        h = P[hid]['num']; hn = np.linalg.norm(h)
        cs = v @ h / (nv * hn)
        if cs > -1 + 1e-9: continue
        mu, j0 = mu_of(pid, hid)
        okx = verify1(pid, hid) if same_field(pid, hid) else None
        if okx is False: continue
        one.append({'helper': hid, 'mu': float(mu), 'exact': okx is True, 'cross_field': okx is None,
                    'unproved_relation': P[pid]['unproved'] or P[hid]['unproved'],
                    'proportions': proportions(pid, hid) if okx else []})
    two = []
    if not one:
        for h1, h2 in itertools.combinations([h for h in lib if h != pid], 2):
            A = np.stack([P[h1]['num'], P[h2]['num']], 1)
            sol, *_ = np.linalg.lstsq(A, -v, rcond=None)
            if np.linalg.norm(A @ sol + v) > 1e-9 * nv: continue
            if not (sol[0] > 1e-9 and sol[1] > 1e-9): continue
            if np.linalg.matrix_rank(A, tol=1e-9 * np.abs(A).max()) < 2: continue
            okx = verify2(pid, h1, h2) if same_field(pid, h1, h2) else None
            if okx is False: continue
            two.append({'helpers': [h1, h2], 'a': [float(sol[0]), float(sol[1])], 'exact': okx is True, 'cross_field': okx is None,
                        'proportion': proportion2(pid, h1, h2) if okx else None})
    res[pid] = {'zero': False, 'support': sorted(p['exact']), 'one_helper': sorted(one, key=lambda d: (not d['proportions'], d['proportions'][0]['n'] + d['proportions'][0]['m'] if d['proportions'] else 0)),
                'two_helpers': two, 'unproved_relation': p['unproved']}
    print(f"{pid}: support {sorted(p['exact'])}; one-helper cancellations {len(one)}; two-helper {len(two) if not one else '-'}", flush=True)

out = {'basis': B, 'packets': {pid: {'support': sorted(P[pid]['exact']), 'numeric': {str(b): mp.nstr(x, 30) for b, x in P[pid]['mp'].items()},
                                     'exact': {str(b): {str(k): [str(t) for t in x] for k, x in v.items()} for b, v in P[pid]['exact'].items()},
                                     'field': P[pid]['field'], 'kind': P[pid]['kind'], 'unproved_relation': P[pid]['unproved']} for pid in P},
       'radicands': {k: [[str(t) for t in r] for r in R.rads] for k, R in RAD.items()},
       'screen': res}
json.dump(out, open(os.path.join(HERE, 'data', 'packets.json'), 'w'), indent=1)
print(f'zero packets: {sorted(cz)}')
print(f'[{time.time() - t0:.1f}s]')
print('FINAL ok' if not FAIL else f'FINAL FAIL {FAIL}')
