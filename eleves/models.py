from django.db import models

# Create your models here.
class Eleves(models.Model):
    code_eleve = models.CharField(max_length=20,unique = True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    classe = models.CharField(max_length=20)
    nb_retard = models.IntegerField(default=0)
    nb_absence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.code_eleve})"
# === REMPLACE tout le bas de ton models.py par ÇA ===

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    coefficient = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nom


class Semestre(models.Model):
    NOM_CHOICES = [('S1', '1er Semestre'), ('S2', '2ème Semestre')]
    nom = models.CharField(max_length=2, choices=NOM_CHOICES)
    annee_scolaire = models.CharField(max_length=9, default="2024-2025")

    class Meta:
        unique_together = ('nom', 'annee_scolaire')

    def __str__(self):
        return f"{self.get_nom_display()} {self.annee_scolaire}"


class Note(models.Model):
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    appreciation = models.TextField(blank=True)

    class Meta:
        unique_together = ('eleve', 'matiere', 'semestre')

    def __str__(self):
        return f"{self.eleve} - {self.matiere} ({self.semestre}) : {self.note}"

