#include <stdio.h>

void swap_val(int a, int b)
{
    int tmp = a;
    a = b;
    b = tmp;
}

void swap_ptr(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int main(void)
{
    int a = 1;
    int b = 2;

    swap_val(a, b);
    printf("apres swap_val: a=%d b=%d\n", a, b);

    swap_ptr(&a, &b);
    printf("apres swap_ptr: a=%d b=%d\n", a, b);
    return 0;
}

