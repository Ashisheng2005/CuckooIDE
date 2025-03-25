#include <bits/stdc++.h>
using namespace std;
long long a[2000001];

int main()
{
    long long n, m, x;
    cin >> n >> m;
    for (int i=1; i<=n; ++i) cin >> a[i];
    for (int i=1; i<=m; ++i) {
    cin >> x;
    cout << a[x] << endl;
    }
    return 0;
}









