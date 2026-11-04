#!/bin/bash
# Library checks for The Centre Pyramids chapter openers (DICTO, 11-02): ask-library (meaning search, local) per claim.
Q=("Plato Timaeus elements fire pyramid tetrahedron triangles" "Euclid Elements XII.7 pyramid one third of a prism" "Euclid Elements XIII five regular solids inscribed in a sphere centre"
   "Leonardo da Vinci vacuus solids Pacioli De divina proportione" "Kepler rhombic dodecahedron Strena seu de nive sexangula 1611 bees pomegranate"
   "rhombic dodecahedron dissected into a cube and six square pyramids" "cube dissected into six square pyramids from the centre" "Aristotle On the Heavens pyramid and cube fill space")
for q in "${Q[@]}"; do echo "=== $q"; ~/bin/ask-library "$q" 6 2>&1 | head -40; done
