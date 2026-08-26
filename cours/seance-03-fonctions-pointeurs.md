# Seance 3 - Fonctions et pointeurs

## Objectifs

- Comprendre les fonctions C.
- Installer un modele unique : les arguments sont passes par copie.
- Manipuler des pointeurs sans multiplier les modeles mentaux.
- Manipuler les chaines C et les pointeurs generiques `void *`.
- Definir et manipuler des structures par valeur et par pointeur.

## Fonctions C et methodes Java

## Prototypes

## Passage d'arguments par copie

## Copier une valeur

## Copier une adresse

::: quiz {#quiz-s3-passage}
title: Passage d'arguments

::: question {#q-s3-copie-adresse}
title: Que recoit une fonction appelee avec `f(&x)` ?
description: On veut modifier indirectement une variable externe.

- [ ] La variable `x` elle-meme
  hint: Les arguments C sont toujours passes par copie.
- [x] Une copie de l'adresse de `x`
- [ ] Une reference Java vers `x`
:::
:::

## Modifier une variable locale pointeur

## Modifier l'objet pointe

## Chaines de caracteres

Une chaine C est un tableau de `char` termine par le caractere nul `\0`.
Cette terminaison fait partie des donnees: elle permet aux fonctions de savoir
ou la chaine s'arrete.

Les fonctions usuelles sont `strlen` pour mesurer une chaine, `strcmp` pour la
comparer, `memcpy` pour copier des octets et `snprintf` pour produire un texte
borne. Une copie de chaine doit reserver une place supplementaire pour `\0`.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    const char source[] = "C11";
    char destination[16];
    size_t length = strlen(source);

    memcpy(destination, source, length + 1);
    printf("%s (%zu caracteres)\n", destination, length);
    return 0;
}
```

## Pointeur generique `void *` et callback

`void *` est une adresse sans type precis. Une fonction qui recoit une telle
adresse doit savoir quel objet est reellement pointe et la convertir avant de
l'utiliser. Une fonction peut aussi etre passee comme valeur: c'est un callback.
La bibliotheque fournie du projet capteurs emploie ce mecanisme pour recevoir les
octets telecharges; les etudiants ne l'implementent pas dans le projet.

```c
#include <stdio.h>

typedef void (*Callback)(void *data);

static void afficher_entier(void *data)
{
    int *value = data;

    printf("%d\n", *value);
}

int main(void)
{
    int value = 42;
    Callback callback = afficher_entier;

    callback(&value);
    return 0;
}
```

{{ c_demo: exercices/seance-03/swap }}

## Definir une `struct`

## Initialiser une structure

## Passer une structure par valeur

## Passer une structure par pointeur

Les types `TemperatureMeasure`, `MeasureSeries` et `TemperatureStatistics` du
projet capteurs sont les structures a lire avant le travail autonome.

## Structures contenant des pointeurs

{{ c_exercise: exercices/seance-03/etudiants }}

## Visualiser avec Python Tutor C

## Tester localement

```bash
cd exercices/seance-03/swap
make test
```

## Exercices proposes

- Fonctions `min`, `max`, `moyenne`.
- `swap` impossible par valeurs.
- `swap` avec pointeurs.
- Fonction qui produit deux resultats via pointeurs.
- Structure contenant une chaine, une valeur et un pointeur.
