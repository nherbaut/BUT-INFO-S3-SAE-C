# Seance 2 - Compilation et outillage

## Objectifs

- Cloner le depot.
- Compiler avec `gcc`.
- Utiliser un Makefile.
- Comprendre l'organisation minimale d'un projet C.

## Cloner le depot

## Compiler avec `gcc`

## Options recommandees

```bash
gcc -std=c11 -Wall -Wextra -pedantic -g
```

## Executer un programme

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
