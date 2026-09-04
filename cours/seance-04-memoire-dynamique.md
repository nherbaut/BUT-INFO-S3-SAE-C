# Phase 4 - Mémoire dynamique et fichiers

## Objectifs

- Distinguer allocations automatique, statique et dynamique.
- Comprendre la durée de vie des données sur la pile, dans les données et dans le tas.
- Utiliser `malloc`, `free` et `realloc` de manière sûre.
- Diagnostiquer fuites, doubles libérations et accès invalides avec Valgrind.
- Découvrir les opérations de base sur les fichiers avec `FILE *`.

## Les trois durées de vie

### Allocation automatique : la pile

Les variables locales d'une fonction sont allouées automatiquement sur la pile
d'appels. L'espace est réservé lors de l'appel de la fonction et restitué quand
la fonction se termine. Une adresse vers une variable locale ne doit donc pas
être utilisée après le retour de la fonction.

```c
void afficher_carre(int valeur)
{
    int carre = valeur * valeur;

    printf("%d\n", carre);
} /* carre cesse d'exister ici */
```

### Allocation statique : les données du programme

Une variable globale existe pendant toute l'exécution. Une variable locale
déclarée `static` a la même durée de vie, mais sa portée reste limitée à sa
fonction. Utilisez-la seulement lorsqu'un état persistant est nécessaire.

```c
int appels_total = 0;

void compter_appel(void)
{
    static int appels_locaux = 0;

    appels_total++;
    appels_locaux++;
}
```

### Allocation dynamique : le tas

Le tas (*heap*) sert aux données dont la taille n'est pas connue à la
compilation ou dont la durée de vie doit dépasser l'appel de fonction courant.
Une allocation dynamique reste valide jusqu'à son appel explicite à `free`.

```c
int *tableau_carres(size_t count)
{
    int *values = malloc(count * sizeof *values);

    if (values == NULL) {
        return NULL;
    }
    for (size_t i = 0; i < count; i++) {
        values[i] = (int)(i * i);
    }
    return values;
}
```

::: quiz {#quiz-s4-duree-vie}
title: Durée de vie des données

::: question {#q-s4-duree-vie}
title: Quelles affirmations sont correctes ?
description: On compare les trois formes d'allocation en C.

- [x] Une variable locale ordinaire cesse d'exister à la fin de son appel de fonction.
- [x] Une variable `static` locale conserve sa valeur entre deux appels.
- [x] Une zone obtenue par `malloc` reste allouée jusqu'à `free`.
- [ ] Une zone du tas est libérée automatiquement à la fin du bloc qui contient `malloc`.
  hint: Ce comportement concerne les variables automatiques, pas le tas.
:::
:::

## Pratique de l'allocation dynamique

### `malloc` : réserver une zone

`malloc` reçoit un nombre d'octets et retourne l'adresse du premier octet de la
zone réservée, ou `NULL` si l'allocation échoue. En C, le résultat est converti
implicitement vers le type de pointeur attendu : il ne faut pas le convertir
explicitement.

```c
size_t count = 20;
struct Personne *personnes = malloc(count * sizeof *personnes);

if (personnes == NULL) {
    return 1;
}
```

`sizeof *personnes` évite de répéter le nom du type et reste correct si ce type
évolue. Les éléments d'une zone fraîchement allouée ne sont pas initialisés.

### Fil rouge : un annuaire extensible

```c
struct Date {
    int jour;
    int mois;
    int annee;
};

struct Personne {
    char *nom;
    char *prenom;
    struct Date naissance;
};

struct Annuaire {
    size_t taille;
    struct Personne *tableau;
};
```

L'annuaire associe une taille à l'adresse de son tableau de personnes. Sa
structure contient une adresse ; les chaînes de caractères et le tableau devront
avoir des règles de propriété claires avant toute libération.

### `free` : libérer une zone

Chaque zone obtenue par `malloc`, `calloc` ou `realloc` doit être libérée une
fois lorsqu'elle n'est plus utile. Il faut conserver l'adresse jusqu'à cet
appel, sinon la zone devient inaccessible : c'est une fuite mémoire.

```c
free(annuaire.tableau);
annuaire.tableau = NULL;
annuaire.taille = 0;
```

Mettre le pointeur à `NULL` est une précaution utile contre sa réutilisation et
une double libération accidentelle. `free(NULL)` n'a aucun effet.

::: quiz {#quiz-s4-free}
title: Libérer une allocation

::: question {#q-s4-free}
title: Que faut-il faire avec une zone obtenue par `malloc` ?
description: On alloue un tableau dynamique.

- [x] Appeler `free` quand la zone n'est plus utile.
- [x] Éviter d'utiliser le pointeur après la libération.
- [x] Conserver l'adresse jusqu'à l'appel à `free`.
- [ ] Attendre la fin du bloc : la zone sera libérée automatiquement.
  hint: Seules les variables automatiques suivent cette règle.
:::
:::

### `realloc` : redimensionner une zone

`realloc` reçoit l'adresse d'une allocation existante et sa nouvelle taille. Il
peut conserver l'adresse ou déplacer la zone ; dans ce second cas, il copie la
partie des données qui tient dans la nouvelle allocation. Les nouveaux octets ne
sont pas initialisés.

Ne réaffectez pas directement le résultat à votre unique pointeur : en cas
d'échec, `realloc` retourne `NULL` et l'ancienne zone est toujours valide. Un
pointeur temporaire permet de la libérer proprement ou de continuer à l'utiliser.

```c
struct Personne *redimensionne = realloc(
    annuaire.tableau, nouvelle_taille * sizeof *annuaire.tableau);

if (redimensionne == NULL) {
    return 0;
}
annuaire.tableau = redimensionne;
annuaire.taille = nouvelle_taille;
```

{{ c_exercise: exercices/seance-04/tableau-dynamique }}

::: quiz {#quiz-s4-realloc}
title: Redimensionnement

::: question {#q-s4-realloc}
title: Pourquoi utiliser un pointeur temporaire avec `realloc` ?
description: L'allocation peut échouer.

- [x] Pour ne pas perdre l'adresse de l'ancienne zone si `realloc` retourne `NULL`.
- [x] Parce que l'adresse de la zone peut changer après une réallocation réussie.
- [ ] Parce que `realloc` initialise toujours les nouveaux éléments à zéro.
  hint: Les octets supplémentaires ne sont pas initialisés.
:::
:::

## Chaînes de caractères C

Une chaîne C est une suite d'octets terminée par l'octet nul `\0`. Cette
terminaison fait partie de la donnée : les fonctions de `<string.h>` s'en servent
pour trouver la fin de la chaîne. Un `char` représente un octet ; avec UTF-8, un
caractère visible peut occuper plusieurs octets.

```c
char prenom[] = "Ada";

printf("%s\n", prenom);
/* Le tableau contient 'A', 'd', 'a', '\0'. */
```

### Littéral ou tableau modifiable

Ces deux déclarations ne désignent pas la même zone mémoire :

```c
const char *lecture_seule = "abc";
char modifiable[] = "abc";

modifiable[0] = 'A';
```

Un littéral peut être partagé et ne doit pas être modifié. Le déclarer `const`
rend cette règle visible. La seconde forme réserve un tableau de quatre octets,
dont un pour `\0`, et son contenu peut être changé.

### Copier et comparer des chaînes

On ne copie pas une chaîne avec `=` après sa déclaration : cette opération
copierait seulement une adresse. `<string.h>` fournit notamment `strlen`,
`strcmp`, `strcpy`, `strcat` et `strdup`.

| Fonction | Rôle | Précaution |
| --- | --- | --- |
| `strlen(s)` | Longueur avant `\0` | Ne compte pas l'octet final. |
| `strcmp(a, b)` | Compare deux chaînes | Retourne `0` si elles sont égales. |
| `strcpy(dest, src)` | Copie `src` dans `dest` | `dest` doit être assez grand. |
| `strcat(dest, src)` | Ajoute `src` à la fin de `dest` | `dest` doit avoir assez de place. |
| `strdup(src)` | Alloue puis retourne une copie de `src` | Vérifier le retour, puis appeler `free`. |

`strcpy` et `strdup` copient le même contenu, y compris le `\0` final, mais
ne gèrent pas la mémoire de la même façon. Avec `strcpy`, la destination existe
déjà : c'est au programme de réserver un buffer assez grand. Avec `strdup`, la
fonction réserve exactement la place nécessaire dans le tas et retourne son
adresse ; la copie doit donc être libérée avec `free`.

```c
char buffer[32];
char *copie;

strcpy(buffer, "Ada");        // buffer a déjà été réservé
copie = strdup("Ada");        // copie est NULL en cas d'échec
if (copie != NULL) {
    /* utiliser copie */
    free(copie);
}
```

`strdup` est une fonction POSIX courante, mais pas une fonction du standard C
ISO. Dans un environnement où elle n'est pas disponible, on peut écrire son
équivalent avec `malloc`, `strlen` et `memcpy` ci-dessous.

Pour un buffer de taille connue, `snprintf` est souvent plus sûr : il limite le
nombre d'octets écrits et termine la chaîne quand la taille est non nulle.

```c
char nom_complet[64];

snprintf(nom_complet, sizeof nom_complet, "%s %s", "Ada", "Lovelace");
```

::: quiz {#quiz-s4-string-h}
title: Fonctions de `string.h`

::: question {#q-s4-string-h-contrats}
title: Quels contrats sont corrects ?
description: On manipule des chaînes C correctement terminées par `\0`.

- [x] `strlen("Ada")` retourne `3`.
- [x] `strcmp(a, b)` retourne `0` lorsque les deux chaînes ont le même contenu.
- [x] `strcpy(dest, src)` exige que `dest` puisse contenir `src` et son `\0` final.
- [x] `strcat(dest, src)` conserve le contenu initial de `dest` puis ajoute `src`.
- [ ] `strcpy` alloue automatiquement la mémoire nécessaire à `dest`.
  hint: La destination doit être réservée avant l'appel.
- [x] Le résultat non nul de `strdup(source)` doit être libéré avec `free`.
- [ ] `strlen` compte l'octet nul final.
  hint: La longueur est le nombre d'octets avant `\0`.
:::
:::

### Copier une chaîne dans le tas

Quand la taille est déterminée à l'exécution, on réserve `strlen(source) + 1`
octets : le `+ 1` est indispensable pour `\0`. La fonction qui reçoit ce
pointeur devient responsable de l'appel à `free`.

```c
char *copie_chaine(const char *source)
{
    size_t taille = strlen(source) + 1;
    char *copie = malloc(taille);

    if (copie != NULL) {
        memcpy(copie, source, taille);
    }
    return copie;
}
```

Cette règle s'applique aux champs `char *nom` et `char *prenom` d'un annuaire :
libérer un annuaire implique aussi de libérer les chaînes qu'il possède.


::: quiz {#quiz-s4-chaines}
title: Chaînes C

::: question {#q-s4-chaines-terminaison}
title: Quelles affirmations sont correctes ?
description: On manipule des chaînes terminées par `\0`.

- [x] `char texte[] = "abc";` réserve quatre octets.
- [x] Une copie dynamique doit réserver `strlen(source) + 1` octets.
- [ ] `strlen("abc")` vaut `4`.
  hint: `strlen` ne compte pas l'octet nul final.
- [ ] Il est sûr d'écrire dans le littéral pointé par `const char *texte`.
  hint: Un littéral est en lecture seule ; `const` l'indique.
:::
:::



{{ c_exercise: exercices/seance-04/identifiant-dynamique }}


## Erreurs mémoire courantes

- **Fuite mémoire** : perdre la dernière adresse vers une zone allouée sans
  l'avoir libérée.
- **Double libération** : appeler deux fois `free` sur la même allocation.
- **Accès après libération** : lire ou écrire par un pointeur après `free`.
- **Dépassement de tableau** : accéder à un indice hors des bornes réservées.

Ces erreurs peuvent sembler fonctionner lors d'un essai puis provoquer des
résultats aléatoires ou une panne sur une autre machine. Elles doivent être
corrigées, non contournées.

## Diagnostiquer avec Valgrind

Valgrind exécute le programme et signale les accès mémoire invalides et les
fuites. Depuis un exercice ou le projet :

```bash
make memcheck
```

Lisez la première erreur rapportée : elle indique généralement l'accès fautif
et sa pile d'appels. Corrigez-la avant d'interpréter les erreurs suivantes.

{{ c_exercise: exercices/seance-04/diagnostiquer-valgrind }}

## Fichiers

Un fichier ouvert est représenté par un `FILE *` fourni par `<stdio.h>`. Son
contenu interne est opaque ; il faut seulement transmettre ce pointeur aux
fonctions de la bibliothèque.

```c
FILE *file = fopen("donnees.txt", "r");

if (file == NULL) {
    perror("donnees.txt");
    return 1;
}

/* lire ou écrire le fichier */
fclose(file);
```

Les modes les plus courants sont `r` pour lire un fichier existant, `w` pour
écrire en créant ou écrasant le fichier, et `a` pour ajouter à la fin. Un fichier
ouvert doit être fermé avec `fclose`, surtout après une écriture.

Les fonctions `fprintf` et `fscanf` sont les équivalents formatés de `printf`
et `scanf` sur un fichier. `fgets` et `fputs` lisent ou écrivent des chaînes ;
`fgetc` et `fputc` traitent un caractère. `getline` peut agrandir la mémoire
de sa chaîne avec `realloc` et doit donc être suivi de la libération de cette
chaîne.

```remember
Les énumérations vues en phase 3 peuvent aussi servir à nommer des constantes.
Dans l'exercice suivant, `TEXTE_MAX` et `LIGNE_MAX` remplacent ainsi des tailles
« magiques » par des noms qui documentent leur rôle.
```

{{ c_exercise: exercices/seance-04/annuaire-csv }}

## Exercices proposés

- Écrire `afficher_annuaire(const struct Annuaire *annuaire)`.
- Écrire `detruire_annuaire(struct Annuaire *annuaire)` et remettre ses champs
  dans un état vide après `free`.
- Écrire `ajouter_personne` avec `realloc` et un pointeur temporaire.
- Sauvegarder puis recharger un annuaire avec `fopen`, `fprintf`, `fscanf` et
  `fclose`.
- Diagnostiquer une fuite, une double libération et un accès après libération
  avec Valgrind.
