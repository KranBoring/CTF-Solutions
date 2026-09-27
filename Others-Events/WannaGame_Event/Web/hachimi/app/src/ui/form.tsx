import { Html } from "@elysiajs/html";

export function Form({
  action,
  button,
  error,
}: {
  action: string;
  button: string;
  error?: string;
}) {
  return (
    <div class="form-wrap">
      <h1>{button}</h1>
      {error && <p class="error">{error}</p>}
      <form method="POST" action={action}>
        <label>
          Username
          <input type="text" name="username" required />
        </label>
        <label>
          Password
          <input type="password" name="password" required />
        </label>
        <button type="submit">{button}</button>
      </form>
    </div>
  );
}
