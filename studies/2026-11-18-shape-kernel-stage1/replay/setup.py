#!/usr/bin/env python3
"""Build the replay trees (shape kernel, stage 1 proper, 2026-11-18).  For each case in cases.py, two trees:
  cases/<case>/orig/studies   the case's studies copied unchanged; every other study linked read-only from the source
  cases/<case>/kern/studies   the same, except that the covered number code is replaced by the kernel shims (replay/shims/)
The study files in the source are only read.  Records every replaced line range in data/replay-swaps.json.  Ends with FINAL ok / FAIL.
usage: setup.py <studies source root> [case name substring]"""
import os, sys, shutil, json, subprocess
R = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(R); sys.path.insert(0, R)
from cases import CASES
SRC = os.path.abspath(sys.argv[1]); SEL = sys.argv[2] if len(sys.argv) > 2 else ''
IGN = shutil.ignore_patterns('__pycache__', '*.pyc')
swaps_log = {}; bad = []
studies = sorted(d for d in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, d)))
for c in CASES:
    if SEL not in c['name']: continue
    root = os.path.join(R, 'cases', c['name'])
    if os.path.exists(root): shutil.rmtree(root)
    for t in ('orig', 'kern'):
        st = os.path.join(root, t, 'studies'); os.makedirs(st)
        for s in studies:
            if s in c['copies']: shutil.copytree(os.path.join(SRC, s), os.path.join(st, s), ignore=IGN, symlinks=True)
            else: os.symlink(os.path.join(SRC, s), os.path.join(st, s))
    rec = []
    for sw in c['swaps']:
        mod, mode, shim = sw[0], sw[1], os.path.join(R, 'shims', sw[2])
        src, dst = os.path.join(SRC, mod), os.path.join(root, 'kern', 'studies', mod)
        if mod.split('/')[0] not in c['copies']: bad.append(f"{c['name']}: {mod} is not in a copied study"); continue
        if mode == 'whole':
            shutil.copyfile(shim, dst); rec.append(f'{mod}: whole file -> {sw[2]}')
        elif mode == 'head':
            text = open(src, encoding='utf-8').read(); i = text.index(sw[3])
            open(dst, 'w', encoding='utf-8').write(open(shim, encoding='utf-8').read() + text[i:])
            rec.append(f'{mod}: lines before {sw[3]!r} -> {sw[2]} (rest unchanged, {text[i:].count(chr(10))} lines)')
        else:
            p = subprocess.run([sys.executable, os.path.join(R, 'swap.py'), src, dst, shim] + sw[3], capture_output=True, text=True)
            if p.returncode: bad.append(p.stderr.strip() or p.stdout.strip())
            rec.append(p.stdout.strip())
    swaps_log[c['name']] = rec
    print(f"{c['name']}: {len(c['copies'])} studies copied; " + ' | '.join(rec))
old = {}
P = os.path.join(BASE, 'data', 'replay-swaps.json')
if os.path.exists(P): old = json.load(open(P))
old.update(swaps_log); json.dump(old, open(P, 'w'), indent=1)
print('FINAL ok: replay trees built' if not bad else 'FINAL FAIL: ' + '; '.join(bad))
