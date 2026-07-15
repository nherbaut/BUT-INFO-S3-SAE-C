#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int a;
    int b;
    int max;

    scanf("%d %d", &a, &b);

    int *toto=(int *)malloc(sizeof(int));
    toto++;
    toto=NULL;
    max = a;
    if (b > max) {
        max = b;
    }

    printf("max = %d\n", max);
    return 0;
}
