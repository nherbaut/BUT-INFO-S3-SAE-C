# Corriger les diagnostics du compilateur

Travaillez dans `src/main.c` et lancez `make` apres chaque correction. Le
Makefile transforme les warnings demandes en erreurs afin de les rendre
visibles.

Corrigez les points suivants :

- point-virgule manquant ;
- variable non declaree ;
- format de `printf` incompatible avec l'argument ;
- adresse manquante dans l'appel a `scanf` ;
- affectation a la place d'une comparaison ;
- lecture d'une variable non initialisee ;
- conversion de `double` vers `int` qui perd une information ;
- comparaison entre un indice signe et une taille non signee ;
- ecriture apres le dernier element d'un tableau.

Le programme corrige lit un entier, affiche `conversion = 3.7`, calcule la
somme du tableau et affiche le maximum entre ses elements et l'entree. Testez
la version finale avec `make test`.
