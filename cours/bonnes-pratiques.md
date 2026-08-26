# Bonnes pratiques C

## Objectifs

- Reconnaitre quelques protections utiles dans un programme C.
- Distinguer le code pedagogique du code de bibliotheque fourni.

## Verifier les tailles et les capacites

Une capacite et un nombre d'elements utilisent `size_t`. Avant de doubler une
capacite, le programme doit verifier qu'il ne depasse pas `SIZE_MAX`; sinon une
multiplication peut produire une taille plus petite que celle demandee.

## Verifier les allocations

`malloc` et `realloc` peuvent renvoyer `NULL`. Le programme doit alors conserver
un etat coherent et signaler l'echec sans dereferencer le pointeur nul.

## Limiter la portee avec `static`

Une fonction ou une variable `static` dans un fichier `.c` est un detail interne
du module. Seules les fonctions declarees dans le fichier `.h` constituent son
interface publique.

## Nettoyer les ressources globales

Certaines bibliotheques initialisent un etat global. Lorsqu'elles l'exigent, le
programme enregistre leur nettoyage avec `atexit` et conserve cette logique dans
le module qui utilise la bibliotheque.

## Compiler sans warnings

Les warnings sont traites comme des defauts a comprendre avant d'aller plus
loin. Les options `-Wall`, `-Wextra` et `-Wpedantic` font partie de la commande
de compilation du projet.

## Isoler le code fourni

Le repertoire `provided/` du projet capteurs contient le reseau, les fichiers,
le JSON et les dependances. Les modules etudiants communiquent avec lui par un
en-tete public, sans recopier ces details dans le code metier.
