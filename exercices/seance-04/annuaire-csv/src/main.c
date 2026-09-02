#include <stdio.h>
#include <stdlib.h>

enum {
    TEXTE_MAX = 32,
    LIGNE_MAX = 128
};

struct Personne {
    char prenom[TEXTE_MAX];
    char nom[TEXTE_MAX];
    int jour;
    int mois;
    int annee;
};

struct Annuaire {
    size_t taille;
    struct Personne *personnes;
};

static int ecrire_csv(const struct Annuaire *annuaire, const char *chemin)
{
    /* TODO : ouvrir chemin en écriture, écrire chaque personne et fermer. */
    (void)annuaire;
    (void)chemin;
    return 0;
}

static int lire_csv(struct Annuaire *annuaire, const char *chemin)
{
    /*
     * TODO : ouvrir chemin en lecture, lire chaque ligne avec fgets, analyser
     * le CSV avec sscanf, agrandir annuaire->personnes avec realloc, puis fermer.
     */
    (void)annuaire;
    (void)chemin;
    return 0;
}

static void afficher_annuaire(const struct Annuaire *annuaire)
{
    size_t i;

    for (i = 0; i < annuaire->taille; i++) {
        const struct Personne *personne = &annuaire->personnes[i];

        printf("%s %s (%02d/%02d/%04d)\n", personne->prenom, personne->nom,
               personne->jour, personne->mois, personne->annee);
    }
}

static void liberer_annuaire(struct Annuaire *annuaire)
{
    free(annuaire->personnes);
    annuaire->personnes = NULL;
    annuaire->taille = 0;
}

int main(int argc, char *argv[])
{
    struct Personne personnes[] = {
        {"Ada", "Lovelace", 10, 12, 1815},
        {"Alan", "Turing", 23, 6, 1912}
    };
    struct Annuaire source = {2, personnes};
    struct Annuaire reconstruit = {0, NULL};

    if (argc != 2) {
        fprintf(stderr, "usage: %s FICHIER.csv\n", argv[0]);
        return 1;
    }
    if (!ecrire_csv(&source, argv[1])) {
        return 1;
    }
    if (!lire_csv(&reconstruit, argv[1])) {
        liberer_annuaire(&reconstruit);
        return 1;
    }
    afficher_annuaire(&reconstruit);
    liberer_annuaire(&reconstruit);
    return 0;
}
