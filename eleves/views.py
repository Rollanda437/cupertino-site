# eleves/views.py (Modifications Maintes)

from django.shortcuts import render, get_object_or_404
# ⚠️ Importez les fonctions de remplacement au lieu des modèles
from .sheets_repository import get_eleve_by_code, get_notes_for_bulletin, EleveSheet 

from django.http import Http404
# ... (votre fonction index_eleves reste inchangée) ...

def rechercher_eleve(request):
    eleve_info = None
    erreur_message = None
    if request.method == 'POST':
        code = request.POST.get('code_eleve', '').strip().upper()
        if code:
            try:
                # 🔄 Remplacement de Eleves.objects.get()
                eleve_info = get_eleve_by_code(code)
            except EleveSheet.DoesNotExist: 
                # 🔄 Remplacement de Eleves.DoesNotExist
                erreur_message = f"Aucun élève trouvé avec le code {code}."
    return render(request, 'eleves/recherche.html', {
        'eleve_info': eleve_info,
        'erreur_message': erreur_message,
    })


def bulletin(request, code_eleve):
    # ⚠️ Changements très minimes pour utiliser le Repository ⚠️
    
    # Remplacement de get_object_or_404(Eleves, code_eleve=code_eleve.upper())
    try:
        eleve = get_eleve_by_code(code_eleve.upper())
    except EleveSheet.DoesNotExist:
        raise Http404(f"Élève {code_eleve} non trouvé.")

    semestre_nom = request.GET.get('semestre', 'S1')
    
    # ❌ Suppression du code de création de Semestre dans la base de données
    # Car nous n'utilisons plus la DB.
    # if semestre_nom in ['S1', 'S2']:
    #     Semestre.objects.get_or_create(nom='S1')
    #     Semestre.objects.get_or_create(nom='S2')
    # semestre, _ = Semestre.objects.get_or_create(nom=semestre_nom) # Ligne supprimée
    
    # Nous recréons ici l'objet Semestre simulé pour que la suite du code fonctionne
    class SemestrePlaceholder: 
        def __init__(self, nom): self.nom = nom
    semestre = SemestrePlaceholder(semestre_nom)
    
    # 🔄 Remplacement de Note.objects.filter(...)
    notes = get_notes_for_bulletin(eleve, semestre_nom)

    # ----------------------------------------------------------------------
    # TOUT LE CODE SUIVANT (LOGIQUE DE CALCUL) RESTE INCHANGÉ !
    # ----------------------------------------------------------------------

    total_moyennes = []
    for n in notes:
        # Votre logique de calcul n'est PAS MODIFIÉE, elle utilise les attributs de NoteSheet
        inters = [x for x in [n.inter1, n.inter2, n.inter3, n.inter4] if x is not None]
        n.moyenne_interrogations = round(sum(inters)/len(inters), 2) if inters else None

        devoirs = [x for x in [n.devoir1, n.devoir2] if x is not None]
        n.moyenne_devoirs = round(sum(devoirs)/len(devoirs), 2) if devoirs else None

        if n.moyenne_interrogations is not None and n.moyenne_devoirs is not None:
            n.moyenne_semestre = round((n.moyenne_interrogations + 2 * n.moyenne_devoirs) / 3, 2)
            total_moyennes.append(n.moyenne_semestre)
        else:
            n.moyenne_semestre = None

    moyenne_generale = round(sum(total_moyennes)/len(total_moyennes), 2) if total_moyennes else None

    context = {
        'eleve': eleve,
        'notes': notes,
        'semestre': semestre,
        'moyenne_generale': moyenne_generale,
    }
    return render(request, 'eleves/bulletin.html', context)