import { Html } from "@elysiajs/html";
import { Layout } from "./layout";
import { Form } from "./form";

export function LoginPage({ error }: { error?: string }) {
  return (
    <Layout title="Login">
      <Form action="/login" button="Login" error={error} />
    </Layout>
  );
}
