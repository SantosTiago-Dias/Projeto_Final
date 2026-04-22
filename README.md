# Projeto Final - Engenharia Informática 25/26

Final year project for Computer Engineering course (2025/2026).

## Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline with data processing and AI for population of data and integration capabilities.

## Prerequisites

If you want to use `docker` ensure you have `docker desktop`
If you want to ``install`` ensure you have ``Python 3.8+`` installed on your system and some system you can see data like ``workbench``.

## Docker

You can run this project with docker with command ``docker compose up -d --build``

## Installation

Install all required dependencies:

```bash
python -m pip install requests
python -m pip install pandas
python -m pip install alive-progress
python -m pip install python-dotenv
python -m pip install mysql-connector-python
python -m pip install cerebras-cloud-sdk
python -m pip install loguru
python -m pip install openpyxl
```

Or install all at once:

```bash
pip install requests pandas alive-progress python-dotenv mysql-connector-python cerebras-cloud-sdk loguru openpyxl
```

## Configuration

1. Create a `.env` file from `.env.example`
2. Go to cerebras web site `https://www.cerebras.ai/` and generate a key for you AI
3. Change `.env` with you enviroment

## Project Structure

- Database -> Mysql scripts need to init database and procedures
- ETL -> with py scripts for ETL
