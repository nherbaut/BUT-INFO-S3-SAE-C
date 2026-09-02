# Construire un identifiant dynamique

Complétez `construire_identifiant` afin qu'elle retourne une chaîne allouée
dynamiquement au format `prenom.nom`.

Pour `"Ada"` et `"Lovelace"`, la fonction doit retourner `"Ada.Lovelace"`.
La taille à réserver comprend la longueur du prénom, celle du nom, le point et
l'octet final `\0`.

Utilisez `strlen`, `malloc`, `strcpy` et `strcat`. La fonction appelante devient
propriétaire de la chaîne retournée : elle doit donc l'appeler avec `free`.

`main` vérifie les résultats avec `strcmp`. Lancez `make test`, puis
`make memcheck` pour contrôler que chaque chaîne allouée est bien libérée.
