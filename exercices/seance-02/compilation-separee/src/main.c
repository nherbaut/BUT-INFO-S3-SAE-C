#include <stdio.h>

double moyenne(const int values[], size_t count)
{
    int sum = 0;
    size_t i;

    if (count == 0) {
        return 0.0;
    }

    for (i = 0; i < count; i++) {
        sum += values[i];
    }
    return (double)sum / (double)count;
}

int maximum(const int values[], size_t count)
{
    int max = values[0];
    size_t i;

    for (i = 1; i < count; i++) {
        if (values[i] > max) {
            max = values[i];
        }
    }
    return max;
}

int main(void)
{
    int notes[] = {12, 14, 10};
    size_t count = sizeof notes / sizeof notes[0];

    printf("moyenne = %.2f\n", moyenne(notes, count));
    printf("max = %d\n", maximum(notes, count));
    return 0;
}
