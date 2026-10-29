# HexOct-K, the stacking as the clock (DICTO 10-29: "more research on HexOct-K"). In the interlocking range a tile touches
# several tiles of the layer below. Lattice offsets (du, dv) are taken in the 60-degree lattice of #75; every layer shift
# (B = (1/3,1/3), C = (2/3,2/3)) lies along (1, 1), so s = du - dv does not change from layer to layer. The claim to test:
# for every five-layer context and every interlocking weight, the tiles a tile touches below have s in {-1, 0, +1}, with
# all three present (faces of positive area), and the same holds above. Then a tile can read its left, centre and right
# neighbour of the layer below along s, and keyed tiles run any elementary cellular automaton, one step per layer.
# Sampled face areas (contacts.py, floats on the exact tiles). Usage: clock_contacts.py <context index 0..31>
import sys, json
from fractions import Fraction as Fr
from tiles import ctx_words
from contacts import contacts
LAMS = [Fr(-1, 4), Fr(-1, 6), Fr(0), Fr(1, 10), Fr(1, 4), Fr(1, 3)]
ctx = sorted(ctx_words().items()); key, (word, L) = ctx[int(sys.argv[1])]
for lam in LAMS:
    area, gap, total = contacts(word, L, lam, N=1500)
    rows = {d: {} for d in (-1, 0, 1)}
    for (d, du, dv), a in area.items():
        if d in rows and a > 1e-4 * total:
            s = du - dv; assert s.denominator == 1, (d, du, dv)
            rows[d][int(s)] = rows[d].get(int(s), 0) + a
    print(json.dumps(dict(context=key, word=word, layer=L, lam=str(lam), total=total, gap=gap,
                          below={str(k): round(v, 4) for k, v in sorted(rows[-1].items())},
                          above={str(k): round(v, 4) for k, v in sorted(rows[1].items())},
                          lateral={str(k): round(v, 4) for k, v in sorted(rows[0].items())})), flush=True)
