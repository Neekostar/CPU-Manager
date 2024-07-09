FROM node:18 as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM node:18 as production-stage

WORKDIR /app

RUN npm install -g serve

COPY --from=build-stage /app/dist /app

EXPOSE 5173

CMD ["serve", "-s", ".", "-l", "5173"]