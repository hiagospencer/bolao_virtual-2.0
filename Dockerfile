FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Adicione esta linha para coletar static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# CMD ["gunicorn", "bolao_virtual.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
