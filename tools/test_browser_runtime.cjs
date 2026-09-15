const assert = require("node:assert/strict");

global.window = global;
global.document = { addEventListener() {}, removeEventListener() {} };
require("../web/player/tscc/tscc-bundle.js");

async function main() {
  const source = `#include <stdio.h>
int main(void)
{
    int i = 0;
    int m = 10;
    while (i < m) {
        printf("%d\\n", i);
        i++;
    }
    return 0;
}`;
  const result = await global.CCompilerRuntime.run({ source, stdin: "" });

  assert.equal(result.compilerStderr, "");
  assert.equal(result.programStderr, "");
  assert.equal(result.programStdout, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n");
  process.stdout.write("Runtime navigateur : boucle while avec printf validée.\n");
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
