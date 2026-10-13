# For each 13 kit: its distinct piece shapes (congruent by a rotation, or a mirror image) and each piece's placement
# (rotation + translation of the shape's first copy). Shared by the kit builder; prints a summary when run alone.
import json, sys, itertools, numpy as np
def kabsch(A, B):
    a, b = A.mean(0), B.mean(0); H = (A - a).T @ (B - b); U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return R, b - R @ a, np.abs((A - a) @ R.T + b - B).max()
def signature(V):
    V = np.array(V); c = V.mean(0)
    return (len(V), tuple(np.round(sorted(np.linalg.norm(V - c, axis=1)), 4)))
def match(A, B):
    # same vertex order first (symmetry copies keep it), else pair vertices by distance from the centre and try a few
    R, t, err = kabsch(A, B)
    if err < 1e-4: return R, t
    ca, cb = A.mean(0), B.mean(0); da, db = np.linalg.norm(A - ca, axis=1), np.linalg.norm(B - cb, axis=1)
    # anchor three far, non-collinear points of A; try every candidate image in B with the same distances
    order = np.argsort(-da)[:3]
    cands = [[j for j in range(len(B)) if abs(db[j] - da[i]) < 1e-4] for i in order]
    for js in itertools.product(*cands):
        if len(set(js)) < 3: continue
        R, t, err = kabsch(A[order], B[list(js)])
        if err > 1e-4 or np.linalg.det(R) < 0: continue
        P = A @ R.T + t
        if all(np.min(np.linalg.norm(B - p, axis=1)) < 1e-4 for p in P):
            return R, t
    return None
def classify(pieces):
    shapes, entries = [], []
    for role, V, F in pieces:
        V = np.array(V, float); placed = None
        for si, s in enumerate(shapes):
            if signature(s['V']) != signature(V): continue
            m = match(s['V'], V)
            if m: placed = (si, m[0], m[1], False); break
            M = s['V'] * np.array([-1, 1, 1])            # mirror image of the shape
            m = match(M, V)
            if m: placed = (si, m[0] @ np.diag([-1, 1, 1]), m[1], True); break
        if placed is None:
            shapes.append({'role': role, 'V': V, 'F': F}); placed = (len(shapes) - 1, np.eye(3), np.zeros(3), False)
        entries.append({'shape': placed[0], 'R': placed[1], 't': placed[2], 'mirror': placed[3], 'role': role})
    return shapes, entries
if __name__ == '__main__':
    s = open(sys.argv[1]).read(); D = json.loads(s[s.index('{'):s.rindex('}') + 1])
    for name, d in D.items():
        for kit, pieces in d['views'].items():
            shapes, entries = classify(pieces)
            mir = sum(e['mirror'] for e in entries)
            print(f"{name:9s} {kit:8s} {len(pieces):4d} pieces -> {len(shapes):2d} shapes ({', '.join(s['role'] for s in shapes)}){'  mirrored copies: %d' % mir if mir else ''}")
