# import_eleves.py

import os
import csv
import django
from django.conf import settings # Importation OK

# --- INITIALISATION CRITIQUE DE DJANGO (DOIT ÊTRE FAIT AVANT LES IMPORTS DE MODÈLES) ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
django.setup() 
# -------------------------------------------------------------------------------------

# 1. Importation des Modèles (MAINTENANT que Django est configuré)
from eleves.models import Eleves, Classe 

# 2. Définition du chemin d'accès au fichier (MAINTENANT que settings est disponible)
CSV_FILE_NAME = 'eleves_import.csv'
CSV_FILE_PATH = os.path.join(settings.BASE_DIR, CSV_FILE_NAME) 


def importer_dernier_csv():
    """Importe les élèves directement depuis 'eleves_import.csv'."""
    
    # Sécurité : Supprime d'abord les anciennes données pour garantir une base propre
    Eleves.objects.all().delete()
    Classe.objects.all().delete()
    print("Anciennes données élèves et classes supprimées.")

    # --- Lecture du fichier CSV committé ---
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes_importe = 0
            
            for row in reader:
                classe_nom = row.get('classe', '').strip().upper()
                if not classe_nom: continue 

                # get_or_create pour la table Classe
                classe, created = Classe.objects.get_or_create(nom=classe_nom)
                
                # update_or_create pour la table Eleves
                Eleves.objects.update_or_create(
                        # Le premier argument doit être le nom du champ du modèle :
                        code_eleve=row.get('code_eleves', '').strip(), # ✅ Utilise code_eleve
                        defaults={
                            'prenom': row.get('prenom', '').strip().title(),
                            'nom': row.get('nom', '').strip().upper(),
                            'classe': classe,
                        }
                    )
            lignes_importe += 1
        
        # ⚠️ Correction du nom du fichier dans le message de succès (eleves_import.csv)
        print(f"✅ {Eleves.objects.count()} élèves importés depuis {CSV_FILE_NAME}!") 
        
    except FileNotFoundError:
        print(f"Erreur : Le fichier CSV est introuvable au chemin : {CSV_FILE_PATH}. Assurez-vous qu'il est bien committé.")
    except KeyError as e:
        print(f"Erreur : Colonne manquante dans le CSV : {e}.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")


if __name__ == "__main__":
    importer_dernier_csv()