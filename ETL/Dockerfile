FROM python:3.14-slim as base
 

RUN pip install --no-cache-dir requests pandas alive-progress cerebras-cloud-sdk loguru openpyxl python-dotenv mysql-connector-python redis

FROM base  as builder

WORKDIR /app

COPY . .

CMD [ "python","main.py" ]