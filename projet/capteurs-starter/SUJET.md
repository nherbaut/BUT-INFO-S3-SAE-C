# Projet capteurs

## Objectif

Vous allez construire un programme C qui analyse les températures d'un
historique de mesures. Chaque mesure contient aussi des valeurs d'humidité,
mais les calculs demandés dans ce projet portent uniquement sur les
températures. Le programme charge les mesures, calcule des statistiques,
affiche un rapport dans le terminal et produit une synthèse CSV.

Les données proviennent du flux suivant :

```text
https://tribequa.org/assets/data/sensors-history.json
```

Le réseau et le JSON sont pris en charge par le code fourni. Votre travail porte
sur les structures C, les fonctions, les tableaux dynamiques, la mémoire, les
chaînes, les fichiers et les rapports.

## Préparer l'environnement

Depuis le répertoire du projet, exécutez :

```sh
make check-tools
make
```

Vous avez besoin d'un compilateur C, de Make, de la bibliothèque de
développement `libcurl`, de `cppcheck` et de Valgrind. Sous Debian ou Ubuntu,
installez notamment `build-essential`, `libcurl4-openssl-dev`, `cppcheck` et
`valgrind`.

### Configurer VS Code avec Makefile Tools

1. Installez les extensions **C/C++** et **Makefile Tools** (éditeur :
   Microsoft) depuis l'onglet Extensions de VS Code.
2. Ouvrez directement le dossier `projet/capteurs-starter` avec **Fichier >
   Ouvrir un dossier** : son `Makefile` doit être à la racine du dossier ouvert.
3. Ouvrez la palette de commandes (`Ctrl+Maj+P`), exécutez
   `Makefile: Configure`, puis acceptez la proposition d'utiliser Makefile
   Tools comme fournisseur de configuration C/C++ si VS Code l'affiche.
4. Pour choisir une cible, exécutez `Makefile: Set the target to be built by
   make` (par exemple `test-statistics`, `test-series` ou `test`). Lancez-la
   ensuite avec `Makefile: Build the current target`.

La cible par défaut est `all` : `Makefile: Build the current target` équivaut
alors à `make`. Aucune configuration `.vscode` n'est fournie avec le starter :
la détection est automatique lorsque le dossier ouvert contient le `Makefile`.

Au départ, plusieurs tests échouent : c'est normal. Les fonctions à compléter
contiennent des marqueurs `TODO`.

Les tests fournis constituent un socle de développement. L'évaluation peut
utiliser des tests complémentaires pour vérifier tous les contrats décrits
dans ce sujet et dans les fichiers d'en-tête.

## Organisation

| Répertoire ou fichier | Rôle |
| --- | --- |
| `include/projet/` | Interfaces publiques : types et prototypes. |
| `src/statistics.c` | Calcul des statistiques de température. |
| `src/series.c` | Tableau dynamique de mesures. |
| `src/report.c` | Rapports terminal et CSV, libellé dynamique. |
| `src/main.c` | Arguments et ouverture du fichier CSV. |
| `tests/` | Tests unitaires et jeu de données local. |
| `provided/` | Code HTTP/JSON fourni : ne le modifiez pas. |

Lisez les headers avant de modifier les sources. Utilisez uniquement
`include/projet/sensor_source.h` pour charger un `SensorDataset`.

## Commandes utiles

| Commande | Effet |
| --- | --- |
| `make` | Compile `build/capteurs`. |
| `make test-statistics` | Exécute les tests des statistiques. |
| `make test-series` | Exécute les tests du tableau dynamique. |
| `make test-report` | Exécute les tests du rapport et du CSV. |
| `make test-cli` | Vérifie un lancement complet avec fichier CSV. |
| `make test` | Exécute tous les tests. |
| `make memcheck` | Exécute les tests avec Valgrind. |
| `make memcheck-series` | Vérifie isolément la mémoire de la série dynamique. |
| `make cppcheck` | Analyse votre code dans `src/`. |
| `make clean` | Supprime le répertoire `build/`. |

## Jalon 1 — Prise en main (phases 1 et 2)

1. Ouvrez le projet dans VS Code.
2. Exécutez `make check-tools`, `make`, `make test` et `make cppcheck`.
3. Lisez `include/projet/`, `src/` et `tests/`.
4. Repérez le rôle de `src/`, `include/`, `tests/`, `provided/` et du
   Makefile.
5. Créez un premier commit.

**Attendu :** vous savez compiler le projet, lancer les vérifications et
distinguer le code à compléter du code fourni.

## Jalon 2 — Fonctions, pointeurs et structures (phase 3)

Le test `tests/test_statistics.c` construit un tableau de mesures sur la pile.
N'utilisez donc ni `malloc` ni `realloc` à ce jalon.

Dans `src/statistics.c`, implémentez :

1. `temperature_statistics_compute` : nombre de mesures, minimum, maximum et
   moyenne de la température demandée par `TemperatureKind` ;
2. `temperature_average_gap` : moyenne de
   `température intérieure - température extérieure` ;
3. les cas invalides : série vide, pointeur nul ou grandeur inconnue doivent
   retourner `0`.

Validez avec :

```sh
make test-statistics
make cppcheck
```

**Attendu :** les statistiques reposent sur les structures, les pointeurs et
les fonctions de la phase 3, sans allocation dynamique.

## Jalon 3 — Mémoire dynamique, chaînes et fichiers (phase 4)

### Étape 3A — Série dynamique et Valgrind

Dans `src/series.c` :

1. allouez une première capacité avec `malloc` à la première insertion ;
2. agrandissez le tableau avec `realloc` lorsqu'il est plein ;
3. mettez à jour `count` après chaque insertion réussie ;
4. libérez le tableau avec `free` dans `measure_series_clear` et réinitialisez
   la structure.

Validez cette étape avec `make test-series` puis `make memcheck-series`.

### Étape 3B — Libellé, rapport terminal et export CSV

Dans `src/report.c`, `sensor_report_options_init` doit refuser un libellé nul,
vide, ou contenant une virgule, un guillemet ou un retour à la ligne. Copiez un
libellé valide avec les fonctions de `string.h` et `malloc`, puis libérez-le
dans `sensor_report_options_clear`.

`sensor_report_print` affiche le libellé, le nombre de mesures, la date de mise
à jour, les minimums, maximums et moyennes intérieur/extérieur, ainsi que
l'écart moyen.

Le rapport terminal doit suivre ce format :

```text
Rapport : Mesures locales
Mesures: 3
Mise a jour: 2026-09-24T08:30:00+02:00
Temperature interieure: min=27.20 max=27.50 moyenne=27.33
Temperature exterieure: min=27.60 max=27.90 moyenne=27.77
Ecart interieur-exterieur moyen: -0.43
```

Validez cette étape avec `make test-report`.

### Étape 3C — Arguments, CSV et intégration

Dans `src/main.c`, implémentez `parse_options` avec une boucle sur `argv` et
`strcmp`. Les options peuvent être fournies dans n'importe quel ordre :

```sh
./build/capteurs [--url URL | --file FICHIER] [--csv FICHIER] [--label TEXTE]
```

- `--csv` et `--label` sont facultatifs et ne peuvent être fournis qu'une fois ;
- sans `--csv`, le fichier `rapport.csv` est utilisé ; sans `--label`, le
  libellé `Rapport capteurs` est utilisé ;
- `--url` et `--file` sont exclusifs ;
- sans source explicite, l'URL par défaut est utilisée ;
- une option inconnue, incomplète ou dupliquée affiche l'usage et retourne
  le code `2`.

`write_csv_report` ouvre le fichier avec `fopen("w")`, appelle
`sensor_report_write_csv`, vérifie l'écriture et la fermeture, puis ferme le
fichier dans tous les cas.

Le CSV contient un en-tête et une ligne de synthèse. Les colonnes, séparées par
des virgules, sont dans cet ordre :

1. `label`, `updated_at`, `count` ;
2. `indoor_minimum`, `indoor_maximum`, `indoor_average` ;
3. `outdoor_minimum`, `outdoor_maximum`, `outdoor_average` ;
4. `average_gap`.

Les valeurs statistiques sont écrites avec deux décimales. La fonction retourne
`0` si les arguments sont invalides, si la série est vide, si un calcul échoue
ou si une écriture échoue.

Validez la version finale avec :

```sh
make test
make cppcheck
make memcheck
./build/capteurs --file tests/data/sensors-history.json \
  --csv rapport.csv --label "Mesures locales"
```

**Attendu :** tous les tests passent, le CSV respecte le format demandé et
Valgrind ne signale aucune erreur ni fuite.

## Travail personnel et évaluation

Travaillez dans votre dépôt ou votre branche personnelle et réalisez des
commits réguliers. Vous devez comprendre et pouvoir modifier chaque partie du
code rendu : l'évaluation individuelle peut notamment porter sur les arguments,
la mémoire, les pointeurs, les fichiers ou les statistiques.

## Périmètre fourni

Ne modifiez pas `provided/`. Il contient l'adaptation HTTP avec `libcurl` et le
parseur JSON `cJSON`. Le reste du projet communique avec cette couche uniquement
par `include/projet/sensor_source.h`.
