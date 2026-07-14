# Seance 4 - Memoire dynamique

## Objectifs

- Distinguer pile et tas.
- Comprendre la duree de vie des donnees.
- Utiliser `malloc`, `free` et `realloc`.
- Diagnostiquer les erreurs memoire avec Valgrind.

## Pile et variables automatiques

## Tas et duree de vie explicite

## `malloc`

## `free`

::: quiz {#quiz-s4-duree-vie}
title: Duree de vie dynamique

::: question {#q-s4-free}
title: Que faut-il faire avec une zone obtenue par `malloc` ?
description: On alloue un tableau avec `malloc`.

- [x] Appeler `free` quand la zone n'est plus utile
- [ ] La zone disparait automatiquement a la fin du bloc
  hint: Ce comportement correspond aux variables automatiques, pas au tas.
- [x] Eviter d'utiliser le pointeur apres liberation
:::
:::

## `realloc`

{{ c_exercise: exercices/seance-04/tableau-dynamique }}

## Fuites memoire

## Double liberation

## Acces apres liberation

## Utiliser Valgrind

```bash
make memcheck
```

## Exercices proposes

- Allouer un tableau d'entiers.
- Agrandir un tableau dynamique.
- Corriger une fuite memoire.
- Diagnostiquer une erreur avec Valgrind.
