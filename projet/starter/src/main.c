#include "carnet.h"

#include <stdio.h>

int main(void)
{
    Contact *contact = contact_creer("Grace", 42);

    if (contact == NULL) {
        fprintf(stderr, "creation du contact impossible\n");
        return 1;
    }

    printf("%s (%d ans)\n", contact_nom(contact), contact_age(contact));
    contact_liberer(contact);
    return 0;
}

