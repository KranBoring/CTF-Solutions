FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock ./

COPY ./src ./src

RUN yarn install

ENV FLAG hkcert22{***REDACTED***}

CMD ["yarn", "run", "start"]
