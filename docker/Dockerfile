# docker/Dockerfile
FROM python:3.11-slim

LABEL maintainer="OmAum Development Team"
LABEL version="2.0"
LABEL description="OM-AUM Django Application"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=omaum.settings.production

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    gettext \
    postgresql-client \
    netcat-openbsd \
    libpango-1.0-0 \
    libcairo2 \
    libgobject-2.0-0 \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r omaum && useradd -r -g omaum omaum

WORKDIR /app
RUN mkdir -p /app/static /app/media /app/logs
RUN chown -R omaum:omaum /app

COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/development.txt

COPY . /app/
RUN chown -R omaum:omaum /app

COPY docker/scripts/entrypoint.sh /entrypoint.sh
COPY docker/scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /entrypoint.sh /wait-for-it.sh

USER omaum

RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "omaum.wsgi:application"]
