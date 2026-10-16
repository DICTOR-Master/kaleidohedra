# DICTO OCD Stella seed, exact in Q(√5) (DICTO 2026-10-16). Minkowski argument: for a convex S containing the origin, S + φv ⊂ S + φS = φ²S
# for every corner v, touching at φ²v; and S/φ + S = φS, so the centre S/φ touches S + φv at φv exactly when v is on the surface. So the seed
# (outer φ²S, twelve S + φv_i at the 12 farthest corners v_i, centre S/φ) closes iff no two of the twelve overlap: S + φv_i and S + φv_j are
# interior-disjoint iff the gauge of S − S = 2S (S is centrally symmetric) at φ(v_i − v_j) is at least 1, i.e. g_S(φ(v_i − v_j)/2) ≥ 1, with
# equality when they touch. g_S(x) = max over faces n·x/d. Checked exactly here, with the 12 far corners, their axes, and which faces meet.
# -> data/stella-seed-exact.txt
src = open('scripts/crystal_gap_exact.py').read(); exec(src[:src.index("S = polytope(H_K + HEX + HC)")])
S = polytope(H_K + HEX + HC)
from collections import Counter
phi = Q(Fr(1, 2), Fr(1, 2)); half = Q(Fr(1, 2))
out.clear(); say('DICTO · dictospheres.com'); say('DICTO OCD Stella seed, exact in Q(√5)')
r2 = [dot(v, v) for v in S['V']]; m = max(r2, key=lambda x: x.f())
far = [v for v, r in zip(S['V'], r2) if r == m]
say(f'OCD Stella: {len(S["V"])} corners, {len(S["F"])} faces; corners at the largest squared radius {m!r}: {len(far)}, on axes {sorted(Counter(axtype(v) for v in far).items())}')
assert S['V'] and all(sgn(d) > 0 for n, d in S['H'])          # the origin is inside
sym = all(any(key(neg(v)) == key(w) for w in S['V']) for v in S['V']); say(f'centrally symmetric: {sym}')
def gauge(x): return max((dot(n, x) / d for n, d in S['H']), key=lambda q: q.f())
pairs = {}
for i, j in itertools.combinations(range(len(far)), 2):
    g = gauge(mul(sub(far[i], far[j]), phi * half)); pairs.setdefault(repr(g), []).append((i, j))
say('gauge g_S(φ(v_i − v_j)/2) over the 66 pairs of the twelve (1 = touching, > 1 = apart, < 1 = overlap):')
for g, L in pairs.items():
    gv = gauge(mul(sub(far[L[0][0]], far[L[0][1]]), phi * half))
    say(f'   {g} = {gv.f():.6f}: {len(L)} pairs{"  (touching)" if gv == Q(1) else ""}{"  OVERLAP" if sgn(gv - Q(1)) < 0 else ""}')
touch = [p for g, L in pairs.items() for p in L if gauge(mul(sub(far[p[0]], far[p[1]]), phi * half)) == Q(1)]
deg = Counter(k for p in touch for k in p)
say(f'touching pairs {len(touch)}; each of the twelve touches {sorted(set(deg.values()))} others')
ok = all(sgn(gauge(mul(sub(far[i], far[j]), phi * half)) - Q(1)) >= 0 for i, j in itertools.combinations(range(12), 2))
say(f'no two of the twelve overlap: {ok}; so the seed closes exactly at φ², with the centre S/φ touching all twelve')
vS = pvol(S); gap = Q(1) - (Q(12) + Q(1) / (phi * phi * phi)) / (phi * phi * phi * phi * phi * phi)
say(f'gap share 1 − (12 + φ⁻³)/φ⁶ = {gap!r} = {gap.f():.6f}')
open('data/stella-seed-exact.txt', 'w').write('\n'.join(out) + '\n')
