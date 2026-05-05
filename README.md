# Django Demo Project

Questo è un progetto Django configurato con una struttura pulita e moderna, pronto per lo sviluppo locale e con supporto Docker.

## Struttura del Progetto

- `config/`: Contiene le impostazioni del progetto, gli URL principali e le configurazioni WSGI/ASGI.
- `manage.py`: L'utility da riga di comando per gestire il progetto.
- `Dockerfile` & `docker-compose.yml`: Configurazioni per l'ambiente containerizzato.
- `requirements.txt`: Elenco delle dipendenze Python.

## Comandi Principali

Di seguito sono elencati i comandi fondamentali per la gestione del server e del progetto.

### Gestione del Server (Locale)

Per eseguire questi comandi, assicurati di aver attivato il tuo ambiente virtuale (`venv`).

- **Avviare il server di sviluppo**:
  ```bash
  python manage.py runserver
  ```
- **Creare nuove migrazioni** (dopo aver modificato i modelli):
  ```bash
  python manage.py makemigrations
  ```
- **Applicare le migrazioni** (per aggiornare il database):
  ```bash
  python manage.py migrate
  ```
- **Creare un utente amministratore** (per l'area `/admin`):
  ```bash
  python manage.py createsuperuser
  ```
- **Creare una nuova app**:
  ```bash
  python manage.py startapp nome_app
  ```

### Gestione con Docker

Se preferisci usare Docker, usa questi comandi:

- **Costruire e avviare i container**:
  ```bash
  docker-compose up --build
  ```
- **Fermare i container**:
  ```bash
  docker-compose down
  ```
- **Eseguire comandi Django dentro il container**:
  ```bash
  docker-compose exec web python manage.py migrate
  ```

## Note sulla Sicurezza

- La `SECRET_KEY` attuale è visibile in `config/settings.py`. Per la messa in produzione, assicurati di spostarla in un file `.env`.
- Il database `db.sqlite3` è escluso dal controllo versione tramite `.gitignore`.

# Workflow

Per creare una nuova pagina, bisogna: 

1) Nel terminale del container, scrivi `python manage.py startapp new_function`
2) Vai in config/settings.py, aggiungi 'new_function' in INSTALLED_APPS 
3) Apri new_function/models.py e definisci il modello di dati
4) Crea la Tabella nel Database e scrivi `python manage.py makemigrations` e `python manage.py migrate`
5) Visualizza i dati nell'Area Admin new_function/admin.py
6) Crea il backend in new_function/views.py
7) Crea template in new_function/templates/new_function.html
8) apri config/urls.py e aggiungi `path('spesa/', lista_spesa, name='lista_spesa')` a urlpatterns