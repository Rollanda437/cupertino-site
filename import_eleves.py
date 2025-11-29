import os
import django
import csv

# --- AJOUTER CES LIGNES ---
# 1. Configurer l'environnement de votre projet Django
# Remplacez 'votre_projet.settings' par le chemin réel de votre fichier settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings') 
django.setup()

# 2. Importer les modèles après django.setup()
from eleves.models import Eleves, Classe 
# -------------------------

nombre_eleves_traites = 0

with open('eleves_import.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Récupère ou crée l'objet Classe
        classe_obj, created = Classe.objects.get_or_create(nom=row['classe'])
        
        # Met à jour ou crée l'objet Eleves
        Eleves.objects.update_or_create(
            code_eleve=row['code_eleve'],
            defaults={
                'prenom': row['prenom'],
                'nom': row['nom'],
                'classe': classe_obj # Utiliser l'objet Classe récupéré/créé
            }
        )
        nombre_eleves_traites += 1

print(f"{nombre_eleves_traites} élèves importés ou mis à jour !")