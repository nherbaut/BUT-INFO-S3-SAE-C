# Phase 5 - Atelier d'aide au projet

## Objectifs

- Débloquer les difficultés rencontrées sur le projet capteurs.
- Finaliser une version candidate compilable, testée et sans fuite mémoire.
- Relire les contrats des fonctions et améliorer l'organisation du code.
- S'entraîner à expliquer et modifier son propre projet.

## Diagnostic de la version candidate

Commencez par exécuter `make test`, `make memcheck` et `make cppcheck`. À partir
des résultats, isolez un seul problème à la fois : contrat non respecté,
allocation, pointeur, chaîne, écriture de fichier ou analyse des arguments.

Avant de modifier du code, relisez le header concerné et ajoutez ou corrigez le
test qui décrit le comportement attendu.

## Vérifier l'intégration complète

Le rapport terminal s'appuie uniquement sur les structures et fonctions du
projet. Le réseau, les fichiers et le JSON restent dans `provided/` et ne sont
pas à modifier.

```bash
cd projet/capteurs-starter
make
./build/capteurs --file tests/data/sensors-history.json \
  --csv rapport.csv --label "Mesures locales"
make run
```

Vérifiez le contenu du CSV, les erreurs affichées en cas de mauvais argument et
le nettoyage de la mémoire sur le chemin normal comme sur les chemins d'erreur.

## Bonnes pratiques

- Traiter les warnings avant de continuer.
- Vérifier les retours de `malloc` et `realloc`.
- Ne pas utiliser un pointeur après `free`.
- Garder les détails internes dans les fichiers `.c` avec `static`.
- Isoler les bibliothèques fournies derrière un en-tête public.

La page [Bonnes pratiques C](bonnes-pratiques.html) sert de support de
référence pour ces points.

## Atelier de finalisation

Utilisez ce temps pour stabiliser votre version candidate, compléter les tests
utiles et vérifier la mémoire avec Valgrind. Demandez de l'aide avec un élément
précis : la commande lancée, le message obtenu, le fichier concerné et ce que
vous avez déjà essayé.

## Méthode de travail

Le dépôt doit montrer une progression régulière, avec des commits personnels
décrivant les étapes significatives du travail. Les étudiants peuvent consulter
la documentation, les supports, les manuels et les exemples fournis ; en cas de
doute sur une ressource, ils la signalent à l'enseignant.

Faites des commits courts et explicites après chaque étape fonctionnelle. Vous
devez pouvoir retrouver une modification, expliquer son intention et revenir à
un test qui la justifie.

## Checklist de version candidate

- les fichiers `src/`, `include/` et `tests/` sont cohérents ;
- `provided/` n'a pas été modifié ;
- le Makefile fonctionne depuis un répertoire propre ;
- `make test`, `make memcheck` et `make cppcheck` passent ;
- le rapport terminal et le CSV ont été vérifiés avec le jeu local ;
- l'historique Git contient des commits personnels et réguliers.
