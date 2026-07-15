#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t size = 3;
    size_t i;
    int sum = 0;
    int *values = malloc(size * sizeof *values);

    if (values == NULL) {
        perror("malloc");
        return 1;
    }

    for (i = 0; i < size; i++) {
        values[i] = (int)i + 1;
    }

    size = 5;
    int *resized = realloc(values, size * sizeof *values);
    if (resized == NULL) {
        free(values);
        perror("realloc");
        return 1;
    }
    values = resized;

    values[3] = 4;
    values[4] = 5;

    for (i = 0; i < size; i++) {
        sum += values[i];
    }

    printf("taille=%zu somme=%d\n", size, sum);
    free(values);
    return 0;
}

