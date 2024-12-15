# syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV TELEGRAM_TOKEN=
ENV OLLAMA_API_URL=http://host.docker.internal:11434/api/chat
ENV OLLAMA_API_MODEL=llama3.1:latest
CMD python main.py