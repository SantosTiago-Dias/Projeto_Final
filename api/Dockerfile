FROM dunglas/frankenphp:1.10.1-php8.4 AS base

RUN apt-get update && apt-get install -y \
    git unzip libzip-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN install-php-extensions pdo_mysql gd intl zip opcache

RUN pecl install redis && docker-php-ext-enable redis
RUN docker-php-ext-install pcntl


# Build stage
FROM base AS builder

WORKDIR /app

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

COPY . .

RUN composer install --no-interaction --prefer-dist --optimize-autoloader

# Production stage
FROM base AS production

WORKDIR /app

ARG USER=appuser

COPY --from=builder /app ./

RUN \
    useradd ${USER}; \
    setcap CAP_NET_BIND_SERVICE=+eip /usr/local/bin/frankenphp; \
    chown -R ${USER}:${USER} /config/caddy /data/caddy; \
    chown -R ${USER}:${USER} /app/storage /app/bootstrap/cache; \
    chmod -R 775 /app/storage /app/bootstrap/cache

USER ${USER}

CMD ["frankenphp", "run", "--config", "/etc/caddy/Caddyfile"]
