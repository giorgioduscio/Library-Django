from django.contrib import admin
from django.urls import path
from catalogo import views
from chat import views as chat_views

urlpatterns = [
    # FUNZIONAMENTO BASE
    path('admin/', admin.site.urls),
    path('', views.redirect_alla_home, name='redirect_alla_home'),
    path('home/', views.home, name='home'),

    # CHAT
    path('chat/', chat_views.room_list, name='room_list'),
    path('chat/nuova/', chat_views.room_create, name='room_create'),
    path('chat/<int:id>/', chat_views.chat, name='chat'),
    path('chat/<int:id>/modifica/', chat_views.room_update, name='room_update'),
    path('chat/<int:id>/elimina/', chat_views.room_delete, name='room_delete'),

    # GESTIONE UTENTI
    path('utenti/', views.utente_list, name='user_list'),
    path('utenti/nuovo/', views.utente_create, name='user_create'),
    path('utenti/<int:pk>/', views.UtenteDetailView.as_view(), name='user_detail'),
    path('utenti/modifica/<int:pk>/', views.utente_update, name='user_update'),
    path('utenti/elimina/<int:pk>/', views.UtenteDeleteView.as_view(), name='user_delete'),
    
    # CATALOGO
    path('catalogo/', views.risorsa_all, name='risorsa_all'),
    path('catalogo/nuovo/', views.risorsa_create, name='risorsa_create'),
    path('catalogo/modifica/<int:pk>/', views.risorsa_update, name='risorsa_update'),
    path('catalogo/elimina/<int:pk>/', views.risorsa_delete, name='risorsa_delete'),

    # PROFILO UTENTI
    path('register/', views.auth_register, name='auth_register'),
    path('access/', views.auth_access, name='auth_access'),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('profilo/<int:pk>/', views.utente_profilo, name='user_profile'),
]
