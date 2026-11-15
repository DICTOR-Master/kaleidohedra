# Scutoid lenses: small-aperture arrays for near vision (scope study)

DICTO, 15 Nov 2026 (his own idea, outside the main plan). His observation: distance vision is perfect, but the comfortable near
point is past his wrist; yet in some bright light he can focus a few inches away and see his fingerprint ridges. His idea: lenses
(spectacles, camera lenses) that give the near-vision benefit of a small pupil without losing too much light, using arrays of tiny
apertures or lenslets on a curved surface, where cells packed between two curved surfaces may be forced into scutoids
(Gómez-Gálvez et al. 2018; Mughal, Cox et al. 2018; #104 Scutoids: Layers, Shells and Cycles).

Every source checked is listed in [PRIOR_ART.md](PRIOR_ART.md). Numbers come from data/scutlens.json (script
scripts/scutlens.py, run on the compute machine, FINAL ok, all 7 controls passed; pilot logs in data/).

> **Safety.** Any device worn on or in the eye is a medical device. Nothing here is advice to make or wear home-made spectacles
> or lenses. KAMRA and IC-8 are surgical implants with real complications (below). A camera lens is the safe place to try ideas.

## VERDICT

1. **The observation is the pinhole effect, and it needs a very small aperture.** With a near point of about 60 cm, a finger at
   10 cm is 8.3 D out of focus. Ridge contrast (ridge period 0.48 mm, a typical adult value from memory) at 5-10 cm is at most
   6% for any aperture of 1 mm or more, or reversed (stripes in the wrong place, up to 11%). It reaches about 20% only for an
   aperture near 0.5 mm (table A2). Bright light alone narrows an older pupil to roughly 2-3 mm (typical value, from memory), so the likely extra aperture is the
   eyelids and lashes when squinting. A useful law follows: with a small aperture, blur divided by ridge size tends to
   (aperture ÷ ridge period) as the finger comes closer, and diffraction gets relatively smaller, so moving in costs nothing and
   magnifies. This is the known "pinhole magnifier" (Exploratorium exhibit).
2. **Established: one small aperture deepens focus, and costs light, contrast and comfort.** Depth of focus is about 2β/p
   (β = tolerated blur angle, p = aperture): 1.2 D total at 1 mm, 0.4 D at 3 mm for β = 2 arcmin. Diffraction grows as 2.44λ/p, so the best
   aperture for a defocus ΔD is sqrt(2.44λ/ΔD) (the classical Petzval-Rayleigh pinhole result): 0.82 mm for 2 D, 0.41 mm for 8 D.
   Implants that use it: KAMRA corneal inlay (1.6 mm hole; halos, glare and night-vision symptoms in more than 30%; explants with
   lasting haze, 16 of 22 in one series) and the IC-8 Apthera IOL (1.36 mm hole, FDA 2022, one eye only, monocular contrast
   lower). Pinhole glasses improve near acuity but lower reading speed and comfort (32-presbyope trial, NCT02722291).
3. **New, proved here: no hole array gives exactly one hole in the pupil for every gaze, and the best possible is about 93%.**
   If every disc of the pupil's size held a hole, the holes would be within p/2 of every point (covering radius at most p/2).
   If no disc held two, any two holes would be at least p apart. But every Delaunay triangle with sides of at least d has
   circumradius of at least d/√3, so the covering radius is at least p/√3, which is more than p/2. Contradiction. The
   computation gives the best fractions: hexagonal holes 0.93 (at spacing 0.92-0.96 × pupil), square holes 0.83, random holes
   1/e = 0.37 (check: μe^-μ matched within 0.012). The other 7% is split between no hole (dimming, flicker as the eye moves) and
   two holes (double images: Scheiner's doubling, about 10 arcmin per dioptre of defocus for 3 mm-spaced holes). Colicchia et al. (2008) state the dead-spot versus
   double-image trade-off in words; the bound and the 93% figure are this study's.
4. **Multi-hole arrays do not give more light per image.** Every layout passes 8-12% of a 3 mm pupil's light, about what one
   1 mm hole passes (11%). Extra holes only widen the field of gaze. More light needs more than one hole in the pupil, which
   means several images, and they coincide only for objects in focus. So "small-pupil depth with big-pupil light" cannot be had
   by apertures alone in an eye. In a camera, software can merge the several images: lenslet light-field cameras (Adelson-Wang
   1992; Ng et al. 2005) and wavefront coding (Dowski-Cathey 1995) already do this.
5. **DICTO's geometry, tested.** On a spectacle mask (12 mm in front of the cornea, holes 1 mm, gaze up to 25°):
   - **Bend the sheet round the eye's centre of rotation.** A flat hex sheet bent onto a sphere centred on the eye's turning point
     gives the most even result over gaze (P(one hole) 0.90-0.94 in every gaze band at spacing 2.82 mm, pupil 3 mm). A flat sheet is nearly as good
     at ±25°.
   - **No pentagons needed at spectacle size.** By Gauss-Bonnet, a pentagon carries π/3 of curvature. The 25° gaze cap holds only
     0.56 of a pentagon's worth (the 42° hole cap 1.5), and a 35 mm lenslet zone on a 6 D front surface only 0.12. The icosahedral
     (Goldberg-Coxeter) layout scored lower (0.79-0.91), because its cells vary in size, and a pentagon on the visual axis scored lowest
     (0.73). The golden spiral scored 0.80-0.82, and random holes 0.36-0.44 (control).
   - **One spacing fits one pupil.** Holes spaced for a 3 mm pupil leave 56-67% of gazes with no full hole when the pupil is 2 mm,
     and 30-68% with two holes when it is 4 mm (all non-random layouts). That is the main practical failure, and it is unavoidable with fixed holes.
   - **Scutoids do not form in spectacle lenses.** Hole columns aimed at the eye's centre, between a back surface centred there
     and a front surface of 2, 6 or 10 D base curve or plano, are stretched unevenly by at most 1.15:1. A hexagonal lattice needs
     √3 = 1.73:1 before any neighbour swaps (control: none at 1.70, all 210 row edges at 1.76). So the regular layouts give
     **0 swaps**. The golden spiral and random holes give 1-4 swaps in about 175 edges, at near-tied quadrilaterals only.
     Concentric surfaces give 0 for every layout (control). Columns are plain frusta.
6. **Where the idea can add something real.**
   (a) **Wide-angle curved lens arrays** (artificial compound-eye cameras: Song et al. 2013, about 160°, 180 lenslets, flat array
   stretched into a dome; Jeong, Kim, Lee 2006, about 8,700 hexagonal lenslets on a dome). There the curvature budget is about 5
   pentagons (160° cap), so the defect layout really matters. Placing defects (Goldberg cap versus stretched square or hex grid) is a
   concrete, checkable design problem.
   (b) **A biological prediction for the scutoid thread.** Ommatidia run as columns between the cornea and the basement membrane.
   If both are concentric, the columns are frusta and swap no neighbours. Swaps (scutoids) should appear where the eye is
   unevenly curved (oval or band-shaped eyes) and where facets are irregular (Kim et al. 2016 measure such disorder). No study of
   scutoids in compound eyes was found.
   (c) The exactly-one bound (item 3) is a clean statement for #104's audience and for designers of pinhole-array displays
   (Huang, Wetzstein et al. 2014 use 75 µm holes at 390 µm pitch).

**Status: scoped; one law proved (exactly-one bound), one design rule (bend round the centre of rotation, no defect at spectacle
size), and one negative (no scutoids in spectacle lenses).** Spectacles from hole arrays are not a promising route; a camera with a
curved lens array is.

## Next steps (in order)
1. Camera, not eyewear: a hole-array or lenslet cap on a small camera, with a hemispherical (Goldberg) layout against a stretched
   grid, scored by the gaze-statistics code here turned into field-angle statistics. Paper-only first.
2. Compound-eye scutoids: find open 3D datasets (micro-CT of insect heads) of an oval eye and count cornea-to-basement neighbour
   changes with the #104 swap counter. Literature search first.
3. If wanted for #104: write item 3 as a short theorem with the 93% hexagonal optimum computed exactly (the area covered exactly once
   by discs on the triangular lattice), not by sampling.

## Tables

### A1. One aperture (λ = 555 nm, tolerated blur 2 arcmin)
| aperture mm | depth of focus D (total) | Airy diameter arcmin | light vs 3 mm pupil |
|---|---|---|---|
| 0.5 | 2.33 | 9.3 | 0.03 |
| 1.0 | 1.16 | 4.7 | 0.11 |
| 1.36 (IC-8) | 0.86 | 3.4 | 0.21 |
| 1.6 (KAMRA) | 0.73 | 2.9 | 0.28 |
| 2.0 | 0.58 | 2.3 | 0.44 |
| 3.0 | 0.39 | 1.6 | 1 |

Best pinhole for a defocus: 1.16 mm (1 D), 0.82 (2 D), 0.58 (4 D), 0.41 (8 D), 0.29 (16 D).

### A2. Fingerprint ridges (near point 60 cm, ridge period 0.48 mm); ridge contrast, negative = reversed stripes
| aperture mm | 25 cm | 10 cm | 7.5 cm | 5 cm |
|---|---|---|---|---|
| 3.0 | -0.04 | 0.00 | -0.01 | -0.02 |
| 2.0 | 0.04 | -0.03 | -0.04 | -0.04 |
| 1.5 | -0.09 | 0.06 | 0.06 | 0.05 |
| 1.0 | 0.00 | -0.11 | -0.10 | -0.09 |
| 0.7 | 0.17 | 0.00 | -0.03 | -0.06 |
| 0.5 | 0.19 | 0.23 | 0.21 | 0.19 |

### B. Exactly-one fraction in the plane (holes 1 mm; point holes in brackets)
| layout | pupil 2 mm | pupil 3 mm | pupil 4 mm | best spacing ÷ pupil |
|---|---|---|---|---|
| hexagonal | 0.930 (0.926) | 0.932 (0.933) | 0.928 (0.933) | 0.92-0.96 |
| square | 0.828 (0.824) | 0.827 (0.830) | 0.829 (0.829) | 0.88-0.94 |
| random | max 1/e = 0.368 | | | |

### C. Spectacle mask, pupil 3 mm, gaze up to 25°: P(no hole) / P(one) / P(two or more) / light
Spacing 2.82 mm (best plane spacing for 3 mm), distance viewing:
| layout | holes | none | one | two+ | light |
|---|---|---|---|---|---|
| hex sheet bent round the eye's centre | 163 | 0.03 | 0.93 | 0.04 | 0.116 |
| hex sheet flat | 241 | 0.02 | 0.91 | 0.07 | 0.114 |
| icosahedral, face centre on axis (ν = 11) | 156 | 0.07 | 0.91 | 0.03 | 0.111 |
| icosahedral, pentagon on axis | 101 | 0.27 | 0.73 | 0.00 | 0.085 |
| golden spiral | 152 | 0.10 | 0.82 | 0.08 | 0.114 |
| random (control) | 152 | 0.34 | 0.44 | 0.21 | 0.108 |

Commercial spacing 3.0 mm: bent hex 0.10 / 0.90 / 0.00; flat hex 0.08 / 0.91 / 0.01; icosahedral 0.21 / 0.79 / 0.00; golden
0.17 / 0.80 / 0.03; random 0.48 / 0.36 / 0.16. Reading at 40 cm changes P(one) by -0.06 to +0.02. The pentagon-on-axis layout picked
the same frequency for both spacings, so its rows match. Light per pupil stays at 8-12% throughout.

### D. Neighbour swaps of hole columns, back surface (sphere about the eye's centre) to front surface, holes 3 mm apart
| layout | concentric | 2 D base | 6 D base | 10 D base | plano front | edges |
|---|---|---|---|---|---|---|
| hex bent | 0 | 0 | 0 | 0 | 0 | 186 |
| hex flat | 0 | 0 | 0 | 0 | 0 | 222 |
| icosahedral (both) | 0 | 0 | 0 | 0 | 0 | 177 / 130 |
| golden spiral | 0 | 3 | 2 | 1 | 4 | 173 |
| random | 0 | 2 | 1 | 0 | 2 | 186 |
| largest uneven stretch | 1.00 | 1.12 | 1.06 | 1.03 | 1.15 | |

## Model and assumptions
Typical eye values, assumed and not measured: centre of rotation 13.5 mm behind the cornea, entrance pupil 10.5 mm in front of
it, mask 25.5 mm in front of it (12 mm vertex distance). A hole "counts" when at least half its area projects inside the pupil
(rays parallel to the gaze for distance, from the fixation point for reading). Light = summed projected overlap ÷ pupil area.
Delaunay neighbours on each surface come from a stereographic projection, which keeps circles, so the planar Delaunay equals the spherical one.
Ray optics plus the Airy estimate only: no aberrations of the eye, no Stiles-Crawford effect, no neural factors. Fingerprint
contrast = disc-defocus MTF × diffraction MTF at the ridge frequency.

## Faults on the way (recorded once)
- Pilot 1: the random-holes control used one realization per density, which was too noisy (max 0.39 against 1/e). It now
  averages 8 realizations and checks μe^-μ at every density.
- Pilot 2: numpy booleans broke the JSON writer. Checks are cast to bool. (Its log is not kept: the traceback held machine paths.)
