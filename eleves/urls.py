# eleves/urls.py
from django.urls import path
from . import views

#app_name = "eleves"
urlpatterns = [
    path('eleves/', views.index_eleves, name='index_eleves'),  # Exemple de vue de test
    path('rechercher/', views.rechercher_eleve, name='rechercher_eleve'),
    path('bulletin/<str:code_eleve>/', views.bulletin, name='bulletin'),
]
# === NETLIFY - GÉNÉRATION STATIQUE (CORRIGÉ) ===
from django_distill import distill_path
from eleves.views import rechercher_eleve, bulletin
from eleves.models import Eleves


urlpatterns += [
    # Page de recherche
    distill_path(
        'rechercher/',
        rechercher_eleve,
        name='rechercher',
        distill_func=lambda: [()]
    ),

    # Bulletins
    distill_path(
        'bulletin/<str:code_eleve>/',
        bulletin,
        name='bulletin',
        distill_func=lambda: [(e.code_eleve,) for e in Eleves.objects.all()]
    ),
]

