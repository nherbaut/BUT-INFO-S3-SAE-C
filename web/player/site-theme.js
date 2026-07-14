<script>
(() => {
  const storageKey = "sae-c.theme.v1";

  function currentTheme() {
    return localStorage.getItem(storageKey) || "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme);
    localStorage.setItem(storageKey, theme);
    for (const button of document.querySelectorAll("[data-theme-toggle]")) {
      button.textContent = theme === "dark" ? "Mode clair" : "Mode sombre";
      button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    }
  }

  applyTheme(currentTheme());

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-theme-toggle]");
    if (!button) {
      return;
    }
    const nextTheme = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
  });
})();
</script>
