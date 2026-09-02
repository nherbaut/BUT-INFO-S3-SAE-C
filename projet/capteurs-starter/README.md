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
fonctions, les tableaux dynamiques, la mémoire, les chaînes, les fichiers et
les rapports terminal/CSV.

## Avant de commencer

Depuis le répertoire de ce projet, vérifiez votre environnement :

```sh
make check-tools
make
```

Il faut disposer d'un compilateur C, de Make, de la bibliothèque de
développement `libcurl`, de `cppcheck` et de Valgrind. Sous
Debian ou Ubuntu, les paquets utiles sont notamment `build-essential`,
`libcurl4-openssl-dev`, `cppcheck` et `valgrind`.

Au départ, plusieurs tests échouent : c'est normal. Les fonctions à compléter
contiennent des marqueurs `TODO`. Chaque jalon indique les tests qui doivent
passer avant de continuer.

## Organisation du projet

| Répertoire ou fichier | Rôle |
| --- | --- |
| `include/projet/` | Interfaces publiques : types et prototypes à lire avant de coder. |
| `src/statistics.c` | Calcul du minimum, maximum, moyenne et écart moyen. |
| `src/series.c` | Tableau dynamique de mesures. |
| `src/report.c` | Rapports terminal et CSV, ainsi que le libellé dynamique. |
| `src/main.c` | Programme principal, arguments et ouverture du fichier CSV. |
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
| `make test-report` | Compile et exécute les tests du rapport et du CSV. |
| `make test-cli` | Vérifie un lancement complet avec fichier CSV. |
| `make test` | Exécute tous les tests du projet. |
| `make memcheck` | Exécute les tests avec Valgrind. |
| `make cppcheck` | Analyse votre code dans `src/`. |
| `make clean` | Supprime les fichiers construits dans `build/`. |
| `make pdf` | Génère le sujet PDF à partir de ce README. |

Pour analyser le jeu de données local, une fois le projet terminé :

```sh
./build/capteurs --file tests/data/sensors-history.json \
  --csv rapport.csv --label "Mesures locales"
```

`make run` utilise le flux en ligne. Préférez le fichier de test local pour
obtenir un résultat reproductible pendant le développement.

## Jalon 1 - Prise en main (phases 1 et 2)

Ce jalon ne demande pas encore d'implémenter les fonctions du projet.

1. Clonez le dépôt et ouvrez `projet/capteurs-starter` dans VS Code.
2. Exécutez `make check-tools`, puis `make`.
3. Lisez les fichiers de `include/projet/`, `src/` et `tests/`.
4. Lancez `make test` pour identifier les fonctions encore incomplètes.
5. Repérez dans le Makefile les cibles `make`, `make test` et
   `make test-statistics`.
6. Créez un premier commit après votre prise en main du projet.

**Attendu du jalon 1 :** vous savez compiler le projet, localiser les fichiers
à modifier, expliquer le rôle de `src/`, `include/`, `tests/` et `provided/`,
et expliquer la différence entre le code à compléter et le code fourni.

## Jalon 2 - Fonctions, pointeurs et structures (phase 3)

Le fichier `tests/test_statistics.c` construit déjà un tableau de mesures sur
la pile. À ce jalon, vous ne devez utiliser ni `malloc` ni `realloc` : vous
mettez en œuvre les fonctions, pointeurs, structures et énumérations de la
phase 3.

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

## Jalon 3 - Mémoire dynamique, chaînes et fichiers (phase 4)

Ce jalon final réunit les notions de la phase 4. Commencez par compléter le
cycle de vie de `MeasureSeries` dans `src/series.c` :

1. `measure_series_append` doit allouer une première capacité avec `malloc` à
   la première insertion.
2. Lorsque la capacité est atteinte, elle doit agrandir le tableau avec
   `realloc`.
3. Après chaque insertion réussie, `count` doit être mis à jour.
4. `measure_series_clear` doit libérer le tableau avec `free` puis remettre la
   série dans son état initial.

### 1. Gérer le libellé et afficher le rapport

Dans `src/report.c`, `sensor_report_options_init` doit refuser un libellé nul,
vide ou contenant une virgule, un guillemet ou un retour à la ligne. Copiez un
libellé valide dans une zone allouée dynamiquement avec les fonctions de
`string.h` et `malloc`. `sensor_report_options_clear` doit ensuite libérer
cette zone, même après un chemin d'erreur, et remettre le pointeur à `NULL`.

Utilisez ensuite les fonctions de statistiques dans `sensor_report_print` pour
afficher le libellé, le nombre de mesures, la date de mise à jour, les
minimums, maximums et moyennes intérieur/extérieur, ainsi que l'écart moyen.

### 2. Analyser les arguments

Dans `src/main.c`, implémentez `parse_options` avec une boucle sur `argv` et
`strcmp`. La commande doit respecter la forme suivante, les options pouvant
être placées dans n'importe quel ordre :

```sh
./build/capteurs [--url URL | --file FICHIER] --csv FICHIER --label TEXTE
```

- `--csv` et `--label` sont obligatoires et ne peuvent apparaître qu'une fois ;
- `--url` et `--file` sont exclusifs ;
- sans `--url` ni `--file`, l'URL par défaut est employée ;
- une option inconnue, dupliquée ou sans valeur doit afficher l'usage et
  produire le code de sortie `2`.

### 3. Écrire la synthèse CSV

`write_csv_report` doit ouvrir le chemin reçu avec `fopen("w")`, appeler
`sensor_report_write_csv`, détecter une erreur d'écriture ou de fermeture, puis
fermer le fichier dans tous les cas. L'export contient exactement un en-tête et
une ligne de synthèse. Les colonnes, séparées par des virgules, sont les
suivantes dans cet ordre :

1. `label`, `updated_at`, `count` ;
2. `indoor_minimum`, `indoor_maximum`, `indoor_average` ;
3. `outdoor_minimum`, `outdoor_maximum`, `outdoor_average` ;
4. `average_gap`.

Par exemple, pour le libellé `Mesures locales`, les valeurs sont `3`, `27.20`,
`27.50`, `27.33`, `27.60`, `27.90`, `27.77` et `-0.43`, après la date de mise à
jour.

Les six valeurs statistiques et l'écart sont écrits avec deux décimales. La
fonction doit retourner `0` si ses arguments sont invalides, si la série est
vide, si un calcul échoue ou si une écriture échoue.

Validez la version candidate avec :

```sh
make test
make cppcheck
make memcheck
./build/capteurs --file tests/data/sensors-history.json \
  --csv rapport.csv --label "Mesures locales"
```

**Attendu du jalon 3 :** tous les tests passent, le CSV possède le format
attendu, et Valgrind ne signale aucune erreur ni fuite. Faites un commit de
version candidate avant la finalisation.

## Travail personnel et évaluation

Le code rendu doit être écrit sans IA générative. Travaillez dans votre dépôt ou
votre branche personnelle et réalisez des commits réguliers qui décrivent les
étapes significatives de votre progression.

L'évaluation individuelle demandera de lire, expliquer et modifier votre propre
code en temps contraint. Elle peut porter sur le parcours de `argv`, la
propriété du libellé, les pointeurs de structure, les erreurs de fichier ou
une modification des statistiques. Conservez donc un projet que vous
comprenez et que vous êtes capable de reconstruire avec `make`, `make test` et
`make memcheck`.

## Périmètre fourni

Ne modifiez pas le répertoire `provided/`. Il contient l'adaptation HTTP avec
`libcurl` et le parseur JSON `cJSON`, tous deux fournis par l'enseignant. Le
reste du projet communique avec cette couche uniquement par
`include/projet/sensor_source.h`.
