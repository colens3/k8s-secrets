FROM python:3.8-alpine

WORKDIR /app
COPY . .

CMD ["python3", "-u", "main.py"]