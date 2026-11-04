#!/bin/bash
Q=("truncation of Platonic solid at golden ratio depth" "truncated icosahedron hexagons with edge lengths in golden ratio" "golden truncated tetrahedron non-regular hexagons"
   "truncated cube octagons alternating edge lengths golden ratio" "truncated dodecahedron edges trisected decagons" "non-Archimedean truncation depth of polyhedra family parameter"
   "polyhedra with two edge lengths in golden ratio icosahedral" "truncated octahedron golden ratio space filling pair")
for q in "${Q[@]}"; do echo "=== $q"; ~/bin/ask-library "$q" 6 2>&1 | head -40; done
