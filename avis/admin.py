from django.contrib import admin
from .models import Avis, Commentaire  # Assurez-vous d'importer vos modèles

# Optionnel : Personnaliser l'affichage dans l'admin
class AvisAdmin(admin.ModelAdmin):
    list_display = ('titre', 'contenu', 'date_publication')  # Champs à afficher dans la liste
    list_filter = ('date_publication',)  # Filtres disponibles
    search_fields = ('titre', 'contenu')  # Champs recherchables
    ordering = ('-date_publication',)  # Tri par défaut

# Enregistrer les modèles
admin.site.register(Avis, AvisAdmin)
admin.site.register(Commentaire)  # Si vous voulez aussi gérer les commentaires

# Register your models here.
