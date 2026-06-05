from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from .models import Risorsa, Utente
from .forms import RisorsaForm
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def redirect_alla_home(request):
    return redirect('home')

def home(request):
    actions=[
        {
            'title': 'Vai alla lista delle risorse',
            'url': 'risorsa_all',
            'icon': 'list'
        }
    ]
    return render(request, 'home.html', {'actions': actions})

def risorsa_all(request):
    """
    Visualizza l'elenco delle risorse con ordinamento e paginazione dinamica.
    """
    # FILTRO
    filter_value =request.GET.get('filter', '')    
    risorse_list = Risorsa.objects.all()
    if filter_value:
        risorse_list = risorse_list.filter(titolo__icontains=filter_value)

    
    # ORDINAMENTO
    sort_field = request.GET.get('sort', 'titolo')
    sort_dir = request.GET.get('dir', 'asc')
    # validation
    campi_ammessi = ['id', 'titolo', 'descrizione', 'prezzo', 'disponibile']
    if sort_field not in campi_ammessi:
        sort_field = 'titolo'
    ordine = f"-{sort_field}" if sort_dir == 'desc' else sort_field
    # apply
    risorse_list = risorse_list.order_by(ordine)

    
    # PAGINAZIONE
    pagination_limit = request.GET.get('limit', '10')
    page_number = request.GET.get('page', 1)
    # Validation
    allowed_limits = ['5', '10', '20', '30', '50', '100']
    if pagination_limit not in allowed_limits:
        pagination_limit = '10'
    pagination_limit_int = int(pagination_limit)
    # apply
    paginator = Paginator(risorse_list, pagination_limit_int)
    risorse = paginator.get_page(page_number)

    print(f"\n[DEBUG] risorsa_all ({paginator.count} results)")
    print(f"- Sort: {sort_field}={sort_dir}\n- Limit: {pagination_limit}\n- Page: {page_number}\n- Filter: {filter_value}")

    return render(request, 'risorsa_all.html', {
        'page_title': 'Risorse',
        'risorse': risorse,
        'current_sort': sort_field,
        'current_dir': sort_dir,
        'current_limit': pagination_limit,
        'allowed_limits': allowed_limits,
        'current_filter': filter_value,
        'page_range': paginator.get_elided_page_range(risorse.number, on_each_side=2, on_ends=1)
    })

def risorsa_create(request):
    """
    Gestisce la creazione di una nuova risorsa.
    Se la richiesta è POST, convalida il form e salva i dati.
    Altrimenti, mostra un form vuoto per l'inserimento manuale.
    """
    if request.method == 'POST':
        # L'utente ha cliccato sul pulsante di invio, processiamo i dati ricevuti
        form = RisorsaForm(request.POST)
        if form.is_valid():
            # I dati sono corretti e sicuri, procediamo con il salvataggio nel database
            form.save()
            return redirect('risorsa_all')
    else:
        # L'utente è appena arrivato sulla pagina, forniamo un modulo vuoto da compilare
        form = RisorsaForm()

    return render(request, 'risorsa_form.html', {
        'form': form, 
        'titolo_pagina': 'Aggiungi Risorsa'
    })

def risorsa_update(request, pk):
    """
    Modifica una risorsa esistente identificata dalla sua chiave primaria (pk).
    Carica i dati correnti nel form e, in caso di invio (POST), aggiorna il database.
    Se la risorsa non esiste, restituisce un errore 404.
    """
    risorsa = get_object_or_404(Risorsa, pk=pk)

    if request.method == 'POST':
        # L'utente ha inviato le modifiche, le applichiamo all'istanza esistente
        form = RisorsaForm(request.POST, instance=risorsa)
        if form.is_valid():
            # Verifichiamo la validità e aggiorniamo il record nel database
            form.save()
            return redirect('risorsa_all')
    else:
        # Carichiamo i dati attuali della risorsa nel form per permetterne la modifica
        form = RisorsaForm(instance=risorsa)

    return render(request, 'risorsa_form.html', {
        'form': form, 
        'risorsa': risorsa, 
        'titolo_pagina': 'Modifica Risorsa'
    })

def risorsa_delete(request, pk):
    """
    Gestisce l'eliminazione sicura di una risorsa.
    Mostra una pagina di conferma. La cancellazione effettiva avviene
    solo se la richiesta viene confermata tramite il metodo POST.
    """
    risorsa = get_object_or_404(Risorsa, pk=pk)

    if request.method == 'POST':
        # L'eliminazione è stata confermata esplicitamente dall'utente
        risorsa.delete()
        return redirect('risorsa_all')

    # Se la richiesta è GET, mostriamo la pagina di avviso prima di procedere
    return render(request, 'risorsa_delete.html', {'risorsa': risorsa})


# UTENTI

utente_fields_list =["nome", "cognome", "email", "eta", "attivo"]

class UtenteCreateView(CreateView):
    model = Utente
    fields = utente_fields_list
    template_name = "utente_form.html"
    success_url =reverse_lazy('utente_list')

@login_required(login_url='auth_access')
def utente_list(request):
    utenti = Utente.objects.all()
    return render(request, "utente_all.html", {
        "title": "Lista Utenti",
        "utenti": utenti
    })

class UtenteDetailView(DetailView):
    model = Utente
    template_name = "utente_detail.html"

class UtenteUpdateView(UpdateView):
    model = Utente
    template_name = "utente_form.html"
    fields = utente_fields_list
    success_url =reverse_lazy('utente_list')

class UtenteDeleteView(DeleteView):
    model = Utente
    template_name = "utente_delete.html"
    success_url =reverse_lazy('utente_list')


# PROFILO UTENTI 

@login_required(login_url='auth_access')
def utente_profilo(request, pk:int):
    utente :Utente = get_object_or_404(Utente, pk=pk)
    return render(request, "utente_profilo.html", {
        "title": f"Profilo {utente.cognome} {utente.nome}",
        "utente": utente
    })

def auth_logout(request):
    logout(request)
    return redirect('risorsa_all')

def auth_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('risorsa_all')
    else:
        form = UserCreationForm()
    return render(request, 'auth_register.html', {'form': form})

def auth_access(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('risorsa_all')
    else:
        form = AuthenticationForm()
    return render(request, 'auth_access.html', {'form': form})


# 2) decoratore cache memorizza ogni 10 minuti che varia in base ai cokie
# 3) view che accestta solo richieste post altrimenti errore 405
# 4) applica una cbv con [GET,POST] -> login_required su metodo dispatch. 
#    @require_http_methods(["GET","POST"])
# 5) @solo_staff controlla request.user.is_staff =True. 
#    se non lo è restituisce HttpResponseForbidden("Accessso riservato solo allo staff"). 
#    usa functools.wraps per preservare i metadati
