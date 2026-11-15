# Quasicrystal extinctions and twisted silence: one phenomenon or two? (15 Nov 2026)

## Verdict

**The two are partly the same phenomenon, and the pilot separates the parts.** The test is in the right setting.

1. **The forced part is the same phenomenon (proved here; the proof is short).** Treat a point set on S³ as a "crystal" in the group SU(2). Its "Bragg peaks" are the Peter–Weyl blocks End(V_k), one block per harmonic degree k, and a set's tone at degree k is its Fourier coefficient there. The twisted action x ↦ a·x·σ(a)⁻¹ is translation by t(a) = a·σ(a)⁻¹ followed by a point operation. Here t is a 1-cocycle, and it is a coboundary exactly when σ is induced by conjugation in SU(2), that is, exactly when the action fixes a point of S³. For 2I and its Galois-type outer automorphism σ, no point is fixed. So the action is **nonsymmorphic** in the same sense as a space group with screws or glides. In crystals, a peak is extinct when its little group acts on the one-dimensional Fourier space with a nontrivial phase, e^{2πiΦ_g(k)} ≠ 1. On S³, a block is extinct when the symmetry has no invariant vector on it, i.e. Hom(π∘σ, π) = 0, i.e. π is not σ-stable. That is the same rule with a matrix in place of the phase (Schur's lemma). Degrees 1 and 2 of the golden 20-set X (and of every twisted class of 2I) are silent because V₁ = 2 and V₂ = 3 are swapped by σ with 2′ and 3′. Those are the systematic absences of this nonsymmorphic "S³ space group". For nonabelian G the link is exact both ways: the twisted action fixes no point of S³ ⇔ degree 1 is forced silent. The crystal analogue is weaker: I2₁2₁2₁ and I2₁3 are nonsymmorphic and still show no systematic extinction (Rabson and Fisher 2001).
2. **The new part, degrees 5 and 7, is not a systematic absence.** Neither the symmetry group of X (S5, order 120) nor its space group forces these zeros. A different X-shaped orbit of the same S5 kills only 1 and 2 (control G below). The crystallographic counterpart is the **special-position (Wyckoff) reflection condition**. The textbook case is diamond's "forbidden" 222 reflection: atoms on the special site 8a of Fd3̄m cancel reflections with h+k+l = 4n+2, which the space group does not forbid. In both cases the cancellation comes from where the generating point sits. A further structural point, derived here from Fable's table and Brauer's defect-zero theorem (quoted, not re-read): the 6-dimensional block that carries degrees 5 and 7 has 3-defect zero in the order-240 group 2I⋊⟨σ⟩, since 240 = 2⁴·3·5. So its character vanishes on every element of order divisible by 3. X is the twisted class over the S5 cycle type (3,2), of order 6. The zero is therefore a cancellation of the phases 1, ω, ω² of an order-3 element in X's site group, which is the same kind of mechanism as a special-position extinction. F's zero (4s on cycle type (4,1)) is not of this kind (Schur's odd-class rule).
3. **In real Bragg diffraction, silent degrees do not make extinct peaks.** Let X decorate every point of a golden cut-and-project module. Then each peak is the window factor times the motif form factor F_X(k), and no peak vanishes for X, −X, F or the control G (pilot, below). A silent degree removes one angular multipole of F_X at every |k|. It does not zero F_X at any point. The diffraction signature it does leave is angular rigidity of the Friedel-odd part. For X, the odd moments satisfy p₅(u) = p₃(u) and p₇(u) = (7/8)·p₃(u) in every direction u (unit radius; observed to 1e-13, not yet proved exactly). So Im F_X(k) keeps the shape of the degree-3 harmonic up to order |k|⁸.

**At true strength:** the forced silences (1, 2) are the same phenomenon as nonsymmorphic extinctions, transported from the translation group Rⁿ to the group S³. The new twisted silences (5, 7) are the analogue of special-position extinctions, not of space-group extinctions. Neither kind appears as an extinct Bragg peak in an icosahedral or H4 quasicrystal decorated by the set. The Galois map enters both subjects in the same structural place: physical × internal = twisted diagonal g ↦ (g, g★). But the silence lives in the group's Fourier transform, not in the translation Fourier transform of the quasicrystal.

## Pilot (exact sets, float64, compute machine, 0.5 s, FINAL ok)

`scripts/qx_pilot.py`, log `data/qx_pilot.log`, 9 CHECK lines, all OK.

| set | points | silent degrees n ≤ 12 | Bragg peaks with F = 0 (of 16 488) | smallest nonzero |F|/|S| |
|---|---|---|---|---|
| X | 20 | 1, 2, 5, 7 | 0 | 4.5e-3 |
| −X | 20 | 1, 2, 5, 7 | 0 | 4.5e-3 |
| F | 30 | 1, 2, 3, 6 | 0 | 4.5e-3 |
| R (A4 roots) | 20 | 2 and all odd | 72 | 1.4e-3 |
| G control, perms of (1.7,1.7,1.7,0.6,0) | 20 | 1, 2 | 0 | 5.6e-3 |

- The Bragg set is k = m/(4φ²), with m in the Z[φ]-module spanned by X (rank 8 over Z), coefficients in [−3,3]⁸, and windows |m| ≤ 6, |m★| ≤ 1.5. This is a stand-in for the true Fourier module L° of the H4 cut-and-project scheme (Elser and Sloane 1987). L° was not constructed. The conclusion does not depend on that choice, because zeros of a complex 20-term exponential sum have codimension 2 and a countable module meets them only through arithmetic coincidence.
- R's 72 zeros come from antipodality (F_R is real, so its zero set has codimension 1). They do not come from silence: X and −X are not antipodal and show none.
- Part 2: p₅/p₃ and p₇/p₃ are constant over 400 directions for X (relative spread 1e-13). For G they are not constant (spread about 100). For F, p₃ vanishes identically.

## Literature (free sources; every source checked)

Opened today:
- Mermin, "Crystallography without periodicity" (arXiv cond-mat/9207028): the extinction rule (gk = k and Φ_g(k) ∉ Z ⇒ ρ(k) = 0) and gauge equivalence of phase functions. It has nothing on icosahedral groups, star maps or Galois.
- Rabson and Fisher, "Fourier-space crystallography as group cohomology", Phys. Rev. B 65, 024201 (arXiv cond-mat/0105036): phase functions as H¹ classes with coefficients in Hom(L, R/Z), extinctions from gauge invariants, and the exceptions I2₁2₁2₁ and I2₁3.
- Fisher and Rabson, "Applications of group cohomology to the classification of Fourier-space quasicrystals" (arXiv math-ph/0105010, abstract): extinctions are physical manifestations of nonzero homology classes.
- A. Yamamoto, Wyckoff positions of icosahedral quasicrystals (NIMS / Hokkaido web page): there are 11 icosahedral space groups (Fm35, Fmxy35, Im35, Pm35, Pmxy35, F235, F235₁, I235, I235₁, P235, P235₁), five of them nonsymmorphic, with translation parts in 6D. "P5₃32" is not an icosahedral symbol. The nonsymmorphic icosahedral elements are the 5₁ screws and the "xy" glides of 6D.
- Search snippets only, not read: Rhyner, "Crystallography of quasicrystals; application to icosahedral symmetry", Phys. Scr. T25 (1989) 367 (3 Bravais classes, 2 point groups, 11 groups, the nonsymmorphic ones with systematic extinctions); Rev. Mod. Phys. 64, 3 (1992) record (Mermin's icosahedral review, behind paywall; errata 64, 635; 64, 1163; 66, 249); diamond 222 "forbidden" reflection (Renninger; h+k+l = 4n+2 rule; bonding-charge papers 1967 and 1977).
- Not reachable today: the Bilbao Crystallographic Server WYCKPOS page for group 227 (certificate and parse errors), where the 8a special condition would have been confirmed.

Cited from memory, not opened: International Tables A (general and special reflection conditions); Rabson, Mermin, Rokhsar and Wright, Rev. Mod. Phys. 63, 699 (1991), axial groups; Rokhsar, Wright and Mermin, Phys. Rev. B 37, 8145 (1988); Levitov and Rhyner, J. Phys. France 49, 1835 (1988); Dräger and Mermin, "superspace groups without the embedding" (PRL 1996); Lifshitz, Fourier-space notes (Tel Aviv, 1995; the page is listed in search); Baake and Grimm, *Aperiodic Order* Vol. 1 (2013), the cut-and-project scheme, the star map ★ and the peak amplitude as the Fourier transform of the window at k★; Elser and Sloane (1987), the H4 quasicrystal from E8 via icosians; Brauer's defect-zero theorem; Schur (1911).

## What a full study would establish

**Theorem to prove (proposition, placeholder wording).** For a finite G ⊂ SU(2) and an automorphism σ, call the twisted diagonal the "space group" of the S³-crystal, with translation cocycle t(a) = a·σ(a)⁻¹. Then:
- (i) The forced silent blocks are exactly the non-σ-stable G-irreducibles, and the forced silent degrees are the k all of whose constituents are non-σ-stable.
- (ii) A forced silence exists iff the cocycle class is nontrivial (σ is not induced by SU(2)) iff degree 1 is forced. This is the S³ analogue of the Rabson–Fisher homology criterion, without the I2₁2₁2₁ exceptions.
- (iii) The site-dependent ("special-position") silences of a twisted class over g come from blocks of p-defect zero for primes p dividing the order of g, plus Schur's odd-class rule. A complete list should follow for 2I.

**First job.** Exact Q(√5) script, pure Python, small:
- Run (i) to (iii) over all binary polyhedral groups and all their automorphisms, and confirm that only 2I with its Galois-type σ has forced degree-1 silence.
- List every special silence with its prime-defect label.
- Prove p₅ = p₃ and p₇ = (7/8)·p₃ exactly on X.

Destination: the twisted silence paper, as its "crystallography" section (Concordance route). This is a scope note, not a release.
