from django.db import models

# Create your models here.
class Evenement(models.Model):
    TYPE_CHOICE = [
        ('vacances','Vacances'),
        ('examen','Examens'),
        ('reunion','Reunions'),
        ('autre','Autres'),
    ]
    titre = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_evenement = models.CharField(max_length=20, choices=TYPE_CHOICE)
    
    def __str__(self):
        return f"{self.titre}"({self.type_evenement})