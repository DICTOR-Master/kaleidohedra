# Real foams changing over time: what public data exists (scope, no tracing)

16 November 2026. Asked by DICTO for the scutoid study ("can we not observe real bubbles live anywhere... there may be a feed somewhere"). This is a scope check only. No foam was traced, and nothing was downloaded beyond a few file headers and three small CSV tables.

**Conclusion: no open dataset lets us count about 1000 swaps against Rutenberg–McCurdy's 0.53 ± 0.05 macroscopic T1 per T2. Real 3D foam time series are public only as two time steps (40 GB) or ten cropped, down-scaled steps of a sheared foam (pilot only). The only open real 2D coarsening data (Chieco and Durian 2022) are bubble lists without identities, which allow a T2 count but no T1. No live feed exists. The test needs DICTO's own 2D foam cell, sized below from Chieco and Durian's measured rates.**

## Candidates

The swap test means macroscopic T1 per T2 in a coarsening foam at its scaling state. It needs bubble identities across frames and a coarsening foam (T2 events). Sheared foams make T1 events without T2 events, so they cannot give the ratio.

| # | Candidate | What it is | Size, format | Time steps | Voxel / pixel | Licence | Can it test swaps (T1 per T2 vs 0.53)? |
|---|---|---|---|---|---|---|---|
| 1a | FoamQuant raw subset, Zenodo 10.5281/zenodo.15564270 (Mokso 2025) | 3D sheared liquid foam in a rheometer, "two consecutive time steps" of series 2 | 1 file, `tomo_rheoscopy_102_103.tar`, 39.7 GB | 2 | 2.75 µm (paper) | CC BY 4.0 | No: 2 steps, sheared (no T2) |
| 1b | FoamQuant tutorial series, GitHub floschott/FoamQuant_binder, `P1_Raw/` | Cropped, down-scaled tomograms from the same rheometer experiment | 10 BigTIFF files `Raw_001`–`Raw_010.tiff`, 15.9 MB each (159 MB in all), 250 × 252 × 252 voxels, 8-bit | 10 | Not stated for the down-scaled set (source 2.75 µm) | MIT (repository) | No for the ratio (sheared, a few hundred bubbles at most). Yes as a free pilot: real 3D bubbles, true contacts with no shadows, a T1 detector can be checked on it |
| 1c | FoamQuant paper's coarsening albumin foam (Schott et al., J. Synchrotron Rad. 32, 1370, 2025) | 3D coarsening foam, one scan every 20 s for about 28 min, field 3.0 × 5.5 × 5.5 mm | Not deposited | about 84 (derived) | 2.75 µm | Article CC BY | Would be the right kind (coarsening), but the data are not public |
| 2 | Schott et al., Soft Matter 19, 1300 (2023), d2sm01299e | 3D foam flowing through a hopper, up to 50,000 bubbles per scan | No data deposit found; the RSC article page refused automatic fetching (HTTP 403), so the supplement could not be listed | n/a | n/a | Article open access | No: no labelled images found, and flow (no T2) |
| 2b | Schott et al., Nat. Commun. (16 Oct 2025), tomo-rheoscopy, 10.1038/s41467-025-64412-z | Sheared 3D foam, 160 tomograms per run every 3 s, 5,000–33,000 T1 per radial position | Raw data "cannot be deposited"; only 1a and 1b above, plus Source Data tables; the rest on request | 160 (not public) | 2.75 µm | Article CC BY | No: sheared (no T2); full series only on request, and we contact no one |
| 3a | Lambert, Mokso, Cantat, Cloetens, Delannay, Glazier, Graner (cond-mat/0702685; ESRF ID19) | 3D wet-foam coarsening tomography | No data deposit or availability statement found | n/a | n/a | n/a | No public data |
| 3b | Mader et al. 2012 (segmentation and morphology of foam); PRL 104, 248304 (2010; 4D movies of up to 30,000 coarsening bubbles) | 3D foam tomography methods and coarsening | No data deposit found | n/a | n/a | n/a | No public data |
| 3c | Guidolin, Rio, Cerbino, Salonen, Giavazzi, Zenodo 10.5281/zenodo.12759664 (arXiv 2405.10657) | "Movies of coarsening foamed emulsions", analysed by differential dynamic microscopy | 1 zip, 4.74 GB | not listed | not listed | CC BY 4.0 | No: optical views of a 3D foam, so the shadow problem applies (projections make false swaps) |
| 4a | Chieco and Durian, Front. Soft Matter 2022, 10.3389/frsfm.2022.941811 (DataSheets 1–3, Figshare 20479146/49/52) | Real 2D dry foam coarsening: per-frame list of bubble area and side number | 3 CSV files, 4.8 + 7.1 + 5.3 MB; columns time (min), area (mm²), A/<A>, n | 80, 101 and 69 frames, every 5 min; bubbles 1745→728, 3025→688, 2588→846 over 308–703, 167–667 and 178–518 min; cell area about 1.1 × 10⁴ mm² | n/a (areas in mm²) | CC BY 4.0 | T2 yes (fall in bubble number); T1 no (no bubble identities or positions). Gives the rates for the home cell |
| 4b | Kroo, Bull, Prakash, arXiv 2204.00937 ("Active foam", 2D foam under cyclic inflation) | 2D foam, reported about 10³ T1 over 10⁴ frames | No data link on the arXiv page | n/a | n/a | n/a | No public data; also driven, not coarsening |
| 4c | Husain, Nair, Bansal, Mohanty, Zenodo 10.5281/zenodo.14331445 | "Videos of bubble raft" (periphery roughening) | No files listed by the Zenodo API | n/a | n/a | CC BY 4.0 | No: no files reachable, and the subject is the raft edge |
| 4d | Frontiers Figshare 21442821 (foam coarsening in porous media) | One 4.5 MB MP4 | 1 video | n/a | n/a | CC BY 4.0 | No: foam confined in a porous micromodel, not a free 2D foam |
| 5 | ESA Foam-Coarsening experiment on the ISS (Fluid Science Laboratory, run from Brussels since April 2020) | Recorded time-lapses and images of 3D foams coarsening for up to 100 h | Press videos and images only | n/a | n/a | ESA media terms | No: no live feed; views are of a 3D foam (shadow problem); no data release found |

No live webcam or streaming foam or bubble experiment was found anywhere (question 5).

## Best pick

**Best public pick: the FoamQuant tutorial series (1b).** It is real 3D foam with true bubble contacts (no shadows), 10 time steps, 159 MB, MIT licence, already segmented by an open tool (FoamQuant has a T1-detection tutorial). It can check that our swap detector works on real bubbles. It cannot give the T1 per T2 ratio, because the foam is sheared and small.

**For the ratio itself, the only route is DICTO's own 2D cell (below).** Chieco and Durian's run 2 shows a real 2D foam losing 2337 bubbles in 500 min. At 0.48–0.53 T1 per T2, that is about 1100–1250 swaps, the target size.

## Home 2D foam cell

- **Solution:** washing-up liquid in water (a few percent), with 10–20% glycerol for longer-lived films.
- **Cell:** two glass (or acrylic) plates about 15–20 cm square with a spacer about 1 mm thick, sealed at the edges so that the foam neither evaporates nor drains. A thin gap keeps the foam a single dry layer, a true 2D monolayer with no shadows. Fill it with bubbles about 2 mm across: Chieco and Durian's run 2 started at a mean area of 3.5 mm² (3025 bubbles in 1.06 × 10⁴ mm²).
- **Light:** a diffuse panel underneath (an LED panel, or a tablet showing plain white), so the films show as dark lines on a bright ground. A low side light also works.
- **Camera:** a phone fixed on a stand above the cell, with focus and exposure locked, in time-lapse at **one frame every 30 s for 10–12 h** (1200–1440 frames). At 4000 px across a 10 cm field, a 2 mm bubble spans about 80 px.
- **Why these numbers:** Glazier, Gross and Stavans (Phys. Rev. A 36, 306, 1987) showed that a 2D soap froth passes through a transient before its long-time power-law regime. Stavans's review (Rep. Prog. Phys. 56, 733, 1993) describes that scaling state, the state where Rutenberg–McCurdy's 0.53 applies, so count only after the transient. For about 1000 swaps at about 0.5 T1 per T2, about 2000 bubbles must disappear: start with about 3000 bubbles and run until about 700 remain. Chieco and Durian's three runs lost 2.6–5.1 bubbles per minute over 5.7–8.3 h, filmed every 5 min. A frame every 30 s is 10 times finer than that: about 1% of bubbles change their side number between frames, so each bubble changes at most once between frames and every event can be put in time order.

## Sources checked (all on 16 November 2026)

- FoamQuant paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC12416428/ (journal page https://journals.iucr.org/s/issues/2025/05/00/gy5076/)
- FoamQuant docs: https://foamquant.readthedocs.io/en/latest/Jupy_FoamQuant_lf_radius.html, and the docs sources in https://github.com/rajmund/foamquant
- FoamQuant portal entry: https://researchportal.ip-paris.fr/en/publications/foamquant-a-python-package-for-time-resolved-3d-image-quantificat/ (seen in search results only)
- Zenodo record API: https://zenodo.org/api/records/15564270, /12759664, /14331445
- Tutorial data: https://github.com/floschott/FoamQuant_binder (API tree listing and the first 8 KB of `P1_Raw/Raw_001.tiff`)
- Nat. Commun. 2025 data statement: https://pmc.ncbi.nlm.nih.gov/articles/PMC12533193/ ; preprint https://arxiv.org/abs/2411.10338
- Soft Matter 2023: https://pubs.rsc.org/en/content/articlehtml/2023/sm/d2sm01299e (HTTP 403 to automatic fetch; not read)
- Earlier flowing-foam tomography: https://arxiv.org/abs/1503.05785 (search result)
- Lambert et al.: https://arxiv.org/abs/cond-mat/0702685 ; ESRF highlight https://www.esrf.fr/UsersAndScience/Publications/Highlights/2004/Imaging/Ima5 (search results)
- Mader et al. 2012: https://core.ac.uk/download/52310821.pdf (search result)
- Guidolin et al.: https://arxiv.org/abs/2405.10657
- Kroo, Bull, Prakash: https://arxiv.org/abs/2204.00937
- Chieco and Durian 2022 data: https://api.figshare.com/v2/articles/20479146 (and 20479149, 20479152); the three CSVs were counted per frame without being kept; paper https://frontiersin.org/articles/10.3389/frsfm.2022.941811/full (HTTP 500 when fetched)
- Durian group 2D foams: https://arxiv.org/abs/2010.06664 ; https://repository.upenn.edu/physics_papers/285 (search results; no image deposit seen)
- ESA Foam-Coarsening: https://www.esa.int/ESA_Multimedia/Videos/2021/07/Foaming_fluid_science_timelapse (search result)
- Repository searches: Zenodo API ("foam tomography", "foam coarsening", "liquid foam", "T1 foam", "emulsion tomography", "foam rheology", "2D foam", "bubble raft", "Hele-Shaw foam"); Figshare API and Dryad API ("foam coarsening", "2D foam", "foam T1", "foam tomography", "bubble raft"; Dryad 0 hits on each); web searches for the ESRF data portal, MorphoSource and the Materials Data Facility (no liquid-foam time series found; the portals were not searched directly).
- Classic 2D coarsening papers cited from the literature, not re-read here: Glazier, Gross and Stavans 1987; Stavans 1993; Rutenberg and McCurdy (the 0.53 ± 0.05 value as used in the scutoid study).

## 16 Nov: DICTO decision
DICTO: "self bubble study not feasible". The home 2D foam rig is dropped. This route is closed for now; the FoamQuant tutorial series remains only as an optional detector pilot.
