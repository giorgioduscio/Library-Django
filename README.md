# Django Demo Project

Questo è un progetto Django configurato con una struttura pulita e moderna, pronto per lo sviluppo locale e con supporto Docker.

## Scaricare il progetto

```bash
git clone https://github.com/giorgioduscio/Library-Django.git
cd Library-Django
```

---

## Comandi Principali

Di seguito sono elencati i comandi fondamentali per la gestione del server e del progetto.

### Gestione con Docker (consigliato)

Se preferisci usare Docker, usa questi comandi:

* **Costruire e avviare i container**:
  ```bash
  docker-compose up --build
  ```
* **Fermare i container**:
  ```bash
  docker-compose down
  ```
* **Eseguire comandi Django dentro il container**:
  ```bash
  docker-compose exec django-demo python manage.py migrate
  ```

* **Shotcut script per avviare i server, eseguire migrazioni e accedere al terminale**:
  
  Bash
  ```bash
  ./cmd.sh
  ```

  Powershell
  ```powershell
  ./cmd.ps1
  ```

---

### Gestione del Server (Locale)

Per eseguire questi comandi, assicurati di aver attivato il tuo ambiente virtuale (`venv`).

* **Avviare il server di sviluppo**:
  ```bash
  python manage.py runserver
  ```
* **Creare nuove migrazioni** (dopo aver modificato i modelli):
  ```bash
  python manage.py makemigrations
  ```
* **Applicare le migrazioni** (per aggiornare il database):
  ```bash
  python manage.py migrate
  ```
* **Creare un utente amministratore** (per l'area `/admin`):
  ```bash
  python manage.py createsuperuser
  ```
* **Creare una nuova app**:
  ```bash
  python manage.py startapp nome_app
  ```

## Struttura del Progetto

* `config/`: Contiene le impostazioni del progetto, gli URL principali e le configurazioni WSGI/ASGI.
* `manage.py`: L'utility da riga di comando per gestire il progetto.
* `Dockerfile` & `docker-compose.yml`: Configurazioni per l'ambiente containerizzato.
* `requirements.txt`: Elenco delle dipendenze Python.

# Workflow creare pagina (Esempio: Spesa)

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
    * Aprire il terminale del container
    ```python
    python manage.py createsuperuser --username gestore 
    ```
    Inserire email (facoltativa) e password (+ conferma)

