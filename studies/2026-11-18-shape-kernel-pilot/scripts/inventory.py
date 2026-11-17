#!/usr/bin/env python3
"""Inventory of exact-number code copied across the studies (shape-kernel pilot, 2026-11-18).

Reads every studies/*/**.py (path given as argv[1], default ~/k-research/studies) with the AST and finds three groups:
  G1  class Q5 / class Q holding a + b*sqrt5 (Fractions a, b): the object form of Q(sqrt5)
  G2  class QF holding a + b*sqrt(d): one real quadratic field, d chosen per class or per element
  G3  Q(sqrt5) as Fraction pairs (a, b) with module-level functions (q, qa, qm, qinv, sgn, ...)
For each copy: path, study, methods / functions, a hash of the class or function source (to group identical copies).
Also counts the neighbours that are not in the three groups (K = Q(sqrt2, sqrt5), a + b*phi bases) for the README.
Writes data/inventory.json and prints a table. Ends with a FINAL line."""
import ast, os, sys, json, hashlib, re, collections, warnings
warnings.simplefilter('ignore')

ROOT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/k-research/studies')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'data', 'inventory.json')
PILOT = '2026-11-18-shape-kernel-pilot'
PAIR_RX = re.compile(r'5 ?\* ?[a-z]\[1\] ?\* ?[a-z]\[1\]')
PAIR_NAMES = {'q', 'qs_', 'qa', 'qs', 'qm', 'qn', 'qr', 'qinv', 'qd', 'qf', 'sgn', 'qsgn', 'qsign', 'qmul', 'qadd', 'qsub', 'qneg',
              'qdiv', 'qstr', 'qsum', 'qlt', 'qeq', 'qfloat', 'qcmp', 'cmp', 'sign', 'qz', 'qiszero', 'qconj', 'qnorm'}


def src_hash(src, node):
    seg = ast.get_source_segment(src, node) or ''
    seg = re.sub(r'#.*', '', seg); seg = re.sub(r'\s+', '', seg)
    seg = re.sub(r'(\"\"\"|\'\'\').*?(\"\"\"|\'\'\')', '', seg, flags=re.S)
    return hashlib.md5(seg.encode()).hexdigest()[:8]


def mul_text(src, cls):
    for n in cls.body:
        if isinstance(n, ast.FunctionDef) and n.name == '__mul__': return ast.get_source_segment(src, n) or ''
    return ''


rows = {'G1': [], 'G2': [], 'G3': []}; other = collections.defaultdict(list); nfiles = 0
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in ('__pycache__', PILOT)]
    for fn in sorted(fns):
        if not fn.endswith('.py'): continue
        p = os.path.join(dp, fn); rel = os.path.relpath(p, ROOT); study = rel.split(os.sep)[0]
        src = open(p, encoding='utf-8', errors='ignore').read()
        try: tree = ast.parse(src)
        except SyntaxError: continue
        nfiles += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                meths = sorted(n.name for n in node.body if isinstance(n, ast.FunctionDef))
                mt = mul_text(src, node)
                if node.name in ('Q5', 'Q') and re.search(r'5 ?\*', mt):
                    rows['G1'].append(dict(path=rel, study=study, cls=node.name, methods=meths, hash=src_hash(src, node), lines=node.end_lineno - node.lineno + 1))
                elif node.name == 'QF':
                    rows['G2'].append(dict(path=rel, study=study, cls=node.name, methods=meths, hash=src_hash(src, node), lines=node.end_lineno - node.lineno + 1,
                                           per_element_d=any('self.d' in (ast.get_source_segment(src, n) or '') or 's.d' in (ast.get_source_segment(src, n) or '') for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')))
                elif node.name == 'K':
                    other['K = Q(sqrt2, sqrt5) or similar four-term field'].append(rel)
                elif node.name == 'Q' and re.search(r'b ?\* ?o\.b\)', mt):
                    other['Q as a + b*phi (golden basis)'].append(rel)
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
                rows['G3'].append(dict(path=rel, study=study, functions=sorted(fs), hash=fh))

out = {'scanned_files': nfiles, 'groups': {}, 'neighbours': {k: sorted(v) for k, v in other.items()}}
names = {'G1': 'Q(sqrt5) as a class (Q5 / Q)', 'G2': 'Q(sqrt d) as a class (QF)', 'G3': 'Q(sqrt5) as Fraction pairs (q, qa, qm, qinv, sgn ...)'}
for g, rs in rows.items():
    variants = collections.Counter(r['hash'] for r in rs)
    api = collections.Counter(m for r in rs for m in r.get('methods', r.get('functions', [])))
    out['groups'][g] = dict(name=names[g], copies=len(rs), studies=len({r['study'] for r in rs}), variants=len(variants),
                            identical_sets={h: [r['path'] for r in rs if r['hash'] == h] for h, c in variants.items() if c > 1},
                            api=dict(api.most_common()), rows=rs)
    print(f"{g} {names[g]}: {len(rs)} copies in {len({r['study'] for r in rs})} studies, {len(variants)} distinct sources")
    print('   API (count of copies providing it):', ', '.join(f'{k}:{v}' for k, v in api.most_common()))
for k, v in out['neighbours'].items(): print(f'neighbour, not in the pilot: {k}: {len(v)} copies')
json.dump(out, open(OUT, 'w'), indent=1)
ok = all(out['groups'][g]['copies'] >= 3 for g in rows)
print(f'FINAL ok: inventory of {nfiles} files written to data/inventory.json' if ok else 'FINAL FAIL: a group has fewer than 3 copies')
