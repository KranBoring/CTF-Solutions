import { Html } from "@elysiajs/html";

export function Layout({ title, children }: { title: string; children: any }) {
  return (
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title}</title>
        <link rel="stylesheet" href="/public/style.css" />
      </head>
      <body>{children}</body>
    </html>
  );
}
