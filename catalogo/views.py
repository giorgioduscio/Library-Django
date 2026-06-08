from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Risorsa
from .forms import RisorsaForm
from django.core.paginator import Paginator
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

def redirect_alla_home(request):
    return redirect('home')

@cache_page(60 * 15) 
@vary_on_cookie
def home(request):
    return render(request, 'home.html', {
        'title': "Home | Library Demo",
        'totale_risorse': len(Risorsa.objects.all()),
        'utenti_attivi': len(User.objects.filter(is_active=True)),
        'prestiti_attivi': len(Risorsa.objects.filter(disponibile=False)),
    })
 
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
    sort_field = request.GET.get('sort', 'id')
    sort_dir = request.GET.get('dir', '')
    # validation
    sort_allowed_fields = ['id', 'titolo', 'descrizione', 'prezzo', 'disponibile']
    if sort_field not in sort_allowed_fields:
        sort_field = 'id'

    headings = [
        {'key': 'id', 'label': 'ID'},
        {'key': 'titolo', 'label': 'Titolo'},
        {'key': 'descrizione', 'label': 'Descrizione'},
        {'key': 'prezzo', 'label': 'Prezzo', 'class': 'badge bg-primary fs-6'},
        {'key': 'disponibile', 'label': 'Disponibile', 'type': 'boolean'},
    ]

    for h in headings:
        if h['key'] == sort_field:
            if sort_dir == 'asc': h['next_dir'] = 'desc'
            elif sort_dir == 'desc': h['next_dir'] = ''
            else: h['next_dir'] = 'asc'
        else:
            h['next_dir'] = 'asc'
        

    ordine = "" 
    if sort_dir == 'desc':
        ordine = f"-{sort_field}"
    elif sort_dir == 'asc':
        ordine = sort_field
    # apply
    if ordine: risorse_list = risorse_list.order_by(ordine)

    # PAGINAZIONE
    pagination_current_limit = request.GET.get('limit', '10')
    page_number = request.GET.get('page', 1)
    # Validation
    pagination_allowed_limits = ['5', '10', '20', '30', '50', '100']
    if pagination_current_limit not in pagination_allowed_limits:
        pagination_current_limit = '10'
    pagination_limit_int = int(pagination_current_limit)
    # apply
    paginator = Paginator(risorse_list, pagination_limit_int)
    risorse = paginator.get_page(page_number)

    return render(request, 'risorsa_all.html', {
        'title': 'Risorse',
        'risorse': risorse,
        'headings': headings,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'pagination_current_limit': pagination_current_limit,
        'pagination_allowed_limits': pagination_allowed_limits,
        'pagination_page_range': paginator.get_elided_page_range(risorse.number, on_each_side=2, on_ends=1),
        'filter_value': filter_value,
    })

def risorsa_create(request):
    if request.method == 'POST':
        form = RisorsaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('risorsa_all')
    else:
        form = RisorsaForm()
    return render(request, 'risorsa_form.html', {'form': form, 'titolo_pagina': 'Aggiungi Risorsa'})

def risorsa_update(request, pk):
    risorsa = get_object_or_404(Risorsa, pk=pk)
    if request.method == 'POST':
        form = RisorsaForm(request.POST, instance=risorsa)
        if form.is_valid():
            form.save()
            return redirect('risorsa_all')
    else:
        form = RisorsaForm(instance=risorsa)
    return render(request, 'risorsa_form.html', {'form': form, 'risorsa': risorsa, 'titolo_pagina': 'Modifica Risorsa'})

def risorsa_delete(request, pk):
    risorsa = get_object_or_404(Risorsa, pk=pk)
    if request.method == 'POST':
        risorsa.delete()
        return redirect('risorsa_all')
    return render(request, 'risorsa_delete.html', {'risorsa': risorsa})


# UTENTI

user_fields_list = ["username", "first_name", "last_name", "email", "is_active"]

class UtenteCreateView(CreateView):
    model = User
    fields = user_fields_list
    template_name = "utente_form.html"
    success_url = reverse_lazy('utente_list')

@login_required(login_url='auth_access')
def utente_list(request):
    utenti = User.objects.all()
    return render(request, "utente_all.html", {
        "title": "Lista Utenti",
        "utenti": utenti
    })

class UtenteDetailView(DetailView):
    model = User
    template_name = "utente_detail.html"
    context_object_name = "utente"

class UtenteUpdateView(UpdateView):
    model = User
    template_name = "utente_form.html"
    fields = user_fields_list
    success_url = reverse_lazy('utente_list')

class UtenteDeleteView(DeleteView):
    model = User
    template_name = "utente_delete.html"
    success_url = reverse_lazy('utente_list')


# PROFILO UTENTI 

@login_required(login_url='auth_access')
def utente_profilo(request, pk:int):
    utente = get_object_or_404(User, pk=pk)
    return render(request, "utente_profilo.html", {
        "title": f"Profilo {utente.last_name} {utente.first_name}",
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
