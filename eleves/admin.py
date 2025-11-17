from django.contrib import admin
from .models import Eleves, Matiere, Semestre, Note

# === INLINE : Ajouter des notes directement sur la page de l'élève ===
class NoteInline(admin.TabularInline):
    model = Note
    extra = 1  # 1 ligne vide pour ajouter une note
    fields = ('matiere', 'semestre', 'note', 'appreciation')
    autocomplete_fields = ['matiere']

@admin.register(Eleves)
class ElevesAdmin(admin.ModelAdmin):
    list_display = ('code_eleve', 'prenom', 'nom', 'classe', 'nb_retard', 'nb_absence')
    search_fields = ('code_eleve', 'nom', 'prenom')
    list_filter = ('classe',)
    inlines = [NoteInline]  # PERMET D'AJOUTER DES NOTES ICI

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'coefficient')
    search_fields = ('nom',)

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee_scolaire')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'matiere', 'semestre', 'note', 'appreciation')
    list_filter = ('semestre', 'matiere')
    search_fields = ('eleve__nom', 'eleve__prenom')
    autocomplete_fields = ['eleve', 'matiere']