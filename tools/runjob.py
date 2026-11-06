#!/usr/bin/env python3
"""Safe study runner (DICTO standing rule 7 Nov 2026: a failed run must never overwrite or reach a data file).
  python3 tools/runjob.py <script.py> <data-file> [args...] [--timeout SEC]
- runs the script with cwd = the script's own folder (relative paths always resolve),
- writes output to <data-file>.part with a heartbeat line every 60 s on stderr,
- replaces <data-file> ONLY if the run exits 0, has no Traceback and its last line starts 'FINAL ok';
  otherwise the old data file is left untouched and the output is kept as <data-file>.FAILED (git-ignored)."""
import os, subprocess, sys, time, threading
a = sys.argv[1:]; tmo = None
if '--timeout' in a: i = a.index('--timeout'); tmo = float(a[i + 1]); del a[i:i + 2]
script, out, rest = os.path.abspath(a[0]), os.path.abspath(a[1]), a[2:]
part, failed = out + '.part', out + '.FAILED'
t0 = time.time(); stop = threading.Event()
def beat():
    while not stop.wait(60): print(f'[runjob] {os.path.basename(script)} running {int(time.time() - t0)} s', file=sys.stderr, flush=True)
threading.Thread(target=beat, daemon=True).start()
status = 'FAIL'
with open(part, 'w') as f:
    try: rc = subprocess.run([sys.executable, script, *rest], cwd=os.path.dirname(script), stdout=f, stderr=subprocess.STDOUT, timeout=tmo).returncode
    except subprocess.TimeoutExpired: rc = None; status = 'TIMEOUT'
stop.set()
txt = open(part).read(); lines = [l for l in txt.splitlines() if l.strip()]
ok = rc == 0 and 'Traceback' not in txt and lines and lines[-1].startswith('FINAL ok')
if ok: os.replace(part, out); status = 'OK'
else:
    os.replace(part, failed)
    if rc is not None and rc != 0: status = f'FAIL (exit {rc})'
    elif rc == 0: status = 'FAIL (no "FINAL ok" last line)'
print(txt if ok else txt[-3000:], end='' if txt.endswith('\n') else '\n')
print(f'[runjob] {status} in {int(time.time() - t0)} s: ' + (out if ok else f'{failed} (old {os.path.basename(out)} kept)'), flush=True)
sys.exit(0 if ok else 1)
