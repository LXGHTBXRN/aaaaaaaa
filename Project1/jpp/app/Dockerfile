FROM python:3.9-slim

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn sqlalchemy databases asyncpg jinja2

COPY ./app /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
