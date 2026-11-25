"""Degree of the t7 apex tangent of the DICTO Yantra and of Kulaichev's yantra.
The flat yantra's great triangle t7 has its apex at the top point O and leg slope u (half-angle arctan u), so its apex angle
alpha = 2 arctan u has tan alpha = 2u / (1 - u^2). u is a root of the integer polynomial of degree 160 (DICTO Yantra; study
2026-11-08-sri-yantra, figures/dicto-yantra-exact-u.txt) or 348 (Kulaichev; study 2026-11-15-yantra-uniqueness, f348); both
copied in study 2026-11-25-plate-harmony, inputs/. Here each polynomial is factored over Z (FLINT), the factor with the root u
(from the plate-harmony Krawczyk boxes, data/yantra.json) is picked by certified complex roots, and
deg Q(tan alpha) >= deg u / 2 because u satisfies the quadratic tau u^2 + 2u - tau = 0 over Q(tau), tau = tan alpha.
Writes data/yantra-degree.json."""
import os, sys, json, re
from flint import fmpz_poly, arb, acb, ctx
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
INP = os.path.normpath(os.path.join(HERE, "../../2026-11-25-plate-harmony/inputs"))
YJ = json.load(open(os.path.normpath(os.path.join(HERE, "../../2026-11-25-plate-harmony/data/yantra.json"))))
ctx.prec = 400


def parse(path):
    s = open(path).read().replace(" ", "").replace("\n", "")
    terms = re.findall(r"([+-]?)(\d+)(?:\*?([a-z])(?:\^(\d+))?)?", s)
    co = {}
    for sg, c, var, e in terms:
        if c == "": continue
        d = int(e) if e else (1 if var else 0)
        co[d] = co.get(d, 0) + (-1 if sg == "-" else 1) * int(c)
    D = max(co)
    return fmpz_poly([co.get(i, 0) for i in range(D + 1)])


out = {}
for key, fn in (("dicto", "dicto-yantra-exact-u.txt"), ("kulaichev", "kulaichev-minpoly-u.txt")):
    f = parse(os.path.join(INP, fn))
    u = float(YJ[key]["u"])
    c, fac = f.factor()
    best = None
    for g, e in fac:
        for r, m in g.complex_roots():
            d = abs(complex(float(r.real.mid()), float(r.imag.mid())) - u)
            if best is None or d < best[0]: best = (d, g.degree(), r)
    assert f.degree() == {"dicto": 160, "kulaichev": 348}[key]
    out[key] = {"poly_degree": f.degree(), "factors": [(g.degree(), e) for g, e in fac], "u": YJ[key]["u"],
                "deg_u": best[1], "root_distance": best[0], "deg_tan_alpha_at_least": best[1] // 2}
    assert best[0] < 1e-20, key
    print(key, out[key], flush=True)
json.dump(out, open(os.path.join(STUDY, "data/yantra-degree.json"), "w"), indent=1)
print("FINAL ok yantra_degree", flush=True)
