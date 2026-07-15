#include "projet/carnet.h"

#include <stdlib.h>
#include <string.h>

struct Contact {
    char *nom;
    int age;
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

Contact *contact_creer(const char *nom, int age)
{
    Contact *contact = malloc(sizeof *contact);

    if (contact == NULL) {
        return NULL;
    }

    contact->nom = copie_chaine(nom);
    if (contact->nom == NULL) {
        free(contact);
        return NULL;
    }

    contact->age = age;
    return contact;
}

const char *contact_nom(const Contact *contact)
{
    return contact->nom;
}

int contact_age(const Contact *contact)
{
    return contact->age;
}

void contact_liberer(Contact *contact)
{
    if (contact != NULL) {
        free(contact->nom);
        free(contact);
    }
}
