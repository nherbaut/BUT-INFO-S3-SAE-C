<script>
class QuizPlayer extends HTMLElement {
  connectedCallback() {
    this.quiz = this.parseQuiz();
    this.progress = this.readProgress();
    this.render();
  }

  parseQuiz() {
    const bytes = Uint8Array.from(atob(this.dataset.quizB64), (char) => char.charCodeAt(0));
    const json = new TextDecoder("utf-8").decode(bytes);
    return JSON.parse(json);
  }

  render() {
    const state = this.quizProgress();
    const validated = state.validated === true;
    this.innerHTML = `
      <section class="quiz-player card my-4" data-quiz-id="${this.escape(this.quiz.id)}">
        <div class="quiz-player__header card-header">
          <div>
            <h2 class="quiz-player__title h5">${this.escape(this.quiz.title)}</h2>
            ${this.quiz.description ? `<p class="quiz-player__description">${this.escape(this.quiz.description)}</p>` : ""}
          </div>
          <span class="quiz-player__badge badge ${validated ? "text-bg-success" : "text-bg-secondary"}">${validated ? "Valide" : "A faire"}</span>
        </div>
        <div class="card-body">
          ${this.quiz.questions.map((question, index) => this.renderQuestion(question, index)).join("")}
          <div class="quiz-player__actions">
            <button type="button" class="quiz-player__validate btn btn-primary">Valider</button>
            <button type="button" class="quiz-player__hint btn btn-info d-none">Afficher les indices</button>
          </div>
          <div class="quiz-player__feedback mt-3" aria-live="polite"></div>
        </div>
      </section>
    `;
    this.querySelector(".quiz-player__validate").addEventListener("click", () => this.validate());
    this.querySelector(".quiz-player__hint").addEventListener("click", () => this.showHints());
  }

  renderQuestion(question, index) {
    const options = this.shuffle(question.options, `${this.quiz.id}:${question.id}`);
    return `
      <fieldset class="quiz-player__question" data-question-id="${this.escape(question.id)}">
        <legend class="quiz-player__question-title">${index + 1}. ${this.escape(question.title)}</legend>
        ${question.description ? `<p class="quiz-player__question-description">${this.escape(question.description)}</p>` : ""}
        <div class="quiz-player__options">
          ${options.map((option) => this.renderOption(question, option)).join("")}
        </div>
        <div class="quiz-player__question-feedback"></div>
      </fieldset>
    `;
  }

  renderOption(question, option) {
    return `
      <label class="quiz-player__option form-check">
        <input class="form-check-input" type="checkbox" name="${this.escape(question.id)}" value="${this.escape(option.id)}">
        <span class="form-check-label">${this.escape(option.text)}</span>
      </label>
    `;
  }

  validate() {
    const quizState = this.quizProgress();
    let allCorrect = true;
    let firstWrongAttempt = false;
    let secondWrongAttempt = false;

    for (const question of this.quiz.questions) {
      const fieldset = this.querySelector(`[data-question-id="${this.escapeSelector(question.id)}"]`);
      const selected = new Set(Array.from(fieldset.querySelectorAll("input:checked"), (input) => input.value));
      const expected = new Set(question.options.filter((option) => option.correct).map((option) => option.id));
      const correct = this.sameSet(selected, expected);
      const questionState = quizState.questions[question.id] || { validated: false, attempts: 0 };
      if (correct) {
        questionState.validated = true;
      } else {
        questionState.validated = false;
        questionState.attempts += 1;
        allCorrect = false;
        firstWrongAttempt = firstWrongAttempt || questionState.attempts === 1;
        secondWrongAttempt = secondWrongAttempt || questionState.attempts >= 2;
      }
      quizState.questions[question.id] = questionState;
      this.renderQuestionFeedback(fieldset, question, questionState, correct);
    }

    quizState.validated = allCorrect;
    if (allCorrect) {
      quizState.validatedAt = new Date().toISOString();
    }
    this.progress[this.quiz.id] = quizState;
    this.writeProgress();
    this.updateQuizBadge(allCorrect);

    if (allCorrect) {
      this.setFeedback("Bonne reponse. Quiz valide.", "success");
      this.setValidateClass("btn-success");
      this.querySelector(".quiz-player__hint").classList.add("d-none");
    } else if (secondWrongAttempt) {
      this.setFeedback("Les bonnes reponses sont affichees.", "danger");
      this.setValidateClass("btn-danger");
      this.querySelector(".quiz-player__hint").classList.add("d-none");
      this.showAnswers();
    } else if (firstWrongAttempt) {
      this.setFeedback("Il manque au moins une bonne reponse.", "warning");
      this.setValidateClass("btn-warning");
      this.toggleHintButton();
    }
  }

  renderQuestionFeedback(fieldset, question, state, correct) {
    const feedback = fieldset.querySelector(".quiz-player__question-feedback");
    feedback.innerHTML = "";
    fieldset.classList.toggle("quiz-player__question--ok", correct);
    fieldset.classList.toggle("quiz-player__question--wrong", !correct && state.attempts > 0);
    if (correct) {
      feedback.innerHTML = '<div class="alert alert-success py-2 mt-2 mb-0">Question validee.</div>';
    }
  }

  toggleHintButton() {
    const hasHints = this.quiz.questions.some((question) => question.options.some((option) => option.hint));
    this.querySelector(".quiz-player__hint").classList.toggle("d-none", !hasHints);
  }

  showHints() {
    for (const question of this.quiz.questions) {
      const fieldset = this.querySelector(`[data-question-id="${this.escapeSelector(question.id)}"]`);
      const hints = question.options.filter((option) => option.hint).map((option) => `<li>${this.escape(option.hint)}</li>`).join("");
      if (hints) {
        fieldset.querySelector(".quiz-player__question-feedback").innerHTML = `<div class="alert alert-info py-2 mt-2 mb-0"><ul class="mb-0">${hints}</ul></div>`;
      }
    }
  }

  showAnswers() {
    for (const question of this.quiz.questions) {
      const fieldset = this.querySelector(`[data-question-id="${this.escapeSelector(question.id)}"]`);
      const expected = new Set(question.options.filter((option) => option.correct).map((option) => option.id));
      for (const input of fieldset.querySelectorAll("input")) {
        input.closest(".quiz-player__option").classList.toggle("quiz-player__option--answer", expected.has(input.value));
      }
    }
  }

  setFeedback(message, type) {
    this.querySelector(".quiz-player__feedback").innerHTML = `<div class="alert alert-${type} mb-0">${this.escape(message)}</div>`;
  }

  setValidateClass(className) {
    const button = this.querySelector(".quiz-player__validate");
    button.className = `quiz-player__validate btn ${className}`;
  }

  updateQuizBadge(validated) {
    const badge = this.querySelector(".quiz-player__badge");
    badge.className = `quiz-player__badge badge ${validated ? "text-bg-success" : "text-bg-secondary"}`;
    badge.textContent = validated ? "Valide" : "A faire";
  }

  quizProgress() {
    const existing = this.progress[this.quiz.id] || {};
    return {
      validated: existing.validated === true,
      validatedAt: existing.validatedAt || null,
      questions: existing.questions || {},
    };
  }

  readProgress() {
    try {
      return JSON.parse(localStorage.getItem("sae-c.quiz.progress.v1") || "{}");
    } catch (_error) {
      return {};
    }
  }

  writeProgress() {
    localStorage.setItem("sae-c.quiz.progress.v1", JSON.stringify(this.progress));
  }

  shuffle(values, seedText) {
    const items = values.slice();
    let seed = this.hash(seedText);
    for (let index = items.length - 1; index > 0; index -= 1) {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      const swapIndex = seed % (index + 1);
      [items[index], items[swapIndex]] = [items[swapIndex], items[index]];
    }
    return items;
  }

  hash(value) {
    let hash = 2166136261;
    for (const char of String(value)) {
      hash ^= char.charCodeAt(0);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  sameSet(left, right) {
    if (left.size !== right.size) {
      return false;
    }
    for (const value of left) {
      if (!right.has(value)) {
        return false;
      }
    }
    return true;
  }

  escapeSelector(value) {
    if (window.CSS?.escape) {
      return CSS.escape(value);
    }
    return String(value).replaceAll('"', '\\"');
  }

  escape(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }
}

customElements.define("quiz-player", QuizPlayer);
</script>
