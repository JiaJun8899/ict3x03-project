FROM node:20.5.1-alpine

WORKDIR /app/frontend

COPY ./frontend .

RUN npm install

RUN npx next build

EXPOSE 3000

CMD [ "npx", "next", "start" ]

