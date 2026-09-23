document.getElementById("sort-select").addEventListener("change", async (e) => {
  const grid = document.getElementById("char-grid");
  grid.innerHTML = '<p style="color:#888">Loading...</p>';
  const res = await fetch("/dashboard/api/characters", {
    method: "POST",
    headers: { 
      "Content-Type": "application/json" 
    },
    body: JSON.stringify({ 
      data: { 
        sort: e.target.value 
      } 
    }),
  });
  const chars = await res.json();
  grid.innerHTML = chars.map((c) =>`<div class="char-card"><img src="${c.image}" alt="${c.name}" class="avatar" /><p class="char-name">${c.name}</p><p class="char-height">${c.height} cm</p></div>`,).join("");
});