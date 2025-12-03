from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404 
from .models import Eleves, Note, Semestre, Matiere # Ajout de Matiere
from gestion_ecole.constants import MATIERES_PAR_CLASSE

def index_eleves(request):
    return render(request, 'index.html')

def rechercher_eleve(request):
    # NOTE: Cette fonction est correcte et ne nécessite pas de modification majeure
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
    
    # 1. Tente de récupérer le Semestre (Lecture seule)
    try:
        semestre = Semestre.objects.get(nom=semestre_nom)
    except Semestre.DoesNotExist:
        raise Http404(f"Le semestre '{semestre_nom}' n'existe pas dans la base de données. Il doit être pré-créé.")

    # =======================================================
    # GESTION DE LA SAUVEGARDE DES NOTES (MÉTHODE POST)
    # =======================================================
    if request.method == 'POST':
        
        for key, value in request.POST.items():
            # Les champs POST sont nommés 'champ-pk', ex: 'inter1-42'
            if '-' in key and value:
                
                try:
                    field_name, note_id = key.split('-')
                    
                    # 1. Récupérer l'objet Note spécifique
                    note = Note.objects.get(pk=note_id, eleve=eleve, semestre=semestre)
                    
                    # 2. Nettoyer la valeur (convertir en float ou None si vide/erreur)
                    try:
                        clean_value = float(value)
                        # Assurer que la valeur est dans les bornes (0-20)
                        if not 0 <= clean_value <= 20:
                             clean_value = None # Ignorer les valeurs hors bornes
                    except ValueError:
                        clean_value = None

                    # 3. Mettre à jour l'attribut
                    if field_name in ['inter1', 'inter2', 'inter3', 'inter4', 'devoir1', 'devoir2']:
                        setattr(note, field_name, clean_value)
                        note.save()
                        
                except Exception:
                    # Ignorer les erreurs de parsing ou d'objet non trouvé
                    continue 

        # Redirection après POST pour éviter la soumission multiple
        return redirect('eleves:bulletin', code_eleve=code_eleve)


    # =======================================================
    # PRÉPARATION DES DONNÉES (MÉTHODE GET / Après POST)
    # =======================================================
    
    # NOTE: Ceci doit se faire localement avant déploiement si vous utilisez SQLite sur Vercel!
    # 1. Assurer que les objets Note existent pour toutes les matières de la classe
    
    nom_classe = getattr(eleve, 'classe', 'CLASSE_INCONNUE') # Assurez-vous que le champ est 'classe'
    matieres_requises = MATIERES_PAR_CLASSE.get(nom_classe, [])
    
    for nom_matiere in matieres_requises:
        # Tente de récupérer ou de créer Matiere (lecture)
        matiere, _ = Matiere.objects.get_or_create(nom=nom_matiere) 
        
        # Tente de récupérer ou de créer la Note (lecture)
        # Note: Si cette opération est effectuée pour la première fois sur Vercel, elle échouera
        # avec 'readonly database'. Elle DOIT être faite en local.
        Note.objects.get_or_create(
            eleve=eleve,
            semestre=semestre,
            matiere=matiere,
            defaults={'inter1': None} # Définit des valeurs initiales si l'objet est créé
        )

    # 2. Récupérer toutes les notes nécessaires (maintenant potentiellement créées/mises à jour)
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
    }
    return render(request, 'eleves/bulletin.html', context)