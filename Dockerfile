# Builder
FROM python:3.12 AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .

# Test
FROM builder AS test
ENV PYTHONPATH=/app
RUN pytest tests/test_app.py

# Final
FROM python:3.12-slim AS final
WORKDIR /app
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app/src ./src
EXPOSE 5000
CMD ["python", "src/app.py"]