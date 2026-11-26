# DICTO · Tacitus (harmonic silence) of the twelve special excavated solids (26 Nov 2026). With Claude (Anthropic).
# Face set = the pit walls (each wall a triangle: edge of P + apex), outward normal = out of the body (into the pit).
# Energies of the face directions in degrees 1..20, unit weights (i) and area weights (iii), classified by the house module
# tacitus.py (study 2026-11-25-tacitus): silent degrees, those forced by symmetry, and any silence beyond symmetry.
# Controls: the plain solids P (Platonic etc.) through the same code reproduce the Tacitus study's own answers.
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.join(HERE, '../../2026-11-25-tacitus/scripts')); import tacitus as T
exec(open(os.path.join(HERE, 'special_depths_all.py')).read().split('found = []')[0])
EX = json.load(open(os.path.join(HERE, '../data-exact-forms.json'))); out = []
def merge(N, A):
    # walls in one plane share a direction: one point per direction, weight = multiplicity (i) or summed area (iii)
    U, M, S_ = [], [], []
    for n, a in zip(N, A):
        for k, u in enumerate(U):
            if np.linalg.norm(u - n) < 1e-6: M[k] += 1; S_[k] += a; break
        else: U.append(n); M.append(1); S_.append(a)
    return np.array(U), np.array(M, float), np.array(S_)
def run(N, A):
    res = {}; N, Mu, Ar = merge(N, A)
    for var, w in (('i', Mu / Mu.sum()), ('iii', Ar / Ar.sum())):
        Rs = T.sym_group(N, T.labels(w)); dims = T.char_dims(Rs); c = T.classify(T.energies(N, w, 3), dims)
        if var == 'iii': c['beyond'] = [k for k in c['beyond'] if k != 1]
        res[var] = dict(G=len(Rs), silent=c['silent'], beyond=c['beyond'], grey=c['grey'])
    res['dirs'] = len(N); return res
for e in EX:
    V, F, N, D = S[e['P']]; s = e['s']; Ap = s * D[:, None] * N; WN, WA = [], []
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]):
            n = np.cross(V[b] - V[a], Ap[fi] - V[a]); ar = np.linalg.norm(n) / 2; n /= np.linalg.norm(n)
            c = (V[a] + V[b] + Ap[fi]) / 3
            cp = (V[f].mean(0) * len(f) + Ap[fi]) / (len(f) + 1)   # a point inside the pit
            if n @ (cp - V[a]) < 0: n = -n   # outward from the body = into the pit
            WN.append(n); WA.append(ar)
    r = run(np.array(WN), WA); r['P'], r['Q'], r['s'] = e['P'], e['Q'], e['closed']; out.append(r)
    print(f"{e['P']:24s} on {e['Q']:28s} |G| {r['i']['G']:3d} dirs {r['dirs']:3d}  silent(i) {r['i']['silent'][:10]}  beyond(i) {r['i']['beyond']}  beyond(iii) {r['iii']['beyond']}  grey {r['i']['grey']}{r['iii']['grey']}", flush=True)
json.dump(out, open(os.path.join(HERE, '../data-tacitus-excavated.json'), 'w'), indent=1)
ok = all(o['i']['G'] in (24, 48, 120) and not o['i']['grey'] and not o['iii']['grey'] for o in out)   # control: each solid keeps its full group (Td, Oh, Ih)
print('FINAL ok' if ok else 'FINAL FAIL (a solid lost its symmetry group, or grey energies)')
