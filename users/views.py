from django.shortcuts import render 
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView 
from config.utils import get_crud_context
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, UserForm

# UTENTI


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
        'cancel_url': reverse_lazy('user_list'),
        'edit': True
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
        'cancel_url': reverse_lazy('user_list'),
        'edit': True
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
    template_name = "shareds/generic_form.html"
    context_object_name = "utente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utente = self.get_object()
        context['form'] = UserForm(instance=utente)
        context['title'] = f"Dettaglio Utente: {utente.username}"
        context['edit'] = False
        context['edit_url'] = reverse_lazy('user_update', kwargs={'pk': utente.pk})
        context['cancel_url'] = reverse_lazy('user_list')
        return context

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
def profilo_privato(request, pk:int):
    utente = get_object_or_404(User, pk=pk)
    risorse_match = utente.risorse.all()
    return render(request, "profilo_privato.html", {
        "title": f"Profilo {utente.last_name} {utente.first_name}",
        "utente": utente,
        "risorse": risorse_match
    })

def auth_logout(request):
    logout(request)
    return redirect('risorsa_all')

def auth_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('risorsa_all')
    else:
        form = RegisterForm()
    
    return render(request, 'shareds/generic_form.html', {
        'form': form,
        'title': 'Registrazione',
        'submit_action_label': 'Registrati',
        'cancel_url': reverse_lazy('home'),
        'edit': True
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
        'cancel_url': reverse_lazy('home'),
        'edit': True
    })
