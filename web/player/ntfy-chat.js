<script>
(() => {
  const storageKey = "sae-c.ntfy.group";
  const groups = {
    S3A: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3A-SAE-C/sse",
    S3B: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3B-SAE-C/sse",
    S3C: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3C-SAE-C/sse",
  };
  let currentSource = null;

  function escape(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function encodeData(value) {
    const json = JSON.stringify(value);
    const bytes = new TextEncoder().encode(json);
    let binary = "";
    for (const byte of bytes) {
      binary += String.fromCharCode(byte);
    }
    return btoa(binary);
  }

  function linkify(message) {
    const parts = String(message).split(/(https?:\/\/[^\s<>"']+)/g);
    return parts
      .map((part) => {
        if (/^https?:\/\//.test(part)) {
          const href = escape(part);
          return `<a href="${href}" target="_blank" rel="noopener noreferrer">${href}</a>`;
        }
        return escape(part).replaceAll("\n", "<br>");
      })
      .join("");
  }

  function storedGroup() {
    try {
      const value = window.localStorage.getItem(storageKey);
      return value === "S3A" || value === "S3B" || value === "S3C" || value === "visiteur" ? value : "";
    } catch (_error) {
      return "";
    }
  }

  function storeGroup(group) {
    try {
      window.localStorage.setItem(storageKey, group);
    } catch (_error) {
      // The widget can still work for the current page without persistence.
    }
  }

  function siteBasePath() {
    const brand = document.querySelector(".navbar-brand");
    const baseUrl = brand ? new URL(brand.getAttribute("href") || ".", window.location.href) : new URL(".", window.location.href);
    return baseUrl.pathname.replace(/[^/]*$/, "");
  }

  function localSiteUrl(message) {
    const trimmed = String(message || "").trim();
    if (!/^https?:\/\/\S+$/.test(trimmed)) {
      return null;
    }
    try {
      const url = new URL(trimmed);
      if (url.origin !== window.location.origin) {
        return null;
      }
      if (!url.pathname.startsWith(siteBasePath())) {
        return null;
      }
      return url;
    } catch (_error) {
      return null;
    }
  }

  function cPayload(source) {
    return encodeData({
      id: `ntfy-${Date.now()}`,
      title: "Message C",
      statement: "",
      sources: ["main.c"],
      main: "main.c",
      stdin: "",
      expected_stdout: "",
      expected_stderr: "",
      path: "",
      files: [{ name: "main.c", content: source }],
      browser_runnable: true,
    });
  }

  function createWidget() {
    const root = document.createElement("section");
    root.className = "ntfy-chat ntfy-chat--collapsed";
    root.innerHTML = `
      <div class="ntfy-chat__header">
        <button class="ntfy-chat__toggle" type="button" aria-expanded="false">
          <span>Chat SAE-C</span>
          <span class="ntfy-chat__status" data-status>Configuration...</span>
        </button>
        <button class="ntfy-chat__settings" type="button" aria-label="Configurer le groupe ntfy" title="Configurer le groupe">Groupe</button>
      </div>
      <div class="ntfy-chat__panel">
        <div class="ntfy-chat__messages" data-messages></div>
      </div>
      <div class="ntfy-chat__modal" data-modal hidden>
        <div class="ntfy-chat__modal-dialog" role="dialog" aria-modal="true" aria-labelledby="ntfy-chat-group-title">
          <h2 id="ntfy-chat-group-title">Groupe ntfy</h2>
          <label for="ntfy-chat-group">Groupe de l'etudiant</label>
          <select id="ntfy-chat-group" data-group-select>
            <option value="S3A">S3A</option>
            <option value="S3B">S3B</option>
            <option value="S3C">S3C</option>
            <option value="visiteur">visiteur</option>
          </select>
          <div class="ntfy-chat__modal-actions">
            <button class="btn btn-secondary" type="button" data-close-config>Annuler</button>
            <button class="btn btn-primary" type="button" data-save-config>Enregistrer</button>
          </div>
        </div>
      </div>
    `;
    document.body.append(root);
    root.querySelector(".ntfy-chat__toggle").addEventListener("click", () => {
      const collapsed = root.classList.toggle("ntfy-chat--collapsed");
      root.querySelector(".ntfy-chat__toggle").setAttribute("aria-expanded", collapsed ? "false" : "true");
    });
    root.querySelector(".ntfy-chat__settings").addEventListener("click", () => openConfig(root));
    root.querySelector("[data-close-config]").addEventListener("click", () => {
      const group = storedGroup();
      closeConfig(root);
      if (!group) {
        storeGroup("visiteur");
        connect(root, "visiteur");
      }
    });
    root.querySelector("[data-save-config]").addEventListener("click", () => {
      const group = root.querySelector("[data-group-select]").value;
      storeGroup(group);
      closeConfig(root);
      connect(root, group);
    });
    return root;
  }

  function appendText(root, message) {
    const entry = document.createElement("article");
    entry.className = "ntfy-chat__message";
    entry.innerHTML = linkify(message);
    appendEntry(root, entry);
  }

  function appendCode(root, source) {
    const entry = document.createElement("article");
    entry.className = "ntfy-chat__message ntfy-chat__message--code";
    const player = document.createElement("c-player");
    player.dataset.readonly = "false";
    player.dataset.exerciseB64 = cPayload(source);
    entry.append(player);
    appendEntry(root, entry);
  }

  function appendEntry(root, entry) {
    const messages = root.querySelector("[data-messages]");
    messages.append(entry);
    while (messages.children.length > 50) {
      messages.firstElementChild.remove();
    }
    messages.scrollTop = messages.scrollHeight;
  }

  function handleMessage(root, rawMessage) {
    const normalized = String(rawMessage || "").replaceAll("\r", "");
    const target = localSiteUrl(normalized);
    if (target) {
      window.location.assign(target.href);
      return;
    }
    const lines = normalized.split("\n");
    if (lines[0] === "c") {
      appendCode(root, lines.slice(1).join("\n"));
      return;
    }
    appendText(root, normalized);
  }

  function setStatus(root, value) {
    root.querySelector("[data-status]").textContent = value;
  }

  function openConfig(root) {
    const group = storedGroup() || "visiteur";
    root.querySelector("[data-group-select]").value = group;
    root.querySelector("[data-modal]").hidden = false;
  }

  function closeConfig(root) {
    root.querySelector("[data-modal]").hidden = true;
  }

  function disconnect() {
    if (currentSource) {
      currentSource.close();
      currentSource = null;
    }
  }

  function connect(root, group) {
    disconnect();
    if (group === "visiteur") {
      setStatus(root, "Visiteur");
      return;
    }
    if (!window.EventSource) {
      setStatus(root, "SSE indisponible");
      return;
    }
    const topicUrl = groups[group];
    if (!topicUrl) {
      setStatus(root, "Groupe requis");
      openConfig(root);
      return;
    }
    currentSource = new EventSource(topicUrl);
    currentSource.onopen = () => setStatus(root, `${group} connecte`);
    currentSource.onerror = () => setStatus(root, `${group} reconnexion...`);
    currentSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.event === "message") {
          handleMessage(root, payload.message);
        }
      } catch (_error) {
        handleMessage(root, event.data);
      }
    };
  }

  const root = createWidget();
  const group = storedGroup();
  if (group) {
    connect(root, group);
  } else {
    setStatus(root, "Groupe requis");
    openConfig(root);
  }
})();
</script>
