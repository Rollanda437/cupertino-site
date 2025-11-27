from django.urls import path
from . import views

app_name = 'avis'  # <--- TRÈS IMPORTANT : namespace !
urlpatterns = [
    path('', views.index_avis, name='index_avis'), 
    path('admin-only/', views.liste_avis, name='liste_avis_admin'),  # /avis/admin-only/
    path('liste/', views.liste_avis, name='liste_avis'),              # /avis/liste/
    path('<int:avis_id>/', views.detail_avis, name='detail_avis'),    # /avis/1/
    path('<int:avis_id>/ajouter_commentaire/', views.ajouter_commentaire, name='ajouter_commentaire'),
]