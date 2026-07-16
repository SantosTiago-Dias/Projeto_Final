# Final Project — Computer Engineering 25/26

ETL pipeline that scrapes data from **Base**, transforms it, and loads it into a MySQL database, exposed via a REST API to a frontend.

## Architecture

```
Base → ETL (Python) → MySQL ← API (Laravel) ← Frontend (Vue 3)
```

## Tech Stack

| Layer          | Technology                                                               |
|----------------|--------------------------------------------------------------------------|
| Scraping / ETL | Python                                                                   |
| Database       | MySQL                                                                    |
| Backend API    | Laravel                                                                  |
| Frontend       | Vue 3                                                                    |
| Scheduler      | [Ofelia](https://hub.docker.com/r/mcuadros/ofelia)                       |
| Deployment     | Docker                                                                   |
| Cache          | Redis                                                                    |
| WS             | socket.io                                                                |
| Proxy manager  | [nginx-proxy-manager](https://hub.docker.com/r/jc21/nginx-proxy-manager) |

> Ofelia runs the ETL script every day at **00:10 AM**.

## Prerequisites

- **Docker** — [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Python 3.8+** *(only for local installation)*
- A MySQL client like [MySQL Workbench](https://www.mysql.com/products/workbench/) *(optional and need to expose port)*
## Getting Started

### Docker (recommended)

```bash
docker compose up -d --build
```

### Local Installation

Install dependencies individually:

```bash
pip install requests pandas alive-progress python-dotenv mysql-connector-python cerebras-cloud-sdk loguru openpyxl
```
>After need to create databse and run every script

## Configuration

1. Go to `init.sql` and change ETL for the name of your DB
2. Copy the example env file:
   ```bash
   cp .env.example .env
   ```

3. Generate a Gord API key at [gorq](https://groq.com/)
4. Fill `.env` with your values
5. Run ```docker compose up -d --build```
6. Go to `localhost:81` to change values in proxy manager