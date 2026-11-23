# Aequus CIRT-30, T 26 (study 2026-11-19-aequi-complete row 504): the fair point restricted to the line d_C6 = d_RT24/12 = 1.
# (1) Krawczyk in one variable t = d_I12 for "solid angle of an I12 face = 4 pi/30" with C6 and RT24/12 planes held at depth 1
#     (on this line the four-plane corners are structural, so the type is certified as in certify.py);
# (2) the identity 2 Om(RT) - Om(C6) = 4 pi/30 along the line, evaluated in ball arithmetic at the root and at other t.
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import certify as C
from flint import arb, ctx
recs = C.load_all(); rec = [x for x in recs if x['study'].startswith('2026-11-19') and x['sid'] == 504][0]
idx = rec['idx']; d = rec['depths']
line = dict(rec, idx=idx[:6] + idx[18:] + idx[6:18], sizes=[18, 12], depths=['1.0', d[1]])
s = C.Die(line); s.setup()
print('line type: corners', len(s.full), 'graph', s.graph_ok, 'accidental', len(s.accidental), 'structural extra', sum(e['zero'] for e in s.extra))
rt, sl = s.type_radius(); print('type radius on the line', float(rt))
k = s.krawczyk(1e-40); print('1D Krawczyk tight:', k['ok'], k['enclosure'])
for e in range(4, 25):
    kk = s.krawczyk(10.0 ** (-e / 2))
    if kk['ok'] and 10.0 ** (-e / 2) < float(rt): print('1D uniqueness box half-width', 10.0 ** (-e / 2)); break
def omegas(t):
    ctx.prec = C.PREC; dep = [arb(1), t]; om = []
    for f in range(s.N):
        c = s.cyc[f]; P = [[C.D(sum((dep[o] * s.A[vi][o][q] for o in range(2)), arb(0)), []) for q in range(3)] for vi in c]
        w = arb(0)
        for i in range(1, len(c) - 1): w += C.tri(P[0], P[i], P[i + 1], s.sg[f][i - 1])[0].v
        om.append(w)
    return sum(om[:6]) / 6, sum(om[6:18]) / 12, sum(om[18:]) / 12
T = 4 * arb.pi() / 30
tstar = arb(k['enclosure'][0])
for t in [tstar, arb('1.0'), arb('1.005'), arb('1.01'), arb('1.02'), arb('1.03')]:
    oc, orr, oi = omegas(t)
    print('t', t.str(12), ' 2*Om_RT - Om_C - 4pi/30 =', (2 * orr - oc - T).str(5), ' Om_I - 4pi/30 =', (oi - T).str(5))
print('FINAL ok' if k['ok'] else 'FAIL')
