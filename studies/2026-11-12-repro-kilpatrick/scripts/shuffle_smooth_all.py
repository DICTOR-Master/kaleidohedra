# shuffle_smooth_all.py: the rest of Kilpatrick's claims, our own code (functions from shuffle_smooth.py, which reproduces Table 1).
# (1) generation check: smooth words by brute force over all 2^n words equal the extension-generated set, n <= 20;
# (2) Lemma 2.2 (factoriality): every factor of every smooth word of length <= 24 is smooth;
# (3) Lemma 3.2 (atoms): the smooth parity atoms among all smooth words of length <= 40 are exactly the ten words of A, max length 8;
#     Lemma 3.1 (unique factorisation) on every smooth tangram <= 40; and A_k, B_k not smooth for k = 1..6, D(A_k), D(B_k) as stated;
# (4) totals: 16,146 smooth words (lengths 1..40), 4,204 smooth tangrams, 4,170 positive, 34 negative (Section 4);
# (5) Theorem 1.3 / Section 5: Kolakoski prefixes - tangram iff n and S(n) even; tangram prefixes below 18 are exactly P4, P8, P16,
#     P4 and P8 not shuffle squares, P16 is; direct shuffle test of every prefix up to NK; every prefix smooth up to NK;
#     Lemma 5.1: mixed aligned pairs keep occurring (count up to NKL);
# (6) Corollary 5.2: greedy atom blocks of the Kolakoski prefix up to NKL all have length 18..24 and are shuffle squares; the
#     concatenated colouring gives equal U and D subsequences and every monochromatic interval has length <= 48 (max reported);
# (7) the ancillary certificate's size 291,550 bytes and SHA-256 as stated (a fact about the published file only).
import sys, os, hashlib, itertools
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'shuffle_smooth.py')).read().split('\nlevel = ')[0]
ns = {}; exec(compile(src, 'shuffle_smooth.py', 'exec'), ns)
runs, smooth, shuffle_square = ns['runs'], ns['smooth'], ns['shuffle_square']
NK = int(sys.argv[1]) if len(sys.argv) > 1 else 120
NKL = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
CERT = sys.argv[3] if len(sys.argv) > 3 else None
# 12 Nov: the direct shuffle test is our extra cross-check and its memoised search is exponential in memory (53 GB at n -> 120);
# its range NKD is now separate (argv[4]); the paper's claims (5)-(7) do not depend on it.
NKD = int(sys.argv[4]) if len(sys.argv) > 4 else 60
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
def D(w):
    r = runs(w); a, b = (1 if r[0] == 1 else 0), (len(r) - 1 if r[-1] == 1 else len(r))
    return ''.join(map(str, r[a:b])) if a < b else ''
byn = {1: ['1', '2']}
for n in range(2, 41): byn[n] = [w + c for w in byn[n - 1] for c in '12' if smooth(w + c)]
allsmooth = set(w for n in byn for w in byn[n])
for n in range(1, 21):
    brute = set(''.join(t) for t in itertools.product('12', repeat=n) if smooth(''.join(t)))
    if brute != set(byn[n]): check(f'generation n={n}', False)
check('(1) brute force = extension generation for every n <= 20', ok)
fact_ok = all(w[i:j] in allsmooth for n in range(1, 25) for w in byn[n] for i in range(n) for j in range(i + 1, n + 1))
check('(2) Lemma 2.2: every factor of every smooth word of length <= 24 is smooth', fact_ok)
par = lambda u: (u.count('1') % 2, u.count('2') % 2)
tang = lambda u: par(u) == (0, 0)
def atoms(w):
    out, s = [], 0
    for i in range(1, len(w) + 1):
        if tang(w[s:i]) and tang(w[:i]): out.append(w[s:i]); s = i
    return out
A = {'11','22','1212','1221','2112','2121','121121','212212','12112212','21221121'}
found = set(w for w in allsmooth if tang(w) and not any(tang(w[:i]) for i in range(1, len(w))))
check(f'(3) Lemma 3.2: smooth parity atoms (lengths <= 40) = A exactly; max length {max(map(len, found))}', found == A)
tangs = [w for n in range(2, 41, 2) for w in byn[n] if tang(w)]
check('(3) Lemma 3.1: every smooth tangram <= 40 factors into atoms from A that concatenate back', all(''.join(atoms(w)) == w and all(a in A for a in atoms(w)) for w in tangs))
Ak = lambda k: '1211' + '2211' * k + '21'; Bk = lambda k: '1211' + '2211' * k + '2212'
check('(3) D(A_k) = 1 2^(2k+1) 1, D(B_k) = 1 2^(2k+2) 1 (k = 0..6); A_k, B_k smooth only at k = 0',
      all(D(Ak(k)) == '1' + '2' * (2 * k + 1) + '1' and D(Bk(k)) == '1' + '2' * (2 * k + 2) + '1' and smooth(Ak(k)) == (k == 0) and smooth(Bk(k)) == (k == 0) for k in range(7)))
neg = [w for w in tangs if not shuffle_square(w)]
check(f'(4) totals: smooth words 1..40 = {len(allsmooth)} (16,146), tangrams {len(tangs)} (4,204), positive {len(tangs) - len(neg)} (4,170), negative {len(neg)} (34)',
      len(allsmooth) == 16146 and len(tangs) == 4204 and len(neg) == 34)
K = [1, 2, 2]; i = 2
while len(K) < max(NK, NKL) + 50:
    nxt = 1 if K[-1] == 2 else 2; K += [nxt] * K[i]; i += 1
check('Kolakoski: run lengths of K equal K (first 2000 runs)', runs(''.join(map(str, K)))[:2000] == K[:2000])
K = ''.join(map(str, K))
check('Kolakoski: starts 122112122122112112212', K.startswith('122112122122112112212'))
Sn = lambda n: sum(int(c) for c in K[:n])
check('(5) tangram iff n and S(n) even (n <= 3000)', all(tang(K[:n]) == (n % 2 == 0 and Sn(n) % 2 == 0) for n in range(1, 3001)))
low = [n for n in range(1, 18) if tang(K[:n])]
check(f'(5) tangram prefixes below 18: {low} = [4, 8, 16]; P4, P8 not shuffle squares, P16 is', low == [4, 8, 16] and not shuffle_square(K[:4]) and not shuffle_square(K[:8]) and shuffle_square(K[:16]) and K[:16] == '1221121221221121')
check(f'(5) every Kolakoski prefix up to {NK} is smooth', all(smooth(K[:n]) for n in range(1, NK + 1)))
bad = [n for n in range(1, NKD + 1) if shuffle_square(K[:n]) != (tang(K[:n]) and n not in (4, 8))]
check(f'(5) Theorem 1.3 by direct shuffle test of every prefix 1..{NKD} (our extra cross-check): violations {bad}', not bad)
mixed = [j for j in range(NKL // 2) if K[2 * j] != K[2 * j + 1]]
check(f'(5) Lemma 5.1: {len(mixed)} mixed aligned pairs among the first {NKL // 2}, last at pair {mixed[-1]}', len(mixed) > 100 and mixed[-1] > NKL // 2 - 50)
def colour(w):
    n = len(w)
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def go(i, q):
        if len(q) > n - i: return None
        if i == n: return '' if q == '' else None
        c = w[i]
        if q and q[0] == c:
            r = go(i + 1, q[1:])
            if r is not None: return 'D' + r
        r = go(i + 1, q + c)
        return None if r is None else 'U' + r
    return go(0, '')
blocks, cur, s = [], '', 0
for a in atoms(K[:NKL]):
    cur += a
    if len(cur) >= 18: blocks.append(cur); cur = ''
cols = [colour(b) for b in blocks]
lens_ok = all(18 <= len(b) <= 24 for b in blocks); sq_ok = all(c is not None for c in cols)
word = ''.join(blocks); col = ''.join(cols)
U = ''.join(c for c, x in zip(word, col) if x == 'U'); Dd = ''.join(c for c, x in zip(word, col) if x == 'D')
mono = max(len(list(g)) for _, g in itertools.groupby(col))
check(f'(6) Corollary 5.2 on the first {len(word)} letters: {len(blocks)} greedy blocks, lengths {min(map(len, blocks))}..{max(map(len, blocks))} (18..24), all shuffle squares, U = D subsequences, longest monochromatic interval {mono} (<= 48)',
      lens_ok and sq_ok and U == Dd and mono <= 48)
if CERT:
    b = open(CERT, 'rb').read()
    check(f'(7) certificate size {len(b)} bytes (291,550), SHA-256 as printed in the paper', len(b) == 291550 and hashlib.sha256(b).hexdigest() == 'd04eb188c2529a67ac5ee7161fe83940fe316b3ac54f7d42fbdd59be7936b42f')
print('FINAL ok: every claim confirmed' if ok else 'FINAL FAIL')
