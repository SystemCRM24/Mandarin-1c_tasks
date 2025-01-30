# Используем базовый образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Устанавливаем PYTHONPATH, чтобы `src` был виден
ENV PYTHONPATH=/app/src

# Запускаем ASGI-приложение через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
