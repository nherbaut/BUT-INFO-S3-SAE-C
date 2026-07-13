# ts-c-compiler runtime

Runtime navigateur construit depuis le monorepo `Mati365/ts-c-compiler`.

- Source: https://github.com/Mati365/ts-c-compiler
- Version npm observee: `1.8.0`
- Usage: compilation C vers x86 16-bit, assemblage, execution par CPU JS, puis
  extraction de la sortie texte VGA.

Limites assumees pour les supports:

- ce n'est pas GCC/Clang;
- pas de compilation multi-fichiers dans le navigateur;
- `scanf(...)` simple est transforme en affectations depuis le champ `stdin`;
- les Makefiles locaux restent la reference pour le C complet.
