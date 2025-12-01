
import os, django, csv
os.environ['DJANGO_SETTINGS_MODULE'] = ('gestion_ecole.settings')
from eleves.models import Eleves, Classe

# Vide tout d'abord
Eleves.objects.all().delete()
Classe.objects.all().delete()

# Importe le nouveau CSV
with open('eleves_import.csv', 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        classe, _ = Classe.objects.get_or_create(nom=row['classe'].strip())
        Eleves.objects.update_or_create(
            code_eleve=row['code_eleve'].strip(),
            defaults={
                'prenom': row['prenom'].strip().title(),
                'nom': row['nom'].strip().upper(),
                'classe': classe
            }
        )

# On compte
print(f"{Eleves.objects.count()} élèves importés avec succès !")