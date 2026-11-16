# Yew and conifer cambium: the tissue recorded in one cross-section (One tissue, a new scale)

DICTO, 15 Nov 2026: "yes scope the yew stream". DICTO's idea: a tree cross-section is a frozen space-time record of the cambium,
a sheet of cells. Outward is time (one ring per year). The radial files of tracheids split, end and shift sideways, so the
section records the splits, deaths and swaps of a tissue over centuries. Very old yews (Taxus baccata: regular tracheids, no
resin canals) are a clean case. Plan and wording: "One tissue, three scales" (14 Nov 2026). The shared event logger
(studies/2026-11-15-event-logger) is used unchanged, through an adapter in this folder.

## VERDICT

1. **Feasible for splits and ends, impossible for swaps in one section.** A single cross-section cuts the cambium in a line.
   Seen in it, the tissue is a 1D row of files. Files can split, end or be inserted, but two files can never pass each other,
   so **a swap (the 2-2 move) cannot be seen in one section**. A sideways shift shows only as a file that stops and continues
   one place over (counted here as a "jump"). Swaps of the 2D cambium need serial tangential sections, the method of Bannan
   and Hejnowicz, or a stack of cross-sections up the stem.
2. **Nobody has done this census.** No per-file, per-ring count of files starting and ending was found, nothing on yew, and
   no topological, T1/T2 or scutoid framing. Known counts: Bannan (1950s–60s) gives divisions per cm of xylem increment and the
   survival of new initials (about 13% kept, Chamaecyparis); Bailey (1923) gives net initials round the whole stem (Pinus
   strobus, 724 to 23 100 in 59 years); Hejnowicz gives domain drift (0.7 mm per mm of xylem, Picea). Every source checked is
   listed in [PRIOR_ART.md](PRIOR_ART.md). Software for radial files (RAPTOR, Brunel et al. 2014) throws broken files away as
   errors instead of counting them.
3. **The tracer works on a synthetic section with known events.** Over 3 seeds with the picture straight: splits found
   65 of 71 (recall 0.92, precision 0.92), ends 41 of 44 (0.93 and 0.87). Turned by 7 degrees, recall stays at 0.90 but
   precision falls to 0.80 and 0.60. A section with no events gives zero splits and zero ends. False events cost 0.0008
   (straight) to 0.0028 (turned) per file per cell. That is the noise floor.
4. **Real conifer wood: counts exist but are not yet stable.** In 299 of the 300 patches of the CoLuS data set (several
   conifer species; 1024-pixel patches, a median of 19 files across and 12 to 16 cells deep), file starts plus ends are
   **0.021 per file per cell** from the manual lumen outlines and **0.047** from our own segmentation. Our segmentation more than
   doubles the count, and per-patch counts from the two methods correlate only at 0.63. The patches hold less than one ring
   (rings found: 0 in 86 patches, 1 in 148), so outward cannot be told from inward reliably. The two methods agree on the
   direction in only 69% of patches, so **splits and ends cannot be separated in this data**: they come out nearly equal
   (manual outlines: 835 starts with a parent, 780 ends). Bannan's 1.3 divisions per cm of xylem in Douglas-fir works out to
   roughly 0.004 per file per cell (our arithmetic, assuming a radial tracheid width of about 35 µm, from memory). The
   manual-outline rate is 5 times that, so much of it is tracing error or anatomy near rays, not cambial events.
5. **The logger's checks hold throughout.** Each row was drawn as a sphere (construction below), so Euler's formula held in
   every frame and the cell balance at every step, for both methods and both step sizes. No swap was logged, as the
   construction requires. The negative control (one event retyped as a swap) was caught in every patch that had a step with a
   cell change. Net counts are step-independent, as the balance forces. The separate split and end counts fall from step 1 to
   step 4 cells (manual outlines: 907 to 749 splits, 724 to 541 ends), because nearby events merge into clumps.
6. **What would be stable, and the data still needed.** Two counts would be stable:
   - the **net** change in file number per ring (splits + inserts − ends). The balance forces it, and it can be checked against
     the growth of the circumference divided by the tracheid width (Bailey's count);
   - **gross** splits and ends per file per ring, but only from pictures that span several rings, where the ring pattern fixes
     the outward direction, traced from manual-quality lumina, with the synthetic error floor subtracted.

   No open yew picture of that kind was found (Zenodo, EnviDat, TRIA, Wikimedia Commons searched). For old yews the same
   construction gives counts per century once such a picture exists. Next: a multi-ring yew or conifer section. Routes: TRIA
   (WSL; Pinus sylvestris and Larix with ROXAS files, browsable but not scriptable), a request to a quantitative wood anatomy
   lab, or DICTO's own section of a yew.

## Row for the comparison table (plan Section 4)

| Quantity | Conifer cambium, one cross-section (CoLuS, manual outlines) | note |
|---|---|---|
| Mean neighbours per cell | 2 in the row (4 on the sphere drawing: 2 row neighbours + N + S) | exact by construction |
| Swaps per birth or split | 0, not observable | needs serial tangential sections |
| Share of rosette (clump) events | 20.6% at step 1 cell, 20.8% at step 4 | clumps = adjacent events in one step |
| Events per cell lifetime | file starts + ends 0.021 per file per cell (own segmentation 0.047); synthetic error floor 0.001–0.003 | not yet stable: segmentation-dependent, direction unknown |
| Net file change | splits + inserts − ends = net change, exactly | balance forced; the stable count |

## The construction (time is the radial coordinate of one picture)

- **Radial file**: the chain of tracheids laid down by one cambial cell. It is traced by linking each lumen to the nearest
  lumen outward within a band of 0.45 file widths round the stem. Links are one-to-one. Gaps of up to 4 cells are closed when
  the files line up. Chains shorter than 3 cells count as debris.
- **Row at outward position u** (in units of the median radial cell spacing): the files present at u, in their order round
  the stem, between two **guard files**. The guards are two long files whose common radial span is the window, so no file
  can enter or leave through the window's sides. The row is the cambium's line at time u. The rows for increasing u (steps of
  1 and 4 cells) are the tiling over time.
- **Events.** A **split** is a file starting next to a file that runs on, which is its parent: an anticlinal division seen in
  section. An **end** is a file stopping inside the wood: the loss of an initial. An **insert** is a file starting with no
  neighbour that could be its parent. A **jump** is an end and a start within 1.5 cells radially and 1.2 file widths round the
  stem; the two chains are joined and the event is counted as one sideways shift. Starts and ends need traced wood beyond them,
  so a file running off the picture is not counted.
- **For the logger** each row is a sphere. The files form a ring round the equator, closed through one cell X (the wood
  outside the window), with two caps, N and S, for the cambium above and below the section. All corners are triple, and
  V − E + F = 2n − 3n + (n + 2) = 2. A split is the logger's split (lineage given), an end is its merge (the neighbours close
  up) and an insert is a split without lineage. N and S never touch, so a logged swap could only be a tracing error.
- **Direction.** Outward is taken where lumina jump up abruptly, at the latewood to earlywood boundary; through a ring they
  shrink only gradually. With less than one ring in a picture this is unreliable (finding 4).

## Data (credit at the point of use)

- **CoLuS**: Conifer Lumen Segmentation data set, M. Katzenmaier and co-workers. It was used in "Towards ROXAS AI: deep learning
  for faster and more accurate conifer cell analysis", Dendrochronologia (2023), doi:10.1016/j.dendro.2023.126126.
  Zenodo 10.5281/zenodo.15096567 (latest version of record 8369376), **CC BY 4.0**. It has 300 RGB patches of 1024 × 1024
  pixels with manual lumen masks; species are not named in the record. 165 MB, checksum verified. It is kept in data/raw on
  the compute machine and not committed. ROXAS is by G. von Arx and co-workers (WSL).
- **Checked but not used.** Pinus radiata xylem microsections (Zenodo 8006687 and 8006705, CC BY 4.0, 0.48 µm per pixel,
  fields of about 0.8 mm, less than a ring of a fast pine with resin canals). A 50-species wood identification set (Zenodo
  7124060, one 3 GB binary, no yew named). TRIA (WSL): QWA data sets of Larix decidua, L. sibirica, Pinus sylvestris and
  Quercus petraea, offered through an interactive app. EnviDat: QWA tables only, and no Taxus. Wikimedia Commons: no yew
  micrograph series. InsideWood: images not under an open licence. Not one open Taxus baccata section picture was found.

## Files

- scripts/trace_files.py: lumina, radial direction, files, events, rows and the logger adapter. It imports
  ../2026-11-15-event-logger/scripts/eventlog.py unchanged.
- scripts/synth.py: synthetic sections with known splits and ends. Files share their walls; rows are staggered; rings have
  earlywood and latewood; the picture can be turned.
- scripts/eval_synth.py: matches traced events to the truth.
- scripts/pilot_batch.py, scripts/pilot.sh: the pilot (job yew-pilot, FINAL ok, 20 s on 16 processes).
- results/pilot/: summary.json, pilot.log, per-patch JSON (colus/, both methods), synthetic truth and evaluation JSON, and the
  run plan.
- PRIOR_ART.md: every source checked, with the numbers found and their units.

## 16 Nov: DICTO decision
DICTO: "forget the yew sample unless available online". No own sample will be cut. One web search (16 Nov, standard: "serial tangential sections vascular cambium fusiform initials dataset Taxus yew image stack open data") found no open Taxus serial-section stack; closest published material: serial tangential sections of fusiform initials in Zelkova, Robinia and Albizia (J. Wood Sci., https://jwoodscience.springeropen.com/counter/pdf/10.1007/BF00770693.pdf) and work on Thuja occidentalis cited there (figures in papers, no dataset found). Status: PARKED until an online serial-section data set turns up (check Dryad, Zenodo, BioImage Archive when next passing).
