# DICTO 2026-10-18 octet study -- STEP 16: how much space each kind of piece takes in the octet build (exact shares of the cell).
# "how much space do these octet arrangements cover together with ocds" -> data/step16-shares.json
from q5 import *
S2 = load('step2-octet-frame.json')['checks']; S3 = load('step3-key-candidate.json')['checks']; S11 = load('step11-exact.json')['checks']; S15 = load('step15-core.json')['checks']
cell = q(S2['cell_volume'])
parts = [('OCD (bare)', qr(1), q(S2['ocd_volume'])), ('keys (8 per OCD)', qr(8), q(S3['key_volume'])),
         ('notched caps', qr(6), q(S11['notched_cap'])), ('Penrose cores', qr(6), q(S15['core'])), ('middle rests', qr(6), q(S15['rest_of_middle'])),
         ('tetrahedra (left + right)', qr(2), q(S11['notched_tet']))]
rows = []; tot = Z
for nm, n, v in parts:
    share = qd(qm(n, v), cell); tot = qa(tot, share); rows.append(dict(piece=nm, per_cell=qs_(qm(n, v)), share=qs_(share), percent=100 * qf(share)))
for r in rows: print(f"{r['piece']:28s} {r['percent']:7.3f}%   exact share {r['share']}")
print('total', qs_(tot), tot == ONE)
bcc = None
save('step16-shares.json', dict(mark=MARK, step=16, cell=qs_(cell), rows=rows, total_is_one=tot == ONE))
