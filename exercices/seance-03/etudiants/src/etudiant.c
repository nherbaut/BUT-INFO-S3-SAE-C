#include "projet/etudiant.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Etudiant {
    char *nom;
    double moyenne;
};

static char *copie_chaine(const char *source)
{
    size_t len = strlen(source) + 1;
    char *copy = malloc(len);

    if (copy != NULL) {
        memcpy(copy, source, len);
    }
    return copy;
}

Etudiant *etudiant_creer(const char *nom, double moyenne)
{
    Etudiant *e = malloc(sizeof *e);

    if (e == NULL) {
        return NULL;
    }

    e->nom = copie_chaine(nom);
    if (e->nom == NULL) {
        free(e);
        return NULL;
    }

    e->moyenne = moyenne;
    return e;
}

void etudiant_afficher(const Etudiant *e)
{
    printf("%s: %.2f\n", e->nom, e->moyenne);
}

void etudiant_liberer(Etudiant *e)
{
    if (e != NULL) {
        free(e->nom);
        free(e);
    }
}
