# Projet C - Starter

Ce repertoire contient deux squelettes de projet:

- `starter/`: carnet de contacts, fil rouge general du cours;
- `capteurs-starter/`: analyse d'un historique de temperatures provenant d'un
  flux JSON, avec un adaptateur HTTP/JSON fourni par l'enseignant.

Pour compiler le projet capteurs depuis la racine du depot:

```bash
make capteurs
```

Pour produire l'archive etudiante de ce projet:

```bash
make capteurs-student-tarball
```

Puis consulter `capteurs-starter/SUJET.md`.

---

Le projet sert de fil rouge entre les seances. Le starter montre la structure
attendue : code metier separe, executable principal, tests et Makefile.

## Commandes

```bash
cd starter
make
make run
make test
make memcheck
make clean
```

## Jalons proposés

Le projet capteurs suit trois jalons : prise en main autonome, statistiques sur
pile, puis une phase finale organisée en trois étapes (série dynamique,
rapports, CLI/CSV). Consulter `capteurs-starter/SUJET.md` pour les commandes
associées.
