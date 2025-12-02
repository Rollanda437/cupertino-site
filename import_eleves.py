# import_eleves.py

import os
import csv
import django
from eleves.models import Eleves, Classe, ListeEleves

# --- 1. Initialisation de l'Environnement Django ---
# Indique à Django le chemin de votre fichier settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
django.setup()
# ----------------------------------------------------


def importer_dernier_csv():
    """
    Récupère le fichier CSV le plus récent de la table ListeEleves,
    efface les données existantes (Eleves et Classe) et importe les nouvelles.
    """
    try:
        # Récupère le fichier le plus récent (si votre modèle a un ordering basé sur la date)
        dernier = ListeEleves.objects.first()  
    except Exception as e:
        # Gérer le cas où la base de données est vide ou la table n'existe pas encore
        print(f"Erreur lors de l'accès à ListeEleves : {e}")
        return

    if not dernier:
        print("Aucun fichier d'élèves uploadé dans la base de données. Opération annulée.")
        return

    # --- Nettoyage des anciennes données ---
    Eleves.objects.all().delete()
    Classe.objects.all().delete()
    print("Anciennes données élèves et classes supprimées.")

    # --- Lecture et Importation du CSV ---
    # Utilisez dernier.fichier.path qui est le chemin d'accès au fichier sur le disque
    try:
        with open(dernier.fichier.path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            lignes_importe = 0
            
            for row in reader:
                # 1. Créer ou récupérer la classe
                classe_nom = row.get('classe', '').strip().upper()
                if not classe_nom:
                    # Sauter les lignes sans nom de classe pour éviter une erreur
                    continue 

                classe, created = Classe.objects.get_or_create(nom=classe_nom)
                
                # 2. Mettre à jour ou créer l'élève
                Eleves.objects.update_or_create(
                    code_eleves=row.get('code_eleves', '').strip(),
                    defaults={
                        'prenom': row.get('prenom', '').strip().title(),
                        'nom': row.get('nom', '').strip().upper(),
                        'classe': classe,
                    }
                )
                lignes_importe += 1
                
        print(f"✅ {Eleves.objects.count()} élèves importés (à partir de {lignes_importe} lignes traitées) !")
        
    except FileNotFoundError:
        print(f"Erreur : Le fichier CSV est introuvable au chemin : {dernier.fichier.path}")
    except KeyError as e:
        print(f"Erreur : Colonne manquante dans le CSV : {e}. Vérifiez les en-têtes (code_eleves, prenom, nom, classe).")
    except Exception as e:
        print(f"Une erreur inattendue est survenue pendant l'importation : {e}")


# --- 2. Exécution du script ---
if __name__ == "__main__":
    importer_dernier_csv()