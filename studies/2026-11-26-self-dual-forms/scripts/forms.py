# DICTO · Vacuus, Resonus and Tacitus of McCooey's self-dual polyhedra (26 Nov 2026). With Claude (Anthropic).
# The solids are David McCooey's (Visual Polyhedra, dmccooey.com/polyhedra: "Greater Self-Dual Solids", "Improper Self-Dual
# Polyhedra", "Symmetries of Canonical Self-Dual Polyhedra"; built from plantri graphs, Brinkmann and McKay 2007), used as given from
# his data files (30-digit coordinates), by his names. Their Vacuus, Resonus and Tacitus forms are DICTO's constructions.
# Per solid: Vacuus plates (plane through the centre O and each edge), Resonus planes (through O parallel to each face), both up to
# sign; how many lie on mirrors of the solid; the overlap; the symmetry group order; Tacitus silences (degrees 1..12) of the face
# directions, unit weights (i) and area weights (iii), with the degrees forced by symmetry and those beyond it.
# Centre O = the origin of his canonical form (edge-scribed sphere centred at O).
# Usage: python forms.py <source dir> <out.json>
import sys, os, re, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../2026-11-25-tacitus/scripts'))
import tacitus as T
T.KMAX = 12
SRC, OUT = (sys.argv[1], sys.argv[2]) if __name__ == '__main__' else (None, None)

def parse(path):
    txt = open(path).read(); name = txt.splitlines()[0].strip()
    C = {}
    for m in re.finditer(r'^\s*(C\d+)\s*=\s*([-+0-9.eE]+)\s*(?:=|$)', txt, re.M): C.setdefault(m.group(1), float(m.group(2)))   # first, numeric value (a formula line may repeat the name)
    def val(tok):
        tok = tok.strip(); s = -1.0 if tok.startswith('-') else 1.0; tok = tok.lstrip('+-').strip()
        return s * (C[tok] if tok in C else float(tok))
    V = [[val(x) for x in m.group(1).split(',')] for m in re.finditer(r'^\s*V\d+\s*=\s*\(([^)]*)\)', txt, re.M)]
    F = [[int(x) for x in m.group(1).split(',')] for m in re.finditer(r'^\s*\{([^}]*)\}', txt, re.M)]
    return name, np.array(V), F

def planes_up_to_sign(N, tol=1e-9):
    out = []
    for n in N:
        n = n / np.linalg.norm(n)
        if not any(abs(abs(n @ m) - 1) < tol for m in out): out.append(n)
    return np.array(out)

def is_mirror(n, V, tol=1e-7):
    R = np.eye(3) - 2 * np.outer(n, n); W = V @ R.T
    return all(np.min(np.linalg.norm(V - w, axis=1)) < tol for w in W)

def analyse(path):
    name, V, F = parse(path)
    E = set()
    for f in F:
        for a, b in zip(f, f[1:] + f[:1]): E.add((min(a, b), max(a, b)))
    vac = planes_up_to_sign([np.cross(V[a], V[b]) for a, b in E if np.linalg.norm(np.cross(V[a], V[b])) > 1e-12])
    fn, area = [], []
    for f in F:
        P = V[f]; c = P.mean(0); n = np.zeros(3)
        for a, b in zip(P, np.roll(P, -1, 0)): n += np.cross(a - c, b - c)
        A = np.linalg.norm(n) / 2; n = n / np.linalg.norm(n)
        if n @ c < 0: n = -n
        fn.append(n); area.append(A)
    fn = np.array(fn); res = planes_up_to_sign(fn)
    vm = sum(is_mirror(n, V) for n in vac); rm = sum(is_mirror(n, V) for n in res)
    overlap = sum(1 for n in res if any(abs(abs(n @ m) - 1) < 1e-9 for m in vac))
    out = dict(name=name, file=os.path.basename(path), V=len(V), F=len(F), E=len(E), vacuus=len(vac), vacuus_mirrors=int(vm),
               resonus=len(res), resonus_mirrors=int(rm), overlap=int(overlap), resonus_in_vacuus=overlap == len(res))
    for var, w in (('i', np.ones(len(fn))), ('iii', np.array(area) / sum(area))):
        Rs = T.sym_group(fn, T.labels(w)); dims = T.char_dims(Rs); c = T.classify(T.energies(fn, w, 3), dims)
        if var == 'iii': c['beyond'] = [k for k in c['beyond'] if k != 1]   # Minkowski
        out[var] = dict(G=len(Rs), silent=c['silent'], forced=c['forced'], beyond=c['beyond'], grey=c['grey'])
    return out

if __name__ == '__main__':
    files = sorted(f for f in glob.glob(os.path.join(SRC, '*SelfDual*.txt')) if 'SelfDuals' not in os.path.basename(f))   # the solids only (not the listing pages)
    res, bad = [], []
    for f in files:
        try: res.append(analyse(f))
        except Exception as ex: bad.append((os.path.basename(f), str(ex)[:80]))
    json.dump(res, open(OUT, 'w'), indent=1)
    print('solids', len(res), 'failed', len(bad), bad[:5])
    for r in sorted(res, key=lambda r: (-r['i']['G'], -r['F']))[:25]:
        print(f"{r['name'][:44]:44s} F{r['F']:3d} |G|{r['i']['G']:3d}  V {r['vacuus']:3d} (mirror {r['vacuus_mirrors']:2d})  R {r['resonus']:3d} (mirror {r['resonus_mirrors']:2d})  R∩V {r['overlap']:2d}  beyond(i) {r['i']['beyond']}  beyond(iii) {r['iii']['beyond']}")
    print('Resonus inside Vacuus:', [r['name'] for r in res if r['resonus_in_vacuus']][:20])
    print('beyond symmetry (i):', [(r['name'], r['i']['beyond']) for r in res if r['i']['beyond']][:30])
    print('beyond symmetry (iii):', [(r['name'], r['iii']['beyond']) for r in res if r['iii']['beyond']][:30])
    print('grey (needs exact check):', [(r['name'], r['i']['grey'], r['iii']['grey']) for r in res if r['i']['grey'] or r['iii']['grey']][:20])
    print('FINAL ok' if res and not bad else 'FINAL FAIL')
