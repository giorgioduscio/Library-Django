from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Risorsa
from .forms import RisorsaForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .utils import get_crud_context
from django import forms

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


# UTENTI

user_fields_list = ["username", "first_name", "last_name", "email", "is_active"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = user_fields_list

def utente_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    
    return render(request, 'shareds/generic_form.html', {
        'form': form,
        'title': 'Nuovo Utente',
        'submit_action_label': 'Crea Utente',
        'cancel_url': reverse_lazy('user_list')
    })

def utente_update(request, pk):
    utente = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=utente)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=utente)
    
    return render(request, 'shareds/generic_form.html', {
        'form': form,
        'title': f'Modifica Utente: {utente.username}',
        'submit_action_label': 'Aggiorna Utente',
        'cancel_url': reverse_lazy('user_list')
    })

@login_required(login_url='auth_access')
def utente_list(request):
    headings = [
        {'key': 'id', 'label': 'ID'},
        {'key': 'username', 'label': 'Username'},
        {'key': 'first_name', 'label': 'Nome'},
        {'key': 'last_name', 'label': 'Cognome'},
        {'key': 'email', 'label': 'Email'},
        {'key': 'is_active', 'label': 'Attivo', 'type': 'boolean'},
    ]
    
    sort_allowed_fields = [h['key'] for h in headings]
    
    context = get_crud_context(
        request,
        queryset=User.objects.all(),
        headings=headings,
        sort_allowed_fields=sort_allowed_fields,
        title='Lista Utenti',
        filter_fields=['username', 'first_name', 'last_name', 'email'],
        url_names={
            'create': 'user_create',
            'detail': 'user_detail',
            'update': 'user_update',
            'delete': 'user_delete',
        }
    )
    context['label_create'] = "Nuovo Utente"
    return render(request, "shareds/crud_list.html", context)

class UtenteDetailView(DetailView):
    model = User
    template_name = "utente_detail.html"
    context_object_name = "utente"

class UtenteDeleteView(DeleteView):
    model = User
    template_name = "shareds/confirm_delete.html"
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utente = self.get_object()
        context['title'] = f"Elimina Utente {utente.username}"
        context['message'] = f"Sei sicuro di voler eliminare l'utente '{utente.username}'?"
        context['object_info'] = f"{utente.first_name} {utente.last_name} ({utente.email})"
        context['cancel_url'] = reverse_lazy('user_list')
        return context


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
    
    return render(request, 'shareds/generic_form.html', {
        'form': form,
        'title': 'Registrazione',
        'submit_action_label': 'Registrati',
        'cancel_url': reverse_lazy('home')
    })

def auth_access(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('risorsa_all')
    else:
        form = AuthenticationForm()
    
    return render(request, 'shareds/generic_form.html', {
        'form': form,
        'title': 'Accesso',
        'submit_action_label': 'Accedi',
        'cancel_url': reverse_lazy('home')
    })
