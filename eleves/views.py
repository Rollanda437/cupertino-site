
from django.shortcuts import render, get_object_or_404
from .models import Eleves, Note, Semestre

def index_eleves(request):
    return render(request, 'index.html')

def rechercher_eleve(request):
    eleve_info = None
    erreur_message = None
    if request.method == 'POST':
        code = request.POST.get('code_eleve', '').strip().upper()
        if code:
            try:
                eleve_info = Eleves.objects.get(code_eleve=code)
            except Eleves.DoesNotExist:
                erreur_message = f"Aucun élève trouvé avec le code {code}."
    return render(request, 'eleves/recherche.html', {
        'eleve_info': eleve_info,
        'erreur_message': erreur_message,
    })

def bulletin(request, code_eleve):
    eleve = get_object_or_404(Eleves, code_eleve=code_eleve.upper())
    semestre_nom = request.GET.get('semestre', 'S1')
    
    # Crée le semestre s'il n'existe pas
    semestre, _ = Semestre.objects.get_or_create(nom=semestre_nom)
    if semestre_nom in ['S1', 'S2']:
        Semestre.objects.get_or_create(nom='S1')
        Semestre.objects.get_or_create(nom='S2')

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