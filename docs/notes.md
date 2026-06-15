# Todo list

* 1. User experience: Utilizzo del sito da parte dell'utente
* 1. Revizionare sicurezza
* 2. Pensonalizzazione users (età, colore, icona bootstrap)
* 2. Implementare test
* 2. Layout chat
* 3. implementare Vue.ts???
* 3. Messa in produzione
* 3. Professionalità sito

# esercizi routing

1) 
re_path('/articoli/(?P<anno>\d{4})-(?P<mese>\d{2})-(?P<giorno>\d{2})', view. ArticoliPerDataView.as_view(), name='articoli_per_data')

2) 
reverse_lazy('prodotto_dettaglio', args={
    'settore':'elettronica',
    'id': 42
})

3) 
class ArticoloCreateView(CreateView):
    def get_success_url():
        return reverse_lazy('blog:lista_articoli')

4) 
urlpatterns =[
    path( include('shop.urls'), namespace='shop' ),
    path( include('blog.urls'), namespace='blog' )
]
