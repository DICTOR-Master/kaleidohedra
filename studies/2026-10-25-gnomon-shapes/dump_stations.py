# Dump the twelve stations of DICTO's golden cycle with exact corners in Q(√5) (a + b√5, a, b rational), built by the published
# construction scripts of Progenitors (#34) and Vajrayana (#35) (studies/2026-10-16-progenitors), not snapped from floats.
# I, ID, O(G), TI, H, RT, I·φ³ from o_dharma.py; rTI (core) and jtI (hull) from core_hull_in_cycle.py; M (G) from gap_pieces_exact.py;
# Cleo star tips = 2 × the face centres of I (each spike is a Cleo-Ico reflected in its face); D′ = the 20 tips (Vajrayana §2).
# -> stations-exact.json  (run from the progenitors study folder; needs ~/kaleidohedra/studies/2026-10-16-polar-dharma)
import os, sys, json
OUTD = os.path.dirname(os.path.abspath(__file__)); P = os.path.expanduser('~/k-research/studies/2026-10-16-progenitors'); os.chdir(P)
src = open('scripts/gap_pieces_exact.py').read().split("vol = lambda V")[0]
exec(src)
I = S['I']; fcI = [[sum((I[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)] for idx in planes(I)]
tips = [[x * 2 for x in c] for c in fcI]
out = {'I': I, 'Cleo star tips': tips, "D′": tips, 'ID': S['ID'], 'OG': S['O'], 'rTI': core, 'TI': S['TI'], 'H': S['H'],
       'jtI': hull, 'RT': S['RT'], 'M': G, 'I·φ³': S['I·φ³']}
ser = {k: [[[str(x.a), str(x.b)] for x in v] for v in V] for k, V in out.items()}
json.dump(ser, open(os.path.join(OUTD, 'stations-exact.json'), 'w'), ensure_ascii=False)
print({k: len(V) for k, V in out.items()})
