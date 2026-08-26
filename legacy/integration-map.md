# Cartographie d'integration du cours legacy

Sources legacy autorisees par Pierre Ramet :

- `td-01.pdf` - TD C part 1
- `td-02.pdf` - TD C part 2
- `td-03.pdf` - TD C part 3
- `td-04.pdf` - TD C part 4

Credits a conserver dans les supports generes : Nicolas Herbaut, Romain Giot et Pierre Ramet.

## Statuts

- `deja couvert` : le support actuel couvre deja l'idee principale.
- `a integrer` : contenu a reinjecter dans une section de cours.
- `a transformer en exercice` : contenu mieux adapte a la pratique.
- `a transformer en quiz` : contenu court utile pour verification de comprehension.
- `hors perimetre court` : a garder pour une extension ulterieure.

## Priorites

- `P1` : utile au deroule actuel des six seances.
- `P2` : utile comme enrichissement apres stabilisation du cours.
- `P3` : extension optionnelle.

## Mapping par source legacy

| Source | Contenu legacy | Cible nouveau cours | Statut | Priorite | Notes d'integration |
| --- | --- | --- | --- | --- | --- |
| `td-01.pdf` | Pourquoi programmer en C, programmation systeme, API UNIX | Seance 1 - Objectifs / contexte | integre | P1 | Integre sous forme de contexte dense en debut de seance 1. |
| `td-01.pdf` | Historique C, UNIX, K&R, ANSI/C89, C99, C11 | Seance 1 - Programme minimal | integre | P2 | Integre comme reperes historiques courts et quiz de contexte. |
| `td-01.pdf` | Exemple `hello.c`, `main`, `printf`, `EXIT_SUCCESS`, headers | Seance 1 - Programme minimal / `printf` | integre | P1 | Integre avec explication de `main`, headers, `printf` et code retour. |
| `td-01.pdf` | Prise en main VS Code, `gcc`, options `--std=c11 -Wall -Wextra -pedantic` | Seance 2 - Outillage | deja couvert | P1 | Harmoniser les options avec `-std=c11 -Wall -Wextra -pedantic -g`. |
| `td-01.pdf` | Makefile minimal, dependances, recompilation incrementale | Seance 2 - Makefile minimal | a integrer | P1 | Ajouter une explication progressive des cibles et dependances. |
| `td-01.pdf` | Compilation separee, `.c`, `.h`, prototypes | Seance 2 - Compilation separee | deja couvert | P1 | Enrichir l'exercice existant avec un schema source/header. |
| `td-01.pdf` | Protection contre les inclusions multiples | Seance 2 - Fichiers d'en-tete | a integrer | P1 | Ajouter `#ifndef/#define/#endif` et un quiz court. |
| `td-02.pdf` | Passage par valeur, transmission d'une adresse, `scanf` | Seance 3 - Passage d'arguments | deja couvert | P1 | Reprendre la formulation "une adresse est une valeur copiee". |
| `td-02.pdf` | Pointeur d'entier, prototype `int *`, absence de `&` quand on a deja une adresse | Seance 3 - Copier une adresse | a integrer | P1 | Ajouter un exemple `demander_entier`. |
| `td-02.pdf` | Dereferencement `*adr_reponse` | Seance 3 - Modifier l'objet pointe | deja couvert | P1 | Ajouter une question de quiz sur adresse vs valeur pointee. |
| `td-02.pdf` | Exercices `echanger_entiers`, `ordonner_entiers`, normaliser une duree | Seance 3 / Seance 5 | a transformer en exercice | P1 | `echanger` pour pointeurs ; `Duree` pour structures. |
| `td-02.pdf` | Logique des declarations `int *p, q` | Seance 3 - Prototypes / pointeurs | a transformer en quiz | P1 | Important pour eviter une confusion classique. |
| `td-02.pdf` | Structures, initialisateurs designes, notation point et fleche | Seance 5 - Structures | a integrer | P1 | Completer les titres existants avec un exemple `Personne` ou `Duree`. |
| `td-02.pdf` | Exercices structures avec `assert`, `const`, passage par adresse | Seance 5 - Exercices proposes | a transformer en exercice | P1 | Bon candidat pour starter multi-fichier local. |
| `td-03.pdf` | Tableaux : zone memoire consecutive, indices a partir de 0 | Seance 1 - Tableaux simples | integre | P1 | Integre dans la section tableaux simples avec quiz dedie. |
| `td-03.pdf` | Taille de tableaux automatiques/statiques, initialisation | Seance 1 / Seance 3 | partiellement integre | P2 | Taille et initialisation simples integrees ; aspects statiques/VLA repousses. |
| `td-03.pdf` | Parametre tableau equivalent pointeur | Seance 3 - Fonctions et pointeurs | a integrer | P1 | Relier a la notion de copie d'adresse. |
| `td-03.pdf` | Arithmetique des pointeurs | Seance 3 - Pointeurs | hors perimetre court | P2 | Introduire seulement apres tableaux/pointeurs de base. |
| `td-03.pdf` | Chaines C terminees par `'\0'`, litteraux vs tableaux modifiables | Extension apres structures | hors perimetre court | P2 | Utile pour projet si chaines dynamiques. |
| `td-03.pdf` | Reimplementation `strlen`, `strcat`, `strcmp` | Exercices supplementaires | a transformer en exercice | P2 | Peut devenir une page d'exercices avancee. |
| `td-04.pdf` | Allocation automatique, statique, dynamique | Seance 4 - Pile, tas, duree de vie | a integrer | P1 | Tres bon contenu conceptuel a reprendre. |
| `td-04.pdf` | `malloc`, taille en octets, `sizeof`, retour `NULL` | Seance 4 - `malloc` | deja couvert | P1 | Ajouter l'exemple `Annuaire` en fil rouge possible. |
| `td-04.pdf` | `free`, fuite memoire, mettre le pointeur a `NULL` | Seance 4 - `free` | a integrer | P1 | Ajouter une note "precaution utile, pas une liberation automatique". |
| `td-04.pdf` | `realloc`, copie de contenu, echec possible | Seance 4 - `realloc` | deja couvert | P1 | Verifier que l'exercice actuel montre le pointeur temporaire. |
| `td-04.pdf` | Exercices `Annuaire`, ajout/retrait de personnes | Projet / Seance 5 | a transformer en exercice | P2 | Peut inspirer le projet ou un TD structures + allocation. |
| `td-04.pdf` | Fichiers : `FILE*`, `fopen`, modes `r/w/a`, `fclose` | Seance 6 ou extension projet | a integrer | P2 | Utile si le projet doit charger/sauvegarder des donnees. |
| `td-04.pdf` | `fprintf`, `fscanf`, `fgets`, `fputs`, `getline` | Extension projet | hors perimetre court | P3 | A garder pour une suite programmation systeme/fichiers. |

## Prochaine passe editoriale recommandee

1. Relire la seance 1 enrichie et ajuster le niveau de detail si necessaire.
2. Integrer ensuite la seance 2 : Makefile, dependances et protections d'en-tete.
3. Transformer les items `P1` marques `a transformer en quiz` en blocs `::: quiz`.
4. Transformer les exercices legacy `echanger_entiers`, `Duree` et protections d'en-tete en starters locaux.
5. Decider ensuite si les fichiers (`FILE*`) entrent dans la seance 6 ou restent une extension projet.
