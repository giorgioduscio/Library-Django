echo "[1/3] Costruzione del container (http://localhost:8000)"
docker compose up -d

echo "[2/3] Accesso alla console"
docker compose exec django-demo bash

echo "[3/3] Fermare il container"
docker compose stop
echo ""