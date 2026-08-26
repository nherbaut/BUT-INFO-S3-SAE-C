# Seance 5 - Projet, bonnes pratiques et evaluation

## Objectifs

- Finaliser le projet capteurs a partir de la version candidate.
- Verifier compilation, tests et memoire.
- Lire le rapport produit a partir du flux live et de la fixture locale.
- Realiser une evaluation individuelle courte sur machine.

## Retour sur le jalon autonome 3

La seance commence par la verification de `make test` et `make memcheck`. Les
erreurs de capacite, de pointeur, de liberation et de rapport sont corrigees a
partir du code apporte par les etudiants.

## Integrer le rapport

Le rapport terminal s'appuie uniquement sur les structures et fonctions du
projet. Le reseau, les fichiers et le JSON restent dans `provided/` et ne sont
pas a modifier.

```bash
cd projet/capteurs-starter
make
./build/capteurs --file tests/data/sensors-history.json
make run
```

## Bonnes pratiques

- Traiter les warnings avant de continuer.
- Verifier les retours de `malloc` et `realloc`.
- Ne pas utiliser un pointeur apres `free`.
- Garder les details internes dans les fichiers `.c` avec `static`.
- Isoler les bibliotheques fournies derriere un en-tete public.

La page [Bonnes pratiques C](bonnes-pratiques.html) sert de support de
reference pour ces points.

## Finalisation accompagnee

Pendant environ 45 minutes, les etudiants stabilisent leur version candidate,
completent les tests utiles et verifient la memoire avec Valgrind.

## Evaluation individuelle

Les 30 dernieres minutes sont consacrees a une modification individuelle du
projet: lecture d'un test, correction d'un calcul, ajout d'un cas limite ou
explication d'un choix de memoire. La version livree doit compiler avec `make`
et passer `make test` et `make memcheck`.

## Depot attendu

- fichiers `src/`, `include/` et `tests/` modifies;
- aucune modification dans `provided/`;
- Makefile fonctionnel;
- tests verts et absence de fuite signalee par Valgrind.
