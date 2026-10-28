# The Hexagonality Law in alloys (DICTO, 10-28) — QUEUED study plan
Status 10-28: set up, not started. Replaces the separate Ti/Zr item (powders folded in).
Cases (DICTO approved order):
1. Ti-6Al-4V: main titanium case. alpha (hcp) + beta (bcc); AM powders and parts full of alpha' martensite with stacking faults
   -> #67 fault shares (hcp faults I1, I2, E = 1 : 2 : 3 layers turned cubic); hydrogen hole space; spherical powders: inside grains
   (faults) and between grains (ordered powder beds = close-packed layers, often random stacking -> #67 Thm 1).
2. Ti-Nb-Zr: the honest limit. beta (bcc, not close-packed): law not directly; stress-induced alpha'' martensite and omega phase are
   layered but not close-packed -> state where the law stops.
3. Mg-Zn-Y LPSO (long-period stacking ordered 10H, 14H, 18R, 24R; Kawamura KUMADAI magnesium): cleanest direct test; hexagonality of
   each LPSO phase -> exact hole shares; solute (Zn, Y) on the faulted layers.
4. Fe-Mn TRIP/TWIP steels and FeMnCoCr high-entropy alloys: fcc -> hcp epsilon-martensite and twinning = #67 faults.
5. Cobalt alloys (CoCrMo implants, Stellite): fcc/hcp switching with faults.
6. Zircaloy (Zr-Sn): hydrides at faults, hydrogen hole space.
Method: library + literature data (lattice parameters per phase, fault energies, LPSO stacking sequences), law predictions from layer
types (Jagodzinski), exact hole shares where a weighted model is meaningful; no claims beyond geometry.

## Progress 10-28: 3. Mg-Zn-Y LPSO (lpso.py) — DONE (structure)
Source read: Egusa and Abe, "Polytypes of long-period stacking structures synchronized with chemical order in a dilute Mg-Zn-Y
alloy", arXiv 1106.4944 (pp. 3-5, Fig. 2 text). LPSO = hcp Mg with a fault every k layers, each fault a local ABCA unit whose two
middle layers are cubic (c) and Zn/Y-enriched (STEM).
Exact sequences and hexagonalities (lpso.py, checked with Jagodzinski's rule):
  10H ABCBCBACAC, h = 3/5; 18R ABCBCBCABABABCACAC, h = 2/3; 14H ABCBCBCBACACAC, h = 5/7; 24R ABCBCBCBCABABABABCACACAC, h = 3/4.
The literature's own composition model is of the law's form: assuming the c layers are Mg85Zn5Y10 and the h layers pure Mg, the
authors give Mg94.0(Zn,Y)6.0, Mg95.0(Zn,Y)5.0, Mg95.7(Zn,Y)4.3, Mg96.3(Zn,Y)3.7 for 10H, 18R, 14H, 24R = 15% x (1 - h) exactly:
composition linear in the hexagonality, each layer type carrying a fixed share (their STEM: c-layer intensity identical in all polytypes).
So LPSO alloys are a real material where a property is ASSUMED and observed to follow the law's form layer by layer; the
Hexagonality Law adds that the geometric hole shares per layer are exactly linear too. Next: which hole kind the solutes prefer
(c vs h shares) needs a model with two atom sizes -> after Ti-6Al-4V.

## Progress 10-28: 1. Ti-6Al-4V, hydrogen sites (hydrogen_sites.py, hydrogen_sites.out) — DONE (geometry)
Explicit coordinates (6x6 in-plane cell, periodic in all three directions, ideal close packing, ball diameter a), six stackings
(3C, 2H, 4H, 6H, Mg LPSO 10H and 14H). Per ball, exact:
  tetrahedral holes 2, octahedral holes 1 (every stacking);
  face-sharing tetrahedral pairs (centres 0.408a apart) = h;  face-sharing octahedral pairs (0.816a apart) = h;
  tetrahedral pairs 0.707a apart (sharing an edge) = 6 - 3h.
All three are the law's form, linear in the hexagonality, exact on all six stackings.
For alpha titanium (a = 2.95 A): the face-sharing tetrahedral pair is 1.20 A apart, far inside Switendick's 2.1 A H-H limit, so at
most one hydrogen per pair: usable tetrahedral sites = 2 - h per ball (hcp alpha-Ti: 1; a cubic layer region: 2). The 0.707a class
is 2.09 A, right at the limit (not used for claims). Real alpha-Ti has c/a = 1.587, not the ideal 1.633: the counts are exact
(topology), the distances shift by ~3% along c.
Consequence (geometry only): a fluorite-type hydride (delta-TiH2, all tetrahedral sites of a cubic metal stacking filled) cannot
form in hexagonal stacking without blocked pairs; it needs locally cubic layers, which faults supply (I1, I2, E turn 1, 2, 3
layers cubic, #67). Consistent with the known hcp -> fcc shift of the metal in hydride formation; literature check next (sources
to be listed) before any claim beyond the counts.
Next: 4. Fe-Mn / high-entropy (fcc -> hcp epsilon by faults), 5. cobalt, 6. Zircaloy hydrides, 2. Ti-Nb-Zr limit.

## Progress 10-28: 4. Fe-Mn TRIP/TWIP and high-entropy alloys (hea_faults.py, hea_faults.out) — DONE (reading)
Standard model of these alloys (Olson and Cohen 1976): gamma_ISF = 2 rho dG(fcc->hcp) + 2 sigma; the intrinsic fault is a two-layer
hcp embryo; low SFE -> epsilon-martensite (TRIP), medium -> twinning (TWIP). Read in the ANNNI form of #68 (Denteneer and van
Haeringen's expressions): rho dG = 2(J1+J3), so 2 sigma = 4 J2 exactly and ESF - ISF = 4(J2+J3).
CONCLUSION: the Olson-Cohen interface energy sigma is the measure of how far a material is from the Hexagonality Law: the law
(two-layer roles) holds iff J2 = J3 = 0, i.e. sigma = 0 and ISF = ESF = 2 TSF = 2 rho dG. (Identification follows at once from the
standard expressions; not claimed as new.)
Data, CrCoNi DFT (Ding, Yu, Asta, Ritchie, arXiv 1806.00718 = PNAS 2018, read pp. 9-13): 2 sigma ~ 18 mJ/m^2 -> J2 ~ 4.5;
random: ISF -42.9, ESF -27.8 (law off by 15); most ordered: ISF 30, ESF 66 (law off by 36); J1 between -14.5 and -1.5.
So high-entropy alloys are the clearest case where the law FAILS: J2 is as large as J1 (local chemical order reaches across layers).
Contrast: SiC volume (#68) J2 ~ 0; Si/Ge J2 ~ J1 too. Status: the law is exact for geometry (hole counts, hydrogen sites, this study
step 1) and for volumes of SiC; energies of metals with low SFE need the second-neighbour term.
Sources checked: arXiv 1806.00718 (Ding et al.); web search "first-principles intrinsic extrinsic stacking fault twin boundary energy
CoCrNi CoCrFeMnNi Fe-Mn ANNNI" (also listed Ikeda et al. Entropy 2018, PMC7513178, not read). Library check to do for
Olson-Cohen 1976 and Denteneer-van Haeringen 1987 before any paper text.

## Progress 10-28: 5. Cobalt (cobalt_faults.py, cobalt_faults.out) — DONE (reading)
Data: Aas, Szunyogh, Evans, Chantrell, arXiv 1304.1353 (read pp. 3, 7): hcp Co fault energies I1 16, I2 48, E 62, T2 39 meV
(40, 122, 160, 100 mJ/m^2), error ~0.2 meV. Cubic layers made (checked from their sequences): I1 1, I2 2, E 3, T2 2 (#67's 1:2:3).
Law test (energy per cubic layer one constant): 16.0, 24.0, 20.7, 19.5 meV -> spread +/-20%: the law's ordering I1 < T2 ~ I2 < E holds,
the ratios are off. ANNNI fit to third neighbours (#68 convention): J1 -12.3, J2 +1.9, J3 +2.9 meV; |J2/J1| 0.15 -> cobalt sits
between SiC (J2 ~ 0, law exact) and CrCoNi (J2 ~ J1, law broken); fit residuals 1.6-3 meV (> stated error: longer-range terms too).
CONCLUSION: cobalt is close to the law: about four fifths of each fault energy is the per-cubic-layer term.
Sources checked: web search "cobalt fcc hcp first-principles stacking fault energies intrinsic extrinsic twin ANNNI J1 J2 polytypes dhcp
energy difference"; arXiv 1304.1353 read; Lizarraga et al. Sci. Rep. 2017 (DOAJ 4f607be5...) listed, not read.
