/* maxclique.c: our own exact maximum-clique search (Tomita-style branch and bound with greedy colouring bound, bitsets), written
   12 Nov 2026 to check the Ramsey witnesses of Cremer, "Lower bounds for Ramsey numbers: R(6,8) >= 135 and R(8,10) >= 345"
   (aiXiv 2610.01289, ai-discovered). Input: n lines of n characters 0/1 (adjacency of the red graph). Output: n, red edge count,
   symmetric/zero-diagonal check, omega(red), omega(blue = complement). Usage: maxclique file.txt */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 512
#define W ((MAXN+63)/64)
static int n, nw; static uint64_t adj[MAXN][W]; static int best;
static int popc(const uint64_t *a){int c=0;for(int i=0;i<nw;i++)c+=__builtin_popcountll(a[i]);return c;}
static void expand(uint64_t *P, int size){
  /* greedy colouring of P for bounds */
  int order[MAXN], col[MAXN], k=0; uint64_t U[W]; memcpy(U,P,sizeof(uint64_t)*nw);
  int color=0;
  while(1){ int any=0; for(int i=0;i<nw;i++) if(U[i]){any=1;break;} if(!any)break; color++;
    uint64_t Q[W]; memcpy(Q,U,sizeof(uint64_t)*nw);
    for(int i=0;i<nw;i++) while(Q[i]){ int b=__builtin_ctzll(Q[i]); int v=i*64+b; Q[i]&=Q[i]-1;
        U[v>>6]&=~(1ULL<<(v&63)); for(int j=0;j<nw;j++) Q[j]&=~adj[v][j]; order[k]=v; col[k]=color; k++; } }
  for(int t=k-1;t>=0;t--){ if(size+col[t]<=best) return; int v=order[t];
    uint64_t NP[W]; int empty=1; for(int j=0;j<nw;j++){ NP[j]=P[j]&adj[v][j]; if(NP[j])empty=0; }
    if(empty){ if(size+1>best) best=size+1; } else expand(NP,size+1);
    P[v>>6]&=~(1ULL<<(v&63)); }
}
static int omega(void){ uint64_t P[W]; memset(P,0,sizeof P); for(int v=0;v<n;v++) P[v>>6]|=1ULL<<(v&63); best=0; expand(P,0); return best; }
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); if(!f){perror("open");return 2;} char line[4096]; n=0; static char M[MAXN][MAXN+2];
  while(fgets(line,sizeof line,f)){ int L=strlen(line); while(L&&(line[L-1]=='\n'||line[L-1]=='\r'||line[L-1]==' '))line[--L]=0; if(!L)continue; memcpy(M[n],line,L+1); n++; }
  fclose(f); nw=(n+63)/64; long red=0; int ok=1;
  for(int i=0;i<n;i++){ if((int)strlen(M[i])!=n){ok=0;} for(int j=0;j<n;j++){ int r=M[i][j]=='1'; if(r!=(M[j][i]=='1'))ok=0; if(i==j&&r)ok=0; if(r&&i<j)red++; } }
  memset(adj,0,sizeof adj);
  for(int i=0;i<n;i++)for(int j=0;j<n;j++) if(i!=j&&M[i][j]=='1') adj[i][j>>6]|=1ULL<<(j&63);
  int wr=omega();
  memset(adj,0,sizeof adj);
  for(int i=0;i<n;i++)for(int j=0;j<n;j++) if(i!=j&&M[i][j]!='1') adj[i][j>>6]|=1ULL<<(j&63);
  int wb=omega();
  printf("n %d red_edges %ld symmetric_zero_diagonal %s omega_red %d omega_blue %d\n",n,red,ok?"yes":"NO",wr,wb);
  return 0;
}
