import { Elysia } from "elysia";
import { Html } from "@elysiajs/html";
import { object, string } from "valibot";
import { signToken } from "../utils/key";
import { addUser, findUser, userExists } from "../utils/data";
import { RegisterPage } from "../ui/register";
import { LoginPage } from "../ui/login";

const credentialsSchema = object({
  username: string(),
  password: string(),
});

export function authRoutes(app: Elysia) {
  return app
    .get("/register", () => <RegisterPage />)
    .post(
      "/register",
      ({ body, redirect }) => {
        const { username, password } = body;
        if (userExists(username)) {
          return <RegisterPage error="Username already taken" />;
        }
        addUser(username, password);
        return redirect("/login");
      },
      { body: credentialsSchema },
    )
    .get("/login", () => <LoginPage />)
    .post(
      "/login",
      ({ body, cookie, redirect }) => {
        const { username, password } = body;
        const user = findUser(username);
        if (!user || user.password !== password) {
          return <LoginPage error="Invalid credentials" />;
        }
        const token = signToken({ sub: user.id, username: user.username });
        cookie.auth.set({ value: token, httpOnly: true, path: "/" });
        return redirect("/dashboard");
      },
      { body: credentialsSchema },
    );
}
