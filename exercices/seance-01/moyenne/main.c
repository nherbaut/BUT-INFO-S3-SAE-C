#include <stdio.h>

int main(void)
{
    int a;
    int b;
    int moyenne;

    scanf("%d %d", &a, &b);

    moyenne = (a + b) / 2;
    printf("moyenne = %d\n", moyenne);
    return 0;
}
