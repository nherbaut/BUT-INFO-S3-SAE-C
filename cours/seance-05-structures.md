# Seance 5 - Structures

## Objectifs

- Definir un type structure.
- Manipuler des structures par valeur et par pointeur.
- Combiner structures, pointeurs et allocation dynamique.
- Preparer les structures du projet.

## Definir une `struct`

## Initialiser une structure

## Passer une structure par valeur

## Passer une structure par pointeur

::: quiz {#quiz-s5-structures}
title: Structures et pointeurs

::: question {#q-s5-passage-struct}
title: Pourquoi passer une structure par pointeur ?
description: Une fonction doit modifier une structure existante.

- [x] Pour acceder a l'objet original via son adresse
- [ ] Parce que le C interdit le passage par valeur des structures
  hint: Une structure peut etre copiee par valeur.
- [x] Pour eviter de copier toute la structure
:::
:::

## Structures contenant des pointeurs

{{ c_exercise: exercices/seance-05/etudiants }}

## Allocation et liberation d'un objet compose

## Preparer les structures du projet

## Exercices proposes

- Structure `Etudiant`.
- Tableau dynamique d'etudiants.
- Recherche dans un tableau de structures.
- Liberation propre d'une structure allouee.
