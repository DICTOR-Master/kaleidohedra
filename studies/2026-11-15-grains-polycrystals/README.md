# Grains: polycrystals, metamorphic rocks and polar ice (One tissue, three scales, GRAINS stream)

DICTO, 15 Nov 2026: "metamorphic rocks and mineral aggregates, polycrystalline materials", plus polar ice grain fabric. A polycrystal
is a tiling of space by grains, three at an edge and four at a corner; on a section, three at a junction. When it is annealed, the
boundaries move by their curvature, small grains vanish and neighbours exchange. Each system makes its tiling for its own physical
reasons; nothing here assumes or tests any influence of one system on another. Plan and wording: the "One tissue, three scales" plan
(14 Nov 2026). Shared logger: studies/2026-11-15-event-logger, used unchanged (md5 2e2b526f..., recorded in every census file).
Reference values: studies/2026-11-15-tissue-null-models. 2D soap froth is covered by the foam ladder (studies/2026-11-15-interstellar-bubbles)
and is not repeated here; in 2D, froth and grain growth obey the same law (von Neumann).

## VERDICT (15 Nov 2026)
- **2D, curvature-driven grain growth (curved-boundary vertex model, exact events): 1.22 to 1.27 swaps per vanished grain in the
  steady state** (6 runs, 3 seeds, T1 threshold varied 4-fold, 3 or 6 points per boundary; 1001 to 2500 vanishings per window).
  The value is stable to the threshold (eps 0.025 / 0.05 / 0.1: 1.27 / 1.23 / 1.22 in the last window) and to a two-sided
  persistence rule (q = 1%: 1.13 to 1.25; q = 5%: 1.12 to 1.17, partly from censoring at the run's end).
  Published: about 1.34 (Sprague, Patterson, Grandhi 2009, vertex model; wording UNVERIFIED, paywalled) and 3/2 with side-shedding
  (Herdtle & Aref 1992 for froth, via the null-model study). Ours lies 8% below the first and 18% below the second.
- **89 to 95% of these swaps are side-shedding by grains that are about to vanish.** One of the two grains that lose a side is
  smaller than 0.1 <A> in 1.14 to 1.21 swaps per vanished grain. Only 0.06 to 0.14 per vanished grain are "macroscopic". Rutenberg &
  McCurdy give 0.53 macroscopic for froth. This does NOT agree. Their definition of "macroscopic" may not be ours; this is open.
- **Control, partly failed.**
  - Passed:
    - torus Euler V - E + F = 0 in every frame (15,268 frames);
    - every junction triple;
    - logger balance 0 failures, and the negative control caught in every run and stride;
    - von Neumann's law linear in n with zero at n = 5.99 (all runs but one);
    - mean sides 6 exactly.
  - Failed:
    - the slope is 0.76 (K = 3) or 0.87 (K = 6), not pi/3 = 1.047. A uniform slope is a rescaling of time, but three-sided grains
      shrink more slowly than the line;
    - the steady-state spread of sides mu2 is 1.88 to 2.01, against 1.620 for the accurate front-tracking of Mason et al. 2015.
      So this model's topology is about 20% too broad, and its swap counts carry that model error.
- **3D, threshold dynamics (diffusion-generated motion): steady-state mean faces 13.65 to 13.85**, against Mason et al. 13.766 and
  the Fe experiment 13.77 (Zhang 2018). **The control passes.**
  - Per vanished grain, steady windows: contacts gained 2.3 to 2.7, lost 3.9 to 4.8 (2.0 to 2.4 and 3.6 to 4.6 persistent over 5
    frames).
  - The faces of a vanishing grain in its last frame are 5.3 to 5.5 (4.6 to 4.7 when contacts below 4 voxel faces are dropped).
  - **The identity "survivors' net contact change per vanished grain = f_v - <F>/2" holds in the steady windows**: -1.49 vs -1.43,
    -1.66 vs -1.60, -2.18 vs -2.21, -2.12 vs -2.06, -1.52 vs -1.49, -1.43 vs -1.53, -2.11 vs -2.14, -1.91 vs -2.10. It fails in the
    first window (mean faces still falling from the Voronoi start), as it must.
  - Published 3D event counts: only Wakai et al. 2001, with 3.7 face-creations and 13.2 face-eliminations per vanished grain. By the
    identity, a steady state with <F> = 13.77 and tetrahedral vanishing needs a net of -2.88. Wakai's -9.5 therefore describes a
    shrinking-<F> transient, or counts differently.
  - Mason, Lazar et al. (2011, 2015) implement the events but publish no counts.
- **Experiments.**
  - The only free event counts are in a figure (Shahani et al. 2024, Fe DCT). Their data are not public.
  - Public: the Ni HEDM maps of Bhattacharya et al. 2021 (6 states). A pilot here registers 2 of the 5 intervals by orientation
    fingerprints (shift MAD 2-3 um, median misorientation 0.05 deg). The other three intervals carry a rotation of the sample.
  - Grain matching is too noisy for event ratios: 15-17% of the later interior grains have no predecessor, and 29% / 15% of the
    earlier ones vanish, against about 10% published (Peng 2022). The net contacts per "vanished" grain (-0.19, -0.33) are far from
    the identity (2.8, 1.2). So the counts are NOT usable as they stand.
  - Next decided: the authors' own grain correspondences in their face table (data.zip, 0.9 GB, columns "Grain ID t0 / t1").
- **Ice: no time series of the same grains exists** (ice-core sections are cut once per depth). The usable data are single sections
  with grain outlines: EGRIP PANGAEA.933045 (CC-BY) and NEEM PANGAEA.919775.
- **Rocks and analogues: public time-lapse movies exist, but nobody has counted events in them.** These are the octachloropropane
  movies (Means, Albany 13.mov, 0.6 MB) and the Virtual Explorer Vol. 2 camphor and OCP collection. They are low resolution, with
  tens of grains. ELLE (GPL-2) is the reproducible route. No natural-rock time series was found.
- **A prediction from the null-model study (no new computation).** Serial sections through any static 3D grain map are a 2D tissue
  with swaps per birth = <F>/2 - 3 exactly. That is 3.883 for the steady-state grain structure (Mason <F> = 13.766), against
  4.768 for Poisson-Voronoi. Any public 3D EBSD or DCT volume can test it.

## Comparison row (for the One-tissue table)
| system | dimension | driver | swaps per vanished cell | other ratios | source |
|---|---|---|---|---|---|
| polycrystal grain growth, simulation (this study) | 2 | boundary curvature (von Neumann) | 1.22-1.27 (exact T1/T2; 89-95% side-shedding); persistent 1.13-1.25 | vanishing sides at 0.02 <A>: 3 / 4 / 5 = 27 / 68 / 5 %; mu2 1.9 (too broad vs 1.62) | vertex2d runs |
| same, literature | 2 | same | about 1.34 (Sprague 2009, unverified); 3/2 froth with shedding; 0.53 macroscopic froth | experiment (succinonitrile): mean class of vanishing grains about 4.5 | Fradkov 1994; null-model study |
| polycrystal grain growth, simulation (this study) | 3 | mean curvature | contacts gained 2.3-2.7, lost 3.9-4.8 per vanished grain | <F> 13.65-13.85; net = f_v - <F>/2 holds | mbo3d runs |
| same, literature | 3 | same | 3.7 created / 13.2 eliminated (Wakai 2001, not steady by the identity) | <F> 13.766 (Mason 2015); Fe 13.77, F0 3.33 (Zhang 2018) | sources.md |
| Ni anneal, experiment (public) | 3 | same | not usable yet (matching noise of the size of the signal) | interior <F> 10.6-11.0 (resolution) | ni_events.json |
| serial sections of a 3D grain map | 2 (moving plane) | none (static) | 3.883 swaps per birth (exact, from <F>) | Poisson-Voronoi 4.768 | null-model THEORY section 2 |

## 2D results (job grains-2d, FINAL ok; results/v2d/*.census.json)
Windows by grain number. All runs start at 20,000 grains and end at 1500, except the K = 6 run (8000 to 800). Exact counts come
from the simulation's own event list.

| run | T1 / T2 total | T1 per vanished, windows N/2-N/4 / N/4-N/8 / last | persistent q 1% (last) | shedding area < 0.1 <A> (last) | mu2 (last two windows) | von Neumann slope, n0 |
|---|---|---|---|---|---|---|
| K3 eps 0.05 seed 1 | 24,445 / 18,500 | 1.294 / 1.226 / 1.227 | 1.203 | 1.147 | 1.97, 1.92 | 0.758, 5.996 |
| K3 eps 0.05 seed 2 | 24,550 / 18,500 | 1.291 / 1.242 / 1.231 | 1.215 | 1.151 | 1.95, 1.95 | 0.758, 5.992 |
| K3 eps 0.05 seed 3 | 24,622 / 18,501 | 1.277 / 1.226 / 1.222 | 1.204 | 1.143 | 2.01, 1.88 | 0.759, 5.992 |
| K3 eps 0.025 | 23,711 / 18,500 | 1.288 / 1.244 / 1.273 | 1.254 | 1.208 | 1.92, 1.90 | 0.763, 5.993 |
| K3 eps 0.1 | 26,296 / 18,500 | 1.287 / 1.233 / 1.222 | 1.202 | 1.086 | 1.98, 1.90 | measurement broken (-3.8): see below |
| K6 eps 0.05 (8000 to 800) | 9605 / 7200 | 1.315 / 1.272 / 1.184 | 1.134 | 1.129 | 1.94, 1.91 | 0.866, 5.987 |

- **Shedding.**
  - By the second definition, the losing grain vanishes before <A> grows by 5%. Then the shedding swaps are 1.05 to 1.18 per vanished
    grain, and the macroscopic ones 0.10 to 0.19.
  - The first window (from the Voronoi start) has more swaps (1.37 to 1.56) and more macroscopic ones (0.2 to 0.4).
- **Sides of a grain when it first falls below a fixed small area** (seed 1, 18,500 grains):

  | area | 3 sides | 4 sides | 5 sides |
  |---|---|---|---|
  | 0.02 <A> | 27% | 68% | 5% |
  | 0.05 <A> | 12% | 71% | 16% |
  | 0.1 <A> | 5% | 63% | 34% |

  - Rutenberg & McCurdy (froth) give 9 / 84 / 7.
  - In this model only three-sided grains vanish (T2 is applied only to them). Real 4- and 5-sided grains can vanish without
    shedding (Fradkov et al. 1993, succinonitrile films), so a model with only 3-sided T2 sets a floor of mean class 3 at vanishing,
    while the experiment gives about 4.5.
- **The logger on the frames** (frames every 0.2% of N in events):
  - At stride 1 it finds 17,631 swaps against 24,445 exact T1s. Its deaths plus merges are 18,492, against 18,500 T2s.
  - About 35% of the deaths are read as merges, because a shedding swap and the death of the same grain fall into one frame.
  - Swaps at strides 1 / 2 / 4: 17,631 / 16,375 / 14,940.
  - The pair rule and the segment rule agree exactly.
  - The logger is exact in its balance but undercounts swaps by 28% at this frame rate. Every frame-sampled count
    carries that warning; the exact event list does not.
- **eps 0.1 run**: the von Neumann regression is broken (every class shrinks). This is not explained. The topology and counts of
  that run agree with the others.
- **Anomaly counters** (T1 with R = S, T2 with shared outer boundaries, lens collapses, one-sided grains): 0 in every run. No
  two-sided grain arose.

## 3D results (jobs grains-3d on the large machine, grains-3dn on the small one, FINAL ok; results/m3d/)
| run | grains | frames | <F> steady (contact area >= 1 / >= 4 voxel faces) | gained / lost per vanished (amin 1, windows after N0/2) | persistent k5 | f_v last frame | net vs identity |
|---|---|---|---|---|---|---|---|
| 256^3 | 4000 to 393 | 109 | 13.65-13.83 / 13.47-13.57 | 2.69 / 4.18; 2.33 / 4.00 | 2.43 / 3.89; 2.06 / 3.80 | 5.46, 5.25 | -1.49 vs -1.43; -1.66 vs -1.60 |
| 160^3 | 1000 to 150 | 89 | 13.62-13.95 / 13.35-13.83 | 2.59 / 4.11; 2.44 / 3.87 | 2.30 / 3.83; 2.05 / 3.62 | 5.39, 5.40 | -1.52 vs -1.49; -1.43 vs -1.53 |

- Faces at small volume (256^3): mean 7.0 at 0.05 <V>, 8.0 at 0.1 <V>, 9.1 at 0.2 <V>.
- Logger (contacts only; no edges or corners on a voxel grid):
  - balance 0 failures, negative control caught at all strides;
  - most vanishings are clumps, because a grain usually loses several contacts within one frame (about 1 to 1.5% of grains vanish
    per step);
  - contact counts fall steeply with stride: lost 10,740 / 7010 / 3905 at strides 1 / 2 / 4.
  - Only the per-frame contact histories (above) are used for ratios.
- Limits: kernel width sigma = sqrt(0.8 Rbar) (2.5 to 4.2 voxels) against Rbar 10 to 22 voxels; time steps are coarse (about 1% of
  grains per step); 978 voxels (256^3) were moved by the fragment rule in 109 frames.

## Ni experiment pilot (results/ni/ni_events.json; scripts ni_probe.py, ni_register.py, ni_events.py)
- The data: the public Dream.3D voxel maps of Bhattacharya et al., Science 374 (2021) 189. They come from the Grain Boundary Data
  Archive of G. S. Rohrer (CMU), Ni_Reconstructed_D3D.zip, 0.37 GB, six states. We read Dream.3D's own neighbour lists and shared
  areas.
- Registration:
  - The stated origins do not register the states (median misorientation of overlap matches 41 deg).
  - Orientation fingerprints do, for intervals 0-1 and 4-5 (297 and 298 of the 300 largest grains below 0.5 deg; shifts
    (43.4, 45.2, 2.1) and (11.3, -1.9, 11.6) um).
  - Intervals 1-2, 2-3 and 3-4 match only 177, 9 and 94 of 300, so the sample was rotated between them.
- Results:
  - Interior grains: 1917 and 1691. Matched below 1 deg: 2264 and 2129, with 143 and 129 later grains matched twice.
  - Interior later grains with no predecessor: 336 and 299, which should be 0 in grain growth.
  - "Vanished" interior grains: 553 and 255. Their faces are 8.3 and 6.5 on average.
  - Gained / lost contacts among tracked grains: 370 / 474 and 242 / 325.
  - Mean faces of interior grains: 10.6 to 11.0, below 13.77 because of finite resolution, as Shen et al. 2019 found for Fe (12).
- Verdict: the matching noise is of the size of the signal; no ratio is quoted.

## Methods
- **2D (scripts/vertex2d.py).**
  - Curved-boundary vertex model on a torus, written here; the virtual-vertex idea is that of Weygand, Brechet & Lepinoux 1998.
  - K points per boundary; discrete curvature motion; junctions free with three-tension balance; equal arc-length re-spacing.
  - Short boundaries are kept straight (below 4 delta).
  - Exact T1 (hysteresis 2 delta), T2 (three-sided grains below 0.002 <A> or with a side below delta), lens collapse.
  - Start: periodic Voronoi.
  - Frames go to the logger (scripts/census2d.py: strides 1, 2, 4, torus Euler, negative control, persistence and shedding from the
    exact list).
- **3D (scripts/mbo3d.py).**
  - Threshold dynamics of Merriman, Bence & Osher 1994 in the multi-phase form of Esedoglu & Otto 2015 (equal energies: each voxel
    joins the grain with the largest Gaussian-smoothed indicator), with per-grain windows as in Elsey, Esedoglu & Smereka 2009.
  - Written here with numpy/scipy. sigma^2 = 0.8 Rbar, at least 2.5.
  - Fragments are given to their main neighbour at each frame.
  - Contacts are written with areas; census in scripts/census3d.py.
- **Pilot** (job grains-pilot, FINAL ok; results/pilot): K = 3 / 6 / 10 and straight-short threshold 2 / 4. The von Neumann slope
  was 0.70 to 0.86, with n0 = 6.0. K = 3 was chosen for speed, with K = 6 as a check.
- **Persistence.**
  - 2D: two-sided; the old contact had lasted, and the new one lasts, while <A> grows by q.
  - 3D: k frames, about k% coarsening.
  - Tolerances were fixed before counting.

## Files
- Scripts: scripts/ (vertex2d.py, census2d.py, mbo3d.py, census3d.py, ni_probe.py, ni_register.py, ni_events.py; pilot.sh, run2d.sh,
  run3d.sh).
- Results: results/v2d (census JSON, logs, final.json, gzipped stats and exact events); results/m3d; results/pilot; results/ni.
- Frames stay on the compute host: the seed-1 2D frames are gzipped there (0.5 GB), and the rest were deleted after the census.
- Literature: literature/sources.md (every source checked, with marks).

## Next (decided)
1. Ni correspondences from the authors' face table (data.zip), then events for all 5 intervals.
2. A more accurate 2D scheme (the Lazar 2010 corrections, or 4- and 5-sided T2 when area falls below a threshold) to bring mu2 to
   1.62 and the slope to pi/3. Then recount the swaps per vanished grain.
3. Serial-section test of <F>/2 - 3 on a public 3D grain map.
4. Ask DICTO whether the OCP movie count (13.mov) is worth doing by hand.
