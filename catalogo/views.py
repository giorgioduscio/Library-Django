from django.shortcuts import render, get_object_or_404, redirect
from .models import Risorsa
from .forms import RisorsaForm

def lista_risorse(request):
    """
    Visualizza l'elenco completo delle risorse.
    Recupera tutti i record dal database e li invia al template del catalogo.
    """
    risorse = Risorsa.objects.all()
    return render(request, 'catalogo.html', {'risorse': risorse})

def crea_risorsa(request):
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
            return redirect('lista_risorse')
    else:
        # L'utente è appena arrivato sulla pagina, forniamo un modulo vuoto da compilare
        form = RisorsaForm()

    return render(request, 'risorsa_form.html', {
        'form': form, 
        'titolo_pagina': 'Aggiungi Risorsa'
    })

def modifica_risorsa(request, pk):
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
            return redirect('lista_risorse')
    else:
        # Carichiamo i dati attuali della risorsa nel form per permetterne la modifica
        form = RisorsaForm(instance=risorsa)

    return render(request, 'risorsa_form.html', {
        'form': form, 
        'risorsa': risorsa, 
        'titolo_pagina': 'Modifica Risorsa'
    })

def elimina_risorsa(request, pk):
    """
    Gestisce l'eliminazione sicura di una risorsa.
    Mostra una pagina di conferma. La cancellazione effettiva avviene
    solo se la richiesta viene confermata tramite il metodo POST.
    """
    risorsa = get_object_or_404(Risorsa, pk=pk)

    if request.method == 'POST':
        # L'eliminazione è stata confermata esplicitamente dall'utente
        risorsa.delete()
        return redirect('lista_risorse')

    # Se la richiesta è GET, mostriamo la pagina di avviso prima di procedere
    return render(request, 'risorsa_confirm_delete.html', {'risorsa': risorsa})