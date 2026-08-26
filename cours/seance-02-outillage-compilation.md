# Seance 2 - Compilation et outillage

## Objectifs

- Cloner le depot.
- Compiler avec `gcc`.
- Utiliser un Makefile.
- Comprendre l'organisation minimale d'un projet C.
- Lire les arguments de ligne de commande.

## Retour sur le jalon autonome 1

La prise en main locale est realisee en autonomie avant cette seance. On
verifie les choix de tests proposes, puis on traite les erreurs rencontrees
pendant le clonage, la compilation et l'execution.

## Cloner le depot

La fiche autonome demande d'executer les commandes suivantes avant la seance :

```bash
git clone https://github.com/nherbaut/BUT-INFO-S3-SAE-C.git
cd BUT-INFO-S3-SAE-C
make
make test
make capteurs
```

La seance ne refait pas ces etapes pas a pas: elle aide a comprendre et corriger
les sorties obtenues.

## Compiler avec `gcc`

## Options recommandees

```bash
gcc -std=c11 -Wall -Wextra -pedantic -g
```

## Executer un programme

## Arguments de ligne de commande

`main` peut recevoir le nombre d'arguments dans `argc` et leurs valeurs dans
`argv`. A cette seance, on utilise `argc` pour verifier la forme de la commande;
la manipulation detaillee des chaines contenues dans `argv` sera vue en seance 3.

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

Les options `--file` et `--url` du projet capteurs sont un exemple de cette
convention.

## Lire les erreurs et warnings

## Makefile minimal

## Cibles attendues

- `make`
- `make run`
- `make test`
- `make memcheck`
- `make clean`

::: quiz {#quiz-s2-make}
title: Makefile minimal

::: question {#q-s2-cibles}
title: Quelles cibles doivent etre disponibles ?
description: Le depot doit permettre de compiler, executer et tester localement.

- [x] `make`
- [x] `make test`
- [ ] `make push`
  hint: Le depot local ne doit pas publier automatiquement.
- [x] `make clean`
:::
:::

## Compilation separee

## Fichiers d'en-tete

{{ c_exercise: exercices/seance-02/compilation-separee }}

## Organisation d'un petit projet C

## Exercices proposes

- Transformer un programme monofichier en plusieurs fichiers.
- Ecrire un Makefile avec `all`, `run`, `test`, `clean`.
- Corriger un programme qui compile avec warnings.
