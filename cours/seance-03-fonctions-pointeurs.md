# Phase 3 - Fonctions, pointeurs et structures

## Objectifs

- Comprendre que les arguments C sont toujours passés par copie.
- Transmettre une adresse pour modifier une variable de l'appelant.
- Distinguer pointeur et valeur pointée avec `*`.
- Écrire des fonctions d'échange, d'ordonnancement et de normalisation.
- Déclarer une structure et accéder à ses champs avec `.` et `->`.
- Tester avec `assert`.

## Passage par valeur et adresse

Une fonction C reçoit toujours des copies de ses arguments. Modifier un
paramètre entier ne modifie donc pas la variable de l'appelant. Pour déposer
un résultat dans cette variable, on transmet une copie de son adresse avec `&`.

```c
#include <stdio.h>

#include <stdio.h>

void demander_entier(const char question[], int *adresse_reponse)
{
    printf("%s\n", question);
    scanf("%d", adresse_reponse);
}

int main(void)
{
    int a;
    int b;

    demander_entier("Combien vaut a ?", &a);
    demander_entier("Combien vaut b ?", &b);
    printf("la somme vaut %d\n", a + b);
    return 0;
}

```

`adresse_reponse` contient déjà une adresse : il ne faut donc pas écrire
`&adresse_reponse` dans l'appel a `scanf`.

::: quiz {#quiz-s3-passage}
title: Passage d'arguments

::: question {#q-s3-copie-adresse}
title: Que reçoit une fonction appelée avec `f(&x)` ?
description: On veut modifier indirectement une variable externe.

- [ ] La variable `x` elle-meme
  hint: Les arguments C sont toujours passes par copie.
- [x] Une copie de l'adresse de `x`
- [ ] Une référence vers `x`
:::
:::

## Pointeurs et déréférencement

Dans `int *adresse_reponse`, `*adresse_reponse` désigne l'entier stocké à
l'adresse pointée. On peut donc lire ou modifier la variable de l'appelant.

```c
void demander_entier_positif(const char question[], int *adresse_reponse)
{
    do {
        printf("%s\\n", question);
        scanf("%d", adresse_reponse);
    } while (*adresse_reponse < 0);
}
```

Comparer `adresse_reponse < 0` comparerait une adresse, pas la valeur lue.
Dans `int *p, q;`, seul `p` est un pointeur ; `q` est un entier. Préférez une
déclaration par ligne.

::: quiz {#quiz-s3-declaration-pointeur}
title: Lire une déclaration de pointeur

::: question {#q-s3-int-star-p-q}
title: Quels sont les types dans `int *p, q;` ?
description: L'étoile appartient au déclarateur de `p`.

- [x] `p` est un pointeur vers `int` et `q` est un `int`
- [ ] `p` et `q` sont tous les deux des pointeurs vers `int`
  hint: Il faudrait écrire `int *p, *q;`.
- [ ] `p` est un `int` et `q` est un pointeur vers `int`
:::
:::

## Échanger et ordonner deux entiers

Pour échanger deux valeurs, une fonction doit recevoir leurs adresses et les
déréférencer. L'exemple compare l'échange par valeur et l'échange par pointeur.

{{ c_demo: exercices/seance-03/swap }}

{{ c_exercise: exercices/seance-03/ordonner-entiers }}

## Structures

Une structure regroupe des valeurs qui décrivent la même entité. Le mot-clé
`struct` fait partie du nom du type.

```c
struct Duree {
    int heures;
    int minutes;
    int secondes;
};

struct Duree pause = {
    .heures = 1,
    .minutes = 23,
    .secondes = 45
};

void ajouter_une_minute(struct Duree *duree)
{
    duree->minutes++;
    /* equivalent a : (*duree).minutes++; */
}
```

Les initialiseurs désignés rendent le code lisible. On utilise `.` avec une
structure et `->` avec un pointeur vers une structure.

## Énumérations

```technical
Une énumération définit un type dont les valeurs possibles portent un nom. Elle
évite de représenter un choix par des nombres sans signification explicite.

~~~c
typedef enum {
    TEMPERATURE_INDOOR,
    TEMPERATURE_OUTDOOR
} TemperatureKind;
~~~

Sans valeur indiquée, `TEMPERATURE_INDOOR` vaut `0`, puis
`TEMPERATURE_OUTDOOR` vaut `1`. Une fonction recevant un `TemperatureKind` doit
malgré tout vérifier la valeur reçue : un cast peut produire une valeur qui ne
correspond à aucun membre de l'énumération.
```

Dans le projet capteurs, `TemperatureKind` indique si une fonction doit traiter
la température intérieure ou extérieure.

## Tester avec `assert`

`assert(condition)` arrête le programme si la condition est fausse et indique
la ligne fautive. Il permet de tester des cas normaux et limites sans saisie.

```c
#include <assert.h>

assert(minutes >= 0 && minutes < 60);
assert(secondes >= 0 && secondes < 60);
```

Une fonction comme `afficher_duree(const struct Duree *duree)` reçoit une
adresse pour éviter de copier la structure. `const` interdit sa modification.

## Exercice final : normaliser une durée

Une durée peut avoir plus de 59 minutes ou secondes. Complétez
`normaliser_duree` : elle reçoit l'adresse d'une `struct Duree` et doit
modifier ses champs avec la notation `->`. La structure est initialisée avec
les valeurs `0`, `123` et `78` ; le programme doit afficher `2 h 4 min 18 s`.

Cet exercice de synthèse réunit l'initialisation d'une structure, le passage de
son adresse avec `&`, le déréférencement et la notation `->`. Il est entièrement
exécutable dans le navigateur.

{{ c_exercise: exercices/seance-03/duree }}
