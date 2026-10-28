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
