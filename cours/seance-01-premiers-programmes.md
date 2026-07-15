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

// pour la compilation dans le navigateur
#ifndef EXIT_SUCCESS
  #define EXIT_SUCCESS 0
#endif

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

`gcc` transforme le fichier source `hello.c` en exécutable. Les options activent
un dialecte C précisé et des avertissements utiles.

## Variables et types simples

Une variable C contient directement une valeur du type annonce. Pour un premier
programme, on peut raisonner comme en Java sur les entiers, les conditions et les
boucles, mais il faut garder en tête que C fait peu de contrôles automatiques.

```c
int note = 12;
int seuil = 10;

if (note >= seuil) {
    printf("valide\n");
}
```

Le type `int` représente un entier. La variable `note` contient ici la valeur
`12`, pas une référence vers un objet.

::: quiz {#quiz-s1-types}
title: Types et variables

::: question {#q-s1-variable-int}
title: Que stocke une variable `int` ?
description: On declare `int note = 12;`.

- [x] Une valeur entière copiée dans la variable
- [ ] Une référence vers un objet Java
  hint: En C, une variable simple contient directement sa valeur.
- [ ] Une chaine de caractères
:::
:::

## Conditions

Les conditions ressemblent à Java sur la syntaxe de base.

```c
if (a > b) {
    printf("a est plus grand\n");
} else {
    printf("b est plus grand ou egal\n");
}
```

L'exercice suivant demande d'identifier un maximum. Il sert à vérifier les
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

Du point de vue algorithmique, un tableau est une collection de données du même
type, accessibles par un indice entier. En C, un tableau est aussi une zone
mémoire contenant des éléments consécutifs.

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

Pour cette séance, on retient surtout :

- tous les éléments d'un tableau ont le même type ;
- l'indice du premier élément est `0` ;
- la taille indiquée dans une déclaration réserve de la place ;
- accéder hors des bornes est une erreur que C ne détecte pas toujours.

::: quiz {#quiz-s1-tableaux}
title: Tableaux simples

::: question {#q-s1-indices-tableau}
title: Quelles affirmations décrivent un tableau C simple ?
description: On declare `int notes[3] = {12, 14, 9};`.

- [x] Le premier élément est `notes[0]`
- [x] Le tableau contient des éléments de même type
- [ ] `notes[3]` désigne le troisième élément
  hint: Avec trois éléments, les indices valides sont 0, 1 et 2.
- [x] La déclaration réserve de la place pour trois entiers
:::
:::

## Tester par entrées/sorties attendues

Au début du cours, les tests peuvent rester simples : on donne des valeurs en
entrée standard et on compare la sortie produite à une sortie attendue.

Exemple de commande locale :

```bash
printf "12 14\n" | ./moyenne
```

Le programme lit les valeurs comme si elles avaient été tapées au clavier.

## Executer dans le navigateur

Le player intègre a la page compile et exécute des programmes courts. Il ne
remplace pas GCC/Clang, mais il suffit pour manipuler les premières notions sans
installer l'outillage pendant la séance 1.

Pour chaque exercice :

- lire le code ;
- modifier une partie limitée ;
- lancer `Build & Run` ;
- observer les sorties du compilateur et du programme.

## Retrouver l'exercice dans le dépôt local

Les mêmes exercices existent dans le dépôt. Quand l'environnement local est
utilisé, les commandes deviennent :

```bash
cd exercices/seance-01/moyenne
make run
make test
```

La prise en main détaillée de `gcc`, des Makefiles et de l'organisation des
fichiers est l'objectif de la séance 2.

## Présentation rapide du projet

- Theme general.
- Livrables.
- Jalons non encadrés.
- Évaluation individuelle finale.

Le projet n'est pas développable entièrement des la séance 1. Le travail non
encadre peut déjà porter sur la lecture du sujet, les spécifications, les cas de
test attendus et la compréhension de l'organisation du dépôt.

## Exercices propose

- Hello personnalise : afficher un message et retourner `EXIT_SUCCESS`.
- Calcul de moyenne.
- Maximum de trois entiers.
- Comptage des notes superieures a 10.
- Somme des éléments d'un tableau d'entiers.
- Table de multiplication.
