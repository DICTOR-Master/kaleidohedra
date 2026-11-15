# Literature: surgery proofs for polygon counts on stackings (15 November 2026)

Free sources only. This builds on LITERATURE.md of study 2026-11-15-ring-counts-stackings, whose sources are not repeated here: Herrero–Ramírez 2013, the ISAACS ring definitions, OEIS A038515 with Guttmann–Jensen 2009, Grimmett 2026, and the ice papers.

## Findings

1. **Whitney twists.** H. Whitney, *2-isomorphic graphs*, Amer. J. Math. 55 (1933). Known via citations.
   - A twist at a 2-vertex separation preserves the cycle matroid.
   - Seen in: arXiv:2607.25410 (genus polynomial of cubic graphs; definition of the twist), arXiv:0811.3859 (matroid isomorphism complexity; twists and Truemper's bound), arXiv:1208.1994 (Katz, a non-Abelian analogue), arXiv:2605.16152 (Whitney's theorem for graphings). Search snippets and abstracts only.
   - Our Theorem A is the same idea across a cut of infinitely many bonds, applied polygon by polygon when two bonds of the cut are used. We credit the idea to Whitney.
2. **Self-avoiding walks on hcp versus fcc.** M. Benito, I. Urrutia, N. Ch. Karayiannis, M. Laso, *Crystals* 13, 1316 (2023); preprint preprints.org 202308.0999.
   - Search-result summary only: both the MDPI page and the preprint page returned HTTP 403.
   - They enumerate SAWs on hcp and fcc (close-packed spheres, coordination 12) and report that the hcp count becomes marginally higher beyond some length. They use enumeration only; no structural explanation is mentioned in the summary.
   - This is the nearest analogue of our question (stacking c versus h, walks rather than polygons, a different network).
3. **Polytype enumeration and notation.** arXiv:2302.01016 (polytypism of layered MX2), and the IUCr papers listed by the search (Acta Cryst. A 2026 cam5016; IUCr Tables C 9.2.1).
   - These concern crystallography and counting polytypes. They contain nothing on cycles.
4. **SAW and SAP enumeration methods.** arXiv:1212.3448 (Guttmann, overview), Slade's lace-expansion enumeration notes, and arXiv:2208.06744 (SAWs and SAPs crossing a domain).
   - None treats diamond versus lonsdaleite or stackings.
5. **Conway–Sloane on polytypes.** *Sphere Packings, Lattices and Groups* treats close-packed stackings (the "Barlow packings"), and Conway–Sloane, *What are all the best sphere packings in low dimensions?* (1995) treats packings and stackings. These are known via citations only, not opened in this study. No cycle counts are known to us from them.
6. **Coordination sequences of polytypes.**
   - Herrero–Ramírez 2013: Ih and Ic first differ at the third shell. Read in the previous study.
   - No coordination-sequence paper found uses a surgery argument.

## Queries (web search, 15 Nov 2026)
1. `self-avoiding polygons lonsdaleite hexagonal diamond lattice enumeration compared diamond`
2. `polytypes stacking sequence cycle counts invariant twist surgery graph "same number of" rings coordination sequences polytypes Conway Sloane "Low-dimensional lattices" polytypes`
3. `"coordination sequences" polytypes close-packed stacking ice Herrero Ramírez polytypes coordination sequence identical first shells`
4. `Whitney twist 2-isomorphism cycles preserved graph flip two-vertex separation cycle matroid`
5. `self-avoiding walks polygons "stacking" polytypes face-centred cubic hexagonal close-packed difference enumeration series hcp fcc`

DICTO's library was not searched for this study.

## Verdict on priority
- **Not found in the sources checked:**
  - a bijective (twist) proof that polygon counts agree across stackings;
  - the local formula Δ = −½ Σ A_root A_far;
  - an explanation of the first differing length.
- **Known and credited:**
  - the twist idea (Whitney 1933);
  - diamond's polygon numbers (Guttmann–Jensen 2009);
  - Ih/Ic ring statistics (Herrero–Ramírez 2013);
  - hcp versus fcc SAW counts differing (Benito et al. 2023, by enumeration).
