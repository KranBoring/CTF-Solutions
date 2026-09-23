import { Elysia } from "elysia";
import { Html } from "@elysiajs/html";
import { union, optional, literal, object, any } from "valibot";
import { verifyToken } from "../utils/key";
import { getCharacters } from "../utils/data";
import { DashboardPage } from "../ui/dashboard";

const sortSchema = object({
  data: object({
    sort: optional(
      union([
        literal("default"),
        literal("name-az"),
        literal("name-za"),
        literal("height-desc"),
        literal("height-asc"),
      ]),
      "default",
    ),
  }),
});

function sortCharacters(
  characters: ReturnType<typeof getCharacters>,
  sort: string,
) {
  const sorted = [...characters];
  switch (sort) {
    case "name-az":
      sorted.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case "name-za":
      sorted.sort((a, b) => b.name.localeCompare(a.name));
      break;
    case "height-desc":
      sorted.sort((a, b) => b.height - a.height);
      break;
    case "height-asc":
      sorted.sort((a, b) => a.height - b.height);
      break;
  }
  return sorted;
}

export function dashboardRoutes(app: Elysia) {
  return app
    .guard({
      schema: "standalone",
      body: object({
        data: any(),
      }),
    })
    .get("/dashboard", ({ cookie, redirect }) => {
      const token = cookie.auth.value;
      if (!token) {
        return redirect("/login");
      }
      try {
        const payload = verifyToken<{ sub: number; username: string }>(
          String(token),
        );
        return (
          <DashboardPage
            name={payload.username}
            characters={getCharacters()}
            sort="default"
          />
        );
      } catch {
        return redirect("/login");
      }
    })
    .post(
      "/dashboard/api/characters",
      ({ body }) => {
        const sort = body.data.sort;
        return sortCharacters(getCharacters(), sort);
      },
      { body: sortSchema },
    )
    .get("/logout", ({ cookie, redirect }) => {
      cookie.auth.remove();
      return redirect("/");
    });
}
