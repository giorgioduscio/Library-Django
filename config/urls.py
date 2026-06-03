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

    # GESTIONE UTENTI
    # CATALOGO
    path('catalogo/', views.risorsa_all, name='risorsa_all'),
    path('catalogo/nuovo/', views.risorsa_create, name='risorsa_create'),
    path('catalogo/modifica/<int:pk>/', views.risorsa_update, name='risorsa_update'),
    path('catalogo/elimina/<int:pk>/', views.risorsa_delete, name='risorsa_delete'),
]
