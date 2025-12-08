// static/js/songs.js

(function () {
  const searchInput = document.getElementById("song-search");
  const clearButton = document.getElementById("song-search-clear");
  const tableBody = document.getElementById("songs-table-body");

  if (!searchInput || !tableBody) return;

  // Pequeño debounce para no hacer fetch en cada tecla
  let debounceTimer = null;

  function fetchSongs(query) {
    const url = new URL(window.location.origin + "/songs/api/");
    if (query) {
      url.searchParams.set("q", query);
    }

    // Efecto visual: opacidad baja mientras carga
    tableBody.classList.add("is-loading");

    fetch(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        renderSongs(data.results || []);
      })
      .catch((err) => {
        console.error("Error fetching songs:", err);
      })
      .finally(() => {
        // restaurar opacidad
        setTimeout(() => {
          tableBody.classList.remove("is-loading");
        }, 150);
      });
  }

  function renderSongs(songs) {
    if (!songs.length) {
      tableBody.innerHTML =
        '<tr><td colspan="5" class="table-empty">No hay canciones disponibles.</td></tr>';
      return;
    }

    const rows = songs
      .map((song, index) => {
        const artistsText = song.artists || "";
        return `
          <tr class="song-row">
            <td><span class="rank">#${index + 1}</span></td>
            <td><a href="${song.detail_url}">${song.name}</a></td>
            <td><a href="${song.genre_url}" class="badge">${song.genre}</a></td>
            <td class="muted">${artistsText}</td>
            <td><a class="btn ghost" href="${song.detail_url}">Ver</a></td>
          </tr>
        `;
      })
      .join("");

    tableBody.innerHTML = rows;

    attachRowClickEffects();
  }

  function attachRowClickEffects() {
    const rows = tableBody.querySelectorAll(".song-row");
    rows.forEach((row) => {
      // EFECTO: fila clicable -> navega al detalle
      row.addEventListener("click", (e) => {
        const link = row.querySelector("td:nth-child(2) a");
        if (link) {
          window.location.href = link.href;
        }
      });

      // Evitar que un click directo en un botón/link repita navegación
      row.querySelectorAll("a, button").forEach((el) => {
        el.addEventListener("click", (e) => e.stopPropagation());
      });

      // EFECTO: hover con clase extra (puedes definirla en CSS)
      row.addEventListener("mouseenter", () => {
        row.classList.add("row-hover");
      });
      row.addEventListener("mouseleave", () => {
        row.classList.remove("row-hover");
      });
    });
  }

  // Listener de búsqueda
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim();

    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    debounceTimer = setTimeout(() => {
      fetchSongs(query);
    }, 300);
  });

  // Botón "Limpiar filtro"
  if (clearButton) {
    clearButton.addEventListener("click", () => {
      searchInput.value = "";
      fetchSongs("");
    });
  }

  // Inicial: enganchar efectos a las filas ya renderizadas
  attachRowClickEffects();
})();
