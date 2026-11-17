#!/usr/bin/env python3
"""Inventory of exact-number code copied across the studies (shape kernel, stage 1 proper, 2026-11-18).

Extends the pilot's scan (groups G1-G3, unchanged rules) with the groups of stage 1 proper and a wider scan.
Reads every studies/*/**.py (root given as argv[1], default ~/k-research/studies) with the AST; no study code runs.

  G1  class Q5 / class Q holding a + b*sqrt5 (Fractions a, b)                                     [pilot]
  G2  class QF holding a + b*sqrt(d)                                                              [pilot]
  G3  Q(sqrt5) as Fraction pairs with module-level functions (q, qa, qm, qinv, sgn, ...)          [pilot]
  G4  class K: the pilot's "four-term fields" list (K of cubes_lib.py and its namesakes), each classified by its product
  G5  the golden basis a + b*phi as a class (product with s.a*o.a + s.b*o.b, no factor d)
  G6  Z[phi] as integer pairs (zadd, zsub, zmul, zneg, zsign, zfloat, zconj; zsurf.py)
  G7  cubic and general number fields Q(t) (classes KC, AlgField, RF; exactlib.py)
  G8  other Q(sqrt d) classes found by the product pattern s.a*o.a + d*s.b*o.b (wider scan), not in G1, G2, G4
  W   wider scan: (a) pair arithmetic with a factor other than 5; (b) the code-map names conj2, conj5, sqrtQ, qsqrt,
      exact_volume, faces_exact; (c) inline norm / sign formulas x*x - d*y*y outside the copies above; (d) other classes with a
      product (__mul__) that are not number fields; (e) scripts using sympy for exact numbers; (f) vectorised (numpy) copies.
      Each item gets a verdict: a real number-field copy, a number-field operation, or not a copy (and why).
Writes data/inventory.json and prints a table. Ends with FINAL ok / FINAL FAIL."""
import ast, os, sys, json, hashlib, re, collections, warnings
warnings.simplefilter('ignore')

ROOT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/k-research/studies')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'data', 'inventory.json')
SKIP = {'__pycache__', '2026-11-18-shape-kernel-pilot', '2026-11-18-shape-kernel-stage1', '_src'}
PAIR_RX = re.compile(r'5 ?\* ?[a-z]\[1\] ?\* ?[a-z]\[1\]')
PAIR_RX_ANY = re.compile(r'\b([0-9]+|[A-Z]\w*) ?\* ?([a-z]\w*)\[1\] ?\* ?([a-z]\w*)\[1\]')
PAIR_NAMES = {'q', 'qs_', 'qa', 'qs', 'qm', 'qn', 'qr', 'qinv', 'qd', 'qf', 'sgn', 'qsgn', 'qsign', 'qmul', 'qadd', 'qsub', 'qneg',
              'qdiv', 'qstr', 'qsum', 'qlt', 'qeq', 'qfloat', 'qcmp', 'cmp', 'sign', 'qz', 'qiszero', 'qconj', 'qnorm'}
Z_NAMES = {'zadd', 'zsub', 'zmul', 'zneg', 'zsign', 'zfloat', 'zconj'}
GOLD_RX = re.compile(r's\.a ?\* ?o\.a ?\+ ?s\.b ?\* ?o\.b\b(?! ?\*)')
QD_RX = re.compile(r'\.a ?\* ?o\.a ?\+ ?\(?([A-Za-z_][\w.]*|\d+) ?\* ?s\.b ?\* ?o\.b')
NORM_RX = re.compile(r'\b(\w+(?:\.\w+|\[\d\])?) ?\* ?\1 ?(-|<|>|<=|>=|==) ?(\d+|[A-Z]\w*) ?\* ?(\w+(?:\.\w+|\[\d\])?) ?\* ?\4\b')
CODEMAP = {'conj2': 'number-field operation (Galois conjugate)', 'conj5': 'number-field operation (Galois conjugate)',
           'sqrtQ': 'number-field operation (square root in Q(sqrt5), found by a float search over small denominators)',
           'qsqrt': 'number-field operation (square root in Q(sqrt d), found by sympy sqrtdenest)',
           'exact_volume': 'not a copy: geometry (a volume) computed with a number class',
           'faces_exact': 'not a copy: geometry (hull faces checked exactly) computed with a number class'}


def src_hash(src, node):
    seg = ast.get_source_segment(src, node) or ''
    seg = re.sub(r'#.*', '', seg); seg = re.sub(r'\s+', '', seg)
    seg = re.sub(r'(\"\"\"|\'\'\').*?(\"\"\"|\'\'\')', '', seg, flags=re.S)
    return hashlib.md5(seg.encode()).hexdigest()[:8]


def mul_text(src, cls):
    for n in cls.body:
        if isinstance(n, ast.FunctionDef) and n.name == '__mul__': return ast.get_source_segment(src, n) or ''
    return ''


def k_kind(src, node, mt):
    if 'fmpq' in (ast.get_source_segment(src, node) or ''): return 'Q(sqrt D), D per run (2 or 5), python-flint rationals', 'quad-flint'
    if re.search(r'10 ?\* ?d ?\* ?h|5 ?\* ?c ?\* ?g', mt): return 'four-term field Q(sqrt2, sqrt5) = a + b sqrt2 + c sqrt5 + d sqrt10', 'mq'
    if 'K.k' in mt or 'K.n' in mt: return 'pure radical field Q(k^(1/n)), basis 1, r, ..., r^(n-1), class-level n, k', 'radical'
    if re.search(r'5 ?\* ?s\.b ?\* ?o\.b', mt): return 'Q(sqrt5) = a + b sqrt5 (two terms; named K)', 'quad5'
    return 'unclassified', 'other'


rows = {g: [] for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8')}
W = {'vectorised': [], 'pairs_other_d': [], 'codemap_names': [], 'inline_norms': [], 'other_mul_classes': [], 'sympy_scripts': 0, 'sympy_examples': []}
nfiles = 0
for dp, dns, fns in os.walk(ROOT):
    dns[:] = sorted(d for d in dns if d not in SKIP)
    for fn in sorted(fns):
        if not fn.endswith('.py'): continue
        p = os.path.join(dp, fn); rel = os.path.relpath(p, ROOT); study = rel.split(os.sep)[0]
        src = open(p, encoding='utf-8', errors='ignore').read()
        try: tree = ast.parse(src)
        except SyntaxError: continue
        nfiles += 1
        has_copy = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef): continue
            meths = sorted(n.name for n in node.body if isinstance(n, ast.FunctionDef))
            mt = mul_text(src, node)
            base = dict(path=rel, study=study, cls=node.name, methods=meths, hash=src_hash(src, node), lines=node.end_lineno - node.lineno + 1,
                        lineno=node.lineno)
            if node.name in ('Q5', 'Q') and re.search(r'5 ?\*', mt):
                rows['G1'].append(base); has_copy = True
            elif node.name == 'QF':
                rows['G2'].append(dict(base, per_element_d=any('self.d' in (ast.get_source_segment(src, n) or '') or 's.d' in (ast.get_source_segment(src, n) or '')
                                                               for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')))
                has_copy = True
            elif node.name == 'K' and mt:
                kind, code = k_kind(src, node, mt)
                rows['G4'].append(dict(base, kind=kind, code=code)); has_copy = True
            elif node.name in ('KC', 'AlgField', 'RF'):
                rows['G7'].append(dict(base, kind={'KC': 'pure cubic field Q(k^(1/3)), sign by the norm',
                                                   'AlgField': 'the field Q(t): polynomial and isolating interval, sign by bisection',
                                                   'RF': 'element of Q(t) (uses AlgField)'}[node.name])); has_copy = True
            elif mt and '2 * d - 1' in mt and 'self.c' in mt:
                rows['G7'].append(dict(base, kind='general field Q(alpha), monic minimal polynomial (Q, sqrt5, sqrt2, sqrt6, cbrt2, cbrt6), '
                                                  'sign from an 80-digit evaluation')); has_copy = True
            elif mt and GOLD_RX.search(mt):
                rows['G5'].append(dict(base, kind='a + b phi (golden basis)' + (' or a + b sqrt2, chosen per element' if '2 * s.b' in mt else '')))
                has_copy = True
            elif mt and QD_RX.search(mt):
                d = QD_RX.search(mt).group(1)
                rows['G8'].append(dict(base, d=d, rational=('gmpy2 mpq' if 'mpq' in src else 'Fraction'))); has_copy = True
            elif mt:
                W['other_mul_classes'].append(dict(path=rel, cls=node.name))
        top = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        if PAIR_RX.search(src):
            fs = {}
            for n in tree.body:
                if isinstance(n, ast.FunctionDef) and n.name in PAIR_NAMES: fs[n.name] = src_hash(src, n)
                if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Lambda) and n.targets[0].id in PAIR_NAMES:
                    fs[n.targets[0].id] = src_hash(src, n)
                if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Tuple) and isinstance(n.value, ast.Tuple):
                    for t, v in zip(n.targets[0].elts, n.value.elts):
                        if isinstance(t, ast.Name) and isinstance(v, ast.Lambda) and t.id in PAIR_NAMES: fs[t.id] = src_hash(src, v)
            if fs:
                fh = hashlib.md5(json.dumps(sorted(fs.items())).encode()).hexdigest()[:8]
                rows['G3'].append(dict(path=rel, study=study, functions=sorted(fs), hash=fh)); has_copy = True
        zs = {k: src_hash(src, v) for k, v in top.items() if k in Z_NAMES}
        if 'zmul' in zs and 'zsign' in zs:
            rows['G6'].append(dict(path=rel, study=study, functions=sorted(zs), hash=hashlib.md5(json.dumps(sorted(zs.items())).encode()).hexdigest()[:8],
                                   lineno=min(top[k].lineno for k in zs))); has_copy = True
        # ---- wider scan
        if not has_copy:
            for m in PAIR_RX_ANY.finditer(src):
                if m.group(1) != '5':
                    W['pairs_other_d'].append(dict(path=rel, d=m.group(1), text=m.group(0))); break
        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef) and n.name in CODEMAP:
                W['codemap_names'].append(dict(path=rel, name=n.name, verdict=CODEMAP[n.name], in_copy=has_copy))
        if not has_copy:
            hits = [m.group(0) for m in NORM_RX.finditer(src) if m.group(3) in ('2', '3', '5', '6', '10', 'D', 'M') or m.group(3).isupper()]
            if hits: W['inline_norms'].append(dict(path=rel, count=len(hits), example=hits[0]))
        if re.search(r'2 ?\* ?x\[\.\.\., ?0\] ?\+ ?x\[\.\.\., ?1\]', src):
            W['vectorised'].append(dict(path=rel, verdict='a real Z[phi] copy, vectorised on numpy int64 arrays, written from scratch for an '
                                        'independent check: kept apart by design (an independent check must not share the kernel)'))
        if re.search(r'^\s*(import sympy|from sympy)', src, re.M):
            W['sympy_scripts'] += 1
            if len(W['sympy_examples']) < 5: W['sympy_examples'].append(rel)

NOT_FIELD = {'T': 'logging wrapper of a symbolic expression (records divisors)', 'I': 'interval arithmetic wrapper (mpmath iv)',
             'D': 'interval value with two derivatives (certified bounds)', 'E': 'expression tree, or polynomial in t over Q(sqrt D)',
             'KP': 'pair of multivariate polynomials over python-flint (A + B sqrt D with polynomial A, B)'}
for r in W['other_mul_classes']:
    r['verdict'] = 'not a copy: ' + NOT_FIELD.get(r['cls'], 'a product that is not a real number field (vectors, quaternions, matrices or wrappers)')
for r in W['pairs_other_d']:
    r['verdict'] = 'to check by eye: pair arithmetic with a factor other than 5'
for r in W['inline_norms']:
    r['verdict'] = 'inline norm or sign test a^2 against d b^2 in a script without its own number class'

names = {'G1': 'Q(sqrt5) as a class (Q5 / Q)', 'G2': 'Q(sqrt d) as a class (QF)', 'G3': 'Q(sqrt5) as Fraction pairs (q, qa, qm, qinv, sgn ...)',
         'G4': 'class K (the pilot\'s four-term field list), by product', 'G5': 'golden basis a + b phi as a class',
         'G6': 'Z[phi] as integer pairs (zadd, zmul, zsign ...)', 'G7': 'cubic and general fields Q(t) (KC, AlgField, RF)',
         'G8': 'other Q(sqrt d) classes (wider scan)'}
out = {'scanned_files': nfiles, 'groups': {}, 'wider_scan': W}
for g, rs in rows.items():
    variants = collections.Counter(r['hash'] for r in rs)
    api = collections.Counter(m for r in rs for m in r.get('methods', r.get('functions', [])))
    out['groups'][g] = dict(name=names[g], copies=len(rs), studies=len({r['study'] for r in rs}), variants=len(variants),
                            identical_sets={h: [r['path'] for r in rs if r['hash'] == h] for h, c in variants.items() if c > 1},
                            api=dict(api.most_common()), rows=rs)
    print(f"{g} {names[g]}: {len(rs)} copies in {len({r['study'] for r in rs})} studies, {len(variants)} distinct sources")
    if g in ('G4', 'G5', 'G7', 'G8'):
        for r in rs: print(f"     {r['path']} class {r['cls']}: {r.get('kind') or ('d = ' + r['d'] + ', ' + r['rational'])}")
    if g == 'G6':
        for r in rs: print(f"     {r['path']}: {', '.join(r['functions'])}")
print(f"W (a) pair arithmetic with another factor, outside the copies: {len(W['pairs_other_d'])} files")
for r in W['pairs_other_d']: print(f"     {r['path']}: {r['text']}")
print(f"W (b) code-map names: {len(W['codemap_names'])}")
for r in W['codemap_names']: print(f"     {r['name']:13s} {r['path']}: {r['verdict']}{' (inside a listed copy)' if r['in_copy'] else ''}")
print(f"W (c) inline norm / sign formulas outside the copies: {len(W['inline_norms'])} files, {sum(r['count'] for r in W['inline_norms'])} formulas")
for r in W['inline_norms']: print(f"     {r['path']}: {r['count']} e.g. {r['example']}")
print(f"W (d) other classes with a product: {len(W['other_mul_classes'])}")
for r in W['other_mul_classes']: print(f"     {r['path']} class {r['cls']}: {r['verdict']}")
print(f"W (f) vectorised copies: {len(W['vectorised'])}")
for r in W['vectorised']: print(f"     {r['path']}: {r['verdict']}")
print(f"W (e) scripts importing sympy (library use, not a copy): {W['sympy_scripts']}")
json.dump(out, open(OUT, 'w'), indent=1)
need = {'G1': 32, 'G2': 14, 'G3': 10, 'G4': 6, 'G5': 1, 'G6': 2, 'G7': 6}   # the pilot's counts and the copies the task names
short = [g for g, m in need.items() if out['groups'][g]['copies'] < m]
print(f'FINAL ok: inventory of {nfiles} files written to data/inventory.json' if not short
      else f'FINAL FAIL: fewer copies than the pilot found or the task lists, in {short}')
