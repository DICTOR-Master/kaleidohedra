# Packet screen 2026-11-21, step 3: Q-linear relations among the irrational dihedral angles and pi.
# (a) Square classes: for theta with cos^2 = c2 in the field K, w = exp(2 i theta) = (2 c2 - 1) + 2 sqrt(-c2 (1 - c2)) lies in
#     K(sqrt(-d)), d = c2 (1 - c2).  Angles are grouped by the class of d in K*/K*^2 (exact square tests).
#     Kummer lemma (proved in README): in a relation sum k_j theta_j in Q pi among irrational angles, no angle's class can lie
#     outside the span of the other angles' classes; in particular an angle whose class is shared by no other angle, and is not a
#     product of other classes, takes part in no relation.  We use the classes only to ORDER the search; the search itself is PSLQ.
# (b) PSLQ (mpmath, 300 digits, coefficients <= 10^4) builds a basis greedily: each angle is tested against [basis..., pi].
# (c) Every relation found is PROVED exactly: prod_j (cos_j + i sin_j)^(k_j) = (-1)^p is checked as an identity in the formal
#     radical ring K[i, sqrt(c2_j), sqrt(1 - c2_j)] (sound for every choice of roots, hence for the true ones).
import sys, os, json, time
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, os.path.dirname(__file__))
from nf import fields, Radicals

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DPS = 300
mp.mp.dps = DPS + 20
F = fields()
for K in F.values():   # refine roots to working precision
    f = lambda t, K=K: sum(mp.mpf(c.numerator) / c.denominator * t ** i for i, c in enumerate(K.m))
    K.r = mp.findroot(f, K.r); K.pw = [K.r ** i for i in range(K.n)]
FAIL = []
def check(label, ok):
    print(('ok   ' if ok else 'FAIL ') + label, flush=True)
    if not ok: FAIL.append(label)

def el(K, s): return K.el([Fr(t) for t in s])

def prove(rel, ang, K):
    """rel: dict angle_id -> integer k, plus 'pi': p meaning sum k theta = p pi.  All angles in field K."""
    R = Radicals(K); I = R.imag(); z = {0: K.q(1)}
    for aid, k in rel.items():
        if aid == 'pi': continue
        o = ang[aid]['occ']; c2 = el(K, o[2]); sg = o[1]
        c = R.scal(K.q(sg), R.register(c2)); s = R.register(K.sub(K.q(1), c2))
        zz = R.add(c, R.mul(I, s)) if k > 0 else R.sub(c, R.mul(I, s))
        z = R.mul(z, R.pow(zz, abs(k)))
    target = {0: K.q(-1 if rel['pi'] % 2 else 1)}
    ok = R.iszero(R.sub(z, target))
    return ok, abs(R.num(z) - R.num(target))

def main():
    rows = json.load(open(os.path.join(HERE, 'data', 'angles.json')))
    ang = {}
    for r in rows:
        if r['rational']: continue
        o = r['occurs'][0]; K = F[o[0]]; c2 = el(K, o[2])
        cosv = o[1] * mp.sqrt(K.num(c2)); th = mp.acos(cosv)
        assert abs(th - mp.mpf(r['theta'])) < mp.mpf(10) ** -100
        ang[r['id']] = {'occ': o, 'field': o[0], 'theta': th, 'deg': r['deg'], 'c2': c2, 'd': K.mul(c2, K.sub(K.q(1), c2))}
    # (a) square classes per field
    classes = {}
    for aid, a in ang.items():
        K = F[a['field']]; placed = False
        for key, members in classes.items():
            if key[0] != a['field']: continue
            b = ang[members[0]]
            if K.sqrt(K.mul(a['d'], b['d'])) is not None: members.append(aid); placed = True; break
        if not placed: classes[(a['field'], aid)] = [aid]
    print(f'irrational angles: {len(ang)}; square classes of c2(1-c2): {len(classes)}')
    for key, m in classes.items(): print('  class', key, [f"{ang[i]['deg'][:9]}" for i in m])
    # (b) greedy PSLQ: first inside each class, then across classes
    order = []
    for key, m in sorted(classes.items(), key=lambda kv: -len(kv[1])): order += sorted(m, key=lambda i: ang[i]['theta'])
    basis = []; relations = []; t0 = time.time(); done = set()
    ck = os.path.join(HERE, 'data', 'relations-checkpoint.json')   # resume (the search is split into runs under ~280 s)
    if os.path.exists(ck):
        st = json.load(open(ck)); basis = st['basis']; relations = st['relations']; done = set(st['done'])
        print(f'resumed: {len(done)} angles done, basis {len(basis)}', flush=True)
    tol = mp.mpf(10) ** -(DPS - 60)
    cls = {aid: k for k, m in classes.items() for aid in m}
    for aid in order:
        if aid in done: continue
        r = None
        # first against the basis angles of the same square class (small, fast), then against the whole basis
        for pool in ([b for b in basis if cls[b] == cls[aid]], basis):
            vec = [ang[aid]['theta']] + [ang[b]['theta'] for b in pool] + [mp.pi]
            with mp.workdps(DPS):
                r = mp.pslq(vec, maxcoeff=10 ** 4, maxsteps=10 ** 6, tol=tol)
            if r is not None and r[0] != 0:
                r = [r[0]] + [r[1 + pool.index(b)] if b in pool else 0 for b in basis] + [r[-1]]; break
            r = None
        done.add(aid)
        if r is None:
            basis.append(aid); json.dump({'basis': basis, 'relations': relations, 'done': sorted(done)}, open(ck, 'w')); print(f'   basis + th{aid} ({ang[aid]["deg"][:10]} deg) [{time.time() - t0:.1f}s]', flush=True); continue
        rel = {aid: r[0]}
        for j, b in enumerate(basis):
            if r[1 + j]: rel[b] = r[1 + j]
        rel['pi'] = -r[-1]
        fset = set(ang[i]['field'] for i in rel if i != 'pi')
        if len(fset) == 1:
            ok, err = prove(rel, ang, F[fset.pop()])
        else:
            ok, err = False, None
        relations.append({'angle': aid, 'relation': {str(k): v for k, v in rel.items()}, 'proved_exact': ok,
                          'text': ' + '.join(f'({v})*th{k}' for k, v in rel.items() if k != 'pi') + f" = ({rel['pi']})*pi"})
        json.dump({'basis': basis, 'relations': relations, 'done': sorted(done)}, open(ck, 'w'))
        check(f"relation for th{aid} ({ang[aid]['deg'][:10]} deg): {relations[-1]['text']}  proved exactly", ok)
    out = {'dps': DPS, 'maxcoeff': 10 ** 4, 'basis': basis,
           'basis_deg': {b: ang[b]['deg'] for b in basis},
           'classes': [[k[0], m] for k, m in classes.items()], 'relations': relations}
    json.dump(out, open(os.path.join(HERE, 'data', 'relations.json'), 'w'), indent=1)
    print(f'basis angles: {len(basis)}; relations: {len(relations)}; proved: {sum(r["proved_exact"] for r in relations)}  [{time.time() - t0:.1f}s]')
    allp = all(r['proved_exact'] for r in relations)
    print('FINAL ok' if (not FAIL and allp) else f'FINAL FAIL {FAIL} all relations proved: {allp}')

if __name__ == '__main__':
    main()
