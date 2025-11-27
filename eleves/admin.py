# eleves/admin.py – VERSION ULTIME : tu remplis tout comme dans Excel
from django.contrib import admin
from .models import Eleves, Note

class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    fields = ('matiere', 'interro1', 'interro2', 'interro3', 'interro4',
              'devoir1', 'devoir2', 'appreciation')
    # Tu peux tout modifier ici !
    readonly_fields = ()  # RIEN n’est en lecture seule → tu modifies tout

    # Style magnifique (comme ton bulletin)
    class Media:
        css = {'all': ('css/admin_bulletin.css',)}

@admin.register(Eleves)
class ElevesAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'classe', 'code_eleve')
    search_fields = ('nom', 'prenom', 'code_eleve')
    list_filter = ('classe',)
    inlines = [NoteInline]   # ← TOUTES LES NOTES D’UN ÉLÈVE S’AFFICHENT ICI

    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom.upper()}"
    nom_complet.short_description = "Élève"