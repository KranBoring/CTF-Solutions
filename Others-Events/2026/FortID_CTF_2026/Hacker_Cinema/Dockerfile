FROM php:8.4.16-cli-bookworm

WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libgmp-dev libpng-dev libjpeg62-turbo-dev libfreetype6-dev \
       fonts-dejavu-core qrencode zbar-tools \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gmp gd \
    && rm -rf /var/lib/apt/lists/*

COPY public /app/public
COPY src /app/src
COPY flag.txt /app/flag.txt

ENV HOST=0.0.0.0
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "php -S ${HOST}:${PORT} -t public public/index.php"]
