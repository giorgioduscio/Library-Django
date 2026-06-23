# DOCKER: Usa un'immagine Python ufficiale come base
FROM python:3.12-slim

# SICUREZZA: Impedisce a Python di scrivere file .pyc e di bufferizzare l'output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# SICUREZZA: Crea utente non-root per sicurezza
RUN groupadd -r django && useradd -r -g django django

# DOCKER: Imposta la directory di lavoro nel contenitore
WORKDIR /app

# DOCKER: Installa le dipendenze di sistema necessarie
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installa le dipendenze Python
# SICUREZZA: usa --user per installare in home directory dell'utente non-root
COPY requirements.txt /app/
RUN pip install --no-cache-dir --user -r requirements.txt

# Copia il resto del codice del progetto
# SICUREZZA: copia con proprietario django:django
COPY --chown=django:django . /app/

# SICUREZZA: cambia utente a non-root
USER django
ENV PATH=/home/django/.local/bin:$PATH

# DOCKER: Espone la porta su cui gira Django
EXPOSE 8000

# DOCKER: Comando di default per avviare il server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
