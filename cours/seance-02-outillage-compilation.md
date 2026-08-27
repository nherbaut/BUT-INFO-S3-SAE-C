# Phase 2 - Compilation et outillage

## Objectifs

- Cloner le dépôt.
- Compiler avec `gcc`.
- Utiliser un Makefile.
- Comprendre l'organisation minimale d'un projet C.
- Lire les arguments de ligne de commande.

## Compiler avec `gcc`

gcc (ou son alias cc sur vos machine) peut être utiliser pour compiler directement un fichier source. De nombreuses options sont utiles lors de la compilation, en voici quelques unes.

```bash {playback=typing}
## Appel de gcc (GNU Compiler Collection)
# De nombreux compilateurs C existent. GCC est le compilateur historique, mais des compilateurs plus modernes existent comme LLVM/Clang, ou plus compacts comme TinyCC.
gcc \
##
## Spécification de la norme C
# de nombreuses spécifications de C existent (K&R C ANSI C C99 C11 C17 C23 C29), même si les nouvelles modifications apportées dans le langage sont bien moins importantes que Java ou Python.
# Nous utiliserons le C11, équivalent à la norme ISO IEC 9899:2011.
-std=c11
##
## Les Warnings
# Il est très utile d'afficher les avertissements de compilation, car le plus souvent, ils correspondent à des problèmes de programmation. Nous utiliserons les flags suivants:
-Wall -Wextra -pedantic\
##
## Le débugger
# Il est possible de debugger du C dans la ligne de commande avec l'utilitaire gdb, ou directement dans un front-end de gdb fourni par votre IDE. Nous utiliserons le frontend de vscode dans ce cours.
-g
##
```



::: quiz {#quiz-s2-gcc}
title: compiler avec gcc

::: question {#q-s2-gcc-options}
title: quelles options sont utiles pour compiler ce cours ?
description: Sélectionnez les options qui demandent le C11, des warnings utiles et des informations de débogage.

- [x] `-std=c11`
- [x] `-Wall`
- [x] `-g`
- [ ] `--execute`
  hint: La compilation et l'exécution sont deux étapes distinctes.
:::
:::

## Piloter la construction et les tests du projet avec un Makefile

La compilation est une étape primordiale de tout projet, ainsi, elle est le plus souvent automatisée. De nombreux outils d'automatisation existent, le plus utilisé est Makefile. 

Il peut être écrit à la main, ou généré automatiquement à partir d'utilitaires de plus haut niveau. L'industrie utilise beaucoup CMake, qui permet de générer les Makefiles ainsi que l'intégration aux IDE les plus connus.

```bash {playback=typing}
## Voir le fichier
# make lit un fichier nommé Makefile. On commence par afficher ici une version
# minimale, contenant un exécutable et son unique fichier objet.
$ cat Makefile
##
## Options de compilation
# La variable CFLAGS regroupe les options passées au compilateur : la norme C11,
# les warnings utiles et les informations de débogage pour gdb ou VS Code.
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic -g
##
## Cible finale
# La partie à gauche des deux-points est une cible. Pour produire le programme,
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

## Executer un programme

Vous pouvez également exécuter le programme directement depuis le terminal

```bash {playback=typing}

## Compilation et exécution du programme monolithique
# Dans l'état initial, la cible run dépend de l'exécutable build/stats.
# Cet exécutable dépend uniquement de src/main.c, qui contient toutes les fonctions.
# nous allons construire l'exécutable build/stats avec make

(base) nherbaut@ares:~/Documents/teaching/IUTBDX/SAE-C/exercices/seance-02/compilation-separee$ make build/stats
##
mkdir -p build
cc -Iinclude -std=c11 -Wall -Wextra -Wpedantic -g src/main.c -o build/stats

## Exécution manuelle
# le programme peut être directement lancé en tapant son nom (n'oubliez pas ./ devant pour lancer l'exécution!)
(base) nherbaut@ares:~/Documents/teaching/IUTBDX/SAE-C/exercices/seance-02/compilation-separee$ ./build/stats 
##
moyenne = 12.00
max = 14


## Exécution avec make
# make permet également de lancer le programme. Si celui-ci n'est pas déjà compilé, make le compilera pour vous
(base) nherbaut@ares:~/Documents/teaching/IUTBDX/SAE-C/exercices/seance-02/compilation-separee$ make run
##
./build/stats
moyenne = 12.00
max = 14

## Test du programme
# La cible compare la sortie du programme avec le fichier de référence.
# Avec le programme monolithique, c'est la seule façon de tester simplement
(base) nherbaut@ares:~/Documents/teaching/IUTBDX/SAE-C/exercices/seance-02/compilation-separee$ make test
##
./build/stats | diff -u tests/expected-output.txt -
## cible de vérification mémoire
# Cette cible utilise l'outil externe valgrind pour vérifier l'exécution du programme.
# la sortie ne montre aucun problème de mémoire.
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

## Organisation standard d'un projet C

L'exercice `exercices/seance-02/compilation-separee` commence avec une
organisation normale de projet C, mais avec un programme encore monolithique :

```text
compilation-separee/
|-- exercise.json
|-- include
|   \-- projet/
|-- Makefile
|-- src
|   \-- main.c
\-- tests
    \-- expected-output.txt

```

- `src/main.c` contient initialement `main`, `moyenne` et `maximum`.
- `include/projet/` est prêt-à-recevoir les fichiers d'en-tête publics.
- `tests/` contient le résultat attendu par `make test`.
- `build/` contient les fichiers objets et l'exécutable produits par la
  compilation. Il est généré par `make` et ne doit pas être modifie a la main.
- Le `Makefile` décris les dépendances entre ces fichiers et fournit les cibles
  `make`, `make run`, `make test`, `make memcheck` et `make clean`.

L'objectif est de transformer ce programme en compilation séparée : creer
`include/projet/stats.h`, déplacer `moyenne` et `maximum` dans `src/stats.c`,
inclure le header dans `src/main.c`, puis modifier le `Makefile`. La version
finale produira d'abord `build/main.o` et `build/stats.o`, puis l'edition de
liens les assemblera dans l'exécutable `build/stats`.

::: quiz {#quiz-s2-layout}
title: Organisation d'un projet C

::: question {#q-s2-layout-directories}
title: Quels répertoires appartiennent a cette organisation ?
description: Sélectionnez les associations correctes entre un répertoire et son rôle.

- [x] `src/` contient les fichiers source C.
- [x] `include/` contient les fichiers d'en-tête.
- [x] `tests/` contient les programmes ou jeux de tests.
- [ ] `build/` est le répertoire dans lequel on écrit les fichiers source à la main.
  hint: `build/` est produit par la compilation et peut être supprime avec `make clean`.
:::
:::



## Utilisation des arguments de ligne de commande en C

La fonction `main` peut recevoir le nombre d'arguments dans `argc` et leurs valeurs dans
`argv`. A cette phase, on utilise `argc` pour vérifier la forme de la commande;
la manipulation détaillée des chaines contenues dans `argv` sera vue en phase 3.

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
Ajouter des Paramètres d'exécution à passer à stdin et vérifiez le programme les compte bien.
```

Les options `--file` et `--url` du projet capteurs sont un exemple de cette
convention.

::: quiz {#quiz-s2-argv}
title: Arguments de ligne de commande

::: question {#q-s2-argv-content}
title: Que reçoit le programme appelé avec `./capteurs --file mesures.json` ?
description: Sélectionnez les affirmations correctes sur `argc` et `argv`.

- [x] `argc` vaut `3`.
- [x] `argv[0]` contient le nom utilise pour lancer le programme.
- [x] `argv[1]` contient `--file`.
- [ ] `argv` contient les valeurs saisies sur l'entree standard.
  hint: Les arguments sont donnés dans la commande ; stdin est un flux distinct.
:::
:::

## Lire les erreurs et warnings

Les diagnostics du compilateur indiquent un fichier, une ligne et la nature du
problème. Corriger d'abord les erreurs de syntaxe, puis les warnings : certains
warnings signalent un programme qui compile, mais dont le comportement est
incorrect ou indéfini.

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
- [x] `main.o` doit être produit avant `programme` si nécessaire.
- [ ] `main.o` est execute apres `programme`.
  hint: Une dépendance est construite avant la cible qui en dépend.
:::

::: question {#q-s2-cibles}
title: Quelles cibles doivent être disponibles ?
description: Le dépôt doit permettre de compiler, exécuter et tester localement.

- [x] `make`
- [x] `make run`
- [x] `make test`
- [ ] `make push`
  hint: Le dépôt local ne doit pas publier automatiquement.
- [x] `make clean`
:::
:::

## Fichier d'en-tête

Un fichier d'en-tête, généralement nommé avec l'extension `.h`, décrit
l'**interface** d'un module : ce que les autres fichiers C peuvent utiliser
sans avoir à connaître son implémentation. Il contient notamment des
déclarations de fonctions, des types, des constantes et éventuellement des
macros.

Dans cet exercice, `include/projet/stats.h` déclarera les fonctions `moyenne`
et `maximum`. Le fichier `src/main.c` et le futur fichier `src/stats.c`
l'incluront avec `#include "projet/stats.h"`. Les corps des fonctions restent
dans le fichier `.c` : le header expose le contrat, le source fournit le code.

Voici l'interface attendue :

```c
#ifndef PROJET_STATS_H
#define PROJET_STATS_H

#include <stddef.h>

double moyenne(const int values[], size_t count);
int maximum(const int values[], size_t count);

#endif
```

```technical
Une garde d'inclusion protège un header contre les inclusions multiples. Lors
de la première inclusion, le préprocesseur conserve le contenu du fichier et
marque la garde comme définie. Lors d'une inclusion suivante, il ignore le même
contenu : les déclarations ne sont donc pas lues deux fois dans la même unité de
compilation.

Le nom de la garde doit être suffisamment précis pour éviter une collision avec
un autre header. `PROJET_STATS_H` reflète ici le rôle et le chemin du fichier
`projet/stats.h`.
```

## Exercice de la compilation séparée

Transformez le projet monolithique proposé ci-dessous en projet à compilation
séparée. Travaillez localement et vérifiez après chaque étape avec `make test`.

{{ c_exercise: exercices/seance-02/compilation-separee }}


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
5. **Ecrivez des tests unitaires**. Un fichier  `test/stats_test.c` doit être ajouté au projet. Dans celui-ci, vous écrirez un test unitaire pour vérifier le calcul de la moyenne. Pour cela, appellerez [la fonction assert](https://man7.org/linux/man-pages/man3/assert.3.html) dans une fonction main() de ce fichier.
6. **Valider le résultat.** `make`, `make run`, `make test` et `make memcheck`
   doivent toujours fonctionner. `make clean` doit supprimer `build/`.


## Organisation d'un petit projet C

## Exercices proposés

- Transformer un programme monofichier en plusieurs fichiers.
- Écrire un Makefile avec `all`, `run`, `test`, `clean`.
- Corriger un programme qui compile avec warnings.
