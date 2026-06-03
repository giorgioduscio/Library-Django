from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Risorsa
from .forms import RisorsaForm
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def redirect_alla_home(request):
    return redirect('risorsa_all')

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