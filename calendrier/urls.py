# calendrier/urls.py
from django.urls import path
from gestion_ecole import views

urlpatterns = [
    # exemple de route
    path('', views.index_calendrier, name='index_calendrier'),
]
