# import_eleves.py (version finale)
from eleves.models import Eleves, Classe, ImportElevesFile

def importer_eleves():
    # Prend le tout dernier fichier uploadé
    dernier = ImportElevesFile.objects.order_by('-date_upload').last()
    if not dernier:
        print("Aucun fichier uploadé")
        return

    import csv
    import os
    chemin = dernier.fichier.path  # ou .url si tu utilises Cloudinary/S3 plus tard

    Eleves.objects.all().delete()
    Classe.objects.all().delete()

    with open(chemin, 'r', encoding='utf-8') as f:
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
    print(f"{Eleves.objects.count()} élèves importés avec succès !")