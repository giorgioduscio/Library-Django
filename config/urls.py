from django.contrib import admin
from django.urls import path
from users import views as users_views
from catalogo import views as catalogo_views
from chat import views as chat_views

urlpatterns = [
    # FUNZIONAMENTO BASE
    path('admin/', admin.site.urls),
    path('', catalogo_views.redirect_alla_home, name='redirect_alla_home'),
    path('home/', catalogo_views.home, name='home'),

    # CHAT
    path('chat/', chat_views.room_list, name='room_list'),
    path('chat/nuova/', chat_views.room_create, name='room_create'),
    path('chat/<str:room_name>/', chat_views.chat, name='chat'),
    path('chat/<str:room_name>/modifica/', chat_views.room_update, name='room_update'),
    path('chat/<str:room_name>/elimina/', chat_views.room_delete, name='room_delete'),

    # GESTIONE UTENTI
    path('utenti/', users_views.utente_list, name='user_list'),
    path('utenti/nuovo/', users_views.utente_create, name='user_create'),
    path('utenti/<int:pk>/', users_views.UtenteDetailView.as_view(), name='user_detail'),
    path('utenti/modifica/<int:pk>/', users_views.utente_update, name='user_update'),
    path('utenti/elimina/<int:pk>/', users_views.UtenteDeleteView.as_view(), name='user_delete'),
    
    # CATALOGO
    path('catalogo/', catalogo_views.risorsa_all, name='risorsa_all'),
    path('catalogo/nuovo/', catalogo_views.risorsa_create, name='risorsa_create'),
    path('catalogo/modifica/<int:pk>/', catalogo_views.risorsa_update, name='risorsa_update'),
    path('catalogo/elimina/<int:pk>/', catalogo_views.risorsa_delete, name='risorsa_delete'),

    # PROFILO UTENTI
    path('register/', users_views.auth_register, name='auth_register'),
    path('access/', users_views.auth_access, name='auth_access'),
    path('logout/', users_views.auth_logout, name='auth_logout'),
    path('profilo/<int:pk>/', users_views.utente_profilo, name='user_profile'),
]
