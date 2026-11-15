# Prior art: scutoids and neighbour changes in compound eyes (compound-eye scutoids study)

Date: 2026-11-16. Free sources only; nothing was bought. "Full text" means the text was read (by a page reader, so quoted
numbers were checked against its output). "Abstract only" means the full text was not read. "Snippet only" means only a
search-engine summary was seen, so the point should be checked before anyone quotes it. "From memory" means a standard reference
cited without re-reading it here.

Question: has anyone reported scutoid-type ommatidia (a different neighbour set at the cornea and at depth), or traced ommatidia
from the facet layer to the retina in 3D, and are there open 3D eye volumes in which this can be tested?

## Search queries run (web search engine)
1. scutoid ommatidia compound eye (null for scutoids)
2. ODA ommatidia detecting algorithm Currea 2023 micro-CT dataset compound eye
3. compound eye facet lattice defects pentagons heptagons ommatidia hexagonal disorder curvature
4. Taylor Baird micro-CT bumblebee compound eye ommatidial axes skewness interommatidial angle dataset MorphoSource
5. decapod square facets hexagonal transition reflecting superposition eye crayfish facet lattice
6. Kim Biophysical Journal 2016 hexagonal patterning insect compound eye facet area variation defects disorder
7. honeybee compound eye interommatidial angle horizontal vertical anisotropy Seidl Kaiser facet diameter ommatidium length rhabdom
8. Wolff Ready 1991 Drosophila eye development hexagonal lattice ommatidia rotation equator; Ready 1989 cell biology ommatidial lattice
9. Mughal Cox Weaire Burke Hutzler 2018 demonstration of scutoids in quasi-two-dimensional foam cylindrical shell Philosophical Magazine Letters
10. ommatidia shape through depth basement membrane retina mosaic differs from facet mosaic three-dimensional reconstruction compound eye
11. Rigosi honeybee compound eye synchrotron micro-CT 2021 dataset ommatidia segmentation open data
12. dragonfly compound eye facet mosaic acute zone facet rows irregular dislocations Sherk 1978 facet lattice (Sherk not found)
13. "scutoid" retina OR "compound eye" OR ommatidium three-dimensional epithelial packing curvature apico-basal neighbour exchange (null for scutoids)
14. Megaphragma viggianii eye 3D reconstruction volume electron microscopy data availability EMPIAR segmentation

## Pages, databases and files opened
- PMC9992655: Currea, Sondhi, Kawahara, Theobald 2023, Measuring compound eye optics with microscope and microCT images, Commun.
  Biol. (full text, first 100,000 characters). ODA-3D clusters crystalline cones on one fitted surface. It does not trace through
  depth. Axis skew medians: 4.6° (D. mauritiana), 5.9° (D. elpenor), 5.8° (M. sexta), 12.8° (A. mellifera). Data: figshare
  10.6084/m9.figshare.21521142. The bee stack is from Taylor et al. 2018 (MorphoSource project 646).
- figshare API, article 21521142: licence CC BY 4.0; files d_melanogaster_data.zip 7.7 MB, benchmark_3D_data.zip 17,111 MB,
  benchmark_2D_data.zip 2,718 MB, revised_figs.zip 57 MB. The zip's central directory was read by range requests (listing in
  data/benchmark_3D_data_listing.txt); the zip README was read; the four ommatidial_data.csv members were used.
- github.com/jpcurrea/ODA (MIT licence): src/ODA/analysis_tools.py read for the column meanings (x_, dx_, dx) and for theta =
  inclination, phi = azimuth.
- PMC10985371: Paukner et al. 2024, Synchrotron-source micro-x-ray computed tomography for examining butterfly eyes (full text).
  Seven animals, six species; about 600 nm voxels; 14.3 mm³ in all; one point per cone; no tracing through depth, no lattice
  defects reported; cone length 22-72 µm (mean 44.4).
- BossDB API (public read): collection paukner2024, 7 experiments (butterfly_retina_xray_grp02_gw05 ... grp04_gw07), channel
  032019_DP_full_vol, uint8, 600 nm isotropic, 3 hierarchy levels. Frames checked: gw05 1676×2264×1004, gw13 3424×3424×1200,
  gw06 1844×2626×1035, gw07 2975×2975×2162. Stored in the bossdb-open-data bucket. No licence was found in the API records.
- PMC12045625: Makarova et al. 2025, The first complete 3D reconstruction and morphofunctional mapping of an insect eye, eLife
  (first 100,000 characters). Megaphragma viggianii: oval eye (50.6 × 32.6 µm), 29 ommatidia, 478 cells, FIB-SEM. Data on
  waspem-lamina.flatironinstitute.org (no licence named). No neighbour changes with depth or bending are discussed.
- elifesciences.org/articles/103247: the page did not load (script error); PMC was used instead.
- morphosource.org project 0000C0646: the page was fetched, but no dataset licence could be read without logging in.

## Search results used (abstract or snippet only)
- Kim, Cassidy, Yang, Carthew, Hilgenfeldt 2016, Hexagonal patterning of the insect compound eye: facet area variation, defects and
  disorder, Biophys. J. 111:2735 (abstract only). Defects (cells with other than six neighbours) follow facet-size variation.
  Their pupal retina is flat, which avoids curvature effects.
- Butterfly (mourning cloak) corneal nipple arrays (Beilstein J. Nanotechnol. 4:32, 2013; snippet only): 5-7 pairs dominate.
  The authors attribute the disorder to the cornea's convex shape, without showing it.
- NSF grant PHY-1504301 (snippet only): it proposes comparing ommatidial defects with the mechanics of curved patterned surfaces.
- Small-eye mutants with square facets, and square-faceted decapod superposition eyes. Nephrops has a hexagonal dorsal growth
  zone; Oplophorus changes from hexagonal to square facets as it grows (snippets; Hull repository, Naturalis CTZ 1998,
  bioRxiv 786087).
- Wolff & Ready 1991, Development 113:825 and 113:841 (snippets). Cagan & Ready 1989 (cited in the snippets): pigment cells
  build the hexagonal lattice. "Ready 1989" itself was not found. Ready, Hanson, Benzer 1976 (the neurocrystalline lattice) is
  from memory.
- Hayashi & Carthew 2004, Nature (Drosophila cone cells pack like soap bubbles): from memory. It supports the foam/Voronoi reading.
- Honeybee interommatidial angles: minimum 0.9° vertical and 1.6° horizontal (Baumgärtner, as cited in the snippets); frontal
  acute zone minimum 1.3° (snippet).
- Taylor et al. 2019, eLife 8:e40613, bumblebee visual allometry from micro-CT (snippet); Jie, Miettinen & Baird 2023, Insects
  14:670, bumblebee dorsal rim (snippet).
- Gómez-Gálvez et al. 2018, Nat. Commun. 9:2960; Mughal, Cox, Weaire, Burke, Hutzler 2018, Philos. Mag. Lett. 98:358 (record and
  snippets; both already in the lens study).

## Not found
- Any report of scutoids, or of neighbour exchanges between the facet layer and the retina, in any compound eye.
- Any depth-resolved trace of whole ommatidia in an open 3D volume, apart from the 29-ommatidium wasp eye (whose authors do not
  discuss neighbours).
- Sherk 1978 (dragonfly acute zone facet rows) and Ready 1989: not found by these searches.
