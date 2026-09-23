import { Html } from "@elysiajs/html";
import { Layout } from "./layout";

export function Home() {
  return (
    <Layout title="Hachimi">
      <img src="/public/logo.png" alt="Hachimi logo" class="logo" />
      <h1>Hachimi</h1>
      <div class="buttons">
        <a href="/login" class="login">
          Login
        </a>
        <a href="/register" class="register">
          Register
        </a>
      </div>
    </Layout>
  );
}
