# eleves/models.py → VERSION FINALE QUI MARCHE À 100% (2025)
from django.db import models


class Classe(models.Model):
    nom = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Classes"

class ListeEleves(models.Model):
    fichier = models.FileField(upload_to='liste/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Liste du {self.uploaded_at.strftime('%d/%m %Y %H:%M')}"
class ListeEleves(models.Model):
    fichier = models.FileField(upload_to='liste/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Listes des élèves"

    def __str__(self):
        return f"Liste uploadée le {self.uploaded_at.strftime('%d/%m/%Y %H:%M')}"
class Eleves(models.Model):
    code_eleve = models.CharField("Code élève", max_length=20, unique=True, primary_key=True)
    nom = models.CharField("Nom", max_length=50)
    prenom = models.CharField("Prénom", max_length=50)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, verbose_name="Classe")
    nb_retard = models.IntegerField("Retards", default=0)
    nb_absence = models.IntegerField("Absences", default=0)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.code_eleve})"

    class Meta:
        verbose_name_plural = "Élèves"
        ordering = ['nom', 'prenom']


class Matiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Matières"


class Semestre(models.Model):
    nom = models.CharField(max_length=10, unique=True)  # S1, S2, S3...

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Semestres"


class Note(models.Model):
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    inter1 = models.DecimalField("Inter 1", max_digits=4, decimal_places=2, null=True, blank=True)
    inter2 = models.DecimalField("Inter 2", max_digits=4, decimal_places=2, null=True, blank=True)
    inter3 = models.DecimalField("Inter 3", max_digits=4, decimal_places=2, null=True, blank=True)
    inter4 = models.DecimalField("Inter 4", max_digits=4, decimal_places=2, null=True, blank=True)
    devoir1 = models.DecimalField("Devoir 1", max_digits=4, decimal_places=2, null=True, blank=True)
    devoir2 = models.DecimalField("Devoir 2", max_digits=4, decimal_places=2, null=True, blank=True)
    appreciation = models.TextField("Appréciation", blank=True)

    def moyenne_inter(self):
        notes = [n for n in [self.inter1, self.inter2, self.inter3, self.inter4] if n]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_devoir(self):
        notes = [n for n in [self.devoir1, self.devoir2] if n]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_semestre(self):
        inter = self.moyenne_inter() or 0
        devoir = self.moyenne_devoir() or 0
        return round((inter + 2 * devoir) / 3, 2)

    def __str__(self):
        return f"{self.eleve} - {self.matiere} ({self.semestre})"

    class Meta:
        unique_together = ('eleve', 'matiere', 'semestre')
        verbose_name_plural = "Notes"