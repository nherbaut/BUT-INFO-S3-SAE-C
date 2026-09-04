# Jalons autonomes

Les jalons structurent le travail personnel à réaliser entre les phases encadrées.

Les modalités de rendu et la répartition de la note sont décrites dans la page
[Évaluation de la SAE C](evaluation.html).

## Jalon autonome 1 - Prise en main (phases 1 et 2)

Sans modifier le projet, ouvrez-le dans VS Code et vérifiez l'environnement
avec `make check-tools`, `make`, `make test` et `make cppcheck`.

Lisez ensuite le `SUJET.md` du projet capteurs et repérez le rôle de `src/`,
`include/`, `tests/`, `provided/` et du Makefile. Distinguez le code à
compléter du code fourni.

Le [sujet du projet capteurs est également disponible au format PDF](assets/pdf/projet-capteurs.pdf).

Notez les questions et difficultés que vous avez eues ; nous les aborderons
pendant la phase 2.

### Prise en main locale

La prise en main locale est réalisée pendant ce jalon. Vérifiez les choix de
tests proposés et notez les erreurs rencontrées pendant l'ouverture du projet, la
compilation, l'exécution ou l'analyse statique.

### Ouvrir le projet fourni

```todo
Dans un terminal, ouvrez le dossier du projet fourni avec les commandes ci-dessous.
```

```bash {playback=typing}
## ouvrir le projet
# On ouvre le répertoire du projet
(base) nherbaut@ares:~/projet-sae-c$ cd projet/capteurs-starter/
##

## Utilisation du Makefile
# L'outil make utilise le fichier Makefile pour automatiser les opérations du cycle de développement : compilation, tests, lancement du programme et vérification de la mémoire.
# L'argument passé à make est appelé une cible (target).
# Ici, la cible `build/capteurs` construit le projet.
(base) nherbaut@ares:~/tmp/BUT-INFO-S3-SAE-C/projet/capteurs-starter$ make build/capteurs
##

mkdir -p build

## Exécution du préprocesseur et compilation au stade objet.
# Cette commande exécutée par le Makefile réalise deux opérations.
# 1/ Le préprocesseur modifie le code source à partir des directives telles que #ifdef et #define.
# 2/ La compilation produit du code machine non encore exécutable et des symboles en attente de liaison.
cc -Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu -std=c11 -Wall -Wextra -Wpedantic -c src/main.c -o build/main.o
##
## Détail d'une commande de compilation
# Ici, on appelle le compilateur (via son alias cc)
cc \
##
## Headers
# Ici, on indique les répertoires contenant les headers C (*.h).
-Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu \
##
## Options de compilation
# Ici, on indique le standard C à utiliser (C11) et le niveau de warnings demandé :
# all : tous les warnings courants
# extra : des warnings supplémentaires
# pedantic : respect strict du standard C
-std=c11 -Wall -Wextra -Wpedantic\
##
## Spécification du source
# Le source est ensuite passé à l'aide de l'option -c
-c src/series.c\
##
## Spécification de la cible
# Le fichier objet à créer est ensuite indiqué.
-o build/series.o
##
## *.c => *.c
# Pour chaque fichier sources l'opération est répétée
cc -Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu -std=c11 -Wall -Wextra -Wpedantic -c src/statistics.c -o build/statistics.o
cc -Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu -std=c11 -Wall -Wextra -Wpedantic -c provided/sensor_source.c -o build/sensor_source.o
cc -Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu -std=c11 -Wall -Wextra -Wpedantic -c src/report.c -o build/report.o
cc -Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu -std=c11 -Wall -Wextra -Wpedantic -c provided/cjson/cJSON.c -o build/cJSON.o
##

## Edition de liens
# Dernière étape de la construction : l'éditeur de liens réunit les fichiers objets (*.o) et les bibliothèques tierces pour produire un exécutable.
cc \
##
## On commence par les objets
build/main.o build/series.o build/statistics.o build/sensor_source.o build/report.o build/cJSON.o\
##
## Puis les bibliothèques tierces (ici, math et curl)
-lm -lcurl  \
##
## Et on finit par spécifier le nom de l'exécutable
-o build/capteurs
##
```

### Vérifier les outils

```todo
Depuis `projet/capteurs-starter`, exécutez `make check-tools`, puis `make cppcheck`.
```

`check-tools` vérifie que le compilateur, Make, `cppcheck` et Valgrind sont
disponibles. `cppcheck` analyse uniquement `src/`, c'est-à-dire
le code à modifier ; il n'analyse ni le réseau ni le parseur JSON fournis.

### Première préparation des statistiques

Avant d'écrire les statistiques du projet, proposez sur papier les signatures
de deux fonctions sur un tableau de mesures : une fonction de minimum et une
fonction de maximum. Précisez les paramètres nécessaires et le comportement
attendu lorsque le tableau est vide. Ces choix seront discutés avant le jalon 2.

### Ouvrir le projet avec VS Code

Avant d'ouvrir le projet avec VS Code, installez deux extensions utiles pour le développement C.

```todo
Dans un terminal, tapez les commandes suivantes:
```

```bash
code  --install-extension ms-vscode.makefile-tools
code  --install-extension ms-vscode.cpptools-extension-pack
```

Ouvrez ensuite le répertoire `exercices/seance-02/compilation-separee` avec VS Code (`File > Open Folder`).

Configurez ensuite VS Code pour qu'il utilise les bonnes cibles du Makefile :

```todo
reproduisez la configuration suivante
```

![configuration de l'extension makefile dans vscode](assets/vscode-configure-makefile.png)

Ensuite, ouvrez le fichier `main.c` qui se trouve dans ./src

![ouverture du source principal avec main](assets/vscode-main-c.png)

Placez un point d'arrêt ligne 7 (point rouge) en cliquant dans la goutière.

![placement d'un point d'arrêt](assets/vscode-breakpoint.png)

Puis lancez le debug du programme dans l'extension Makefile.

![lancement du programme](assets/vscode-debug.png)

Vous pouvez ensuite utiliser la petite boite de contrôle du debugger ou les raccourcis clavier pour naviguer dans l'exécution de votre code.

![contrôles du débug](assets/vscode-debug-box.png)

```todo
Lancez le programme avec le débogueur et parcourez son exécution. Survolez les
variables pour afficher leur valeur courante.
```

## Jalon autonome 2 - Fonctions, pointeurs et structures (phase 3)

Implémentez `temperature_statistics_compute` et
`temperature_average_gap`. Le test `tests/test_statistics.c` construit déjà un
tableau de mesures sur la pile : il n'y a donc encore ni `malloc` ni `realloc`
à utiliser. Implémentez les deux fonctions, y compris les cas de pointeur nul,
série vide et `TemperatureKind` invalide.

```bash
cd projet/capteurs-starter
make test-statistics
make cppcheck
```

## Jalon autonome 3 - Mémoire dynamique, chaînes et fichiers (phase 4)

Réalisez les trois étapes suivantes dans l'ordre :

1. **3A — série dynamique et Valgrind** : implémentez
   `measure_series_append` et `measure_series_clear`. Le test de série ajoute
   17 mesures afin de forcer l'agrandissement du tableau. Validez avec
   `make test-series` et `make memcheck-series`.
2. **3B — libellé, rapport terminal et export CSV** : gérez le libellé
   dynamique, puis produisez le rapport terminal au format demandé et l'export
   CSV de synthèse. Validez avec
   `make test-report`.
3. **3C — CLI et intégration** : complétez l'analyse des options et validez le
   programme complet sur le fichier local avec `--csv` et `--label`.

```bash
cd projet/capteurs-starter
make test-series
make memcheck-series
make test-report
make test
make cppcheck
make memcheck
```

La version obtenue est celle apportée à la phase finale.
