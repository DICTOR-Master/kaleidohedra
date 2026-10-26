# The Icosaxes Hexa: Cage, Shell and Orb

## 1. Introduction
DICTO's idea, conceived in 2026, posits that the inspiration for this work is not the shape itself but the dynamic process of pieces passing into one another until they close, a concept first explored in the DICTO Hexa (#18). This paper extends that concept to icosahedral symmetry, utilizing the golden-split pair of the Icosaxes and Unborn Axes (#48) to construct a new stellated jewel network.

## 2. Theorem: The Three Golden Stops
**Theorem.** Twenty Icosaxes, positioned on the corners of a dodecahedron and rotated by the icosahedral symmetry carrying $(1,1,1)$ to each corner, exhibit three distinct geometric stops as their centers approach the origin. They first touch at a center distance $d = \phi^2\sqrt{3}/2$, forming a cage of 20 pieces meeting along the 30 dodecahedron edges with 12 open windows (genus 11). The 12 windows close simultaneously at $d = \sqrt{3}/2$, creating a sealed shell around a hollow. The hollow fills completely at $d = \phi^2/(2\sqrt{3})$. For the variant using Lotus Jewel Axes, the hollow fills at $d = \sqrt{3}/(2\phi)$, where the Tricap tips meet.

Precisely, let the Icosaxes be defined by the intersection of the cube $\{|x|,|y|,z| \le \phi/2\}$ and the octahedron $\{|x|+|y|+|z| \le \phi^2/2\}$. The first stop corresponds to the separation of axes along face normals and edge cross products. The window stop is determined by a two-variable linear program on the five-fold axis, and the hollow stop is determined by the center point. The Lotus Jewel Axes variant, obtained by removing all 8 Tricaps, maintains the first two stops but shifts the hollow fill to the distance where the Tricap tips converge.

## 3. The Pieces: Icosaxes and Volumes
The primary component, the Icosaxes, is defined as the intersection of a cube and an octahedron: $\{|x|,|y|,|z| \le \phi/2\} \cap \{|x|+|y|+|z| \le \phi^2/2\}$. Its volume is $1 + 2\sqrt{5}/3$, and its hexagonal faces lie at a distance of $\phi^2/(2\sqrt{3})$, which is the inradius of an icosahedron with edge length 1.

The companion piece, the Unborn Axes, has a volume of $1 + \sqrt{5}/3$. The Lotus Jewel Axes is a variant of the Icosaxes with all 8 Tricaps removed, resulting in a volume of $\sqrt{5}$. The Tricap itself, a dent removed from the Icosaxes, has a volume of $(1 - \sqrt{5}/3)/8$. The Dodecaxes, defined as Unborn Axes with 8 Tricap keys, has a volume of 2.

## 4. Proof of the Stops
The proof of the stops relies on exact symbolic computation using `sympy`, verifying the first touch via separating axes between neighbors, the window stop via a linear program on the five-fold axis, and the hollow stop via the center point. By symmetry, the last point of a window lies on its five-fold axis, and the last point of the hollow is the center; float sweeps using `manifold3d` unions confirm these stops at every stage.

In the Lotus Jewel Axes version, the geometry remains identical for the first two stops, but the hollow fills at $d = \sqrt{3}/(2\phi)$, which is exactly $1/\phi^3$ of the first touch distance. This corresponds to the moment the tips of the removed Tricaps meet at the center.

## 5. The Icosaxes Hexa
The Icosaxes Hexa is constructed by placing 8 Icosaxes on the corners of a cube around an Unborn Axes at the golden split sites. This configuration is equivalent to 9 Icosaxes passing through each other, where each overlap has a volume of $\sqrt{5}/24$.

What remains of the middle piece in this cluster is exactly an Unborn Axes, forming one closed solid with a total volume of $9 + 6\sqrt{5}$. Whether this geometric equivalence holds along the whole golden bond is currently pending verification [CHECK: pending].

## 6. The Icosaxes Kagome Network and Keyaxes
The Icosaxes Kagome network places Icosaxes on the lattice $(2\mathbb{Z})^3$ and Unborn Axes on $(2\mathbb{Z}+1)^3$ (scaled by $\phi/2$). Following the rules of #17, no piece belongs to more than two clusters, and no two clusters share more than one piece. On the BCC anchor lattice, the "cube8" cluster (8 Icosaxes around an Unborn Axes) ensures every Icosaxes is in exactly two clusters with 8 neighbors, a property described as perfect like the rhombohedron in #17.

When Dodecaxes are placed at the cluster centers, each Icosaxes is dented towards its two centers (opposite hexagons) and keyed outward on six faces, resulting in no overlaps. This keyed piece, given the placeholder name Keyaxes, has a volume exactly equal to $\phi^2 = (3+\sqrt{5})/2$.

## 7. Prior Art and Credit
We credit the following prior art: Wolfram Demonstration "Cluster of 20 Icosahedra" (twenty icosahedra on a dodecahedron's corners); G. Hart, *Polyhedra Clusters* (twenty great icosahedra); S. Kabai (2010), *30 Cubes on a Rhombic Triacontahedron*; Koca et al. (2015), who identified Icosaxes/Unborn Axes as truncated octahedra with $x = \tau, 1/\tau$; and corner-sharing cube nets (*Molecules* 24(7):1221, 2019).

Not found in the sources searched (library of 302 references; web, 2026-10-27) are: truncated octahedra on a dodecahedron's corners; the golden stops; and the Icosaxes Kagome network.

## 8. Methods and Data
The study was conducted in the folder `k-research studies/2026-10-27-icosaxes-twenty`. The exact scripts used are `exact.py`, `twenty*.py`, `kagome-b.py`, and `check-net.py`. The resulting renders include `twenty-sheet.png`, `twenty-lja-sheet.png`, and `NK2x-parts.png`.

## 9. Placeholder Names
The following working names are used as defined by DICTO:
*   **Cage/Shell/Orb:** Icosaxes Cage, Icosaxes Shell, Icosaxes Orb; Lotus Cage/Shell/Orb.
*   **Block:** Icosaxes Hexa (keyed variant: Lotus Hexa).
*   **Piece:** Keyaxes.
*   **Network:** Icosaxes Kagome.
