# Final Project — Computer Engineering 25/26

ETL pipeline that scrapes data from **Base**, transforms it, and loads it into a MySQL database, exposed via a REST API to a frontend.

## Architecture

```
Base → ETL (Python) → MySQL ← API (Laravel) ← Frontend (Vue 3)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Scraping / ETL | Python |
| Database | MySQL |
| Backend API | Laravel |
| Frontend | Vue 3 |
| Scheduler | [Ofelia](https://hub.docker.com/r/mcuadros/ofelia) |
| Deployment | Docker |

> Ofelia runs the ETL script every day at **00:10 AM**.

## Prerequisites

- **Docker** — [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Python 3.8+** *(only for local installation)*
- A MySQL client like [MySQL Workbench](https://www.mysql.com/products/workbench/) *(optional)*
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

## Configuration

1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```
2. Generate a Cerebras API key at [cerebras.ai](https://www.cerebras.ai/)
3. Fill in your values in `.env`