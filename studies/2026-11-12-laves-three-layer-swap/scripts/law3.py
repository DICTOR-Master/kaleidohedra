# The Laves big atom M0 on the three-layer window (DICTO 12 Nov 2026; gap row "Hexagonality Law for the Laves big atom (#66, #67)").
# Window Law (#84, Main Theorem (c)) at g = 3: a count F fixed by three layer types is a straight line in the hexagonality on every
# stacking iff Delta_c = Delta_h = 0 (three layers -> two) and the Swap defect of the remaining pair count P is 0 (two -> one).
# Reads #64's exact weight walks (run 2 raw files, #57's census engine), finds the shortest type window fixing each piece, computes the
# three defects exactly (polynomials in lam) and compares the prediction with the law tested directly on every stacking.
# Controls: positive = the five two-layer Laves roles, M0 below 17/96, one-letter + coboundary tables; negative = restricted counts
# from the real M0 / M1 volumes, random tables (theorem check on every c/h word up to 12 layers).
# Usage: python3 law3.py pilot|full     (pilot: stackings up to 6 layers)
import os, sys, json, glob, itertools, random
from fractions import Fraction as Fr
import sympy as sp
L = sp.Symbol('lam')
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, '..', '..', '2026-10-27-splash-rules', 'run2', 'raw'))
OUT = os.path.normpath(os.path.join(HERE, '..', 'out'))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'pilot'
ROLES = ['M0', 'M1', 'K1', 'K2', 'K3', 'T']
STEP = {('A', 'B'): 1, ('B', 'C'): 1, ('C', 'A'): 1, ('B', 'A'): -1, ('C', 'B'): -1, ('A', 'C'): -1}
def steps(w): n = len(w); return [STEP[(w[k], w[(k + 1) % n])] for k in range(n)]
def types(w): st = steps(w); n = len(w); return ['c' if st[k - 1] == st[k] else 'h' for k in range(n)]   # layer k sits below gap k
W3 = [''.join(p) for p in itertools.product('ch', repeat=3)]
fails = []          # control or consistency failures -> FINAL FAIL
def bad(msg): fails.append(msg); print('  !! ' + msg, flush=True)

# ---------- defects on a three-layer table (any number type with + and -) ----------
def defects(F):
    Dc = F['ccc'] + F['hch'] - F['cch'] - F['hcc']
    Dh = F['chc'] + F['hhh'] - F['chh'] - F['hhc']
    # pair count left when Dc = Dh = 0 (#84 proof of (c)): A(xv) = F(xvc), B(vy) = F(cvy) - F(cvc), P = A + B
    P = {x + y: F[x + y + 'c'] + F['c' + x + y] - F['c' + x + 'c'] for x in 'ch' for y in 'ch'}
    DP = P['cc'] + P['hh'] - P['ch'] - P['hc']
    return Dc, Dh, DP, P
def cyc(u, g=3): m = len(u); return [''.join(u[(i + j) % m] for j in range(g)) for i in range(m)]
def cycle_sum(F, u):   # sum over the c/h cyclic word u minus the line through the pure stackings
    return sum(F[x] for x in cyc(u)) - u.count('c') * F['ccc'] - u.count('h') * F['hhh']
SHORT = ['ch', 'cch', 'chh']

# ---------- stage 0: the theorem itself, combinatorially (no geometry) ----------
def all_cyclic(maxlen):
    seen, out = set(), []
    for m in range(1, maxlen + 1):
        for t in itertools.product('ch', repeat=m):
            k = min(t[i:] + t[:i] for i in range(m))
            if k not in seen: seen.add(k); out.append(''.join(k))
    return out
def theorem_check():
    words = all_cyclic(12); rng = random.Random(20261112); agree = tot = 0; pos_ok = neg_ok = 0
    # span check: (Dc, Dh, DP) and the three short-cycle sums are the same three linear conditions
    sym = {u: sp.Symbol('F_' + u) for u in W3}
    Dc, Dh, DP, _ = defects(sym); K = [cycle_sum(sym, u) for u in SHORT]
    vec = lambda e: [sp.expand(e).coeff(sym[u]) for u in W3]
    rA = sp.Matrix([vec(e) for e in (Dc, Dh, DP)]).rank(); rB = sp.Matrix([vec(e) for e in K]).rank()
    rAB = sp.Matrix([vec(e) for e in (Dc, Dh, DP, *K)]).rank()
    print(f'  span check: rank(defects) {rA}, rank(short cycles) {rB}, rank(both) {rAB} (expect 3, 3, 3)', flush=True)
    if (rA, rB, rAB) != (3, 3, 3): bad('span check')
    for trial in range(600):
        kind = trial % 3
        if kind == 0:   # random table (negative unless by chance)
            F = {u: rng.randint(-5, 5) for u in W3}
        elif kind == 1:  # one-letter + coboundary (positive): f(middle) + b(first two) - b(last two)
            f = {x: rng.randint(-5, 5) for x in 'ch'}; b = {x + y: rng.randint(-5, 5) for x in 'ch' for y in 'ch'}
            F = {u: f[u[1]] + b[u[:2]] - b[u[1:]] for u in W3}
        else:            # pair count with a Swap defect, lifted (Dc = Dh = 0, DP != 0 in general)
            q = {x + y: rng.randint(-5, 5) for x in 'ch' for y in 'ch'}; F = {u: q[u[:2]] for u in W3}
        d = defects(F)[:3]; pred = all(x == 0 for x in d)
        obs = all(cycle_sum(F, u) == 0 for u in words)
        tot += 1; agree += (pred == obs)
        if kind == 1: pos_ok += obs
        if kind == 2 and d[2] != 0: neg_ok += (not obs)
    print(f'  theorem check on {len(words)} cyclic c/h words up to 12 layers: prediction = observation in {agree}/{tot} tables;'
          f' positives (one-letter + coboundary) on the line {pos_ok}/200; pair counts with a Swap defect off the line {neg_ok}', flush=True)
    if agree != tot or pos_ok != 200: bad('theorem check')

# ---------- stage 1: the Laves data ----------
def load():
    files = sorted(glob.glob(os.path.join(RAW, 'lvw_*.json')))
    data = {}
    for f in files:
        w = os.path.basename(f)[4:-5]
        if MODE == 'pilot' and len(w) > 6: continue
        d = json.load(open(f))
        if d.get('_w') != w: bad(f'{w}: _w mismatch')
        if d.get('_fails', 1) != 0: bad(f'{w}: census checks failed {d.get("_fails")}')
        data[w] = d
    return data
_cache = {}
def vol(d, w, i, lo, hi):
    for k, iv in enumerate(d['intervals']):
        if iv['lo'] in (None, 'None') or iv['hi'] in (None, 'None'): continue
        if Fr(iv['lo']) <= lo and hi <= Fr(iv['hi']):
            key = (w, k, i)
            if key not in _cache:
                x = iv['sites'][i]
                _cache[key] = sp.Integer(0) if x.get('vanished') or 'volume' not in x else sp.expand(len(w) * sp.sympify(x['volume']).subs('lam', L))
            return _cache[key]
    return None
def zero(e): return sp.expand(e) == 0
def main():
    print(f'law3 {MODE}: raw = run 2 Laves walks', flush=True)
    theorem_check()
    data = load(); W = sorted(data, key=lambda w: (len(w), w))
    T = {w: types(w) for w in W}
    print(f'  stackings: {len(W)}', {w: ''.join(T[w]) for w in W}, flush=True)
    if fails: print('FINAL FAIL before the Laves stage:', fails); sys.exit(1)
    cuts = sorted({Fr(iv[x]) for d in data.values() for iv in d['intervals'] for x in ('lo', 'hi') if iv[x] not in (None, 'None')})
    wins = [(lo, hi) for lo, hi in zip(cuts, cuts[1:]) if vol(data['ABC'], 'ABC', 0, lo, hi) is not None and vol(data['AC'], 'AC', 0, lo, hi) is not None]
    total = len(wins) * len(ROLES); done = 0; report = {'mode': MODE, 'stackings': {w: ''.join(T[w]) for w in W}, 'windows': []}
    verdict_M0 = []; mismatch = 0; neg_results = []
    for lo, hi in wins:
        wrep = {'lo': str(lo), 'hi': str(hi), 'roles': {}}
        for r in ROLES:
            ri = ROLES.index(r)
            V = {}
            for w in W:
                n = len(w); vs = [vol(data[w], w, 6 * g + ri, lo, hi) for g in range(n)]
                if all(v is not None for v in vs): V[w] = vs
            # locality: shortest type window (length, offset) with no clash
            loc = []
            for glen in (1, 2, 3, 4):
                for off in range(-glen, 2):
                    tab = {}; clash = 0
                    for w, vs in V.items():
                        n = len(w)
                        for g in range(n):
                            key = ''.join(T[w][(g + off + j) % n] for j in range(glen))
                            if key in tab and not zero(tab[key] - vs[g]): clash += 1
                            tab.setdefault(key, vs[g])
                    if clash == 0: loc.append((glen, off, len(tab)))
                if loc: break
            if not loc: bad(f'{r} ({lo},{hi}): no type window up to 4 layers fixes the piece'); done += 1; continue
            glen, off, nkeys = loc[0]
            # three-layer table: window (g+off3 .. g+off3+2) containing the fixing window
            off3 = next((c for c in [-1, 0] + list(range(-4, 3)) if c <= off and off + glen - 1 <= c + 2), None)   # prefer windows holding the gap's own two layers
            if glen == 4: bad(f'{r} ({lo},{hi}): needs four layer types'); done += 1; continue
            F = {}; clash3 = 0
            for w, vs in V.items():
                n = len(w)
                for g in range(n):
                    key = ''.join(T[w][(g + off3 + j) % n] for j in range(3))
                    if key in F and not zero(F[key] - vs[g]): clash3 += 1
                    F.setdefault(key, vs[g])
            if clash3: bad(f'{r} ({lo},{hi}): three-layer table clashes {clash3}')
            missing = [u for u in W3 if u not in F]
            rrep = {'fixing_window': {'layers': glen, 'offset': off, 'all_offsets_ok': [(a, b) for a, b, _ in loc]}, 'stackings': len(V)}
            # the law, tested directly
            a = sum(V['ABC']) / 3; b = sum(V['AC']) / 2
            law = {w: zero(sum(vs) - T[w].count('c') * a - T[w].count('h') * b) for w, vs in V.items() if w not in ('ABC', 'AC')}
            # the table reproduces every stacking total (Window Law (a))
            for w, vs in V.items():
                n = len(w)
                if not zero(sum(vs) - sum(F[''.join(T[w][(g + off3 + j) % n] for j in range(3))] for g in range(n))): bad(f'{r} {w}: table does not reproduce the total')
            if missing:
                rrep['missing_windows'] = missing; pred = None
            else:
                Dc, Dh, DP, P = defects(F)
                Ks = {u: sp.factor(cycle_sum(F, u)) for u in SHORT}
                pred = zero(Dc) and zero(Dh) and zero(DP)
                if pred != all(zero(k) for k in Ks.values()): bad(f'{r} ({lo},{hi}): defects and short cycles disagree')
                rrep.update({'F': {u: str(sp.factor(F[u])) for u in W3}, 'Delta_c': str(sp.factor(Dc)), 'Delta_h': str(sp.factor(Dh)),
                             'Delta_pair': str(sp.factor(DP)), 'short_cycles': {u: str(k) for u, k in Ks.items()}})
            obs = all(law.values())
            rrep.update({'law_all_tested': obs, 'law_fails_on': [w for w, ok in law.items() if not ok], 'predicted_line': pred})
            if pred is not None and pred != obs:
                # a failing prediction is only a contradiction if the tested words cover a short cycle; record either way
                mismatch += 1; bad(f'{r} ({lo},{hi}): prediction {pred} but law on tested stackings {obs}')
            # positive controls: every role fixed by two layers must obey the Swap Rule and the law (#66)
            if glen <= 2 and not (pred and obs): bad(f'positive control {r} ({lo},{hi}) (two-layer piece) off the line')
            if r == 'M0':
                ctx = {min(tuple(steps(w)[(g + j) % len(w)] for j in range(-2, 3)), tuple(-steps(w)[(g + j) % len(w)] for j in range(-2, 3))) for w in V for g in range(len(w))}
                rrep['six_layer_contexts_seen'] = f'{len(ctx)} of 16'
                verdict_M0.append((str(lo), str(hi), glen, pred, obs, len(V)))
                # negative control from real volumes: M0 counted only where its window reads chc
                if not missing and not zero(F['chc']):
                    Fn = {u: (F[u] if u == 'chc' else sp.Integer(0)) for u in W3}
                    pn = all(zero(x) for x in defects(Fn)[:3])
                    on = all(zero(sum(Fn[''.join(T[w][(g + off3 + j) % len(w)] for j in range(3))] for g in range(len(w)))) for w in V)   # pure stackings give 0, so the line is 0
                    neg_results.append(('M0 only at chc', str(lo), pn, on));
                    if pn or on: bad(f'negative control M0-only-at-chc ({lo},{hi}) not off the line: pred {pn} obs {on}')
            if r == 'M1' and not missing and off3 in (-1, 0):
                Fm = {u: (F[u] if u[(-off3)] != u[(-off3) + 1] else sp.Integer(0)) for u in W3}     # M1 only in mixed gaps
                if not all(zero(Fm[u]) for u in W3):    # a vanished M1 piece gives no test
                    pn = all(zero(x) for x in defects(Fm)[:3])
                    on = all(zero(sum(Fm[''.join(T[w][(g + off3 + j) % len(w)] for j in range(3))] for g in range(len(w)))) for w in V)
                    neg_results.append(('M1 only in mixed gaps', str(lo), pn, on))
                    if pn or on: bad(f'negative control M1-mixed-only ({lo},{hi}) not off the line: pred {pn} obs {on}')
            wrep['roles'][r] = rrep; done += 1
            print(f'PROGRESS {done}/{total} window ({lo}, {hi}) {r}: fixed by {glen} layer types (offset {off});'
                  f' defects zero: {pred}; law on {len(law)} stackings: {obs}', flush=True)
        report['windows'].append(wrep)
    report['M0'] = verdict_M0; report['negative_controls'] = neg_results; report['fails'] = fails
    os.makedirs(OUT, exist_ok=True)
    json.dump(report, open(os.path.join(OUT, f'law3_{MODE}.json'), 'w'), indent=1, default=str)
    print('M0 by window (lo, hi, layer types read, three-layer Swap Rule holds, law on all tested, stackings):', verdict_M0, flush=True)
    print('negative controls (name, window, predicted line, observed line):', neg_results, flush=True)
    three = [v for v in verdict_M0 if v[2] == 3]
    if fails: print(f'FINAL FAIL {len(fails)} failures: {fails[:5]}', flush=True); sys.exit(1)
    if not neg_results: print('FINAL FAIL no negative control ran', flush=True); sys.exit(1)
    print(f'FINAL ok {MODE}: prediction = observation in every window and role (mismatches {mismatch}); M0 reads three layer types in '
          f'{len(three)} windows; three-layer Swap Rule holds in {sum(1 for v in three if v[3])} of them; negatives off the line {len(neg_results)}/{len(neg_results)}', flush=True)
main()
