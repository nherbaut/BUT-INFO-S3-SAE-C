#include "projet/carnet.h"

#include <assert.h>
#include <string.h>

int main(void)
{
    Contact *contact = contact_creer("Grace", 42);

    assert(contact != NULL);
    assert(strcmp(contact_nom(contact), "Grace") == 0);
    assert(contact_age(contact) == 42);

    contact_liberer(contact);
    return 0;
}
