# Planets: cellular patterns on other worlds as changing tilings (scope study, no tracing)

DICTO, 16 Nov 2026: a new stream of the scutoid / neighbour-swap work ("One tissue, three scales", 14 Nov 2026; #104 Scutoid
Tissues). The swap is the 2-2 move (T1): two cells stop touching and two others start. Lesson of 16 Nov ("that last eye test
doesnt seem to be relevant data"): before any tracing, say what each data set CAN and CANNOT decide. This study does only that.
Counting rules, the event logger and the lessons are those of studies/2026-11-15-event-logger, -earth-plates, -sun-granulation,
-atmosphere-seaice and -tissue-null-models. Nothing here assumes or tests any influence of one body on another.

## VERDICT (16 Nov 2026)

| candidate | public data (free) | swaps countable? | recommendation |
|---|---|---|---|
| 1 Jupiter polar cyclone rings (Juno) | JIRAM calibrated images on PDS (orbits 1-77); per-perijove centres of the 6 southern cyclones, PJ4-PJ30, CC BY 4.0 (Zenodo 6611745) | yes in principle, but 6 (south) or 9 (north) cells and one event in 9 years: an event catalogue, never a rate | GO, small: exact event reading of the south ring |
| 2 Saturn north polar hexagon (Cassini) | Cassini ISS on PDS Rings Node | no: one wave on one jet round one polar vortex, not a tiling | NO-GO |
| 3 Pluto, Sputnik Planitia cells (New Horizons) | LORRI/MVIC global mosaic, 300 m/pixel (USGS, 310 MB GeoTIFF) | no: one epoch (flyby 14 Jul 2015) | side-number statistics only |
| 4 Mars polygonal ground (HiRISE) | HiRISE RDR on PDS; many repeat images | no: topology changes over centuries or longer; repeats show frost and trough change, no new junctions published | side-number statistics only (already begun by others) |
| 5 Sun, supergranulation | hourly HMI magnetograms (FITS) and 15-minute images free without login | possibly, through the magnetic network; belongs to the Sun stream | not here: a lead for the Sun stream |
| 6a Venus cloud-top cells (Akatsuki UVI, Venus Express VMC) | JAXA DARTS, ESA PSA | doubtful: about 2-hour cadence, irregular, stretched cells | NO-GO for now |
| 6b Jupiter north octagon, extra cyclones at corners | JunoCam maps (amateur-processed), JIRAM PDS | insertions only, as for 1 | fold into 1 |

**One pick: the Jupiter south polar ring (candidate 1).** Reasons: it is the only planetary cell pattern with a public, repeated,
cell-resolved time series; the cell centres for 22 epochs are already published as a table (no segmentation step, which was the
main error source in the Sun and cloud studies); the one known topological event is described in a refereed paper with dates;
and the claim it can test is exact and small: whether the ring ever exchanged neighbours (a 2-2 move), and whether the 2019
newcomer was a birth in place or an intruder. What it cannot give: any rate, any ratio to compare with the 4.77 swaps per birth of
the Poisson-Voronoi null model, or anything statistical. The runner-up, Pluto side-number statistics, is a static test of the
Lewis and Aboav-Weaire laws on several hundred cells, not a swap study.

**What Juno actually observed (south).** Mura et al. 2021 (GRL 48, e2021GL094235): "Only once, in 2019, a sixth cyclone joined
the pentagonal structure in the South, but it disappeared after 2 months without merging with the pre-existing cyclones;
disappearance or creation of stable cyclones has never been observed." In the text: in July 2019 CPC1 and CPC5 began to move
apart; a sixth, smaller cyclone appeared in September 2019 in the gap (longitudes 180-270 W); the six occupied the corners of a
hexagon "for a couple of months, until December 2019", when it disappeared without merging with CPC1 or CPC5; their sequence
analysis "suggests that this event was not the joining/exiting of an external cyclone moving poleward/equatorward, but rather the
fast formation/disappearance of a new, small cyclone in the space freed by the moving apart of the two cyclones". Figure 1
caption: appears orbit 22, near-perfect hexagon orbit 23 (Nov 2019), starts to vanish orbit 24, gone in orbit 25 (Feb 2020).
Earlier, Adriani et al. 2020 (JGR Planets 125, e2019JE006098) report a vortex dipole between their CPCs #5 and #6, visible as an
embryo from PJ15, and at PJ18 (12 Feb 2019) "the Southern CPCs appeared to move to a hexagonal shape where the new-born vortex
is joining the previous ones around the central cyclone". Gavriel & Kaspi 2022 mark both PJ18 and PJ23 as intruder epochs.
No paper we found reports a neighbour exchange (2-2 move) among the established cyclones, a merger, or the loss of an
established cyclone, at either pole.

Read as a tiling (cells = regions nearest each cyclone centre on the polar cap): the 2019 event is a cell inserted into the
contact CPC1-CPC5 and later removed, with the ring order otherwise kept. Within the logger's rules an insertion into an edge is a
birth plus a contact loss (CPC1 and CPC5 stop touching; nobody new starts), so it is not a 2-2 move. Light check of the public
table (PJ4-PJ30, 22 epochs): the cyclic order of the five CPCs is 1-2-3-4-5 in every epoch where they were all seen (19 of 22;
PJ5 shows two CPCs, PJ26 and PJ27 four), the polar cyclone stays 1.4-2.7 degrees from the pole and the CPCs 4.2-7.8 degrees. So the
22-epoch table already shows zero swaps among the six tracked cyclones; the intruder itself is not in the table.

## Candidates in detail

### 1. Jupiter polar cyclone polygons (Juno JIRAM and JunoCam)

Prior art (all checked 16 Nov 2026, free copies):
- Adriani et al. 2018, "Clusters of cyclones encircling Jupiter's poles", Nature 555, 216-219, doi:10.1038/nature25491 (known from
  the reference lists of the papers below; full text not read here): discovery, 8 + 1 north, 5 + 1 south, from PJ4 (2 Feb 2017).
- Adriani et al. 2020, "Two-year observations of the Jupiter polar regions by JIRAM on board Juno", JGR Planets 125,
  e2019JE006098, doi:10.1029/2019JE006098; read in full (Caltech copy https://authors.library.caltech.edu/103532/1/2019JE006098.pdf).
  PJ4-PJ18; pentagon "substantially unchanged, with only occasional perturbations"; dipole embryo PJ15, apparent hexagon at PJ18
  (quoted above); outer cyclones "never appeared to last for more than a 53-day perijove pass". Figure data: Mendeley Data
  doi:10.17632/mg2nskjzm2.1, CC BY 4.0 (file list not shown on the page; centre table not confirmed).
- Mura et al. 2021, "Oscillations and stability of the Jupiter polar cyclones", GRL 48, e2021GL094235,
  doi:10.1029/2021GL094235; read in full (https://authors.library.caltech.edu/records/cecxt-hee93). Table 1 lists all south-pole
  observations 2017-2020; the 2019 event as quoted above; "No changes in the number of cyclones or shape of the polar structures
  were observed in four years" apart from it; lifetime of a cyclone above about 20 years at the 5% level (their estimate);
  oscillations pass from cyclone to neighbouring cyclone. NOTE, the paper is not consistent about the duration: abstract "2
  months", text "about 6 months" and "a couple of months, until December 2019", caption "disappears completely in orbit 25 (Feb.
  2020)"; the caption dates orbit 22 to Aug 2019, their own table to 12 Sep 2019.
- Mura et al. 2022, "Five years of observations of the circumpolar cyclones of Jupiter", JGR Planets 127, e2022JE007241,
  doi:10.1029/2022JE007241 (abstract only via https://authors.library.caltech.edu/117294 and search snippets; the open copies
  at openaccess.inaf.it and Wiley refused automated access): the whole north structure seen again, "almost unperturbed, just like
  the South one"; equilibrium wandering on a few-month scale.
- Mura et al., EGU21-16226, "The evolution of Jupiter polar cyclones", doi:10.5194/egusphere-egu21-16226 (abstract,
  https://meetingorganizer.copernicus.org/EGU21/EGU21-16226.html): south "temporarily changed ... moved in a hexagon for a few
  months, before returning to its original pentagonal shape"; north: "significant hints that the octagonal shape may have been
  lost for a similar period of time". This northern hint is not repeated in Mura et al. 2021 or 2022 as far as we read; treat it
  as unconfirmed.
- NASA/JPL PIA23608, "A sixth cyclone has joined the configuration of circumpolar cyclones at Jupiter's south pole", 12 Dec 2019
  (https://science.nasa.gov/photojournal/a-sixth-cyclone-has-joined-the-configuration-of-circumpolar-cyclones-at-jupiters-south-pole):
  JunoCam, PJ23, 3 Nov 2019; the gap between cyclones 1 and 2 (JunoCam numbering) "varied in extent"; asks whether it will "stay or
  drift out again". News of 12 Dec 2019 (AGU meeting; e.g. Sky & Telescope, https://skyandtelescope.org/astronomy-news/new-cyclone-joins-jupiters-south-pole-club/)
  call 3 Nov 2019 the "22nd science pass": the same pass as PJ23 (counting differs).
- Li, Ingersoll, Klipfel & Brettle 2020, "Modeling the stability of polygonal patterns of vortices at the poles of Jupiter as
  revealed by the Juno spacecraft", PNAS 117, 24082-24087, doi:10.1073/pnas.2008440117 (abstract and news only): shallow-water
  stability set by shielding; too little shielding gives mergers.
- Gavriel & Kaspi 2022, "The oscillatory motion of Jupiter's polar cyclones results from vorticity dynamics", GRL 49,
  e2022GL098708, doi:10.1029/2022GL098708; read in full (https://weizmann.ac.il/EPS/kaspi/sites/EPS.kaspi/files/publications/Gavriel-Kaspi-2022.pdf).
  South only (north too sparse); about 53 days per orbit for the first 30 perijoves; intruders at PJ18 and PJ23. Data and scripts:
  Zenodo 6611745 (CC BY 4.0) holding the Mura 2021 centre table (data/ here).
- Gavriel & Kaspi 2025, "Dynamical constraints on the vertical structure of Jupiter's polar cyclones", PNAS 122, e2503737122,
  doi:10.1073/pnas.2503737122, arXiv:2502.12789 (read): starts from PJ4 positions; mergers only in model runs; nothing on joining
  or leaving.
- Brueshaber, Rogers, Williams, Eichstaedt, Orton & Hansen, EPSC2026-710, "Tracking Jupiter's north polar vortices from JunoCam",
  doi:10.5194/epsc2026-710 (abstract): north tracked to PJ73; "Sometimes one or two extra cyclones are seen at corners of the
  octagon"; one, "X", from PJ30 to PJ45, absent or reduced at PJ50, a possible revival PJ58-PJ66; CPCs and polar cyclone "the only
  features that have persisted throughout Juno's mission". No data release stated.
- Rogers, BAA page "Maps of Jupiter's south polar region (JunoCam and ground-based)", 14 Jul 2025 (https://britastro.org/?p=311215):
  southern CPCs "could not be consistently tracked after PJ35" in JunoCam (range and tilt).
- Siegelman, Young & Ingersoll 2022, "Polar vortex crystals: emergence and structure", PNAS (cited by Gavriel & Kaspi 2022; not
  read): theory of the ring as a vortex crystal.

Public data: JIRAM calibrated RDR images (PDS4 bundle juno_jiram_bundle, PDS Atmospheres Node, atmos.nmsu.edu), orbits 1 to 77,
432 x 256 float32 images, 3036 image products in orbit 23 alone (checked 16 Nov: listing and one label read). The labels carry
time but no per-pixel latitude and longitude: mapping needs the public SPICE kernels (NAIF). NASA data, no licence restriction.
JunoCam raw images and community maps (missionjuno.swri.edu; Eichstaedt and Rogers maps), credit required. Centre table PJ4-PJ30
(south): Zenodo 6611745, CC BY 4.0, copied to data/ with credit (Mura et al. 2021 via Gavriel & Kaspi 2022).
Cadence: one look per perijove, about 53 days early in the mission, shorter later (not checked); gaps when the pole is not covered.

CAN decide: the exact neighbour graph of the 6 (south) or 9 (north) cyclones at each perijove; whether any 2-2 move happened
among the established cyclones (in PJ4-PJ30: none, from the table); how to type the 2019 event in the logger (insertion into a
contact and removal: birth and death, not a swap) and the PJ18 dipole; north insertions at octagon corners from PJ30 on, if centres
are measured. CANNOT decide: any rate or ratio (one or two events, at most nine cells, 53-day sampling against events lasting a
few months); anything about the scutoid law beyond "this ring keeps its neighbours"; the PJ31-PJ77 south series without new
centre measurement from JIRAM images (JunoCam fails after PJ35).

Effort: small for PJ4-PJ30 (table in hand; add the intruder centres from the published figures or from JIRAM orbit 18, 22-25
images); medium to extend to PJ77 (SPICE mapping of JIRAM images, centre picking by hand per perijove, 2 poles).

Recommendation: GO, small: log the south ring PJ4-PJ30 with the event logger (frames = spherical-cap Voronoi of the centres,
plus a power-diagram variant weighted by cyclone size), add the intruder for PJ18 and PJ22-PJ25, and write the one-paragraph
result: a cell pattern that kept every neighbour for years, with one insertion and removal. Extension to PJ77 only if DICTO wants
the north insertions too.

### 2. Saturn's north polar hexagon (Cassini)

Prior art: Godfrey 1988 (Voyager discovery; cited in the papers below, not read); Sánchez-Lavega et al. 2014, "The long-term
steady motion of Saturn's hexagon and the stability of its enclosed jet stream under seasonal changes", GRL,
doi:10.1002/2013GL059078 (abstract via search; arXiv:2402.06371): 2008-2014 Cassini ISS and ground-based, period 10 h 39 min 23.01 s,
size and jet unchanged; a vertically trapped Rossby wave. Sánchez-Lavega et al. 2019/2020, arXiv:1909.13849 (search snippet):
amateur vertex positions 2015-2018. Nothing on neighbours: there is one cell.
Public data: Cassini ISS on PDS Rings Node (VICAR images), public. CAN decide: hexagon phase and shape. CANNOT decide: any swap
(one jet, one polar vortex; small vortices inside the hexagon do not tile). Recommendation: NO-GO.

### 3. Pluto's Sputnik Planitia convection cells (New Horizons)

Prior art: McKinnon et al. 2016, Nature 534 (cells 20-40 km, convection; via search and Wikipedia, not read); Trowbridge et
al. 2016, Nature 534 (not read); Buhler & Ingersoll 2017/2018, Icarus, "Sublimation pit distribution indicates convection
cell surface velocities of about 10 cm per year" (abstract, https://resolver.caltech.edu/CaltechAUTHORS:20170921-101750166):
12 297 pits on 7 cells; White et al. 2017 (cited there, not read); Vilella et al. 2017 (https://www.ep.sci.hokudai.ac.jp/~kenny/Articles/Vilella2017b.pdf,
listed by search, not read): network like laboratory convection patterns; Dimitracopoulos 2017, Univ. Maryland undergraduate
poster (https://www.geol.umd.edu/undergraduate/poster/dimitracopoulos.pdf, search snippet): polygon sizes, elliptical shapes.
No side-number, Lewis or Aboav-Weaire statistics of the cells found.
Public data: USGS Pluto New Horizons LORRI/MVIC global mosaic, 300 m/pixel, 8-bit GeoTIFF, 309 806 463 bytes (reachable, checked
16 Nov); highest-resolution LORRI strips (about 80 m/pixel) on PDS Small Bodies Node. Public domain.
CAN decide: side-number distribution, mu2, Lewis and Aboav-Weaire laws on several hundred cells (the plain is about 1000 km across;
cells 20-40 km), against the planar Poisson-Voronoi values of the null-model study. CANNOT decide: any swap or birth (one epoch;
convective overturn takes about 10^5 to 10^6 years by the pit ages). Effort: medium (troughs must be traced; the image is not
uniform in resolution and lighting). Recommendation: side-number statistics only.

### 4. Mars polygonal terrain (HiRISE)

Prior art: HiRISE captions ESP_019669_2450 and ESP_077840_2375 (https://www.uahirise.org/ESP_019669_2450): thermal-contraction
polygons several metres across, troughs deepen over centuries, new polygon sets overprint old ones; Levy et al. 2010, Icarus 206,
229 (abstract via ADS listing): synthesis, polygons in the ice-rich mantle; Saraiva, Bandeira, Antunes, Pina & Barata 2009,
"Polygonal terrains on Mars", Finisterra 44 (87), 71-80 (abstract): automated detection and planned geometric and topological
characterisation (TERPOLI project). NASA PIA release on south polar "Swiss cheese" terrain monitoring: depressions grow over years
(not a tiling with triple junctions). No published change of polygon topology between repeat HiRISE images found.
Public data: HiRISE RDR (PDS, hirise-pds.lpl.arizona.edu, reachable), 25-50 cm/pixel, many repeat and stereo pairs; public.
CAN decide: static side-number statistics at many sites. CANNOT decide: swaps (the network changes over centuries or more; repeats
over 2006-2026 show frost and trough change only). Recommendation: side-number statistics only, and only after reading the
TERPOLI results (they may already give them; the ice-wedge networks were already set aside in the atmosphere-seaice study for the
same reason).

### 5. The Sun beyond granulation

Already in the Sun stream: studies/2026-11-15-sun-granulation (PRIOR_ART.md covers supergranulation; its lead 5 says the JSOC
export needs a registered e-mail). New fact found here, for that stream: hourly HMI line-of-sight magnetograms (hmi.M_720s FITS,
24 per day) and 15-minute 4k JPEG continuum and magnetogram images are listed free without login under jsoc1.stanford.edu/data/hmi/
(checked 16 Nov); Dopplergrams are not. The magnetic network outlines supergranules, so a network-based tiling over days may be
possible without registration. Not repeated here; recorded as a lead for the Sun stream.

### 6. Other planetary or lunar cell patterns with time-resolved public data

- Venus cloud-top cells: small (under 1000 km) cellular structures at low latitudes in 365 nm images; Akatsuki UVI about every
  2 hours (Yamazaki et al. 2018, Earth Planets Space, doi:10.1186/s40623-017-0775-3, via search); Suda & Imamura, JpGU 2022
  PPS05-06, and Matsui & Imamura, SGEPSS 2024 R009-23 (abstracts, via search): cells stretched poleward, temporal change studied.
  No cell-neighbour statistics found. Data: JAXA DARTS (Akatsuki), ESA PSA (Venus Express VMC), public. Cells are irregular and
  the cadence is coarse; NO-GO for swaps until a cell lifetime is known to exceed several frames.
- Jupiter north octagon: ancillary cyclones at the corners (Brueshaber et al. EPSC2026, above): insertions into the ring, same
  logic and data as candidate 1; fold into it.
- Moon, Mars clouds, Titan, the ice giants: no cell pattern with a public time series found in this scan (not searched in depth).

## Files

- data/Mura_2021_pj_info_sp.txt, Mura_2021_sp_lat.txt, Mura_2021_sp_lon.txt: south-pole cyclone centres (planetocentric latitude,
  west longitude; columns CPC1-CPC5 then the polar cyclone) and perijove dates, PJ4-PJ30. Source: Mura et al. 2021, GRL 48,
  e2021GL094235, as supplied in Gavriel & Kaspi 2022, Zenodo 6611745, CC BY 4.0. Copied unchanged.
- No scripts: the light check (cyclic order per epoch) was a few lines run on the compute machine and is described above.

## Version

Scope study of 16 Nov 2026 (Claude for DICTO). Faults met: the INAF open-access server, Wiley and one university repository
refused automated downloads (403); the same papers were read from Caltech and Weizmann copies where available; Mura et al. 2022
was read only as an abstract.

## Leads

1. Jupiter south ring PJ4-PJ30 through the event logger, with the PJ18 and PJ22-25 intruder (the pick).
2. If wanted: JIRAM PJ31-PJ77 centres by SPICE mapping, both poles; then the north corner insertions (cyclone "X", PJ30-45).
3. Pluto side-number statistics from the 300 m mosaic (static, Lewis and Aboav-Weaire).
4. Sun stream: supergranule tiling from free hourly HMI magnetograms (no registration).
