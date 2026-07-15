#include <assert.h>
#include <string.h>

#include <projet/greet.h>

int main(void)
{
    assert(strcmp(projet_greet(), "Bonjour depuis C11") == 0);
    return 0;
}
