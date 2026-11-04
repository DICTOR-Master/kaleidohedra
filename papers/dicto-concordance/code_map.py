#!/usr/bin/env python3
"""Code-sharing map for The DICTO Concordance (DICTO 4 Nov 2026: "a code sharing map for concordance might be an idea").
Scans studies/*/(scripts/)*.py with the AST: functions defined, modules imported (incl. studies/_lib). Groups same-named functions defined in
more than one study (duplicated methods = candidates for studies/_lib) and tags known methods by name patterns. Writes code_map.json."""
import ast, os, re, json, collections
ROOT = os.path.expanduser('~/k-research/studies')
METHODS = {
    'harmonic fingerprint (Q_l, W_l)': r'^(Q|Q2|fp|fingerprint|W6)$',
    'forced-sector search (normal / reversed pieces)': r'^(search|candidates|cands|sector_candidates|refl|refl_perp|reflect_bisector)$',
    'separating-axis overlap test': r'^(overlap|axes|axes_edges|hull_info)$',
    'polar sweep sections S(mu) = P ∩ mu P*': r'^(S|sweep|co|cord|section|sections)$',
    'permutations / symmetric point sets': r'^(perms|even_perms|cyc|ico)$',
    'exact checks (PASS/FAIL ledger)': r'^(check)$',
    'rotations about an axis': r'^(rot|turn|rotate)$',
}
defs = collections.defaultdict(set); uses = collections.defaultdict(set); imports = collections.defaultdict(set); files = 0
for dirpath, _, fns in os.walk(ROOT):
    for fn in fns:
        if not fn.endswith('.py'): continue
        p = os.path.join(dirpath, fn); rel = os.path.relpath(p, ROOT); study = rel.split(os.sep)[0]
        try: tree = ast.parse(open(p, encoding='utf-8', errors='ignore').read())
        except SyntaxError: continue
        files += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef): defs[node.name].add(rel)
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                mod = node.module if isinstance(node, ast.ImportFrom) else ','.join(a.name for a in node.names)
                if mod: imports[rel].add(mod)
methods = {}
for m, pat in METHODS.items():
    rx = re.compile(pat); hits = sorted({f for name, fs in defs.items() if rx.match(name) for f in fs})
    methods[m] = {'scripts': hits, 'studies': sorted({h.split(os.sep)[0] for h in hits})}
dups = {name: sorted(fs) for name, fs in defs.items() if len({f.split(os.sep)[0] for f in fs}) >= 3 and not name.startswith('_')}
lib_users = sorted(f for f, ms in imports.items() if any('_lib' in x or x.startswith('lib') for x in ms))
out = {'scanned_files': files, 'methods': methods, 'duplicated_functions_3plus_studies': dict(sorted(dups.items(), key=lambda kv: -len(kv[1]))), 'scripts_using_studies_lib': lib_users}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'code_map.json'), 'w'), indent=1)
print('scanned', files, 'scripts')
for m, v in methods.items(): print(f'{m}: {len(v["scripts"])} scripts in {len(v["studies"])} studies')
print('functions defined in 3+ studies:', len(dups), '| top:', [(k, len(v)) for k, v in list(out['duplicated_functions_3plus_studies'].items())[:12]])
print('scripts importing studies/_lib:', len(lib_users))
