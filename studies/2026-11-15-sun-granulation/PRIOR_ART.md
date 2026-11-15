# Prior art: neighbour swaps in convection cell patterns (free sources only, 15 Nov 2026)

"Abstract only" = the abstract was read, not the full paper. "Memory" = recalled, not checked today. Paywalled pages were not
bought or read.

## Solar granulation and supergranulation: are neighbour swaps counted?

None found. The tracking literature counts events of single cells (appearance, fragmentation, merging, disappearance) and family
trees, and the network literature measures single-frame statistics. No source found counts neighbour exchanges (the 2-2 move,
T1 in foam language) between granules or supergranules.

- Malherbe, Roudier, Stein & Frank 2018, arXiv:1804.01870 (abstract only): trees of fragmenting granules (TFG), Hinode/SOT against
  a Stein-Nordlund simulation; horizontal velocities, magnetic fields, TFG evolution. No neighbour exchange in the abstract.
- Roudier, Malherbe, Rieutord & Frank 2016, arXiv:1604.04118 (abstract only): TFG and supergranulation evolution.
- Roudier, Malherbe, Stein & Frank 2019, arXiv:1901.03255 (abstract only): TFG and deep downflows in an MHD simulation. Its text
  (search snippet) says the authors could not obtain the simulation's intensity cubes "owing to excessive data volume".
- Malherbe & Roudier 2025, arXiv:2503.09161 (abstract only): TFG in the formation of the supergranular pattern.
- Lemmerer, Hanslmeier, Muthsam & Piantschitsch 2017, A&A 598, A126, arXiv:1611.06786 (abstract only): granule tracking with
  lifetime, fragmentation, size, intensity, vertical velocity in simulations and observations. No neighbour exchange in the abstract.
- Rieutord, Roudier, Roques & Ducottet 2007, arXiv:0707.1991 (abstract only): CST granule segmentation and tracking; tracking is
  hampered by fragmentation.
- Del Moro et al. 2015, arXiv:1501.05444 (abstract only): passive tracers advected by a deforming Voronoi network of granules.
- Schrijver, Hagenaar & Title 1997, ApJ 475, 328, doi:10.1086/303528 (title and metadata via Crossref; abstract seen by the event
  logger study): granulation and supergranulation patterns compared with Voronoi tessellations. Single frames.
- Hagenaar, Schrijver & Title 1997, ApJ 481, 988, doi:10.1086/304066 (metadata): cell sizes of the chromospheric network.
- DeRosa & Toomre 2004, ApJ 616, 1242 (abstract via the event logger study): more than 3000 supergranules tracked; merging and
  fragmentation in more than half of the histories. Single-cell events.
- Rieutord & Rincon 2010, Living Rev. Solar Phys. 7, 2, doi:10.12942/lrsp-2010-2; Rincon & Rieutord 2018, Living Rev. Solar Phys.
  15, 6, doi:10.1007/s41116-018-0013-5 (metadata only): supergranulation reviews; to read for any supergranule topology statistics.
- A&A 282 (1994), "Solar granulation and statistical crystallography" (snippet only, via the event logger study): the
  Aboav-Weaire law holds for granules. Authors not yet confirmed.

## Laboratory convection (Bénard-Marangoni, Rayleigh-Bénard): known, qualitatively

- Cerisier, Rahal & Rivier 1996, Phys. Rev. E 54, 5086-5094, doi:10.1103/PhysRevE.54.5086 (Crossref metadata; abstract text seen
  only as fragments on an author page): topological analysis of Bénard-Marangoni cells; the elementary transformations
  "neighbor switching process, cell disappearance or creation, and cellular division"; Lewis's, Aboav-Weaire's, Peshkin's and
  Lemaître's laws satisfied, fair for pentagons, hexagons, heptagons. Whether rates of neighbour switching are given is NOT known
  (paywalled, not read).
- Cerisier, Occelli, Pérez-García & Jamond 1987, J. Phys. 48, 569, doi:10.1051/jphys:01987004804056900 (metadata): structural
  disorder in Bénard-Marangoni convection.
- Cerisier, Rahal & Azuma 2007, J. Phys. Conf. Ser. 64, 012004, doi:10.1088/1742-6596/64/1/012004 (metadata): pattern dynamics in
  a medium aspect ratio container.
- A stochastic-geometry study of the hexagon-square transition in surface-tension-driven convection (TU Dresden portal, snippet):
  Aboav-Weaire holds at all times, also with fourfold vertices.
- So neighbour switching in convection cells has been described in the lab (Cerisier and co-workers). A count of swaps per split
  or per cell lifetime was not found in the free sources.

## Foams and epithelia (reference vocabulary)

- Weaire & Rivier 1984, Contemp. Phys. 25, 59, doi:10.1080/00107518408210979: soap froths and cellular patterns; T1 (neighbour
  exchange) and T2 (three-sided cell vanishes) as the elementary moves; Lewis and Aboav-Weaire laws.
- Aboav 1970, Metallography 3, 383; Weaire 1974, Metallography 7, 157; Lewis 1928, Anat. Rec. 38, 341 (memory; the laws used in
  our tables).
- A 1999 EPL paper extending the Aboav-Weaire law to T1 neighbours in dry froth (doi:10.1209/epl/i1999-00138-7; search snippet).
- Gómez-Gálvez et al. 2018, Nat. Commun. 9, 2960 (memory): scutoids; neighbour exchanges along the apico-basal axis of curved
  epithelia. A recent arXiv paper on the geometry of T1 transitions in epithelia (2504.16765, snippet).
- A froth-physics paper (arXiv cond-mat/9709227, snippet) lists solar granulation among cellular networks whose topology changes
  by T1 and T2 moves, without counting them for the Sun.

## Data sources checked

- Hinode Science Data Centre Europe, sdc.uio.no/vol/simulations (public Bifrost runs): USED (en024048_hion, qs024048_by3363).
- Stein (Michigan State) simulation pages: the live site was unreachable; the archived 2012 page (web.archive.org) lists emergent
  intensity slices of 48 and 96 Mm runs at 1 min cadence, but the data directories were not archived. Not used.
- MURaM: no public time series found (MPS project page, papers 2202.09332, 2511.19048, 1201.1103: data from the authors only).
- SDO/HMI (supergranulation): the JSOC export needs a registered e-mail address; not used (no personal details sent to outside
  services). Supergranules are not reached in this study.
- Hinode SOT/BFI, SST, DKIST observations: not attempted in this pass (calibration needed; a simulation was available).

## Searches with no relevant hit

arXiv API (abstracts): granulation AND "T1"; granul* AND "neighbor exchange"; granules AND topolog* AND network; "Rayleigh-Bénard"
AND "T1"; convection AND cells AND "neighbor switching"; granules AND "Aboav"; "Lewis" AND "Aboav" AND convection; granul* AND
"topological changes"; "cellular pattern" AND convection AND topolog*. Web: "T1" neighbour exchange solar granulation; Bénard-
Marangoni T1 T2 Lewis Aboav; Rivier Cerisier Bénard-Marangoni neighbour switching frequency; granule tracking number of neighbours.
Blocked or not used: NASA ADS (HTTP 405 for the logger study), scite.ai (HTTP 405), publisher full texts (paywalled).
