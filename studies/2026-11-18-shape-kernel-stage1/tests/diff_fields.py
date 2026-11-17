"""Differential test of the stage-1-proper groups (G4-G8) against the kernel; used by tests/test_differential.py.

Each copy is lifted from its study file by the AST (tests/test_differential.py: lift; no study code runs) and compared, operation by
operation, with its kernel counterpart: the shim class that the replays use (replay/shims/*.py) where a shim exists, otherwise the
kernel element of the same field (Quad, NF, MQ, zphi).  Elements: random coefficients (small and 9-digit) and near-zero elements
built from units of each field.  Operations: + - * neg / inv sign == < <= > >= abs pow conj norm iszero float dec hash repr, and for
AlgField the field's own methods (poly_string, approx, interval_value) with the bisection state compared after every call."""
import os, sys, math, random, collections, operator as O
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.join(HERE, '..')
from kernel import Quad, STYLES
from kernel.field import NF, MQ, NumberField, GOLDEN, pure_field, NF_STYLES, MQ_STYLES
from kernel import zphi as KZ

SHIMS = os.path.join(BASE, 'replay', 'shims')


def shim(name):
    ns = {'__name__': 'shim_' + name}
    exec(compile(open(os.path.join(SHIMS, name + '.py')).read(), name, 'exec'), ns)
    return ns


F_, L_ = [0, 1], [2, 1]
for _n in range(90): F_.append(F_[-1] + F_[-2]); L_.append(L_[-1] + L_[-2])
PELL = {2: (3, 2), 3: (2, 1), 5: (9, 4), 6: (5, 2), 10: (19, 6)}


def quad_near(d, k=24):
    u0, w0 = PELL[d]; u, w = u0, w0; out = []
    for _ in range(k):
        out += [(Fr(u), Fr(-w)), (Fr(-u), Fr(w))]
        u, w = u0 * u + d * w0 * w, w0 * u + u0 * w
    if d == 5: out += [(Fr(L_[n]), Fr(-F_[n])) for n in range(4, 80, 5)]
    return out


def golden_near(k=70):
    return [(Fr((-1) ** j * F_[j + 1]), Fr((-1) ** (j + 1) * F_[j])) for j in range(1, k)]


def rnd(rng, n, m):
    return tuple(Fr(rng.randint(-m, m), rng.randint(1, m)) if rng.random() > 0.15 else Fr(0) for _ in range(n))


def coeff_sets(rng, n, near, N):
    base = [tuple([Fr(0)] * n), tuple([Fr(1)] + [Fr(0)] * (n - 1)), tuple([Fr(0), Fr(1)] + [Fr(0)] * (n - 2))[:n], tuple([Fr(-3, 2)] + [Fr(0)] * (n - 1))]
    return base + list(near) + [rnd(rng, n, rng.choice((9, 100, 10 ** 9))) for _ in range(N)]


def unit_powers(F, u, k=30):
    if u.sign() < 0: u = -u
    if u > 1: u = u.inv()
    out = []
    for j in range(1, k):
        w = u ** j; out += [w.c, (-w).c, (w - u ** (j + 1)).c]
    return out


def mq_near():
    e2, e5 = MQ(-1, 1), MQ(Fr(-1, 2), 0, Fr(1, 2)); out = []
    for i in range(1, 26, 4):
        for j in range(1, 36, 5):
            u, w = e2 ** i, e5 ** j; out += [(u * w).v, (u - w).v, (w - u).v]
    return out


SIGNLIKE = ('sign', '<', '<=', '>', '>=', 'abs')
import mpmath as _mp


def mpval(X):
    """an independent 120-digit value of a kernel element (mpmath), to settle a sign on which a copy and the kernel differ"""
    _mp.mp.dps = 120
    f = lambda q: _mp.mpf(q.numerator) / q.denominator
    if isinstance(X, Quad): return f(X.a) + f(X.b) * _mp.sqrt(X.d)
    if isinstance(X, MQ): p, q = X.RADS; a, b, c, d = X.v; return f(a) + f(b) * _mp.sqrt(p) + f(c) * _mp.sqrt(q) + f(d) * _mp.sqrt(p * q)
    if isinstance(X, NF):
        F = X.F; rts = _mp.polyroots([f(c) for c in F.P], maxsteps=300, extraprec=400)
        t = [_mp.re(r) for r in rts if abs(_mp.im(r)) < _mp.mpf(10) ** -90 and f(F.lo0) < _mp.re(r) < f(F.hi0)][0]
        return sum(f(c) * t ** i for i, c in enumerate(X.c))
    return None


def truth_for(X, Y):
    def t(name):
        try:
            if name == 'sign': v = mpval(X); return None if v is None or abs(v) < _mp.mpf(10) ** -100 else int(_mp.sign(v))
            if name == 'abs': return None
            v = mpval(X - Y)
            if v is None or abs(v) < _mp.mpf(10) ** -100: return None
            sg = int(_mp.sign(v)); return {'<': sg < 0, '<=': sg <= 0, '>': sg > 0, '>=': sg >= 0}[name]
        except Exception: return None
    return t


class Cmp:
    """records the comparisons of one copy"""
    def __init__(s):
        s.n = collections.Counter(); s.bad = collections.defaultdict(list); s.notprov = set(); s.refused = collections.Counter()
        s.copy_wrong = collections.defaultdict(list); s.truth = None

    def op(s, name, f, g, rd, kd, ctx=''):
        try: got = f()
        except ZeroDivisionError: got = 'ZeroDivisionError'
        except AssertionError as e:
            if name in ('/', 'inv'): got = 'ZeroDivisionError'
            elif name in ('sign', '<', '<=', '>', '>=', 'abs'): s.refused[name] += 1; return
            else: got = 'AssertionError'
        except (AttributeError, TypeError, NotImplementedError): s.notprov.add(name); return
        except StopIteration:                    # a copy's Gauss-Jordan inverse finds no pivot on 0: its way of refusing 1/0
            if name in ('/', 'inv'): got = 'ZeroDivisionError'; s.refused['1/0 as StopIteration'] += 1
            else: got = 'StopIteration'
        except Exception as e: got = type(e).__name__
        try: want = g()
        except ZeroDivisionError: want = 'ZeroDivisionError'
        s.n[name] += 1
        cg = got if isinstance(got, (bool, int, str, float, Fr)) or got is None else rd(got)
        cw = want if isinstance(want, (bool, int, str, float, Fr)) or want is None else kd(want)
        if isinstance(cg, tuple): cg = tuple(Fr(x) if not isinstance(x, Fr) else x for x in cg)
        if cg != cw:
            if name in SIGNLIKE and s.truth is not None:
                tv = s.truth(name)
                if tv is not None and tv == cw: s.copy_wrong[name].append(f'{ctx}: copy {got!r}, kernel {want!r} = 120-digit value'); return
            s.bad[name].append(f'{ctx}: copy {got!r} kernel {want!r}')

    def result(s, extra=None):
        r = {'status': ('ok' if not s.copy_wrong else 'ok, copy wrong where noted') if not s.bad else 'differs', 'ops_compared': dict(s.n),
             'copy_wrong_checked_at_120_digits': {k: v[:3] + [f'... {len(v)} in all'] for k, v in s.copy_wrong.items()},
             'differences': {k: v[:3] + [f'... {len(v)} in all'] for k, v in s.bad.items()}, 'not_provided': sorted(s.notprov),
             'copy_refused_sign': dict(s.refused)}
        r.update(extra or {})
        return r


def compare_elements(C, mk, kk, rd, kd, sets, ctx, meths, cmp_repr=True, float_name=None, dec=False, float_k=None):
    """mk(coeffs) -> copy element, kk(coeffs) -> kernel element; rd / kd read a result's coefficients"""
    c = Cmp(); reprs = collections.Counter(); hashes = collections.Counter()
    E = sets
    for xa, ya in zip(E, E[1:] + E[:1]):
        x, y, X, Y = mk(xa), mk(ya), kk(xa), kk(ya); t = f'{ctx} x={xa} y={ya}'; c.truth = truth_for(X, Y)
        c.op('+', lambda: x + y, lambda: X + Y, rd, kd, t); c.op('-', lambda: x - y, lambda: X - Y, rd, kd, t)
        c.op('*', lambda: x * y, lambda: X * Y, rd, kd, t); c.op('neg', lambda: -x, lambda: -X, rd, kd, t)
        c.op('int*', lambda: x * 3, lambda: X * 3, rd, kd, t); c.op('+int', lambda: x + 2, lambda: X + 2, rd, kd, t)
        if '__truediv__' in meths: c.op('/', lambda: x / y, lambda: X / Y, rd, kd, t)
        if 'inv' in meths: c.op('inv', lambda: x.inv(), lambda: X.inv(), rd, kd, t)
        for cn, kn in (('conj', 'conj'), ('gal', 'conj'), ('conj2', 'conj2'), ('conj5', 'conj5')):
            if cn in meths: c.op(cn, lambda cn=cn: getattr(x, cn)(), lambda kn=kn: getattr(X, kn)(), rd, kd, t)
        if 'norm' in meths: c.op('norm', lambda: x.norm(), lambda: X.norm(), rd, kd, t)
        if '__pow__' in meths: c.op('pow3', lambda: x ** 3, lambda: X ** 3, rd, kd, t)
        if '__abs__' in meths: c.op('abs', lambda: abs(x), lambda: abs(X), rd, kd, t)
        if 'sign' in meths: c.op('sign', lambda: x.sign(), lambda: X.sign(), rd, kd, t)
        if '__eq__' in meths: c.op('==', lambda: x == y, lambda: X == Y, rd, kd, t); c.op('==self', lambda: x == mk(xa), lambda: True, rd, kd, t)
        for nm, fn in (('<', O.lt), ('<=', O.le), ('>', O.gt), ('>=', O.ge)):
            if any(m in meths for m in ('__lt__', '__le__', '__gt__', '__ge__')):
                c.op(nm, lambda fn=fn: fn(x, y), lambda fn=fn: fn(X, Y), rd, kd, t)
        for zn in ('iszero', 'z', 'zero', 'is_zero'):
            if zn in meths: c.op('iszero', lambda zn=zn: getattr(x, zn)(), lambda: X.iszero(), rd, kd, t)
        if float_name:
            c.op('float', lambda: float(x) if float_name == '__float__' else getattr(x, float_name)(), lambda: float_k(X) if float_k else float(X), rd, kd, t)
        if dec: c.op('dec', lambda: x.dec(15), lambda: X.dec(15), rd, kd, t)
        if '__hash__' in meths:
            c.op('hash', lambda: hash(x), lambda: hash(X), rd, kd, t)
        if cmp_repr and '__repr__' in meths:
            try: reprs[repr(x) == repr(X)] += 1
            except Exception: pass
    extra = {'repr_equal': dict(reprs)}
    if cmp_repr and '__repr__' in meths and reprs.get(False): c.bad['repr'].append(f'{reprs[False]} printed forms differ')
    return c, extra


def tup(x): return tuple(x)


class GoldenPhi(NF):
    """golden basis with the float of residents.py: float(a) + float(b) * ((1 + 5 ** .5) / 2)"""
    __slots__ = (); FLOAT = 'golden (phi first)'


class QuadPair(Quad):
    """the kernel element with the copies' pair hash (every G8 copy hashes (a, b))"""
    __slots__ = (); HASH_PAIR = True


def run_new(INV, ROOT, lift, N, seed=1118):
    rng = random.Random(seed); out = {}
    for g in ('G4', 'G5', 'G6', 'G7', 'G8'):
        for row in INV['groups'][g]['rows']:
            p = row['path']
            try: r = one(g, row, lift, rng, N)
            except Exception as e:
                import traceback; r = {'status': 'error', 'error': traceback.format_exc(limit=3)[-900:]}
            out[p + ('' if g not in ('G7', 'G5', 'G8', 'G4') else f"::{row.get('cls')}")] = dict(group=g, **r)
    # numpy Z[phi] copy found by the wider scan (vectorised, independent check)
    for w in INV['wider_scan'].get('vectorised', []):
        try: r = numpy_zphi(w['path'], lift, rng, N)
        except Exception as e:
            import traceback; r = {'status': 'error', 'error': traceback.format_exc(limit=3)[-900:]}
        out[w['path']] = dict(group='W', **r)
    return out


def one(g, row, lift, rng, N):
    p = row['path']; meths = set(row.get('methods', []))
    if g == 'G6': return zfuncs(p, lift, rng, N, row['functions'])
    ns = lift(p); C = ns.get(row['cls'])
    if C is None: return {'status': 'not lifted'}
    meths |= {m for m in ('inv', 'conj', 'norm', 'sign', 'iszero', 'z', 'f', 'dec') if hasattr(C, m)}
    if g == 'G4':
        code = row['code']
        if code == 'mq':
            K = shim('cubes_lib_K')['K']
            sets = coeff_sets(rng, 4, mq_near(), N)
            c, ex = compare_elements(C, lambda v: C(*v), lambda v: K(*v), lambda z: tuple(z.v), lambda z: tuple(z.v), sets, 'Q(sqrt2,sqrt5)', meths,
                                     float_name='__float__')
            ks = shim('cubes_lib_K')['kstr']
            kb = sum(1 for v in sets if ns['kstr'](C(*v)) != ks(K(*v)))
            if kb: c.bad['kstr'].append(f'{kb} kstr texts differ')
            c.n['kstr'] += len(sets)
            return c.result(dict(ex, fields=['Q(sqrt2, sqrt5)'], kernel='replay/shims/cubes_lib_K.py (MQ)'))
        if code == 'radical':
            sh = shim('octet_special_exact_K'); K = sh['K']; allc = Cmp(); ex = {}
            for n, k in ((2, 2), (2, 6), (3, 2)):
                C.n, C.k = n, k; K.n, K.k = n, k
                F = pure_field(k, n); u = NF([1, 1, 1], F) if (n, k) == (3, 2) else (NF([1, 1], F) if k == 2 else NF([5, 2], F))
                sets = coeff_sets(rng, n, unit_powers(F, u, 25), N // 2)
                c, e = compare_elements(C, lambda v: C(list(v)), lambda v: K(list(v)), lambda z: tuple(z.c), lambda z: tuple(z.c), sets,
                                        f'Q({k}^(1/{n}))', meths, float_name='__float__')
                allc.n.update(c.n); allc.notprov |= c.notprov; allc.refused.update(c.refused); [allc.copy_wrong[k2].extend(v2) for k2, v2 in c.copy_wrong.items()]
                for kk, vv in c.bad.items(): allc.bad[kk] += vv
                ex[f'Q({k}^(1/{n}))'] = e
            C.n, C.k = 2, 2; K.n, K.k = 2, 2
            return allc.result({'per_field': ex, 'fields': ['Q(sqrt2)', 'Q(sqrt6)', 'Q(2^(1/3))'], 'kernel': 'replay/shims/octet_special_exact_K.py (NF)'})
        if code == 'quad5':
            K = shim('pds_line_K')['K']
            sets = coeff_sets(rng, 2, quad_near(5), N)
            c, ex = compare_elements(C, lambda v: C(*v), lambda v: K(*v), lambda z: (z.a, z.b), lambda z: (z.a, z.b), sets, 'Q(sqrt5)', meths,
                                     float_name='__float__')
            return c.result(dict(ex, fields=['Q(sqrt5)'], kernel='replay/shims/pds_line_K.py (Quad)'))
        if code == 'quad-flint':
            allc = Cmp(); ex = {}
            def fr(q): return Fr(int(q.p), int(q.q))
            for d in (2, 5):
                ns['set_field'](d)
                sets = coeff_sets(rng, 2, quad_near(d), N // 2)
                c, e = compare_elements(C, lambda v: C(*v), lambda v, d=d: Quad(v[0], v[1], d), lambda z: (fr(z.a), fr(z.b)), lambda z: (z.a, z.b), sets,
                                        f'Q(sqrt{d})', meths - {'__hash__', '__repr__'}, cmp_repr=False, float_name='__float__',
                                        float_k=lambda X: X.float_hp())
                allc.n.update(c.n); allc.notprov |= c.notprov; allc.refused.update(c.refused); [allc.copy_wrong[k2].extend(v2) for k2, v2 in c.copy_wrong.items()]
                for kk, vv in c.bad.items(): allc.bad[kk] += vv
                rep = sum(1 for v in sets[:60] if repr(C(*v)) == STYLES['(a+b*sqrtd)'](Quad(v[0], v[1], d))); ex[f'repr style (a+b*sqrtd) matches, d={d}'] = f'{rep} of 60'
                if rep != 60: allc.bad['repr'].append(f'd={d}: {60 - rep} of 60 printed forms differ')
            ns['set_field'](2)
            return allc.result(dict(ex, fields=['Q(sqrt2)', 'Q(sqrt5)'], kernel='Quad (no replay shim: a, b are python-flint fmpq numbers that the study\'s '
                                                                                'polynomial class E and its arb balls read directly)',
                                    hash_note='copy hashes (a.p, a.q, b.p, b.q) of python-flint integers; not compared'))
    if g == 'G5':
        cls = row['cls']
        if cls == 'Q':                      # mixlib
            K = shim('mixlib_Q')['Q']
            sets = coeff_sets(rng, 2, golden_near(), N)
            c, ex = compare_elements(C, lambda v: C(*v), lambda v: K(*v), lambda z: (z.a, z.b), lambda z: (z.c[0], z.c[1]), sets, 'Q(phi)', meths,
                                     float_name='f')
            return c.result(dict(ex, fields=['Q(phi), golden basis'], kernel='replay/shims/mixlib_Q.py (NF over GOLDEN)'))
        if cls == 'Q5':                     # echo_lib, qlib
            K = shim('golden_Q5')['Q5']
            sets = coeff_sets(rng, 2, golden_near(), N)
            c, ex = compare_elements(C, lambda v: C(*v), lambda v: K(*v), lambda z: (z.a, z.b), lambda z: (z.c[0], z.c[1]), sets, 'Q(phi)', meths,
                                     float_name='__float__')
            return c.result(dict(ex, fields=['Q(phi), golden basis'], kernel='replay/shims/golden_Q5.py (NF over GOLDEN)'))
        if cls == 'E':                      # residents: a + b phi (d = 5) or a + b sqrt2 (d = 2)
            allc = Cmp(); ex = {}
            g2q = lambda z: (z.c[0] + z.c[1] / 2, z.c[1] / 2) if isinstance(z, NF) else (z.a, z.b)
            for d in (5, 2):
                if d == 5: kk = lambda v: GoldenPhi(list(v), GOLDEN); near = golden_near()
                else: kk = lambda v: QuadPair(v[0], v[1], 2); near = quad_near(2)
                sets = coeff_sets(rng, 2, near, N // 2)
                c, e = compare_elements(C, lambda v, d=d: C(v[0], v[1], d), kk, lambda z: (z.a, z.b), (lambda z: tuple(z.c)) if d == 5 else (lambda z: (z.a, z.b)),
                                        sets, f'd={d}', meths, cmp_repr=False, float_name='__float__')
                allc.n.update(c.n); allc.notprov |= c.notprov; allc.refused.update(c.refused); [allc.copy_wrong[k2].extend(v2) for k2, v2 in c.copy_wrong.items()]
                for kk2, vv in c.bad.items(): allc.bad[kk2] += vv
                rep = sum(1 for v in sets[:80] if repr(C(v[0], v[1], d)) == STYLES['a +- b*sqrtd'](Quad(*g2q(kk(v)), 5 if d == 5 else 2)))
                ex[f'd={d} repr = Quad style "a +- b*sqrtd" (of a + b phi written in sqrt5)'] = f'{rep} of 80'
                if rep != 80: allc.bad['repr'].append(f'd={d}: {80 - rep} of 80 printed forms differ')
            return allc.result(dict(ex, fields=['Q(phi)', 'Q(sqrt2)'], kernel='NF over GOLDEN (d = 5), Quad (d = 2)'))
    if g == 'G7':
        cls = row['cls']
        if cls in ('KC', 'RF', 'AlgField') and 'exactlib' in p:
            sh = shim('exactlib_fields')
            if cls == 'KC':
                K = sh['KC']; allc = Cmp()
                for k in (2, 3, 6):
                    F = pure_field(k, 3); u = {2: NF([1, 1, 1], F), 3: NF([4, 3, 2], F), 6: None}[k]
                    sets = coeff_sets(rng, 3, unit_powers(F, u, 20) if u is not None else [], N // 3)
                    c, e = compare_elements(C, lambda v, k=k: C(*v, k=k), lambda v, k=k: K(*v, k=k), lambda z: tuple(z.c), lambda z: tuple(z.c), sets,
                                            f'Q({k}^(1/3))', meths | {'f', 'dec', 'mp'}, float_name='f', dec=True)
                    allc.n.update(c.n); allc.notprov |= c.notprov; [allc.copy_wrong[k2].extend(v2) for k2, v2 in c.copy_wrong.items()]
                    for kk, vv in c.bad.items(): allc.bad[kk] += vv
                    for v in (sets[:40] if hasattr(C, 'fmt') else []):
                        allc.n['fmt'] += 1
                        if C(*v, k=k).fmt() != K(*v, k=k).fmt(): allc.bad['fmt'].append(str(v))
                        allc.n['mp'] += 1
                        if C(*v, k=k).mp() != K(*v, k=k).mp(): allc.bad['mp'].append(str(v))
                        allc.n['d'] += 1
                        if C(*v, k=k).d != K(*v, k=k).d: allc.bad['d'].append(str(v))
                return allc.result({'fields': ['Q(2^(1/3))', 'Q(3^(1/3))', 'Q(6^(1/3))'], 'kernel': 'replay/shims/exactlib_fields.py KC (NF over pure_field(k, 3))'})
            # RF and AlgField: two separate fields (copy's and kernel's) driven by the same calls; their bisection states must stay equal
            A = ns['AlgField']; RFc = ns['RF']; KR = sh['RF']; KA = sh['AlgField']
            Fc = A([1536, 5184, -3384, 11], Fr(-1, 8), Fr(5, 24), 't'); Fk = KA([1536, 5184, -3384, 11], Fr(-1, 8), Fr(5, 24), 't')
            near = [((-r), Fr(1)) + (Fr(0),) for r in (Fr(math.floor(Fk.approx(Fr(1, 10 ** 30)) * 10 ** j), 10 ** j) for j in range(4, 28, 3))]
            Fk.lo, Fk.hi = Fk.lo0, Fk.hi0               # undo the refinement made to build the near-zero list
            sets = coeff_sets(rng, 3, near, N // 2)
            c, e = compare_elements(RFc, lambda v: RFc(list(v), Fc), lambda v: KR(list(v), Fk), lambda z: tuple(z.c), lambda z: tuple(z.c), sets, 'Q(t) of #56',
                                    set(row['methods']) | {'__lt__', '__eq__', '__hash__', '__truediv__', 'inv', 'sign', '__repr__'}, float_name='f', dec=True)
            st = (Fc.lo, Fc.hi) == (Fk.lo, Fk.hi)
            c.n['bisection state'] += 1
            if not st: c.bad['bisection state'].append(f'copy ({Fc.lo}, {Fc.hi}) kernel ({Fk.lo}, {Fk.hi})')
            c.n['poly_string'] += 1
            if Fc.poly_string() != Fk.poly_string(): c.bad['poly_string'].append('differs')
            c.n['key'] += 1
            if Fc.key != Fk.key: c.bad['key'].append('differs')
            for v in sets[:50]:
                c.n['interval_value'] += 1
                if Fc.interval_value(list(v)) != Fk.interval_value(list(v)): c.bad['interval_value'].append(str(v))
                c.n['mp'] += 1
                if RFc(list(v), Fc).mp() != KR(list(v), Fk).mp(): c.bad['mp'].append(str(v))
            return c.result(dict(e, fields=['Q(t), 1536t^3 + 5184t^2 - 3384t + 11, t in (-1/8, 5/24)'],
                                 kernel='replay/shims/exactlib_fields.py RF, AlgField (NF, NumberField)', bisection_state_equal_at_end=st))
        if cls == 'E':                      # web-of-bonds: general field Q(alpha), sign from 80 digits
            allc = Cmp(); ex = {}
            for fname, F in (('Q5', pure_field(5, 2)), ('Q2', pure_field(2, 2)), ('Q6', pure_field(6, 2)), ('C2', pure_field(2, 3)), ('C6', pure_field(6, 3))):
                Fc = ns.get(fname)
                if Fc is None:                  # the module-level fields are calls (not lifted): build them with the copy's own Field class
                    mpm = ns['mp']; mpm.mp.dps = 80
                    spec = {'Q5': ('Q(sqrt5)', [-5, 0, 1], mpm.sqrt(5)), 'Q2': ('Q(sqrt2)', [-2, 0, 1], mpm.sqrt(2)), 'Q6': ('Q(sqrt6)', [-6, 0, 1], mpm.sqrt(6)),
                            'C2': ('Q(cbrt2)', [-2, 0, 0, 1], mpm.cbrt(2)), 'C6': ('Q(cbrt6)', [-6, 0, 0, 1], mpm.cbrt(6))}[fname]
                    Fc = ns['Field'](*spec)
                u = {'Q5': NF([9, 4], F), 'Q2': NF([1, 1], F), 'Q6': NF([5, 2], F), 'C2': NF([1, 1, 1], F), 'C6': None}[fname]
                sets = coeff_sets(rng, F.n, unit_powers(F, u, 40) if u is not None else [], N // 4)
                c, e = compare_elements(C, lambda v, Fc=Fc: Fc(*v), lambda v, F=F: NF(list(v), F), lambda z: tuple(z.c), lambda z: tuple(z.c), sets, fname,
                                        {'__mul__', '__add__', '__eq__', '__hash__', 'sign', 'iszero'}, cmp_repr=False)
                allc.n.update(c.n); allc.notprov |= c.notprov; allc.refused.update(c.refused); [allc.copy_wrong[k2].extend(v2) for k2, v2 in c.copy_wrong.items()]
                for kk, vv in c.bad.items(): allc.bad[kk] += vv
            return allc.result({'fields': ['Q(sqrt5)', 'Q(sqrt2)', 'Q(sqrt6)', 'Q(2^(1/3))', 'Q(6^(1/3))'], 'kernel': 'NF over pure_field',
                                'note': 'division only by rationals in the copy; repr shows a float, not compared'})
    if g == 'G8':
        cls = row['cls']; d0 = row['d']
        fields = [5] if d0 == '5' else [2, 3, 5]
        allc = Cmp(); ex = {}
        for d in fields:
            if cls == 'QS': ns['M'] = d; mk = lambda v: C(*v)
            elif cls == 'QD': mk = lambda v, d=d: C(v[0], v[1], d)
            elif d0 == 'F.D': C.D = d; mk = lambda v: C(*v)
            elif d0 == 'D': ns['D'] = d; mk = lambda v: C(*v)
            else: mk = lambda v: C(*v)
            # methods read the module-level field from the lifted namespace: rebind it for every function of the class
            sets = coeff_sets(rng, 2, quad_near(d), N // len(fields))
            c, e = compare_elements(C, mk, lambda v, d=d: QuadPair(v[0], v[1], d), lambda z: (Fr(z.a), Fr(z.b)), lambda z: (z.a, z.b), sets, f'd={d}', meths,
                                    cmp_repr=False, float_name='f' if 'f' in meths else '__float__')
            allc.n.update(c.n); allc.notprov |= c.notprov; allc.refused.update(c.refused); [allc.copy_wrong[k2].extend(v2) for k2, v2 in c.copy_wrong.items()]
            for kk, vv in c.bad.items(): allc.bad[kk] += vv
            st = None
            for v in sets[:60]:
                try: txt = repr(mk(v))
                except Exception: continue
                ok = {s for s, f in STYLES.items() if f(Quad(v[0], v[1], d)) == txt}
                st = ok if st is None else st & ok
            ex[f'd={d} repr styles'] = sorted(st) if st is not None else None
            if st is not None and not st: allc.bad['repr'].append(f'd={d}: no kernel style reproduces the printed form')
        return allc.result(dict(ex, fields=[f'Q(sqrt{d})' for d in fields], kernel='Quad (no shim yet: stage 2)',
                                rationals=row.get('rational')))
    return {'status': 'no adapter'}


def zfuncs(p, lift, rng, N, fnames):
    ns = lift(p); c = Cmp()
    import numpy as np
    isnp = 'np.stack' in open(os.path.join(lift.ROOT, p)).read()
    pts = [(rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)) for _ in range(N)] + [(int(a), int(b)) for a, b in golden_near(80)]
    for _ in range(N // 2):                      # large near-zero: b up to 2^49, a = -floor(b phi) + small
        b = rng.randint(-2 ** 49, 2 ** 49); a = -Quad(Fr(b, 2), Fr(b, 2), 5).floor() + rng.randint(-1, 1); pts.append((a, b))
    K = {'zadd': KZ.zadd, 'zsub': KZ.zsub, 'zmul': KZ.zmul, 'zneg': KZ.zneg, 'zsign': KZ.zsign, 'zfloat': KZ.zfloat, 'zconj': KZ.zconj}
    for x, y in zip(pts, pts[1:] + pts[:1]):
        for nm in fnames:
            f = ns.get(nm)
            if f is None: c.notprov.add(nm); continue
            args = (x, y) if nm in ('zadd', 'zsub', 'zmul') else (x,)
            if isnp: args = tuple(np.array([a], dtype=np.int64) for a in args)
            def call():
                r = f(*args)
                if isnp: r = r.tolist()[0]
                return tuple(r) if isinstance(r, list) else r
            if isnp and nm in ('zadd', 'zsub', 'zmul') and max(abs(t) for t in x + y) >= 2 ** 31:
                c.refused['outside the int64 domain of the copy'] += 1; continue
            want = K[nm](*((x, y) if nm in ('zadd', 'zsub', 'zmul') else (x,)))
            try: got = call()
            except AssertionError: c.refused[nm] += 1; continue
            c.n[nm] += 1
            if isinstance(got, float) or isinstance(want, float):
                if float(got) != float(want): c.bad[nm].append(f'x={x}: copy {got!r} kernel {want!r}')
            elif got != want or (not isnp and type(got) != type(want)):
                if nm == 'zsign':
                    _mp.mp.dps = 120; v = _mp.mpf(x[0]) + _mp.mpf(x[1]) * (1 + _mp.sqrt(5)) / 2
                    if int(_mp.sign(v)) == want: c.copy_wrong[nm].append(f'x={x}: copy {got!r}, kernel {want!r} = 120-digit value'); continue
                c.bad[nm].append(f'x={x} y={y}: copy {got!r} kernel {want!r}')
    return c.result({'vectorised_numpy': isnp, 'kernel': 'kernel/zphi.py' + (' (shim replay/shims/zsurf_zphi.py)' if 'zsurf' in p else ''),
                     'elements': f'{len(pts)} integer pairs incl. Fibonacci units and {N // 2} large near-zero pairs (|b| < 2^49)'})


def numpy_zphi(p, lift, rng, N):
    ns = lift(p); c = Cmp()
    import numpy as np
    pts = [(rng.randint(-10 ** 4, 10 ** 4), rng.randint(-10 ** 4, 10 ** 4)) for _ in range(N)] + [(int(a), int(b)) for a, b in golden_near(40)]
    X = np.array(pts, dtype=np.int64); Y = np.roll(X, 1, axis=0)
    got = ns['mul'](X, Y).tolist(); c.n['mul'] += len(pts)
    for g_, x, y in zip(got, X.tolist(), Y.tolist()):
        if tuple(g_) != KZ.zmul(tuple(x), tuple(y)): c.bad['mul'].append(f'{x} {y}: copy {g_} kernel {KZ.zmul(tuple(x), tuple(y))}')
    sg = ns['sign'](X).tolist(); c.n['sign'] += len(pts)
    for s_, x in zip(sg, X.tolist()):
        if s_ != KZ.zsign(tuple(x)): c.bad['sign'].append(f'{x}: copy {s_} kernel {KZ.zsign(tuple(x))}')
    if 'times_phi' in ns:
        tp = ns['times_phi'](X).tolist(); c.n['times_phi'] += len(pts)
        for t_, x in zip(tp, X.tolist()):
            if tuple(t_) != KZ.zmul(tuple(x), (0, 1)): c.bad['times_phi'].append(str(x))
    return c.result({'vectorised_numpy': True, 'kernel': 'kernel/zphi.py',
                     'note': 'written from scratch for an independent check; compared, not to be replaced (independence by design)'})
