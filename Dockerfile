FROM python:3.12-slim-bullseye



# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Expose port
EXPOSE 8000

# Start FastAPI app with Uvicorn (from src/main.py)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
