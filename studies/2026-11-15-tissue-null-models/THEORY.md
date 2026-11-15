# Tissue null models: derivations

Notation: F cells (faces of the 2D tiling), E edges (contacts), V vertices (junctions). Triple junctions only: 3V = 2E.

## 1. Euler identities for triple-junction tilings (sphere, plane)

**Sphere.** V − E + F = 2 and 3V = 2E give E = 3(F − 2), V = 2(F − 2), sum of sides Σn = 2E = 6F − 12, mean sides
⟨n⟩ = 6 − 12/F. **Plane** (a periodic patch, i.e. a torus): V − E + F = 0, so E = 3F, V = 2F, ⟨n⟩ = 6 exactly.
A large free patch in the plane: ⟨n⟩ = 6 − (12 − boundary term)/F → 6.

Because 3V = 2E holds before and after every event, every event obeys ΔE = 3ΔF, ΔV = 2ΔF, Δ(Σn) = 6ΔF.

| event | ΔF | ΔE | ΔV | side counts |
|---|---|---|---|---|
| birth (inverse T2: a triangle appears at a junction) | +1 | +3 | +2 | new cell n = 3; the three cells round the junction +1 each |
| death (T2: a triangle vanishes) | −1 | −3 | −2 | the three neighbours −1 each |
| split (division: a new edge across an n-cell) | +1 | +3 | +2 | n → n₁ + n₂ = n + 4 (n₁, n₂ ≥ 3); the two cells at the ends of the new edge +1 each |
| merge (an edge removed, two cells fuse) | −1 | −3 | −2 | n₁ + n₂ → n₁ + n₂ − 4; the two cells at the ends of the removed edge −1 each |
| swap (T1, neighbour exchange) | 0 | 0 | 0 | two cells −1, two cells +1 |

**Forced** (Euler): over any interval, F_end − F_start = births + splits − deaths − merges; with it ΔE, ΔV, Δ(Σn) and the mean
⟨n⟩. **Free**: the number of swaps (T1 leaves F, E, V unchanged, so Euler sees nothing), and how the net change is shared between
births and splits (and between deaths and merges). In a generic smooth evolution only triangles vanish; a 4- or 5-sided cell
vanishes as T1 side-shedding followed by a T2 of a triangle (the "T2(4)", "T2(5)" of foam papers are such composites).

So **swaps per birth is not fixed by topology in 2D alone.** It becomes fixed when the 2D tissue is a moving section of a
3D (or 4D) cell complex, Section 2: then the third dimension's Euler relation fixes it.

## 2. Sweeps: a 2D tissue as the moving section of a 3D tessellation

Sweep a normal 3D tessellation (four cells at every vertex, four edges at every vertex, three cells at every edge) by
parallel planes in a generic direction. The section is a 2D triple-junction tissue; it changes only when the plane passes a
vertex, and in exactly one of three ways by the number i of the vertex's four edges that go down (the same proof as #104
Theorem 1; i = 0 and i = 4 cannot occur inside a tessellation because the four edges positively span space):
i = 1 birth, i = 2 swap, i = 3 death.

**Counting per period** (periodic tessellation, C cells and V vertices per period):
* every cell has exactly one lowest and one highest vertex: births h₁ = C, deaths h₃ = C;
* h₂ = V − 2C swaps;
* each 2-face has one lowest vertex, and a vertex of index i is the lowest vertex of C(4 − i, 2) faces: F₂ = 3C + h₂ = V + C
  (the Euler relation of the 3-torus, V − E + F₂ − C = 0 with E = 2V);
* mean faces per cell k̄ = 2F₂/C, so

> **swaps per birth = h₂/h₁ = V/C − 2 = k̄/2 − 3**, exactly, for every generic direction and every normal 3D tessellation.

Swap participations per cell lifetime (each swap changes the side numbers of four cells) = 4h₂/C = 2k̄ − 12.

**Closed version (#104 Theorem 1).** For a simple 4-polytope (its boundary is a 3-sphere tessellated by f₃ cells, with f₂
2-faces and f₀ corners): h₁ = f₃ − 4, h₂ = f₀ − 2f₃ + 6 = f₂ − 3f₃ + 6, so

> h₂/h₁ = (f₂ − 3f₃ + 6)/(f₃ − 4) = (f₃(k̄ − 6)/2 + 6)/(f₃ − 4) → (k̄ − 6)/2 as f₃ grows,

with k̄ = 2f₂/f₃ the mean number of neighbours of a cell. The +6 and −4 are the sphere's Euler terms (the sweep starts and
ends with a tetrahedral section). 120-cell: k̄ = 12, (120·3 + 6)/116 = 366/116.

**One dimension up** (3D tissue as a section of a normal 4D tessellation, five edges at every vertex): births = deaths = C,
gains (i = 2: a 2-3 flip, one contact made) h₂ and losses (i = 3: a 3-2 flip, one contact lost) h₃ with
h₂ = h₃ = V/2 − C exactly (count lowest vertices of edges: Σ(5 − i)h_i = E = 5V/2). Contact changes per birth = V/C − 2.

## 3. Poisson–Voronoi values

Typical Poisson–Voronoi cell (Meijering 1953; Miles 1970; Møller 1989, *Adv. Appl. Prob.* 21, and *Lectures on Random
Voronoi Tessellations* 1994; Okabe, Boots, Sugihara, Chiu, *Spatial Tessellations* 2000): mean vertices per cell
E f₀ = (2^{d+1} π^{(d−1)/2} / d²) · Γ((d²+1)/2)/Γ(d²/2) · [Γ(d/2 + 1)/Γ((d+1)/2)]^d:
d = 2: 6; d = 3: 96π²/35 = 27.0709 (faces 2 + 48π²/35 = 15.5355); d = 4: 1430/9 = 158.889 (we evaluated the formula; Delaunay
simplices per seed 286/9). Vertices per cell per period V/C = E f₀/(d + 1).

* 3D Poisson–Voronoi swept by a plane (= 2D power diagram whose weights change linearly in time, below):
  **swaps per birth = 24π²/35 − 2 = 4.76773**; swap participations per cell lifetime 96π²/35 − 8 = 19.0709.
* 4D Poisson–Voronoi swept by a 3-space (= 3D power diagram with linear weights): contact changes per birth
  286/9 − 2 = 268/9 = 29.7778, half gains, half losses (134/9 each).
* Random simple 4-polytope (polar of n random points on the 3-sphere; its boundary is a spherical Poisson–Voronoi
  tessellation): h₂/h₁ → 24π²/35 − 2 from below as n grows.

**Why the sweep is a moving power diagram.** The section z = t of the Voronoi tessellation of seeds (xᵢ, yᵢ, zᵢ) is the 2D
power (Laguerre) diagram of the points (xᵢ, yᵢ) with weights −(zᵢ − t)²; weight differences
(zⱼ − t)² − (zᵢ − t)² are linear in t. Sections of Voronoi tessellations are Laguerre tessellations (Lautensack and Zuyev
2008, *Adv. Appl. Prob.* 40; Okabe et al. 2000).

## 4. Moving Voronoi with a fixed number of seeds

Seeds that move but never appear or vanish: every Voronoi cell stays non-empty, so births = deaths = 0 and the only events
are T1 swaps (2D) or 2-3 / 3-2 flips (3D). Swaps per birth is infinite: this null model is the opposite pole to the sweep.

* **Linear seed motion** (constant velocities, components N(0, s²)): the swap rate per unit time is finite and is a
  number per cell per mean spacing ℓ = ρ^{−1/d} of rms seed displacement. Computed two ways (time-stepped simulation, and
  an integral over the typical Poisson–Delaunay simplex: a flip is a seed crossing an empty circumsphere, and outside an
  empty circumsphere the seeds are an unconditioned Poisson field).
* **Brownian seed motion**: a Brownian path crosses a circumcircle infinitely often near each crossing, so the number of
  swaps in any time interval is infinite; with frames every Δt the count grows as Δt^{−1/2} (as 1/δ at per-frame rms
  displacement δ). **Any data set with jittery boundaries has frame-rate-dependent T1 counts.** The net count (contacts
  present at the end and not at the start) is frame-rate independent and is the quantity to compare.

## 5. Coarsening (2D soap froth, von Neumann law)

dA/dt = κ(n − 6) (von Neumann 1952; Mullins 1956). Cells disappear (T2), and T1s occur both at macroscopic scale and as
side-shedding of small 4- and 5-sided cells just before they vanish. Literature values (no simulation run here; a faithful
froth needs curved films):
* Rutenberg and McCurdy (arXiv cond-mat/0502287, 2005), force-based vertex model, scaling state:
  macroscopic T1 per T2 = 0.53 ± 0.05; cells vanish as triangles 9 ± 2 %, 4-sided 84 ± 2 %, 5-sided 7 ± 2 %.
* Herdtle and Aref 1992 (*J. Fluid Mech.* 241, 233): T1 per T2 = 3/2 including side-shedding T1s.
* Consistency (our arithmetic): side-shedding adds n − 3 T1s per vanishing n-cell, 0.84·1 + 0.07·2 = 0.98 per T2, and
  0.53 + 0.98 = 1.51 ≈ 3/2.
* Experiments: Glazier, Gross and Stavans 1987 (*Phys. Rev. A* 36, 306); Stavans 1993 (*Rep. Prog. Phys.* 56, 733): most
  topological changes are T2s.
