# Dockerfile (na raiz do projeto)
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["celery", "-A", "bolao_virtual", "worker", "--loglevel=info"]
