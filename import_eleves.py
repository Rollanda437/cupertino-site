# import_eleves.py
import csv
from eleves.models import Eleves, Classe, ListeEleves

def importer_dernier_csv():
    dernier = ListeEleves.objects.first()  # le plus récent grâce à l'ordering
    if not dernier:
        print("Aucun fichier uploadé")
        return

    Eleves.objects.all().delete()
    Classe.objects.all().delete()

    with open(dernier.fichier.path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            classe, _ = Classe.objects.get_or_create(nom=row['classe'].strip().upper())
            Eleves.objects.update_or_create(
                code_eleves=row['code_eleves'].strip(),
                defaults={
                    'prenom': row['prenom'].strip().title(),
                    'nom': row['nom'].strip().upper(),
                    'classe': classe,
                }
            )
    print(f"{Eleves.objects.count()} élèves importés !")