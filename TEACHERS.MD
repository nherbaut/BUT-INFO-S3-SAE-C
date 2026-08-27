# Pense-bete des elements pedagogiques

Ce guide documente les extensions Markdown reconnues par
`tools/build_supports.py`. Les syntaxes ci-dessous s'utilisent dans les fichiers
de `cours/`.

## Exercices et demonstrations

```markdown
{{ c_exercise: exercices/seance-01/max3 }}
{{ c_demo: exercices/seance-01/moyenne }}
```

- `c_exercise` affiche un exercice editable.
- `c_demo` affiche une demonstration dont le code est en lecture seule.
- Le chemin designe un dossier contenant `exercise.json`.
- Un projet monofichier peut etre execute dans le navigateur. Un projet a
  plusieurs fichiers reste executable localement avec son Makefile.

## Code C et Bash

````markdown
```c
#include <stdio.h>

int main(void)
{
    puts("Bonjour");
    return 0;
}
```

```bash
make test
```
````

- Un bloc C complet contenant `main` devient un `c-player` editable et
  executable dans le navigateur.
- Les autres blocs C et les blocs Bash sont rendus comme du code statique.
- Les seules langues ayant des options personnalisees sont `c` et `bash`.

## Lecture guidee

Ajoutez l'option `playback=typing` a une fence C ou Bash.

````markdown
```c {playback=typing}
/** Titre de l'etape
 *
 * Explication affichee dans le lecteur.
 */
int value = 42;
/** */
```

```bash {playback=typing}
## Titre de l'etape
# Explication affichee dans le lecteur.
$ make test
##
```
````

- En C, `/** ... */` ouvre une annotation et `/** */` la ferme.
- En Bash, `## Titre` ouvre une annotation, les lignes `#` suivantes forment
  son texte, et `##` la ferme.
- En Bash, une ligne commencant par un prompt (`$`, par exemple) est frappee
  progressivement. Une ligne sans prompt est rendue comme une sortie de
  commande, plus rapidement et avec le son d'imprimante matricielle.
- `playback=typing` est la seule option de lecture guidee actuellement prise
  en charge.

## Encadres

````markdown
```todo
Cloner le depot et lancer `make test`.
```

```trap
Un pointeur obtenu par `malloc` peut etre `NULL`.
```

```warning
Ne pas appeler `free` deux fois sur la meme zone.
```

```remember
Les arguments C sont toujours passes par copie.
```

```tip
Compiler avec `-Wall -Wextra -Wpedantic -g`.
```

```technical
`void *` represente une adresse sans type statique associe.
```
````

- `todo` : action a realiser. Dans le navigateur, un clic sur le texte lance
  des confettis et enregistre l'action dans `localStorage`.
- `trap` : piege courant.
- `warning` : risque ou action dangereuse.
- `remember` : regle fondamentale.
- `tip` : conseil pratique.
- `technical` : approfondissement facultatif.
- Ces fences n'acceptent aucune option. Elles sont rendues avec une icone dans
  le PDF.
- Leur contenu accepte le Markdown usuel, notamment les listes, le code en
  ligne, les liens et les paragraphes.

## Quiz

````markdown
::: quiz {#quiz-pointeurs}
title: Pointeurs
description: Verifier les notions essentielles.

::: question {#question-adresse}
title: Que recoit `f(&x)` ?
description: Une fonction C recoit toujours une copie de ses arguments.

- [ ] La variable `x` elle-meme
  hint: Une variable externe n'est pas copiee automatiquement.
- [x] Une copie de son adresse
:::
:::
````

- L'identifiant `{#...}` est optionnel pour `quiz` et `question`, mais
  recommande : il stabilise le suivi dans `localStorage` lors des editions.
- `title` et `description` sont optionnels pour le quiz et chaque question.
- Les reponses utilisent `- [x]` pour une bonne reponse et `- [ ]` pour une
  mauvaise reponse. Plusieurs bonnes reponses sont possibles.
- `hint:` est optionnel et doit etre indente sous la reponse concernee.
