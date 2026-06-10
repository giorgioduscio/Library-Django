from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Risorsa
from .forms import RisorsaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
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
            'value': len(Risorsa.objects.all()),
            'color': 'info'
        },
        {
            'title':'Utenti Attivi', 
            'value': len(User.objects.filter(is_active=True)),
            'color': 'info'
        },
        {
            'title':'Prestiti Attivi', 
            'value': len(Risorsa.objects.filter(disponibile=False)),
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

@login_required
def risorsa_all(request):
    """
    Visualizza l'elenco delle risorse con ordinamento e paginazione dinamica.
    """
    headings = [
        {'key': 'id', 'label': 'ID'},
        {'key': 'titolo', 'label': 'Titolo'},
        {'key': 'descrizione', 'label': 'Descrizione'},
        {'key': 'prezzo', 'label': 'Prezzo', 'class': 'badge bg-primary fs-6'},
        {'key': 'disponibile', 'label': 'Disponibile', 'type': 'boolean'},
    ]
    
    sort_allowed_fields = [h['key'] for h in headings]
    
    context = get_crud_context(
        request, 
        queryset=Risorsa.objects.all(),
        headings=headings,
        sort_allowed_fields=sort_allowed_fields,
        title='Risorse',
        filter_fields=['titolo'],
        url_names={
            'create': 'risorsa_create',
            'update': 'risorsa_update',
            'delete': 'risorsa_delete',
        }
    )
    context['label_create'] = "Nuova risorsa"
    
    return render(request, 'shareds/crud_list.html', context)

@login_required
def risorsa_create(request):
    if request.method == 'POST':
        form = RisorsaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('risorsa_all')
    else:
        form = RisorsaForm()
    
    return render(request, 'shareds/generic_form.html', {
        'form': form, 
        'title': 'Aggiungi Risorsa',
        'submit_action_label': 'Crea Risorsa',
        'cancel_url': reverse_lazy('risorsa_all')
    })

@login_required
def risorsa_update(request, pk):
    risorsa = get_object_or_404(Risorsa, pk=pk)
    if request.method == 'POST':
        form = RisorsaForm(request.POST, instance=risorsa)
        if form.is_valid():
            form.save()
            return redirect('risorsa_all')
    else:
        form = RisorsaForm(instance=risorsa)
    
    return render(request, 'shareds/generic_form.html', {
        'form': form, 
        'title': f'Modifica Risorsa: {risorsa.titolo}',
        'submit_action_label': 'Aggiorna Risorsa',
        'cancel_url': reverse_lazy('risorsa_all')
    })

@login_required
def risorsa_delete(request, pk):
    risorsa = get_object_or_404(Risorsa, pk=pk)
    if request.method == 'POST':
        risorsa.delete()
        return redirect('risorsa_all')
    
    context = {
        'title': f'Elimina {risorsa.titolo}',
        'message': f"Stai per eliminare la risorsa '{risorsa.titolo}'.",
        'object_info': (risorsa.descrizione[:100] + '...') if len(risorsa.descrizione) > 100 else risorsa.descrizione,
        'cancel_url': reverse_lazy('risorsa_all')
    }
    return render(request, 'shareds/confirm_delete.html', context)

