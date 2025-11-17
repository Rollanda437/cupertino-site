# avis/models.py
from django.db import models

class Avis(models.Model):
    titre = models.CharField(max_length=100)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    classe_concernee = models.CharField(max_length=20, blank=True, null=True)  # ex: "6ème A"

    class Meta:
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    avis = models.ForeignKey(Avis, on_delete=models.CASCADE, related_name='commentaires')
    nom_parent = models.CharField(max_length=50, blank=True)
    commentaire = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_publication']

    def __str__(self):
        return f"Commentaire de {self.nom_parent or 'Anonyme'}"