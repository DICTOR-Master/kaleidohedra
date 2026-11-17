#!/usr/bin/env python3
"""Replay test (shape-kernel pilot, 2026-11-18): run three small study scripts twice, as they are (orig/) and with their exact-number
module replaced by the kernel shim (kern/), and compare byte for byte: kern vs orig (same machine, same libraries) and both vs the
outputs stored in the studies. Only elapsed-time fields are masked ('<n> s' -> '<t> s'); every other byte must agree.
usage: replay.py <python>   (run setup.sh first). Writes data/replay.json and data/replay-<case>-<orig|kern>.log."""
import os, sys, re, json, subprocess, time, hashlib
R = os.path.dirname(os.path.abspath(__file__)); PILOT = os.path.dirname(R); C = os.path.join(R, 'cases')
PY = sys.argv[1] if len(sys.argv) > 1 else sys.executable
TIME = re.compile(r'\b\d+(\.\d+)? s\b')
mask = lambda t: TIME.sub('<t> s', t)

CASES = [
    # (case, script, args, cwd relative to tree, stored stdout to compare, [(produced file, stored file)])
    ('paradigm-exact', 'scripts/hemi_exact.py', ['input/dicto-build-worldpoly.json'], '.', 'hemi-exact.log', []),
    ('paradigm-exact', 'scripts/scutoid_exact.py', ['all'], '.', 'scutoid-exact.log', []),
    ('fans-law', 'scripts/fans_law.py', ['input/registry-solids.json', 'input/disc-ranking.json', 'data/fans-law.json'], '.', 'fans-law.log',
     [('data/fans-law.json', 'fans-law.json')]),
    ('ocd-octet', 'scripts/step12_exact_faces.py', [], 'scripts', 'step12.log', [('data/step12-faces.json', 'step12-faces.json')]),
]


def run(case, tree, script, args, cwd):
    root = os.path.join(C, case, tree); env = dict(os.environ, PYTHONHASHSEED='0')
    env['PYTHONPATH'] = PILOT if tree == 'kern' else ''
    wd = os.path.join(root, cwd)
    sp = os.path.relpath(os.path.join(root, script), wd); aa = [os.path.relpath(os.path.join(root, a), wd) if '/' in a else a for a in args]
    t0 = time.time()
    p = subprocess.run([PY, sp] + aa, cwd=wd, env=env, capture_output=True, text=True, timeout=280)
    out = p.stdout + (f'[exit {p.returncode}]\n' if p.returncode else '')
    if p.stderr.strip(): out += '[stderr]\n' + p.stderr
    open(os.path.join(PILOT, 'data', f'replay-{case}-{os.path.basename(script)[:-3]}-{tree}.log'), 'w').write(out)
    return p.returncode, p.stdout, time.time() - t0


def first_diff(a, b):
    la, lb = a.splitlines(), b.splitlines()
    for i, (x, y) in enumerate(zip(la, lb)):
        if x != y: return f'line {i + 1}: {x[:160]!r} vs {y[:160]!r}'
    return f'lengths {len(la)} vs {len(lb)} lines' if len(la) != len(lb) else 'none'


rows = []; allok = True
for case, script, args, cwd, stored_log, files in CASES:
    r = {'case': case, 'script': script}
    rc_o, out_o, t_o = run(case, 'orig', script, args, cwd)
    rc_k, out_k, t_k = run(case, 'kern', script, args, cwd)
    stored = open(os.path.join(C, case, 'stored', stored_log)).read()
    # stored logs written by '> log' may end with an '[exit 0]' line added by the job runner; compare the script's own output
    stored_core = re.sub(r'\n?\[exit 0\]\n?$', '\n', stored)
    r.update(rc_orig=rc_o, rc_kern=rc_k, secs_orig=round(t_o, 1), secs_kern=round(t_k, 1),
             stdout_kern_eq_orig_raw=out_k == out_o, stdout_kern_eq_orig=mask(out_k) == mask(out_o),
             stdout_kern_eq_stored=mask(out_k) == mask(stored_core), stdout_orig_eq_stored=mask(out_o) == mask(stored_core),
             masked_time_fields=len(TIME.findall(out_k)), stdout_lines=out_k.count('\n'),
             diff_kern_orig=first_diff(mask(out_k), mask(out_o)), diff_kern_stored=first_diff(mask(out_k), mask(stored_core)))
    fr = []
    for prod, sto in files:
        po, pk = os.path.join(C, case, 'orig', prod), os.path.join(C, case, 'kern', prod)
        so = os.path.join(C, case, 'stored', sto)
        h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16] if os.path.exists(p) else None
        fr.append(dict(file=prod, bytes=os.path.getsize(pk) if os.path.exists(pk) else None, sha_orig=h(po), sha_kern=h(pk), sha_stored=h(so),
                       kern_eq_orig=h(pk) == h(po) and h(pk) is not None, kern_eq_stored=h(pk) == h(so) and h(pk) is not None))
    r['files'] = fr
    ok = rc_k == 0 and r['stdout_kern_eq_orig'] and all(f['kern_eq_orig'] for f in fr)
    r['ok'] = ok; allok &= ok; rows.append(r)
    print(f"{'ok  ' if ok else 'FAIL'} {case}/{script}: exit {rc_o}/{rc_k}; stdout kern=orig {r['stdout_kern_eq_orig']} (raw {r['stdout_kern_eq_orig_raw']}),"
          f" kern=stored {r['stdout_kern_eq_stored']}, orig=stored {r['stdout_orig_eq_stored']}; {r['stdout_lines']} lines, {r['masked_time_fields']} time fields masked;"
          f" {t_o:.1f} s / {t_k:.1f} s")
    if not r['stdout_kern_eq_orig']: print('     first difference kern vs orig:', r['diff_kern_orig'])
    if not r['stdout_kern_eq_stored']: print('     first difference kern vs stored:', r['diff_kern_stored'])
    for f in fr: print(f"     {f['file']} ({f['bytes']} bytes): kern=orig {f['kern_eq_orig']}, kern=stored {f['kern_eq_stored']}")
json.dump(rows, open(os.path.join(PILOT, 'data', 'replay.json'), 'w'), indent=1)
print('FINAL ok: all replays byte-identical to the original scripts (time fields masked)' if allok else 'FINAL FAIL: a replay differs (see data/replay.json)')
