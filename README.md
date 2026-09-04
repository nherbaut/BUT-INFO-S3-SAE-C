# BUT INFO S3 SAE-C

Depot de travail du cours de C, en preparation de la programmation systeme.
Il contient les exercices, le projet capteurs et les Makefiles utilises pendant
les phases du cours.

## Prerequis

- `build-essential`
- `make`
- VS Code
- un navigateur recent

## Demarrer

```bash
git clone https://github.com/nherbaut/BUT-INFO-S3-SAE-C.git
cd BUT-INFO-S3-SAE-C
```

Chaque exercice et projet possede son propre Makefile. Depuis son dossier :

```bash
make
make run
make test
make memcheck
make clean
```

Par exemple :

```bash
cd exercices/seance-01/bonjour
make run
```

## Organisation

- `cours/` : supports des phases et bonnes pratiques ;
- `exercices/` : exercices C a compiler et modifier ;
- `projet/capteurs-starter/` : projet de travail ;
- `projet/starter/` : squelette du projet initial.

## Parcours

Le parcours alterne cinq phases encadrees et trois jalons autonomes :

1. Phase 1, puis jalon autonome 1 de prise en main.
2. Phases 2 et 3, puis jalon autonome 2 de statistiques sur la pile.
3. Phase 4, puis jalon autonome 3 de serie dynamique et version candidate.
4. Phase 5 d'aide à la finalisation du projet.
