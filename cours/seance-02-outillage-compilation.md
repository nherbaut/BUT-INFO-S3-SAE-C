# Seance 2 - Compilation et outillage

## Objectifs

- Cloner le depot.
- Compiler avec `gcc`.
- Utiliser un Makefile.
- Comprendre l'organisation minimale d'un projet C.
- Lire les arguments de ligne de commande.

## Retour sur le jalon autonome 1

La prise en main locale est realisee en autonomie avant cette seance. On
verifie les choix de tests proposes, puis on traite les erreurs rencontrees
pendant le clonage, la compilation et l'execution.

## Cloner le depot

La fiche autonome demande d'executer les commandes suivantes avant la seance :

```bash {playback=typing}
## Clone du projet
# à partir de gitlab
(base) nherbaut@ares:~/tmp$ git clone https://github.com/nherbaut/BUT-INFO-S3-SAE-C.git
##

Cloning into 'BUT-INFO-S3-SAE-C'...
remote: Enumerating objects: 468, done.
remote: Counting objects: 100% (468/468), done.
remote: Compressing objects: 100% (311/311), done.
remote: Total 468 (delta 167), reused 409 (delta 109), pack-reused 0 (from 0)
Receiving objects: 100% (468/468), 2.78 MiB | 11.39 MiB/s, done.
Resolving deltas: 100% (167/167), done.

## ouvrir le projet
# On ouvre le répertoire du projet
(base) nherbaut@ares:~/tmp$ cd BUT-INFO-S3-SAE-C/projet/capteurs-starter/
##

## Utilisation du Makefile
# l'outil make utilise le fichier Makefile pour savoir comment réaliser toutes les opérations du cycle de développement. Compilation, exécution de test, lancement du programme, vérification de la mémoire...
# l'argument passé à make est appelé une **target**. 
# Ici, la target `build/capteurs` construit le projet
(base) nherbaut@ares:~/tmp/BUT-INFO-S3-SAE-C/projet/capteurs-starter$ make build/capteurs
##

mkdir -p build

## Exécution du préprocesseur et compilation au stade objet.
# Cette série de commandes exécutée par le Makefile réalise deux opérations en un seule commande
# 1/ le préprocesseur. Celui-ci modifie le code source en utilisant les directives telles que #ifdef #define...
# 2/ la compilation au stade objet. Le code C est transformé en code machine non exécutable et en symboles en attente de liaison
cc -Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu -std=c11 -Wall -Wextra -Wpedantic -c src/main.c -o build/main.o
##
## Détail d'une commande de compilation
# Ici, on appelle le compilateur (via son alias cc)
cc \
##
## Headers
# Ici, on spécifie quels sont les répertoire contenant les headers c (*.h)
-Iinclude -Iprovided/cjson -I/usr/include/x86_64-linux-gnu \
##
## Options de compilation
# Ici, on spécifie le standard C à utiliser (C11), et le niveau de Warning retourné:
# all: tous les warning
# extra: encore plus de warning
# pedantic: respect strict du standard C
-std=c11 -Wall -Wextra -Wpedantic\
##
## Spécification du source
# Le source est ensuite passé à l'aide de l'option -c
-c src/series.c\
##
## Specification de la cible
# Le fichier objet cible à créer est ensuite indiqué
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
# Dernière étape de la compilation, le linker prend les fichiers objets produits (*.o), les librairies tières pour générer un exécutable unique.
cc \
## 
## On commence par les objets
build/main.o build/series.o build/statistics.o build/sensor_source.o build/report.o build/cJSON.o\
##
## Puis les librairies tierces (ici, math et curl)
-lm -lcurl  \
##
## Et on finit par spécifier le nom de l'exécutable
-o build/capteurs
## 


```

La seance ne refait pas ces etapes pas a pas: elle aide a comprendre et corriger
les sorties obtenues.

## Compiler avec `gcc`

## Options recommandees

```bash
gcc -std=c11 -Wall -Wextra -pedantic -g
```

## Executer un programme

## Arguments de ligne de commande

`main` peut recevoir le nombre d'arguments dans `argc` et leurs valeurs dans
`argv`. A cette seance, on utilise `argc` pour verifier la forme de la commande;
la manipulation detaillee des chaines contenues dans `argv` sera vue en seance 3.

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
    int i;

    printf("nombre d'arguments: %d\n", argc);
    for (i = 0; i < argc; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    return 0;
}
```

Les options `--file` et `--url` du projet capteurs sont un exemple de cette
convention.

## Lire les erreurs et warnings

## Makefile minimal

## Cibles attendues

- `make`
- `make run`
- `make test`
- `make memcheck`
- `make clean`

::: quiz {#quiz-s2-make}
title: Makefile minimal

::: question {#q-s2-cibles}
title: Quelles cibles doivent etre disponibles ?
description: Le depot doit permettre de compiler, executer et tester localement.

- [x] `make`
- [x] `make test`
- [ ] `make push`
  hint: Le depot local ne doit pas publier automatiquement.
- [x] `make clean`
:::
:::

## Compilation separee

## Fichiers d'en-tete

{{ c_exercise: exercices/seance-02/compilation-separee }}

## Organisation d'un petit projet C

## Exercices proposes

- Transformer un programme monofichier en plusieurs fichiers.
- Ecrire un Makefile avec `all`, `run`, `test`, `clean`.
- Corriger un programme qui compile avec warnings.
