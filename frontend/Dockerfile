#build stage
FROM node:lts-alpine AS build
WORKDIR /app
COPY package*.json ./

RUN npm install
RUN npm install vue-sonner

# Declare each ARG so Vite can see them
ARG VITE_BASE_URL
ARG VITE_REVERB_HOST
ARG VITE_REVERB_PORT
ARG VITE_REVERB_SCHEME
ARG VITE_REVERB_APP_KEY


# Make them available as env vars during build
ENV VITE_BASE_URL=$VITE_BASE_URL
ENV VITE_REVERB_HOST=$VITE_REVERB_HOST
ENV VITE_REVERB_PORT=$VITE_REVERB_PORT
ENV VITE_REVERB_SCHEME=$VITE_REVERB_SCHEME
ENV VITE_REVERB_APP_KEY=$VITE_REVERB_APP_KEY

COPY . .
RUN npm run build

#production stage
FROM nginx:stable-alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
