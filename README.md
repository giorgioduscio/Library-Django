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

# Workflow creare pagina (Esempio: Spesa)

**Sintesi**

1) *Crea*:    `python manage.py startapp spesa`
2) *Registra* `INSTALLED_APPS = [..., 'spesa']`
3) *Modello*  `class ModelloCustom(models.Model):`
4) *Sync*     `python manage.py makemigrations` -> `python manage.py migrate`
5) *Admin*    admin.site.register(ModelloCustom)
6) *Logica*   `def lista_spesa_view(request):`
7) *Template* `proj/templates/proj/file.html`: <html></html> 
8) *url*      urlpatterns = [... path('spesa/', nome_view, name='nome_view') ]  

**Dettagli**

1. **Crea App**: Nel terminale (del container) 
    * `python manage.py startapp spesa`
2. **Registra**: In `config/settings.py` -> `INSTALLED_APPS = [..., 'spesa']`
3. **Modella**: In `spesa/models.py`:
    ```python
    from django.db import models
    class ElementoLista(models.Model):
        title = models.CharField(max_length=200)
        complete = models.BooleanField(default=False)
    ```
4. **Database**: Scrivere nel terminale (del container)
    * `python manage.py makemigrations` 
    * `python manage.py migrate`
5. **Admin**: In `spesa/admin.py`: 
    ```python
    from django.contrib import admin
    from .models import ElementoLista

    admin.site.register(ElementoLista)
    ```
6. **Logica**: In `spesa/views.py`:
    ```python
    from django.shortcuts import render
    from .models import ElementoLista
    def lista_spesa_view(request):
        elementi = ElementoLista.objects.all()
        return render(request, 'spesa/lista.html', {'lista': elementi})
    ```
7. **Template**: In `spesa/templates/spesa/lista.html`:
    ```html
      <ul>
        {% for x in lista %} 
        <li>{{ x.title }}</li>
        {% endfor %}
      </ul>
    ```
8. **URL**: In `config/urls.py`:
    ```python
    from django.contrib import admin
    from django.urls import path
    from spesa.views import lista_spesa_view

    urlpatterns = [
        ...
        path('spesa/', lista_spesa_view, name='lista_spesa_view')
    ]  
    ```

9. **Creare utente**
    - Aprire il terminale del container
    ```python
    python manage.py createsuperuser --username gestore
    ```
    Inserire email (facoltativa) e password (+ conferma)

python manage.py shell