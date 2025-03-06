FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["bash", "-c"]
CMD ["python manage.py collectstatic --noinput && \
      python manage.py migrate && \
      python manage.py generate_sales_data && \
      python manage.py create_superuser && \
      gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]