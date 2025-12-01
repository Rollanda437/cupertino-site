# avis/views.py

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .forms import CommentaireForm
# ⚠️ Importez les fonctions de l'API Sheets (assurez-vous que le chemin est correct)
from sheets_api import get_data_from_sheet, authenticate 
# Si sheets_api est à la racine, vous devrez peut-être utiliser 'gestion_ecole' (le nom de votre projet principal)
# OU si le script est dans un package, adaptez l'importation.
# sheets_api.py

CLIENT_SECRET_FILE = 'client_secret.json' 
# ⬇️ Collez l'ID ici ⬇️
GOOGLE_SHEET_ID = '1iaegOAee9aA-nNyozgDnROwQPS3EJw9qoYhpeKd0TAM'
# Pour la gestion du formulaire, nous allons SIMPLEMENT utiliser un formulaire standard 
# pour capturer les données, car nous n'écrivons plus dans le modèle Avis.
from .forms import AvisForm 
# Nous n'importons plus Avis, Commentaire ou CommentaireForm car ils sont gérés par Sheets/API.


# 🏠 Page d’accueil des avis
def index_avis(request):
    return render(request, "avis/index.html")


# 📰 Liste + ajout d’un avis
def liste_avis(request):
    # 1. 🔍 Lire les avis depuis Google Sheets
    # Assurez-vous que votre onglet s'appelle EXACTEMENT "Avis_DB"
    avis_liste = get_data_from_sheet("Avis_DB")
    
    if request.method == "POST":
        form = AvisForm(request.POST)
        
        if form.is_valid():
            # 2. ✍️ Écrire le nouvel avis dans Google Sheets
            
            # Récupérer les données nettoyées
            titre = form.cleaned_data['titre']
            contenu = form.cleaned_data['contenu']
            
            # Créer la ligne de données à ajouter au format attendu par Sheets
            # Note : Assurez-vous que les colonnes de votre feuille sont: 'titre', 'contenu', 'date_publication'
            new_row = [
                titre, 
                contenu, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Format de date pour Google Sheets
            ]
            
            try:
                gc = authenticate()
                if gc:
                    sh = gc.open_by_key("1iaegOAee9aA-nNyozgDnROwQPS3EJw9qoYhpeKd0TAM")
                    worksheet = sh.worksheet("Avis_DB")
                    # Ajoute la nouvelle ligne à la feuille
                    worksheet.append_row(new_row)
                    
            except Exception as e:
                # Gérer l'erreur de l'API Sheets (loggez-la si possible)
                print(f"Erreur lors de l'ajout de l'avis à Sheets: {e}") 
                pass # Continue sans erreur fatale, mais l'avis ne sera pas enregistré
            
            return redirect('avis:liste_avis') # Rediriger après l'ajout
    else:
        form = AvisForm()

    return render(request, 'avis/liste_avis.html', {
        'avis_liste': avis_liste,
        'form': form
    })


# 📄 Détail d’un avis
# Cette vue DOIT être revue car vous ne pouvez plus utiliser get_object_or_404() de Django
# à moins que vous ne recréiez cette logique de recherche manuellement dans Sheets.

# 📄 Détail d’un avis
def detail_avis(request, avis_id):
    # --- 1. Récupérer l'avis ---
    avis_data = get_data_from_sheet("Avis_DB")
    # Tenter de trouver l'avis correspondant (en utilisant l'ID que vous avez défini dans Sheets)
    avis_detail = next((item for item in avis_data if str(item.get('id')) == str(avis_id)), None)

    if avis_detail is None:
        from django.http import Http404
        raise Http404("Avis non trouvé")

    # --- 2. Récupérer et Filtrer les commentaires ---
    
    # Récupérer TOUS les commentaires depuis la nouvelle feuille
    all_commentaires = get_data_from_sheet("Commentaires_DB") 

    # Filtrer les commentaires manuellement pour ne garder que ceux de cet avis
    commentaires = [
        com for com in all_commentaires if str(com.get('avis_id')) == str(avis_id)
    ]
    
    # Optionnel: Trier par date
    # Si les dates sont au format ISO (AAAA-MM-JJ), Python peut les trier.
    try:
        commentaires.sort(key=lambda x: datetime.strptime(x['date_publication'], "%Y-%m-%d %H:%M:%S"), reverse=True)
    except Exception:
        pass # Si le format de date est incorrect, on ne trie pas.

    return render(request, 'avis/detail_avis.html', {
        'avis_detail': avis_detail,
        'commentaires': commentaires
    })


# 💬 Ajouter un commentaire
# Cette fonctionnalité doit être entièrement réécrite pour écrire dans une feuille "Commentaires_DB"
# Elle est laissée vide car elle n'est pas supportée par l'approche Sheets.
# 💬 Ajouter un commentaire
def ajouter_commentaire(request, avis_id):
    # Nous avons besoin de l'avis pour la redirection et pour son ID
    # ... (le code pour récupérer l'avis_detail comme dans detail_avis) ...

    if request.method == "POST":
        form = CommentaireForm(request.POST) # Utiliser un formulaire Django pour la validation
        
        if form.is_valid():
            # Préparer la ligne pour Google Sheets
            new_row = [
                avis_id, # C'est le lien vers l'avis
                form.cleaned_data['contenu'], 
                form.cleaned_data['auteur'], # Si votre formulaire a un champ 'auteur'
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]

            try:
                gc = authenticate()
                if gc:
                    sh = gc.open_by_key("1iaegOAee9aA-nNyozgDnROwQPS3EJw9qoYhpeKd0TAM")
                    worksheet = sh.worksheet("Commentaires_DB")
                    worksheet.append_row(new_row)
                    
            except Exception as e:
                print(f"Erreur lors de l'ajout du commentaire à Sheets: {e}") 
            
            return redirect('avis:detail_avis', avis_id=avis_id) # Redirection vers la page de détail
    else:
        form = CommentaireForm()

    return render(request, 'avis/ajouter_commentaire.html', {
        'form': form,
        'avis_id': avis_id # Passer l'ID pour le formulaire
    })