from django.shortcuts import render, get_object_or_404
from django.http import Http404 # ⬅️ NOUVEL IMPORT NÉCESSAIRE
from .models import Eleves, Note, Semestre

# ... (fonctions précédentes)

def bulletin(request, code_eleve):
    eleve = get_object_or_404(Eleves, code_eleve=code_eleve.upper())
    semestre_nom = request.GET.get('semestre', 'S1')
    
    # ❌ ANCIEN CODE (Provoque l'erreur en essayant de CRÉER)
    # semestre, _ = Semestre.objects.get_or_create(nom=semestre_nom)
    # if semestre_nom in ['S1', 'S2']:
    #     Semestre.objects.get_or_create(nom='S1')
    #     Semestre.objects.get_or_create(nom='S2')

    # ✅ NOUVEAU CODE (Tente seulement de LIRE, ou 404)
    # 1. Tente de récupérer le Semestre demandé (S1, S2, etc.)
    try:
        semestre = Semestre.objects.get(nom=semestre_nom)
    except Semestre.DoesNotExist:
        # Si le semestre n'est pas trouvé (et donc pas créé), renvoie une erreur 404
        raise Http404(f"Le semestre '{semestre_nom}' n'existe pas dans la base de données. Il doit être pré-créé.")

    # 2. Le reste du code reste inchangé...
    notes = Note.objects.filter(eleve=eleve, semestre=semestre).select_related('matiere')

    total_moyennes = []
    for n in notes:
        # Calcul moyenne interrogations
        inters = [x for x in [n.inter1, n.inter2, n.inter3, n.inter4] if x is not None]
        n.moyenne_interrogations = round(sum(inters)/len(inters), 2) if inters else None

        # Calcul moyenne devoirs
        devoirs = [x for x in [n.devoir1, n.devoir2] if x is not None]
        n.moyenne_devoirs = round(sum(devoirs)/len(devoirs), 2) if devoirs else None

        # Moyenne semestre = (inter + 2×devoirs)/3
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