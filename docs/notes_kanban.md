# Note
## Comandi django abituaali

```bash
# requirements
pip freeze > requirements.txt
pip install -r requirements.txt

# cambia password admin
manage.py changepassword admin
```

## Modificare il modello (sviluppo)
**Situazione**: modifiche al modello quando il db è già popolato con dati inerenti al vecchio modello

* Se aggiungi un campo nuovo, aggiungi (blank=True, null=True)
* Se rimuovi i campi blank e null:
  1. Cancellare il database: rimuovere db.sqlite3
  2. Cancellare le migrazioni: cancellare tutti i file in `<app>/migrations/` tranne `__init__.py`
  3. Modificare il modello: rimuovere (blank=True, null=True)
  4. Creare nuove migrazioni: python manage.py makemigrations
  5. Applicare le migrazioni: python manage.py migrate
  6. Popolare i dati: python manage.py restart_db


# Kanban
## Work In Progress

* 1. *User experience*
  * dod: accessibilità
* 1. Revizionare sicurezza
  * leggi la sezione Checklist di Sicurezza in  @docs/security_practice.md 
* 2. Pensonalizzazione users (età, colore, icona bootstrap)
* 2. Implementare test
* 3. Estetica Layout chat
* 3. Professionalità sito

## Done

* catalogo risorse
* funzionamento base
* lista utenti 
* autenticazione
* implementare Vue.ts

## freeze

* Messa in produzione??