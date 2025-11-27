from django.shortcuts import render,get_object_or_404
from .models import Eleves
from django.urls import reverse
from django.http import HttpResponse
from .models import Eleves, Note, Semestre, Matiere

def index_eleves(request):
    return render(request, 'index.html')
def rechercher_eleve(request):
    eleve_info = None
    erreur_message = None

    if request.method == 'POST':
        code_eleve = request.POST.get('code_eleve', '').strip()
        if code_eleve:
            try:
                eleve_info = Eleves.objects.get(code_eleve=code_eleve)
            except Eleves.DoesNotExist:
                erreur_message = f"Aucun élève trouvé avec le code {code_eleve}."

    context = {
        'eleve_info': eleve_info,
        'erreur_message': erreur_message,
    }
    return render(request, 'eleves/recherche.html', context)

def bulletin(request, code_eleve):
    eleve = get_object_or_404(Eleves, code_eleve=code_eleve)
    semestre_param = request.GET.get('semestre', 'S1')

    notes = Note.objects.filter(
        eleve=eleve,
        semestre__nom=semestre_param
    ).select_related('matiere', 'semestre')

    # Calcul moyenne pondérée
    total_points = 0
    total_coeff = 0
    for n in notes:
        if n.notes is not None:
            total_points += float(n.notes) * n.matiere.coefficient
            total_coeff += n.matiere.coefficient

    moyenne_generale = round(total_points / total_coeff, 2) if total_coeff > 0 else None

    context = {
        'eleve': eleve,
        'notes': notes,
        'semestre': semestre_param,
        'moyenne_generale': moyenne_generale,
    }
    return render(request, 'eleves/bulletin.html', context)