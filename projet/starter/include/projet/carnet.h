#ifndef CARNET_H
#define CARNET_H

typedef struct Contact Contact;

Contact *contact_creer(const char *nom, int age);
const char *contact_nom(const Contact *contact);
int contact_age(const Contact *contact);
void contact_liberer(Contact *contact);

#endif

