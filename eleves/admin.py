# eleves/admin.py
from django.contrib import admin
from .models import Eleves, Matiere, Semestre, Note

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