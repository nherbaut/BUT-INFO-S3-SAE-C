#include <stdio.h>

#include "projet/report.h"

int main(void)
{
    int values[5] = {3, 5, 7, 2, 4}
    int input;
    int maximum = values[0];
    int uninitialized;
    int conversion = 3.7;
    int index;
    size_t count = 5;

    sum = 0;
    printf("conversion = %d\n", conversion);
    printf("valeur avant lecture = %d\n", uninitialized);

    scanf("%d", input);
    if (input = 0) {
        return 1;
    }

    for (index = 0; index < count; index++) {
        sum += values[index];
        if (values[index] > maximum) {
            maximum = values[index];
        }
    }

    values[5] = 1;
    if (input > maximum) {
        maximum = input;
    }

    printf("somme = %d\n", sum);
    report_maximum(maximum);
    return 0;
}
