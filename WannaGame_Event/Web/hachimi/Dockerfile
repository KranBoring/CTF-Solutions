FROM oven/bun AS build

WORKDIR /app

COPY ./app/package.json ./package.json
COPY ./app/bun.lock ./bun.lock

RUN bun install

COPY ./app .

ENV NODE_ENV=production

RUN bun build \
	--compile \
	--minify-whitespace \
	--minify-syntax \
	--outfile server \
	src/index.ts

FROM gcr.io/distroless/base

WORKDIR /app

COPY --from=build /app/server server
COPY --from=build /app/public public

COPY secrets /secrets
COPY flag.txt /

ENV NODE_ENV=production

CMD ["./server"]

EXPOSE 3000
