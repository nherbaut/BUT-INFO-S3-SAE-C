# Projet capteurs

## Objectif

Vous allez construire un programme C qui analyse un historique de mesures de
température et d'humidité. Le programme charge un jeu de mesures, calcule des
statistiques, puis affiche un rapport dans le terminal.

Les données réelles proviennent du flux suivant :

```text
https://tribequa.org/assets/data/sensors-history.json
```

Le réseau et le JSON ne sont **pas** dans le périmètre du projet. Ils sont pris
en charge par le code fourni. Votre travail porte sur les structures C, les
fonctions, les tableaux dynamiques, la mémoire et le rapport terminal.

## Avant de commencer

Depuis le répertoire de ce projet, vérifiez votre environnement :

```sh
make check-tools
make
```

Il faut disposer d'un compilateur C, de Make, de `pkg-config`, de la
bibliothèque de développement `libcurl`, de `cppcheck` et de Valgrind. Sous
Debian ou Ubuntu, les paquets utiles sont notamment `build-essential`,
`pkg-config`, `libcurl4-openssl-dev`, `cppcheck` et `valgrind`.

Au départ, plusieurs tests échouent : c'est normal. Les fonctions à compléter
contiennent des marqueurs `TODO`. Chaque jalon indique les tests qui doivent
passer avant de continuer.

## Organisation du projet

| Répertoire ou fichier | Rôle |
| --- | --- |
| `include/projet/` | Interfaces publiques : types et prototypes à lire avant de coder. |
| `src/statistics.c` | Calcul du minimum, maximum, moyenne et écart moyen. |
| `src/series.c` | Tableau dynamique de mesures. |
| `src/report.c` | Construction du rapport affiché dans le terminal. |
| `src/main.c` | Programme principal et traitement de `--url` / `--file`. |
| `tests/` | Tests unitaires et jeu de données local déterministe. |
| `provided/` | Code enseignant pour HTTP et JSON : ne pas modifier. |

Les headers décrivent le contrat de chaque fonction. Lisez-les avant de modifier
un fichier source. En particulier, `sensor_source.h` est la seule interface à
utiliser pour charger les données.

## Commandes utiles

| Commande | Effet |
| --- | --- |
| `make` | Compile le programme `build/capteurs`. |
| `make test-statistics` | Compile et exécute les tests des statistiques. |
| `make test-series` | Compile et exécute les tests du tableau dynamique. |
| `make test` | Exécute tous les tests du projet. |
| `make memcheck` | Exécute les tests avec Valgrind. |
| `make cppcheck` | Analyse le code des étudiants dans `src/`. |
| `make clean` | Supprime les fichiers construits dans `build/`. |
| `make pdf` | Génère le sujet PDF à partir de ce README. |

Pour analyser le jeu de données local, une fois le projet terminé :

```sh
./build/capteurs --file tests/data/sensors-history.json
```

`make run` utilise le flux en ligne. Préférez le fichier de test local pour
obtenir un résultat reproductible pendant le développement.

## Jalon 1 - Prise en main et préparation

Ce jalon ne demande pas encore d'implémenter les fonctions du projet.

1. Clonez le dépôt et ouvrez `projet/capteurs-starter` dans VS Code.
2. Exécutez `make check-tools`, puis `make`.
3. Lisez les fichiers de `include/projet/`, `src/` et `tests/`.
4. Lancez `make test` pour identifier les fonctions encore incomplètes.
5. Proposez les signatures et les cas limites de fonctions de minimum et de
   maximum sur un tableau de mesures.
6. Créez un premier commit après votre prise en main du projet.

**Attendu du jalon 1 :** vous savez compiler le projet, localiser les fichiers
à modifier, expliquer le rôle de `src/`, `include/`, `tests/` et `provided/`,
et décrire les statistiques à calculer.

## Jalon 2 - Statistiques sur un tableau existant

Le fichier `tests/test_statistics.c` construit déjà un tableau de mesures sur
la pile. À ce jalon, vous ne devez utiliser ni `malloc` ni `realloc`.

Dans `src/statistics.c`, implémentez :

1. `temperature_statistics_compute` : calculer le nombre de mesures, le
   minimum, le maximum et la moyenne de la température intérieure ou extérieure
   demandée par `TemperatureKind`.
2. `temperature_average_gap` : calculer la moyenne de
   `température intérieure - température extérieure`.
3. Les cas invalides : série vide, pointeur nul ou grandeur non reconnue doivent
   retourner `0`, conformément aux contrats des headers.

Validez ce jalon avec :

```sh
make test-statistics
make cppcheck
```

**Attendu du jalon 2 :** `make test-statistics` passe et les calculs sont
réalisés à partir des données d'un tableau existant, sans allocation dynamique.
Faites un commit décrivant les statistiques terminées.

## Jalon 3 - Série dynamique et rapport terminal

Dans `src/series.c`, complétez le cycle de vie de `MeasureSeries` :

1. `measure_series_append` doit allouer une première capacité avec `malloc` à
   la première insertion.
2. Lorsque la capacité est atteinte, elle doit agrandir le tableau avec
   `realloc`.
3. Après chaque insertion réussie, `count` doit être mis à jour.
4. `measure_series_clear` doit libérer le tableau avec `free` puis remettre la
   série dans son état initial.

Dans `src/report.c`, utilisez les fonctions de statistiques pour afficher :

- le nombre de mesures et la date de mise à jour ;
- minimum, maximum et moyenne des températures intérieure et extérieure ;
- l'écart intérieur-extérieur moyen.

Validez la version candidate avec :

```sh
make test-series
make test
make cppcheck
make memcheck
./build/capteurs --file tests/data/sensors-history.json
```

**Attendu du jalon 3 :** tous les tests passent, Valgrind ne signale aucune
erreur ni fuite, et le programme produit un rapport à partir du fichier local.
Faites un commit de version candidate avant la phase de finalisation.

## Travail personnel et évaluation

Le code rendu doit être écrit sans IA générative. Travaillez dans votre dépôt ou
votre branche personnelle et réalisez des commits réguliers qui décrivent les
étapes significatives de votre progression.

L'évaluation individuelle demandera de lire, expliquer et modifier votre propre
code en temps contraint. Conservez donc un projet que vous comprenez et que
vous êtes capable de reconstruire avec `make`, `make test` et `make memcheck`.

## Périmètre fourni

Ne modifiez pas le répertoire `provided/`. Il contient l'adaptation HTTP avec
`libcurl` et le parseur JSON `cJSON`, tous deux fournis par l'enseignant. Le
reste du projet communique avec cette couche uniquement par
`include/projet/sensor_source.h`.
