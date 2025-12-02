import os
import csv
import django
from django.conf import settings
from django.db import transaction

# --- INITIALISATION CRITIQUE DE DJANGO ---
# Doit être fait avant d'importer les modèles ou de faire des opérations de base de données.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
django.setup() 
# ----------------------------------------

# 1. Importation des Modèles
from eleves.models import Eleves, Classe 

# 2. Définition du chemin d'accès au fichier
CSV_FILE_NAME = 'eleves_import.csv'
CSV_FILE_PATH = os.path.join(settings.BASE_DIR, CSV_FILE_NAME) 


def importer_dernier_csv():
    """
    Importe les élèves en utilisant l'approche "bulk_create" pour une meilleure performance.
    Crée d'abord toutes les classes nécessaires, puis tous les élèves.
    """
    
    # Sécurité : Supprime d'abord les anciennes données pour garantir une base propre
    # Utilisation d'une transaction pour garantir l'atomicité de la suppression
    try:
        with transaction.atomic():
            Eleves.objects.all().delete()
            Classe.objects.all().delete()
            print("Anciennes données élèves et classes supprimées.")
    except Exception as e:
        print(f"Erreur lors de la suppression des anciennes données : {e}. Le script s'arrête.")
        return

    eleves_a_creer = []
    classes_noms = set()
    
    # --- ÉTAPE 1: Lecture et Préparation des données ---
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Première passe : Collecter toutes les données et identifier toutes les classes
            all_rows = list(reader)

            for row in all_rows:
                # S'assurer que la ligne n'est pas vide et contient au moins une classe
                if not row or not row.get('classe', '').strip():
                    continue 

                classe_nom = row['classe'].strip().upper()
                classes_noms.add(classe_nom)
            
            print(f"Classes identifiées à créer : {list(classes_noms)}")

            # --- ÉTAPE 2: Création des Classes en Masse ---
            # Crée les objets Classe pour toutes les classes identifiées
            Classe.objects.bulk_create([
                Classe(nom=nom) for nom in classes_noms
            ], ignore_conflicts=True) # ignore_conflicts=True est une bonne pratique

            # Récupérer les objets Classe créés pour les lier aux élèves
            classes_map = {classe.nom: classe for classe in Classe.objects.filter(nom__in=classes_noms)}
            
            # --- ÉTAPE 3: Préparation des Objets Élèves ---
            for row in all_rows:
                if not row or not row.get('classe', '').strip():
                    continue

                classe_nom = row['classe'].strip().upper()
                classe_obj = classes_map.get(classe_nom)

                # Si la classe a été trouvée, préparer l'objet Eleves
                if classe_obj:
                    eleve = Eleves(
                        code_eleve=row.get('code_eleves', '').strip(), 
                        prenom=row.get('prenom', '').strip().title(),
                        nom=row.get('nom', '').strip().upper(),
                        classe=classe_obj,
                    )
                    eleves_a_creer.append(eleve)
                else:
                    print(f"⚠️ Avertissement : Classe '{classe_nom}' introuvable pour l'élève {row.get('nom', 'Inconnu')}. Ligne ignorée.")


        # --- ÉTAPE 4: Création des Élèves en Masse ---
        if eleves_a_creer:
             Eleves.objects.bulk_create(eleves_a_creer, batch_size=500)
             print(f"✅ {len(eleves_a_creer)} élèves créés en masse. {Classe.objects.count()} classes enregistrées.")
        else:
             print("⚠️ Aucune ligne valide trouvée pour l'importation des élèves.")
        
        print(f"✅ Total des élèves importés depuis {CSV_FILE_NAME}: {Eleves.objects.count()}!") 
        
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier CSV est introuvable au chemin : {CSV_FILE_PATH}.")
    except KeyError as e:
        print(f"❌ Erreur : Colonne manquante dans le CSV. Vérifiez que toutes les colonnes sont présentes : {e}.")
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue : {e}")


if __name__ == "__main__":
    importer_dernier_csv()