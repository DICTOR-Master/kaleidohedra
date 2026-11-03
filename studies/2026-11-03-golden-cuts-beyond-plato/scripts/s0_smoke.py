# Smoke test of gcb.py: every solid builds, has the right face counts, unit edges, vertices on one sphere.
import numpy as np, collections, gcb
for name in gcb.PLATONIC + gcb.ARCH + ['elongated square gyrobicupola']:
    V = gcb.platonic(name) if name in gcb.PLATONIC else gcb.archimedean(name)
    F = gcb.faces(V); E = gcb.edges_of(F)
    L = [np.linalg.norm(V[a] - V[b]) for a, b in E]; R = np.linalg.norm(V, axis=1)
    print(f"{name:32s} V={len(V):3d} E={len(E):3d} F={len(F):3d} {dict(sorted(collections.Counter(len(f) for f in F).items()))} "
          f"edge {min(L):.12f}-{max(L):.12f} R {R.min():.12f}-{R.max():.12f}")
for name in gcb.ARCH:
    V, F, orb = gcb.catalan(name)
    print(f"dual of {name:28s} V={len(V)} F={len(F)} face sizes {set(len(f) for f in F)} orbits {dict(collections.Counter(orb))}")
