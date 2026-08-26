# C pour la programmation systeme

Ossature de cours C pour des etudiants de BUT2 qui suivront ensuite un cours
de programmation systeme.

Le depot est volontairement leger : il fournit les grandes lignes des séances,
quelques exercices C représentatifs, une structure de projet, et des Makefiles
fonctionnels. Les explications détaillées sont a compléter par l'equipe
enseignante.

# Planning

Le parcours alterne cinq seances encadrees et trois jalons autonomes:

1. Seance 1, puis jalon autonome 1 de prise en main.
2. Seances 2 et 3, puis jalon autonome 2 de statistiques sur la pile.
3. Seance 4, puis jalon autonome 3 de serie dynamique et version candidate.
4. Seance 5 de finalisation et evaluation.

## Prerequis etudiants

- `build-essential`
- `make`
- VS Code
- Podman, optionnel pour un environnement de secours
- navigateur recent

## Utilisation rapide

```bash
make
make test
make run
make memcheck
make clean
```

Les exercices de la seance 1 sont aussi conçus pour etre copies dans [Compiler
Explorer](https://godbolt.org/). Les exemples de pointeurs de la seance 3 peuvent etre visualises avec
[Python Tutor C](https://pythontutor.com/c.html#).

## Arborescence

- `cours/` : trames des cinq seances et page de bonnes pratiques
- `exercices/` : exercices C compilables avec Makefile
- `projet/` : starter code du projet
- `assets/` : emplacement pour images et schemas

## Generation des supports

Si Pandoc est installe :

```bash
make supports
```

Les fichiers HTML et PDF generes sont places dans `build/supports/`.
Les pages HTML generes par Pandoc utilisent Bootstrap, vendorise dans
`web/vendor/bootstrap/`.

La generation produit notamment :

- `index.html` : landing page du cours ;
- `index-cours.html` : accueil de la documentation en ligne ;
- `exercices.html` : page regroupant tous les exercices ;
- `assets/pdf/but-info-s3-sae-c.pdf` : PDF complet ;
- `assets/pdf/seance-*.pdf` : PDF par seance.

Les pages HTML integrent les exercices avec un composant `c-player` :

- le code source vient des fichiers des exercices ;
- le starter code est visible et editable dans la page ;
- le bouton `Build & Run` compile dans le navigateur avec `ts-c-compiler`,
  execute le programme dans un CPU x86 JS et affiche les flux compilateur /
  programme ;
- les Makefiles locaux restent la reference pour GCC/Clang, les tests et
  Valgrind.

Le runtime navigateur est vendorise dans `web/player/tscc/`. Ses limites sont
documentees dans `web/player/tscc/ORIGIN.md` : ce n'est pas GCC/Clang, la
compilation multi-fichiers navigateur n'est pas prise en charge, et les appels
simples a `scanf` sont transformes depuis le champ `stdin` de l'exercice.

Pour verifier que le runtime navigateur est reellement installe :

```bash
make check-runtime
```

Les pages doivent etre servies en HTTP pour charger le bundle JavaScript du
runtime :

```bash
cd build/supports
python3 -m http.server 8000
```

Pour inclure un exercice dans une seance :

```markdown
{{ c_demo: exercices/seance-01/moyenne }}
{{ c_exercise: exercices/seance-01/max3 }}
```

Chaque dossier d'exercice doit contenir un `exercise.json` qui decrit les
sources, l'entree standard, la sortie attendue et les commandes locales.

### Lecture C animee

Un bloc C peut etre presente comme une lecture guidee, sans edition ni
compilation, avec l'attribut Pandoc `playback=typing` :

````markdown
```c {playback=typing}
/**
 * Titre de l'etape
 *
 * Explication affichee pendant la pause.
 */
#include <stdio.h>
/** */
```
````

Un commentaire de documentation non vide ouvre une annotation; le marqueur
`/** */` la ferme. Le code entre les deux est tape, puis surligne avant
l'affichage de l'explication. Les marqueurs ne sont pas visibles dans le lecteur
navigateur et ne creent pas de lignes vides supplementaires, mais restent des
commentaires C ordinaires dans le PDF. Chaque bloc annote recoit une couleur;
son commentaire est visible au survol et peut etre epingle par clic. Les
commentaires `/* ... */` et `// ...` ne creent pas de pause.

### Messages des composants web

Les textes ajoutes dynamiquement par les composants web sont regroupes dans
`web/player/messages.js`. Ce fichier est charge avant les lecteurs C, les quiz,
le widget ntfy, le theme et le suivi des exercices. Modifier ses valeurs suffit
pour adapter ou traduire l'interface publiee.

Les variables d'un message utilisent la forme `{nom}`, par exemple
`"Etape {current} / {total}"`. Les composants passent les valeurs necessaires
au dictionnaire; les contenus pedagogiques Markdown, les exercices et les
messages ntfy recus ne sont pas concernes.

Une valeur peut aussi etre un tableau de chaines. Le resoluteur choisit alors
une variante au hasard a chaque appel, avant de remplacer les variables :

```js
typing: ["Je tape vite non?", "Le C, c'est la vie"]
```

## Publication GitHub Pages

Le workflow `.github/workflows/pages.yml` construit les supports avec Pandoc,
execute `make test`, puis publie `build/supports` avec GitHub Pages.

Dans les settings du depot GitHub, configurer GitHub Pages avec la source
`GitHub Actions`.
