#!/bin/bash
Q=("flat-ended triangle hexagon face polyhedron" "truncated triangle face semiregular hexagon alternating sides" "hexagonal faces with alternating edge lengths golden ratio polyhedron"
   "polyhedra with ditrigonal or 3-fold symmetric hexagonal faces" "golden hexagon icosahedral polyhedron faces" "truncated tetrahedron non-regular hexagon faces golden")
for q in "${Q[@]}"; do echo "=== $q"; ~/bin/ask-library "$q" 6 2>&1 | head -40; done
