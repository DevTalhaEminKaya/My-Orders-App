FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Gereksinimler kuruluyor
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["python", "app.py"]
