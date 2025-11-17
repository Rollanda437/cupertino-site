from django import forms
from .models import Commentaire
from .models import Avis
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['nom_parent', 'commentaire']
        widgets = {
            'nom_parent': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Votre nom(optionnel)"}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Laissez un commentaire...", 'rows': 3}),
        }
class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['titre', 'contenu']  # Ajustez selon vos champs