# Use official Python image as base
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Expose port
EXPOSE 8000

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build the Docker image
# docker build -t fastapi-tutorial .
