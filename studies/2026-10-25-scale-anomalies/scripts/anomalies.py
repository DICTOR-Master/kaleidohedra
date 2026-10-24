# Scale anomalies of the physical anchors (2026-10-25): testing the MODEL INPUTS (radii, conditions), not new physics.
# Builds on ../../2026-10-25-physical-anchors (contact maps, windows, Shannon radii via the Imperial College transcription).
#  E (exact, sympy): window edges and the octet as exact surds; for every placed compound, the exact radius each ion
#     would need to sit on the nearest window edge (and, Delian, on the octet t = 1/3); exact under the contact model.
#  Q1 error bars: required shifts (A, %) vs the spreads between radius conventions (IR/CR, CN choices, halide CN VI proxy,
#     0.005 A rounding of the tabulated values) and vs the additivity residual against measured lattice constants.
#  Q2 pressure, Q3 temperature, Q4 metastability/nonstoichiometry, Q5 gravity: PHYSICAL ESTIMATES (floats, labelled).
# Every input number carries its source key (see SOURCES); nothing is fitted or invented.
# Output: ../data/raw/anomalies.json, ../data/checks/anomalies-checks.txt
import json, os, math
import sympy as sp
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
PA = os.path.join(HERE, '..', '..', '2026-10-25-physical-anchors', 'data', 'raw')
SH = json.load(open(os.path.join(PA, 'shannon.json')))
COMP = json.load(open(os.path.join(PA, 'compounds.json')))['compounds']
checks, raw = [], {}
def check(name, ok, detail=""):
    ok = bool(ok); checks.append(("PASS" if ok else "FAIL", name, detail))
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""), flush=True)

def sh(el, ch, cn, kind="IR"):
    for r in SH[el]:
        if r["charge"] == ch and r["CN"] == cn:
            return sp.Rational(r[kind])
    raise KeyError((el, ch, cn))

# ---------------- E: exact edges ----------------
r3, r2 = sp.sqrt(3), sp.sqrt(2)
G_LO = r3 - 1                      # golden: big-big contact (Pauling 0.732), rho = r_small/r_big <= 1 by convention
D_LO, D_HI = sp.sqrt(sp.Rational(3, 2)) - 1, (r3 + 1) / 2   # Delian: oct-oct contact / tet-tet contact
OCTET = sp.Rational(1, 2)          # Delian octet stop t = 1/3  <->  rho = 1/2
t = sp.symbols('t', positive=True)
check("E1 Delian octet: t = 1/3 <-> rho = t/(1-t) = 1/2 (exact)", sp.simplify(t / (1 - t)).subs(t, sp.Rational(1, 3)) == OCTET)
check("E2 Delian upper edge (sqrt3+1)/2 = 1/(sqrt3-1) (tet-tet contact <-> Pauling 0.732 inverted)", sp.simplify(D_HI - 1 / (r3 - 1)) == 0)
check("E3 golden lower edge sqrt3-1 equals Delian upper edge inverted", sp.simplify(G_LO * D_HI - 1) == 0)

# ---------------- compounds: site assignment from the anchors study ----------------
SPEC = {  # formula: (loop, (cation el, charge, CN), (anion el, charge, CN), which ion is on 'small'/'tet')
 "CsCl": ("golden", ("Cs", 1, "VIII"), ("Cl", -1, "VI"), "cation"), "CsBr": ("golden", ("Cs", 1, "VIII"), ("Br", -1, "VI"), "cation"),
 "CsI": ("golden", ("Cs", 1, "VIII"), ("I", -1, "VI"), "cation"), "TlCl": ("golden", ("Tl", 1, "VIII"), ("Cl", -1, "VI"), "cation"),
 "TlBr": ("golden", ("Tl", 1, "VIII"), ("Br", -1, "VI"), "cation"),
 "CaF₂": ("delian", ("Ca", 2, "VIII"), ("F", -1, "IV"), "anion"), "SrF₂": ("delian", ("Sr", 2, "VIII"), ("F", -1, "IV"), "anion"),
 "BaF₂": ("delian", ("Ba", 2, "VIII"), ("F", -1, "IV"), "anion"), "CdF₂": ("delian", ("Cd", 2, "VIII"), ("F", -1, "IV"), "anion"),
 "PbF₂ (β)": ("delian", ("Pb", 2, "VIII"), ("F", -1, "IV"), "anion"), "UO₂": ("delian", ("U", 4, "VIII"), ("O", -2, "IV"), "anion"),
 "ThO₂": ("delian", ("Th", 4, "VIII"), ("O", -2, "IV"), "anion"), "CeO₂": ("delian", ("Ce", 4, "VIII"), ("O", -2, "IV"), "anion"),
 "ZrO₂ (cubic)": ("delian", ("Zr", 4, "VIII"), ("O", -2, "IV"), "anion"),
 "Li₂O (anti)": ("delian", ("Li", 1, "IV"), ("O", -2, "VIII"), "cation"), "Na₂O (anti)": ("delian", ("Na", 1, "IV"), ("O", -2, "VIII"), "cation"),
 "K₂O (anti)": ("delian", ("K", 1, "IV"), ("O", -2, "VIII"), "cation"),
}
# alternative CN choices that a reader could defensibly make (all values from the same Shannon transcription)
ALT = {"O": [("O", -2, "IV"), ("O", -2, "VI"), ("O", -2, "VIII")], "F": [("F", -1, "IV"), ("F", -1, "VI")],
       "Li": [("Li", 1, "IV"), ("Li", 1, "VI")]}

def rho_of(rc, ra, small):
    return (rc / ra) if small == "cation" else (ra / rc)

rows = []
for c in COMP:
    f = c["formula"].replace("2", "₂").replace("PbF₂ (beta)", "PbF₂ (β)")
    key = next(k for k in SPEC if k.split(" ")[0] == f.split(" ")[0])
    loop, cat, an, small = SPEC[key]
    rc, ra = sh(*cat), sh(*an)
    rho = rho_of(rc, ra, small)
    # consistency with the anchors study (same radii, same rho)
    assert abs(float(rho) - c["rho_f"]) < 1e-12, (key, float(rho), c["rho_f"])
    r_small, r_big = (rc, ra) if small == "cation" else (ra, rc)   # 'small' = golden small site / Delian tet site
    edges = {"golden": {"window low (like contact, sqrt3-1)": G_LO},
             "delian": {"window low (oct-oct contact, sqrt(3/2)-1)": D_LO, "window high (tet-tet contact, (sqrt3+1)/2)": D_HI,
                        "octet t=1/3 (rho=1/2)": OCTET}}[loop]
    inside = (rho >= G_LO) if loop == "golden" else (D_LO <= rho <= D_HI)
    row = dict(compound=key, loop=loop, r_cation=str(rc), r_anion=str(ra), rho=float(rho), in_window=bool(inside), edges={})
    for name, e in edges.items():
        # exact required radii: move the 'small'/tet ion alone, or the 'big'/oct ion alone
        need_small = sp.nsimplify(e * r_big); need_big = sp.nsimplify(r_small / e)
        mv = {}
        for ion, cur, need in ((("cation" if small == "cation" else "anion"), r_small, need_small),
                               (("anion" if small == "cation" else "cation"), r_big, need_big)):
            d = need - cur
            mv[ion] = dict(need_exact=str(sp.radsimp(need)), need=float(need), shift_A=float(d), shift_pct=float(100 * d / cur))
        # split equally in relative terms: r_small*(1-e), r_big*(1+e): (1-e)/(1+e) = edge/rho
        q = e / rho; eps = (1 - q) / (1 + q)
        row["edges"][name] = dict(edge=float(e), moves=mv, split_rel_pct=float(100 * eps),
                                  rho_gap_pct=float(100 * (rho - e) / e))
    # convention spreads
    spread = {}
    rcC, raC = sh(*cat, kind="CR"), sh(*an, kind="CR")
    spread["CR (crystal radii)"] = float(rho_of(rcC, raC, small))
    for el_tuple in (cat, an):
        for alt in ALT.get(el_tuple[0], []):
            if alt == el_tuple:
                continue
            try:
                r_alt = sh(*alt)
            except KeyError:
                continue
            rc2, ra2 = (r_alt, ra) if el_tuple is cat else (rc, r_alt)
            spread[f"{alt[0]} CN {alt[2]}"] = float(rho_of(rc2, ra2, small))
    # tabulation rounding: radii printed to 0.01 A (0.005 A half-unit) -> worst-case rho band
    lo = rho_of(rc - Fr(1, 200) if small == "cation" else rc + Fr(1, 200), ra + Fr(1, 200) if small == "cation" else ra - Fr(1, 200), small)
    hi = rho_of(rc + Fr(1, 200) if small == "cation" else rc - Fr(1, 200), ra - Fr(1, 200) if small == "cation" else ra + Fr(1, 200), small)
    spread["rounding ±0.005 Å (both ions, worst case)"] = [float(lo), float(hi)]
    if loop == "golden":   # halide CN VI proxy: illustrate with O2- own VI->VIII increment ratio (ESTIMATE, labelled)
        k = sh("O", -2, "VIII") / sh("O", -2, "VI")
        spread["ESTIMATE anion CN VIII via O²⁻ VI→VIII ratio 1.42/1.40"] = float(rho_of(rc, ra * k, small))
    row["spread"] = spread
    rows.append(row)
raw["compounds"] = rows

def within(row, rhos, edge):
    vals = []
    for v in rhos.values():
        vals += v if isinstance(v, list) else [v]
    return min(vals), max(vals)

# checks on Q1
byname = {r["compound"]: r for r in rows}
misfits = [k for k in byname if not byname[k]["in_window"]]
check("Q1a the misfits are exactly UO₂, CeO₂, cubic ZrO₂ (as in the anchors study)", sorted(misfits) == sorted(["UO₂", "CeO₂", "ZrO₂ (cubic)"]), str(misfits))
hi = "window high (tet-tet contact, (sqrt3+1)/2)"
U = byname["UO₂"]["edges"][hi]["moves"]; C = byname["CeO₂"]["edges"][hi]["moves"]; Z = byname["ZrO₂ (cubic)"]["edges"][hi]["moves"]
check("Q1b exact: UO₂ enters the window iff r(U⁴⁺) >= 1.38(sqrt3-1) = 1.0102 Å (cation +0.0102 Å) or r(O²⁻) <= 1.00(sqrt3+1)/2 = 1.3660 Å",
      abs(U["cation"]["need"] - 1.38 * (3 ** .5 - 1)) < 1e-12 and abs(U["anion"]["need"] - (3 ** .5 + 1) / 2) < 1e-12,
      f"cation {U['cation']['shift_A']:+.4f} Å ({U['cation']['shift_pct']:+.2f}%), anion {U['anion']['shift_A']:+.4f} Å ({U['anion']['shift_pct']:+.2f}%)")
for nm in ("UO₂", "CeO₂", "ZrO₂ (cubic)"):
    s = byname[nm]["spread"]["CR (crystal radii)"]
    check(f"Q1c {nm}: crystal-radius convention puts it inside (rho_CR <= (sqrt3+1)/2)", s <= float(D_HI), f"rho_CR {s:.4f}")
li = byname["Li₂O (anti)"]; lo_, hi_ = within(li, li["spread"], None)
check("Q1d Li₂O: the convention spread straddles the octet rho = 1/2 (IR below, CR above)",
      li["rho"] < .5 < li["spread"]["CR (crystal radii)"], f"IR {li['rho']:.4f}, CR {li['spread']['CR (crystal radii)']:.4f}, Li CN VI {li['spread'].get('Li CN VI')}")

# ---------------- additivity residual vs measured lattice constants ----------------
LAT = {"UO₂": (5.47127, "Leinders2015 (547.127 ± 0.008 pm, 20 °C, UO2.000)"),
       "CeO₂": (5.411102, "NIST SRM 674a certificate 1989, Table 3 (information value, σ 0.000097 Å)")}
add = {}
for nm, (a, src) in LAT.items():
    r = byname[nm]; rc, ra = float(sp.Rational(r["r_cation"])), float(sp.Rational(r["r_anion"]))
    d = math.sqrt(3) / 4 * a; aa = a / 2
    # measured-lattice placement (power diagram fixes only r_tet^2 - r_oct^2): t = 1/2 + (8/3)(r_tet^2 - r_oct^2)/a^2
    tm = 0.5 + (8 / 3) * (ra ** 2 - rc ** 2) / a ** 2
    add[nm] = dict(a=a, source=src, d_cat_an=d, sum_radii=rc + ra, residual_A=rc + ra - d, anion_anion=aa,
                   two_r_anion=2 * ra, anion_overlap_A=2 * ra - aa, anion_overlap_pct=100 * (2 * ra - aa) / aa,
                   t_measured_lattice=tm, t_window_max=1 / math.sqrt(3))
raw["additivity"] = add
check("Q1e sanity: measured-lattice placement keeps UO₂ and CeO₂ outside too (t > 1/sqrt3), so the misfit is not a contact-model artefact",
      all(v["t_measured_lattice"] > 1 / math.sqrt(3) for v in add.values()), str({k: round(v["t_measured_lattice"], 4) for k, v in add.items()}))
check("Q1f additivity residual r⁺+r⁻−d is at the 0.01 Å level (|res| < 0.02 Å) for UO₂ and CeO₂",
      all(abs(v["residual_A"]) < 0.02 for v in add.values()), str({k: round(v["residual_A"], 4) for k, v in add.items()}))

# ---------------- Q2 pressure (ESTIMATES) ----------------
# third-order Birch-Murnaghan; K0' = 4 ASSUMED (Duclos 1988 also assumed 4.00 for CeO2)
def bm3(x, K0, K1=4.0):   # x = V/V0
    y = x ** (-1 / 3)
    return 1.5 * K0 * (y ** 7 - y ** 5) * (1 + 0.75 * (K1 - 4) * (y ** 2 - 1))
def x_of_p(P, K0):
    lo, hi = 0.3, 1.0
    for _ in range(200):
        m = (lo + hi) / 2
        if bm3(m, K0) > P: lo = m
        else: hi = m
    return (lo + hi) / 2
K = {"UO₂": (207, "Idiri2004"), "CeO₂": (230, "Duclos1988 (K0'=4 assumed there)"), "ThO₂": (198, "Idiri2004"), "Li₂O (anti)": (90, "Lazicki2006 (±1)")}
TRANS = {"CeO₂": (31.5, "Duclos1988: fluorite→cotunnite-like Pnam at 31.5 ± 1.0 GPa"),
         "Li₂O (anti)": (50.0, "Lazicki2006: antifluorite→anticotunnite at 50 ± 5 GPa"),
         "UO₂": (None, "Idiri2004: still cubic at 69 GPa in that run (sluggish transition to cotunnite type)")}
press = {}
for nm, (K0, ksrc) in K.items():
    r = byname[nm]; rc, ra = float(sp.Rational(r["r_cation"])), float(sp.Rational(r["r_anion"])); d0 = rc + ra
    small = SPEC[nm][3]
    rs, rb = (rc, ra) if small == "cation" else (ra, rc)
    target = (float(OCTET) if nm.startswith("Li") else float(D_HI))
    # model H (homothetic): every length scales the same, rho constant at any P.
    # model A (anion takes all the bond shortening, cation rigid) and model C (cation takes all of it).
    res = dict(K0=K0, K0_source=ksrc, models={})
    for mdl in ("A anion-only", "C cation-only"):
        anion_moves = mdl.startswith("A")
        def rho_at(P):
            dd = d0 * (1 - x_of_p(P, K0) ** (1 / 3))
            r_c, r_a = (rc, ra - dd) if anion_moves else (rc - dd, ra)
            return (r_c / r_a) if small == "cation" else (r_a / r_c)
        drho = (rho_at(0.1) - rho_at(0.0)) / 0.1
        # pressure to reach the target (if the model moves rho the right way)
        Pneed = None
        f0 = rho_at(0) - target
        for Ptry in [i * 0.05 for i in range(1, 4001)]:
            if (rho_at(Ptry) - target) * f0 <= 0:
                Pneed = Ptry; break
        res["models"][mdl] = dict(drho_dP_perGPa=drho, drho_dP_pct_perGPa=100 * drho / rho_at(0), P_to_target_GPa=Pneed,
                                  V_over_V0_at_target=(x_of_p(Pneed, K0) if Pneed else None))
    res["target_rho"] = target
    if nm in TRANS:
        Pt, tsrc = TRANS[nm]; res["transition"] = dict(P=Pt, source=tsrc, V_over_V0=(x_of_p(Pt, K0) if Pt else None))
    press[nm] = res
raw["pressure"] = press
check("Q2a homothetic compression (all fluorite/CsCl positions are special, no free parameter): rho is P-independent (exact: ratio of equally scaled lengths)",
      sp.simplify((sp.Symbol('s') * sp.Symbol('ra')) / (sp.Symbol('s') * sp.Symbol('rc')) - sp.Symbol('ra') / sp.Symbol('rc')) == 0)
pu = press["UO₂"]["models"]["A anion-only"]["P_to_target_GPa"]; pc = press["CeO₂"]["models"]["A anion-only"]["P_to_target_GPa"]
check("Q2b bound (anion-only compression): UO₂ and CeO₂ reach the window below their fluorite→cotunnite pressures",
      pu is not None and pc is not None and pc < 31.5, f"UO₂ {pu} GPa, CeO₂ {pc} GPa")
check("Q2c cation-only compression moves UO₂/CeO₂ further OUT (no pressure reaches the window)",
      press["UO₂"]["models"]["C cation-only"]["P_to_target_GPa"] is None and press["CeO₂"]["models"]["C cation-only"]["P_to_target_GPa"] is None)
pl = press["Li₂O (anti)"]["models"]["A anion-only"]["P_to_target_GPa"]
check("Q2d Li₂O: even the most favourable bound needs more than its 50 GPa antifluorite→anticotunnite pressure to reach the octet",
      pl is None or pl > 50, f"P needed {pl} GPa")
xc = press["CeO₂"]["transition"]["V_over_V0"]
check("Q2e EoS sanity: BM3 (K0=230, K0'=4) gives V/V0 within 0.01 of the ≈0.89 Duclos 1988 gives for the transition", abs(xc - 0.89) < 0.01, f"V/V0 {xc:.4f}")

# ---------------- Q3 temperature (ESTIMATES) ----------------
# IAEA-TECDOC-1496 Table 1 (Martin 1988 recommended), UO2 dL/L273 in %:
TAB = {273: 0.000, 298: 0.025, 1000: 0.730, 1100: 0.837, 1200: 0.948, 2600: 3.238, 2700: 3.484, 3100: 4.624, 3120: 4.688}
def dl(T):
    ks = sorted(TAB)
    for a_, b_ in zip(ks, ks[1:]):
        if a_ <= T <= b_:
            return TAB[a_] + (TAB[b_] - TAB[a_]) * (T - a_) / (b_ - a_)
    raise ValueError(T)
L293 = dl(293)
uo = add["UO₂"]; need_lin = uo["two_r_anion"] / uo["anion_anion"] - 1
temp = dict(source="IAEA-TECDOC-1496 (2006) Table 1, recommending Martin (1988)", dL_293=L293,
            dL_rel_293_to_TS=(1 + dl(2670) / 100) / (1 + L293 / 100) - 1, dL_rel_293_to_Tm=(1 + dl(3120) / 100) / (1 + L293 / 100) - 1,
            T_S=2670, T_m=3120, rigid_ion_linear_expansion_needed=need_lin)
# rigid-ion picture (radii fixed at their ambient values, lattice expands): temperature at which a/2 = 2 r(O2-)
Tx = next(T for T in range(300, 3121) if (1 + dl(T) / 100) / (1 + L293 / 100) - 1 >= need_lin) if need_lin > 0 else None
temp["rigid_ion_T_window"] = Tx
raw["temperature"] = temp
check("Q3a UO₂ linear expansion 293 K → 2670 K (superionic λ transition) is 3.4 % (IAEA table, interpolated)", abs(100 * temp["dL_rel_293_to_TS"] - 3.39) < 0.02,
      f"{100*temp['dL_rel_293_to_TS']:.3f} %; to Tm {100*temp['dL_rel_293_to_Tm']:.3f} %")
check("Q3b rigid-ion bound: the 0.89 % O–O overlap of UO₂ would be removed by heating to ~1.1–1.2 kK (before T_S)", Tx is not None and 1000 < Tx < 1300, f"T = {Tx} K")

# ---------------- Q4 metastability and nonstoichiometry (radius averages = ESTIMATES, Vegard-type) ----------------
rO = sh("O", -2, "IV"); need_rc = float(rO * (r3 - 1))
q4 = {}
rCe4, rCe3 = float(sh("Ce", 4, "VIII")), float(sh("Ce", 3, "VIII"))
x_ce = (need_rc - rCe4) / (rCe3 - rCe4) / 2           # CeO(2-x): 2x Ce3+ per formula unit
q4["CeO2-x"] = dict(r_Ce4=rCe4, r_Ce3=rCe3, need_mean_cation=need_rc, x_needed=x_ce, note="ignores the vacancies themselves")
rU4, rU5_VII, rU6 = float(sh("U", 4, "VIII")), float(sh("U", 5, "VII")), float(sh("U", 6, "VIII"))
q4["UO2+x"] = dict(r_U4=rU4, r_U5_CN7_proxy=rU5_VII, r_U6=rU6,
                   mean_cation_x0_13_U5=(1 - 0.26) * rU4 + 0.26 * rU5_VII, mean_cation_x0_13_U6=(1 - 0.13) * rU4 + 0.13 * rU6,
                   note="oxidation makes the mean cation smaller: rho moves further out; excess O sits near the empty 4b interstices (Wang2014), not on a model site")
rZr, rCa = float(sh("Zr", 4, "VIII")), float(sh("Ca", 2, "VIII"))
q4["ZrO2-CaO"] = dict(r_Zr=rZr, r_Ca=rCa, need_mean_cation=need_rc, y_Ca_needed=(need_rc - rZr) / (rCa - rZr),
                      note="cation fraction of Ca needed by radius averaging alone; real stabilisation mechanism: O vacancies next to Zr (Li1993)")
raw["metastability"] = q4
check("Q4a CeO₂₋ₓ: radius averaging needs x ≈ 0.12 (CeO₁.₈₈) to enter the window", 0.10 < x_ce < 0.13, f"x = {x_ce:.4f}")
check("Q4b UO₂₊ₓ: oxidation (U⁵⁺/U⁶⁺ smaller than U⁴⁺) moves rho further OUT", q4["UO2+x"]["mean_cation_x0_13_U5"] < rU4 and q4["UO2+x"]["mean_cation_x0_13_U6"] < rU4)
check("Q4c cubic ZrO₂: radius averaging with Ca²⁺ needs a Ca cation fraction > 0.5, i.e. not a dilute dopant", q4["ZrO2-CaO"]["y_Ca_needed"] > 0.5,
      f"y = {q4['ZrO2-CaO']['y_Ca_needed']:.3f}")

# ---------------- Q5 gravity (ESTIMATES with exact-defined constants) ----------------
NA = 6.02214076e23; g = 9.80665; Gc = 6.67430e-11; e = 1.602176634e-19; kC = 8.9875517923e9; u = 1.66053906660e-27
M = {"U": 238.02891, "O": 15.999, "Ce": 140.116}
a = add["UO₂"]["a"] * 1e-10
dens = 4 * (M["U"] + 2 * M["O"]) * 1e-3 / (NA * a ** 3)          # kg/m^3
K0 = 207e9
grav = dict(density_UO2=dens)
for h in (0.01, 1.0, 1000.0):
    P = dens * g * h
    grav[f"P_base_{h}m_Pa"] = P; grav[f"strain_{h}m"] = P / (3 * K0)
grav["Fg_over_FCoulomb_U_O"] = Gc * M["U"] * u * M["O"] * u / (kC * 4 * 2 * e ** 2)
P_need = press["UO₂"]["models"]["A anion-only"]["P_to_target_GPa"] * 1e9
grav["column_height_for_P_need_m_crystal"] = P_need / (dens * g)
grav["ESTIMATE depth_for_P_need_km_rock3300"] = P_need / (3300 * g) / 1e3
raw["gravity"] = grav
check("Q5a UO₂ density from a and formula mass ≈ 10.95 g/cm³ (sanity: 4 formula units per fluorite cell)", abs(dens / 1000 - 10.95) < 0.01, f"{dens/1000:.4f} g/cm³")
check("Q5b own weight of a 1 m UO₂ crystal strains it by < 1e-6 (ρ shift < 1e-6 of the 1 % needed)", grav["strain_1.0m"] < 1e-6, f"strain {grav['strain_1.0m']:.2e}")
check("Q5c gravity / Coulomb force between U⁴⁺ and O²⁻ < 1e-30 (distance-independent ratio)", grav["Fg_over_FCoulomb_U_O"] < 1e-30, f"{grav['Fg_over_FCoulomb_U_O']:.2e}")

json.dump(raw, open(os.path.join(HERE, '..', 'data', 'raw', 'anomalies.json'), 'w'), indent=1, ensure_ascii=False)
with open(os.path.join(HERE, '..', 'data', 'checks', 'anomalies-checks.txt'), 'w') as fh:
    for s, n, d in checks:
        fh.write(f"{s} {n}{(' | ' + d) if d else ''}\n")
    fh.write(f"TOTAL {sum(s == 'PASS' for s, _, _ in checks)} PASS, {sum(s == 'FAIL' for s, _, _ in checks)} FAIL\n")
print(f"TOTAL {sum(s == 'PASS' for s, _, _ in checks)} PASS, {sum(s == 'FAIL' for s, _, _ in checks)} FAIL")
