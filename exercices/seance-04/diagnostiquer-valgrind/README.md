# Diagnostiquer des erreurs mémoire

Compilez avec `make`. Les scénarios sont `fuite`, `pointeur-perdu`,
`double-free` et `apres-free`.

```bash
make run SCENARIO=fuite
make memcheck-fuite
```

`make memcheck` exécute les quatre scénarios. Dans l'état initial, il doit
échouer : chaque scénario contient volontairement une erreur mémoire.

Corrigez `src/main.c` sans modifier le Makefile ni supprimer d'appel de
fonction. L'objectif est que `make memcheck` termine sans erreur, fuite ni
accès invalide. Après chaque correction, relancez le scénario concerné : la
première erreur signalée par Valgrind est généralement la plus utile.
