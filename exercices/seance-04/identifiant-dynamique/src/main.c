#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *construire_identifiant(const char *prenom, const char *nom)
{
    /*
     * TODO : réserver strlen(prenom) + strlen(nom) + 2 octets, construire
     * "prenom.nom" avec strcpy et strcat, puis retourner cette nouvelle chaîne.
     */
    (void)prenom;
    (void)nom;
    return NULL;
}

int main(void)
{
    char *ada = construire_identifiant("Ada", "Lovelace");
    char *alan = construire_identifiant("Alan", "Turing");

    if (ada == NULL || alan == NULL) {
        free(ada);
        free(alan);
        return 1;
    }
    assert(strcmp(ada, "Ada.Lovelace") == 0);
    assert(strcmp(alan, "Alan.Turing") == 0);
    printf("%s\n", ada);
    printf("%s\n", alan);
    free(ada);
    free(alan);
    return 0;
}
