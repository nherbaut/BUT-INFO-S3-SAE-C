# Annuaire CSV

Le `main` construit un annuaire de deux personnes puis doit :

1. écrire les personnes dans un fichier CSV ;
2. relire ce fichier pour créer un second annuaire ;
3. afficher le second annuaire et libérer sa mémoire.

Le format imposé est une personne par ligne :

```text
prenom,nom,jour,mois,annee
Ada,Lovelace,10,12,1815
```

Complétez `ecrire_csv` avec `fopen`, `fprintf` et `fclose`, puis `lire_csv`
avec `fopen`, `fgets`, `sscanf`, `realloc` et `fclose`. Chaque erreur d'ouverture,
de lecture, de réallocation ou de fermeture doit faire retourner `0`.

Testez avec `make test`. Le fichier CSV de test est créé dans `build/`.
