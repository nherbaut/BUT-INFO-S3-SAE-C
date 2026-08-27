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
    return source.replace(
      /int\s+main\s*\(\s*int\s+([A-Za-z_][A-Za-z0-9_]*)\s*,\s*char\s*\*\s*(?:\*\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[\s*\])?\s*\)\s*\{/,
      (_match, argc, argv) => `int main(void) {\n    int ${argc} = ${argumentsList.length + 1};\n    char *${argv}[] = {${values}};`,
    );
  }

  runtime.run = ({ source, argv, ...options }) => run({
    ...options,
    source: injectArguments(source, argv),
  });
})();
</script>
