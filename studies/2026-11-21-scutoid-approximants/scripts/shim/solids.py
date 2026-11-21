"""Shim for amber.py: everything from the amber-cell sweep's solids.py unchanged, plus one extra core for the approximants study:
'capped_icosidodecahedron' = convex hull of the sweep's icosidodecahedron (edge 1, circumradius phi) and the icosahedron whose vertices
lie on its 12 five-fold axes at radius CAP_LAMBDA * |(0, phi, 1)| (CAP_LAMBDA = rational p/q from the environment), i.e. the
Mackay/Tsai shell pair (30 + 12 atoms).  Exact in Q(sqrt5); the five-fold directions are asserted to be the pentagon normals."""
import importlib.util, os
from fractions import Fraction as Fr
_p = os.path.join(os.environ["SWEEP_DIR"], "solids.py")
_spec = importlib.util.spec_from_file_location("_sweep_solids", _p); _m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
globals().update({k: v for k, v in vars(_m).items() if not k.startswith("__")})
_build = _m.build
def build(name):
    if name != "capped_icosidodecahedron": return _build(name)
    lam = Fr(os.environ["CAP_LAMBDA"]); H = Fr(1, 2)
    ID = _build("icosidodecahedron")
    caps = _m.orbit([(Q(0), PHI*lam, Q(lam))])
    pent = [(n, c) for (f, k), (n, c) in zip(ID["faces"], ID["planes"]) if len(f) == 5]
    assert len(caps) == 12 and len(pent) == 12
    for v in caps:   # each apex on a pentagon normal, outside its plane
        assert any(all(x.sign() == 0 for x in cross(n, v)) and (dot(n, v) - c).sign() > 0 for n, c in pent), "apex on a five-fold axis, outside"
    S = _m.hull(ID["V"] + caps, _m.KIND); S["name"] = name
    return S
