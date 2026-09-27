import { Html } from "@elysiajs/html";
import { Layout } from "./layout";
import type { Character } from "../utils/data";

const SORT_OPTIONS = [
  { value: "default", label: "Default" },
  { value: "name-az", label: "Name (A–Z)" },
  { value: "name-za", label: "Name (Z–A)" },
  { value: "height-desc", label: "Height (High → Low)" },
  { value: "height-asc", label: "Height (Low → High)" },
];

export function DashboardPage({
  name,
  characters,
  sort,
}: {
  name: string;
  characters: Character[];
  sort: string;
}) {
  return (
    <Layout title="Dashboard">
      <header class="topbar">
        <span class="username">Welcome, {name}</span>
        <a href="/logout" class="logout">
          Logout
        </a>
      </header>
      <div class="form-wrap dashboard">
        <h1>Characters</h1>
        <div class="sort-form">
          <label>
            Sort by
            <select name="sort" id="sort-select">
              {SORT_OPTIONS.map((o) => (
                <option
                  value={o.value}
                  selected={sort === o.value ? true : undefined}
                >
                  {o.label}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div class="char-grid" id="char-grid">
          {characters.map((c) => (
            <div class="char-card">
              <img src={c.image} alt={c.name} class="avatar" />
              <p class="char-name">{c.name}</p>
              <p class="char-height">{c.height} cm</p>
            </div>
          ))}
        </div>
      </div>
      <script src="/public/dashboard.js"></script>
    </Layout>
  );
}
