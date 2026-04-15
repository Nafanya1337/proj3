FROM python:3.9-alpine AS builder

WORKDIR /install
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

FROM python:3.9-alpine

WORKDIR /app
COPY --from=builder /install/deps /usr/local
COPY app.py .
COPY templates ./templates
COPY static ./static

EXPOSE 8080

CMD ["python", "app.py"]
