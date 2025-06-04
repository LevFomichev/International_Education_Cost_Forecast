FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY model_service/ ./model_service/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]