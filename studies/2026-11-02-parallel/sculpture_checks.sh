#!/bin/bash
# Prior art for Vacuus sculpture (DICTO, 11-02): slotted / intersecting-plane sculpture and models. Library first (ask-library).
Q=("slide-together sculpture slotted flat pieces polyhedron George Hart" "intersecting planes sculpture polyhedron Rinus Roelofs" "Naum Gabo stereometric construction interlocking planes head"
   "sliceform slotted cardboard model polyhedron intersecting planes" "three mutually perpendicular squares slotted together octahedron model"
   "great circles slotted together sphere model" "cuboctahedron four hexagons intersecting planes model" "icosidodecahedron six decagons great circles model")
for q in "${Q[@]}"; do echo "=== $q"; ~/bin/ask-library "$q" 6 2>&1 | head -40; done
