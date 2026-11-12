# exact_key.py, 12 Nov 2026 (aim 3; DICTO "go ahead with exact keying"). For one marking scheme: refine the types round by round
# (refine_snip.py, targeted: only the faces of fit-classes that hold an extra fit record their neighbour) until the bump-and-dent
# keying admits EXACTLY the allowed face pairs (fit = allowed). Then test the exactly keyed set: registration_check.py (lattice, hand),
# contact_test.py (chair contacts vs Kamenetsky's P*), integrity_test.py (whole chairs, R = 2 then 3), all with the refined types.
# usage: exact_key.py <scheme> <max rounds> <out dir>     (PY = interpreter, default: this one)
# Prints: per round types / allowed / extra; final verdict lines; 'EXACT <scheme> types T classes C' when fit = allowed.
import sys, os, json, subprocess
SCH, MAXR, OUT = sys.argv[1], int(sys.argv[2]), os.path.abspath(sys.argv[3]); os.makedirs(OUT, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__)); PY = os.environ.get('PY', sys.executable)
# 12 Nov: a scheme moved to another job leaves data/exact/SKIP-<scheme>; the old job's copy then stops at once (no double run)
if os.path.exists(os.path.join(here, '..', 'data', 'exact', f'SKIP-{SCH}')) and os.path.abspath(OUT) == os.path.abspath(os.path.join(here, '..', 'data', 'exact', 'work')):
    print(f'SKIPPED {SCH}: moved to another job'); print('DONE'); sys.exit(0)
def run(script, args, env_extra):
    env = dict(os.environ, **env_extra)
    r = subprocess.run([PY, '-W', 'ignore', '-u', os.path.join(here, script)] + args, env=env, capture_output=True, text=True)
    return r.stdout + r.stderr
spec = []; exact = False
for k in range(MAXR + 1):
    sp = os.path.join(OUT, f'spec-{SCH}-r{k}.json'); json.dump(spec, open(sp, 'w'))
    kj = os.path.join(OUT, f'exact-{SCH}-r{k}.json')
    out = run('keyed_rd.py', ['4', SCH, '1', kj], {'REFINE_SPEC': sp})
    if 'FINAL ok' not in out: print(out[-2000:]); print(f'CONTROL FAIL {SCH} round {k}: keyed_rd did not end FINAL ok (an allowed pair does not fit)'); sys.exit(1)
    D = json.load(open(kj))
    print(f'{SCH} round {k}: {D["types"]} types, {D["allowed"]} allowed, {D["fit"]} fit, extra {D["bad_fit"]}, classes {D["classes"]}', flush=True)
    print(f'PROGRESS {(k + 1) / (MAXR + 1):.2f} rounds', flush=True)
    if D['bad_fit'] == 0: exact = True; break
    spec.append(D['next_round'])
if not exact: print(f'NOT EXACT {SCH} after {MAXR} rounds'); print('DONE'); sys.exit(0)
print(f'EXACT {SCH} types {D["types"]} classes {D["classes"]} rounds {k}', flush=True)
# COMPLETENESS control: the refined types and their face pairs must be the same from the level-4 and the level-5 patch
k5 = os.path.join(OUT, f'exact-{SCH}-L5.json'); o5 = run('keyed_rd.py', ['5', SCH, '1', k5], {'REFINE_SPEC': sp})
if 'FINAL' not in o5: print(o5[-1500:])
D5 = json.load(open(k5)) if os.path.exists(k5) else None
def keyrel(DD): K = DD['type_keys']; return {(K[a], tuple(e), K[b], q) for a, e, b, q in DD['fit_relation']}
same = D5 is not None and set(D['type_keys']) == set(D5['type_keys']) and keyrel(D) == keyrel(D5) and D5['bad_fit'] == 0
print(f'COMPLETE {SCH}: level 4 {D["types"]} types {D["fit"]} pairs; level 5 {D5["types"] if D5 else "?"} types {D5["fit"] if D5 else "?"} pairs, extra {D5["bad_fit"] if D5 else "?"} -> {"SAME" if same else "DIFFERENT"}', flush=True)
env = {'REFINE_SPEC': sp}
for line in run('registration_check.py', [kj], {}).splitlines():
    if not line.startswith('PROGRESS'): print('REG ' + line, flush=True)
env['RULES'] = kj
# 12 Nov (coordinator: use idle cores): if data/exact/PARTESTS exists, hand contact + R2 + R3 to the parallel-tests job (par_tests.sh),
# wait for it without using CPU, then print its output in the usual form
W = os.path.abspath(os.path.join(here, '..', 'data', 'exact', 'work'))
if os.path.exists(os.path.join(here, '..', 'data', 'exact', 'PARTESTS')) and os.path.abspath(OUT) == W:
    import time
    json.dump(dict(sch=SCH, kj=kj, sp=sp), open(os.path.join(W, f'DEFER-{SCH}.json'), 'w'))
    t0 = time.time(); done = os.path.join(W, f'TESTS-DONE-{SCH}')
    while not os.path.exists(done):
        if time.time() - t0 > 5 * 3600: print(f'CONTROL FAIL {SCH}: parallel tests never came back'); print('DONE'); sys.exit(0)
        time.sleep(20)
    T = os.path.join(here, '..', 'data', 'exact', 'tests')
    for line in open(os.path.join(T, f'{SCH}.contact')).read().splitlines():
        if any(w in line for w in ('allowed by', 'survive', 'VERDICT', 'control', 'Error', 'Traceback')): print('CONTACT ' + line, flush=True)
    for R in (2, 3):
        for line in open(os.path.join(T, f'{SCH}.R{R}')).read().splitlines():
            if any(w in line for w in ('(G)', 'control', '(C)', 'VERDICT', 'types', 'Error', 'Traceback')): print(f'R{R} ' + line, flush=True)
    print('DONE', flush=True); sys.exit(0)
for line in run('contact_test.py', ['4', SCH, 'encl'], env).splitlines():
    if any(w in line for w in ('allowed by', 'survive', 'VERDICT', 'control', 'Error', 'Traceback')): print('CONTACT ' + line, flush=True)
for R in (2, 3):
    o = run('integrity_test.py', ['4', SCH, str(R)], env)
    for line in o.splitlines():
        if any(w in line for w in ('(G)', 'control', '(C)', 'VERDICT', 'types', 'Error', 'Traceback')): print(f'R{R} ' + line, flush=True)
    if 'WHOLE CHAIRS FORCED' in o: break
print('DONE', flush=True)
