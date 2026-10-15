# Step 30c: exact check of the clashes behind step 30b at height 12.81: the rival (h 13.80) against the target, the third copy
# (h 14.04, rho 1.91) and the self-clashing ring copy (h 14.79); and whether the third copy's own ring clashes with itself.
import numpy as np
exec(open('scripts/chorus_h128.py').read().split("# the chorus's greedy")[0])
iR = ov[0]; zR = LP @ ax; rR = np.linalg.norm(LP - np.outer(zR, ax), axis=1)
d2 = np.linalg.norm(LP - LP[iR], axis=1); cand = [j for j in range(NL) if j != iR and d2[j] < rmax]
hits = [(j, state(loc[iR][1], loc[j][1])) for j in cand]
res = ['(30c) exact, height 12.81: every copy the rival (h %.4f, rho %.4f) overlaps:' % (zR[iR], rR[iR])]
for j, s_ in hits:
    if s_ == 'overlap': res.append(f'    h {zR[j]:.4f} rho {rR[j]:.4f}{" (target)" if j == iT else ""}: OVERLAP (exact); its own ring self-clashes: {forced(j)}')
res.append(f'    rival touches exactly: {sum(s_ == "touch" for _, s_ in hits)}')
print('\n'.join(res)); open('data/chorus-fork-exact2.txt', 'w').write('\n'.join(res) + '\n')
