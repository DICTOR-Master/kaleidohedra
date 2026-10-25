# Weaker form: do the HALF VOLUMES of a mixed-stacking octahedral piece equal half-volumes of the cubic / hexagonal pieces?
exec(open("halves.py").read().split("lams = ")[0])
for word, lam in (("ABAC", 0.2083333333333333), ("ABAC", -0.375), ("ABAC", 0.1), ("ABAC", -0.25), ("ABCACB", 0.1)):
    refs = {}
    for rw in ("ABC", "AB"):
        RM, RS = ref[rw]; j = next(j for j, (k, p) in enumerate(RM) if k == "oct"); V = cellV(RM, RS, j, lam)
        refs[rw] = halves(V, RM[j][1][2])[2:] if V is not None else (0, 0)
    M, S = sites_of(word)
    for i, (k, p) in enumerate(M):
        if k != "oct": continue
        V = cellV(M, S, i, lam)
        if V is None: continue
        u, d, vu, vd = halves(V, p[2])
        print(f"{word} λ={lam:+.4f} site {i}: halves {vu:.6f} / {vd:.6f}   ABC halves {refs["ABC"][0]:.6f}/{refs["ABC"][1]:.6f}   AB halves {refs["AB"][0]:.6f}/{refs["AB"][1]:.6f}")
        break
