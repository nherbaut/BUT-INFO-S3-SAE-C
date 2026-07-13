#include "etudiant.h"

#include <stdio.h>

int main(void)
{
    Etudiant *ada = etudiant_creer("Ada", 15.5);

    if (ada == NULL) {
        fprintf(stderr, "creation impossible\n");
        return 1;
    }

    etudiant_afficher(ada);
    etudiant_liberer(ada);
    return 0;
}

