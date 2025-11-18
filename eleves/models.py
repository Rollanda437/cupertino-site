from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Eleves(models.Model):
    code_eleve = models.CharField(max_length=20, unique=True, verbose_name="Code élève")
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    classe = models.CharField(max_length=20)
    nb_retard = models.PositiveIntegerField(default=0)
    nb_absence = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.classe}"

    class Meta:
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"
        ordering = ['nom', 'prenom']


class Matiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    coefficient = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Matière"
        ordering = ['nom']


class Semestre(models.Model):
    NOM_CHOICES = [('S1', '1er Semestre'), ('S2', '2ème Semestre')]
    nom = models.CharField(max_length=2, choices=NOM_CHOICES)
    annee_scolaire = models.CharField(max_length=9, default="2025-2026")

    class Meta:
        unique_together = ('nom', 'annee_scolaire')

    def __str__(self):
        return f"{self.get_nom_display()} {self.annee_scolaire}"


class Note(models.Model):
    eleve = models.ForeignKey(Eleves, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)

    # === 4 INTERROGATIONS ===
    inter1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    inter2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    inter3 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    inter4 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])

    # === 2 DEVOIRS ===
    devoir1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    devoir2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])

    # === APPRÉCIATION À LA FIN (comme sur les vrais bulletins) ===
    appreciation = models.TextField(blank=True, verbose_name="Appréciation du professeur")

    class Meta:
        unique_together = ('eleve', 'matiere', 'semestre')
        verbose_name = "Bulletin de notes"

    # Moyennes automatiques
    def moyenne_interrogations(self):
        notes = [n for n in [self.inter1, self.inter2, self.inter3, self.inter4] if n is not None]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_devoirs(self):
        notes = [n for n in [self.devoir1, self.devoir2] if n is not None]
        return round(sum(notes)/len(notes), 2) if notes else None

    def moyenne_semestre(self):
        inter = self.moyenne_interrogations() or 0
        devoir = self.moyenne_devoirs() or 0
        return round((inter + 2 * devoir) / 3, 2)  # Devoir coef 2

    def __str__(self):
        return f"{self.eleve} - {self.matiere} ({self.semestre})"