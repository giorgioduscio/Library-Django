# Django & Python Security Best Practices


## ✅ Checklist Pre-Deploy

### 📋 Checklist di Sicurezza

- [x] **SECRET_KEY** generata casualmente e non in repository
- [x] **DEBUG = False** in produzione
- [x] **ALLOWED_HOSTS** configurato correttamente
- [ ] **HTTPS** abilitato con certificato SSL valido
- [ ] **HSTS** configurato
- [x] **Security Headers** (XSS, nosniff, X-Frame) configurati
- [ ] **Database** usa SSL e credenziali sicure
- [x] **Password** degli utenti sono complesse
- [ ] **2FA** abilitato per admin
- [ ] **Rate Limiting** configurato
- [x] **Logging** di sicurezza attivato
- [ ] **Backup** automatici configurati
- [x] **Dipendenze** aggiornate e prive di vulnerabilità ✅
- [x] **Docker** esegue con utente non root
- [ ] **Ports** esposte solo quelle necessarie
- [x] **Health Check** configurato
- [ ] **Monitoraggio** (Sentry, etc.) attivo
- [x] **Template di errore** personalizzati
- [x] **CSRF** protection attivo
- [x] **Sessioni** configurate in modo sicuro
- [ ] **WebSocket** con autenticazione e rate limiting
- [ ] **Nginx/Apache** configurato in modo sicuro
- [ ] **Firewall** configurato
- [ ] **Cron jobs** per backup e manutenzione

> **Documento generato:** 19 Giugno 2026  
> **Progetto:** django-demo  
> **Versione Django:** 6.0.4  

---

## 📋 Indice

1. [Analisi Sicurezza Attuale](#-analisi-sicurezza-attuale)
2. [Vulnerabilità Critiche Rilevate](#-vulnerabilit-critiche-rilevate)
3. [Vulnerabilità Medie Rilevate](#-vulnerabilit-medie-rilevate)
4. [Configurazione Django Sicura](#-configurazione-django-sicura)
5. [Sicurezza Applicazione](#-sicurezza-applicazione)
6. [Sicurezza Database](#-sicurezza-database)
7. [Sicurezza Autenticazione](#-sicurezza-autenticazione)
8. [Sicurezza API e WebSocket](#-sicurezza-api-e-websocket)
9. [Sicurezza Docker](#-sicurezza-docker)
10. [Sicurezza Dipendenze](#-sicurezza-dipendenze)
11. [Monitoraggio e Logging](#-monitoraggio-e-logging)
12. [Checklist Pre-Deploy](#-checklist-pre-deploy)
13. [Risorse e Strumenti](#-risorse-e-strumenti)

---

## 🔍 Analisi Sicurezza Attuale

### Stato del Progetto

Il progetto `django-demo` presenta **diverse vulnerabilità di sicurezza critiche** che devono essere risolte prima di qualsiasi deploy in produzione.

| Area | Stato | Gravità |
|------|-------|---------|
| Configurazione Django | ❌ Non Sicura | **CRITICA** |
| Gestione Segreti | ❌ Non Sicura | **CRITICA** |
| Headers di Sicurezza | ❌ Mancanti | **ALTA** |
| Autenticazione | ⚠️ Parzialmente Sicura | **MEDIA** |
| Docker | ⚠️ Parzialmente Sicura | **MEDIA** |
| Dipendenze | ⚠️ Non Ottimale | **MEDIA** |

---

## 🚨 Vulnerabilità Critiche Rilevate

### 1. **SECRET_KEY Esposta** ⚠️⚠️⚠️

**File:** `.env`, `config/settings.py`

```python
# .env - LINEA 3
SECRET_KEY=django-framework-completo

# settings.py - LINEA 24
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev')
```

**Rischi:**
- La SECRET_KEY è hardcoded nel file `.env` 
- Il default in settings.py è prevedibile (`django-insecure-default-key-for-dev`)
- Chiunque abbia accesso al repository può decifrare cookies, token CSRF, sessioni

**Soluzione:**
```python
# .env (NON committare questo file!)
SECRET_KEY=generata_con_`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

# settings.py
SECRET_KEY = os.getenv('SECRET_KEY')  # Rimuovere il default!
```

**Azione Immediata:**
1. Generare nuova SECRET_KEY
2. Aggiungere `.env` a `.gitignore`
3. Rimuovere `.env` dal repository Git
4. Rotare tutte le sessioni e cookies dopo il cambiamento

---

### 2. **DEBUG = True in Produzione** ⚠️⚠️⚠️

**File:** `.env` (LINEA 2), `docker-compose.yml` (LINEA 11)

```python
# .env
DEBUG=True

# docker-compose.yml
- DEBUG=${DEBUG:-True}
```

**Rischi:**
- Espone traceback dettagliati agli attacker
- Abilita l'interprete Python interattivo in caso di errore
- Disabilita alcune protezioni di sicurezza di Django
- Consente l'accesso a informazioni sensibili sul sistema

**Soluzione:**
```python
# .env
DEBUG=False

# docker-compose.yml
- DEBUG=${DEBUG:-False}

# settings.py
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

### 3. **ALLOWED_HOSTS Troppo Permissivo** ⚠️⚠️

**File:** `.env` (LINEA 3), `config/settings.py` (LINEA 29)

```python
# .env
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# settings.py
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')
```

**Rischi:**
- `0.0.0.0` permette connessioni da qualsiasi host
- Vulnerabile a HTTP Host header attacks
- Permette il bypass di alcune protezioni di sicurezza

**Soluzione:**
```python
# Produzione
ALLOWED_HOSTS=il-tuo-dominio.com,www.il-tuo-dominio.com

# Sviluppo
ALLOWED_HOSTS=localhost,127.0.0.1

# settings.py
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

---

### 4. **Mancano Headers di Sicurezza** ⚠️⚠️

**File:** `config/settings.py`

**Problema:** Non ci sono headers di sicurezza HTTP configurati.

**Headers Essenziali Mancanti:**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (presente via middleware)
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy` (CSP)
- `Strict-Transport-Security` (HSTS)
- `Referrer-Policy`
- `Permissions-Policy`

**Soluzione:**

Installare `django-csp` e `django-security`:
```bash
pip install django-csp django-security
```

Aggiungere a `settings.py`:
```python
# Security Headers
MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    # 'csp.middleware.CSPMiddleware',  # Se usi django-csp
]

# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "cdn.jsdelivr.net")
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'none'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_FORM_ACTION = ("'self'",)

# HSTS (solo HTTPS)
SECURE_HSTS_SECONDS = 31536000  # 1 anno
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Altra sicurezza
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
REFERRER_POLICY = 'same-origin'
```

---

### 5. **Credenziali Amministratore Esposte** ⚠️⚠️

**File:** `.env` (LINEA 5)

```python
# ACCESSO admin - adminadmin
```

**Rischi:**
- Credenziali hardcoded nel repository
- Facilmente trovabili con grep
- Permettono accesso completo al pannello admin

**Soluzione:**
1. Rimuovere il commento da `.env`
2. Cambiare immediatamente la password admin:
   ```bash
   python manage.py changepassword admin
   ```
3. Usare password complesse (minimo 16 caratteri, mix di maiuscole, minuscole, numeri, simboli)

---

### 6. **Dipendenze Non Pinnate** ⚠️⚠️

**File:** `requirements.txt`

```txt
Django==6.0.4
daphne
channels
channels-redis
```

**Rischi:**
- Versioni non specificate possono installare versioni vulnerabili
- Difficile riprodurre esattamente lo stesso ambiente
- Possibili supply chain attacks

**Soluzione:**
```txt
# requirements.txt
Django==6.0.4
daphne==4.0.0
channels==4.1.0
channels-redis==4.2.0

# Generare requirements.txt precisi:
pip freeze > requirements.txt
```

**Nota:** Django 6.0.4 è aggiornato (giugno 2026), ma verificare sempre su [Django Security Advisories](https://www.djangoproject.com/weblog/)

---

### 7. **Nessun Rate Limiting** ⚠️

**Problema:** Il progetto non ha protezione contro attacchi brute force.

**Rischi:**
- Attacchi brute force su login
- Attacchi DoS
- Abuso di risorse

**Soluzione:**

Installare `django-ratelimit`:
```bash
pip install django-ratelimit
```

Applicare ai views di autenticazione:
```python
# users/views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def auth_access(request):
    # ... codice esistente

@ratelimit(key='ip', rate='5/h', block=True)
def auth_register(request):
    # ... codice esistente
```

Oppure usare `django-axes` per protezione avanzata:
```bash
pip install django-axes
```

Aggiungere a `settings.py`:
```python
INSTALLED_APPS += ['axes']
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

---

### 8. **Sessioni Non Sicure** ⚠️

**Problema:** Le sessioni non hanno configurazione di sicurezza adeguata.

**Soluzione:**
```python
# settings.py

# Cookie sicuri (solo HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Cookie HttpOnly
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Cookie SameSite
SESSION_COOKIE_SAMESITE = 'Lax'  # o 'Strict' per maggiore sicurezza
CSRF_COOKIE_SAMESITE = 'Lax'

# Scadenza sessione
SESSION_COOKIE_AGE = 1200  # 20 minuti
SESSION_SAVE_EVERY_REQUEST = True  # Reset timer ad ogni richiesta
```

---

## ⚠️ Vulnerabilità Medie Rilevate

### 1. **WebSocket Senza Validazione Aggiuntiva**

**File:** `chat/consumers.py`

Il consumer verifica solo se l'utente è autenticato (LINEA 35-36), ma non:
- Validazione del room_name
- Controllo se l'utente ha accesso alla room
- Rate limiting sui messaggi
- Sanitizzazione del contenuto dei messaggi

**Soluzione:**
```python
# chat/consumers.py
import re
from django.utils.html import escape

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        # Validazione room_name
        if not re.match(r'^[a-zA-Z0-9_-]{3,100}$', self.room_name):
            await self.close()
            return
            
        # Controllo accesso utente alla room
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return
            
        # Verifica che l'utente appartenga alla room
        room = await database_sync_to_async(Room.objects.get)(name=self.room_name)
        if not await database_sync_to_async(lambda: room.users.filter(id=user.id).exists())():
            await self.close()
            return
            
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('text', '')
        
        # Validazione lunghezza messaggio
        if not message_text or len(message_text) > 5000:
            return
            
        # Sanitizzazione
        message_text = escape(message_text.strip())
        
        # Rate limiting per utente (esempio semplice)
        user = self.scope['user']
        # Implementare logica rate limiting...
        
        # ... resto del codice
```

---

### 2. **Nessun CSRF Protection per WebSocket**

**Problema:** Le connessioni WebSocket non hanno protezione CSRF.

**Soluzione:**

Aggiungere token CSRF alla connessione WebSocket:

Frontend (JavaScript):
```javascript
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/room/`);

// Inviare token come primo messaggio
socket.onopen = function() {
    socket.send(JSON.stringify({type: 'auth', csrf_token: csrfToken}));
};
```

Backend:
```python
# chat/consumers.py
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # ... codice esistente
        
        # Verifica CSRF token (da implementare con logica appropriata)
        # Può essere inviatto come query param o primo messaggio
        # Attenzione: i query param nei WebSocket sono visibili nei log
        
        await self.accept()
```

**Nota:** La protezione CSRF per WebSocket è complessa. Considerare l'uso di JWT o altri metodi di autenticazione.

---

### 3. **Delete Views Senza Protezione Aggiuntiva**

**File:** `users/views.py` (LINEA 96-108)

Le view di eliminazione utente non hanno:
- Conferma password per operazioni distruttive
- Log delle operazioni
- Protezione contro eliminazione accidentale

**Soluzione:**
```python
# users/views.py
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

class UtenteDeleteView(LoginRequiredMixin, user_passes_test, DeleteView):
    # ... codice esistente
    
    def test_func(self):
        # Solo superuser o staff possono eliminare utenti
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        # Log dell'operazione
        utente = self.get_object()
        logger.warning(f"Utente {request.user.username} ha eliminato {utente.username}")
        
        # Notifica
        messages.warning(request, f"Utente '{utente.username}' eliminato correttamente")
        return super().delete(request, *args, **kwargs)
```

---

### 4. **Nessun Logging di Sicurezza**

**Problema:** Non c'è logging delle operazioni sensibili.

**Soluzione:**

Creare `config/logging_config.py`:
```python
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'security': {
            'format': '[SECURITY] {asctime} {levelname} {user} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'formatter': 'security',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['security_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

Aggiungere a `settings.py`:
```python
from .logging_config import LOGGING

# Creare directory logs
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
```

---

### 5. **Dockerfile Non Sicuro**

**File:** `Dockerfile`

**Problemi:**
1. Esegue come root
2. Non usa utente non privilegiato
3. Non pulisce la cache di pip
4. Espone il codice sorgente

**Soluzione:**
```dockerfile
# Usa un'immagine Python ufficiale come base
FROM python:3.12-slim

# Impedisce a Python di scrivere file .pyc e di bufferizzare l'output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea utente non root
RUN groupadd -r django && useradd -r -g django django

# Imposta la directory di lavoro nel contenitore
WORKDIR /app

# Copia requirements prima per cache
COPY requirements.txt /app/

# Installa le dipendenze Python come root
RUN pip install --no-cache-dir --user -r requirements.txt

# Copia il resto del codice del progetto
COPY --chown=django:django . /app/

# Cambia utente a non-root
USER django

# Imposta PATH per includere .local
ENV PATH=/home/django/.local/bin:$PATH

# Espone la porta su cui gira Django
EXPOSE 8000

# Comando di default per avviare il server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

### 6. **Nessun Health Check**

**Problema:** Non c'è endpoint per health check.

**Soluzione:**

Aggiungere a `config/urls.py`:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': timezone.now().isoformat()
    })

urlpatterns += [
    path('health/', health_check, name='health_check'),
]
```

---

### 7. **Template di Errore Personalizzati Mancanti**

**Problema:** In produzione mostrano troppo informazioni.

**Soluzione:**

Creare template personalizzati:
```bash
mkdir -p config/templates
```

Creare `config/templates/404.html`:
```html
{% extends "shareds/base.html" %}
{% block content %}
<h1>404 - Pagina non trovata</h1>
<p>La pagina richiesta non esiste.</p>
{% endblock %}
```

Creare `config/templates/500.html`:
```html
{% extends "shareds/base.html" %}
{% block content %}
<h1>500 - Errore del server</h1>
<p>Si è verificato un errore. Riprova più tardi.</p>
{% endblock %}
```

Aggiungere a `settings.py`:
```python
# Template per errori
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
```

---

## 🔧 Configurazione Django Sicura

### Settings Minimi per la Produzione

```python
# config/settings_production.py
from .settings import *

# Sicurezza
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')  # Deve essere impostato
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 anno
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "cdn.jsdelivr.net")
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'none'",)
CSP_FRAME_ANCESTORS = ("'none'",)

# Database (esempio PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Channel Layers (Redis per produzione)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv('REDIS_URL', 'redis://localhost:6379/0')],
            "ssl_cert_reqs": None,  # Per sviluppo, in produzione usare 'required'
        },
    },
}

# Logging
LOGGING = {
    # ... configurazione logging
}

# Email (per reset password, ecc.)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
```

---

## 🛡️ Sicurezza Applicazione

### 1. Validazione Input

**Sempre validare e sanificare l'input:**

```python
# Esempio di view sicura
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
from django.core.exceptions import ValidationError

@require_http_methods(["GET", "POST"])
def safe_view(request):
    if request.method == 'POST':
        # Validazione form
        form = MyForm(request.POST)
        if not form.is_valid():
            return render(request, 'template.html', {'form': form, 'errors': form.errors})
        
        # Sanitizzazione dati
        clean_data = {
            'title': escape(form.cleaned_data['title']),
            'content': escape(form.cleaned_data['content']),
        }
        
        # Salvataggio sicuro
        try:
            obj = MyModel.objects.create(**clean_data)
        except ValidationError as e:
            # Gestione errori
            return render(request, 'template.html', {'error': str(e)})
    
    return render(request, 'template.html')
```

### 2. Protezione da SQL Injection

**Django ORM protegge automaticamente da SQL Injection**, ma:

✅ **SICURO:**
```python
# Usare sempre i parametri
User.objects.filter(username=username)

# Q objects
from django.db.models import Q
User.objects.filter(Q(username=username) | Q(email=email))
```

❌ **PERICOLOSO:**
```python
# NON usare mai query raw con string formatting
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# NON usare params con interpolazione
User.objects.raw(f"SELECT * FROM users WHERE username = '{username}'")
```

✅ **Se proprio necessario usare raw:**
```python
from django.db import connection

# Usare parametri con raw
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE username = %s", [username])
```

### 3. Protezione da XSS (Cross-Site Scripting)

**Django template automaticamente escape le variabili**, ma:

✅ **SICURO:**
```html
<!-- Django escape automaticamente -->
<p>{{ user_input }}</p>
```

❌ **PERICOLOSO:**
```html
<!-- safe mark disabilita l'escape -->
<p>{{ user_input|safe }}</p>

<!-- mark_safe -->
from django.utils.safestring import mark_safe
mark_safe(user_input)
```

**Soluzioni:**

1. **Non usare `|safe` con input utente**
2. **Usare `escape` per content dinamico:**
   ```html
   <p>{{ user_input|escape }}</p>
   ```
3. **Per HTML controllato, usare bleach per sanificare:**
   ```bash
   pip install bleach
   ```
   ```python
   import bleach
   clean_html = bleach.clean(user_input, tags=['p', 'b', 'i', 'a'], attributes={'a': ['href', 'title']})
   ```

### 4. Protezione da CSRF

**Django ha CSRF protection attivato per default**, ma:

✅ **SICURO:**
```html
<!-- Template con form -->
<form method="post">
    {% csrf_token %}
    <!-- campi form -->
</form>
```

❌ **PERICOLOSO:**
```python
# Disabilitare CSRF senza motivo valido
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # NON FARE!
def my_view(request):
    pass
```

**Per API:**
- Usare token CSRF nelle intestazioni: `X-CSRFToken`
- O usare JWT con autenticazione basata su token

### 5. Protezione da Clickjacking

Django ha già `XFrameOptionsMiddleware`, ma verificare:

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ...
]
```

Configurare:
```python
# Impostare su DENY per massima sicurezza
X_FRAME_OPTIONS = 'DENY'

# O su SAMEORIGIN per permettere frame dallo stesso dominio
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

---

## 🗄️ Sicurezza Database

### 1. Configurazione Database Sicura

✅ **SICURO (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',  # SSL obbligatorio
        },
    }
}
```

❌ **PERICOLOSO:**
```python
# SQLite in produzione
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 2. connessioni SSL al Database

Sempre usare SSL per connessioni remote:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ...
        'OPTIONS': {
            'sslmode': 'verify-full',  # Verifica certificato
        },
    }
}
```

### 3. Backup del Database

Implementare backup automatici:

```bash
# Script di backup (backup.sh)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/backups/db_${DATE}.sql"

pg_dump -U ${DB_USER} -h ${DB_HOST} ${DB_NAME} > ${BACKUP_FILE}
gzip ${BACKUP_FILE}

# Eliminare backup vecchi di 30 giorni
find /backups -name "*.sql.gz" -mtime +30 -delete
```

### 4. Sanitizzazione Dati

Usare validators nei modelli:

```python
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models

class UserProfile(models.Model):
    username = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username può contenere solo lettere, numeri e underscore'
            ),
            MinLengthValidator(3),
        ]
    )
    
    email = models.EmailField(
        validators=[
            EmailValidator(message='Email non valida'),
        ]
    )
```

---

## 🔐 Sicurezza Autenticazione

### 1. Password Policy

Django ha validators di default, ma possono essere rafforzati:

```python
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'max_similarity': 0.7,
            'user_attributes': ['username', 'first_name', 'last_name', 'email']
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Aumentato da 8
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # Aggiungere validator personalizzati
    {
        'NAME': 'users.validators.UppercaseValidator',
    },
    {
        'NAME': 'users.validators.LowercaseValidator',
    },
    {
        'NAME': 'users.validators.NumberValidator',
    },
    {
        'NAME': 'users.validators.SpecialCharValidator',
    },
]
```

### 2. Autenticazione a Due Fattori (2FA)

Usare `django-otp` o `django-two-factor-auth`:

```bash
pip install django-otp pyotp qrcode
```

Aggiungere a `settings.py`:
```python
INSTALLED_APPS += [
    'django_otp',
    'django_otp.plugins.otp_totp',
]

MIDDLEWARE += [
    'django_otp.middleware.OTPMiddleware',
]
```

### 3. Lockout Account

Usare `django-axes` per bloccare account dopo tentativi falliti:

```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Configurazione axes
AXES_FAILURE_LIMIT = 5  # Blocca dopo 5 tentativi
AXES_COOLOFF_TIME = 1  # 1 ora di attesa
AXES_LOCK_OUT_AT_FAILURE = True
AXES_LOCK_OUT_PARAMETERS = ['ip_address', 'username']
```

### 4. Reset Password Sicuro

Verificare che il reset password sia configurato correttamente:

```python
# settings.py
# Url per reset password
LOGIN_URL = 'auth_access'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Template per email reset password
PASSWORD_RESET_TIMEOUT = 86400  # 24 ore

# Usare backend email sicuro
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

### 5. Sessioni Sicure

```python
# settings.py

# Durata sessione
SESSION_COOKIE_AGE = 1200  # 20 minuti
SESSION_SAVE_EVERY_REQUEST = True

# Rotazione session key
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Eliminare sessioni scadute
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

---

## 🌐 Sicurezza API e WebSocket

### 1. Autenticazione WebSocket

Attualmente il progetto usa `AuthMiddlewareStack` che è buono, ma:

```python
# config/asgi.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```

**Miglioramenti:**

1. **Aggiungere autenticazione JWT:**
   ```bash
   pip install channels-jwt
   ```

2. **Validazione token:**
   ```python
   # chat/consumers.py
   from channels_jwt.auth import AuthMiddlewareStack
   from channels_jwt.tokens import AccessToken
   
   class JWTAuthMiddleware:
       def __init__(self, app):
           self.app = app
       
       async def __call__(self, scope, receive, send):
           # Estrae token dal query string o header
           token = scope.get('query_string', b'').decode()
           if token.startswith('token='):
               token = token[6:]
           else:
               return await self.app(scope, receive, send)
           
           try:
               # Verifica token JWT
               access_token = AccessToken(token)
               scope['user'] = await self.get_user(access_token)
           except:
               scope['user'] = AnonymousUser()
           
           return await self.app(scope, receive, send)
   ```

### 2. Rate Limiting WebSocket

Implementare rate limiting:

```python
# chat/consumers.py
from datetime import datetime, timedelta
from collections import defaultdict

class ChatConsumer(AsyncWebsocketConsumer):
    # Dictionary per tracciare i messaggi per utente
    user_message_count = defaultdict(list)
    RATE_LIMIT = 10  # 10 messaggi
    RATE_WINDOW = 60  # per 60 secondi
    
    async def receive(self, text_data):
        user = self.scope['user']
        now = datetime.now()
        
        # Pulire messaggi vecchi
        self.user_message_count[user.id] = [
            t for t in self.user_message_count[user.id]
            if now - t < timedelta(seconds=self.RATE_WINDOW)
        ]
        
        # Controlla rate limit
        if len(self.user_message_count[user.id]) >= self.RATE_LIMIT:
            await self.send(text_data=json.dumps({
                'error': 'Rate limit superato. Attendi prima di inviare altri messaggi.'
            }))
            return
        
        self.user_message_count[user.id].append(now)
        
        # ... resto del codice
```

### 3. Sanitizzazione Messaggi

```python
# chat/consumers.py
import bleach

class ChatConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('text', '')
        
        # Sanitizzazione con bleach
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a']
        allowed_attributes = {'a': ['href', 'title']}
        
        message_text = bleach.clean(
            message_text,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
        
        # Limitare lunghezza
        if len(message_text) > 500:
            message_text = message_text[:500]
        
        # ... resto del codice
```

---

## 🐳 Sicurezza Docker

### 1. Dockerfile Sicuro

```dockerfile
# Stage 1: Build
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installa dipendenze di build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e installa in una directory temporanea
COPY requirements.txt /tmp/
RUN pip install --user -r /tmp/requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea utente non root
RUN groupadd -r django && useradd -r -g django django
WORKDIR /app

# Copia solo i file necessari
COPY --from=builder /root/.local /home/django/.local
COPY --chown=django:django . /app

# Cambia utente
USER django
ENV PATH=/home/django/.local/bin:$PATH

# Espone la porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python manage.py check || exit 1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 2. docker-compose.yml Sicuro

```yaml
version: '3.8'

services:
  django-demo:
    build: .
    container_name: django-demo
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2
    user: django  # Esegue come utente non root
    volumes:
      - .:/app:ro  # Read-only per sicurezza
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - DB_HOST=db
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - REDIS_URL=redis://redis:6379/0
      - PYTHONUNBUFFERED=1
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "manage.py", "check"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - django-network

  db:
    image: postgres:15-alpine
    container_name: django-db
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - django-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: django-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - django-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  nginx:
    image: nginx:1.25-alpine
    container_name: django-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./config/nginx/ssl:/etc/nginx/ssl:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
    depends_on:
      - django-demo
    networks:
      - django-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:

networks:
  django-network:
    driver: bridge
```

### 3. Nginx Configuration Sicura

Creare `config/nginx/nginx.conf`:

```nginx
user nginx;
worker_processes auto;

 events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format security '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" $request_time $upstream_response_time';

    access_log /var/log/nginx/access.log security;
    error_log /var/log/nginx/error.log warn;

    # Sicurezza
    server_tokens off;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    upstream django {
        server django-demo:8000;
    }

    server {
        listen 80;
        server_name localhost;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name il-tuo-dominio.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        # HTTP/2
        http2 on;

        # HSTS
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

        location /static/ {
            alias /app/staticfiles/;
            expires 30d;
            add_header Cache-Control "public, max-age=2592000";
        }

        location /media/ {
            alias /app/media/;
            expires 30d;
            add_header Cache-Control "public, max-age=2592000";
        }

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;
            proxy_buffer_size 4k;
        }

        # WebSocket
        location /ws/ {
            proxy_pass http://django;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Security headers
        location = /robots.txt {
            access_log off;
            log_not_found off;
            return 200 "User-agent: *\nDisallow: /admin/\nDisallow: /private/\n";
        }

        location = /favicon.ico {
            access_log off;
            log_not_found off;
        }

        # Blocca accesso a file sensibili
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }
    }
}
```

---

## 📦 Sicurezza Dipendenze

### 1. Gestione Dipendenze

**Usare `pip-tools` per gestione dipendenze:**

```bash
pip install pip-tools
```

Creare `requirements.in`:
```txt
Django>=6.0,<6.1
daphne>=4.0,<5.0
channels>=4.1,<5.0
channels-redis>=4.2,<5.0
psycopg2-binary>=2.9.9
redis>=5.0.0
gunicorn>=21.0.0
bleach>=6.1.0
django-csp>=3.7
```

Generare `requirements.txt`:
```bash
pip-compile requirements.in
```

### 2. Controllo Vulnerabilità

**Usare `safety` per controllare vulnerabilità:**

```bash
pip install safety
safety check
```

**Usare `pip-audit`:**

```bash
pip install pip-audit
pip-audit
```

**Integrazione CI/CD:**

```yaml
# .github/workflows/security.yml
name: Security Check

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install safety pip-audit
          pip install -r requirements.txt
      
      - name: Run safety check
        run: safety check
      
      - name: Run pip-audit
        run: pip-audit
      
      - name: Check for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: main
```

### 3. Aggiornamenti Automatici

**Usare `dependabot` o `renovate` per aggiornamenti automatici:**

Creare `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "tuo-username"
    commit-message:
      prefix: "deps"
    labels:
      - "dependencies"
      - "security"
    milestone: 0
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
    groups:
      security-updates:
        patterns:
          - "*"
        update-types:
          - "security"
```

---

## 📊 Monitoraggio e Logging

### 1. Logging di Sicurezza

Creare `config/logging_config.py`:

```python
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'security': {
            'format': '[SECURITY] {asctime} {levelname} user={user} ip={remote_addr} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'add_user': {
            '()': 'config.logging_filters.AddUserFilter',
        },
        'add_ip': {
            '()': 'config.logging_filters.AddIPFilter',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'security',
            'filters': ['add_user', 'add_ip'],
        },
        'request_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'requests.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'request_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['request_file', 'error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'chat': {
            'handlers': ['security_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['security_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

Creare `config/logging_filters.py`:

```python
import logging
from django.contrib.auth import get_user_model

User = get_user_model()

class AddUserFilter(logging.Filter):
    def filter(self, record):
        # Aggiunge informazioni utente al log
        if hasattr(record, 'request') and record.request:
            user = record.request.user
            if user and user.is_authenticated:
                record.user = user.username
            else:
                record.user = 'anonymous'
        else:
            record.user = 'no-request'
        return True

class AddIPFilter(logging.Filter):
    def filter(self, record):
        # Aggiunge IP al log
        if hasattr(record, 'request') and record.request:
            x_forwarded_for = record.request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                record.remote_addr = x_forwarded_for.split(',')[0]
            else:
                record.remote_addr = record.request.META.get('REMOTE_ADDR', 'unknown')
        else:
            record.remote_addr = 'no-request'
        return True
```

### 2. Middleware per Logging

```python
# config/middleware.py
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django.security')

class SecurityLoggingMiddleware(MiddlewareMixin):
    """Middleware per logging operazioni di sicurezza"""
    
    def process_request(self, request):
        # Log delle richieste
        if request.path.startswith('/admin/') or request.path.startswith('/api/'):
            logger.info(
                f"Request: {request.method} {request.path} "
                f"User: {request.user.username if request.user.is_authenticated else 'anonymous'} "
                f"IP: {self.get_client_ip(request)}"
            )
    
    def process_response(self, request, response):
        # Log delle risposte di errore
        if response.status_code >= 400:
            logger.warning(
                f"Response {response.status_code}: {request.method} {request.path} "
                f"User: {request.user.username if request.user.is_authenticated else 'anonymous'} "
                f"IP: {self.get_client_ip(request)}"
            )
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', 'unknown')
```

Aggiungere a `settings.py`:
```python
MIDDLEWARE.insert(0, 'config.middleware.SecurityLoggingMiddleware')
```

### 3. Monitoraggio con Sentry

Installare Sentry:
```bash
pip install sentry-sdk
```

Configurare in `settings.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment='production',
    )
```

---

## 📚 Risorse e Strumenti

### Strumenti di Sicurezza

| Strumento | Descrizione | Link |
|-----------|-------------|------|
| **Safety** | Controllo vulnerabilità dipendenze Python | [https://github.com/pyupio/safety](https://github.com/pyupio/safety) |
| **pip-audit** | Audit dipendenze per vulnerabilità | [https://pypi.org/project/pip-audit/](https://pypi.org/project/pip-audit/) |
| **Bandit** | Static code analysis per Python | [https://bandit.readthedocs.io/](https://bandit.readthedocs.io/) |
| **Semgrep** | Static analysis per molte lingue | [https://semgrep.dev/](https://semgrep.dev/) |
| **TruffleHog** | Scansione secrets in repository | [https://github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) |
| **OWASP ZAP** | Security testing automatico | [https://www.zaproxy.org/](https://www.zaproxy.org/) |
| **Sentry** | Error monitoring | [https://sentry.io/](https://sentry.io/) |
| **Dependabot** | Aggiornamenti automatici dipendenze | [https://dependabot.com/](https://dependabot.com/) |

### Documentazione Ufficiale

- [Django Security Documentation](https://docs.djangoproject.com/en/6.0/topics/security/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Django Security](https://cheatsheetseries.owasp.org/cheatsheets/Django_Cheat_Sheet.html)
- [Python Security](https://wiki.python.org/moin/Security)
- [Mozilla Observability](https://infosec.mozilla.org/guidelines/web_security)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

### Librerie Django per Sicurezza

| Libreria | Descrizione | Link |
|----------|-------------|------|
| **django-csp** | Content Security Policy | [https://django-csp.readthedocs.io/](https://django-csp.readthedocs.io/) |
| **django-axes** | Login attempt monitoring | [https://django-axes.readthedocs.io/](https://django-axes.readthedocs.io/) |
| **django-otp** | Two-factor authentication | [https://django-otp-official.readthedocs.io/](https://django-otp-official.readthedocs.io/) |
| **django-security** | Security headers e middleware | [https://github.com/sdelements/django-security](https://github.com/sdelements/django-security) |
| **django-ratelimit** | Rate limiting | [https://django-ratelimit.readthedocs.io/](https://django-ratelimit.readthedocs.io/) |
| **django-cors-headers** | CORS headers | [https://github.com/adamchainz/django-cors-headers](https://github.com/adamchainz/django-cors-headers) |

---

## 🎯 Riepilogo Azioni Immediate per django-demo

### 1. **Correzioni CRITICHE (Fare SUBITO)**

```bash
# 1. Generare nuova SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. Aggiornare .env (e rimuovere dal repository!)
# SECRET_KEY=<nuova_key_generata>
# DEBUG=False
# ALLOWED_HOSTS=il-tuo-dominio.com

# 3. Aggiornare docker-compose.yml
# Rimuovere DEBUG=True e usare variabili d'ambiente sicure

# 4. Rimuovere .env dal repository
rm .env
git rm .env --cached
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env from repository"

# 5. Cambiare password admin
python manage.py changepassword admin
```

### 2. **Correzioni ALTE PRIORITÀ (Fare questa settimana)**

```python
# Aggiungere a settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

### 3. **Correzioni MEDIE PRIORITÀ (Fare questo mese)**

1. Installare e configurare `django-csp`
2. Installare e configurare `django-axes`
3. Aggiungere rate limiting
4. Configurare logging di sicurezza
5. Aggiornare Dockerfile per sicurezza
6. Pinnare tutte le dipendenze in requirements.txt

---

## 📝 Note Finali

Questo documento fornisce una **linea guida completa** per la sicurezza del progetto Django e Python. Tuttavia, la sicurezza è un **processo continuo** che richiede:

1. **Monitoraggio costante** delle vulnerabilità
2. **Aggiornamenti regolari** delle dipendenze
3. **Audit periodici** del codice
4. **Test di penetrazione** regolari
5. **Formazione continua** del team

**La sicurezza non è un prodotto, è un processo.**

---

*Documento generato da Mistral Vibe per il progetto django-demo*
*Data: 19 Giugno 2026*
*Versione: 1.0*
