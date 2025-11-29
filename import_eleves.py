import os
import sys
import django
import csv

# --- 1. CONFIGURATION DE L'ENVIRONNEMENT DJANGO ---

# Permet à Python de trouver le répertoire de configuration (là où est manage.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Configure le module de réglages de Django. (Changez 'sjcj_site' si le nom est différent)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings') 

# Initialise l'environnement Django.
django.setup() 

# --- 2. IMPORTS DES MODÈLES (Après django.setup()) ---
from eleves.models import Eleves, Classe 

# --- 3. EXÉCUTION DU SCRIPT D'IMPORTATION ---

print("--------------------------------------------------")
print("🚀 Début du processus de mise à jour des élèves.")
print("--------------------------------------------------")

# Étape A : Suppression des anciennes données (VIDER LA TABLE)
try:
    count_eleves_deleted, _ = Eleves.objects.all().delete()
    print(f"✅ Anciens élèves supprimés : {count_eleves_deleted}")
    # ATTENTION : Si vous voulez aussi supprimer toutes les classes, décommentez la ligne ci-dessous :
    # count_classes_deleted, _ = Classe.objects.all().delete()
    # print(f"✅ Anciennes classes supprimées : {count_classes_deleted}")

except Exception as e:
    print(f"❌ ERREUR lors de la suppression des anciennes données : {e}")
    sys.exit(1) # Arrête le script si la suppression échoue

# Étape B : Lecture et Importation du nouveau CSV
nombre_eleves_traites = 0

print("📚 Début de l'importation du nouveau fichier 'eleves_import.csv'...")

try:
    with open('eleves_import.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 1. Gère la clé étrangère (Classe)
            classe_obj, created = Classe.objects.get_or_create(nom=row['classe'])
            
            # 2. Crée ou met à jour l'élève
            Eleves.objects.update_or_create(
                code_eleve=row['code_eleve'], # Clé pour identifier l'élève
                defaults={
                    'prenom': row['prenom'],
                    'nom': row['nom'],
                    'classe': classe_obj 
                }
            )
            nombre_eleves_traites += 1

    print("--------------------------------------------------")
    print(f"🎉 SUCCÈS ! {nombre_eleves_traites} élèves ont été importés ou mis à jour.")
    print("--------------------------------------------------")

except FileNotFoundError:
    print("\n❌ ERREUR : Le fichier 'eleves_import.csv' est introuvable. Placez-le à côté de 'manage.py'.")
except KeyError as e:
    print(f"\n❌ ERREUR : Colonne manquante. Vérifiez la présence de la colonne {e} dans votre CSV.")
except Exception as e:
    print(f"\n❌ ERREUR fatale durant l'importation : {e}")