# Progenitors step 8 (DICTO: "how would real compound size work"): O at its compound size (rho² = 9/4, interlocked with H) in the golden cycle.
# The compound as one double station between its core and hull: exact relations of O(9/4) with every station. -> data/compound-station.txt
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
O94 = [[x * Fr(9, 4) for x in v] for v in O]                    # O as H's polar in the TI midsphere (unit-sphere polar × 9/4)
def rel(A, B):
    pl = planes_exact(B); m = [max((dot(n, a) - d for n, d in pl), key=lambda q: q.f()) for a in A]
    return all(not (x.f() > 0 and x != 0) for x in m), sum(1 for x in m if x == 0)
S = [C[0], C[1], ('rTI', core), C[3], C[4], ('hull', hull), C[5], C[6]]
out = ['DICTO · dictospheres.com', 'Progenitors step 8: O at its compound size 9/4 (interlocked with H) against the stations (exact)']
for n, V in S:
    a, at = rel(O94, V); b, bt = rel(V, O94)
    out.append(f'  O(9/4) vs {n:5s}: O inside {n} {a} ({at} on faces); {n} inside O {b} ({bt} on faces)' + ('  — crossing' if not a and not b else ''))
a, _ = rel(C[1][1], core); out.append(f'  ID inside rTI: {a}')
print('\n'.join(out)); open('data/compound-station.txt', 'w').write('\n'.join(out) + '\n')
