# ts-c-compiler runtime

Runtime navigateur construit depuis le monorepo `Mati365/ts-c-compiler`.

- Source: https://github.com/Mati365/ts-c-compiler
- Version npm observee: `1.8.0`
- Usage: compilation C vers x86 16-bit, assemblage, execution par CPU JS, puis
  extraction de la sortie texte VGA.

Limites assumees pour les supports:

- ce n'est pas GCC/Clang;
- pas de compilation multi-fichiers dans le navigateur;
- les appels numériques à `scanf(...)` employés comme instructions sont
  transformés en lectures depuis le champ `stdin` ; les lectures répétées dans
  une boucle et les cibles de type `tableau[indice]` sont prises en charge ;
- les assistants simples recevant une question (`const char[]`) et un pointeur
  vers `int`, tels que `demander_entier`, sont développés à l'appel afin que
  leur question s'affiche correctement ;
- les structures simples composées de champs `int` sont aplaties pour contourner
  une limite du compilateur embarqué ; l'initialisation, `.` et `->` restent
  utilisables dans le code affiché ;
- les arguments `argc` et `argv` sont adaptés par `c-runtime-adapter.js` pour
  les signatures usuelles de `main`; cette adaptation est propre au support et
  ne remplace pas l'exécution locale;
- les Makefiles locaux restent la reference pour le C complet.
