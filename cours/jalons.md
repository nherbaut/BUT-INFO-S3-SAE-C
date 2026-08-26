# Jalons autonomes

Les jalons structurent le travail personnel. Ils ne font pas partie du contenu
pedagogique des seances ni du PDF de cours.

## Jalon autonome 1 - Comprendre le projet

Sans modifier le projet, les etudiants clonent le depot, ouvrent le projet dans
VS Code et lancent `make`, `make test` et `make capteurs`. Ils lisent ensuite le
README du projet capteurs, decrivent le rapport attendu et proposent des cas de
test pour minimum, maximum, moyenne et ecart interieur-exterieur. Ils notent les
questions a traiter lors de la seance d'outillage.

## Jalon autonome 2 - Statistiques sur la pile

Les etudiants implementent `temperature_statistics_compute` et
`temperature_average_gap`. Le test `tests/test_statistics.c` construit deja un
tableau de mesures sur la pile : il n'y a donc encore ni `malloc` ni `realloc` a
utiliser.

```bash
cd projet/capteurs-starter
make test-statistics
```

## Jalon autonome 3 - Serie dynamique et version candidate

Les etudiants implementent `measure_series_append` et `measure_series_clear`,
puis le rapport terminal. Le test de serie ajoute 17 mesures afin de forcer
l'agrandissement du tableau.

```bash
cd projet/capteurs-starter
make test-series
make test
make memcheck
```

La version obtenue est celle apportee a la seance finale.
