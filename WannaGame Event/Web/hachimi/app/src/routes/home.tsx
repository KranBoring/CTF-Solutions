import { Elysia } from "elysia";
import { Html } from "@elysiajs/html";
import { Home } from "../ui/home";

export function homeRoute(app: Elysia) {
  return app.get("/", () => <Home />);
}
