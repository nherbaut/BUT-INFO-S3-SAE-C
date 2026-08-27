<script>
class CTypingPlayer extends HTMLElement {
  t(key, values) {
    return window.SAECMessages.t(`typing.${key}`, values);
  }

  contentType() {
    return window.SAECMessages.t("contentType.guidedReading");
  }

  connectedCallback() {
    this.lesson = this.parseLesson();
    this.language = this.lesson.language || "c";
    try {
      const parsed = this.parseAnnotatedSource(this.lesson.source || "");
      this.source = parsed.source;
      this.steps = parsed.steps;
      this.commentedSource = this.commentSource(this.lesson.source || "");
      this.lessonError = "";
    } catch (error) {
      this.source = "";
      this.steps = [];
      this.commentedSource = "";
      this.lessonError = error.message || String(error);
    }
    this.audioKey = "sae-c.typing-player.muted.v1";
    this.completionKey = "sae-c.typing-player.completed.v1";
    this.commentsKey = "sae-c.typing-player.c-comments.v1";
    this.reset({ showCompleted: this.wasCompleted() });
  }

  disconnectedCallback() {
    this.stopAudio(true);
    window.clearTimeout(this.timer);
    window.cancelAnimationFrame(this.followFrame);
  }

  parseLesson() {
    const bytes = Uint8Array.from(atob(this.dataset.lessonB64 || ""), (char) => char.charCodeAt(0));
    return JSON.parse(new TextDecoder("utf-8").decode(bytes));
  }

  parseAnnotatedSource(source) {
    if (this.language === "bash") {
      return this.parseBashAnnotatedSource(source);
    }
    const steps = [];
    const matcher = /\/\*\*([\s\S]*?)\*\//g;
    let cursor = 0;
    let visibleSource = "";
    let annotation = null;
    let skipLeadingNewline = false;

    const appendVisible = (fragment) => {
      let normalized = fragment;
      if (skipLeadingNewline) {
        normalized = normalized.replace(/^\r?\n/, "");
        skipLeadingNewline = false;
      }
      if (!visibleSource) {
        normalized = normalized.replace(/^\r?\n/, "");
      }
      if (visibleSource.endsWith("\n") && normalized.startsWith("\n")) {
        normalized = normalized.replace(/^\r?\n/, "");
      }
      visibleSource += normalized;
    };

    for (const match of source.matchAll(matcher)) {
      appendVisible(source.slice(cursor, match.index));
      const comment = match[1]
        .split("\n")
        .map((line) => line.replace(/^\s*\*?\s?/, ""))
        .join("\n")
        .trim();
      if (!comment) {
        if (!annotation) {
          throw new Error(this.t("noOpenAnnotation"));
        }
        const end = visibleSource.replace(/\r?\n+$/, "").length;
        if (end <= annotation.start) {
          throw new Error(this.t("emptyAnnotation", { title: annotation.title }));
        }
        steps.push({ ...annotation, until: end, colorIndex: steps.length % 6 });
        annotation = null;
        cursor = match.index + match[0].length;
        skipLeadingNewline = true;
        continue;
      }
      if (annotation) {
        throw new Error(this.t("nestedAnnotation", { title: annotation.title }));
      }
      const lines = comment.split("\n");
      const title = lines.shift().trim();
      const body = lines.join("\n").trim();
      annotation = {
        title,
        body,
        start: visibleSource.length,
      };
      cursor = match.index + match[0].length;
      skipLeadingNewline = true;
    }
    appendVisible(source.slice(cursor));
    if (annotation) {
      throw new Error(this.t("unclosedAnnotation", { title: annotation.title }));
    }
    return {
      source: visibleSource,
      steps: steps.map((step) => ({
        ...step,
        lines: [this.lineAt(visibleSource, step.start), this.lineAt(visibleSource, Math.max(step.start, step.until - 1))],
      })),
    };
  }

  parseBashAnnotatedSource(source) {
    const steps = [];
    const visibleLines = [];
    let annotation = null;

    for (const line of source.split(/\r?\n/)) {
      const marker = line.match(/^##(?:\s+(.*?))?\s*$/);
      if (marker) {
        const title = (marker[1] || "").trim();
        if (title) {
          if (annotation) {
            throw new Error(this.t("nestedBashAnnotation", { title: annotation.title }));
          }
          annotation = { title, body: [], start: visibleLines.join("\n").length };
        } else {
          if (!annotation) {
            throw new Error(this.t("noOpenBashAnnotation"));
          }
          const visibleSource = visibleLines.join("\n");
          const end = visibleSource.replace(/\n+$/, "").length;
          if (end <= annotation.start) {
            throw new Error(this.t("emptyBashAnnotation", { title: annotation.title }));
          }
          steps.push({ ...annotation, body: annotation.body.join("\n").trim(), until: end, colorIndex: steps.length % 6 });
          annotation = null;
        }
        continue;
      }
      const comment = annotation ? line.match(/^#(?: ?(.*))?$/) : null;
      if (comment) {
        annotation.body.push(comment[1] || "");
        continue;
      }
      visibleLines.push(line);
    }

    if (annotation) {
      throw new Error(this.t("unclosedBashAnnotation", { title: annotation.title }));
    }

    const visibleSource = visibleLines.join("\n");
    return {
      source: visibleSource,
      steps: steps.map((step) => ({
        ...step,
        lines: [this.lineAt(visibleSource, step.start), this.lineAt(visibleSource, Math.max(step.start, step.until - 1))],
      })),
    };
  }

  commentSource(source) {
    if (this.language === "bash") {
      return source.replace(/^##\s*$/gm, "");
    }
    return source.replace(/\/\*\*\s*\*\//g, "");
  }

  lineAt(source, index) {
    return source.slice(0, index).split("\n").length;
  }

  render() {
    const muted = localStorage.getItem(this.audioKey) === "true";
    const title = this.lesson.title || this.t("defaultTitle");
    const titleSuffix = this.lesson.title ? `<span>${this.escape(this.lesson.title)}</span>` : "";
    if (this.lessonError) {
      this.innerHTML = `
        <section class="c-typing-player" aria-label="${this.escape(title)}">
          <header class="c-typing-player__bar"><strong><span class="content-kind content-kind--guided-reading"><span class="content-kind__icon" aria-hidden="true">&gt;_</span>${this.escape(this.contentType())}</span>${titleSuffix}</strong></header>
          <div class="alert alert-danger m-3 mb-0">${this.escape(this.t("invalidAnnotation", { error: this.lessonError }))}</div>
        </section>
      `;
      return;
    }
    this.innerHTML = `
      <section class="c-typing-player" aria-label="${this.escape(title)}">
        <header class="c-typing-player__bar">
          <strong><span class="content-kind content-kind--guided-reading"><span class="content-kind__icon" aria-hidden="true">&gt;_</span>${this.escape(this.contentType())}</span>${titleSuffix}</strong>
          <div class="c-typing-player__actions">
            <label class="visually-hidden" for="typing-speed-${this.lesson.id}">${this.escape(this.t("speed"))}</label>
            <select class="form-select form-select-sm c-typing-player__speed" id="typing-speed-${this.lesson.id}">
              <option value="36">${this.escape(this.t("speedSlow"))}</option>
              <option value="18" selected>${this.escape(this.t("speedNormal"))}</option>
              <option value="7">${this.escape(this.t("speedFast"))}</option>
            </select>
            <button class="btn btn-outline-secondary btn-sm c-typing-player__icon-button c-typing-player__mute" type="button" aria-label="${this.escape(this.t(muted ? "soundMuted" : "soundActive"))}" title="${this.escape(this.t(muted ? "soundMuted" : "soundActive"))}" aria-pressed="${muted}">${muted ? "🔇" : "🔊"}</button>
            <button class="btn btn-outline-secondary btn-sm c-typing-player__icon-button c-typing-player__reset" type="button" aria-label="${this.escape(this.t("reset"))}" title="${this.escape(this.t("reset"))}" disabled>↺</button>
          </div>
        </header>
        <div class="c-typing-player__status" aria-live="polite">${this.escape(this.t("ready"))}</div>
        <div class="c-typing-player__layout">
          <div class="c-typing-player__canvas c-typing-player__canvas--empty" tabindex="0" aria-label="${this.escape(this.t("canvasLabel"))}">
            <pre class="c-typing-player__code"></pre>
            <button class="btn btn-primary c-typing-player__start" type="button">${this.escape(this.t("start"))}</button>
          </div>
          <aside class="c-typing-player__notes" aria-live="polite">
            <div class="c-typing-player__step">${this.escape(this.t("initialStep", { total: this.steps.length }))}</div>
            <h3 class="h6 c-typing-player__note-title">${this.escape(this.t("preparedTitle"))}</h3>
            <p class="mb-0 c-typing-player__note-body">${this.escape(this.t("preparedBody"))}</p>
            <div class="c-typing-player__note-actions">
              <button class="btn btn-primary btn-sm c-typing-player__play" type="button" hidden>${this.escape(this.t("play"))}</button>
              <button class="btn btn-outline-primary btn-sm c-typing-player__next" type="button" hidden>${this.escape(this.t("next"))}</button>
              <button class="btn btn-outline-secondary btn-sm c-typing-player__comments" type="button" hidden></button>
            </div>
          </aside>
        </div>
        <audio class="c-typing-player__audio c-typing-player__audio--typing" preload="none" loop src="player/typing.mp3"></audio>
        <audio class="c-typing-player__audio c-typing-player__audio--matrix" preload="none" loop src="player/matrix.mp3"></audio>
      </section>
    `;
    this.querySelector(".c-typing-player__start").addEventListener("click", () => this.start());
    this.querySelector(".c-typing-player__play").addEventListener("click", () => this.play());
    this.querySelector(".c-typing-player__next").addEventListener("click", () => this.next());
    this.querySelector(".c-typing-player__reset").addEventListener("click", () => this.reset());
    this.querySelector(".c-typing-player__mute").addEventListener("click", () => this.toggleMute());
    this.querySelector(".c-typing-player__comments").addEventListener("click", () => this.toggleComments());
    const code = this.querySelector(".c-typing-player__code");
    code.addEventListener("pointerup", () => this.copySelectedCode());
    code.addEventListener("keyup", () => this.copySelectedCode());
    code.addEventListener("mouseover", (event) => this.previewAnnotation(event));
    code.addEventListener("mouseout", (event) => this.clearPreview(event));
    code.addEventListener("focusin", (event) => this.previewAnnotation(event));
    code.addEventListener("focusout", (event) => this.clearPreview(event));
    code.addEventListener("click", (event) => this.pinAnnotation(event));
    code.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        this.pinAnnotation(event);
      }
    });
    this.noteState = {
      step: this.t("initialStep", { total: this.steps.length }),
      title: this.t("preparedTitle"),
      body: this.t("preparedBody"),
    };
  }

  reset({ showCompleted = false } = {}) {
    window.clearTimeout(this.timer);
    window.cancelAnimationFrame(this.followFrame);
    this.followFrame = null;
    this.visible = "";
    this.stepIndex = 0;
    this.typing = false;
    this.pausedAtStep = false;
    this.completed = false;
    this.showCComments = false;
    this.hoveredStepIndex = null;
    this.pinnedStepIndex = null;
    this.audioMode = null;
    this.stopAudio(true);
    this.render();
    if (showCompleted) {
      this.showCompleted();
    }
  }

  wasCompleted() {
    try {
      const completed = JSON.parse(localStorage.getItem(this.completionKey) || "{}");
      return completed[this.lesson.id] === true;
    } catch (_error) {
      return false;
    }
  }

  markCompleted() {
    try {
      const completed = JSON.parse(localStorage.getItem(this.completionKey) || "{}");
      completed[this.lesson.id] = true;
      localStorage.setItem(this.completionKey, JSON.stringify(completed));
    } catch (_error) {
      // The player remains usable if localStorage is unavailable.
    }
  }

  prefersCComments() {
    try {
      const preferences = JSON.parse(localStorage.getItem(this.commentsKey) || "{}");
      return preferences[this.lesson.id] === true;
    } catch (_error) {
      return false;
    }
  }

  saveCCommentsPreference() {
    try {
      const preferences = JSON.parse(localStorage.getItem(this.commentsKey) || "{}");
      preferences[this.lesson.id] = this.showCComments;
      localStorage.setItem(this.commentsKey, JSON.stringify(preferences));
    } catch (_error) {
      // The player remains usable if localStorage is unavailable.
    }
  }

  showCompleted() {
    this.visible = this.source;
    this.stepIndex = this.steps.length;
    this.completed = true;
    this.pinnedStepIndex = null;
    this.showCComments = this.prefersCComments();
    this.noteState = {
      step: this.t("completeStep", { total: this.steps.length }),
      title: this.t("completeTitle"),
      body: this.t("completeBody"),
    };
    this.renderNote(this.noteState);
    this.querySelector(".c-typing-player__start").hidden = true;
    this.querySelector(".c-typing-player__reset").disabled = false;
    this.querySelector(".c-typing-player__play").hidden = false;
    this.querySelector(".c-typing-player__play").textContent = this.t("replay");
    this.querySelector(".c-typing-player__next").hidden = true;
    this.querySelector(".c-typing-player__comments").hidden = false;
    this.updateCommentsButton();
    this.setStatus(this.t("completed"));
    this.updateCode();
  }

  toggleComments() {
    if (!this.completed) {
      return;
    }
    this.showCComments = !this.showCComments;
    this.saveCCommentsPreference();
    this.updateCommentsButton();
    if (this.showCComments) {
      this.renderNote({
        step: this.t("completeStep", { total: this.steps.length }),
        title: this.t("cCommentsTitle"),
        body: this.t("cCommentsBody"),
      });
    } else {
      this.renderNote(this.noteState);
    }
    this.updateCode();
  }

  updateCommentsButton() {
    const button = this.querySelector(".c-typing-player__comments");
    const label = this.t(this.showCComments ? "showGuidedReading" : "showCComments");
    button.textContent = label;
    button.setAttribute("aria-pressed", String(this.showCComments));
  }

  start() {
    this.querySelector(".c-typing-player__start").hidden = true;
    this.querySelector(".c-typing-player__reset").disabled = false;
    this.querySelector(".c-typing-player__play").hidden = false;
    this.querySelector(".c-typing-player__next").hidden = false;
    this.play();
  }

  play() {
    if (this.typing) {
      this.pause();
      return;
    }
    if (this.completed) {
      this.reset();
      this.start();
      return;
    }
    if (this.pausedAtStep) {
      this.pausedAtStep = false;
    }
    this.hoveredStepIndex = null;
    this.pinnedStepIndex = null;
    this.typing = true;
    this.setStatus(this.t("typing"));
    this.querySelector(".c-typing-player__play").textContent = this.t("pause");
    this.tick();
  }

  pause() {
    this.typing = false;
    window.clearTimeout(this.timer);
    this.stopAudio(false);
    this.setStatus(this.t("paused"));
    this.querySelector(".c-typing-player__play").textContent = this.t("play");
    this.updateCode();
  }

  next() {
    if (this.completed) {
      return;
    }
    if (this.typing) {
      this.visible = this.source.slice(0, this.nextTarget());
      this.arriveAtTarget();
      return;
    }
    this.play();
  }

  tick() {
    if (!this.typing) {
      return;
    }
    const target = this.nextTarget();
    if (this.visible.length >= target) {
      this.arriveAtTarget();
      return;
    }
    const character = this.source[this.visible.length];
    const audioMode = this.audioModeForIndex(this.visible.length);
    this.startAudio(audioMode);
    this.visible += character;
    this.updateCode();
    const speed = Number(this.querySelector(".c-typing-player__speed").value);
    const delay = audioMode === "matrix"
      ? Math.max(3, character === "\n" ? speed * 0.3 : speed * 0.15)
      : audioMode === "silent"
        ? Math.max(3, speed * 0.2)
        : character === "\n" ? speed * 2.6 : /[;{}]/.test(character) ? speed * 1.6 : speed;
    this.timer = window.setTimeout(() => this.tick(), delay);
  }

  audioModeForIndex(index) {
    if (this.language !== "bash") {
      return "typing";
    }
    const lineStart = this.source.lastIndexOf("\n", index - 1) + 1;
    const lineEnd = this.source.indexOf("\n", index);
    const line = this.source.slice(lineStart, lineEnd === -1 ? this.source.length : lineEnd);
    if (!line.trim()) {
      return "silent";
    }
    return this.isBashPrompt(line) ? "typing" : "matrix";
  }

  isBashPrompt(line) {
    return /^[^\r\n]*[#$]\s/.test(line);
  }

  nextTarget() {
    return this.steps[this.stepIndex]?.until ?? this.source.length;
  }

  arriveAtTarget() {
    this.typing = false;
    this.stopAudio(false);
    if (this.stepIndex < this.steps.length) {
      const step = this.steps[this.stepIndex];
      this.stepIndex += 1;
      this.pausedAtStep = true;
      this.pinnedStepIndex = this.stepIndex - 1;
      this.setAnnotationNote(this.pinnedStepIndex);
      this.querySelector(".c-typing-player__play").textContent = this.t("continue");
      this.setStatus(this.t("explanationPause"));
    } else {
      this.completed = true;
      this.markCompleted();
      this.pinnedStepIndex = null;
      this.noteState = {
        step: this.t("completeStep", { total: this.steps.length }),
        title: this.t("completeTitle"),
        body: this.t("completeBody"),
      };
      this.renderNote(this.noteState);
      this.querySelector(".c-typing-player__play").textContent = this.t("replay");
      this.querySelector(".c-typing-player__next").hidden = true;
      this.querySelector(".c-typing-player__comments").hidden = false;
      this.updateCommentsButton();
      this.setStatus(this.t("completed"));
    }
    this.updateCode();
  }

  updateCode() {
    if (this.showCComments) {
      this.updateCommentedCode();
      return;
    }
    const lines = this.visible.split("\n");
    const code = lines.map((line, index) => {
      const number = index + 1;
      const annotationIndex = this.annotationIndexForLine(number);
      const step = annotationIndex === null ? null : this.steps[annotationIndex];
      const selected = annotationIndex !== null && annotationIndex === (this.hoveredStepIndex ?? this.pinnedStepIndex);
      const cursor = this.typing && index === lines.length - 1 ? '<span class="c-typing-player__cursor"></span>' : "";
      const annotationClass = step ? ` c-typing-player__line--annotation-${step.colorIndex}` : "";
      const selectedClass = selected ? " c-typing-player__line--selected" : "";
      const interactive = step ? ` data-annotation-index="${annotationIndex}"` : "";
      const focusable = step && number === step.lines[0]
        ? ` tabindex="0" role="button" aria-label="${this.escape(this.t("annotationAria", { title: step.title }))}"`
        : "";
      return `<span class="c-typing-player__line${annotationClass}${selectedClass}"${interactive}${focusable}><span class="c-typing-player__line-number">${number}</span><span>${this.highlight(line)}${cursor}</span></span>`;
    }).join("");
    const canvas = this.querySelector(".c-typing-player__canvas");
    this.querySelector(".c-typing-player__code").innerHTML = code;
    canvas.classList.toggle("c-typing-player__canvas--empty", this.visible.length === 0);
    canvas.scrollTop = canvas.scrollHeight;
    this.followTypedLine();
  }

  followTypedLine() {
    if (!this.typing || this.followFrame) {
      return;
    }

    this.followFrame = window.requestAnimationFrame(() => {
      this.followFrame = null;
      if (!this.typing) {
        return;
      }

      const line = this.querySelector(".c-typing-player__line:last-child");
      if (!line || line.getBoundingClientRect().bottom <= window.innerHeight - 24) {
        return;
      }

      line.scrollIntoView({ block: "end", behavior: "smooth" });
    });
  }

  copySelectedCode() {
    const code = this.querySelector(".c-typing-player__code");
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed || selection.rangeCount === 0) {
      return;
    }

    const range = selection.getRangeAt(0);
    const withinCode = (node) => code.contains(node.nodeType === Node.ELEMENT_NODE ? node : node.parentNode);
    if (!withinCode(range.startContainer) || !withinCode(range.endContainer)) {
      return;
    }

    const fragment = range.cloneContents();
    fragment.querySelectorAll(".c-typing-player__line-number").forEach((lineNumber) => lineNumber.remove());
    const lines = Array.from(fragment.querySelectorAll(".c-typing-player__line"));
    const text = lines.length > 0 ? lines.map((line) => line.textContent).join("\n") : fragment.textContent;
    if (!text) {
      return;
    }

    const copied = () => this.setStatus(this.t("codeCopied"));
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(text).then(copied).catch(() => this.copyTextFallback(text, copied));
      return;
    }
    this.copyTextFallback(text, copied);
  }

  copyTextFallback(text, copied) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.append(textarea);
    textarea.select();
    const success = document.execCommand("copy");
    textarea.remove();
    if (success) {
      copied();
    } else {
      this.setStatus(this.t("codeCopyFailed"));
    }
  }

  updateCommentedCode() {
    const lines = this.commentedSource.split("\n");
    const code = lines.map((line, index) => {
      const number = index + 1;
      return `<span class="c-typing-player__line"><span class="c-typing-player__line-number">${number}</span><span>${this.highlight(line)}</span></span>`;
    }).join("");
    const canvas = this.querySelector(".c-typing-player__canvas");
    this.querySelector(".c-typing-player__code").innerHTML = code;
    canvas.classList.remove("c-typing-player__canvas--empty");
    canvas.scrollTop = 0;
  }

  annotationIndexForLine(number) {
    const index = this.steps.findIndex((step) => number >= step.lines[0] && number <= step.lines[1]);
    return index === -1 ? null : index;
  }

  annotationIndexFromEvent(event) {
    const line = event.target.closest("[data-annotation-index]");
    return line ? Number(line.dataset.annotationIndex) : null;
  }

  previewAnnotation(event) {
    const index = this.annotationIndexFromEvent(event);
    if (index === null || index === this.hoveredStepIndex) {
      return;
    }
    this.hoveredStepIndex = index;
    this.setAnnotationNote(index, false);
    this.updateCode();
  }

  clearPreview(event) {
    const index = this.annotationIndexFromEvent(event);
    const related = event.relatedTarget?.closest?.("[data-annotation-index]");
    if (index === null || related?.dataset.annotationIndex === String(index)) {
      return;
    }
    this.hoveredStepIndex = null;
    this.restoreNote();
    this.updateCode();
  }

  pinAnnotation(event) {
    const index = this.annotationIndexFromEvent(event);
    if (index === null) {
      return;
    }
    if (this.typing) {
      this.pause();
    }
    this.hoveredStepIndex = null;
    this.pinnedStepIndex = index;
    this.setAnnotationNote(index);
    this.updateCode();
  }

  setAnnotationNote(index, persist = true) {
    const step = this.steps[index];
    const state = {
      step: this.t("step", { current: index + 1, total: this.steps.length }),
      title: step.title,
      body: step.body || this.t("explanationFallback"),
    };
    if (persist) {
      this.noteState = state;
    }
    this.renderNote(state);
  }

  restoreNote() {
    if (this.pinnedStepIndex !== null) {
      this.setAnnotationNote(this.pinnedStepIndex, false);
      return;
    }
    this.renderNote(this.noteState);
  }

  renderNote(state) {
    this.querySelector(".c-typing-player__step").textContent = state.step;
    this.querySelector(".c-typing-player__note-title").textContent = state.title;
    this.querySelector(".c-typing-player__note-body").textContent = state.body;
  }

  highlight(line) {
    if (this.language === "bash") {
      return this.highlightBash(line);
    }
    const pattern = /(\/\/.*|\/\*.*?\*\/|"(?:\\.|[^"\\])*"|^\s*#.*|\b(?:int|void|return|if|else|for|while|const|static)\b|\b(?:0[xX][0-9a-fA-F]+|\d+)\b)/g;
    let cursor = 0;
    let result = "";
    for (const match of line.matchAll(pattern)) {
      result += this.escape(line.slice(cursor, match.index));
      const token = match[0];
      let kind = "keyword";
      if (token.startsWith("//") || token.startsWith("/*")) kind = "comment";
      else if (token.startsWith('"')) kind = "string";
      else if (/^\s*#/.test(token)) kind = "preproc";
      else if (/^\d|^0x/i.test(token)) kind = "number";
      result += `<span class="c-token c-token--${kind}">${this.escape(token)}</span>`;
      cursor = match.index + token.length;
    }
    return result + this.escape(line.slice(cursor));
  }

  highlightBash(line) {
    const pattern = /#.*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\$\{?[A-Za-z_][A-Za-z0-9_]*\}?|\b(?:cd|echo|printf|mkdir|rm|cp|mv|curl|make|gcc|clang|git|cat|head|tail|grep|rg|if|then|fi|for|in|do|done|while|case|esac)\b|--?[A-Za-z][A-Za-z0-9-]*/g;
    let cursor = 0;
    let result = "";
    for (const match of line.matchAll(pattern)) {
      result += this.escape(line.slice(cursor, match.index));
      const token = match[0];
      let kind = "keyword";
      if (token.startsWith("#")) kind = "comment";
      else if (token.startsWith('"') || token.startsWith("'")) kind = "string";
      else if (token.startsWith("$")) kind = "constant";
      else if (token.startsWith("-")) kind = "preproc";
      result += `<span class="c-token c-token--${kind}">${this.escape(token)}</span>`;
      cursor = match.index + token.length;
    }
    return result + this.escape(line.slice(cursor));
  }

  toggleMute() {
    const muted = localStorage.getItem(this.audioKey) !== "true";
    localStorage.setItem(this.audioKey, String(muted));
    const button = this.querySelector(".c-typing-player__mute");
    const label = this.t(muted ? "soundMuted" : "soundActive");
    button.textContent = muted ? "🔇" : "🔊";
    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
    button.setAttribute("aria-pressed", String(muted));
    if (muted) this.stopAudio(false);
    else if (this.typing) this.startAudio(this.audioModeForIndex(this.visible.length));
  }

  startAudio(mode) {
    if (localStorage.getItem(this.audioKey) === "true" || mode === "silent") {
      this.stopAudio(false);
      return;
    }
    const typingAudio = this.querySelector(".c-typing-player__audio--typing");
    const matrixAudio = this.querySelector(".c-typing-player__audio--matrix");
    const audio = mode === "matrix" ? matrixAudio : typingAudio;
    const other = mode === "matrix" ? typingAudio : matrixAudio;
    if (this.audioMode !== mode) {
      other.pause();
      other.currentTime = 0;
      this.audioMode = mode;
    }
    audio.volume = 0.2;
    if (audio.paused) {
      audio.play().catch(() => {});
    }
  }

  stopAudio(rewind) {
    for (const audio of this.querySelectorAll(".c-typing-player__audio")) {
      audio.pause();
      if (rewind) audio.currentTime = 0;
    }
    this.audioMode = null;
  }

  setStatus(text) {
    this.querySelector(".c-typing-player__status").textContent = text;
  }

  escape(value) {
    return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
  }
}

customElements.define("c-typing-player", CTypingPlayer);
</script>
