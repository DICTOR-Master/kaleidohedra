"""Driver for bij.c (study 2026-11-15-polygon-bijection).  Exact integers only.

Usage:
  bij.py words L W [chunk nchunks]   every c/h word on bilayers kr-W..kr+W around the root (letters outside: c), both atoms,
                                      every flip bilayer kf in kr-W..kr+W, correct surgery (mode 0); one line per run
  bij.py named L                      3C and 2H, both atoms, flips at kr-5..kr+5, mode 0, plus the rigid counts per flip
  bij.py negative L                   wrong twists (modes 1, 2, 3) on 3C/2H and two random words: each must break
  bij.py dump L WORD U KF [DMIN]      print the rigid-at-KF polygons (length >= DMIN, default L-2) of G and of G2 (for the local count)
Each run line ends 'END ok' or 'END FAIL'; the last line of every mode is 'ALLCHECKS ok' or 'ALLCHECKS FAIL'.
"""
import sys, os, subprocess, itertools, random, time
HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.join(HERE, 'bij')
out = lambda *a: print(*a, flush=True)

def letters(word):
    """letters s[0..K-1] for a c/h word given for bilayers 1..K-2 (word[k-1] = letter of bilayer k); bilayer k is h iff s[k-1] = s[k+1]."""
    s = [0, 1]
    for x in word:
        k = len(s) - 1
        d = (s[k] - s[k - 1]) % 3
        s.append((s[k] + d) % 3 if x == 'c' else s[k - 1])
    return s

def ch(s):
    return ''.join('h' if s[k - 1] == s[k + 1] else 'c' for k in range(1, len(s) - 1))

def run(L, word, kr, u, kf, mode=0, dump=0, dumpmin=0):
    s = letters(word); K = len(s)
    inp = f'{L} {K} {kr} {u} {kf} {mode} {dump} {dumpmin}\n' + ' '.join(map(str, s)) + '\n'
    p = subprocess.run([CORE], input=inp, capture_output=True, text=True)
    if p.returncode != 0: raise RuntimeError(f'bij failed ({p.returncode}): {p.stderr[-300:]}')
    return p.stdout

def parse(txt):
    res = {}
    for line in txt.splitlines():
        f = line.split()
        if f[0] == 'LEN':
            d = dict(zip(f[2::2], map(int, f[3::2]))); res[int(f[1])] = d
    end = [l for l in txt.splitlines() if l.startswith('END')][-1]
    mr = [l for l in txt.splitlines() if l.startswith('MINRIGID')][-1].split()
    return res, end.endswith('ok'), int(mr[2]), int(mr[4])

def window(L):
    """bilayers needed: a polygon of length L through an atom of bilayer kr stays in kr - L//4 - 1 .. kr + L//4 + 1 (Lemma 4 of #102)."""
    h = L // 4 + 2
    return h

if __name__ == '__main__':
    mode = sys.argv[1]; L = int(sys.argv[2]); T0 = time.time(); allok = True
    h = window(L)
    if mode == 'words':
        Wd = int(sys.argv[3]); chunk, nch = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
        words = [''.join(w) for w in itertools.product('ch', repeat=2 * Wd + 1)]
        jobs = [(w, u, kf) for w in words for u in (0, 1) for kf in range(-Wd, Wd + 1)]
        jobs = jobs[chunk::nch]
        for n, (w, u, kf) in enumerate(jobs):
            # bilayers 1..K-2; root bilayer kr = h + 1; word w occupies kr-Wd..kr+Wd, 'c' elsewhere
            pad = h + 1 - Wd
            full = 'c' * (pad - 1) + w + 'c' * (pad - 1)
            kr = 1 + (pad - 1) + Wd
            res, ok, mr, mr2 = parse(run(L, full, kr, u, kr + kf))
            allok &= ok
            out('RUN', w, u, kf, ' '.join(f'{l}:{res[l]["symG"]}/{res[l]["rigG"]}/{res[l]["rig2"]}' for l in sorted(res) if l >= 12), 'minrigid', mr, mr2, 'END', 'ok' if ok else 'FAIL')
            if n % 20 == 0: out(f'PROGRESS {round(n / len(jobs), 3)} runs {n}/{len(jobs)} ({time.time() - T0:.0f} s)')
    elif mode == 'named':
        for name, sym in (('3C', 'c'), ('2H', 'h')):
            kr = h + 2
            full = sym * (2 * h + 3)
            for u in (0, 1):
                for kf in range(-(L // 4 + 1), L // 4 + 2):
                    res, ok, mr, mr2 = parse(run(L, full, kr, u, kr + kf)); allok &= ok
                    for l in sorted(res):
                        d = res[l]
                        out('NAMED', name, 'u', u, 'flip', kf, 'l', l, 'tot', d['totG'], 'sym', d['symG'], 'rigG', d['rigG'], 'rig2', d['rig2'], 'tot2', d['tot2'],
                            'badimg', d['badimg'], 'dup', d['dupimg'], 'profbad', d['profbad'], 'setequal', d['setequal'])
                    out('NAMEDEND', name, u, kf, 'minrigid', mr, mr2, 'ok' if ok else 'FAIL')
                out(f'PROGRESS {0.5 if name == "3C" and u else (1 if name == "2H" and u else 0.25)} {name} u{u} ({time.time() - T0:.0f} s)')
    elif mode == 'negative':
        random.seed(20261115)
        cases = [('c' * (2 * h + 3), 'c'), ('h' * (2 * h + 3), 'h')] + [(''.join(random.choice('ch') for _ in range(2 * h + 3)), 'r') for _ in range(2)]
        for full, tag in cases:
            kr = h + 2
            for m in (0, 1, 2, 3):
                for kf in (0, 1, -1):
                    txt = run(L, full, kr, 0, kr + kf, mode=m)
                    res, ok, _, _ = parse(txt)
                    bad = sum(res[l]['badimg'] for l in res)
                    good = ok
                    allok &= good
                    out('NEG', ch(letters(full))[kr - 3:kr + 2], 'mode', m, 'flip', kf, 'invalid images', bad,
                        'expected', 'valid bijection' if m == 0 else 'break', '->', 'ok' if good else 'FAIL')
    elif mode == 'dump':
        word, u, kf = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
        kr = h + 2
        full = (word * (2 * h + 3))[:2 * h + 3] if len(word) < 2 * h + 3 else word
        dmin = int(sys.argv[6]) if len(sys.argv) > 6 else L - 2
        sys.stdout.write(run(L, full, kr, u, kr + kf, dump=1, dumpmin=dmin))
        sys.exit(0)
    out('ALLCHECKS', 'ok' if allok else 'FAIL', f'({time.time() - T0:.0f} s)')
