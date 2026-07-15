# Projet C11 minimal

Exemple minimal sans bibliothèque externe, comprenant :

- un module `greet` avec un en-tête public ;
- un exécutable `projet-cli` ;
- un test unitaire ;
- un Makefile ;
- deux modes principaux de validation mémoire avec Valgrind.

## Compilation

```sh
make
./build/projet-cli
```

## Tests unitaires

Exécution normale des tests :

```sh
make test
```

Exécution des tests sous Valgrind :

```sh
make memcheck
```

`memcheck` est un alias de `memcheck-tests` :

```sh
make memcheck-tests
```

Cette cible sert à détecter les erreurs mémoire et les fuites produites pendant les tests unitaires.

## Exécution normale sous Valgrind

Le programme doit être démarré sous Valgrind. Une exécution antérieure sans Valgrind ne peut pas être analysée rétroactivement.

```sh
make memcheck-run
```

Des arguments peuvent être transmis au programme avec `ARGS` :

```sh
make memcheck-run ARGS="arg1 arg2"
```

Le rapport de fuite est produit à la terminaison du programme.

## Scénario reproductible

La cible suivante est destinée à un scénario déterministe, par exemple en intégration continue :

```sh
make memcheck-scenario SCENARIO_ARGS="arg1 arg2"
```

Dans un projet réel, `SCENARIO_ARGS` peut contenir un jeu d'entrée de référence, par exemple :

```sh
make memcheck-scenario \
    SCENARIO_ARGS="--input tests/data/example.txt --output build/result.txt"
```

## Options Valgrind

Les options par défaut sont :

```text
--leak-check=full
--show-leak-kinds=all
--errors-for-leak-kinds=definite,indirect,possible
--track-origins=yes
--error-exitcode=1
```

Les catégories `definite`, `indirect` et `possible` font échouer la cible. Les blocs `still reachable` restent affichés sans provoquer d'échec.

Les options peuvent être remplacées à l'appel :

```sh
make memcheck-tests \
    VALGRIND_FLAGS="--leak-check=full --error-exitcode=42"
```

## Cibles principales

| Cible | Sémantique |
|---|---|
| `make test` | Exécute les tests sans Valgrind. |
| `make memcheck` | Alias de `make memcheck-tests`. |
| `make memcheck-tests` | Exécute les tests unitaires sous Valgrind. |
| `make memcheck-run` | Exécute le programme sous Valgrind avec les arguments de l'utilisateur. |
| `make memcheck-scenario` | Exécute un scénario Valgrind reproductible. |
| `make clean` | Supprime le répertoire `build/`. |

## Nettoyage

```sh
make clean
```
