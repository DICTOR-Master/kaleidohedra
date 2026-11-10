### Hand Computation of Small Cases ($n=3, 4, 5$)

**Theorem 3 Formula:** $N(n) = \sum_{\substack{a,b,c \ge 1 \\ a+b+c=n}} \frac{n!}{a!b!c!} + T(n)$, where $T(n) = 2^{n-1}-1$ (odd) or $2^{n-2}-1$ (even).
*Note: The sum counts ordered splits $(a,b,c)$ where $a \neq c$. The term $T(n)$ counts the "coincidence" cases where $a=c$ (even $n$) or the specific odd $n$ case where the split is symmetric in a way that reduces the count.*

**Correction on the Paper's Logic:** The paper's proof for $T(n)$ is slightly garbled in its description of the "split" vs "pair" logic, but the *numbers* in the table are correct. Let's verify the counts manually.

**Case $n=3$ (Permutahedron is a Hexagon):**
*   **Ridges:** Edges of the hexagon. Total = $3! \times (3-1) / 2 = 9$? No, edges = $n! \times (n-1)/2$? No.
    *   Vertices: $3! = 6$.
    *   Edges (Ridges): Each vertex has degree $n-1=2$. Total edges = $6 \times 2 / 2 = 6$.
    *   Splits $(a,b,c)$ with $a+b+c=3$:
        *   $(1,1,1)$: $3!/(1!1!1!) = 6$. Here $a=c=1$.
        *   $(1,2,0)$? No, $c \ge 1$.
        *   $(2,1,0)$? No.
        *   Only $(1,1,1)$ is possible for $a,b,c \ge 1$.
    *   The paper claims $N(3) = 3$.
    *   Manual check: The 6 edges of a hexagon lie on 3 lines through the center (the 3 long diagonals).
    *   Formula check:
        *   Sum over $a \neq c$: None (only $1,1,1$ exists). Sum = 0.
        *   $T(3)$ (odd): $2^{3-1}-1 = 3$.
        *   Total $N(3) = 3$. **Matches.**

**Case $n=4$ (Truncated Octahedron):**
*   **Ridges:** Edges of the truncated octahedron.
    *   Vertices: $4! = 24$.
    *   Edges: $24 \times 3 / 2 = 36$.
*   **Splits $(a,b,c)$ with $a+b+c=4$:**
    *   $(1,1,2)$: $4!/(1!1!2!) = 12$. ($a \neq c$)
    *   $(1,2,1)$: $4!/(1!2!1!) = 12$. ($a=c=1$)
    *   $(2,1,1)$: $4!/(2!1!1!) = 12$. ($a \neq c$)
    *   $(1,3,0)$? No.
    *   $(2,2,0)$? No.
    *   $(1,1,2)$ and $(2,1,1)$ are distinct ordered splits.
    *   $(1,2,1)$ is the symmetric case ($a=c$).
*   **Paper's Count:** $N(4) = 15$.
*   **Formula Check:**
    *   Sum ($a \neq c$): $12 + 12 = 24$.
    *   Wait, the paper says "splits $(a,b,c)$... only the split and its reverse give it".
    *   Let's re-read the paper's counting logic carefully.
    *   The paper states: "splits (1,1,3) and (1,2,2) give 20 and 30 slices".
    *   For $n=4$:
        *   $(1,1,2)$: 12 splits. Reverse is $(2,1,1)$. These are distinct ordered splits. Do they give the same slice?
        *   The normal vector for $(a,b,c)$ is $c_1 = bc(b+c)$, $c_2 = -ac(a+2b+c)$, $c_3 = ab(a+b)$.
        *   For $(1,1,2)$: $c_1 = 1(3)=3$, $c_2 = -1(1+2+2)=-5$, $c_3 = 1(2)=2$. Vector $(3, -5, 2)$.
        *   For $(2,1,1)$: $c_1 = 1(2)=2$, $c_2 = -2(2+2+1)=-10$, $c_3 = 2(3)=6$. Vector $(2, -10, 6) \propto (1, -5, 3)$.
        *   These are NOT the same. $(3, -5, 2)$ vs $(1, -5, 3)$.
        *   So $(1,1,2)$ and $(2,1,1)$ are distinct slices.
        *   Count for $a \neq c$: $12 + 12 = 24$.
        *   Count for $a=c$: $(1,2,1)$. $4!/(1!2!1!) = 12$.
        *   The paper says for even $n$, $(a,b,a)$ coincides with $(b/2, 2a, b/2)$.
        *   Here $a=1, b=2$. Coincides with $(2/2, 2(1), 2/2) = (1, 2, 1)$. It coincides with itself?
        *   The paper says "When $n$ is even... the split $(a,b,a)$ gives the same slice as $(b/2, 2a, b/2)$".
        *   If $a=1, b=2$, then $(1,2,1)$ is the same as $(1,2,1)$.
        *   So the 12 splits of type $(1,2,1)$ collapse to how many?
        *   The paper claims $N(4) = 15$.
        *   My manual count of distinct normal vectors:
            *   Type $(1,1,2)$: 12 distinct vectors.
            *   Type $(2,1,1)$: 12 distinct vectors.
            *   Type $(1,2,1)$: 12 splits. Do they collapse?
            *   The paper says $T(4) = 2^{4-2}-1 = 3$.
            *   This implies the 12 splits of type $(1,2,1)$ collapse to 3 distinct slices.
            *   Why? Because the normal vector depends on the *set* of positions, not the order?
            *   The normal vector for $(1,2,1)$ is $c_1 = 2(3)=6$, $c_2 = -1(1+4+1)=-6$, $c_3 = 1(3)=3$. Vector $(6, -6, 3) \propto (2, -2, 1)$.
            *   The vector depends only on the sizes $a,b,c$.
            *   For $(1,2,1)$, the vector is determined by the partition of indices into sets of size 1, 2, 1.
            *   There are $\binom{4}{1,2,1} = 12$ ways to assign indices.
            *   However, the normal vector is $(c_1, c_2, c_3)$ assigned to the blocks.
            *   If we swap the two blocks of size 1 (B1 and B3), the vector becomes $(c_3, c_2, c_1) = (3, -6, 6) \propto (1, -2, 2)$.
            *   Is $(2, -2, 1)$ the same as $(1, -2, 2)$? No.
            *   Wait, the paper says "only the split and its reverse give it".
            *   Reverse of $(1,2,1)$ is $(1,2,1)$.
            *   So the 12 splits should give 12 slices?
            *   But the table says 15.
            *   Let's re-evaluate the "coincidence" logic.
            *   Maybe the "splits" in the sum are not the ordered splits, but the *geometric* slices?
            *   Let's trust the table numbers for a moment and reverse engineer.
            *   $N(4) = 15$.
            *   Total ridges = 36.
            *   If we have 15 planes, average ridges per plane = 2.4.
            *   The paper says: "splits (1,1,3) and (1,2,2) give 20 and 30 slices" for $n=5$.
            *   For $n=4$:
                *   $(1,1,2)$: 12 splits.
                *   $(2,1,1)$: 12 splits.
                *   $(1,2,1)$: 12 splits.
                *   Total 36 ridges.
                *   If $(1,1,2)$ and $(2,1,1)$ are distinct, that's 24.
                *   If $(1,2,1)$ collapses to 3, total 27. Too high.
                *   If $(1,1,2)$ and $(2,1,1)$ are the *same*?
                *   Normal for $(1,1,2)$: $(3, -5, 2)$.
                *   Normal for $(2,1,1)$: $(2, -10, 6) \propto (1, -5, 3)$.
                *   These are different.
                *   Maybe the "splits" in the sum are just the *types*?
                *   No, the formula has $n!/(a!b!c!)$.
                *   Let's look at the "coincidence" again.
                *   "When $n$ is even... the split $(a,b,a)$ gives the same slice as $(b/2, 2a, b/2)$".
                *   For $n=4$, $a=1, b=2$. $(1,2,1)$ vs $(1,2,1)$.
                *   Maybe the coincidence is between $(1,1,2)$ and $(2,1,1)$?
                *   No, $a \neq c$ there.
                *   Let's re-read the proof: "A split with $a \neq c$ gives a slice... only the split and its reverse give it".
                *   So $(1,1,2)$ and $(2,1,1)$ are distinct.
                *   "A split with $a=c$ gives a normal with two values... the ratio $c_1:c_2$ depends only on $S$ and $T$".
                *   For $(1,2,1)$, $S$ (size 2) and $T$ (size 2).
                *   The normal vector has values $c_1$ on $B_1$, $c_2$ on $B_2$, $c_3$ on $B_3$.
                *   Since $a=c$, $c_1 = c_3$.
                *   So the vector is $(k, m, k)$.
                *   The slice is defined by the set of indices in $B_1$ and $B_2$ (since $B_3$ is the rest).
                *   But $B_1$ and $B_3$ have the same value $k$.
                *   So swapping $B_1$ and $B_3$ does not change the vector.
                *   The number of ways to choose $B_1$ (size 1) and $B_3$ (size 1) from 4 items is $\binom{4}{1} \times \binom{3}{1} = 12$.
                *   But since $B_1$ and $B_3$ are indistinguishable (same value), we divide by 2?
                *   $12 / 2 = 6$.
                *   So there are 6 slices of type $(1,2,1)$.
                *   Total so far: $12 + 12 + 6 = 30$.
                *   Still not 15.
                *   Wait, the paper says $N(4) = 15$.
                *   Maybe the "splits" $(1,1,2)$ and $(2,1,1)$ are actually the same?
                *   Let's check the normal vector again.
                *   $(1,1,2)$: $c_1 = 1(3)=3$, $c_2 = -1(5)=-5$, $c_3 = 1(2)=2$. $(3, -5, 2)$.
                *   $(2,1,1)$: $c_1 = 1(2)=2$, $c_2 = -2(5)=-10$, $c_3 = 2(3)=6$. $(2, -10, 6) \propto (1, -5, 3)$.
                *   These are definitely different.
                *   Is it possible the paper counts *unoriented* hyperplanes?
                *   "Central hyperplanes". A hyperplane is unoriented.
                *   $(3, -5, 2)$ and $(-3, 5, -2)$ are the same.
                *   But $(3, -5, 2)$ and $(1, -5, 3)$ are not parallel.
                *   Let's re-read the table.
                *   $n=4$, ridges=36, $N(n)=15$.
                *   Maybe the formula in the paper is:
                    *   Sum over $a < c$?
                    *   If we sum over $a < c$:
                        *   $(1,1,2)$: $a=1, c=2$. $4!/(1!1!2!) = 12$.
                        *   $(1,2,1)$: $a=c$.
                        *   $(2,1,1)$: $a=2, c=1$. (Reverse of first).
                    *   If we count pairs $\{ (a,b,c), (c,b,a) \}$ for $a \neq c$:
                        *   $(1,1,2)$ and $(2,1,1)$ form 1 pair.
                        *   Number of such pairs = $12$? No.
                        *   The number of *splits* is 12. The number of *pairs of splits* is 12?
                        *   No, the 12 splits of $(1,1,2)$ are distinct. The 12 splits of $(2,1,1)$ are distinct.
                        *   Do they map to the same hyperplane?
                        *   The hyperplane is defined by the normal vector.
                        *   If the normal vectors are different, the hyperplanes are different.
                        *   Unless... the paper is counting *types* of hyperplanes?
                        *   No, "exactly 65 central slices".
                        *   Let's check the $n=5$ case in the paper.
                        *   $N(5) = 65$.
                        *   Splits:
                            *   $(1,1,3)$: $20$.
                            *   $(1,2,2)$: $30$.
                            *   $(1,3,1)$: $10$.
                            *   $(2,1,2)$: $5$.
                            *   $(2,2,1)$: $30$? No, $5!/(2!2!1!) = 30$.
                            *   $(3,1,1)$: $20$.
                        *   Total splits = $20+30+10+5+30+20 = 115$.
                        *   Paper says 65.
                        *   Coincidences:
                            *   $(1,1,3)$ and $(3,1,1)$ are reverses. Do they give the same slice?
                            *   Normal $(1,1,3)$: $c_1 = 1(4)=4$, $c_2 = -1(1+2+3)= -6$, $c_3 = 1(2)=2$. $(4, -6, 2) \propto (2, -3, 1)$.
                            *   Normal $(3,1,1)$: $c_1 = 1(2)=2$, $c_2 = -3(3+2+1)= -18$, $c_3 = 3(4)=12$. $(2, -18, 12) \propto (1, -9, 6)$.
                            *   Different.
                            *   So $(1,1,3)$ and $(3,1,1)$ are distinct.
                            *   Wait, the paper says "only the split and its reverse give it".
                            *   This implies $(1,1,3)$ and $(3,1,1)$ are the *same* slice?
                            *   If they are the same, then the 20 splits of $(1,1,3)$ and 20 splits of $(3,1,1)$ collapse to 20? Or 10?
                            *   If they are the same, then the 20 splits of $(1,1,3)$ are the same as the 20 splits of $(3,1,1)$?
                            *   No, the splits are different sets of indices.
                            *   Maybe the normal vector for $(1,1,3)$ is the same as $(3,1,1)$?
                            *   Let's re-calculate $c_2$ for $(1,1,3)$: $-ac(a+2b+c) = -1(1)(1+2+3) = -6$.
                            *   For $(3,1,1)$: $-ac(a+2b+c) = -3(1)(3+2+1) = -18$.
                            *   Ratios: $(4, -6, 2)$ vs $(2, -18, 12)$.
                            *   $4/2 = 2$. $-6/-18 = 1/3$. Not proportional.
                            *   So they are different.
                            *   Then why does the paper say "only the split and its reverse give it"?
                            *   Maybe "reverse" means reversing the *values*? No, the values are fixed $1..n$.
                            *   Maybe the paper is wrong about the formula?
                            *   Let's check the numbers in the table again.
                            *   $N(5) = 65$.
                            *   If we sum the "types" (unordered splits):
                                *   $\{1,1,3\}$: 20 splits.
                                *   $\{1,2,2\}$: 30 splits.
                                *   $\{1,3,1\}$: 10 splits.
                                *   $\{2,1,2\}$: 5 splits.
                                *   Total = 65.
                            *   Aha! The paper is counting the number of **unordered** splits $\{a,b,c\}$?
                            *   No, the formula has $n!/(a!b!c!)$.
                            *   For $\{1,1,3\}$, the number of ordered splits is $20+20=40$.
                            *   The paper says "splits (1,1,3) and (1,2,2) give 20 and 30 slices".
                            *   This implies the count for $\{1,1,3\}$ is 20.
                            *   This means the 20 splits of $(1,1,3)$ and the 20 splits of $(3,1,1)$ are **identical** sets of slices?
                            *   Or maybe the paper counts the number of **geometric** slices, and for $(1,1,3)$ and $(3,1,1)$, the set of slices generated by $(1,1,3)$ is the same as the set generated by $(3,1,1)$?
                            *   If the normal vectors are different, the slices are different.
                            *   Unless... the paper is counting the number of **orbits** under the symmetry group?
                            *   "Up to the symmetries of the solid... there are four slices".
                            *   But $N(n)$ is the total count, not up to symmetry.
                            *   Let's re-read the proof: "A split with $a \neq c$ gives a slice whose normal takes three different values, and only the split and its reverse give it".
                            *   This implies that the slice defined by split $S$ is the same as the slice defined by split $S^R$ (reverse).
                            *   If $S = (1,1,3)$
