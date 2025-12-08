document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("global-search-form");
  const input = document.getElementById("global-search-input");
  const resultsBox = document.getElementById("global-search-results");

  if (!form || !input || !resultsBox) return;

  const searchUrl = form.dataset.searchUrl;
  let debounceId = null;

  function clearResults() {
    resultsBox.innerHTML = "";
    resultsBox.classList.remove("is-open");
  }

  function renderSection(title, items) {
    if (!items || !items.length) return "";
    const lis = items
      .map(
        (item) => `
      <li class="search-result-item">
        <a href="${item.url}">
          <span class="search-result-name">${item.name}</span>
          ${
            item.subtitle
              ? `<span class="search-result-sub">${item.subtitle}</span>`
              : ""
          }
        </a>
      </li>`
      )
      .join("");

    return `
      <div class="search-result-section">
        <div class="search-result-title">${title}</div>
        <ul class="search-result-list">
          ${lis}
        </ul>
      </div>
    `;
  }

  function renderResults(data) {
    const html =
      renderSection("Songs", data.songs) +
      renderSection("Artists", data.artists) +
      renderSection("Genres", data.genres) +
      renderSection("Albums", data.albums);

    if (!html) {
      resultsBox.innerHTML =
        '<div class="search-result-empty">No results found</div>';
    } else {
      resultsBox.innerHTML = html;
    }
    resultsBox.classList.add("is-open");
  }

  async function performSearch(query) {
    const q = query.trim();
    if (!q) {
      clearResults();
      return;
    }

    try {
      const resp = await fetch(
        `${searchUrl}?q=${encodeURIComponent(q)}`,
        { headers: { "X-Requested-With": "XMLHttpRequest" } }
      );
      if (!resp.ok) {
        clearResults();
        return;
      }
      const data = await resp.json();
      renderResults(data);
    } catch (err) {
      console.error("Global search error:", err);
      clearResults();
    }
  }

  // Búsqueda con debounce
  input.addEventListener("input", () => {
    clearTimeout(debounceId);
    debounceId = setTimeout(() => performSearch(input.value), 300);
  });

  // Enter en el buscador
  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    performSearch(input.value);
  });

  // Cerrar resultados al hacer click fuera
  document.addEventListener("click", (ev) => {
    if (
      !resultsBox.contains(ev.target) &&
      ev.target !== input &&
      !input.contains(ev.target)
    ) {
      clearResults();
    }
  });
});