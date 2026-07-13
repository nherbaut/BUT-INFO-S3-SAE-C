#include <stdio.h>

int main(void)
{
    int a;
    int b;
    int max;

    scanf("%d %d", &a, &b);

    max = a;
    if (b > max) {
        max = b;
    }

    printf("max = %d\n", max);
    return 0;
}
