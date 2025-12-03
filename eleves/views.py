from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404 
from django.contrib.auth.decorators import login_required # Import pour la restriction d'accès
from .models import Eleves, Note, Semestre, Matiere 
from gestion_ecole.constants import MATIERES_PAR_CLASSE

def index_eleves(request):
    return render(request, 'index.html')

def rechercher_eleve(request):
    # La fonction est correcte.
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

# =======================================================
# VUE DU BULLETIN (avec restriction de sécurité)
# =======================================================

def bulletin(request, code_eleve):
    eleve = get_object_or_404(Eleves, code_eleve=code_eleve.upper())
    semestre_nom = request.GET.get('semestre', 'S1')
    
    # 🛑 Restriction de Permission : Seul le Superutilisateur peut modifier les notes.
    peut_modifier = request.user.is_superuser # False pour tout autre utilisateur
    
    # 1. Tente de récupérer le Semestre
    try:
        semestre = Semestre.objects.get(nom=semestre_nom)
    except Semestre.DoesNotExist:
        raise Http404(f"Le semestre '{semestre_nom}' n'existe pas dans la base de données. Il doit être pré-créé.")

    # =======================================================
    # GESTION DE LA SAUVEGARDE DES NOTES (MÉTHODE POST)
    # =======================================================
    if request.method == 'POST':
        # 🛑 Blocage Sécurité : Si pas Superuser, ignorer la soumission POST.
        if not peut_modifier:
            return redirect('eleves:bulletin', code_eleve=code_eleve) 
        
        # Logique de sauvegarde des notes
        for key, value in request.POST.items():
            if '-' in key and value:
                
                try:
                    field_name, note_id = key.split('-')
                    note = Note.objects.get(pk=note_id, eleve=eleve, semestre=semestre)
                    
                    try:
                        clean_value = float(value)
                        # Assurer que la valeur est dans les bornes (0-20)
                        if not 0 <= clean_value <= 20:
                             clean_value = None 
                    except ValueError:
                        clean_value = None

                    if field_name in ['inter1', 'inter2', 'inter3', 'inter4', 'devoir1', 'devoir2']:
                        setattr(note, field_name, clean_value)
                        note.save()
                        
                except Exception:
                    continue 

        # Redirection après POST pour afficher les notes mises à jour et éviter la soumission multiple
        return redirect('eleves:bulletin', code_eleve=code_eleve)


    # =======================================================
    # PRÉPARATION DES DONNÉES (MÉTHODE GET / Après POST)
    # =======================================================
    
    # 1. Assurer que les objets Note existent pour toutes les matières de la classe
    # RAPPEL : Cette étape DOIT être exécutée en local avant le déploiement sur Vercel.
    
    nom_classe = getattr(eleve, 'classe', 'CLASSE_INCONNUE')
    matieres_requises = MATIERES_PAR_CLASSE.get(nom_classe, [])
    
    for nom_matiere in matieres_requises:
        # get_or_create s'exécute, mais la création (write) échouera sur Vercel/SQLite.
        matiere, _ = Matiere.objects.get_or_create(nom=nom_matiere) 
        Note.objects.get_or_create(
            eleve=eleve,
            semestre=semestre,
            matiere=matiere,
            defaults={'inter1': None}
        )

    # 2. Récupérer toutes les notes nécessaires (Lecture)
    notes = Note.objects.filter(eleve=eleve, semestre=semestre).select_related('matiere')

    # 3. Calcul des moyennes (Logique existante)
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
        'peut_modifier': peut_modifier, # ⬅️ Essentiel pour le template HTML
    }
    return render(request, 'eleves/bulletin.html', context)