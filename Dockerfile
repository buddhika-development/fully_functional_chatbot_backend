FROM ubuntu:latest
LABEL authors="buddhika-madusanka"

# Use the official Python 3.13 slim image
FROM python:3.13-slim-bookworm

# Copy the uv binary from the official astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache

# Copy the rest of your application code
COPY . .

# Expose the port
EXPOSE 8000

# Start the application
CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]