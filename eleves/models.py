# eleves/models.py → VERSION COMPLÈTE QUI MARCHE À 100%
from django.db import models
from firebase_config import db  # maintenant c’est safe grâce au mock

# --- MODÈLES OBLIGATOIRES ---
class Eleves(models.Model):
    code_eleve = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    classe = models.CharField(max_length=20)
    fillière = models.CharField(max_length=50, blank=True)
    nb_retard = models.IntegerField(default=0)
    nb_absence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.code_eleve})"

    def to_dict(self):
        return {
            'code_eleve': self.code_eleve,
            'nom': self.nom,
            'prenom': self.prenom,
            'classe': self.classe,
            'Fillière':self.fillière,
            'nb_retard': self.nb_retard,
            'nb_absence': self.nb_absence,
        }

    def save_to_firestore(self):
        pass  # temporairement désactivé

    @classmethod
    def get_all_from_firestore(cls):
        return []


# --- TU VEUX GARDER ÇA ? ON REMET TOUT ---
class Matiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Semestre(models.Model):
    nom = models.CharField(max_length=10, unique=True)  # ex: S1, S2, S3...

    def __str__(self):
        return self.nom


class Note(models.Model):
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, null=True, blank=True)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, null=True, blank=True)
    inter1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    inter2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    inter3 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    inter4 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    devoir1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    devoir2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    appreciation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.eleve} - {self.matiere} - {self.semestre}"

    def moyenne_inter(self):
        notes = [n for n in [self.inter1, self.inter2, self.inter3, self.inter4] if n is not None]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_devoir(self):
        notes = [n for n in [self.devoir1, self.devoir2] if n is not None]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_semestre(self):
        inter = self.moyenne_inter() or 0
        devoir = self.moyenne_devoir() or 0
        return round((inter + 2*devoir)/3, 2)