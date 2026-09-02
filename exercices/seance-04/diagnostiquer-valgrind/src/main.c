#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void fuite_simple(void)
{
    int *values = malloc(3 * sizeof *values);

    if (values == NULL) {
        return;
    }
    values[0] = 10;
    values[1] = 20;
    values[2] = 30;
    printf("somme = %d\n", values[0] + values[1] + values[2]);
    /* TODO : corriger la fuite sans supprimer l'allocation. */
}

static void pointeur_perdu(void)
{
    char *message = malloc(16);

    if (message == NULL) {
        return;
    }
    strcpy(message, "bonjour");
    printf("%s\n", message);
    message = NULL;
    /* TODO : corriger la perte de la dernière adresse de l'allocation. */
}

static void double_liberation(void)
{
    int *value = malloc(sizeof *value);

    if (value == NULL) {
        return;
    }
    *value = 42;
    printf("value = %d\n", *value);
    free(value);
    free(value);
    /* TODO : conserver une seule libération de cette allocation. */
}

static void acces_apres_free(void)
{
    int *value = malloc(sizeof *value);

    if (value == NULL) {
        return;
    }
    *value = 7;
    free(value);
    printf("value = %d\n", *value);
    /* TODO : ne plus lire value après sa libération. */
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s SCENARIO\n", argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "fuite") == 0) {
        fuite_simple();
    } else if (strcmp(argv[1], "pointeur-perdu") == 0) {
        pointeur_perdu();
    } else if (strcmp(argv[1], "double-free") == 0) {
        double_liberation();
    } else if (strcmp(argv[1], "apres-free") == 0) {
        acces_apres_free();
    } else if (strcmp(argv[1], "aide") == 0) {
        printf("scenarios: fuite pointeur-perdu double-free apres-free\n");
    } else {
        fprintf(stderr, "scenario inconnu: %s\n", argv[1]);
        return 1;
    }
    return 0;
}
