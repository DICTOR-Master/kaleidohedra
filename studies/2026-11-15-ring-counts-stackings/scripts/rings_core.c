/* rings_core.c - exact cycle (ring) enumeration through given root sites of a 4-regular network.
   stdin:  n L nroots / n lines of 4 neighbour ids (-1 = outside the window) / nroots root ids
   For each root and each length l <= L it counts
     every simple cycle (self-avoiding polygon) through the root, each cycle once,
     the shortest-path (SP) rings among them: cycles C with d_G(a,b) = d_C(a,b) for all vertices a,b of C
       (no shortcut; the primitive-ring criterion as used by Franzblau 1991 and Yuan-Cormack 2002),
   in total and per bond at the root (bond k = edge root - neighbour k).
   stdout: "R <root> <l> <cycles> <sp> <c0> <c1> <c2> <c3> <s0> <s1> <s2> <s3>" for l = 3..L, then "DONE <root>".
   Exits with status 2 if a vertex within distance L of a root lacks a neighbour (window too small). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, L, *nb, *distr, *bidx, *ball, B, *queue, *stamp, stampv = 0, *tmpd;
static unsigned char *D;   /* B x B distances among ball vertices, capped at 255 */
static int path[64], onpath_dummy;
static unsigned char *onp;
static long long cyc[64], sp[64], cb[64][4], sb[64][4];
static int root, half;
static void bfs_root(void) {
  for (int i = 0; i < n; i++) distr[i] = -1;
  int h = 0, t = 0; queue[t++] = root; distr[root] = 0;
  while (h < t) { int v = queue[h++];
    if (distr[v] >= L) continue;
    for (int k = 0; k < 4; k++) { int w = nb[4*v+k];
      if (w < 0) { fprintf(stderr, "WINDOW TOO SMALL at vertex %d (distance %d from root %d)\n", v, distr[v], root); exit(2); }
      if (distr[w] < 0) { distr[w] = distr[v] + 1; queue[t++] = w; } } }
  B = 0; for (int i = 0; i < t; i++) { int v = queue[i]; if (distr[v] <= half) { bidx[v] = B; ball[B++] = v; } else bidx[v] = -1; }
  for (int i = t; i < n; i++) ; 
}
static void ball_distances(void) {
  D = realloc(D, (size_t)B * B);
  memset(D, 255, (size_t)B * B);
  for (int a = 0; a < B; a++) {
    stampv++; int h = 0, t = 0; queue[t++] = ball[a]; stamp[ball[a]] = stampv; tmpd[ball[a]] = 0;
    while (h < t) { int v = queue[h++]; if (bidx[v] >= 0 && distr[v] <= half) D[(size_t)a*B + bidx[v]] = (unsigned char)tmpd[v];
      if (tmpd[v] >= half) continue;
      for (int k = 0; k < 4; k++) { int w = nb[4*v+k]; if (stamp[w] != stampv) { stamp[w] = stampv; tmpd[w] = tmpd[v] + 1; queue[t++] = w; } } }
  }
}
static int is_sp(int l) {
  for (int i = 0; i < l; i++) { int bi = bidx[path[i]];
    for (int j = i + 2; j < l; j++) { int r = j - i; if (l - r < r) r = l - r;
      if (D[(size_t)bi*B + bidx[path[j]]] < r) return 0; } }
  return 1;
}
static int nbindex(int v, int w) { for (int k = 0; k < 4; k++) if (nb[4*root+k] == w) return k; return -1; }
static void dfs(int v, int len) {
  for (int k = 0; k < 4; k++) { int w = nb[4*v+k];
    if (w == root) { if (len + 1 >= 3 && len >= 2 && path[1] < v) { int l = len + 1; int s = is_sp(l);
        int b1 = nbindex(root, path[1]), b2 = nbindex(root, v);
        cyc[l]++; cb[l][b1]++; cb[l][b2]++; if (s) { sp[l]++; sb[l][b1]++; sb[l][b2]++; } }
      continue; }
    if (onp[w] || distr[w] > L - (len + 1)) continue;
    onp[w] = 1; path[len + 1] = w; dfs(w, len + 1); onp[w] = 0; }
}
int main(void) {
  int nr; if (scanf("%d %d %d", &n, &L, &nr) != 3) return 1; half = L / 2;
  nb = malloc(sizeof(int) * 4 * n); for (int i = 0; i < 4 * n; i++) if (scanf("%d", &nb[i]) != 1) return 1;
  distr = malloc(sizeof(int) * n); bidx = malloc(sizeof(int) * n); ball = malloc(sizeof(int) * n); queue = malloc(sizeof(int) * n);
  stamp = calloc(n, sizeof(int)); tmpd = malloc(sizeof(int) * n); onp = calloc(n, 1); D = NULL;
  for (int r = 0; r < nr; r++) { if (scanf("%d", &root) != 1) return 1;
    memset(cyc, 0, sizeof cyc); memset(sp, 0, sizeof sp); memset(cb, 0, sizeof cb); memset(sb, 0, sizeof sb);
    bfs_root(); ball_distances();
    onp[root] = 1; path[0] = root; dfs(root, 0); onp[root] = 0;
    for (int l = 3; l <= L; l++) printf("R %d %d %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld\n", root, l, cyc[l], sp[l], cb[l][0], cb[l][1], cb[l][2], cb[l][3], sb[l][0], sb[l][1], sb[l][2], sb[l][3]);
    printf("DONE %d ball %d\n", root, B); fflush(stdout); }
  return 0;
}
