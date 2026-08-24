# C pour la programmation systeme

Ossature de cours C pour des etudiants de BUT2 qui suivront ensuite un cours
de programmation systeme.

Le depot est volontairement leger : il fournit les grandes lignes des séances,
quelques exercices C représentatifs, une structure de projet, et des Makefiles
fonctionnels. Les explications détaillées sont a compléter par l'equipe
enseignante.

# Planning

 - Semaine 38 (14/09/2026) : 2 séances de 2h encadrées (4h) et 1 séance 2 de 2h non encadrée
 - Semaine 39 (21/09/2026) : 2 séances de 2h encadrées (4h) et 1 séance 2 de 2h non encadrée
 - Semaine 40 (28/09/2026) : 1 séance de 2h encadrée (2h) et 1 séance 2 de 2h non encadrée  
 - Semaine 50 (07/12/2026) : 2 séances de 2h non encadrées (4h)

Soit 5 séances encadrées et 5 séances non encadrées.

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

- `cours/` : trames des six seances
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

## Publication GitHub Pages

Le workflow `.github/workflows/pages.yml` construit les supports avec Pandoc,
execute `make test`, puis publie `build/supports` avec GitHub Pages.

Dans les settings du depot GitHub, configurer GitHub Pages avec la source
`GitHub Actions`.
