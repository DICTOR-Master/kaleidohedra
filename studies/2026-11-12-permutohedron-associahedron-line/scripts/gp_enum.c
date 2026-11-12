/* Exact vertex candidates of the equal-speed line B (permutohedron -> Loday), any n (used for n = 4, 5, 6).
   DICTO · dictospheres.com - study 2026-11-12-permutohedron-associahedron-line, 13 Nov 2026.

   P(z) = { x : sum x = z_[n], sum_{i in S} x_i >= z_S, S nonempty proper }, coordinates u = (x_1..x_{n-1}), d = n - 1.
   Line B: z_S(s) = C(|S|+1, 2) - s for every non-interval S, C(|S|+1, 2) for intervals, s in [0, smax], smax = max D_S.
   For every d-subset of the 2^n - 2 inequalities with nonzero determinant the solution is u(s) = (P0 + s P1) / det (integers,
   Cramer); it is a vertex exactly on a closed s-interval [lo, hi] (every other inequality is affine in s). All integer arithmetic
   (int64 values, __int128 products), so the intervals are exact rationals.
   Output (stdout): one line per subset whose interval is nonempty:  m_1 .. m_d  det  P0_1 .. P0_d  P1_1 .. P1_d  lo_num lo_den hi_num hi_den
   (m = subset bitmasks, bit i-1 = element i).  stderr: PROGRESS lines and a summary.  Usage: gp_enum n > candidates.txt */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll; typedef __int128 i128;
static int n, d, M; static int mask[1 << 10]; static ll A[1 << 10][9], B0[1 << 10], B1[1 << 10];
static ll gcdll(ll a, ll b) { if (a < 0) a = -a; if (b < 0) b = -b; while (b) { ll t = a % b; a = b; b = t; } return a; }
static ll det(ll m[9][9], int k) {   /* Bareiss, exact for integer matrices */
  ll a[9][9]; for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) a[i][j] = m[i][j];
  ll prev = 1; int sign = 1;
  for (int c = 0; c < k; c++) {
    int p = c; while (p < k && a[p][c] == 0) p++;
    if (p == k) return 0;
    if (p != c) { for (int j = 0; j < k; j++) { ll t = a[c][j]; a[c][j] = a[p][j]; a[p][j] = t; } sign = -sign; }
    for (int i = c + 1; i < k; i++) {
      for (int j = c + 1; j < k; j++) a[i][j] = (ll)(((i128)a[i][j] * a[c][c] - (i128)a[i][c] * a[c][j]) / prev);
      a[i][c] = 0;
    }
    prev = a[c][c];
  }
  return sign * a[k - 1][k - 1];
}
static int isint(int m) { int lo = __builtin_ctz(m), hi = 31 - __builtin_clz(m); return hi - lo + 1 == __builtin_popcount(m); }
static ll C2(ll k) { return k * (k - 1) / 2; }
/* rational compare a/b ? c/e with b, e > 0 */
static int cmpq(ll a, ll b, ll c, ll e) { i128 l = (i128)a * e, r = (i128)c * b; return (l > r) - (l < r); }
int main(int argc, char **argv) {
  n = atoi(argv[1]); d = n - 1; M = 0; int full = (1 << n) - 1;
  ll zE = C2(n + 1); ll smax = 0;
  for (int m = 1; m < full; m++) {
    mask[M] = m; int k = __builtin_popcount(m), hasn = (m >> (n - 1)) & 1;
    for (int i = 0; i < d; i++) A[M][i] = ((m >> i) & 1) - hasn;
    ll D = 0;   /* D_S = C(|S|+1,2) - #intervals inside S */
    { ll ints = 0; int i = 0; while (i < n) { if ((m >> i) & 1) { int j = i; while (j < n && ((m >> j) & 1)) j++; ll L = j - i; ints += L * (L + 1) / 2; i = j; } else i++; }
      D = C2(k + 1) - ints; }
    if (D > smax) smax = D;
    B0[M] = C2(k + 1) - (hasn ? zE : 0); B1[M] = isint(m) ? 0 : -1;
    if (isint(m) && D != 0) { fprintf(stderr, "FAIL D of an interval\n"); return 1; }
    M++;
  }
  fprintf(stderr, "n=%d d=%d M=%d smax=%lld\n", n, d, M, smax);
  int idx[9]; for (int i = 0; i < d; i++) idx[i] = i;
  ll total = 0, nonsing = 0, out = 0; ll ncomb = 1; for (int i = 0; i < d; i++) ncomb = ncomb * (M - i) / (i + 1);
  ll step = ncomb / 20 + 1;
  while (1) {
    total++;
    if (total % step == 0) fprintf(stderr, "PROGRESS %lld/%lld subsets, %lld nonsingular, %lld candidates\n", total, ncomb, nonsing, out);
    ll m[9][9]; for (int r = 0; r < d; r++) for (int c = 0; c < d; c++) m[r][c] = A[idx[r]][c];
    ll D = det(m, d);
    if (D != 0) {
      nonsing++;
      ll P0[9], P1[9];
      for (int c = 0; c < d; c++) {
        ll mm[9][9];
        for (int r = 0; r < d; r++) for (int cc = 0; cc < d; cc++) mm[r][cc] = (cc == c) ? B0[idx[r]] : A[idx[r]][cc];
        P0[c] = det(mm, d);
        for (int r = 0; r < d; r++) mm[r][c] = B1[idx[r]];
        P1[c] = det(mm, d);
      }
      ll dd = D; if (dd < 0) { dd = -dd; for (int c = 0; c < d; c++) { P0[c] = -P0[c]; P1[c] = -P1[c]; } }
      ll lon = 0, lod = 1, hin = smax, hid = 1; int ok = 1;
      for (int k = 0; k < M && ok; k++) {
        i128 al = -(i128)dd * B0[k], be = -(i128)dd * B1[k];
        for (int c = 0; c < d; c++) { al += (i128)A[k][c] * P0[c]; be += (i128)A[k][c] * P1[c]; }
        /* slack * dd = al + be s >= 0 */
        if (be == 0) { if (al < 0) ok = 0; continue; }
        ll a = (ll)al, b = (ll)be;
        if (b > 0) { ll num = -a, den = b; ll g = gcdll(num, den); if (g) { num /= g; den /= g; } if (cmpq(num, den, lon, lod) > 0) { lon = num; lod = den; } }
        else { ll num = a, den = -b; ll g = gcdll(num, den); if (g) { num /= g; den /= g; } if (cmpq(num, den, hin, hid) < 0) { hin = num; hid = den; } }
        if (cmpq(lon, lod, hin, hid) > 0) ok = 0;
      }
      if (ok) {
        out++;
        for (int i = 0; i < d; i++) printf("%d ", mask[idx[i]]);
        printf("%lld", dd); for (int c = 0; c < d; c++) printf(" %lld", P0[c]); for (int c = 0; c < d; c++) printf(" %lld", P1[c]);
        printf(" %lld %lld %lld %lld\n", lon, lod, hin, hid);
      }
    }
    int i = d - 1; while (i >= 0 && idx[i] == M - d + i) i--;
    if (i < 0) break;
    idx[i]++; for (int j = i + 1; j < d; j++) idx[j] = idx[j - 1] + 1;
  }
  fprintf(stderr, "ENUM done n=%d: %lld subsets, %lld nonsingular, %lld candidates (vertex on a nonempty s-interval)\n", n, total, nonsing, out);
  return 0;
}
