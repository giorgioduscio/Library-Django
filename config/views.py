
from django.shortcuts import render

def handler404(request, exception=None):
    return render(request, 'shareds/error.html', {
        'code': 404, 
        'specify': 'Pagina non trovata', 
        'description': 'La pagina che stai cercando non esiste.'
    }, status=404)

def handler500(request):
    return render(request, 'shareds/error.html', {
        'code': 500, 
        'specify': 'Errore del server', 
        'description': 'Si è verificato un errore nel server.'
    }, status=500)