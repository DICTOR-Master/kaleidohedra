"""Prior-art search for the Silent Running paper: full text of every PDF in the reference library (pdftotext), case-insensitive.
Prints, per query, every file with hits, the hit count and the first snippet. usage: python3 lib_search.py LIBRARY_DIR"""
import os, re, subprocess, sys
lib = sys.argv[1]
Q = ['twisted conjugacy', 'twisted class', 'twisted character', 'spherical design', 'harmonic index', 'Delsarte', 'Goethals', '600-cell', 'binary icosahedral', 'icosian', 'spin character', 'spin representation', 'Schur', 'double cover', 'Brauer', 'defect zero', 'McKay', 'Molien', 'Koca', 'Bannai', 'Galois conjugat', 'outer automorphism', 'systematic absence', 'extinction', 'nonsymmorphic', 'Wyckoff', 'special position', 'Chebyshev', 'Gegenbauer', 'cubature', 'truncated 5-cell', 'cantellated', 'Schlegel']
files = []
for root, _, fs in os.walk(lib):
    if '/.git' in root: continue
    files += [os.path.join(root, f) for f in fs if f.lower().endswith('.pdf')]
files.sort(); texts = {}
for i, f in enumerate(files):
    try: t = subprocess.run(['pdftotext', '-q', f, '-'], capture_output=True, timeout=120).stdout.decode('utf8', 'replace')
    except Exception as e: t = ''
    texts[f] = re.sub(r'\s+', ' ', t)
    if i % 20 == 0: print(f'PROGRESS {i/len(files):.2f} text layers', flush=True)
withtext = sum(1 for t in texts.values() if len(t) > 500)
print(f'files {len(files)}, with a text layer {withtext}')
for q in Q:
    print(f'\n### {q}')
    pat = re.compile(re.escape(q), re.I); n = 0
    for f, t in texts.items():
        hits = [m.start() for m in pat.finditer(t)]
        if hits:
            n += 1; s = hits[0]
            print(f'  {os.path.relpath(f, lib)} | {len(hits)} | ...{t[max(0, s-120):s+160]}...')
    print(f'  ({n} files)')
print('PROGRESS 1.00 done'); print('FINAL ok' if withtext > 200 else 'FINAL FAIL (too few text layers)')
