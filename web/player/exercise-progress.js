<script>
(() => {
  "use strict";

  const storageKey = "sae-c.exercise.progress.v1";
  const t = (key, values) => window.SAECMessages.t(`exerciseProgress.${key}`, values);

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

  function updateCount(list) {
    const inputs = Array.from(list.querySelectorAll("[data-exercise-progress]"));
    const completed = inputs.filter((input) => input.checked).length;
    const count = list.querySelector("[data-exercise-progress-count]");
    if (count) {
      count.textContent = t("count", {
        completed,
        total: inputs.length,
        plural: inputs.length > 1 ? t("plural") : "",
      });
    }
  }

  const progress = readProgress();
  document.querySelectorAll("[data-exercise-progress-list]").forEach((list) => {
    list.querySelectorAll("[data-exercise-progress]").forEach((input) => {
      const key = input.dataset.exerciseProgress;
      input.checked = progress[key] === true;
      input.addEventListener("change", () => {
        progress[key] = input.checked;
        saveProgress(progress);
        updateCount(list);
      });
    });
    updateCount(list);
  });
})();
</script>
