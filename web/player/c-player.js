<script>
class CPlayer extends HTMLElement {
  t(key, values) {
    return window.SAECMessages.t(`cPlayer.${key}`, values);
  }

  connectedCallback() {
    this.exercise = this.parseExercise();
    this.readonly = this.dataset.readonly === "true";
    this.contentKind = this.dataset.contentKind || "";
    this.initialCode = this.exercise.files?.[0]?.content || "";
    this.browserRunnable = this.exercise.browser_runnable !== false;
    this.render();
  }

  disconnectedCallback() {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
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
    const title = this.exercise.title || this.t("defaultTitle");
    const parameters = this.exercise.argv || this.exercise.stdin || "";
    const usesStdin = this.exercise.uses_stdin === true;
    const usesArgs = this.exercise.uses_args === true;
    const runDisabled = this.browserRunnable ? "" : "disabled";
    const runnableLabel = this.browserRunnable ? "" : `<span class="c-player__badge">${this.escape(this.t("localOnly"))}</span>`;
    const kindLabel = this.contentKind
      ? `<span class="content-kind content-kind--${this.escape(this.contentKind)}"><span class="content-kind__icon" aria-hidden="true">${this.contentKind === "exercise" ? "&lt;/&gt;" : "{}"}</span>${this.escape(window.SAECMessages.t(`contentType.${this.contentKind}`))}</span>`
      : "";
    const parametersBlock = this.browserRunnable
      ? `
            <details class="c-player__parameters-details" ${usesStdin || usesArgs ? "open" : ""}>
              <summary class="c-player__field-title">
                ${this.escape(this.t("parameters"))}
                <span
                  class="c-player__help"
                  tabindex="0"
                  title="${this.escape(this.t("parametersHelp"))}"
                >(?)</span>
              </summary>
              <textarea class="c-player__parameters" spellcheck="false">${this.escape(parameters)}</textarea>
            </details>`
      : "";
    const outputBlock = this.browserRunnable
      ? `
          <div class="c-player__output">
            <div class="c-player__panel c-player__panel--unified">
              <strong>${this.escape(this.t("outputs"))}</strong>
              <pre class="c-player__combined-output"></pre>
            </div>
          </div>`
      : "";
    const bodyClass = this.browserRunnable ? "c-player__body" : "c-player__body c-player__body--single";
    this.innerHTML = `
      <div class="c-player${this.contentKind ? ` c-player--${this.escape(this.contentKind)}` : ""}" tabindex="0">
        <div class="c-player__bar">
          <span class="c-player__title">${kindLabel}<span>${this.escape(title)}</span> ${runnableLabel}</span>
        </div>
        <div class="c-player__note">
          <span class="c-player__status">${this.escape(this.t("initializing"))}</span>
        </div>
        <div class="${bodyClass}">
          <div class="c-player__editor">
            <label>
              <strong>${this.escape(this.t("starterCode"))}</strong>
              <span class="c-player__code-wrap">
                <pre class="c-player__highlight" aria-hidden="true"></pre>
                <textarea class="c-player__code" spellcheck="false" ${this.readonly ? "readonly" : ""}>${this.escape(this.initialCode)}</textarea>
              </span>
            </label>
            ${parametersBlock}
          </div>
          ${outputBlock}
        </div>
        <div class="c-player__footer">
          <span class="c-player__actions">
            <button class="c-player__run" type="button" ${runDisabled}>${this.escape(this.t("run"))} <kbd class="c-player__enter-key" aria-hidden="true">&#9166;</kbd></button>
            <button class="c-player__reset" type="button">${this.escape(this.t("reset"))}</button>
          </span>
        </div>
      </div>
    `;
    this.querySelector(".c-player__run").addEventListener("click", () => this.run());
    this.querySelector(".c-player__reset").addEventListener("click", () => this.reset());
    const player = this.querySelector(".c-player");
    player.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && event.target === player && !this.querySelector(".c-player__run").disabled) {
        event.preventDefault();
        this.run();
      }
    });
    this.setupCodeEditor();
    this.updateStatus();
  }

  setupCodeEditor() {
    const textarea = this.querySelector(".c-player__code");
    if (!textarea) {
      return;
    }
    if (window.CodeMirror) {
      const wrap = this.querySelector(".c-player__code-wrap");
      const highlight = this.querySelector(".c-player__highlight");
      if (wrap) {
        wrap.classList.add("c-player__code-wrap--codemirror");
      }
      if (highlight) {
        highlight.hidden = true;
      }
      this.editor = window.CodeMirror.fromTextArea(textarea, {
        mode: "text/x-csrc",
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: false,
        readOnly: this.readonly ? "nocursor" : false,
        theme: this.codeMirrorTheme(),
        viewportMargin: Infinity,
      });
      this.editor.setSize("100%", "18rem");
      this.themeObserver = new MutationObserver(() => {
        this.editor.setOption("theme", this.codeMirrorTheme());
      });
      this.themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ["data-bs-theme"] });
      return;
    }

    textarea.addEventListener("input", () => this.refreshHighlight());
    textarea.addEventListener("scroll", () => this.syncHighlightScroll());
    this.refreshHighlight();
  }

  codeMirrorTheme() {
    return document.documentElement.getAttribute("data-bs-theme") === "dark" ? "material-darker" : "default";
  }

  getCode() {
    return this.editor ? this.editor.getValue() : this.querySelector(".c-player__code").value;
  }

  setCode(value) {
    if (this.editor) {
      this.editor.setValue(value);
    } else {
      this.querySelector(".c-player__code").value = value;
    }
  }

  reset() {
    this.setCode(this.initialCode);
    const parameters = this.querySelector(".c-player__parameters");
    if (parameters) {
      parameters.value = this.exercise.argv || this.exercise.stdin || "";
    }
    this.clearOutputs();
    this.refreshHighlight();
  }

  async run() {
    this.clearOutputs();
    if (!this.browserRunnable) {
      const newline = String.fromCharCode(10);
      this.show({
        compilerStderr: this.t("localOnlyOutput"),
      });
      this.setStatus(this.t("localOnlyStatus"));
      return;
    }

    const source = this.getCode();
    const parameters = this.querySelector(".c-player__parameters")?.value || "";
    const argv = parameters.trim() ? parameters.trim().split(/\s+/).join("\n") : "";

    if (window.CCompilerRuntime?.run) {
      this.setStatus(this.t("compiling"));
      try {
        const result = await window.CCompilerRuntime.run({
          exercise: this.exercise,
          source,
          stdin: parameters,
          argv,
        });
        this.show(result);
        const hasStderr = [result.compilerStderr, result.programStderr]
          .some((stream) => String(stream || "").trim().length > 0);
        this.setStatus(this.t(hasStderr ? "completedWithErrors" : "completed"));
      } catch (error) {
        const newline = String.fromCharCode(10);
        this.show({
          compilerStderr: this.t("runtimeError", { error: error.message || error }),
        });
        this.setStatus(this.t("runtimeErrorStatus"));
      }
      return;
    }

    const unchanged = source.trim() === this.initialCode.trim();
    const newline = String.fromCharCode(10);
    this.show({
      compilerStdout: unchanged ? this.t("referenceCompilation") : "",
      compilerStderr: unchanged
        ? this.t("runtimeUnavailableReference")
        : this.t("runtimeUnavailableChanged"),
      programStdout: unchanged ? (this.exercise.expected_stdout || "") : "",
      programStderr: unchanged ? (this.exercise.expected_stderr || "") : "",
    });
    this.setStatus(this.t("runtimeUnavailableStatus"));
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
    const output = this.querySelector(".c-player__combined-output");
    if (output) {
      output.innerHTML = html;
    }
  }

  clearOutputs() {
    if (!this.querySelector(".c-player__combined-output")) {
      return;
    }
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
      this.setStatus(this.t("localMakefileStatus"));
    } else if (window.CCompilerRuntime?.ready === false) {
      this.setStatus(this.t("runtimeWaiting"));
    } else if (window.CCompilerRuntime?.run) {
      this.setStatus(this.t("runtimeReady"));
    } else {
      this.setStatus(this.t("runtimeUnavailableStatus"));
    }
  }

  refreshHighlight() {
    const code = this.querySelector(".c-player__code");
    const highlight = this.querySelector(".c-player__highlight");
    if (!code || !highlight) {
      return;
    }
    highlight.innerHTML = this.highlightC(code.value);
    this.syncHighlightScroll();
  }

  syncHighlightScroll() {
    const code = this.querySelector(".c-player__code");
    const highlight = this.querySelector(".c-player__highlight");
    if (!code || !highlight) {
      return;
    }
    highlight.scrollTop = code.scrollTop;
    highlight.scrollLeft = code.scrollLeft;
  }

  highlightC(source) {
    const tokenPattern = /(\/\*[\s\S]*?\*\/|\/\/[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|^\s*#\s*[A-Za-z_][A-Za-z0-9_]*|\b(?:auto|break|case|const|continue|default|do|else|enum|extern|for|goto|if|register|return|sizeof|static|struct|switch|typedef|union|volatile|while)\b|\b(?:char|double|float|int|long|short|signed|unsigned|void|size_t|FILE|bool)\b|\b(?:NULL|EXIT_SUCCESS|EXIT_FAILURE|true|false)\b|\b(?:0[xX][0-9A-Fa-f]+|\d+(?:\.\d+)?)\b)/gm;
    let cursor = 0;
    let html = "";
    for (const match of source.matchAll(tokenPattern)) {
      html += this.escape(source.slice(cursor, match.index));
      html += this.highlightToken(match[0]);
      cursor = match.index + match[0].length;
    }
    html += this.escape(source.slice(cursor));
    if (html.endsWith("\n")) {
      html += " ";
    }
    return html;
  }

  highlightToken(token) {
    let kind = "plain";
    if (token.startsWith("/*") || token.startsWith("//")) {
      kind = "comment";
    } else if (token.startsWith('"') || token.startsWith("'")) {
      kind = "string";
    } else if (/^\s*#/.test(token)) {
      kind = "preproc";
    } else if (/^(char|double|float|int|long|short|signed|unsigned|void|size_t|FILE|bool)$/.test(token)) {
      kind = "type";
    } else if (/^(NULL|EXIT_SUCCESS|EXIT_FAILURE|true|false)$/.test(token)) {
      kind = "constant";
    } else if (/^(0[xX][0-9A-Fa-f]+|\d+(?:\.\d+)?)$/.test(token)) {
      kind = "number";
    } else {
      kind = "keyword";
    }
    return `<span class="c-token c-token--${kind}">${this.escape(token)}</span>`;
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
