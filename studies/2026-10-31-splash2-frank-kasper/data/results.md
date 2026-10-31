## Checks on all 199 TCP structures (count of structures passing)
- T_per_atom: 199/199
- bonds_per_atom: 199/199
- five_bonds_per_atom_6: 199/199
- six_bonds_per_atom: 199/199
- Zbar_from_sites: 199/199
- tet_j_sum: 199/199
- tet_six_edges: 199/199
- j2_always_opposite: 199/199
- no_tet_with_3_six_edges: 199/199
- shell6_sum: 199/199
- YK_line: 199/199
- ring_sizes_6: 199/199

## Physical phases (per cell, exact)
| phase | compound | N | N12:N14:N15:N16 | Zbar | tetrahedra/atom | 6-bonds/atom | 6-bond share | YK defect a0 | j2 tet/atom | major skeleton |
|---|---|---|---|---|---|---|---|---|---|---|
| A15 | Cr3Si | 8 | 2:6:0:0 | 27/2 | 23/4 | 3/4 | 1/9 | 0 | 3/4 | lines |
| C15 | MgCu2 | 24 | 16:0:0:8 | 40/3 | 17/3 | 2/3 | 1/10 | 0 | 0 | 3D net (nodes 4-valent) |
| C14 | MgZn2 | 12 | 8:0:0:4 | 40/3 | 17/3 | 2/3 | 1/10 | 0 | 0 | 3D net (nodes 4-valent) |
| C14 ternary | U2Cr3Si | 12 | 8:0:0:4 | 40/3 | 17/3 | 2/3 | 1/10 | 0 | 0 | 3D net (nodes 4-valent) |
| C36 | MgNi2 | 24 | 16:0:0:8 | 40/3 | 17/3 | 2/3 | 1/10 | 0 | 0 | 3D net (nodes 4-valent) |
| 9R Laves | Mg(Li,Zn)2 | 54 | 36:0:0:18 | 40/3 | 17/3 | 2/3 | 1/10 | 0 | 0 | 3D net (nodes 4-valent) |
| Laves 9-layer (Ag) | Mg9(Zn,Ag)18 | 54 | 36:0:0:18 | 40/3 | 17/3 | 2/3 | 1/10 | 0 | 0 | 3D net (nodes 4-valent) |
| Laves long period (Ag) | Mg(Zn,Ag)2 | 126 | 84:0:0:42 | 40/3 | 17/3 | 2/3 | 1/10 | 0 | 0 | 3D net (nodes 4-valent) |
| Z | Zr4Al3 | 7 | 3:2:2:0 | 94/7 | 40/7 | 5/7 | 5/47 | 0 | 6/7 | layer net (nodes 3-valent); lines |
| sigma | CrFe-type (Cr,Fe,Ni,Pd,Rh) | 30 | 10:16:4:0 | 202/15 | 86/15 | 11/15 | 11/101 | 0 | 4/5 | layer net (nodes 2+3-valent); lines |
| sigma (COD) | (Cr,Fe,Mn,Mo,Ni)30 | 30 | 10:16:4:0 | 202/15 | 86/15 | 11/15 | 11/101 | 0 | 4/5 | layer net (nodes 2+3-valent); lines |
| mu | W6Fe7 | 39 | 21:6:6:6 | 174/13 | 74/13 | 9/13 | 3/29 | 0 | 6/13 | 3D net (nodes 2+4-valent); layer net (nodes 3-valent) |
| delta | MoNi | 56 | 24:20:8:4 | 94/7 | 40/7 | 5/7 | 5/47 | 0 | 9/14 | 3D net (nodes 2+3+4-valent) |
| P | Mo-Ni-Cr | 56 | 24:20:8:4 | 94/7 | 40/7 | 5/7 | 5/47 | 0 | 9/14 | 3D net (nodes 2+3+4-valent); lines |
| R | Mo-Co-Cr | 159 | 81:36:18:24 | 710/53 | 302/53 | 37/53 | 37/355 | 0 | 24/53 | 3D net (nodes 2+3+4-valent) |
| R (Mn-Si) | Mn85.5Si14.5 | 159 | 81:36:18:24 | 710/53 | 302/53 | 37/53 | 37/355 | 0 | 24/53 | 3D net (nodes 2+3+4-valent) |
| nu | Mn81.5Si18.5 | 186 | 74:80:20:12 | 1250/93 | 532/93 | 67/93 | 67/625 | 0 | 2/3 | 3D net (nodes 2+3+4-valent); lines |
| T (Bergman) | Mg32(Al,Zn)49 | 162 | 98:12:12:40 | 1082/81 | 460/81 | 55/81 | 55/541 | 0 | 2/9 | 3D net (nodes 2+3+4-valent) |

Not TCP (Voronoi/Delaunay test): chi (alpha-Mn) (site 34: bond folds [(4, 1)]); Mg17Al12 (alpha-Mn type) (site 34: bond folds [(4, 1)]); Mg23Al30 (site 0: bond folds [(4, 6)]); Mg21Zn25 (site 0: bond folds [(3, 1), (7, 1)])

## FK59 kagome family: 119 stackings; 22 Z/L patterns realised by 2 or more different Laves stackings
Census keys identical (per slab) for every stacking with the same Z/L pattern: 119 of 119
Keys that do depend on the Laves c/h letters: 

## Window fits (per row of tiles / per kagome slab; coefficients are per window of that kind)
- N: square-triangle window 1: S 8, T 7 | FK59 window 1: + 6, 0 7
- N12: square-triangle window 1: S 2, T 3 | FK59 window 1: + 4, 0 3
- N14: square-triangle window 1: S 6, T 2 | FK59 window 1: 0 2
- N15: square-triangle window 1: T 2 | FK59 window 1: 0 2
- N16: square-triangle window 0: const 0 | FK59 window 1: + 2
- T: square-triangle window 1: S 46, T 40 | FK59 window 1: + 34, 0 40
- Zsum: square-triangle window 1: S 108, T 94 | FK59 window 1: + 80, 0 94
- bond: square-triangle window 1: S 54, T 47 | FK59 window 1: + 40, 0 47
- bond5: square-triangle window 1: S 48, T 42 | FK59 window 1: + 36, 0 42
- bond5_12_12: square-triangle window 1: T 6 | FK59 window 1: + 12, 0 6
- bond5_12_14: square-triangle window 1: S 24, T 12 | FK59 window 1: 0 12
- bond5_12_15: square-triangle window 1: T 12 | FK59 window 1: 0 12
- bond5_12_16: square-triangle window 0: const 0 | FK59 window 1: + 24
- bond5_14_14: square-triangle window 1: S 24 | FK59 window 0: const 0
- bond5_14_15: square-triangle window 1: T 12 | FK59 window 1: 0 12
- bond5_14_16: square-triangle window 0: const 0 | FK59 window 0: const 0
- bond5_15_15: square-triangle window 0: const 0 | FK59 window 0: const 0
- bond5_15_16: square-triangle window 0: const 0 | FK59 window 0: const 0
- bond6: square-triangle window 1: S 6, T 5 | FK59 window 1: + 4, 0 5
- bond6_14_14: square-triangle window 2: SS 6, ST 7/2, TT 2 | FK59 window 2: +0 1/2, 00 2
- bond6_14_15: square-triangle window 2: ST 1 | FK59 window 0: const 0
- bond6_14_16: square-triangle window 0: const 0 | FK59 window 2: +0 1
- bond6_15_15: square-triangle window 2: ST 1, TT 3 | FK59 window 1: 0 3
- bond6_15_16: square-triangle window 0: const 0 | FK59 window 0: const 0
- bond6_16_16: square-triangle window 0: const 0 | FK59 window 2: ++ 4, +- 4, +0 3/2
- nb_12_12: square-triangle window 1: T 12 | FK59 window 1: + 24, 0 12
- nb_12_14: square-triangle window 1: S 24, T 12 | FK59 window 1: 0 12
- nb_12_15: square-triangle window 1: T 12 | FK59 window 1: 0 12
- nb_12_16: square-triangle window 0: const 0 | FK59 window 1: + 24
- nb_14_12: square-triangle window 1: S 24, T 12 | FK59 window 1: 0 12
- nb_14_14: square-triangle window 2: SS 60, ST 31, TT 4 | FK59 window 2: +0 1, 00 4
- nb_14_15: square-triangle window 2: ST 7, TT 12 | FK59 window 1: 0 12
- nb_14_16: square-triangle window 0: const 0 | FK59 window 2: +0 1
- nb_15_12: square-triangle window 1: T 12 | FK59 window 1: 0 12
- nb_15_14: square-triangle window 2: ST 7, TT 12 | FK59 window 1: 0 12
- nb_15_15: square-triangle window 2: ST 2, TT 6 | FK59 window 1: 0 6
- nb_15_16: square-triangle window 0: const 0 | FK59 window 0: const 0
- nb_16_12: square-triangle window 0: const 0 | FK59 window 1: + 24
- nb_16_14: square-triangle window 0: const 0 | FK59 window 2: +0 1
- nb_16_15: square-triangle window 0: const 0 | FK59 window 0: const 0
- nb_16_16: square-triangle window 0: const 0 | FK59 window 2: ++ 8, +- 8, +0 3
- ring6_Z12: square-triangle window 0: const 12 | FK59 window 1: + 24, 0 12
- ring_14_14_n12=0: square-triangle window 2: TT 1 | FK59 window 1: 0 1
- ring_14_14_n12=1: square-triangle window 2: ST 1 | FK59 window 0: const 0
- ring_14_14_n12=2: square-triangle window 2: SS 6, ST 3/2 | FK59 window 0: const 0
- ring_14_14_n12=3: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_14_14_n12=4: square-triangle window 2: ST 1 | FK59 window 0: const 0
- ring_14_14_n12=6: square-triangle window 2: TT 1 | FK59 window 2: 00 1
- ring_14_15_n12=2: square-triangle window 2: ST 1 | FK59 window 0: const 0
- ring_14_15_n12=4: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_14_15_n12=6: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_14_16_n12=3: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_14_16_n12=4: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_14_16_n12=6: square-triangle window 0: const 0 | FK59 window 2: +0 1
- ring_15_15_n12=2: square-triangle window 2: ST 1, TT 3 | FK59 window 1: 0 3
- ring_15_16_n12=3: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_15_16_n12=4: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_16_16_n12=4: square-triangle window 0: const 0 | FK59 window 0: const 0
- ring_16_16_n12=6: square-triangle window 0: const 0 | FK59 window 2: ++ 4, +- 4, +0 3/2
- shell6_Z12: square-triangle window 0: const 12 | FK59 window 1: + 24, 0 12
- shell6_Z14: square-triangle window 1: S 24, T 12 | FK59 window 1: 0 12
- shell6_Z15: square-triangle window 1: T 6 | FK59 window 1: 0 6
- shell6_Z16: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_j0: square-triangle window 0: const 16 | FK59 window 1: + 10, 0 16
- tet_j1: square-triangle window 1: S 24, T 18 | FK59 window 1: + 24, 0 18
- tet_j2: square-triangle window 0: const 6 | FK59 window 1: 0 6
- tet_j2_opposite: square-triangle window 0: const 6 | FK59 window 1: 0 6
- tet_v2222: square-triangle window 0: const 0 | FK59 window 1: + 2
- tet_v2222_j0: square-triangle window 0: const 0 | FK59 window 1: + 2
- tet_v2224: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2224_j0: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2225: square-triangle window 1: T 4 | FK59 window 1: 0 4
- tet_v2225_j0: square-triangle window 1: T 4 | FK59 window 1: 0 4
- tet_v2226: square-triangle window 0: const 0 | FK59 window 1: + 8
- tet_v2226_j0: square-triangle window 0: const 0 | FK59 window 1: + 8
- tet_v2244: square-triangle window 1: T 6 | FK59 window 2: 00 6
- tet_v2244_j0: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2244_j1: square-triangle window 1: T 6 | FK59 window 2: 00 6
- tet_v2245: square-triangle window 1: T 12 | FK59 window 1: 0 12
- tet_v2245_j0: square-triangle window 1: T 12 | FK59 window 1: 0 12
- tet_v2245_j1: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2246: square-triangle window 0: const 0 | FK59 window 2: +0 6
- tet_v2246_j0: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2246_j1: square-triangle window 0: const 0 | FK59 window 2: +0 6
- tet_v2255: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2255_j0: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2256: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2256_j1: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2266: square-triangle window 0: const 0 | FK59 window 2: ++ 24, +- 24, +0 9
- tet_v2266_j1: square-triangle window 0: const 0 | FK59 window 2: ++ 24, +- 24, +0 9
- tet_v2444: square-triangle window 2: SS 40, ST 18 | FK59 window 0: const 0
- tet_v2444_j0: square-triangle window 1: S 16 | FK59 window 0: const 0
- tet_v2444_j1: square-triangle window 2: SS 24, ST 10 | FK59 window 0: const 0
- tet_v2445: square-triangle window 2: ST 4 | FK59 window 0: const 0
- tet_v2445_j1: square-triangle window 2: ST 4 | FK59 window 0: const 0
- tet_v2446: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2446_j1: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2455: square-triangle window 2: ST 4, TT 12 | FK59 window 1: 0 12
- tet_v2455_j1: square-triangle window 2: ST 4, TT 12 | FK59 window 1: 0 12
- tet_v2456: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2456_j1: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2466: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2466_j1: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2556: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v2556_j1: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4444: square-triangle window 2: SS 6, ST 2 | FK59 window 0: const 0
- tet_v4444_j2: square-triangle window 2: SS 6, ST 2 | FK59 window 0: const 0
- tet_v4445: square-triangle window 2: ST 2 | FK59 window 0: const 0
- tet_v4445_j2: square-triangle window 2: ST 2 | FK59 window 0: const 0
- tet_v4446: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4446_j2: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4455: square-triangle window 2: ST 2, TT 6 | FK59 window 1: 0 6
- tet_v4455_j2: square-triangle window 2: ST 2, TT 6 | FK59 window 1: 0 6
- tet_v4456: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4456_j2: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4466: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4466_j2: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4556: square-triangle window 0: const 0 | FK59 window 0: const 0
- tet_v4556_j2: square-triangle window 0: const 0 | FK59 window 0: const 0

## Global fits (per atom), all TCP / physical only
- N: all constant ['1'] | physical constant
- N12: all line in Zbar ['34', '-5/2'] | physical line in Zbar
- N14: all site-additive (linear in x12, x14, x15, x16) ['0', '1', '0', '0'] | physical site-additive (linear in x12, x14, x15, x16)
- N15: all site-additive (linear in x12, x14, x15, x16) ['0', '0', '1', '0'] | physical site-additive (linear in x12, x14, x15, x16)
- N16: all site-additive (linear in x12, x14, x15, x16) ['1/2', '-1/6', '-7/12', '0'] | physical site-additive (linear in x12, x14, x15, x16)
- T: all line in Zbar ['-1', '1/2'] | physical line in Zbar
- Zsum: all line in Zbar ['0', '1'] | physical line in Zbar
- bond: all line in Zbar ['0', '1/2'] | physical line in Zbar
- bond5: all constant ['6'] | physical constant
- bond5_12_12: all not site-additive  | physical not site-additive
- bond5_12_14: all not site-additive  | physical not site-additive
- bond5_12_15: all not site-additive  | physical not site-additive
- bond5_12_16: all not site-additive  | physical not site-additive
- bond5_14_14: all not site-additive  | physical not site-additive
- bond5_14_15: all not site-additive  | physical not site-additive
- bond5_14_16: all not site-additive  | physical not site-additive
- bond5_15_15: all not site-additive  | physical not site-additive
- bond5_15_16: all not site-additive  | physical not site-additive
- bond6: all line in Zbar ['-6', '1/2'] | physical line in Zbar
- bond6_14_14: all not site-additive  | physical not site-additive
- bond6_14_15: all not site-additive  | physical not site-additive
- bond6_14_16: all not site-additive  | physical not site-additive
- bond6_15_15: all not site-additive  | physical not site-additive
- bond6_15_16: all not site-additive  | physical not site-additive
- bond6_16_16: all not site-additive  | physical not site-additive
- nb_12_12: all not site-additive  | physical not site-additive
- nb_12_14: all not site-additive  | physical not site-additive
- nb_12_15: all not site-additive  | physical not site-additive
- nb_12_16: all not site-additive  | physical not site-additive
- nb_14_12: all not site-additive  | physical not site-additive
- nb_14_14: all not site-additive  | physical not site-additive
- nb_14_15: all not site-additive  | physical not site-additive
- nb_14_16: all not site-additive  | physical not site-additive
- nb_15_12: all not site-additive  | physical not site-additive
- nb_15_14: all not site-additive  | physical not site-additive
- nb_15_15: all not site-additive  | physical not site-additive
- nb_15_16: all not site-additive  | physical not site-additive
- nb_16_12: all not site-additive  | physical not site-additive
- nb_16_14: all not site-additive  | physical not site-additive
- nb_16_15: all not site-additive  | physical not site-additive
- nb_16_16: all not site-additive  | physical not site-additive
- ring6_Z12: all not site-additive  | physical not site-additive
- ring_14_14_n12=0: all not site-additive  | physical not site-additive
- ring_14_14_n12=1: all not site-additive  | physical not site-additive
- ring_14_14_n12=2: all not site-additive  | physical not site-additive
- ring_14_14_n12=3: all not site-additive  | physical not site-additive
- ring_14_14_n12=4: all not site-additive  | physical constant
- ring_14_14_n12=6: all not site-additive  | physical not site-additive
- ring_14_15_n12=2: all not site-additive  | physical not site-additive
- ring_14_15_n12=4: all not site-additive  | physical not site-additive
- ring_14_15_n12=6: all not site-additive  | physical not site-additive
- ring_14_16_n12=3: all not site-additive  | physical not site-additive
- ring_14_16_n12=4: all not site-additive  | physical not site-additive
- ring_14_16_n12=6: all not site-additive  | physical not site-additive
- ring_15_15_n12=2: all not site-additive  | physical not site-additive
- ring_15_16_n12=3: all not site-additive  | physical not site-additive
- ring_15_16_n12=4: all not site-additive  | physical not site-additive
- ring_16_16_n12=4: all not site-additive  | physical not site-additive
- ring_16_16_n12=6: all not site-additive  | physical not site-additive
- shell6_Z12: all not site-additive  | physical not site-additive
- shell6_Z14: all not site-additive  | physical not site-additive
- shell6_Z15: all not site-additive  | physical not site-additive
- shell6_Z16: all not site-additive  | physical not site-additive
- tet_j0: all not site-additive  | physical not site-additive
- tet_j1: all not site-additive  | physical not site-additive
- tet_j2: all not site-additive  | physical not site-additive
- tet_j2_opposite: all not site-additive  | physical not site-additive
- tet_v2222: all not site-additive  | physical not site-additive
- tet_v2222_j0: all not site-additive  | physical not site-additive
- tet_v2224: all not site-additive  | physical not site-additive
- tet_v2224_j0: all not site-additive  | physical not site-additive
- tet_v2225: all not site-additive  | physical not site-additive
- tet_v2225_j0: all not site-additive  | physical not site-additive
- tet_v2226: all not site-additive  | physical not site-additive
- tet_v2226_j0: all not site-additive  | physical not site-additive
- tet_v2244: all not site-additive  | physical not site-additive
- tet_v2244_j0: all not site-additive  | physical not site-additive
- tet_v2244_j1: all not site-additive  | physical not site-additive
- tet_v2245: all not site-additive  | physical not site-additive
- tet_v2245_j0: all not site-additive  | physical not site-additive
- tet_v2245_j1: all not site-additive  | physical not site-additive
- tet_v2246: all not site-additive  | physical not site-additive
- tet_v2246_j0: all not site-additive  | physical not site-additive
- tet_v2246_j1: all not site-additive  | physical not site-additive
- tet_v2255: all not site-additive  | physical not site-additive
- tet_v2255_j0: all not site-additive  | physical not site-additive
- tet_v2256: all not site-additive  | physical not site-additive
- tet_v2256_j1: all not site-additive  | physical not site-additive
- tet_v2266: all not site-additive  | physical not site-additive
- tet_v2266_j1: all not site-additive  | physical not site-additive
- tet_v2444: all not site-additive  | physical not site-additive
- tet_v2444_j0: all not site-additive  | physical not site-additive
- tet_v2444_j1: all not site-additive  | physical not site-additive
- tet_v2445: all not site-additive  | physical not site-additive
- tet_v2445_j1: all not site-additive  | physical not site-additive
- tet_v2446: all not site-additive  | physical not site-additive
- tet_v2446_j1: all not site-additive  | physical not site-additive
- tet_v2455: all not site-additive  | physical not site-additive
- tet_v2455_j1: all not site-additive  | physical not site-additive
- tet_v2456: all not site-additive  | physical not site-additive
- tet_v2456_j1: all not site-additive  | physical not site-additive
- tet_v2466: all not site-additive  | physical not site-additive
- tet_v2466_j1: all not site-additive  | physical not site-additive
- tet_v2556: all not site-additive  | physical not site-additive
- tet_v2556_j1: all not site-additive  | physical not site-additive
- tet_v4444: all not site-additive  | physical not site-additive
- tet_v4444_j2: all not site-additive  | physical not site-additive
- tet_v4445: all not site-additive  | physical not site-additive
- tet_v4445_j2: all not site-additive  | physical not site-additive
- tet_v4446: all not site-additive  | physical not site-additive
- tet_v4446_j2: all not site-additive  | physical not site-additive
- tet_v4455: all not site-additive  | physical not site-additive
- tet_v4455_j2: all not site-additive  | physical not site-additive
- tet_v4456: all not site-additive  | physical not site-additive
- tet_v4456_j2: all not site-additive  | physical not site-additive
- tet_v4466: all not site-additive  | physical not site-additive
- tet_v4466_j2: all not site-additive  | physical not site-additive
- tet_v4556: all not site-additive  | physical not site-additive
- tet_v4556_j2: all not site-additive  | physical not site-additive

## Table of known/hypothetical counts (Deza, Delgado Friedrichs, Dutour Sikiric)
| name | description | Z12:Z14:Z15:Z16 | Zbar | YK line 68/5 - 2x12/5 | a0 |
|---|---|---|---|---|---|
| K | complex, Pmmm | 14:21:6:0 | 552/41 | 552/41 | 0 |
| F | complex, P6/mmm | 9:13:4:0 | 175/13 | 175/13 | 0 |
| J | complex, Pmmm | 4:5:2:0 | 148/11 | 148/11 | 0 |
| H | complex, Cmmm | 5:8:2:0 | 202/15 | 202/15 | 0 |
| K* | Mn77Fe4Si19, C2 | 25:19:4:7 | 738/55 | 738/55 | 0 |
| -* (K7Cs6) | K7Cs6, P63/mmc | 7:2:2:2 | 174/13 | 174/13 | 0 |
| p-sigma | Th6Cd7, Pbam | 7:2:2:2 | 174/13 | 174/13 | 0 |
| M | Nb48Ni39Al13, Pnam | 7:2:2:2 | 174/13 | 174/13 | 0 |
| C | V2(Co,Si)3, C2/m | 15:2:2:6 | 334/25 | 334/25 | 0 |
| I | V41Ni36Si23, Cc | 11:2:2:4 | 254/19 | 254/19 | 0 |
| SM | Mg32(Zn,Al)49, Pm-3n | 49:9:0:23 | 1082/81 | 1082/81 | 0 |
| X | Mn45Co40Si15, Pnnm | 23:2:2:10 | 494/37 | 494/37 | 0 |
| Mg4Zn7 | Mg4Zn7, C2/m | 35:2:2:16 | 734/55 | 734/55 | 0 |
| hyp. 7422 | computer search no. 1 | 7:4:2:2 | 202/15 | 1006/75 | -2/45 |
| hyp. 6640 | computer search no. 40 | 6:6:4:0 | 27/2 | 269/20 | -1/24 |
| hyp. 6840 | computer search nos. 18, 62, 63 | 6:8:4:0 | 122/9 | 202/15 | -2/27 |
| hyp. 6602 | computer search, new | 6:6:0:2 | 94/7 | 94/7 | 0 |
| hyp. 9223 | new | 9:2:2:3 | 107/8 | 107/8 | 0 |
| hyp. 8522 | new | 8:5:2:2 | 228/17 | 228/17 | 0 |
| hyp. 8441 | new | 8:4:4:1 | 228/17 | 228/17 | 0 |
| hyp. 7821 | new | 7:8:2:1 | 121/9 | 121/9 | 0 |
| hyp. 7740 | new | 7:7:4:0 | 121/9 | 121/9 | 0 |
| hyp. 11224 | new | 11:2:2:4 | 254/19 | 254/19 | 0 |
| hyp. 11143 | new | 11:1:4:3 | 254/19 | 254/19 | 0 |
| hyp. 61120 | new | 6:11:2:0 | 256/19 | 256/19 | 0 |
| hyp. 10604 | new | 10:6:0:4 | 67/5 | 67/5 | 0 |
| hyp. 10523 | new | 10:5:2:3 | 67/5 | 67/5 | 0 |
| hyp. 10442 | new | 10:4:4:2 | 67/5 | 67/5 | 0 |
| hyp. 10361 | new | 10:3:6:1 | 67/5 | 67/5 | 0 |
