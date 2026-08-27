# Projet capteurs - Starter

Ce projet analyse l'historique des temperatures interieures et exterieures du
flux `https://tribequa.org/assets/data/sensors-history.json`.

Le document source est du JSON, mais ni le reseau ni le parseur JSON ne font
partie du travail demande. `provided/sensor_source.c` isole `libcurl` et
[cJSON](https://github.com/DaveGamble/cJSON). Tous les autres modules ne
manipulent que des structures C.

## Commandes

```sh
make
make test
make memcheck
make run
```

L'archive a distribuer se genere avec:

```sh
make student-tarball
```

Elle est ecrite dans `dist/capteurs-starter.tar.gz`. Le depot public et cette
archive ne contiennent que le squelette etudiant. La correction complete est
conservee dans le depot prive de l'equipe enseignante.

`make run` recupere et analyse le flux live.
Pour analyser un fichier local, le programme accepte:

```sh
./build/capteurs --file tests/data/sensors-history.json
```

## Organisation

- `provided/`: code fourni, hors travail et hors correction des etudiants;
- `provided/sensor_source.c`: recuperation HTTP avec libcurl et conversion JSON avec cJSON;
- `src/series.c`: tableau dynamique de mesures, cree par `malloc` puis agrandi par `realloc`;
- `src/statistics.c`: calculs statistiques;
- `src/report.c`: rapport terminal;
- `tests/data/sensors-history.json`: extrait deterministe du flux reel.

## Jalons proposes

1. Cloner le depot, executer `make`, `make test` et `make capteurs`, puis
   decrire les resultats attendus.
2. Implementer les statistiques sur le tableau place sur la pile et executer
   `make test-statistics`.
3. Implementer la serie dynamique et le rapport, puis executer `make test` et
   `make memcheck`.
4. Apporter une version candidate pour la finalisation et l'evaluation
   individuelle.

`measure_series_append` rend volontairement visible le cycle de vie du tableau:
la premiere insertion alloue une capacite initiale avec `malloc`; lorsque cette
capacite est atteinte, l'agrandissement passe par `realloc`; enfin
`measure_series_clear` appelle `free`.

## Dependances fournies

`cJSON` 1.7.19 est embarque dans `provided/cjson/` sous licence MIT. La machine
doit posseder les en-tetes et la bibliotheque de developpement `libcurl`, ainsi
que `pkg-config`. Sous Debian/Ubuntu, cela correspond au paquet
`libcurl4-openssl-dev`.

Le reste du projet ne doit pas inclure les en-tetes de ces bibliotheques: seul
le code fourni connait leurs details. Les etudiants utilisent exclusivement
`include/projet/sensor_source.h` pour obtenir un `SensorDataset`.

Dans VS Code, `provided/` est masque par les reglages du projet. Il reste
compile automatiquement par le Makefile, sans faire partie des fichiers a
modifier.
