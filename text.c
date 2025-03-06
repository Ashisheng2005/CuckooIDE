#include <stdio.h>
#define SEC 60;

int Sum(int n){
    int sum=0;
    for(int i=0; i <= n;i++){
        sum = sum + i;
    }
    return sum;
}


void main()
{
    int n;
    scanf("%d", &n);
    printf("from zero to %d sum is %d", n, Sum(n));
    
    
}




