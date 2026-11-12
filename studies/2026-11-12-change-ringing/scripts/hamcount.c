/* hamcount.c - count (and optionally list) the undirected Hamiltonian cycles of a graph with at most 64 vertices.
   Input (stdin): V, then for each vertex v: deg d, then d neighbours.  Usage: hamcount [list]
   Each cycle is counted once: it starts at vertex 0 and its second vertex is smaller than its last.
   Output: with "list", one line "C v0 v1 ... v(V-1)" per cycle; always a last line "COUNT N".
   DICTO · dictospheres.com - change-ringing study, 12 Nov 2026. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int V, deg[64], nb[64][64], path[64], list;
static uint64_t adj[64];
static long long count;
static void dfs(int v, int depth, uint64_t used) {
  if (depth == V) {
    if ((adj[v] >> 0) & 1ULL) {
      if (path[1] < path[V - 1]) {
        count++;
        if (list) { printf("C"); for (int i = 0; i < V; i++) printf(" %d", path[i]); printf("\n"); }
      }
    }
    return;
  }
  for (int k = 0; k < deg[v]; k++) {
    int w = nb[v][k];
    if (used & (1ULL << w)) continue;
    path[depth] = w;
    dfs(w, depth + 1, used | (1ULL << w));
  }
}
int main(int argc, char **argv) {
  list = (argc > 1 && strcmp(argv[1], "list") == 0);
  if (scanf("%d", &V) != 1 || V < 3 || V > 64) { fprintf(stderr, "bad V\n"); return 2; }
  for (int v = 0; v < V; v++) {
    if (scanf("%d", &deg[v]) != 1) return 2;
    for (int k = 0; k < deg[v]; k++) { if (scanf("%d", &nb[v][k]) != 1) return 2; adj[v] |= 1ULL << nb[v][k]; }
  }
  for (int v = 0; v < V; v++) for (int k = 0; k < deg[v]; k++) { int w = nb[v][k]; if (!((adj[w] >> v) & 1ULL)) { fprintf(stderr, "not symmetric %d %d\n", v, w); return 2; } }
  path[0] = 0;
  dfs(0, 1, 1ULL);
  printf("COUNT %lld\n", count);
  return 0;
}
