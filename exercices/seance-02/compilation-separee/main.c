#include <stdio.h>

#include "stats.h"

int main(void)
{
    int notes[] = {12, 14, 10};
    size_t count = sizeof notes / sizeof notes[0];

    printf("moyenne = %.2f\n", moyenne(notes, count));
    printf("max = %d\n", maximum(notes, count));
    return 0;
}

