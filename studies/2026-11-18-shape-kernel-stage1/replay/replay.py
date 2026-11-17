#!/usr/bin/env python3
"""Replay (shape kernel, stage 1 proper, 2026-11-18): run each case of cases.py twice on the same machine, in its orig tree (the study as
stored) and in its kern tree (the same files except the number code, which comes from the kernel), and compare:
  stdout     kern with orig, and kern with the study's stored log
  files      every file the run writes, kern with orig, and kern with the stored file it overwrote (the trees start as copies)
Masked before comparing: elapsed times ('<n> s', '<n>s', JSON keys seconds/secs/elapsed/time/t) and the path of the tree itself.
A case counts if the original finishes within the time limit (280 s, the 5-minute rule) with exit 0 on this machine; it passes if the
kernel run then gives the same stdout and the same files byte for byte (after masking).
usage: replay.py <python> <case name substring> [workers]   writes data/replay/<case>.json, <case>-orig.log, <case>-kern.log
       replay.py --summary                                  table of all cases, data/replay.json, FINAL ok / FINAL FAIL"""
import os, sys, re, json, subprocess, time, hashlib, concurrent.futures as cf
R = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(R); sys.path.insert(0, R)
from cases import CASES
OUT = os.path.join(BASE, 'data', 'replay'); os.makedirs(OUT, exist_ok=True)
LIMIT = 280
TIME = re.compile(r'\b\d+(\.\d+)? ?s\b')
JTIME = re.compile(r'"(seconds|secs|elapsed|time|runtime|wall|t|time_s)": ?-?[0-9.eE+-]+')
STUD = re.compile(r'/home/[^/\s"\']+/(?:k-research|work)/studies')


def mask(t, tree):
    if tree: t = t.replace(tree, '<studies>')
    t = STUD.sub('<studies>', t)
    return JTIME.sub(lambda m: f'"{m.group(1)}": <t>', TIME.sub('<t>s', t))


def snapshot(st, studies):
    h = {}
    for s in studies:
        for dp, dns, fns in os.walk(os.path.join(st, s)):
            dns[:] = [d for d in dns if d != '__pycache__']
            for f in fns:
                p = os.path.join(dp, f)
                if os.path.islink(p): continue
                h[os.path.relpath(p, st)] = (os.stat(p).st_mtime_ns, hashlib.sha256(open(p, 'rb').read()).hexdigest())   # written = new mtime
    return h


def run(c, tree, py):
    st = os.path.join(R, 'cases', c['name'], tree, 'studies'); wd = os.path.join(st, c['study'], c['cwd'])
    env = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg', PYTHONPATH=BASE if tree == 'kern' else '')
    before = snapshot(st, c['copies']); t0 = time.time()
    try:
        p = subprocess.run([py, c['script']] + c['args'], cwd=wd, env=env, capture_output=True, text=True, timeout=LIMIT)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, so, se = 'timeout', (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''), ''
    secs = time.time() - t0
    after = snapshot(st, c['copies'])
    changed = sorted(k for k in after if before.get(k) != after[k])
    open(os.path.join(OUT, f"{c['name']}-{tree}.log"), 'w').write(so + (f'[exit {rc}]\n' if rc else '') + ('[stderr]\n' + se if se.strip() else ''))
    return dict(rc=rc, stdout=so, stderr=se[-2000:], secs=round(secs, 1), changed=changed, st=st)


def first_diff(a, b):
    la, lb = a.splitlines(), b.splitlines()
    for i, (x, y) in enumerate(zip(la, lb)):
        if x != y: return f'line {i + 1}: {x[:150]!r} vs {y[:150]!r}'
    return f'lengths {len(la)} vs {len(lb)} lines' if len(la) != len(lb) else 'none'


def rd(p):
    b = open(p, 'rb').read()
    try: return b.decode('utf-8'), True
    except UnicodeDecodeError: return b, False


def compare(c, o, k):
    r = dict(case=c['name'], group=c['group'], study=c['study'], script=c['script'], args=c['args'], rc_orig=o['rc'], rc_kern=k['rc'],
             secs_orig=o['secs'], secs_kern=k['secs'])
    if o['rc'] == 'timeout':
        r.update(status='over the time limit', ok=None); return r
    if o['rc'] != 0:
        r.update(status='original fails on this machine', ok=None, stderr_orig=o['stderr'][-600:]); return r
    mo, mk = mask(o['stdout'], o['st']), mask(k['stdout'], k['st'])
    r.update(stdout_lines=k['stdout'].count('\n'), stdout_kern_eq_orig=mo == mk, stdout_kern_eq_orig_raw=o['stdout'] == k['stdout'],
             time_fields_masked=len(TIME.findall(k['stdout'])), diff_kern_orig=first_diff(mk, mo))
    if c['log']:
        sp = os.path.join(R, 'cases', c['name'], 'orig', 'studies', c['study'], c['log'])
        stored = open(sp, encoding='utf-8', errors='replace').read() if os.path.exists(sp) else None
        if stored is not None:
            stored = re.sub(r'\n?\[exit 0\]\n?$', '\n', stored); ms = mask(stored, '')
            r.update(stdout_kern_eq_stored=mk == ms, stdout_orig_eq_stored=mo == ms, diff_kern_stored=first_diff(mk, ms))
    files = []
    if set(o['changed']) != set(k['changed']): r['changed_sets_differ'] = sorted(set(o['changed']) ^ set(k['changed']))
    for f in sorted(set(o['changed']) & set(k['changed'])):
        (to, txt), (tk, _) = rd(os.path.join(o['st'], f)), rd(os.path.join(k['st'], f))
        if txt: to, tk = mask(to, o['st']), mask(tk, k['st'])
        stored_p = os.path.join(SRC_ROOT, f) if SRC_ROOT else None
        ts = None
        if stored_p and os.path.exists(stored_p):
            ts, t2 = rd(stored_p)
            if t2 and txt: ts = mask(ts, '')
        if f == (c['log'] and os.path.join(c['study'], c['log'])): continue
        files.append(dict(file=f, kern_eq_orig=to == tk, kern_eq_stored=None if ts is None else tk == ts, bytes=len(tk)))
    r['files'] = files
    ok = k['rc'] == 0 and r['stdout_kern_eq_orig'] and all(f['kern_eq_orig'] for f in files) and 'changed_sets_differ' not in r
    r.update(status='replayed', ok=ok); return r


SRC_ROOT = None
if sys.argv[1] == '--summary':
    rows = [json.load(open(os.path.join(OUT, f))) for f in sorted(os.listdir(OUT)) if f.endswith('.json')]
    names = {c['name'] for c in CASES}; got = {r['case'] for r in rows}
    missing = sorted(names - got)
    print(f"{'case':44s} {'group':6s} {'status':32s} {'s orig/kern':>13s} stdout k=o k=stored | files k=o k=stored")
    for r in sorted(rows, key=lambda r: [c['name'] for c in CASES].index(r['case']) if r['case'] in names else 999):
        fs = r.get('files', [])
        print(f"{r['case']:44s} {r['group']:6s} {('ok ' if r['ok'] else ('FAIL ' if r['ok'] is False else '-- ')) + r['status']:32s} "
              f"{r['secs_orig']:>6}/{r['secs_kern']:<6} {str(r.get('stdout_kern_eq_orig', '')):5s} {str(r.get('stdout_kern_eq_stored', '')):5s} | "
              f"{sum(f['kern_eq_orig'] for f in fs)}/{len(fs)} {sum(1 for f in fs if f['kern_eq_stored'])}/{sum(1 for f in fs if f['kern_eq_stored'] is not None)}")
        if r['ok'] is False: print('      kern vs orig:', r.get('diff_kern_orig'), r.get('changed_sets_differ', ''), [f['file'] for f in fs if not f['kern_eq_orig']])
        if r['ok'] and r.get('stdout_kern_eq_stored') is False: print('      stored log differs (orig too: %s): %s' % (not r.get('stdout_orig_eq_stored'), r.get('diff_kern_stored')))
        if r['status'] == 'original fails on this machine': print('      ', (r.get('stderr_orig') or '').strip().splitlines()[-1:] )
    json.dump(rows, open(os.path.join(BASE, 'data', 'replay.json'), 'w'), indent=1)
    ran = [r for r in rows if r['ok'] is not None]; fails = [r for r in ran if not r['ok']]
    print(f"cases {len(names)}: replayed {len(ran)}, kern = orig {len(ran) - len(fails)}, not counted {len(rows) - len(ran)} "
          f"(over the limit {sum(r['status'] == 'over the time limit' for r in rows)}, original fails here {sum(r['status'] == 'original fails on this machine' for r in rows)}), not run {len(missing)}")
    print('FINAL ok: every replayed run gives byte-identical output with the kernel (times masked)' if ran and not fails and not missing
          else f'FINAL FAIL: {len(fails)} replays differ, {len(missing)} cases not run {missing[:5]}')
    sys.exit()
PY, SEL = sys.argv[1], sys.argv[2]; W = int(sys.argv[3]) if len(sys.argv) > 3 else 20
SRC_ROOT = os.path.abspath(sys.argv[4]) if len(sys.argv) > 4 else None
sel = [c for c in CASES if any(s in c['name'] for s in SEL.split(','))]
with cf.ThreadPoolExecutor(W) as ex:
    futs = {(c['name'], t): ex.submit(run, c, t, PY) for c in sel for t in ('orig', 'kern')}
    res = {k: f.result() for k, f in futs.items()}
for c in sel:
    r = compare(c, res[(c['name'], 'orig')], res[(c['name'], 'kern')])
    json.dump(r, open(os.path.join(OUT, c['name'] + '.json'), 'w'), indent=1)
    print(f"{'ok  ' if r['ok'] else ('FAIL' if r['ok'] is False else '--  ')} {c['name']}: {r['status']}, {r['secs_orig']} s / {r['secs_kern']} s"
          + (f", stdout kern=orig {r['stdout_kern_eq_orig']}, kern=stored {r.get('stdout_kern_eq_stored')}, files {sum(f['kern_eq_orig'] for f in r['files'])}/{len(r['files'])}" if r['ok'] is not None else ''))
bad = [c['name'] for c in sel if json.load(open(os.path.join(OUT, c['name'] + '.json')))['ok'] is False]
print(f'FINAL ok: {len(sel)} cases run, none differs' if not bad else f'FINAL FAIL: {bad}')
