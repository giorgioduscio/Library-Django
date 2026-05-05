# Usa un'immagine Python ufficiale come base
FROM python:3.12-slim

# Impedisce a Python di scrivere file .pyc e di bufferizzare l'output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Imposta la directory di lavoro nel contenitore
WORKDIR /app

# Installa le dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installa le dipendenze Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice del progetto
COPY . /app/

# Espone la porta su cui gira Django
EXPOSE 8000

# Comando di default per avviare il server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
