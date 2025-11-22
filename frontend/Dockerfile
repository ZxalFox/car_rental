FROM node:20-alpine

WORKDIR /app

ENV PATH=/app/node_modules/.bin:$PATH \
    GATSBY_TELEMETRY_DISABLED=1

COPY package.json package-lock.json ./

RUN npm ci --loglevel warn

COPY . .

EXPOSE 8001

CMD ["npm", "run", "develop"]
