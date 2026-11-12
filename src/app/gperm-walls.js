// Generalized Permutohedra: the k-research study's exact data for n = 4 (the permutohedron-to-associahedron lines), copied from its JSON.
// lineA: Postnikov's straight line, one wall at t = 1 (all 5 non-interval faces together); lineB: the equal-speed line, walls at s = 1, 2.
// zStart / zEnd: the face heights of the permutohedron and Loday's associahedron in the study's frame (the permutohedron on 1..4, so each
// z_S is this app's plus |S|: a translation). The unit test checks this app's geometry against every entry; the staged slider's walls
// are computed in gperm-geometry.js (STAGE_WALLS), the study fixes their heights (the deficits zStart − zEnd) and the end shape.
// DICTO · dictospheres.com
export const STUDY = {
 "source": "k-research studies/2026-11-12-permutohedron-associahedron-line, data/gp-line-n4.json (commit ee6fd4e7)",
 "allChecksOk": true,
 "zStart": {
  "{1}": "1",
  "{2}": "1",
  "{3}": "1",
  "{4}": "1",
  "{1,2}": "3",
  "{1,3}": "3",
  "{1,4}": "3",
  "{2,3}": "3",
  "{2,4}": "3",
  "{3,4}": "3",
  "{1,2,3}": "6",
  "{1,2,4}": "6",
  "{1,3,4}": "6",
  "{2,3,4}": "6",
  "{1,2,3,4}": "10"
 },
 "zEnd": {
  "{1}": "1",
  "{2}": "1",
  "{3}": "1",
  "{4}": "1",
  "{1,2}": "3",
  "{1,3}": "2",
  "{1,4}": "2",
  "{2,3}": "3",
  "{2,4}": "2",
  "{3,4}": "3",
  "{1,2,3}": "6",
  "{1,2,4}": "4",
  "{1,3,4}": "4",
  "{2,3,4}": "6",
  "{1,2,3,4}": "10"
 },
 "interval": {
  "{1}": true,
  "{2}": true,
  "{3}": true,
  "{4}": true,
  "{1,2}": true,
  "{1,3}": false,
  "{1,4}": false,
  "{2,3}": true,
  "{2,4}": false,
  "{3,4}": true,
  "{1,2,3}": true,
  "{1,2,4}": false,
  "{1,3,4}": false,
  "{2,3,4}": true
 },
 "lineA": [
  {
   "param": "1",
   "faces": [
    "{1,3}",
    "{1,4}",
    "{2,4}",
    "{1,2,4}",
    "{1,3,4}"
   ],
   "fBefore": [
    24,
    36,
    14
   ],
   "fAt": [
    14,
    21,
    9
   ]
  }
 ],
 "lineB": [
  {
   "param": "1",
   "faces": [
    "{1,3}",
    "{1,4}",
    "{2,4}"
   ],
   "fBefore": [
    24,
    36,
    14
   ],
   "fAt": [
    18,
    27,
    11
   ]
  },
  {
   "param": "2",
   "faces": [
    "{1,2,4}",
    "{1,3,4}"
   ],
   "fBefore": [
    18,
    27,
    11
   ],
   "fAt": [
    14,
    21,
    9
   ]
  }
 ]
};
