# lemma5_check.py: our own exact check of Babanskyy (aiXiv 2610.01847) Section 5 finite data, from the paper's definitions.
# N on {a,b,c,d}: a<b, c<b, c<d. One-point extensions by x with profile (D, U): D an ideal, U a filter, d <_N u for all d in D, u in U.
# Checks: ideals/filters of N (8 each); exactly 20 valid profiles; |L| per profile (the Lemma 5.2 matrix); exactly 15 isomorphism
# classes with |L| multiset 5,5,7,7,8,9,9,11,14,14,16,16,18,18,25; the five stated isomorphisms (by explicit relabeling AND by brute
# isomorphism); Appendix A invariants (|L|, lower/upper count multiset) distinct across classes; Corollary 5.3 (classes with |L| | 120);
# Lemma 5.5: the 8 extensions of P(empty, abd) and its first-letter / first-pair counts; the integer solutions of 5a + 3b = 24.
# Controls: N itself has the 5 extensions acbd, acdb, cabd, cadb, cdab; a deliberately invalid profile (D = {b}) is rejected.
import itertools
E = 'abcdx'
N = {('a', 'b'), ('c', 'b'), ('c', 'd')}
def closure(rel):
    r = set(rel)
    while True:
        add = {(p, s) for (p, q) in r for (q2, s) in r if q == q2} - r
        if not add: return r
        r |= add
def ext(elems, rel):
    return [''.join(w) for w in itertools.permutations(elems) if all(w.index(p) < w.index(q) for p, q in rel)]
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
check('control: N has 5 extensions acbd acdb cabd cadb cdab', sorted(ext('abcd', N)) == sorted(['acbd', 'acdb', 'cabd', 'cadb', 'cdab']))
subsets = [frozenset(s) for k in range(5) for s in itertools.combinations('abcd', k)]
ideals = [S for S in subsets if all(p in S for (p, q) in N if q in S)]
filters = [S for S in subsets if all(q in S for (p, q) in N if p in S)]
name = lambda S: ''.join(sorted(S)) or '0'
check(f'ideals {sorted(map(name, ideals))} = paper', sorted(map(name, ideals)) == sorted(['0', 'a', 'c', 'ac', 'cd', 'abc', 'acd', 'abcd']))
check(f'filters {sorted(map(name, filters))} = paper', sorted(map(name, filters)) == sorted(['0', 'b', 'd', 'ab', 'bd', 'abd', 'bcd', 'abcd']))
prof = [(D, U) for D in ideals for U in filters if all((d, u) in N for d in D for u in U)]
check(f'valid profiles: {len(prof)} (paper 20)', len(prof) == 20)
check('control: D = {b} (not an ideal) is rejected', frozenset('b') not in ideals)
def poset(D, U):
    return closure(N | {(d, 'x') for d in D} | {('x', u) for u in U})
for D, U in prof:   # N stays induced (Lemma 5.1 converse)
    if {(p, q) for (p, q) in poset(D, U) if 'x' not in (p, q)} != N: check(f'N induced in profile ({name(D)},{name(U)})', False)
L = {(name(D), name(U)): len(ext(E, poset(D, U))) for D, U in prof}
paper = {('0', '0'): 25, ('0', 'b'): 18, ('0', 'd'): 16, ('0', 'ab'): 9, ('0', 'bd'): 14, ('0', 'abd'): 8, ('0', 'bcd'): 7, ('0', 'abcd'): 5,
         ('a', '0'): 16, ('a', 'b'): 9, ('c', '0'): 18, ('c', 'b'): 11, ('c', 'd'): 9, ('c', 'bd'): 7, ('ac', '0'): 14, ('ac', 'b'): 7,
         ('cd', '0'): 9, ('abc', '0'): 7, ('acd', '0'): 8, ('abcd', '0'): 5}
check(f'|L| per profile = the Lemma 5.2 matrix (our reading of it): {L == paper}', L == paper)
if L != paper: print('  ours:', L)
def iso(P, Q):
    for perm in itertools.permutations(E):
        f = dict(zip(E, perm))
        if {(f[p], f[q]) for p, q in P} == Q: return True
    return False
keys = list(L); P = {k: poset(frozenset(k[0].strip('0')), frozenset(k[1].strip('0'))) for k in keys}
classes = []
for k in keys:
    for c in classes:
        if iso(P[k], P[c[0]]): c.append(k); break
    else: classes.append([k])
check(f'isomorphism classes: {len(classes)} (paper 15)', len(classes) == 15)
mult = sorted(L[c[0]] for c in classes)
check(f'|L| multiset {mult} = 5,5,7,7,8,9,9,11,14,14,16,16,18,18,25', mult == [5, 5, 7, 7, 8, 9, 9, 11, 14, 14, 16, 16, 18, 18, 25])
pairs = [(('ac', 'b'), ('abc', '0'), '(b x)'), (('0', 'bcd'), ('c', 'bd'), '(c x)'), (('0', 'abd'), ('acd', '0'), '(a d b x c)'),
         (('c', 'd'), ('cd', '0'), '(d x)'), (('0', 'ab'), ('a', 'b'), '(a x)')]
def cyc(s):
    f = {e: e for e in E}; cs = s.strip('()').split()
    for i, e in enumerate(cs): f[e] = cs[(i + 1) % len(cs)]
    return f
same = lambda k1, k2: any(k1 in c and k2 in c for c in classes)
for k1, k2, c in pairs:
    f = cyc(c); mapped = {(f[p], f[q]) for p, q in P[k1]}
    check(f'isomorphism {k1} ~ {k2} by {c}: explicit relabeling {mapped == P[k2]}, same class {same(k1, k2)}', mapped == P[k2] and same(k1, k2))
check('the only identifications are the five stated', sum(len(c) - 1 for c in classes) == 5)
def sig(Pk):
    return (len(ext(E, Pk)), tuple(sorted((sum(1 for p, q in Pk if q == e), sum(1 for p, q in Pk if p == e)) for e in E)))
check('Appendix A: (|L|, lower/upper multiset) distinct across the 15 classes', len({sig(P[c[0]]) for c in classes}) == 15)
div = [c for c in classes if 120 % L[c[0]] == 0]
check(f'Corollary 5.3: classes with |L| | 120: {sorted(L[c[0]] for c in div)} = [5, 5, 8]', sorted(L[c[0]] for c in div) == [5, 5, 8])
e55 = sorted(ext(E, P[('0', 'abd')]))
check(f'Lemma 5.5 extensions {e55}', e55 == sorted(['cxabd', 'cxadb', 'cxdab', 'xacbd', 'xacdb', 'xcabd', 'xcadb', 'xcdab']))
cnt = lambda pre: sum(1 for w in e55 if w.startswith(pre))
check(f'Lemma 5.5 counts: x {cnt("x")}, c {cnt("c")}, xc {cnt("xc")}, xa {cnt("xa")}, cx {cnt("cx")} = 5, 3, 3, 2, 3',
      (cnt('x'), cnt('c'), cnt('xc'), cnt('xa'), cnt('cx')) == (5, 3, 3, 2, 3) and cnt('x') + cnt('c') == 8)
sols = [(a, b) for a in range(6) for b in range(9) if 5 * a + 3 * b == 24]
check(f'5a + 3b = 24 solutions {sols} = [(0, 8), (3, 3)]', sols == [(0, 8), (3, 3)])
check('|L| = 5 classes are (abcd, 0) [all end with x] and (0, abcd) [all begin with x]',
      all(w[-1] == 'x' for w in ext(E, P[('abcd', '0')])) and all(w[0] == 'x' for w in ext(E, P[('0', 'abcd')])))
print('FINAL ok' if ok else 'FINAL FAIL')
