from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator

from .models import Risorsa
from .forms import RisorsaForm
from config.utils import get_crud_context

def redirect_alla_home(request):
    return redirect('home')

@cache_page(60 * 15) 
@vary_on_cookie
def home(request):
    features = [
        {
            'icon': 'book',
            'title': 'Gestione Risorse', 
            'description': 'Aggiungi, modifica e rimuovi risorse con facilità',
        },
        {
            'icon': 'person-fill',
            'title': 'Gestione degli utenti', 
            'description': 'Aggiungi, modifica e rimuovi utenti con facilità',
        },
        {
            'icon': 'shield-lock-fill',
            'title': 'Accesso Sicuro', 
            'description': 'Area protetta per gli amministratori con autenticazione',
            'is_logged': request.user.is_authenticated
        },
        {
            'icon': 'chat-dots',
            'title': 'Chat in Tempo Reale',
            'description': 'Comunica con altri utenti in tempo reale'
        }
    ]

    statistics=[
        {
            'title':'Risorse Totali', 
            'value': Risorsa.objects.count(),
            'color': 'info'
        },
        {
            'title':'Utenti Attivi', 
            'value': User.objects.filter(is_active=True).count(),
            'color': 'info'
        },
        {
            'title':'Prestiti Attivi', 
            'value': Risorsa.objects.filter(disponibile=False).count(),
            'color': 'warning'
        },
    ]

    tools_head=['Strumento', 'Descrizione']
    tools = [
        ['gear',          'Applicazioni', 'Suddivise per ambito Users, Catalogo e Chat'],
        ['box-fill',      'Docker',       'Utilizzo di docker per garantire portabilità e facilità di deploy'],
        ['git',           'Git',          'Utilizzo di git per versionamento del codice'],
        ['shield-fill',   'Guardie',      'Effettuati controlli per l\'accesso alle view'],
        ['key',           'Accesso',      'In caso di accesso non autorizzato, si viene reindirizzati alla pagina di login'],
        ['bootstrap',     'Bootstrap',    'Utilizzo di bootstrap per la creazione di interfacce responsive'],
        ['database-fill', 'Database',     'Utilizzo di database sqllate (attraverso l\'ORM) e Redis (per la chat realtime)'],
        ['code',          'Class based view', 'CBV per le richieste nel Catalogo, garantendo maggiore organizzazione e riutilizzo del codice'],
        ['code',          'Function based view', 'FBV per le richieste nell\'app Chat, garantendo maggiore personalizzazione delle risposte HTTP'],
        ['code',          'HTMX',         'Utilizzo di HTMX nella Chat per la creazione di interfacce interattive'],
        ['code',          'Websocket',    'Utilizzo di websocket nella Chat per rendere la comunicazione bidirezionale (realtime)'],
        ['bug-fill',      'Testing',      'Test di unità per prevenire errori, falsi positivi e regressioni'],
    ]

    return render(request, 'home.html', {
        'title': "Home | Library Demo",
        'features': features,
        'statistics': statistics,
        'tools_head': tools_head,
        'tools': tools,
    })

# --- GESTIONE RISORSE (ADMIN AREA) ---

class RisorsaListView(LoginRequiredMixin, View):
    """Visualizza l'elenco delle risorse con ordinamento e paginazione."""
    def get(self, request):
        headings = [
            {'key': 'id', 'label': 'ID'},
            {'key': 'titolo', 'label': 'Titolo'},
            {'key': 'descrizione', 'label': 'Descrizione'},
            {'key': 'prezzo', 'label': 'Prezzo', 'class': 'badge bg-primary fs-6'},
            {'key': 'disponibile', 'label': 'Disponibile', 'type': 'boolean'},
        ]
        context = get_crud_context(
            request, 
            queryset=Risorsa.objects.all(),
            headings=headings,
            sort_allowed_fields=[h['key'] for h in headings],
            title='Gestione Risorse',
            filter_fields=['titolo'],
            url_names={
                'create': 'risorsa_create',
                'update': 'risorsa_update',
                'delete': 'risorsa_delete',
            }
        )
        context['label_create'] = "Nuova risorsa"
        return render(request, 'shareds/crud_list.html', context)

class RisorsaCreateView(LoginRequiredMixin, CreateView):
    model = Risorsa
    form_class = RisorsaForm
    template_name = 'shareds/generic_form.html'
    success_url = reverse_lazy('risorsa_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Aggiungi Risorsa',
            'submit_action_label': 'Crea Risorsa',
            'cancel_url': self.success_url,
            'edit': True
        })
        return context

class RisorsaUpdateView(LoginRequiredMixin, UpdateView):
    model = Risorsa
    form_class = RisorsaForm
    template_name = 'shareds/generic_form.html'
    success_url = reverse_lazy('risorsa_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Modifica Risorsa: {self.object.titolo}',
            'submit_action_label': 'Aggiorna Risorsa',
            'cancel_url': self.success_url,
            'edit': True
        })
        return context

class RisorsaDeleteView(LoginRequiredMixin, DeleteView):
    model = Risorsa
    template_name = 'shareds/confirm_delete.html'
    success_url = reverse_lazy('risorsa_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Elimina {self.object.titolo}',
            'message': f"Sei sicuro di voler eliminare la risorsa '{self.object.titolo}'?",
            'object_info': self.object.descrizione[:150] + "..." if len(self.object.descrizione) > 150 else self.object.descrizione,
            'cancel_url': self.success_url
        })
        return context

# --- AZIONI UTENTE (SHOP / CATALOGO PUBBLICO) ---

class CatalogoPubblicoListView(LoginRequiredMixin, ListView):
    """Visualizza le risorse disponibili per il riscatto."""
    model = Risorsa
    template_name = 'profilo_catalogo.html'
    context_object_name = 'risorse'

    def get_queryset(self):
        return Risorsa.objects.filter(disponibile=True, utente__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop Risorse Disponibili'
        return context

class RisorsaClaimView(LoginRequiredMixin, View):
    """Assegna una risorsa all'utente corrente."""
    def post(self, request, pk):
        risorsa = get_object_or_404(Risorsa, pk=pk, disponibile=True, utente__isnull=True)
        risorsa.utente = request.user
        risorsa.disponibile = False
        risorsa.save()
        return redirect('user_profile', pk=request.user.pk)

class RisorsaRestituisciView(LoginRequiredMixin, View):
    """Gestisce la restituzione (conferma GET, azione POST)."""
    def get(self, request, pk):
        risorsa = get_object_or_404(Risorsa, pk=pk)
        context = {
            'title': f'Restituisci {risorsa.titolo}',
            'header': 'Conferma Restituzione',
            'message': f"Vuoi restituire la risorsa '{risorsa.titolo}' al catalogo?",
            'object_info': risorsa.titolo,
            'cancel_url': reverse_lazy('user_profile', kwargs={'pk': request.user.pk}),
            'submit_action_label': 'Restituisci',
        }
        return render(request, 'shareds/confirm_delete.html', context)

    def post(self, request, pk):
        risorsa = get_object_or_404(Risorsa, pk=pk)
        risorsa.disponibile = True
        risorsa.utente = None
        risorsa.save()
        return redirect('user_profile', pk=request.user.pk)
