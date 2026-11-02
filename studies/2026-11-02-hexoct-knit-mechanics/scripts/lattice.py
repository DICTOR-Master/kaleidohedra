# Knitted HexOct lattice (DICTO proposed, spec studies/2026-11-02-knitted-hexoct): nodes, links and in-sheet members.
# Node spacing a = 1, sheet spacing d = sqrt(2/3). In-plane periodic rectangular cell nx x ny*sqrt(3)/2 (ny even),
# sheets k = 0..N-1 at z = k d. Optionally periodic through the thickness (word must then be cyclic).
import numpy as np
R3 = np.sqrt(3.0); D = np.sqrt(2.0 / 3.0)
OFF = {'A': (0.0, 0.0), 'B': (0.5, R3 / 6), 'C': (0.0, R3 / 3)}  # C = 2(e1+e2)/3 reduced into the cell

def word_from_labels(labels):
    """labels[k-1] = 'c' or 'h' for sheets k = 1..N-2; sheets 0,1 = A,B."""
    w = ['A', 'B']
    for L in labels:
        w.append(w[-2] if L == 'h' else ({'A', 'B', 'C'} - {w[-2], w[-1]}).pop())
    return ''.join(w)

def labels_of(word, cyclic=False):
    n = len(word); out = []
    for k in (range(n) if cyclic else range(1, n - 1)):
        out.append('h' if word[(k - 1) % n] == word[(k + 1) % n] else 'c')
    return ''.join(out)

def build(word, nx=6, ny=6, zper=False):
    assert ny % 2 == 0
    N = len(word); Lx, Ly = float(nx), ny * R3 / 2; Lz = N * D
    X = []; sheet = []
    for k, P in enumerate(word):
        ox, oy = OFF[P]
        for j in range(ny):
            for i in range(nx):
                X.append(((i + 0.5 * (j % 2) + ox) % Lx, (j * R3 / 2 + oy) % Ly, k * D)); sheet.append(k)
    X = np.array(X); sheet = np.array(sheet)
    per = np.array([Lx, Ly, Lz if zper else np.inf])
    members = []  # (i, j, shift vector s: X_j + s - X_i is the member vector, kind 'link'|'sheet')
    for a in range(len(X)):
        for b in range(a + 1, len(X)):
            dk = int(sheet[b] - sheet[a])
            if (dk % N not in (0, 1, N - 1)) if zper else abs(dk) > 1: continue
            v = X[b] - X[a]; s = np.zeros(3)
            for c in range(3):
                if np.isfinite(per[c]): s[c] = -np.round(v[c] / per[c]) * per[c]
            v = v + s
            if abs(np.linalg.norm(v) - 1) < 1e-9:
                members.append((a, b, s, 'sheet' if abs(v[2]) < 1e-9 else 'link'))
    return dict(X=X, sheet=sheet, N=N, word=word, members=members, cell=(Lx, Ly, Lz), nx=nx, ny=ny, zper=zper)

def check(lat):
    """every node: 6 in-sheet members; 3 links to each neighbouring sheet that exists; forward/backward pattern as spec."""
    X, sh, N = lat['X'], lat['sheet'], lat['N']
    up = np.zeros(len(X), int); dn = np.zeros(len(X), int); ins = np.zeros(len(X), int)
    for a, b, s, k in lat['members']:
        if k == 'sheet': ins[a] += 1; ins[b] += 1; continue
        dz = X[b, 2] + s[2] - X[a, 2]
        if dz > 0: up[a] += 1; dn[b] += 1
        else: up[b] += 1; dn[a] += 1
    zper = lat['zper']
    for n in range(len(X)):
        assert ins[n] == 6, ins[n]
        assert up[n] == (3 if (zper or sh[n] < N - 1) else 0), (n, up[n])
        assert dn[n] == (3 if (zper or sh[n] > 0) else 0), (n, dn[n])
    return True

SEQ_LABELS = {  # 12 sheets -> 10 interior labels (sheet 1 at the bottom ... sheet 10 at the top)
    '3C': 'c' * 10, '2H': 'h' * 10, '4H': 'hc' * 5, '6H': 'hcc' * 3 + 'h',
    'Fibonacci': 'chcchchcch',      # Fibonacci word abaababaab with a -> c, b -> h
    'Graded c-top/h-bottom': 'hhhhhccccc', 'Graded h-top/c-bottom': 'ccccchhhhh'}
PERIODIC_WORDS = {'3C': 'ABC' * 4, '2H': 'AB' * 6, '4H': 'ABCB' * 3, '6H': 'ABCACB' * 2}

if __name__ == '__main__':
    for name, lab in SEQ_LABELS.items():
        w = word_from_labels(lab); assert labels_of(w) == lab
        lat = build(w); check(lat)
        nl = sum(1 for m in lat['members'] if m[3] == 'link'); ns = len(lat['members']) - nl
        print(f"{name:24s} word {w}  labels {lab}  nodes {len(lat['X'])} links {nl} sheet members {ns}")
    for name, w in PERIODIC_WORDS.items():
        lat = build(w, zper=True); check(lat)
        print(f"{name:24s} 3D-periodic word {w} cyclic labels {labels_of(w, True)} members {len(lat['members'])}")
