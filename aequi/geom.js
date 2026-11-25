// Aequi picker geometry: a solid from its half-spaces {x : n·x <= d}, solid angles, Vacuus plates, lookups.
(function (root) {
  'use strict';
  var EPS = 1e-9;
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function len(a) { return Math.sqrt(dot(a, a)); }
  function scale(a, s) { return [a[0] * s, a[1] * s, a[2] * s]; }

  // planes: [{n:[x,y,z] (unit), d:number, k:kind}] ; returns {verts, faces:[{p, k, v:[indices], n, d}], edges}
  function buildSolid(planes) {
    var P = planes.length, verts = [], i, j, l;
    for (i = 0; i < P; i++) for (j = i + 1; j < P; j++) {
      var cij = cross(planes[i].n, planes[j].n);
      if (len(cij) < 1e-12) continue;
      for (l = j + 1; l < P; l++) {
        var det = dot(cij, planes[l].n);
        if (Math.abs(det) < 1e-12) continue;
        // x = (d_i (n_j × n_l) + d_j (n_l × n_i) + d_l (n_i × n_j)) / det
        var a = cross(planes[j].n, planes[l].n), b = cross(planes[l].n, planes[i].n);
        var x = [(planes[i].d * a[0] + planes[j].d * b[0] + planes[l].d * cij[0]) / det,
                 (planes[i].d * a[1] + planes[j].d * b[1] + planes[l].d * cij[1]) / det,
                 (planes[i].d * a[2] + planes[j].d * b[2] + planes[l].d * cij[2]) / det];
        var inside = true;
        for (var q = 0; q < P; q++) if (dot(planes[q].n, x) > planes[q].d + EPS) { inside = false; break; }
        if (!inside) continue;
        var dup = false;
        for (var w = 0; w < verts.length; w++) {
          var v = verts[w];
          if (Math.abs(v[0] - x[0]) < EPS && Math.abs(v[1] - x[1]) < EPS && Math.abs(v[2] - x[2]) < EPS) { dup = true; break; }
        }
        if (!dup) verts.push(x);
      }
    }
    var faces = [];
    for (i = 0; i < P; i++) {
      var pl = planes[i], on = [];
      for (j = 0; j < verts.length; j++) if (Math.abs(dot(pl.n, verts[j]) - pl.d) < EPS) on.push(j);
      if (on.length < 3) continue;
      var c = [0, 0, 0];
      on.forEach(function (k) { c[0] += verts[k][0]; c[1] += verts[k][1]; c[2] += verts[k][2]; });
      c = scale(c, 1 / on.length);
      var u = sub(verts[on[0]], c); u = scale(u, 1 / len(u));
      var vv = cross(pl.n, u);
      on.sort(function (p1, p2) {
        var a1 = sub(verts[p1], c), a2 = sub(verts[p2], c);
        return Math.atan2(dot(a1, vv), dot(a1, u)) - Math.atan2(dot(a2, vv), dot(a2, u));
      });
      faces.push({ p: i, k: pl.k, v: on, n: pl.n, d: pl.d });
    }
    var eset = {}, edges = [];
    faces.forEach(function (f) {
      for (var t = 0; t < f.v.length; t++) {
        var a = f.v[t], b = f.v[(t + 1) % f.v.length], key = a < b ? a + '_' + b : b + '_' + a;
        if (!eset[key]) { eset[key] = 1; edges.push([Math.min(a, b), Math.max(a, b)]); }
      }
    });
    return { verts: verts, faces: faces, edges: edges };
  }

  // solid angle of a triangle seen from the origin (Van Oosterom and Strackee 1983)
  function triSolidAngle(a, b, c) {
    var la = len(a), lb = len(b), lc = len(c);
    var num = dot(a, cross(b, c));
    var den = la * lb * lc + dot(a, b) * lc + dot(a, c) * lb + dot(b, c) * la;
    return 2 * Math.atan2(Math.abs(num), den);
  }
  function faceSolidAngle(S, f) {
    var s = 0, v = S.verts;
    for (var t = 1; t + 1 < f.v.length; t++) s += triSolidAngle(v[f.v[0]], v[f.v[t]], v[f.v[t + 1]]);
    return s;
  }

  // is the plane through the centre with unit normal m a mirror of the solid? (reflect every face plane)
  function isMirror(S, m) {
    for (var i = 0; i < S.faces.length; i++) {
      var f = S.faces[i], k = 2 * dot(f.n, m), r = [f.n[0] - k * m[0], f.n[1] - k * m[1], f.n[2] - k * m[2]], hit = false;
      for (var j = 0; j < S.faces.length; j++) {
        var g = S.faces[j];
        if (Math.abs(g.d - f.d) < 1e-7 && Math.abs(g.n[0] - r[0]) < 1e-7 && Math.abs(g.n[1] - r[1]) < 1e-7 && Math.abs(g.n[2] - r[2]) < 1e-7) { hit = true; break; }
      }
      if (!hit) return false;
    }
    return true;
  }
  // Vacuus plates: one triangle (centre, a, b) per edge; mirror = the plate lies on a mirror plane
  function vacuusPlates(S) {
    return S.edges.map(function (e) {
      var a = S.verts[e[0]], b = S.verts[e[1]], m = cross(a, b), lm = len(m);
      return { e: e, mirror: lm > 1e-12 && isMirror(S, scale(m, 1 / lm)) };
    });
  }

  // the Resonus (DICTO): through the centre, one plane parallel to each face (parallel faces share it); each plate is the cross-section
  // of the solid in that plane, ordered round its normal
  function resonusPlates(S) {
    var out = [], seen = [];
    S.faces.forEach(function (f) {
      var n = f.n;
      if (seen.some(function (m) { return Math.abs(Math.abs(dot(m, n)) - 1) < 1e-9; })) return;
      seen.push(n);
      var pts = [];
      S.verts.forEach(function (v) { if (Math.abs(dot(n, v)) < 1e-9) pts.push(v); });
      S.edges.forEach(function (e) {
        var a = S.verts[e[0]], b = S.verts[e[1]], sa = dot(n, a), sb = dot(n, b);
        if ((sa > 1e-9 && sb < -1e-9) || (sa < -1e-9 && sb > 1e-9)) { var t = sa / (sa - sb); pts.push([a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), a[2] + t * (b[2] - a[2])]); }
      });
      if (pts.length < 3) return;
      var u = pts[0], lu = len(u); u = scale(u, 1 / lu); var w = cross(n, u);
      pts.sort(function (p, q) { return Math.atan2(dot(p, w), dot(p, u)) - Math.atan2(dot(q, w), dot(q, u)); });
      out.push({ n: n, pts: pts, mirror: isMirror(S, n) });
    });
    return out;
  }

  // ---- data helpers
  function planesFor(data, die, perm) {
    var orbs = data.groups[die.g], P = [];
    die.o.forEach(function (oi, j) {
      orbs[oi].dirs.forEach(function (di) {
        var dd = perm ? perm[di] : di;
        P.push({ n: data.dirs[dd], d: die.d[j], k: j });
      });
    });
    return P;
  }
  function compose(p, q) { return p.map(function (_, i) { return q[p[i]]; }); } // i -> q(p(i))
  function inverse(p) { var r = []; p.forEach(function (j, i) { r[j] = i; }); return r; }
  function prepare(data) {
    var n = data.dirs.length, I = [];
    for (var i = 0; i < n; i++) I.push(i);
    var M = data.PM, Q = data.PQ;
    // the transforms tried in a lookup: identity, mirror x -> -x, quarter turn about z, and both
    data.T = [{ id: 'I', p: I, improper: false }, { id: 'M', p: M, improper: true },
              { id: 'Q', p: Q, improper: false }, { id: 'MQ', p: compose(Q, M), improper: true }];
    data.index = {};
    data.byK = {};
    data.dice.forEach(function (e, k) {
      e.k = e.no ? e.no - 1 : k;   // catalogue 2 dice carry their catalogue number (Nos. 1233-1235 are not in the picker)
      data.byK[e.k] = e;
      var ds = [];
      e.osets = e.o.map(function (oi) { return data.groups[e.g][oi].dirs; });
      e.osets.forEach(function (s) { ds = ds.concat(s); });
      e.key = ds.slice().sort(function (a, b) { return a - b; }).join(',');
      (data.index[e.key] = data.index[e.key] || []).push(e);
    });
  }
  // ticked: list of orbit indices of group g. Returns {die, t (transform), exact} or null
  function lookup(data, g, ticked) {
    var orbs = data.groups[g], best = null;
    data.T.forEach(function (t) {
      if (g === 'Ih' && (t.id === 'Q' || t.id === 'MQ')) return;
      var sets = ticked.map(function (oi) { return orbs[oi].dirs.map(function (d) { return t.p[d]; }); });
      var all = [].concat.apply([], sets).sort(function (a, b) { return a - b; });
      var cands = data.index[all.join(',')] || [];
      cands.forEach(function (e) {
        // each orbit of the die must be a union of ticked orbits (then the die has the chosen symmetry)
        var ok = e.osets.every(function (os) {
          var s = {}; os.forEach(function (d) { s[d] = 1; });
          return sets.every(function (ts) {
            var c = ts.filter(function (d) { return s[d]; }).length; return c === 0 || c === ts.length;
          });
        });
        if (!ok) return;
        var score = (e.g === g ? 0 : 2) + (t.id === 'I' ? 0 : 1);
        if (!best || score < best.score) best = { die: e, t: t, score: score };
      });
    });
    if (best) best.exact = best.die.g === g;
    return best;
  }

  // the union of the ticked orbits is one orbit of a group (face-transitive): {g, lab} of the largest such group
  var ORDER = { Ih: 120, Oh: 48, O: 24, Td: 24, Th: 24, T: 12 };
  function singleOrbit(data, g, ticked) {
    var all = [].concat.apply([], ticked.map(function (oi) { return data.groups[g][oi].dirs; }));
    var best = null;
    Object.keys(data.groups).forEach(function (g2) {
      data.groups[g2].forEach(function (o) {
        data.T.forEach(function (t) {
          if (o.dirs.length !== all.length) return;
          var s = {}; o.dirs.forEach(function (d) { s[t.p[d]] = 1; });
          if (all.every(function (d) { return s[d]; }) && (!best || ORDER[g2] > ORDER[best.g])) best = { g: g2, lab: o.lab, plain: o.plain };
        });
      });
    });
    return best;
  }
  var api = { singleOrbit: singleOrbit, ORDER: ORDER, buildSolid: buildSolid, faceSolidAngle: faceSolidAngle, triSolidAngle: triSolidAngle,
    vacuusPlates: vacuusPlates, resonusPlates: resonusPlates, isMirror: isMirror, planesFor: planesFor, prepare: prepare, lookup: lookup,
    inverse: inverse, dot: dot, cross: cross };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.AequiGeom = api;
})(this);
