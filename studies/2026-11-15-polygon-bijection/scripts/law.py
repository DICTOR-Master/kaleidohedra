"""The local laws p_l (l <= 24) from the flip differences, and their check against direct enumeration
(study 2026-11-15-polygon-bijection, section 8).  Exact integers only.

Input: DELTA4 lines (halves24.py: four-crossing part of Delta for flip kf, every c/h pattern of bilayers kf-3..kf+3) and
DELTA6 / DELTA8 lines (six.py: six- and eight-crossing parts, every pattern of kf-1, kf+1).  Delta_kf = p(bilayer kf h) - p(kf c).
A polygon through the root crosses bilayer kf at most 8 times when l <= 24 (10 crossings need 10 + 5*2 + 5*2 = 30 bonds), so
Delta_kf = Delta4 + Delta6 + Delta8 exactly (two-crossing terms are 0 by Theorem A).

1. p(word) for every c/h word on bilayers -6..5 (outside: c) is built by telescoping from 3C, flipping the h letters one by one
   in increasing order; the same is done in decreasing order, and both must agree on every word (the tables are consistent).
2. Moebius inversion gives the unique multilinear polynomial in h[j]: the local law.
3. Checks against direct enumeration (study 2026-11-15-ring-counts-stackings): every site of the 11 named polytypes at l <= 24
   (both atoms; the upper atom by the reflection j -> -j), and every LOCALDATA word given on the command line.
4. Period averages: the law averaged over a period, in terms of f (h fraction) and pair frequencies.
Usage: law.py DELTAFILES... [--named DIR] [--local FILES...] [--drop6]  (--drop6: negative control without the six-crossing terms)
"""
import sys, re, itertools, glob, os
from fractions import Fraction as Fr
from collections import defaultdict
out = lambda *a: print(*a, flush=True)
DIAMOND = {6: 12, 8: 24, 10: 240, 12: 1128, 14: 8148, 16: 50016, 18: 349236, 20: 2362200, 22: 16716612, 24: 118335744}  # 2*A038515
LENS = (18, 20, 22, 24)
args = sys.argv[1:]
named_dir = None; local_files = []; drop6 = '--drop6' in args; files = []
i = 0
while i < len(args):
    if args[i] == '--named': named_dir = args[i + 1]; i += 2
    elif args[i] == '--local':
        i += 1
        while i < len(args) and not args[i].startswith('--'): local_files.append(args[i]); i += 1
    elif args[i] == '--drop6': i += 1
    else: files.append(args[i]); i += 1
D4 = {}; D6 = defaultdict(dict); CHECKS = []
def check(name, ok): CHECKS.append(bool(ok)); out('CHECK', name, 'ok' if ok else 'FAIL'); return ok
for fn in files:
    for line in open(fn):
        m = re.match(r'DELTA4 flip (-?\d+) pattern (\w+) word \w+ (.*?) (ok|FAIL)$', line.strip())
        if m:
            D4[(int(m[1]), m[2])] = {int(a): int(b) for a, b in re.findall(r'l(\d+):(-?\d+)', m[3])}; continue
        m = re.match(r'DELTA([68]) flip (-?\d+) pattern (\w+) (.*?) hand-lemma', line.strip())
        if m:
            D6[(int(m[2]), m[3])][int(m[1])] = {int(a): int(b) for a, b in re.findall(r'l(\d+):(-?\d+)', m[4])}
check(f'input: 512 four-crossing cases ({len(D4)}) and 24 six/eight-crossing cases ({len(D6)})', len(D4) == 512 and len(D6) == 24)

def delta(kf, h):
    """h: dict bilayer -> 0/1 (missing = c); returns {l: Delta} for the flip of kf with all other letters as in h"""
    if not -4 <= kf <= 3: return {}
    pat4 = ''.join('h' if h.get(b, 0) else 'c' for b in range(kf - 3, kf + 4) if b != kf)
    d = defaultdict(int)
    for l, v in D4[(kf, pat4)].items(): d[l] += v
    if -3 <= kf <= 2 and not drop6:
        pat6 = ''.join('h' if h.get(b, 0) else 'c' for b in (kf - 1, kf + 1))
        for n, dl in D6[(kf, pat6)].items():
            for l, v in dl.items(): d[l] += v
    return d

LO, HI = -6, 5; NB = HI - LO + 1
def p_of(word, order):
    """word: tuple of 0/1 for bilayers LO..HI; telescoping from 3C"""
    cur = {}; tot = dict((l, DIAMOND[l]) for l in LENS)
    idx = [j for j in range(NB) if word[j]]
    if order < 0: idx = idx[::-1]
    for j in idx:
        k = LO + j
        for l, v in delta(k, cur).items():
            if l in tot: tot[l] += v
        cur[k] = 1
    return tot
# Delta must not depend on the letters at kf +- 3 (the reach lemma), and six-crossing terms not on kf +- 2: report
# pattern p lists bilayers kf-3, kf-2, kf-1, kf+1, kf+2, kf+3: positions 0 and 5 are kf-3 and kf+3
dep3 = all(D4[(kf, p)] == D4[(kf, 'c' + p[1:5] + 'c')] for kf in range(-4, 4) for p in [''.join(x) for x in itertools.product('ch', repeat=6)])
check('Delta4 does not depend on the letters of bilayers kf-3, kf+3 (tables use c[0..3] of each half)', dep3)
words = list(itertools.product((0, 1), repeat=NB))
P = {}; consistent = True
for w in words:
    a = p_of(w, 1); b = p_of(w, -1)
    consistent &= a == b; P[w] = a
check(f'telescoping in increasing and decreasing order agree on all {len(words)} words of bilayers {LO}..{HI} (consistency of the tables)', consistent)

def moebius(f):
    a = dict(f)
    for j in range(NB):
        for w in words:
            if w[j]:
                w0 = w[:j] + (0,) + w[j + 1:]
                a[w] = a[w] - a[w0]
    return {tuple(LO + j for j in range(NB) if w[j]): v for w, v in a.items() if v}
LAW = {}
for l in LENS:
    co = moebius({w: P[w][l] for w in words}); LAW[l] = co
    terms = []
    for S, v in sorted(co.items(), key=lambda z: (len(z[0]), z[0])):
        terms.append(str(v) if not S else f"{'+' if v > 0 else '-'} {abs(v)}*" + '*'.join(f'h[{j}]' for j in S))
    out(f'LAW lower atom of bilayer 0, l={l}: p = ' + ' '.join(terms))
    dep = sorted({j for S in co for j in S})
    out(f'  depends on bilayers {dep}; terms of degree 2: {sum(1 for S in co if len(S) == 2)}, degree >= 3: {sum(1 for S in co if len(S) >= 3)}')
    check(f'l={l}: window edges {LO}, {HI} not used', LO not in dep and HI not in dep)
check('l=18 law = Theorem 5 of #102 (349236 - 12h[-2] - 30h[-1] - 42h[0] - 24h[1])', LAW[18] == {(): 349236, (-2,): -12, (-1,): -30, (0,): -42, (1,): -24})
check('l=20 law = Theorem 5 of #102 (2362200 - 30h[-2] - 114h[-1] - 204h[0] - 12h[1])', LAW[20] == {(): 2362200, (-2,): -30, (-1,): -114, (0,): -204, (1,): -12})

def predict(l, hfun, u):
    """hfun(j) = 0/1 for bilayer j relative to the site's bilayer; u = 0 lower atom, 1 upper atom (reflection j -> -j)"""
    tot = 0
    for S, v in LAW[l].items():
        prod = 1
        for j in S: prod *= hfun(-j if u else j)
        tot += v * prod
    return tot

if named_dir:
    NAMED = dict([('3C', 'c'), ('2H', 'h'), ('4H', 'hc'), ('6H', 'hcc'), ('8H', 'hccc'), ('9R', 'hhc'), ('10H', 'hcccc'),
                  ('15R', 'hchcc'), ('12R', 'hhhc'), ('21R', 'hcchccc'), ('10H*', 'hhchc')])
    nsite = 0; allok = True; avg = defaultdict(lambda: defaultdict(list))
    for fn in sorted(glob.glob(os.path.join(named_dir, 'named-*.txt'))):
        cur = None
        for line in open(fn):
            m = re.match(r'DATA named (\S+) phase (\d+) u (\d) .*local word (\w+)', line)
            if m: cur = (m[1], int(m[2]), int(m[3]), m[4]); continue
            m = re.match(r'\s+cycles l=6\.\.24 step 2: \[(.*)\]', line)
            if m and cur:
                name, ph, u, lw = cur; w = NAMED[name]
                hf = lambda j: 1 if w[(ph + j) % len(w)] == 'h' else 0
                assert ''.join('h' if hf(j) else 'c' for j in range(-3, 4)) == lw, (cur,)
                vals = dict(zip(range(6, 25, 2), map(int, m[1].split(','))))
                pr = {l: predict(l, hf, u) for l in LENS}
                ok = all(pr[l] == vals[l] for l in LENS); allok &= ok; nsite += 1
                for l in LENS: avg[name][l].append(vals[l])
                out(f'NAMED {name} phase {ph} u {u}: direct {[vals[l] for l in LENS]} law {[pr[l] for l in LENS]}', 'ok' if ok else 'FAIL')
                cur = None
    check(f'law = direct enumeration at every site of the named polytypes, l = 18..24 ({nsite} sites)', allok and nsite > 0)
    out('PERIOD AVERAGES (direct) and Theorem 2 of the ring-counts study: 16716612 - 3696 f; 118335744 - 13464 f + 108 b')
    t2 = True
    for name, d in avg.items():
        w = NAMED[name]; n = len(w); f = Fr(w.count('h'), n); b = Fr(sum(1 for j in range(n) if w[j] != w[(j + 1) % n]), n)
        a22 = Fr(sum(d[22]), len(d[22])); a24 = Fr(sum(d[24]), len(d[24]))
        ok = a22 == 16716612 - 3696 * f and a24 == 118335744 - 13464 * f + 108 * b; t2 &= ok
        out(f'  {name}: f={f} b={b} avg22={a22} avg24={a24}', 'ok' if ok else 'FAIL')
    check('Theorem 2 lines at 22, 24 hold on the direct averages', t2)

if local_files:
    nw = 0; allok = True; bad = []
    for fn in local_files:
        for line in open(fn):
            if not line.startswith('LOCALDATA'): continue
            f = line.split(); L, W, u, word = int(f[2]), int(f[4]), int(f[6]), f[8]
            i = f.index('cyc'); j = f.index('sp'); cyc = dict(zip(range(6, L + 1, 2), map(int, f[i + 1:j])))
            hf = lambda jj: 1 if (-W <= jj <= W and word[jj + W] == 'h') else 0
            for l in LENS:
                if l <= L:
                    pr = predict(l, hf, u)
                    if pr != cyc[l]: allok = False; bad.append((word, u, l, cyc[l], pr))
            nw += 1
    for x in bad[:10]: out('LOCAL MISMATCH word, atom, l, direct, law:', x)
    check(f'law = direct enumeration for every local word given ({nw} (word, atom) pairs, l = 18..{max(LENS)})', allok and nw > 0)

# period averages from the law: shift-average over a period of the multilinear terms
out('PERIOD-AVERAGE FORM: average of p over the sites of a period = c0 + sum over term shapes of coefficient * frequency of that h pattern')
for l in LENS:
    shapes = defaultdict(int)
    for S, v in LAW[l].items():
        if S: shapes[tuple(j - min(S) for j in S)] += v
    out(f'  l={l}: constant {LAW[l].get((), 0)}; ' + ', '.join(f"{'h' + ''.join('h' if k in s else '.' for k in range(1, max(s) + 1)) if len(s) > 1 else 'h'}: {v}" for s, v in sorted(shapes.items())))
out('ALLCHECKS', 'ok' if all(CHECKS) else 'FAIL', f'({sum(CHECKS)}/{len(CHECKS)})')
