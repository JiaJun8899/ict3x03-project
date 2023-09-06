FROM node:20.5.1-alpine

WORKDIR /app/frontend

COPY ./frontend .

RUN npm install

RUN npm run build

EXPOSE 3000

CMD [ "npm", "start" ]