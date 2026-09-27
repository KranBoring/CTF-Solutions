import { Html } from "@elysiajs/html";
import { Layout } from "./layout";
import { Form } from "./form";

export function RegisterPage({ error }: { error?: string }) {
  return (
    <Layout title="Register">
      <Form action="/register" button="Register" error={error} />
    </Layout>
  );
}
