# Seance 1 - Premiers programmes C

## Objectifs

- Situer le langage C dans la programmation systeme.
- Lire et expliquer un programme C minimal.
- Compiler et executer un programme court dans le navigateur.
- Retrouver le meme exercice dans le depot local.
- Identifier les ressemblances et differences initiales avec Java.
- Manipuler des variables, conditions, boucles et tableaux simples.

## Pourquoi programmer en C ?

Ce cours prepare la programmation systeme. La programmation d'application vise
souvent a construire des logiciels directement utiles aux utilisateurs. La
programmation systeme construit plutot les outils, bibliotheques et interfaces
utilises par d'autres programmes.

Une bibliotheque expose une interface de programmation, ou API : une liste de
fonctions, types et constantes que le programmeur peut appeler. L'API UNIX est
historiquement concue pour etre utilisee en C. Comprendre le C aide donc a lire
la documentation systeme, a appeler les fonctions du systeme et a comprendre ce
qui se passe sous les abstractions plus haut niveau.

Le C est aussi un langage proche de la machine : les valeurs, les adresses, les
zones memoire et les fichiers y sont manipules explicitement. Cette proximite
est une contrainte, mais aussi un outil pour former un modele mental solide de
l'execution d'un programme.

## Reperes historiques

Le langage C apparait au debut des annees 1970, dans le contexte du systeme
UNIX, avec Dennis Ritchie et Ken Thompson. Il est influence par BCPL et B, puis
popularise par le livre *The C Programming Language* de Brian Kernighan et
Dennis Ritchie.

Quelques reperes suffisent pour ce cours :

- 1972 : developpement de C avec UNIX.
- 1978 : publication du livre K&R.
- 1989 : standard ANSI C, souvent appele C89.
- 1990 : standard ISO C90.
- 1999 : C99.
- 2011 : C11, la base retenue dans nos options de compilation.

::: quiz {#quiz-s1-histoire}
title: Reperes C et UNIX

::: question {#q-s1-c-systeme}
title: Pourquoi le C est-il utile avant la programmation systeme ?
description: On cherche surtout le lien avec les API systeme.

- [x] Parce que l'API UNIX est historiquement exposee en C
- [ ] Parce que le C cache toujours la memoire au programmeur
  hint: Au contraire, le C rend beaucoup de manipulations memoire explicites.
- [x] Parce qu'il aide a comprendre les appels de bibliotheques bas niveau
- [ ] Parce que C est une variante de Java
:::
:::

## Programme minimal

Un programme C contient une fonction `main`. C'est le point d'entree execute au
lancement du programme.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    printf("Hello World!\n");
    return EXIT_SUCCESS;
}
```

Ce programme :

- inclut des declarations fournies par des fichiers d'en-tete ;
- appelle `printf` pour afficher sur la sortie standard ;
- termine la ligne avec `\n` ;
- retourne un code de fin d'execution au systeme.

La forme `int main(void)` indique que `main` ne recoit aucun argument et retourne
un entier. Par convention, ce code de retour indique si le programme s'est termine
correctement. `EXIT_SUCCESS`, defini dans `stdlib.h`, exprime une terminaison
reussie.

## Fichiers d'en-tete

Un fichier d'en-tete, ou header, contient des declarations necessaires au
compilateur. Il ne contient pas forcement le code complet de la fonction appelee,
mais il annonce son existence et sa forme.

Dans l'exemple precedent :

- `#include <stdio.h>` donne acces a la declaration de `printf` ;
- `#include <stdlib.h>` donne acces a `EXIT_SUCCESS` ;
- les chevrons `<...>` designent un header fourni par le systeme ou la
  bibliotheque standard.

Cette distinction entre declaration et definition deviendra essentielle avec la
compilation separee en seance 2.

## Afficher avec `printf`

`printf` ecrit du texte sur la sortie standard. Le caractere `\n` represente un
retour a la ligne.

```c
printf("Bonjour\n");
```

L'affichage produit par `printf` n'est pas le code de retour du programme. Le
code de retour est la valeur renvoyee par `return` dans `main`. Les deux notions
sont visibles par le systeme, mais elles ne servent pas au meme usage.

{{ c_demo: exercices/seance-01/moyenne }}

::: quiz {#quiz-s1-programme-minimal}
title: Programme minimal

::: question {#q-s1-main-headers}
title: Quelles affirmations sont correctes ?
description: On considere le programme `hello.c` minimal.

- [x] `main` est le point d'entree du programme
- [x] `stdio.h` declare notamment `printf`
- [ ] `printf` definit le code de retour du programme
  hint: Le code de retour vient de l'instruction `return` de `main`.
- [x] `\n` permet d'afficher un retour a la ligne
:::
:::

## Compiler et executer

Pendant cette premiere seance, les exercices peuvent etre lances dans le
navigateur. Cela permet de se concentrer d'abord sur le langage : variables,
conditions, boucles et affichage.

La commande locale complete sera reprise en seance 2. Retenir seulement l'idee
generale :

```bash
gcc -std=c11 -Wall -Wextra -pedantic -g hello.c -o hello
./hello
```

`gcc` transforme le fichier source `hello.c` en executable. Les options activent
un dialecte C precise et des avertissements utiles.

## Variables et types simples

Une variable C contient directement une valeur du type annonce. Pour un premier
programme, on peut raisonner comme en Java sur les entiers, les conditions et les
boucles, mais il faut garder en tete que C fait peu de controles automatiques.

```c
int note = 12;
int seuil = 10;

if (note >= seuil) {
    printf("valide\n");
}
```

Le type `int` represente un entier. La variable `note` contient ici la valeur
`12`, pas une reference vers un objet.

::: quiz {#quiz-s1-types}
title: Types et variables

::: question {#q-s1-variable-int}
title: Que stocke une variable `int` ?
description: On declare `int note = 12;`.

- [x] Une valeur entiere copiee dans la variable
- [ ] Une reference vers un objet Java
  hint: En C, une variable simple contient directement sa valeur.
- [ ] Une chaine de caracteres
:::
:::

## Conditions

Les conditions ressemblent a Java sur la syntaxe de base.

```c
if (a > b) {
    printf("a est plus grand\n");
} else {
    printf("b est plus grand ou egal\n");
}
```

L'exercice suivant demande d'identifier un maximum. Il sert a verifier les
conditions, les variables et l'affichage.

{{ c_exercise: exercices/seance-01/max3 }}

## Boucles

Les boucles `while` et `for` existent aussi en C.

```c
int i;
for (i = 0; i < 5; i++) {
    printf("%d\n", i);
}
```

La boucle ci-dessus affiche les valeurs de `0` a `4`. Cette convention est
importante pour les tableaux : le premier indice est `0`.

## Tableaux simples

Du point de vue algorithmique, un tableau est une collection de donnees du meme
type, accessibles par un indice entier. En C, un tableau est aussi une zone
memoire contenant des elements consecutifs.

```c
int notes[3] = {12, 14, 9};
```

Ici, `notes` contient trois entiers. Les indices valides sont `0`, `1` et `2`.

```c
int somme = 0;
int i;

for (i = 0; i < 3; i++) {
    somme += notes[i];
}

printf("somme = %d\n", somme);
```

Pour cette seance, on retient surtout :

- tous les elements d'un tableau ont le meme type ;
- l'indice du premier element est `0` ;
- la taille indiquee dans une declaration reserve de la place ;
- acceder hors des bornes est une erreur que C ne detecte pas toujours.

::: quiz {#quiz-s1-tableaux}
title: Tableaux simples

::: question {#q-s1-indices-tableau}
title: Quelles affirmations decrivent un tableau C simple ?
description: On declare `int notes[3] = {12, 14, 9};`.

- [x] Le premier element est `notes[0]`
- [x] Le tableau contient des elements de meme type
- [ ] `notes[3]` designe le troisieme element
  hint: Avec trois elements, les indices valides sont 0, 1 et 2.
- [x] La declaration reserve de la place pour trois entiers
:::
:::

## Tester par entrees/sorties attendues

Au debut du cours, les tests peuvent rester simples : on donne des valeurs en
entree standard et on compare la sortie produite a une sortie attendue.

Exemple de commande locale :

```bash
printf "12 14\n" | ./moyenne
```

Le programme lit les valeurs comme si elles avaient ete tapees au clavier.

## Executer dans le navigateur

Le player integre a la page compile et execute des programmes courts. Il ne
remplace pas GCC/Clang, mais il suffit pour manipuler les premieres notions sans
installer l'outillage pendant la seance 1.

Pour chaque exercice :

- lire le code ;
- modifier une partie limitee ;
- lancer `Build & Run` ;
- observer les sorties du compilateur et du programme.

## Retrouver l'exercice dans le depot local

Les memes exercices existent dans le depot. Quand l'environnement local est
utilise, les commandes deviennent :

```bash
cd exercices/seance-01/moyenne
make run
make test
```

La prise en main detaillee de `gcc`, des Makefiles et de l'organisation des
fichiers est l'objectif de la seance 2.

## Presentation rapide du projet

- Theme general.
- Livrables.
- Jalons non encadres.
- Evaluation individuelle finale.

Le projet n'est pas developpable entierement des la seance 1. Le travail non
encadre peut deja porter sur la lecture du sujet, les specifications, les cas de
test attendus et la comprehension de l'organisation du depot.

## Exercices proposes

- Hello personnalise : afficher un message et retourner `EXIT_SUCCESS`.
- Calcul de moyenne.
- Maximum de trois entiers.
- Comptage des notes superieures a 10.
- Somme des elements d'un tableau d'entiers.
- Table de multiplication.
