import { Elysia } from "elysia";
import { html } from "@elysiajs/html";
import { staticPlugin } from "@elysiajs/static";
import { homeRoute } from "./routes/home";
import { authRoutes } from "./routes/auth";
import { dashboardRoutes } from "./routes/dashboard";
import { adminRoutes } from "./routes/admin";

const app = new Elysia()
  .use(html())
  .use(staticPlugin({ prefix: "/public", assets: "public" }))
  .use(homeRoute)
  .use(authRoutes)
  .use(dashboardRoutes)
  .use(adminRoutes)
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`,
);
