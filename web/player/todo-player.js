<script>
(() => {
  "use strict";

  const storageKey = "sae-c.todo.progress.v1";

  function readProgress() {
    try {
      return JSON.parse(localStorage.getItem(storageKey) || "{}");
    } catch (_error) {
      return {};
    }
  }

  function saveProgress(progress) {
    localStorage.setItem(storageKey, JSON.stringify(progress));
  }

  function launchConfetti(todo) {
    const target = todo.querySelector(".todo-confetti");
    target.replaceChildren();
    for (let index = 0; index < 24; index += 1) {
      const piece = document.createElement("span");
      piece.className = "todo-confetti__piece";
      piece.style.setProperty("--confetti-x", `${Math.round((Math.random() - 0.5) * 18)}rem`);
      piece.style.setProperty("--confetti-y", `${Math.round(5 + Math.random() * 7)}rem`);
      piece.style.setProperty("--confetti-rotate", `${Math.round((Math.random() - 0.5) * 720)}deg`);
      piece.style.setProperty("--confetti-delay", `${Math.round(Math.random() * 120)}ms`);
      piece.style.setProperty("--confetti-color", ["#0d6efd", "#198754", "#ffc107", "#dc3545", "#0dcaf0"][index % 5]);
      target.append(piece);
    }
    window.setTimeout(() => target.replaceChildren(), 1100);
  }

  const progress = readProgress();
  document.querySelectorAll("[data-todo-id]").forEach((todo) => {
    const id = todo.dataset.todoId;
    const action = todo.querySelector("[data-todo-complete]");
    action.addEventListener("click", () => {
      progress[id] = true;
      saveProgress(progress);
      launchConfetti(todo);
    });
    action.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") {
        return;
      }
      event.preventDefault();
      action.click();
    });
  });
})();
</script>
