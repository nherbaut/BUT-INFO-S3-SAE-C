# Seance 3 - Fonctions et pointeurs

## Objectifs

- Comprendre les fonctions C.
- Installer un modele unique : les arguments sont passes par copie.
- Manipuler des pointeurs sans multiplier les modeles mentaux.

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

{{ c_demo: exercices/seance-03/swap }}

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
