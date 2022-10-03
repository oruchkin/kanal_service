FROM python:3.9

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE 'kanal.settings'

COPY requirements.txt requirements.txt

RUN  python -m pip install --upgrade pip \
    && pip install psycopg2-binary \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "kanal.wsgi:application", "--bind", "0:8000"]