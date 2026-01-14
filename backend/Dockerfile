FROM python:3.11-slim

WORKDIR /app

# Install system deps (optional but safe)
RUN pip install --no-cache-dir --upgrade pip

# Copy project files
# COPY pyproject.toml /app/pyproject.toml
# COPY README.md /app/README.md
COPY src /app/src
COPY migrations /app/migrations
COPY alembic.ini /app/alembic.ini

# Install dependencies (we’ll keep it simple for now using pip)
# If you're using pyproject/poetry later, we’ll upgrade this.
RUN pip install --no-cache-dir \
    fastapi uvicorn sqlalchemy psycopg[binary] alembic python-dotenv pgvector \
    langchain openai langgraph requests python-multipart

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
