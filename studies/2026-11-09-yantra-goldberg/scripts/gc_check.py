# Which great circles carry the network? Pole of an arc a-b = normalised a x b (up to sign). Count distinct poles per family.
exec(open('id_hexagram_net.py').read().split('def arc')[0])
def poles(polys):
    P = []
    for pts in polys:
        for a, b in zip(pts, pts[1:] + pts[:1]):
            n = nrm(np.cross(a, b)); n = n if (n[0], n[1], n[2]) > (0, 0, 0) else -n
            if not any(abs(abs(np.dot(n, q)) - 1) < 1e-9 for q in P): P.append(n)
    return P
pu, pd, pp = poles(up), poles(down), poles(pent)
same = sum(1 for q in pp if any(abs(abs(np.dot(q, r)) - 1) < 1e-9 for r in pd))
print(f'great circles: up (ID) {len(pu)}, turned {len(pd)}, pentagram {len(pp)}; pentagram circles shared with turned: {same}')
allp = poles(up + down + pent); print('network total distinct great circles:', len(allp))
# arcs per circle on turned+pentagram
import collections
cnt = collections.Counter()
for pts in down + pent:
    for a, b in zip(pts, pts[1:] + pts[:1]):
        n = nrm(np.cross(a, b)); k = min(range(len(allp)), key=lambda i: 1 - abs(np.dot(n, allp[i]))); cnt[k] += 1
print('arcs per blue/violet circle:', sorted(cnt.values()))
ang = sorted(set(round(float(np.degrees(np.arccos(min(1, abs(np.dot(a, b)))))), 4) for a in pd for b in pd if abs(np.dot(a, b)) < 1 - 1e-9))
print('angles between turned circles (deg):', ang[:8]); print('FINAL ok')
