import { Elysia } from "elysia";
import { Html } from "@elysiajs/html";
import { verifyToken } from "../utils/key";
import { AdminPage, ForbiddenPage } from "../ui/admin";

export function adminRoutes(app: Elysia) {
  return app.get("/admin", async ({ cookie, redirect }) => {
    const token = cookie.auth.value;
    if (!token) {
      return redirect("/login");
    }
    try {
      const payload = verifyToken<{ sub: number; username: string }>(
        String(token),
      );
      if (payload.username === "admin") {
        return await (<AdminPage name={payload.username} />);
      }
      return <ForbiddenPage />;
    } catch (error) {
      console.log(error);
      return redirect("/login");
    }
  });
}
