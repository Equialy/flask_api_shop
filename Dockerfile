FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh
RUN mkdir -p logs

#ENV PYTHONPATH=/app
#ENV FLASK_APP=src.presentation.main

#EXPOSE 5555
ENTRYPOINT ["./entrypoint.sh"]
#CMD ["python", "-m", "src.presentation.main"]