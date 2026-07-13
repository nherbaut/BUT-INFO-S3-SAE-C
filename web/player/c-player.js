<script>
class CPlayer extends HTMLElement {
  connectedCallback() {
    this.exercise = JSON.parse(this.dataset.exercise || "{}");
    this.readonly = this.dataset.readonly === "true";
    this.initialCode = this.exercise.files?.[0]?.content || "";
    this.render();
  }

  render() {
    const title = this.exercise.title || "Programme C";
    const stdin = this.exercise.stdin || "";
    this.innerHTML = `
      <div class="c-player">
        <div class="c-player__bar">
          <span class="c-player__title">${this.escape(title)}</span>
          <span class="c-player__actions">
            <button class="c-player__run" type="button">Build & Run</button>
            <button class="c-player__reset" type="button">Reset</button>
          </span>
        </div>
        <div class="c-player__note">
          <span class="c-player__status">Initialisation du runtime...</span>
        </div>
        <div class="c-player__body">
          <div class="c-player__editor">
            <label>
              <strong>Starter code</strong>
              <textarea class="c-player__code" spellcheck="false" ${this.readonly ? "readonly" : ""}>${this.escape(this.initialCode)}</textarea>
            </label>
            <label>
              <strong class="c-player__field-title">
                stdin
                <span
                  class="c-player__help"
                  tabindex="0"
                  title="Entree standard du programme : saisir ici les valeurs que le programme lirait au clavier. Separer les valeurs par des espaces ou des retours a la ligne, par exemple : 12 14"
                >(?)</span>
              </strong>
              <textarea class="c-player__stdin" spellcheck="false">${this.escape(stdin)}</textarea>
            </label>
          </div>
          <div class="c-player__output">
            <div class="c-player__panel c-player__panel--unified">
              <strong>Sorties</strong>
              <pre class="c-player__combined-output"></pre>
            </div>
          </div>
        </div>
      </div>
    `;
    this.querySelector(".c-player__run").addEventListener("click", () => this.run());
    this.querySelector(".c-player__reset").addEventListener("click", () => this.reset());
    this.updateStatus();
  }

  reset() {
    this.querySelector(".c-player__code").value = this.initialCode;
    this.querySelector(".c-player__stdin").value = this.exercise.stdin || "";
    this.clearOutputs();
  }

  async run() {
    this.clearOutputs();
    const source = this.querySelector(".c-player__code").value;
    const stdin = this.querySelector(".c-player__stdin").value;

    if (window.CCompilerRuntime?.run) {
      this.setStatus("Compilation en cours...");
      try {
        const result = await window.CCompilerRuntime.run({
          exercise: this.exercise,
          source,
          stdin,
        });
        this.show(result);
        this.setStatus("Execution terminee.");
      } catch (error) {
        this.show({
          compilerStderr: `Erreur runtime: ${error.message || error}\n`,
        });
        this.setStatus("Erreur runtime.");
      }
      return;
    }

    const unchanged = source.trim() === this.initialCode.trim();
    this.show({
      compilerStdout: unchanged ? "Compilation de reference du support.\n" : "",
      compilerStderr: unchanged
        ? "Runtime navigateur non installe : sortie de reference affichee sans compilation reelle.\n"
        : "Runtime navigateur non installe : impossible de compiler les modifications dans le navigateur.\nUtiliser les commandes locales indiquees sous l'exercice.\n",
      programStdout: unchanged ? (this.exercise.expected_stdout || "") : "",
      programStderr: unchanged ? (this.exercise.expected_stderr || "") : "",
    });
    this.setStatus("Runtime C navigateur absent : sortie de reference uniquement.");
  }

  show(result) {
    const streams = [
      ["comp-stdout", "stdout", result.compilerStdout || ""],
      ["comp-stderr", "stderr", result.compilerStderr || ""],
      ["prog-stdout", "stdout", result.programStdout || ""],
      ["prog-stderr", "stderr", result.programStderr || ""],
    ];
    const html = streams
      .flatMap(([origin, kind, value]) => this.formatStream(origin, kind, value))
      .join("");
    this.querySelector(".c-player__combined-output").innerHTML = html;
  }

  clearOutputs() {
    this.show({});
  }

  formatStream(origin, kind, value) {
    if (!value) {
      return [];
    }
    const lines = String(value).replace(/\r/g, "").replace(/\n$/, "").split("\n");
    return lines.map((line) => {
      const prefix = `[${origin}] `;
      return `<span class="c-player__line c-player__line--${kind}">${this.escape(prefix + line)}</span>\n`;
    });
  }

  setStatus(value) {
    this.querySelector(".c-player__status").textContent = value;
  }

  updateStatus() {
    if (window.CCompilerRuntime?.ready === false) {
      this.setStatus("Runtime C navigateur detecte, mais pas encore pret.");
    } else if (window.CCompilerRuntime?.run) {
      this.setStatus("Runtime C navigateur pret.");
    } else {
      this.setStatus("Runtime C navigateur absent : sortie de reference uniquement.");
    }
  }

  escape(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }
}

customElements.define("c-player", CPlayer);
</script>
