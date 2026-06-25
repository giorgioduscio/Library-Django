# **Implementazione WebSocket con Django Channels e HTMX**

Questo progetto utilizza **Django Channels** per gestire le comunicazioni WebSocket in tempo reale e **HTMX** con l'estensione `ws` per semplificare l'interazione sul frontend.

## 1. **Configurazione Iniziale**

### **Dipendenze**
Assicurati che `channels` e `daphne` siano installati. In produzione si consiglia `channels-redis`.

### **Settings (`config/settings.py`)**
Le impostazioni principali includono l'aggiunta di `daphne`, `channels` e l'app `chat` alle `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'daphne',
    ...,
    'channels',
    'chat',
]

ASGI_APPLICATION = 'config.asgi.application'

# Layer di comunicazione (InMemory per sviluppo locale)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
```

---

## 2. **Configurazione ASGI (`config/asgi.py`)**

Il file `asgi.py` instrada il traffico HTTP standard e le connessioni WebSocket:

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Inizializza Django prima di importare il routing che usa i modelli ORM
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```

---

## 3. **Routing WebSocket (`chat/routing.py`)**

Definisce gli endpoint per le connessioni WebSocket:

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
```

---

## 4. **Il Consumer (`chat/consumers.py`)**

Il `ChatConsumer` gestisce la logica di connessione, ricezione messaggi (con salvataggio su DB) e invio di frammenti HTML ai client.

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('text')
        
        if not message_text or not self.scope['user'].is_authenticated:
            return

        # Salva il messaggio nel database
        message_obj = await self.save_message(self.scope['user'], self.room_name, message_text)

        # Renderizza il frammento HTML per HTMX
        html_message = render_to_string('chat/message_snippet.html', {'msg': message_obj})

        # Invia l'HTML a tutto il gruppo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'html': html_message
            }
        )

    async def chat_message(self, event):
        # Invia l'HTML direttamente al client (HTMX lo gestirà)
        await self.send(text_data=event['html'])

    @database_sync_to_async
    def save_message(self, user, room_name, text):
        room = Room.objects.get(name=room_name)
        return Message.objects.create(user=user, room=room, text=text)
```

---

## 5. **Frontend con HTMX (`chat/templates/chat/chat.html`)**

L'interfaccia utilizza l'estensione `ws` di HTMX per gestire la connessione senza scrivere JavaScript personalizzato.

```html
<script src="https://unpkg.com/htmx.org@1.9.12"></script>
<script src="https://unpkg.com/htmx.org@1.9.12/dist/ext/ws.js"></script>

<div hx-ext="ws" ws-connect="ws://{{ request.get_host }}/ws/chat/{{ room.name }}/">
    
    <!-- Area messaggi: HTMX aggiunge i nuovi messaggi qui (default: append) -->
    <div id="chat-messages">
        {% for msg in messages %}
            {% include 'chat/message.html' %}
        {% endfor %}
    </div>

    <!-- Form per invio messaggi -->
    <form ws-send hx-on="htmx:wsAfterSend: this.reset()">
        <input name="text" type="text" placeholder="Scrivi un messaggio...">
        <button type="submit">Invia</button>
    </form>
</div>
```

---

## 6. **Flusso di Lavoro**

1. **Connessione**: HTMX apre una connessione WebSocket quando l'elemento con `hx-ext="ws"` viene caricato.
2. **Invio**: Quando il form viene inviato, `ws-send` intercetta i dati e li invia come JSON al WebSocket.
3. **Ricezione**: Il server riceve il JSON, salva il messaggio e invia un frammento HTML (renderizzato da `message_snippet.html`) a tutti i client connessi al gruppo.
4. **Aggiornamento**: HTMX riceve l'HTML dal WebSocket e lo inserisce automaticamente nel DOM (tipicamente facendo l'append all'interno del div con l'estensione `ws`).

---

## 7. **Comandi Utili**

* **Sviluppo**: `python manage.py runserver` (usa Daphne automaticamente se configurato).
* **Produzione**: `daphne config.asgi:application`
