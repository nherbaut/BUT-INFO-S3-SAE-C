<script>
class CPlayer extends HTMLElement {
  connectedCallback() {
    this.exercise = this.parseExercise();
    this.readonly = this.dataset.readonly === "true";
    this.initialCode = this.exercise.files?.[0]?.content || "";
    this.browserRunnable = this.exercise.browser_runnable !== false;
    this.render();
  }

  parseExercise() {
    if (this.dataset.exerciseB64) {
      const bytes = Uint8Array.from(atob(this.dataset.exerciseB64), (char) => char.charCodeAt(0));
      const json = new TextDecoder("utf-8").decode(bytes);
      return JSON.parse(json);
    }
    return JSON.parse(this.dataset.exercise || "{}");
  }

  render() {
    const title = this.exercise.title || "Programme C";
    const stdin = this.exercise.stdin || "";
    const runDisabled = this.browserRunnable ? "" : "disabled";
    const runnableLabel = this.browserRunnable ? "" : '<span class="c-player__badge">Local uniquement</span>';
    this.innerHTML = `
      <div class="c-player">
        <div class="c-player__bar">
          <span class="c-player__title">${this.escape(title)} ${runnableLabel}</span>
          <span class="c-player__actions">
            <button class="c-player__run" type="button" ${runDisabled}>Build & Run</button>
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
    if (!this.browserRunnable) {
      const newline = String.fromCharCode(10);
      this.show({
        compilerStderr: `Exercice multi-fichiers : execution navigateur indisponible.${newline}Telecharger le starter code ou cloner le depot, puis utiliser les commandes locales indiquees sous l'exercice.${newline}`,
      });
      this.setStatus("Exercice local uniquement.");
      return;
    }

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
        const newline = String.fromCharCode(10);
        this.show({
          compilerStderr: `Erreur runtime: ${error.message || error}${newline}`,
        });
        this.setStatus("Erreur runtime.");
      }
      return;
    }

    const unchanged = source.trim() === this.initialCode.trim();
    const newline = String.fromCharCode(10);
    this.show({
      compilerStdout: unchanged ? `Compilation de reference du support.${newline}` : "",
      compilerStderr: unchanged
        ? `Runtime navigateur non installe : sortie de reference affichee sans compilation reelle.${newline}`
        : `Runtime navigateur non installe : impossible de compiler les modifications dans le navigateur.${newline}Utiliser les commandes locales indiquees sous l'exercice.${newline}`,
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
    const newline = String.fromCharCode(10);
    const carriageReturn = String.fromCharCode(13);
    const lines = String(value)
      .split(carriageReturn).join("")
      .replace(new RegExp(`${newline}$`), "")
      .split(newline);
    return lines.map((line) => {
      const prefix = `[${origin}] `;
      return `<span class="c-player__line c-player__line--${kind}">${this.escape(prefix + line)}</span>${newline}`;
    });
  }

  setStatus(value) {
    this.querySelector(".c-player__status").textContent = value;
  }

  updateStatus() {
    if (!this.browserRunnable) {
      this.setStatus("Exercice multi-fichiers : utiliser le Makefile local.");
    } else if (window.CCompilerRuntime?.ready === false) {
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
