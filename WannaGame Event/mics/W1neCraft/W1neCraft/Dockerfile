FROM eclipse-temurin:8-jre-jammy

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/challenge

COPY bot/package.json bot/package-lock.json /opt/challenge/bot/
RUN cd /opt/challenge/bot && npm ci --omit=dev

COPY bot/w1-player.js /opt/challenge/bot/w1-player.js
COPY bot/login-proxy.js /opt/challenge/bot/login-proxy.js
COPY server-template /opt/challenge/server-template
COPY entrypoint.sh /opt/challenge/entrypoint.sh

RUN chmod +x /opt/challenge/entrypoint.sh

EXPOSE 1337

ENTRYPOINT ["/opt/challenge/entrypoint.sh"]
