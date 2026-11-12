/* Enumerate every 0/1 wall labelling of a Coxeter fan that closes around every face (= every equal-edged member of the closed
   deformation cone of the Coxeter permutohedron, up to translation), keep one representative per orbit of the fan's symmetry
   group (lexicographically least image), and report dimension and orbit size. Purely combinatorial: the allowed labellings of
   each face were computed exactly in gp_setup.py, so nothing here is floating point.

   gcc -O2 -o gp_enum gp_enum.c
   gp_enum enum IN SHARD NSHARDS OUT     -> OUT: lines "R dim orbit hex"; stdout: PROGRESS and totals
   gp_enum sub IN REPS CAP OUT           -> for each rep (hex per line in REPS), number of members P <= Q (capped at CAP),
                                            and with CAP >= 0 also every such P (lines "S idx hex") when the count is < CAP */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXE 192
#define W 3
typedef struct { uint64_t w[W]; } bits;

int E, NF, NR, G;
int wallroot[MAXE];
int fm[200], fw[200][10], fna[200], *fal[200];
uint32_t cop[16][16];
int (*perm)[MAXE];
int order[200], nfixed[200], fpos[200][10];   /* per depth: positions of the face already fixed by earlier faces */
signed char val[MAXE];

static int bget(const bits *b, int e) { return (b->w[e >> 6] >> (e & 63)) & 1; }
static void bset(bits *b, int e) { b->w[e >> 6] |= 1ULL << (e & 63); }
static int bitcmp(const bits *a, const bits *b) {
  for (int i = W - 1; i >= 0; i--) { if (a->w[i] < b->w[i]) return -1; if (a->w[i] > b->w[i]) return 1; }
  return 0;
}
static void hexout(FILE *f, const bits *b) { fprintf(f, "%016llx%016llx%016llx", (unsigned long long)b->w[2], (unsigned long long)b->w[1], (unsigned long long)b->w[0]); }
static bits hexin(const char *s) {
  bits b; char t[17]; t[16] = 0;
  for (int i = 0; i < 3; i++) { memcpy(t, s + 16 * i, 16); b.w[2 - i] = strtoull(t, NULL, 16); }
  return b;
}

void readin(const char *fn) {
  FILE *f = fopen(fn, "r"); if (!f) { perror(fn); exit(2); }
  if (fscanf(f, "%d %d %d %d", &E, &NF, &NR, &G) != 4) exit(2);
  for (int e = 0; e < E; e++) if (fscanf(f, "%d", &wallroot[e]) != 1) exit(2);
  for (int i = 0; i < NF; i++) {
    if (fscanf(f, "%d", &fm[i]) != 1) exit(2);
    for (int k = 0; k < fm[i]; k++) if (fscanf(f, "%d", &fw[i][k]) != 1) exit(2);
    if (fscanf(f, "%d", &fna[i]) != 1) exit(2);
    fal[i] = malloc(sizeof(int) * fna[i]);
    for (int k = 0; k < fna[i]; k++) if (fscanf(f, "%d", &fal[i][k]) != 1) exit(2);
  }
  for (int i = 0; i < NR; i++) for (int j = 0; j < NR; j++) if (fscanf(f, "%u", &cop[i][j]) != 1) exit(2);
  perm = malloc(sizeof(int[MAXE]) * G);
  for (int g = 0; g < G; g++) for (int e = 0; e < E; e++) if (fscanf(f, "%d", &perm[g][e]) != 1) exit(2);
  fclose(f);
  /* face order: greedily the face with most walls already covered */
  char used[200] = {0}, cov[MAXE] = {0};
  for (int d = 0; d < NF; d++) {
    int best = -1, bs = -1;
    for (int i = 0; i < NF; i++) if (!used[i]) { int s = 0; for (int k = 0; k < fm[i]; k++) s += cov[fw[i][k]]; if (s > bs) { bs = s; best = i; } }
    used[best] = 1; order[d] = best; nfixed[d] = 0;
    for (int k = 0; k < fm[best]; k++) { if (cov[fw[best][k]]) fpos[d][nfixed[d]++] = k; cov[fw[best][k]] = 1; }
  }
}

int dimof(const bits *b) {
  uint32_t m = 0;
  for (int e = 0; e < E; e++) if (bget(b, e)) m |= 1u << wallroot[e];
  if (!m) return 0;
  int i = __builtin_ctz(m); uint32_t r = m & (m - 1);
  if (!r) return 1;
  int j = __builtin_ctz(r);
  return ((m & ~cop[i][j]) == 0) ? 2 : 3;
}

/* ---------------- enum mode ---------------- */
long long nsol = 0, nrep[4] = {0}, nsoldim[4] = {0};
FILE *fout;
int SPLIT = 3, shard, nshards; long long branch = 0, nbranch_total = 0, nbranch_done = 0; int counting = 0;
time_t tstart, tlast;

void found(void) {
  bits b = {{0}};
  for (int e = 0; e < E; e++) if (val[e]) bset(&b, e);
  nsol++;
  int d = dimof(&b); nsoldim[d]++;
  int stab = 0;
  for (int g = 0; g < G; g++) {
    bits im = {{0}};
    for (int e = 0; e < E; e++) if (bget(&b, e)) bset(&im, perm[g][e]);
    int c = bitcmp(&im, &b);
    if (c < 0) return;
    if (c == 0) stab++;
  }
  nrep[d]++;
  fprintf(fout, "R %d %d ", d, G / stab); hexout(fout, &b); fputc('\n', fout);
}

void dfs(int d) {
  if (d == SPLIT && !counting) {
    long long my = branch++;
    if (my % nshards != shard) return;
  }
  if (d == SPLIT && counting) { nbranch_total++; return; }
  if (d == NF) { found(); return; }
  int f = order[d];
  int fixmask = 0, fixval = 0;
  for (int t = 0; t < nfixed[d]; t++) { int k = fpos[d][t]; fixmask |= 1 << k; if (val[fw[f][k]]) fixval |= 1 << k; }
  for (int a = 0; a < fna[f]; a++) {
    int m = fal[f][a];
    if ((m & fixmask) != fixval) continue;
    for (int k = 0; k < fm[f]; k++) if (!(fixmask >> k & 1)) val[fw[f][k]] = (m >> k) & 1;
    dfs(d + 1);
    if (d == SPLIT - 1 && !counting) {
      if (((branch - 1) % nshards) == shard) {
        nbranch_done++;
        time_t now = time(NULL);
        if (now - tlast >= 20) { tlast = now; printf("PROGRESS %.4f shard %d branches %lld/%lld sols %lld reps %lld/%lld/%lld/%lld %lds\n",
          (double)nbranch_done * nshards / (nbranch_total ? nbranch_total : 1), shard, nbranch_done * nshards, nbranch_total, nsol,
          nrep[0], nrep[1], nrep[2], nrep[3], (long)(now - tstart)); fflush(stdout); }
      }
    }
  }
  for (int k = 0; k < fm[f]; k++) if (!(fixmask >> k & 1)) val[fw[f][k]] = -1;
}

/* ---------------- sub mode ---------------- */
long long subcount, subcap; FILE *subout; int subidx;
int sfixed[200], sfpos[200][10];
void sdfs(int d) {
  if (subcount >= subcap) return;
  if (d == NF) {
    subcount++;
    if (subout) { fprintf(subout, "S %d ", subidx); bits b = {{0}}; for (int e = 0; e < E; e++) if (val[e] == 1) bset(&b, e); hexout(subout, &b); fputc('\n', subout); }
    return;
  }
  int f = order[d];
  int fixmask = 0, fixval = 0;
  for (int k = 0; k < fm[f]; k++) if (val[fw[f][k]] >= 0) { fixmask |= 1 << k; if (val[fw[f][k]]) fixval |= 1 << k; }
  int setmask = 0;
  for (int a = 0; a < fna[f]; a++) {
    int m = fal[f][a];
    if ((m & fixmask) != fixval) continue;
    setmask = ~fixmask & ((1 << fm[f]) - 1);
    for (int k = 0; k < fm[f]; k++) if (setmask >> k & 1) val[fw[f][k]] = (m >> k) & 1;
    sdfs(d + 1);
    for (int k = 0; k < fm[f]; k++) if (setmask >> k & 1) val[fw[f][k]] = -1;
    if (subcount >= subcap) return;
  }
}

int main(int argc, char **argv) {
  if (argc < 2) return 2;
  readin(argv[2]);
  tstart = tlast = time(NULL);
  if (!strcmp(argv[1], "enum")) {
    shard = atoi(argv[3]); nshards = atoi(argv[4]);
    fout = fopen(argv[5], "w");
    for (int e = 0; e < E; e++) val[e] = -1;
    counting = 1; dfs(0); counting = 0;
    for (int e = 0; e < E; e++) val[e] = -1;
    printf("PROGRESS 0.0000 shard %d start, %lld split branches\n", shard, nbranch_total); fflush(stdout);
    dfs(0);
    fprintf(fout, "T %lld %lld %lld %lld %lld %lld %lld %lld %lld\n", nsol, nsoldim[0], nsoldim[1], nsoldim[2], nsoldim[3], nrep[0], nrep[1], nrep[2], nrep[3]);
    fclose(fout);
    printf("SHARD %d done: solutions %lld (dims 0..3: %lld %lld %lld %lld) reps %lld %lld %lld %lld in %lds\n", shard, nsol,
           nsoldim[0], nsoldim[1], nsoldim[2], nsoldim[3], nrep[0], nrep[1], nrep[2], nrep[3], (long)(time(NULL) - tstart));
    return 0;
  }
  if (!strcmp(argv[1], "sub")) {
    FILE *fr = fopen(argv[3], "r"); subcap = atoll(argv[4]);
    FILE *fo = fopen(argv[5], "w");
    char line[256]; subidx = 0;
    while (fgets(line, sizeof line, fr)) {
      if (strlen(line) < 48) continue;
      bits q = hexin(line);
      for (int e = 0; e < E; e++) val[e] = bget(&q, e) ? -1 : 0;
      subcount = 0; subout = fo;
      long long cap = subcap;
      sdfs(0);
      fprintf(fo, "C %d %lld%s\n", subidx, subcount, subcount >= cap ? "+" : "");
      subidx++;
    }
    fclose(fo); fclose(fr);
    printf("sub done: %d reps\n", subidx);
    return 0;
  }
  return 2;
}
