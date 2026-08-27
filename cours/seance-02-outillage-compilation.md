# Phase 2 - Compilation et outillage

## Objectifs

- Cloner le depot.
- Compiler avec `gcc`.
- Utiliser un Makefile.
- Comprendre l'organisation minimale d'un projet C.
- Lire les arguments de ligne de commande.

## Compiler avec `gcc`

### Options recommandees

```bash {playback=typing}
## Appel de gcc (GNU Compiler Collection)
# De nombreux compilateur C existent. GCC est le compilateur historique, mais des compilateurs plus modernes existent comme LLVM/Clang, ou plus compacts comme TinyCC.
gcc \
##
## Spécification de la norme C
# de nombreuses spécifications de C existent (K&R C ANSI C C99 C11 C17 C23 C29), même si les nouvelles modifications apportées dans le langages sont bien moins important que Java ou Python.
# Nous utiliserons le C11, équivalent à la norme ISO IEC 9899:2011.
-std=c11
##
## Les Warning
# Il est très utile d'afficher les avertissement de compilation, car le plus souvent, ils correspondent à des problèmes de programmation. Nous utiliserons les flags suivants:
-Wall -Wextra -pedantic\
##
## Le debugger
# Il est possible de debugger du C dans la ligne de commande avec l'utilitaire gdb, ou directement dans un front-end de gdb fourni par votre IDE. Nous utiliserons le frontend de vscode dans ce cours.
-g
##
```

La compilation est une étape primordiale de tout projet, ainsi, elle est le plus souvent automatisée. De nombreux outils d'automatisation existent, le plus utilisé est Makefile. 
Il peut être écrit à la main, ou généré automatiquement à partir d'utilitaires plus avancé. Le standard de-facto dans l'industrie est CMake, qui permet de générer les Makefiles pour un système donnée.

::: quiz {#quiz-s2-gcc}
title: Compiler avec gcc

::: question {#q-s2-gcc-options}
title: Quelles options sont utiles pour compiler ce cours ?
description: Selectionnez les options qui demandent le C11, des warnings utiles et des informations de debogage.

- [x] `-std=c11`
- [x] `-Wall`
- [x] `-g`
- [ ] `--execute`
  hint: La compilation et l'execution sont deux etapes distinctes.
:::
:::

```bash {playback=typing}
## Voir le fichier
# make lit un fichier nommé Makefile. On commence par afficher ici une version
# minimale, contenant un exécutable et son unique fichier objet.
$ cat Makefile
##
## Options de compilation
# La variable CFLAGS regroupe les options passees au compilateur : la norme C11,
# les warnings utiles et les informations de debogage pour gdb ou VS Code.
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic -g
##
## Cible finale
# La partie à gauche des deux-points est une cible. Pour produire programme,
# make doit d'abord produire main.o, placé après les deux-points.
programme: main.o
	$(CC) $(CFLAGS) main.o -o programme
##
## Cible intermédiaire
# main.o dépend de main.c. La ligne indentée par une tabulation est la recette
# exécutée par make lorsque la cible doit être reconstruite.
main.o: main.c
	$(CC) $(CFLAGS) -c main.c -o main.o
##
```

## Organisation standard d'un projet C

L'exercice `exercices/seance-02/compilation-separee` commence avec une
organisation normale de projet C, mais avec un programme encore monolithique :

```text
compilation-separee/
|-- exercise.json
|-- include
|   \-- projet/
|-- Makefile
|-- src
|   \-- main.c
\-- tests
    \-- expected-output.txt

```

- `src/main.c` contient initialement `main`, `moyenne` et `maximum`.
- `include/projet/` est pret a recevoir les fichiers d'en-tete publics.
- `tests/` contient le resultat attendu par `make test`.
- `build/` contient les fichiers objets et l'executable produits par la
  compilation. Il est genere par `make` et ne doit pas etre modifie a la main.
- Le `Makefile` decrit les dependances entre ces fichiers et fournit les cibles
  `make`, `make run`, `make test`, `make memcheck` et `make clean`.

L'objectif est de transformer ce programme en compilation separee : creer
`include/projet/stats.h`, deplacer `moyenne` et `maximum` dans `src/stats.c`,
inclure le header dans `src/main.c`, puis modifier le `Makefile`. La version
finale produira d'abord `build/main.o` et `build/stats.o`, puis l'edition de
liens les assemblera dans l'executable `build/stats`.

::: quiz {#quiz-s2-layout}
title: Organisation d'un projet C

::: question {#q-s2-layout-directories}
title: Quels repertoires appartiennent a cette organisation ?
description: Selectionnez les associations correctes entre un repertoire et son role.

- [x] `src/` contient les fichiers source C.
- [x] `include/` contient les fichiers d'en-tete.
- [x] `tests/` contient les programmes ou jeux de tests.
- [ ] `build/` est le repertoire dans lequel on ecrit les fichiers source a la main.
  hint: `build/` est produit par la compilation et peut etre supprime avec `make clean`.
:::
:::

## Executer un programme

Vous pouvez également exécuter le programme directement depuis le terminal

```bash {playback=typing}

## Compilation et exécution du programme monolithique
# Dans l'état initial, la target run dépend de l'exécutable build/stats.
# Cet exécutable dépend uniquement de src/main.c, qui contient toutes les fonctions.
(base) nherbaut@ares:~/Documents/teaching/IUTBDX/SAE-C/exercices/seance-02/compilation-separee$ make run
##
mkdir -p build
cc -Iinclude -std=c11 -Wall -Wextra -Wpedantic -g src/main.c -o build/stats
./build/stats
moyenne = 12.00
max = 14
## Target de test
# La target compare la sortie du programme avec le fichier de reference.
(base) nherbaut@ares:~/Documents/teaching/IUTBDX/SAE-C/exercices/seance-02/compilation-separee$ make test
##
./build/stats | diff -u tests/expected-output.txt -
## Target de vérification mémoire
# Cette target utilise l'outil externe valgrind pour verifier l'execution du programme.
(base) nherbaut@ares:~/Documents/teaching/IUTBDX/SAE-C/exercices/seance-02/compilation-separee$ make memcheck
##
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --error-exitcode=1 ./build/stats
==327827== Memcheck, a memory error detector
==327827== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==327827== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==327827== Command: ./build/stats
==327827== 
==327827== 
==327827== HEAP SUMMARY:
==327827==     in use at exit: 0 bytes in 0 blocks
==327827==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==327827== 
==327827== All heap blocks were freed -- no leaks are possible
==327827== 
==327827== For lists of detected and suppressed errors, rerun with: -s
==327827== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)


```

## Utilisation des arguments de ligne de commande en C

La fonction `main` peut recevoir le nombre d'arguments dans `argc` et leurs valeurs dans
`argv`. A cette phase, on utilise `argc` pour verifier la forme de la commande;
la manipulation detaillee des chaines contenues dans `argv` sera vue en phase 3.

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
    int i;

    printf("nombre d'arguments: %d\n", argc);
    for (i = 0; i < argc; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    return 0;
}
```

```todo
Ajouter des Parametres d'execution à passer à stdin et vérifiez le programme les compte bien.
```

Les options `--file` et `--url` du projet capteurs sont un exemple de cette
convention.

::: quiz {#quiz-s2-argv}
title: Arguments de ligne de commande

::: question {#q-s2-argv-content}
title: Que recoit le programme appele avec `./capteurs --file mesures.json` ?
description: Selectionnez les affirmations correctes sur `argc` et `argv`.

- [x] `argc` vaut `3`.
- [x] `argv[0]` contient le nom utilise pour lancer le programme.
- [x] `argv[1]` contient `--file`.
- [ ] `argv` contient les valeurs saisies sur l'entree standard.
  hint: Les arguments sont donnes dans la commande ; stdin est un flux distinct.
:::
:::

## Lire les erreurs et warnings

Les diagnostics du compilateur indiquent un fichier, une ligne et la nature du
probleme. Corriger d'abord les erreurs de syntaxe, puis les warnings : certains
warnings signalent un programme qui compile mais dont le comportement est
incorrect ou indefini.

Dans cet exercice local, le `Makefile` transforme les warnings demandes en
erreurs de compilation. Corrigez les neuf diagnostics dans `src/main.c`, puis
verifiez le resultat avec `make test`.

{{ c_exercise: exercices/seance-02/corriger-diagnostics }}

## Makefile minimal

::: quiz {#quiz-s2-makefile}
title: Makefile minimal

::: question {#q-s2-make-dependency}
title: Que signifie `programme: main.o` ?
description: Cette ligne est une regle de Makefile.

- [x] `programme` est une cible.
- [x] `main.o` doit etre produit avant `programme` si necessaire.
- [ ] `main.o` est execute apres `programme`.
  hint: Une dependance est construite avant la cible qui en depend.
:::

::: question {#q-s2-cibles}
title: Quelles cibles doivent etre disponibles ?
description: Le depot doit permettre de compiler, executer et tester localement.

- [x] `make`
- [x] `make run`
- [x] `make test`
- [ ] `make push`
  hint: Le depot local ne doit pas publier automatiquement.
- [x] `make clean`
:::
:::

## Protéger un fichier d'en-tête

Un même fichier d'en-tête peut être inclus depuis plusieurs fichiers C, parfois
indirectement par l'intermédiaire d'un autre header. Sans protection, le
compilateur lirait alors plusieurs fois les mêmes déclarations et pourrait
signaler des redéfinitions.

Une garde d'inclusion rend le contenu du fichier visible une seule fois par
unité de compilation :

```c
#ifndef PROJET_STATS_H
#define PROJET_STATS_H

#include <stddef.h>

double moyenne(const int values[], size_t count);
int maximum(const int values[], size_t count);

#endif
```

Lors de la première inclusion, `PROJET_STATS_H` n'est pas encore défini : le
préprocesseur conserve donc le contenu entre `#ifndef` et `#endif`, puis définit
la macro avec `#define`. Lors d'une inclusion suivante, la macro existe déjà et
le même contenu est ignoré. Le nom de la macro doit être suffisamment précis
pour éviter les collisions avec d'autres headers ; ici, il reflète le chemin et
le rôle du fichier `projet/stats.h`.

## Compilation séparée

Transformez le projet monolithique proposé ci-dessous en projet à compilation
séparée. Travaillez localement et vérifiez après chaque étape avec `make test`.

1. **Extraire l'interface dans un header.** Relevez les signatures de
   `moyenne` et `maximum`, puis créez `include/projet/stats.h`. Ce fichier doit
   inclure `<stddef.h>`, contenir les deux déclarations de fonctions et être
   protégé contre les inclusions multiples avec `#ifndef`, `#define` et
   `#endif`.
2. **Extraire l'implémentation dans un fichier C.** Créez `src/stats.c`.
   Incluez `projet/stats.h`, puis déplacez dans ce fichier les corps complets de
   `moyenne` et `maximum`. Le fichier ne doit pas contenir `main`.
3. **Réduire le fichier principal.** Dans `src/main.c`, remplacez les corps des
   deux fonctions par `#include "projet/stats.h"`. À la fin de cette étape,
   `src/main.c` ne contient plus que `main` et l'appel aux fonctions déclarées
   dans le header.
4. **Adapter la compilation.** Le `Makefile` doit d'abord produire
   `build/main.o` à partir de `src/main.c` et `build/stats.o` à partir de
   `src/stats.c`, avec `-c`. La cible `build/stats` doit ensuite lier ces deux
   fichiers objets. Ajoutez aussi `include/projet/stats.h` aux dépendances des
   deux fichiers objets.
5. **Valider le résultat.** `make`, `make run`, `make test` et `make memcheck`
   doivent toujours fonctionner. `make clean` doit supprimer `build/`.

{{ c_exercise: exercices/seance-02/compilation-separee }}

## Organisation d'un petit projet C

## Exercices proposes

- Transformer un programme monofichier en plusieurs fichiers.
- Ecrire un Makefile avec `all`, `run`, `test`, `clean`.
- Corriger un programme qui compile avec warnings.
