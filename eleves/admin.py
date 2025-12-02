# eleves/admin.py
from django.contrib import admin
from .models import Eleves, Matiere, Semestre, Note
# gestion_ec/admin.py
from django.urls import reverse
from django.utils.html import format_html
from .models import ListeEleves

@admin.register(ListeEleves)
class ListeElevesAdmin(admin.ModelAdmin):
    list_display = ['uploaded_at', 'fichier', 'bouton_refresh']
    readonly_fields = ['uploaded_at']

    def bouton_refresh(self, obj):
        url = reverse('refresh_eleves')
        return format_html(f'<a href="{url}" style="background:#007cba;color:white;padding:10px;padding:10px 20px;border-radius:5px;font-weight:bold;">Rafraîchir la liste des élèves maintenant</a>')
    bouton_refresh.short_description = "Action"
@admin.register(Eleves)
class ElevesAdmin(admin.ModelAdmin):
    list_display = ('code_eleve', 'nom', 'prenom', 'classe')
    search_fields = ('nom', 'prenom', 'code_eleve')

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'matiere', 'semestre', 'moyenne_semestre')
    list_filter = ('semestre', 'matiere')