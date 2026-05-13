FROM node:alpine as base

#Install some dependencies

WORKDIR /usr/app
COPY ./ /usr/app
RUN npm install

FROM base AS builder

EXPOSE 3000

CMD ["node","server.js"]