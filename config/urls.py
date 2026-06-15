from django.contrib import admin
from django.urls import path
from users import views as USERS
from catalogo import views as CATALOGO
from chat import views as CHAT

urlpatterns = [
    # FUNZIONAMENTO BASE
    path('admin/', admin.site.urls),
    path('', CATALOGO.redirect_alla_home, name='redirect_alla_home'),
    path('home/', CATALOGO.home, name='home'),

    # CHAT
    path('chat/', CHAT.room_list, name='room_list'),
    path('chat/nuova/', CHAT.room_create, name='room_create'),
    path('chat/<str:room_name>/', CHAT.chat, name='chat'),
    path('chat/<str:room_name>/modifica/', CHAT.room_update, name='room_update'),
    path('chat/<str:room_name>/elimina/', CHAT.room_delete, name='room_delete'),

    # GESTIONE UTENTI
    path('utenti/', USERS.utente_list, name='user_list'),
    path('utenti/nuovo/', USERS.utente_create, name='user_create'),
    path('utenti/<int:pk>/', USERS.UtenteDetailView.as_view(), name='user_detail'),
    path('utenti/modifica/<int:pk>/', USERS.utente_update, name='user_update'),
    path('utenti/elimina/<int:pk>/', USERS.UtenteDeleteView.as_view(), name='user_delete'),
    
    # GESTIONE RISORSE 
    path('risorsa/', CATALOGO.RisorsaListView.as_view(), name='risorsa_all'),
    path('risorsa/nuovo/', CATALOGO.RisorsaCreateView.as_view(), name='risorsa_create'),
    path('risorsa/modifica/<int:pk>/', CATALOGO.RisorsaUpdateView.as_view(), name='risorsa_update'),
    path('risorsa/elimina/<int:pk>/', CATALOGO.RisorsaDeleteView.as_view(), name='risorsa_delete'),

    # CATALOGO PUBBLICO (SHOP)
    path('catalogo/', CATALOGO.CatalogoPubblicoListView.as_view(), name='catalogo_pubblico'),
    path('catalogo/claim/<int:pk>/', CATALOGO.RisorsaClaimView.as_view(), name='claim_risorsa'),
    path('catalogo/restituisci/<int:pk>/', CATALOGO.RisorsaRestituisciView.as_view(), name='risorsa_restituisci'),

    # PROFILO UTENTI
    path('register/', USERS.auth_register, name='auth_register'),
    path('access/', USERS.auth_access, name='auth_access'),
    path('logout/', USERS.auth_logout, name='auth_logout'),
    path('profilo/<int:pk>/', USERS.profilo_privato, name='user_profile'),
]
