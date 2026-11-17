#!/usr/bin/env python3
"""Differential test (shape kernel, stage 1 proper, 2026-11-18; the pilot's test extended to every group): every copy against the kernel.
G1-G3 as in the pilot (code unchanged); G4-G8 and the vectorised Z[phi] copy through tests/diff_fields.py.
For each copy listed in data/inventory.json, its class (G1, G2) or its pair functions (G3) are lifted out of the study file with
the AST (only imports, function and class definitions and simple constants are executed; no study code runs) and every operation the
copy provides is compared with the kernel's on random and hard elements: + - * / neg inv conj norm pow abs sign == < <= > >= floor
float hash, and the repr / str text against the kernel's named STYLES (the matching style is recorded per copy).
usage: test_differential.py <studies root> [n]     writes data/differential.json; FINAL ok if every copy agrees on every operation
it provides (repr: some kernel style reproduces it) and every planted wrong copy (one per group) is flagged."""
import os, sys, ast, json, math, random, re, collections, traceback, warnings
from fractions import Fraction as Fr
from decimal import Decimal
warnings.simplefilter('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from kernel import Quad, STYLES
from kernel import pairs as KP

ROOT = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
INV = json.load(open(os.path.join(HERE, '..', 'data', 'inventory.json')))
rng = random.Random(1118)
SAFE = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)


def safe_value(v):
    if isinstance(v, (ast.Lambda, ast.Constant)): return True
    if isinstance(v, ast.Tuple): return all(safe_value(e) for e in v.elts)
    if isinstance(v, (ast.BinOp, ast.UnaryOp)): return all(safe_value(e) for e in ast.iter_child_nodes(v) if isinstance(e, ast.expr))
    if isinstance(v, ast.Call):       # Fr(1, 2), math.sqrt(5), Q5(...) style constants
        fn = v.func.id if isinstance(v.func, ast.Name) else (v.func.attr if isinstance(v.func, ast.Attribute) else '')
        return fn in ('Fr', 'F', 'Fraction', 'sqrt', 'Q5', 'Q', 'QF', 'K', 'float', 'int') and all(safe_value(a) for a in v.args) and not v.keywords
    if isinstance(v, (ast.Name, ast.Attribute)): return True
    return False


def lift(path):
    """execute the definitions of a study file in a fresh namespace (no top-level computation)"""
    src = open(os.path.join(ROOT, path), encoding='utf-8').read(); tree = ast.parse(src)
    ns = {'__name__': 'lifted', '__file__': os.path.join(ROOT, path), 'Fr': Fr, 'F': Fr, 'Fraction': Fr, 'math': math, 'Decimal': Decimal}
    try: import gmpy2  # noqa
    except ImportError: ns.update(mpq=Fr, MPQ=Fr)    # stage 1 proper: gmpy2 is absent on the compute machine; mpq is a rational, as Fraction
    d = os.path.dirname(os.path.join(ROOT, path)); before = set(sys.modules); sys.path.insert(0, d)   # sibling modules (mixlib imports zsurf)
    try: _lift_body(tree, path, ns)
    finally:
        sys.path.remove(d)
        for m in set(sys.modules) - before:
            f = getattr(sys.modules[m], '__file__', None) or ''
            if f.startswith(d): del sys.modules[m]
    return ns


def _lift_body(tree, path, ns):
    for node in tree.body:
        if isinstance(node, SAFE) or (isinstance(node, ast.Assign) and safe_value(node.value)):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names]
                mod = getattr(node, 'module', None) or ''
                if any(m.split('.')[0] in ('matplotlib', 'pyvista', 'trimesh', 'plotly') for m in names + [mod]): continue
            try: exec(compile(ast.Module(body=[node], type_ignores=[]), path, 'exec'), ns)
            except Exception: pass


def els(d):
    out = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(-3, 2), Fr(0)), (Fr(0), Fr(-2, 3)), (Fr(1, 2), Fr(1, 2)), (Fr(-1, 2), Fr(1, 2))]
    F_, L_ = [0, 1], [2, 1]
    for n in range(30): F_.append(F_[-1] + F_[-2]); L_.append(L_[-1] + L_[-2])
    if d == 5: out += [(Fr(L_[n]), Fr(-F_[n])) for n in (10, 20, 30)] + [(Fr(-L_[n]), Fr(F_[n])) for n in (11, 25)]
    for _ in range(N):
        m = rng.choice((9, 100, 10 ** 9))
        out.append((Fr(rng.randint(-m, m), rng.randint(1, m)), Fr(rng.randint(-m, m), rng.randint(1, m)) if rng.random() > 0.15 else Fr(0)))
    return out


def ab(x):
    if isinstance(x, (int, Fr)): return (Fr(x), Fr(0))
    if hasattr(x, 'a') and hasattr(x, 'b'): return (x.a, x.b)
    if hasattr(x, 'v'): return tuple(x.v[:2])
    return x


def run_class(row):
    ns = lift(row['path']); C = ns.get(row['cls'])
    if C is None: return {'status': 'not lifted'}
    own = set(row['methods'])
    meths = own | {m for m in ('f', 'inv', 'conj', 'gal', 'sig', 'norm', 'floor', 'dec', 'iszero', 'zero', 'z', 'is_zero', 'sign') if hasattr(C, m)}
    per_d = row.get('per_element_d')
    multi = per_d or hasattr(C, 'D') or 'field' in own
    fields = [5, 2, 3, 6] if multi else [5]
    res = collections.Counter(); bad = collections.defaultdict(list); notprov = set(); floatmode = set(); styles = None; str_styles = None; hash_mode = set()
    for d in fields:
        if row['cls'] == 'QF' and not per_d:
            if 'field' in row['methods'] and isinstance(C.__dict__.get('field'), classmethod): Cd = C.field(d)
            else: C.D = d; Cd = C
            mk = lambda a, b: Cd(a, b)
        elif per_d:
            try: C(1, 1, d); mk = lambda a, b, d=d: C(a, b, d)
            except TypeError: mk = lambda a, b, d=d: C(a, b, d=d)
        else:
            mk = lambda a, b: C(a, b)
        E = els(d); pairs = list(zip(E, E[1:] + E[:1]))
        for (xa, xb), (ya, yb) in pairs:
            x, y = mk(xa, xb), mk(ya, yb); kx, ky = Quad(xa, xb, d), Quad(ya, yb, d)
            def cmpop(name, f, g):
                try: got = f()
                except ZeroDivisionError: got = 'ZeroDivisionError'
                except AssertionError: got = 'ZeroDivisionError' if (name in ('/', 'inv')) else 'AssertionError'
                except Exception as e: got = type(e).__name__
                try: want = g()
                except ZeroDivisionError: want = 'ZeroDivisionError'
                if isinstance(got, str) and got in ('AttributeError', 'TypeError'): notprov.add(name); return   # op not provided by the copy
                res[name] += 1
                if (ab(got) if not isinstance(got, (bool, str, float)) else got) != (ab(want) if not isinstance(want, (bool, str, float)) else want):
                    bad[name].append(f'd={d} x={xa}|{xb} y={ya}|{yb}: copy {got!r} kernel {want!r}')
            cmpop('+', lambda: x + y, lambda: kx + ky); cmpop('-', lambda: x - y, lambda: kx - ky); cmpop('*', lambda: x * y, lambda: kx * ky)
            cmpop('int*', lambda: 3 * x, lambda: 3 * kx); cmpop('+int', lambda: x + 2, lambda: kx + 2)
            if '__truediv__' in meths: cmpop('/', lambda: x / y, lambda: kx / ky)
            if '__neg__' in meths: cmpop('neg', lambda: -x, lambda: -kx)
            if 'inv' in meths: cmpop('inv', lambda: x.inv(), lambda: kx.inv())
            for cn in ('conj', 'gal', 'sig'):
                if cn in meths: cmpop(cn, lambda cn=cn: getattr(x, cn)(), lambda: kx.conj())
            if 'norm' in meths: cmpop('norm', lambda: x.norm(), lambda: kx.norm())
            if '__pow__' in meths: cmpop('pow3', lambda: x ** 3, lambda: kx ** 3)
            if '__abs__' in meths: cmpop('abs', lambda: abs(x), lambda: abs(kx))
            if 'sign' in meths: cmpop('sign', lambda: x.sign(), lambda: kx.sign())
            if '__eq__' in own: cmpop('==', lambda: x == y, lambda: kx == ky); cmpop('==self', lambda: x == mk(xa, xb), lambda: True)
            else: notprov.add('== (identity only)')
            import operator as O
            for op, fn in (('<', O.lt), ('<=', O.le), ('>', O.gt), ('>=', O.ge)):
                cmpop(op, lambda fn=fn: fn(x, y), lambda fn=fn: fn(kx, ky))
            if 'floor' in meths: cmpop('floor', lambda: x.floor(), lambda: kx.floor())
            for fn in ('f', '__float__'):
                if fn in meths or fn in own:
                    try: fv = float(x) if fn == '__float__' else x.f()
                    except Exception: notprov.add('float'); continue
                    res['float'] += 1
                    if fv == float(kx): floatmode.add('plain')
                    elif fv == kx.float_hp(): floatmode.add('high precision')
                    else: bad['float'].append(f'd={d} x={xa}|{xb}: copy {fv!r} kernel {float(kx)!r} / {kx.float_hp()!r}')
            if 'dec' in meths: cmpop('dec', lambda: x.dec(15), lambda: kx.dec(15))
            for zn in ('iszero', 'zero', 'z', 'is_zero'):
                if zn in meths: cmpop('iszero', lambda zn=zn: getattr(x, zn)(), lambda: kx.iszero())
            if '__hash__' in meths and C.__hash__ is not None:
                h = hash(x)
                if h == hash((xa, xb)): hash_mode.add('pair')
                elif h == hash(xa) and xb == 0: hash_mode.add('rational')
                elif h == hash(Quad(xa, xb, d)): hash_mode.add('rational')
                else: hash_mode.add('other')
            # repr / str styles
            for kind in ('repr', 'str'):
                try: txt = repr(x) if kind == 'repr' else str(x)
                except Exception: continue
                if ' object at 0x' in txt: continue
                ok = {s for s, f in STYLES.items() if f(kx) == txt}
                if kind == 'repr': styles = ok if styles is None else styles & ok
                else: str_styles = ok if str_styles is None else str_styles & ok
    fails = {k: v[:3] + [f'... {len(v)} in all'] for k, v in bad.items()}
    return {'status': 'ok' if not bad else 'differs', 'fields': fields, 'ops_compared': dict(res), 'differences': fails,
            'repr_styles': sorted(styles) if styles is not None else None, 'str_styles': sorted(str_styles) if str_styles is not None else None,
            'hash': sorted(hash_mode), 'not_provided': sorted(notprov), 'float_mode': sorted(floatmode)}


PAIR_FUN = {'qa': lambda x, y: KP.qa(x, y), 'qs': KP.qs, 'qm': KP.qm, 'qn': KP.qn, 'qinv': KP.qinv, 'qd': KP.qd, 'qf': KP.qf,
            'sgn': KP.sgn, 'qsgn': KP.qsgn, 'cmp': KP.cmp, 'qr': KP.qr, 'qs_': KP.qs_, 'q': KP.q, 'qsum': KP.qsum}


def run_pairs(row):
    ns = lift(row['path']); res = collections.Counter(); bad = collections.defaultdict(list)
    E = els(5); qstr_kind = None
    for (x, y) in zip(E, E[1:] + E[:1]):
        for name in row['functions']:
            f = ns.get(name)
            if f is None: continue
            if name in ('qa', 'qs', 'qm', 'qd', 'cmp'): args = (x, y)
            elif name in ('qn', 'qinv', 'qf', 'sgn', 'qsgn', 'qs_'): args = (x,)
            elif name == 'qr': args = (x[0],)
            elif name == 'q': args = (KP.qs_(x),)
            elif name == 'qsum': args = ([x, y, x],)
            elif name == 'qstr':
                t = f(x)
                k = 'sqrt5 text' if t == KP.qstr(x) else ('a|b (float) text' if t == KP.qstr_float(x) else 'unmatched')
                qstr_kind = k if qstr_kind in (None, k) else 'mixed'; res['qstr'] += 1; continue
            else: continue
            try: got = f(*args)
            except ZeroDivisionError: got = 'ZeroDivisionError'
            try: want = PAIR_FUN[name](*args)
            except ZeroDivisionError: want = 'ZeroDivisionError'
            res[name] += 1
            if got != want: bad[name].append(f'x={x} y={y}: copy {got!r} kernel {want!r}')
    if qstr_kind == 'unmatched': bad['qstr'].append('no kernel qstr form matches')
    return {'status': 'ok' if not bad else 'differs', 'ops_compared': dict(res), 'differences': {k: v[:3] + [f'... {len(v)} in all'] for k, v in bad.items()},
            'qstr': qstr_kind}


out = {}; summary = []
for g in ('G1', 'G2', 'G3'):
    for row in INV['groups'][g]['rows']:
        try: r = run_pairs(row) if g == 'G3' else run_class(row)
        except Exception as e: r = {'status': 'error', 'error': traceback.format_exc(limit=2)[-600:]}
        out[row['path']] = dict(group=g, **r)
        nops = sum(r.get('ops_compared', {}).values())
        rs = r.get('repr_styles'); sty = '' if g == 'G3' else (f" repr style: {rs[0] if rs else 'NONE'}" if rs is not None else ' repr: none / default')
        print(f"{g} {r['status']:8s} {nops:6d} comparisons  {row['path']}{sty}" + (f"  DIFF {sorted(r['differences'])}" if r.get('differences') else ''))
        summary.append((g, row['path'], r['status'], rs))
# ---------------------------------------------------------------- stage 1 proper: G4-G8 and the vectorised Z[phi] copy
import diff_fields as DF
lift.ROOT = ROOT
new = DF.run_new(INV, ROOT, lift, max(60, N // 2))
for k, r in new.items():
    out[k] = r
    nops = sum(r.get('ops_compared', {}).values())
    ref = sum(r.get('copy_refused_sign', {}).values()); cw = sum(int(v[-1].split()[1]) for v in r.get('copy_wrong_checked_at_120_digits', {}).values())
    print(f"{r['group']} {r['status']:8s} {nops:6d} comparisons  {k}" + (f"  (copy refused {ref} by its own guard: {r['copy_refused_sign']})" if ref else '')
          + (f"  (copy WRONG on {cw}: {sorted(r['copy_wrong_checked_at_120_digits'])}, kernel = 120-digit value)" if cw else '')
          + (f"  DIFF {sorted(r['differences'])}" if r.get('differences') else '') + (f"  ERROR {r['error'][-300:]}" if r.get('error') else ''))
    summary.append((r['group'], k, r['status'], ['new']))
# harness self-test: planted wrong copies, one per group, must be flagged on the planted operation
MUT = os.path.join(HERE, 'mutants')
m1 = run_class({'path': os.path.join(MUT, 'q5_wrong_sign.py'), 'cls': 'Q5', 'methods': ['__init__', '__add__', '__mul__', 'sign']})
m2 = run_class({'path': os.path.join(MUT, 'qf_wrong_mul.py'), 'cls': 'QF', 'methods': ['__init__', '__add__', '__mul__', '__eq__']})
mrng = __import__('random').Random(7)
mut = {
    'G1 q5_wrong_sign': (m1, 'sign'), 'G2 qf_wrong_mul': (m2, '*'),
    'G4 k_wrong_sign': (DF.one('G4', {'path': os.path.join(MUT, 'k_wrong_sign.py'), 'cls': 'K', 'code': 'mq', 'methods': ['__init__', '__add__', '__mul__', 'sign']}, lift, mrng, 60), 'sign'),
    'G5 golden_wrong_mul': (DF.one('G5', {'path': os.path.join(MUT, 'golden_wrong_mul.py'), 'cls': 'Q5', 'methods': ['__init__', '__add__', '__mul__', '__eq__']}, lift, mrng, 60), '*'),
    'G6 zphi_wrong_sign': (DF.one('G6', {'path': os.path.join(MUT, 'zphi_wrong_sign.py'), 'functions': ['zadd', 'zmul', 'zsign']}, lift, mrng, 60), 'zsign'),
    'G7 mut_exactlib_kc': (DF.one('G7', {'path': os.path.join(MUT, 'mut_exactlib_kc.py'), 'cls': 'KC', 'methods': ['__init__', '__add__', '__mul__', 'norm', 'sign', '__eq__']}, lift, mrng, 60), 'sign'),
    'G8 qd_wrong_inv': (DF.one('G8', {'path': os.path.join(MUT, 'qd_wrong_inv.py'), 'cls': 'QD', 'd': 'D', 'methods': ['__init__', '__add__', '__mul__', 'inv']}, lift, mrng, 60), 'inv'),
}
caught = True
for name, (r, want) in mut.items():
    ok = want in r.get('differences', {}) or want in r.get('copy_wrong_checked_at_120_digits', {})   # a wrong sign is settled at 120 digits
    caught &= ok
    print(f"harness self-test {name}: flagged on {sorted(r.get('differences', {}))}, copy wrong at 120 digits on {sorted(r.get('copy_wrong_checked_at_120_digits', {}))} "
          f"(planted: {want}): {'ok' if ok else 'FAIL'}")
out['_mutants'] = {k: v[0] for k, v in mut.items()}
json.dump(out, open(os.path.join(HERE, '..', 'data', 'differential.json'), 'w'), indent=1, default=str)
st = collections.Counter((g, s) for g, _, s, _ in summary)
print('summary:', dict(sorted(st.items())))
no_style = [p for g, p, s, rs in summary if g in ('G1', 'G2') and rs == []]
print('copies whose repr no kernel style reproduces:', no_style)
nd = sum(1 for _, _, s, _ in summary if s not in ('ok', 'ok, copy wrong where noted'))
print('FINAL ok: every copy agrees with the kernel on every operation it provides; planted wrong copies caught in every group' if nd == 0 and not no_style and caught
      else f'FINAL FAIL: {nd} copies differ or could not be lifted, {len(no_style)} repr styles missing, mutants caught: {caught} (see data/differential.json)')
