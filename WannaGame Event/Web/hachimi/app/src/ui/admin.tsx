import { Html } from "@elysiajs/html";
import { Layout } from "./layout";

export async function AdminPage({ name }: { name: string }) {
  const flagFile = Bun.file("/flag.txt");
  const flag = (await flagFile.exists())
    ? await flagFile.text()
    : "no flag";

  return (
    <Layout title="Admin">
      <div class="form-wrap">
        <h1>Congrats</h1>
        <p>You are {name}.</p>
        <p>{flag}</p>
        <a href="/logout" class="logout">
          Logout
        </a>
      </div>
    </Layout>
  );
}

export function ForbiddenPage() {
  return (
    <Layout title="Forbidden">
      <div class="form-wrap">
        <h1>403</h1>
        <p>You are not authorized to view this</p>
        <a href="/dashboard" class="logout">
          Back to Dashboard
        </a>
      </div>
    </Layout>
  );
}
