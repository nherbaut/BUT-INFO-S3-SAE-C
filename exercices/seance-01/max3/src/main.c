#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int a;
    int b;
    int c;
    int max;

    scanf("%d %d %d", &a, &b, &c);

    max = a;
    if (b > max) {
        max = b;
    }
    if (c > max) {
        max = c;
    }

    printf("max = %d\n", max);
    return 0;
}
