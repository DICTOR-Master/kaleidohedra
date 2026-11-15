/* bij.c - exhaustive test of the half-turn surgery on self-avoiding polygons of a c/h stacking (study 2026-11-15-polygon-bijection).

   Network (as #102 / study 2026-11-15-ring-counts-stackings): bilayer k has a lower atom (u=0) and an upper atom (u=1) at every
   in-plane point X = (x, y) with X = s[k](1,1) mod 3 (coordinates in thirds of the 60-degree basis a1, a2); the vertical bond joins
   them; the upper atom of bilayer k bonds to the three lower atoms of bilayer k+1 at squared in-plane distance 3 (units (a/3)^2,
   norm x^2+xy+y^2).

   Flip at bilayer kf.  The ROOT SIDE is the half of the network (atoms up to the lower atoms of kf, or from the upper atoms of kf
   on) that contains the root; the FAR SIDE is the other half.  G2 = the root side of G unchanged + the far side with its letters
   swapped by sigma (the two letters other than s[kf] exchanged).  G2 is the stacking with the c/h letter of bilayer kf flipped and
   every other letter unchanged.

   Surgery.  A polygon C crossing the vertical bonds of kf at the points P (n = |P| even) has root-side arcs and far-side arcs;
   M = the pairing of P by the far-side arcs.  C is SYMMETRIC at kf if some involutive plane isometry g that maps the lattice of
   s[kf] to itself and exchanges the other two lattices ("toggle") satisfies g(P) = P and g(M) = M.  Then g fixes the centroid of P
   and is the half-turn about it or a mirror through it; the first such g in the fixed order (half-turn, then the mirrors in the order
   of the list below) is used.  Phi(C) = root-side part of C + g(far-side part of C), an atom (k, X, u) of the far side going to
   (k, g(X), u).  n = 0: Phi(C) = C.  n = 2: g = the half-turn about the midpoint of the two crossing points (always symmetric).

   The program enumerates every polygon through the root of length <= L in G and in G2, applies Phi to the symmetric ones of G and
   checks: each image is a polygon of G2 through the root, of the same length, with the same crossing numbers at every bilayer;
   images are distinct; the set of images = the set of symmetric-at-kf polygons of G2.  It also counts the non-symmetric (RIGID)
   polygons, and for every polygon the number of bilayers at which it is rigid.
   mode 0 = the surgery above; mode 1 = WRONG: half-turn about the first crossing point; mode 2 = WRONG: no twist (identity on the
   far side); mode 3 = WRONG: 60-degree rotation of the far side about the first crossing point.  (Negative controls: these must
   produce invalid images.)
   dump = 1: print every rigid-at-kf polygon of G and G2 of length >= DUMPMIN as a line of atoms "k x y u".

   stdin: L K kr ur kf mode dump DUMPMIN / K letters s[0..K-1] (0,1,2) of G.   Root = atom (kr, (s[kr], s[kr]), ur).
   stdout: lines "LEN l ..." per even length, "RIGIDHIST ...", "MINRIGID ...", "END ok|FAIL". Exact integer arithmetic only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXL 32
static int L, K, kr, ur, kf, mode, dump, dumpmin, R, W;
static int sG[64], s2[64];
static int rx, ry;
static int *dist; static unsigned char *onp; static int *queue;
static int path[MAXL + 2];
static const int D1[3][2] = {{1, 1}, {-2, 1}, {1, -2}}, D2[3][2] = {{-1, -1}, {2, -1}, {-1, 2}};
static int ID(int k, int x, int y, int u) { return ((k * W + (x + R)) * W + (y + R)) * 2 + u; }
static void DEC(int id, int *k, int *x, int *y, int *u) { *u = id & 1; id >>= 1; *y = id % W - R; id /= W; *x = id % W - R; *k = id / W; }
static int mod3(int a) { a %= 3; return a < 0 ? a + 3 : a; }
/* neighbours of atom id in the network with letters s; returns count, -1 entries for atoms outside the window */
static int nbrs(const int *s, int id, int *out) {
  int k, x, y, u; DEC(id, &k, &x, &y, &u);
  out[0] = ID(k, x, y, 1 - u);
  int k2 = u ? k + 1 : k - 1;
  if (k2 < 0 || k2 >= K) { out[1] = out[2] = out[3] = -1; return 4; }
  int d = mod3(s[k2] - s[k]);           /* 1 or 2 */
  const int (*DD)[2] = d == 1 ? D1 : D2;
  for (int i = 0; i < 3; i++) { int x2 = x + DD[i][0], y2 = y + DD[i][1];
    if (x2 < -R || x2 > R || y2 < -R || y2 > R) out[1 + i] = -1; else out[1 + i] = ID(k2, x2, y2, 1 - u); }
  return 4;
}
static int adjacent(const int *s, int a, int b) { int o[4]; nbrs(s, a, o); for (int i = 0; i < 4; i++) if (o[i] == b) return 1; return 0; }
static int is_atom(const int *s, int id) { int k, x, y, u; DEC(id, &k, &x, &y, &u); return mod3(x) == s[k] && mod3(y) == s[k]; }
static int upper_side(int id, int kb) { int k, x, y, u; DEC(id, &k, &x, &y, &u); return k > kb || (k == kb && u == 1); }

/* ---------- cycle storage ---------- */
typedef struct { int *a; long n, cap; } Store;
static Store stG[MAXL + 1], st2img[MAXL + 1], st2sym[MAXL + 1];
static void canon(const int *c, int l, int *o) {
  int m = 0; for (int i = 1; i < l; i++) if (c[i] < c[m]) m = i;
  int f = c[(m + 1) % l] < c[(m + l - 1) % l];
  for (int i = 0; i < l; i++) o[i] = f ? c[(m + i) % l] : c[(m - i + l) % l];
}
static void push(Store *S, const int *c, int l) {
  if (S->n == S->cap) { S->cap = S->cap ? 2 * S->cap : 1024; S->a = realloc(S->a, sizeof(int) * l * S->cap); if (!S->a) { fprintf(stderr, "out of memory\n"); exit(3); } }
  canon(c, l, S->a + S->n * l); S->n++;
}
static int CL;
static int cmpc(const void *p, const void *q) { return memcmp(p, q, sizeof(int) * CL) ; }
static int cmpc_int(const void *p, const void *q) { const int *a = p, *b = q; for (int i = 0; i < CL; i++) if (a[i] != b[i]) return a[i] < b[i] ? -1 : 1; return 0; }

/* ---------- symmetry at a bilayer ---------- */
static int NINV; static int INV[8][2][2];
static void make_group(void) {
  int Rm[2][2] = {{0, -1}, {1, 1}}, Sw[2][2] = {{0, 1}, {1, 0}};
  int M[12][2][2]; int cur[2][2] = {{1, 0}, {0, 1}};
  for (int r = 0; r < 6; r++) {
    memcpy(M[r], cur, sizeof cur);
    int t[2][2]; for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) t[i][j] = Sw[i][0] * cur[0][j] + Sw[i][1] * cur[1][j];
    memcpy(M[6 + r], t, sizeof t);
    int nx[2][2]; for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) nx[i][j] = Rm[i][0] * cur[0][j] + Rm[i][1] * cur[1][j];
    memcpy(cur, nx, sizeof nx);
  }
  /* involutions other than the identity: the half-turn first, then the six mirrors */
  NINV = 0;
  for (int pass = 0; pass < 2; pass++)
    for (int m = 0; m < 12; m++) { int (*A)[2] = M[m];
      int sq00 = A[0][0] * A[0][0] + A[0][1] * A[1][0], sq01 = A[0][0] * A[0][1] + A[0][1] * A[1][1];
      int sq10 = A[1][0] * A[0][0] + A[1][1] * A[1][0], sq11 = A[1][0] * A[0][1] + A[1][1] * A[1][1];
      int isinv = sq00 == 1 && sq01 == 0 && sq10 == 0 && sq11 == 1, isid = A[0][0] == 1 && A[0][1] == 0 && A[1][0] == 0 && A[1][1] == 1;
      int ishalf = A[0][0] == -1 && A[0][1] == 0 && A[1][0] == 0 && A[1][1] == -1;
      if (!isinv || isid) continue;
      if ((pass == 0) != ishalf) continue;
      memcpy(INV[NINV++], A, sizeof(int) * 4); }
}
static const int *curS;
typedef struct { int n; int px[MAXL], py[MAXL]; int mate[MAXL]; int Sx, Sy; int A[2][2]; int cx, cy; int sym; int gi; } Cross;
/* g(X) with scaled centre: n g(X) = A (n X) + (I - A) S ; returns 0 if not integral */
static int apply_g(const Cross *C, const int A[2][2], int Sx, int Sy, int n, int x, int y, int *ox, int *oy) {
  long nx = (long)n * x, ny = (long)n * y;
  long gx = A[0][0] * nx + A[0][1] * ny + (Sx - (A[0][0] * Sx + A[0][1] * Sy));
  long gy = A[1][0] * nx + A[1][1] * ny + (Sy - (A[1][0] * Sx + A[1][1] * Sy));
  (void)C;
  if (gx % n || gy % n) return 0;
  *ox = (int)(gx / n); *oy = (int)(gy / n); return 1;
}
/* crossing data of cycle c (length l) at bilayer kb, far side relative to the root c[0] */
static void crossing(const int *c, int l, int kb, Cross *C) {
  int rootup = upper_side(c[0], kb);
  C->n = 0; int at[MAXL];         /* at[i] = crossing index of the vertical kb-bond (c[i], c[i+1]) or -1 */
  for (int i = 0; i < l; i++) { at[i] = -1; int a = c[i], b = c[(i + 1) % l];
    int k1, x1, y1, u1, k2, x2, y2, u2; DEC(a, &k1, &x1, &y1, &u1); DEC(b, &k2, &x2, &y2, &u2);
    if (k1 == kb && k2 == kb) { at[i] = C->n; C->px[C->n] = x1; C->py[C->n] = y1; C->n++; } }
  C->Sx = C->Sy = 0; for (int i = 0; i < C->n; i++) { C->Sx += C->px[i]; C->Sy += C->py[i]; }
  /* far arcs: after crossing bond i the walk is on the far side iff c[i+1] is far */
  for (int i = 0; i < l; i++) if (at[i] >= 0) { int nxt = c[(i + 1) % l];
      if (upper_side(nxt, kb) != rootup) { int j = (i + 1) % l; while (at[j] < 0) j = (j + 1) % l; C->mate[at[i]] = at[j]; C->mate[at[j]] = at[i]; } }
  C->sym = 0; C->gi = -1;
  if (C->n == 0) { C->sym = 1; return; }
  int s = curS[kb];   /* lattice letter of kb in the network being enumerated */
  for (int g = 0; g < NINV; g++) {
    int img[MAXL], ok = 1;
    for (int i = 0; i < C->n && ok; i++) { int gx, gy; if (!apply_g(C, INV[g], C->Sx, C->Sy, C->n, C->px[i], C->py[i], &gx, &gy)) { ok = 0; break; }
      img[i] = -1; for (int j = 0; j < C->n; j++) if (C->px[j] == gx && C->py[j] == gy) img[i] = j; if (img[i] < 0) ok = 0; }
    if (!ok) continue;
    /* toggle test on a point of letter s+1 */
    int tx, ty; if (!apply_g(C, INV[g], C->Sx, C->Sy, C->n, C->px[0] + 1, C->py[0] + 1, &tx, &ty)) continue;
    if (!(mod3(tx) == mod3(s + 2) && mod3(ty) == mod3(s + 2))) continue;
    for (int i = 0; i < C->n && ok; i++) if (img[C->mate[i]] != C->mate[img[i]]) ok = 0;
    if (!ok) continue;
    C->sym = 1; C->gi = g; memcpy(C->A, INV[g], sizeof(int) * 4); return;
  }
}

/* ---------- enumeration ---------- */
static void (*visit)(const int *c, int l);
static void bfs_root(const int *s, int root) {
  int n = K * W * W * 2; for (int i = 0; i < n; i++) dist[i] = 1 << 20;
  int h = 0, t = 0; queue[t++] = root; dist[root] = 0;
  while (h < t) { int v = queue[h++]; if (dist[v] >= L / 2) continue; int o[4]; nbrs(s, v, o);
    for (int i = 0; i < 4; i++) { if (o[i] < 0) { fprintf(stderr, "WINDOW TOO SMALL\n"); exit(2); }
      if (dist[o[i]] > dist[v] + 1) { dist[o[i]] = dist[v] + 1; queue[t++] = o[i]; } } }
}
static int ROOT;
static void dfs(int v, int len) {
  int o[4]; nbrs(curS, v, o);
  for (int i = 0; i < 4; i++) { int w = o[i]; if (w < 0) { fprintf(stderr, "WINDOW TOO SMALL (dfs)\n"); exit(2); }
    if (w == ROOT) { if (len >= 2 && path[1] < v) visit(path, len + 1); continue; }
    if (onp[w] || dist[w] > L - (len + 1)) continue;
    onp[w] = 1; path[len + 1] = w; dfs(w, len + 1); onp[w] = 0; }
}
static void enumerate(const int *s, void (*f)(const int *, int)) {
  curS = s; visit = f; bfs_root(s, ROOT); onp[ROOT] = 1; path[0] = ROOT; dfs(ROOT, 0); onp[ROOT] = 0;
}

/* ---------- per-cycle work ---------- */
static long totG[MAXL + 1], symG[MAXL + 1], rigG[MAXL + 1], badimg[MAXL + 1], profbad[MAXL + 1], tot2[MAXL + 1], sym2[MAXL + 1], rig2[MAXL + 1];
static long rhist[MAXL + 1][8], rhist2[MAXL + 1][8];
static int minrig = 999, minrig2 = 999;
static void profile(const int *c, int l, int *pr) { memset(pr, 0, sizeof(int) * K);
  for (int i = 0; i < l; i++) { int k1, x1, y1, u1, k2, x2, y2, u2; DEC(c[i], &k1, &x1, &y1, &u1); DEC(c[(i + 1) % l], &k2, &x2, &y2, &u2); if (k1 == k2) pr[k1]++; } }
static void print_cycle(const char *tag, const int *c, int l) {
  printf("D %s %d", tag, l); for (int i = 0; i < l; i++) { int k, x, y, u; DEC(c[i], &k, &x, &y, &u); printf(" %d %d %d %d", k, x, y, u); } printf("\n");
}
static int nrigid(const int *c, int l) { int r = 0; Cross C; for (int kb = 0; kb < K; kb++) { crossing(c, l, kb, &C); if (!C.sym) r++; } return r; }
static void visitG(const int *c, int l) {
  totG[l]++;
  int r = nrigid(c, l); rhist[l][r < 7 ? r : 7]++; if (r && l < minrig) minrig = l;
  Cross C; crossing(c, l, kf, &C);
  if (!C.sym) { rigG[l]++; if (dump && l >= dumpmin) print_cycle("G", c, l); if (mode == 0) return; }
  symG[l] += C.sym;
  int rootup = upper_side(c[0], kf);
  int A[2][2]; int Sx = C.Sx, Sy = C.Sy, n = C.n;
  if (mode == 0) { if (n) memcpy(A, C.A, sizeof A); }
  else if (mode == 1) { int H[2][2] = {{-1, 0}, {0, -1}}; memcpy(A, H, sizeof A); if (n) { Sx = C.px[0]; Sy = C.py[0]; n = 1; } }
  else if (mode == 2) { int I[2][2] = {{1, 0}, {0, 1}}; memcpy(A, I, sizeof A); n = 0; }
  else { int Rm[2][2] = {{0, -1}, {1, 1}}; memcpy(A, Rm, sizeof A); if (n) { Sx = C.px[0]; Sy = C.py[0]; n = 1; } }
  /* image as an EDGE SET: root-side edges kept, far-side edges moved by g, each crossing bond kept at its root-side atom
     (g(P) = P, so the vertical bonds used are the same); then walk it from the root: it must be one polygon of G2 */
  int ea[MAXL], eb[MAXL]; int ok = 1;
  for (int i = 0; i < l && ok; i++) {
    int a = c[i], b = c[(i + 1) % l], fa = upper_side(a, kf) != rootup, fb = upper_side(b, kf) != rootup;
    int v2[2] = {a, b}, f2[2] = {fa, fb};
    if (fa != fb) { int r = fa ? b : a; int k, x, y, u; DEC(r, &k, &x, &y, &u); ea[i] = r; eb[i] = ID(k, x, y, 1 - u); continue; }
    for (int e = 0; e < 2; e++) {
      if (!f2[e] || n == 0) continue;
      int k, x, y, u; DEC(v2[e], &k, &x, &y, &u); int gx, gy;
      if (!apply_g(&C, A, Sx, Sy, n, x, y, &gx, &gy) || gx < -R || gx > R || gy < -R || gy > R) { ok = 0; break; }
      v2[e] = ID(k, gx, gy, u); }
    ea[i] = v2[0]; eb[i] = v2[1];
  }
  int im[MAXL];
  if (ok) for (int i = 0; i < l && ok; i++) if (!is_atom(s2, ea[i]) || !is_atom(s2, eb[i]) || !adjacent(s2, ea[i], eb[i])) ok = 0;
  if (ok) {   /* walk: every atom must lie on exactly two image edges and the walk from the root must close after l edges */
    int used[MAXL] = {0}; int cur = c[0], prev = -1;
    for (int step = 0; step < l && ok; step++) {
      im[step] = cur; int nx = -1, cntn = 0, ei = -1;
      for (int i = 0; i < l; i++) if (ea[i] == cur || eb[i] == cur) { cntn++; if (!used[i] && nx < 0) { ei = i; nx = ea[i] == cur ? eb[i] : ea[i]; } }
      if (cntn != 2 || nx < 0) { ok = 0; break; }
      used[ei] = 1; prev = cur; cur = nx;
    }
    (void)prev;
    if (ok && cur != c[0]) ok = 0;
    if (ok) for (int i = 0; i < l && ok; i++) for (int j = i + 1; j < l; j++) if (im[i] == im[j]) { ok = 0; break; }
  }
  if (!ok) { badimg[l]++; return; }
  int p1[64], p2[64]; profile(c, l, p1); profile(im, l, p2); if (memcmp(p1, p2, sizeof(int) * K)) profbad[l]++;
  push(&st2img[l], im, l);
}
static void visit2(const int *c, int l) {
  tot2[l]++;
  int r = nrigid(c, l); rhist2[l][r < 7 ? r : 7]++; if (r && l < minrig2) minrig2 = l;
  Cross C; crossing(c, l, kf, &C);
  if (!C.sym) { rig2[l]++; if (dump && l >= dumpmin) print_cycle("H", c, l); return; }
  sym2[l]++; push(&st2sym[l], c, l);
}
int main(void) {
  if (scanf("%d %d %d %d %d %d %d %d", &L, &K, &kr, &ur, &kf, &mode, &dump, &dumpmin) != 8) return 1;
  for (int k = 0; k < K; k++) if (scanf("%d", &sG[k]) != 1) return 1;
  if (L > MAXL || K > 64) return 1;
  R = 3 * L + 6; W = 2 * R + 1;
  make_group();
  /* G2: far side letters swapped by sigma */
  int rootup = (ur == 1 && kr == kf) || kr > kf;
  for (int k = 0; k < K; k++) { int far = rootup ? (k < kf) : (k > kf);
    s2[k] = far ? mod3(-sG[kf] - sG[k]) : sG[k]; }   /* sigma(t) = 2 s[kf] - t = -s[kf] - t mod 3 */
  for (int k = 0; k < K; k++) if (k > 0 && (s2[k] == s2[k - 1] || sG[k] == sG[k - 1])) { fprintf(stderr, "bad letters\n"); return 1; }
  int n = K * W * W * 2; dist = malloc(sizeof(int) * n); onp = calloc(n, 1); queue = malloc(sizeof(int) * n);
  rx = ry = sG[kr]; ROOT = ID(kr, rx, ry, ur);
  enumerate(sG, visitG);
  enumerate(s2, visit2);
  int allok = 1;
  for (int l = 4; l <= L; l += 2) {
    long ni = st2img[l].n, ns = st2sym[l].n; int eq = (ni == ns), dup = 0;
    CL = l;
    if (ni) qsort(st2img[l].a, ni, sizeof(int) * l, cmpc_int);
    if (ns) qsort(st2sym[l].a, ns, sizeof(int) * l, cmpc_int);
    for (long i = 1; i < ni; i++) if (!memcmp(st2img[l].a + (i - 1) * l, st2img[l].a + i * l, sizeof(int) * l)) dup++;
    if (eq && ni) eq = !memcmp(st2img[l].a, st2sym[l].a, sizeof(int) * l * ni);
    printf("LEN %d totG %ld symG %ld rigG %ld badimg %ld dupimg %d profbad %ld setequal %d tot2 %ld sym2 %ld rig2 %ld\n",
           l, totG[l], symG[l], rigG[l], badimg[l], dup, profbad[l], eq, tot2[l], sym2[l], rig2[l]);
    printf("RIGIDHIST %d G", l); for (int r = 0; r < 8; r++) printf(" %ld", rhist[l][r]); printf(" G2"); for (int r = 0; r < 8; r++) printf(" %ld", rhist2[l][r]); printf("\n");
    if (mode == 0 && (badimg[l] || dup || profbad[l] || !eq)) allok = 0;
    free(st2img[l].a); free(st2sym[l].a); st2img[l].a = st2sym[l].a = NULL; st2img[l].n = st2sym[l].n = st2img[l].cap = st2sym[l].cap = 0;
  }
  if (mode != 0) { long nb = 0; for (int l = 4; l <= L; l++) nb += badimg[l]; allok = nb > 0; }   /* a wrong twist must break */
  printf("MINRIGID G %d G2 %d\n", minrig, minrig2);
  printf("END %s\n", allok ? "ok" : "FAIL");
  return 0;
}
