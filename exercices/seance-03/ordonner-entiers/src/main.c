#include <stdio.h>

void echanger_entiers(int *a, int *b)
{
  // TODO 
}

void ordonner_entiers(int *a, int *b)
{
   // TODO
}

int main(void)
{
    int a = 1;
    int b = 2;

    ordonner_entiers(&a, &b);
    printf("ordonne: a=%d b=%d\n", a, b);

    a = 2;
    b = 1;
    ordonner_entiers(&a, &b);
    printf("inverse: a=%d b=%d\n", a, b);

    a = 4;
    b = 4;
    ordonner_entiers(&a, &b);
    printf("egal: a=%d b=%d\n", a, b);
    return 0;
}
