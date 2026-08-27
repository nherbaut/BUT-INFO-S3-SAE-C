<script>
(() => {
  "use strict";

  function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
      modal.hidden = false;
      modal.querySelector("[data-local-modal-close]")?.focus();
    }
  }

  document.addEventListener("click", (event) => {
    const openButton = event.target.closest("[data-local-modal-open]");
    if (openButton) {
      event.preventDefault();
      event.stopPropagation();
      openModal(openButton.dataset.localModalOpen);
      return;
    }

    const closeButton = event.target.closest("[data-local-modal-close]");
    if (closeButton) {
      closeButton.closest("[data-local-modal]").hidden = true;
      return;
    }

    if (event.target.matches("[data-local-modal]")) {
      event.target.hidden = true;
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      document.querySelector("[data-local-modal]:not([hidden])")?.setAttribute("hidden", "");
    }
  });
})();
</script>
