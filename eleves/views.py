from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404 
from .models import Eleves, Note, Semestre, Matiere 
# Assurez-vous que MATIERES_PAR_CLASSE existe dans votre fichier gestion_ecole/constants.py
from gestion_ecole.constants import MATIERES_PAR_CLASSE 
from django.db import IntegrityError 

# ... (index_eleves et rechercher_eleve restent inchangés) ...
def index_eleves(request):
    # Votre logique ici
    return render(request, 'index.html')
def rechercher_eleve(request):
    # Votre logique de recherche
    eleve_info = None
    erreur_message = None
    if request.method == 'POST':
        # ... (votre code de traitement POST)
        pass
    return render(request, 'eleves/recherche.html', {
        'eleve_info': eleve_info,
        'erreur_message': erreur_message,
    })
def bulletin(request, code_eleve):
    # Récupération de l'élève (avec classe reliée)
    eleve = get_object_or_404(Eleves.objects.select_related('classe'), code_eleve=code_eleve.upper())
    semestre_nom = request.GET.get('semestre', 'S1')
    
    try:
        semestre = Semestre.objects.get(nom=semestre_nom)
    except Semestre.DoesNotExist:
        # Gère le cas où le semestre n'existe pas
        raise Http404(f"Le semestre '{semestre_nom}' n'existe pas.")


    # =======================================================
    # GESTION DE LA SAUVEGARDE DES NOTES (MÉTHODE POST)
    # 🛑 BLOC SUPPRIMÉ :
    # Si nous n'utilisons PAS la saisie web, nous ignorons la méthode POST.
    # =======================================================
    # Si jamais un formulaire POST est soumis, on redirige immédiatement
    # pour s'assurer que les paramètres GET sont conservés et éviter les erreurs.
    if request.method == 'POST':
        return redirect('eleves:bulletin', code_eleve=code_eleve) + f'?semestre={semestre_nom}'


    # =======================================================
    # PRÉPARATION DES DONNÉES (MODE LECTURE)
    # =======================================================
    
    # 1. Créer les lignes de notes manquantes (pour que toutes les matières apparaissent dans le bulletin)
    nom_classe_cle = eleve.classe.nom.upper() if eleve.classe else 'CLASSE_INCONNUE'
    matieres_requises = MATIERES_PAR_CLASSE.get(nom_classe_cle, [])
    
    for nom_matiere in matieres_requises:
        try:
            matiere, _ = Matiere.objects.get_or_create(nom=nom_matiere) 
            # Note: Cette opération 'get_or_create' doit être effectuée 
            # pour s'assurer qu'une ligne 'Note' existe pour chaque matière, 
            # même si les notes (inter1, devoir1, etc.) sont NULL.
            Note.objects.get_or_create(
                eleve=eleve,
                semestre=semestre,
                matiere=matiere,
                defaults={'inter1': None}
            )
        except IntegrityError:
            continue

    # 2. Récupérer toutes les notes (Lecture des données saisies par terminal)
    notes = Note.objects.filter(eleve=eleve, semestre=semestre).select_related('matiere').order_by('matiere__nom')

    # 3. Calcul des moyennes (Ce bloc reste car il est nécessaire pour l'affichage du bulletin)
    total_moyennes = []
    for n in notes:
        # Notes individuelles pour le calcul de moyenne (interrogations)
        inters = [getattr(n, f'inter{i}') for i in range(1, 5)]
        inters = [x for x in inters if x is not None]
        # $n.moyenne\_interrogations = \text{round}(\sum(\text{inters}) / \text{len}(\text{inters}), 2)$
        n.moyenne_interrogations = round(sum(inters)/len(inters), 2) if inters else None

        # Notes individuelles pour le calcul de moyenne (devoirs)
        devoirs = [getattr(n, f'devoir{i}') for i in range(1, 3)]
        devoirs = [x for x in devoirs if x is not None]
        # $n.moyenne\_devoirs = \text{round}(\sum(\text{devoirs}) / \text{len}(\text{devoirs}), 2)$
        n.moyenne_devoirs = round(sum(devoirs)/len(devoirs), 2) if devoirs else None

        # Moyenne semestre (Formule : (Interro + 2 * Devoirs) / 3)
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
        'semestres_disponibles': Semestre.objects.all().order_by('nom') 
    }
    return render(request, 'eleves/bulletin.html', context)