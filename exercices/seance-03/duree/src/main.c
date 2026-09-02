#include <stdio.h>

struct Duree {
    int heures;
    int minutes;
    int secondes;
};

void normaliser_duree(struct Duree *duree)
{
    /*
     * À compléter : modifiez les champs pointés pour obtenir une durée
     * normalisée. Utilisez duree->heures, duree->minutes et duree->secondes.
     */
}

int main(void)
{
    struct Duree duree = {
        .heures = 0,
        .minutes = 123,
        .secondes = 78
    };

    normaliser_duree(&duree);
    printf("duree = %d h %d min %d s\n", duree.heures, duree.minutes,
           duree.secondes);
    return 0;
}
