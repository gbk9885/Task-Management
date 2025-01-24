FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN touch /app/.env
RUN apt-get update && apt-get install -y libpq-dev gcc && \
    pip install psycopg2-binary
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]

