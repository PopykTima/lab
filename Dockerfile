FROM python:3.12-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Обов'язково копіюємо всі інші файли проекту в Докер
COPY . .

# Точка входу
CMD ["python", "run.py"]