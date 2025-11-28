import csv
from eleves.models import Eleves, Classe

with open('eleves_import.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        classe, created = Classe.objects.get_or_create(nom=row['classe'])
        Eleves.objects.update_or_create(
            code_eleve=row['code_eleve'],
            defaults={
                'prenom': row['prenom'],
                'nom': row['nom'],
                'classe': classe
            }
        )
print("112 élèves importés !")