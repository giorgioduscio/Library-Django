#!/bin/bash
echo "[1/3] Costruzione del container"
# python manage.py runserver 0.0.0.0:8000
docker compose up -d 
docker compose exec django-demo  python manage.py makemigrations 
docker compose exec django-demo  python manage.py migrate

echo "[2/3] Accesso al terminale (http://localhost:8000)"
docker compose exec django-demo bash

echo "[3/3] Fermare il container"
docker compose stop
echo 