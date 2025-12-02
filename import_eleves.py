# import_eleves.py (MODIFICATION)

import os
import csv
import django
from eleves.models import Eleves, Classe

# Utilisez os.path.join pour construire le chemin vers le fichier
# BASE_DIR est nécessaire pour trouver le fichier par rapport à la racine du projet
from django.conf import settings
CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'eleves_import.csv') 
# Vous pourriez aussi simplement utiliser CSV_FILE_PATH = 'import_eleves.csv' si le script est exécuté depuis la racine


def importer_dernier_csv():
    """Importe les élèves directement depuis 'eleves_import.csv'."""

    # ⚠️ Retirez la ligne qui cherche le fichier dans la base de données ListeEleves :
    # dernier = ListeEleves.objects.first() 
    # if not dernier:
    #     print("Aucun fichier uploadé")
    #     return
    
    Eleves.objects.all().delete()
    Classe.objects.all().delete()
    print("Anciennes données élèves et classes supprimées.")

    # --- Lecture du fichier CSV fixe ---
    try:
        # Utilisez le chemin du fichier que vous avez committé
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # ... (Le reste de la logique d'importation reste inchangé) ...
            
            # ... (Copiez ici toute la boucle 'for row in reader:') ...
            for row in reader:
                classe_nom = row.get('classe', '').strip().upper()
                if not classe_nom: continue 

                classe, created = Classe.objects.get_or_create(nom=classe_nom)
                
                Eleves.objects.update_or_create(
                    code_eleves=row.get('code_eleves', '').strip(),
                    defaults={
                        'prenom': row.get('prenom', '').strip().title(),
                        'nom': row.get('nom', '').strip().upper(),
                        'classe': classe,
                    }
                )
        print(f"✅ {Eleves.objects.count()} élèves importés depuis import_eleves.csv!")
        
    except FileNotFoundError:
        print(f"Erreur : Le fichier CSV est introuvable au chemin : {CSV_FILE_PATH}. Assurez-vous qu'il est bien committé.")
    except KeyError as e:
        print(f"Erreur : Colonne manquante dans le CSV : {e}.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")


if __name__ == "__main__":
    importer_dernier_csv()