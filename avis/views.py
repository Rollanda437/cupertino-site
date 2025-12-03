from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Avis, Commentaire
from .forms import AvisForm, CommentaireForm


# 🏠 Page d’accueil des avis
def index_avis(request):
    return render(request, "avis/index.html")


# 📰 Liste + ajout d’un avis
def liste_avis(request):
    avis_liste = Avis.objects.order_by('-date_publication')

    if request.method == "POST":
        form = AvisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_avis')
    else:
        form = AvisForm()

    return render(request, 'avis/liste_avis.html', {
        'avis_liste': avis_liste,
        'form': form
    })


# 📄 Détail d’un avis
def detail_avis(request, avis_id):
    avis_detail = get_object_or_404(Avis, id=avis_id)
    commentaires = avis_detail.commentaires.order_by('-date_publication')  # avec ton related_name
    return render(request, 'avis/detail_avis.html', {
        'avis_detail': avis_detail,
        'commentaires': commentaires  # on passe explicitement les commentaires
    })


# 💬 Ajouter un commentaire
def ajouter_commentaire(request, avis_id):
    avis = get_object_or_404(Avis, id=avis_id)

    if request.method == "POST":
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)  # ← c'est la variable
            Commentaire.avis = avis
            Commentaire.save()
            return redirect('avis:detail_avis', avis_id=avis.id)
    else:
        form = CommentaireForm()

    return render(request, 'avis/ajouter_commentaire.html', {
        'form': form,
        'avis': avis
    })
