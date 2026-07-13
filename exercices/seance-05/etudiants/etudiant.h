#ifndef ETUDIANT_H
#define ETUDIANT_H

typedef struct Etudiant Etudiant;

Etudiant *etudiant_creer(const char *nom, double moyenne);
void etudiant_afficher(const Etudiant *e);
void etudiant_liberer(Etudiant *e);

#endif

