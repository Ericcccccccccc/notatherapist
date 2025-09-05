FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python modules
COPY app.py .
COPY input_processor.py .
COPY llm_gateway.py .
COPY response_processor.py .

EXPOSE 5004

# Use uvicorn for FastAPI with auto-reload disabled in production
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5004", "--workers", "1", "--loop", "asyncio", "--timeout-keep-alive", "120"]