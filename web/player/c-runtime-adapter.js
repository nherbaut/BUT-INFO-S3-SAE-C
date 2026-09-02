<script>
(() => {
  "use strict";

  const runtime = window.CCompilerRuntime;
  if (!runtime?.run) {
    return;
  }

  const run = runtime.run.bind(runtime);

  function quoteCString(value) {
    return `"${String(value).replaceAll("\\", "\\\\").replaceAll("\"", "\\\"").replaceAll("\n", "\\n").replaceAll("\r", "\\r")}"`;
  }

  function injectArguments(source, argvText) {
    const argumentsList = String(argvText || "").split(/\r?\n/).filter((argument) => argument.length > 0);
    const values = ["programme", ...argumentsList].map(quoteCString).join(", ");
    // The browser runtime only supports main(void). Accept usual C spellings
    // for argv before lowering them to local variables.
    return source.replace(
      /\bint\s+main\s*\(\s*int\s+([A-Za-z_][A-Za-z0-9_]*)\s*,\s*(?:const\s+)?char\s*\*\s*(?:\*\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[\s*(?:[A-Za-z_][A-Za-z0-9_]*|\d+)?\s*\])?\s*\)\s*\{/,
      (_match, argc, argv) => `int main(void) {\n    int ${argc} = ${argumentsList.length + 1};\n    char *${argv}[] = {${values}};`,
    );
  }

  runtime.run = ({ source, argv, ...options }) => run({
    ...options,
    source: injectArguments(source, argv),
  });
})();
</script>
