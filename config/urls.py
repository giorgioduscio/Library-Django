"""
URL configuration for django_demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalogo import views

urlpatterns = [
    # FUNZIONAMENTO BASE
    path('admin/', admin.site.urls),
    path('', views.redirect_alla_home, name='redirect_alla_home'),
    path('home/', views.home, name='home'),

    # GESTIONE UTENTI
    path('utenti/', views.utente_list, name='utente_list'),
    path('utenti/nuovo/', views.UtenteCreateView.as_view(), name='utente_create'),
    path('utenti/<int:pk>/', views.UtenteDetailView.as_view(), name='utente_detail'),
    path('utenti/modifica/<int:pk>/', views.UtenteUpdateView.as_view(), name='utente_update'),
    path('utenti/elimina/<int:pk>/', views.UtenteDeleteView.as_view(), name='utente_delete'),
    
    # CATALOGO
    path('catalogo/', views.risorsa_all, name='risorsa_all'),
    path('catalogo/nuovo/', views.risorsa_create, name='risorsa_create'),
    path('catalogo/modifica/<int:pk>/', views.risorsa_update, name='risorsa_update'),
    path('catalogo/elimina/<int:pk>/', views.risorsa_delete, name='risorsa_delete'),

    # PROFILO UTENTI
    path('register/', views.auth_register, name='auth_register'),
    path('access/', views.auth_access, name='auth_access'),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('profilo/<int:pk>/', views.utente_profilo, name='utente_profile'),
]
