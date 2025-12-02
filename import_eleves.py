import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from datetime import datetime
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
# Définissez le nom du modèle et du fichier CSV
MODEL_NAME = 'Eleves'
CSV_FILE_NAME = 'eleves_import.csv'

class Command(BaseCommand):
    # Ceci est le texte qui s'affiche lorsque l'utilisateur tape : python manage.py help import_eleves
    help = f'Importe les données des élèves à partir du fichier {CSV_FILE_NAME} et les charge dans le modèle {MODEL_NAME}.'

    def handle(self, *args, **options):
        # Cherche le fichier CSV à la racine du projet
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        csv_path = base_dir / CSV_FILE_NAME

        if not csv_path.exists():
            raise CommandError(f'Fichier CSV non trouvé: {csv_path}. Assurez-vous que le fichier est à la racine du projet.')

        try:
            # Récupère le modèle 'Eleves' de l'application 'eleves'
            Eleves = apps.get_model('eleves', MODEL_NAME)
        except LookupError:
            raise CommandError(f"Le modèle '{MODEL_NAME}' n'a pas été trouvé dans l'application 'eleves'. Vérifiez eleves/models.py.")

        self.stdout.write(self.style.SUCCESS(f"Démarrage de l'importation depuis {CSV_FILE_NAME}..."))
        
        rows_imported = 0
        rows_skipped = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Assurez-vous que la ligne d'en-tête du CSV correspond à cette logique
                    code_eleve = row.get('code_eleve')
                    
                    if not code_eleve:
                        self.stdout.write(self.style.WARNING(f"Ligne ignorée : 'code_eleve' manquant."))
                        rows_skipped += 1
                        continue

                    # Tentative de convertir la date de naissance (format YYYY-MM-DD)
                    date_naissance_str = row.get('date_naissance')
                    date_naissance_obj = None
                    if date_naissance_str:
                        try:
                            date_naissance_obj = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
                        except ValueError:
                            self.stdout.write(self.style.ERROR(f"Erreur de format de date pour {code_eleve}. Format attendu : YYYY-MM-DD."))
                            rows_skipped += 1
                            continue

                    try:
                        # Crée ou met à jour l'élève (si le code existe déjà, il le met à jour)
                        eleve, created = Eleves.objects.update_or_create(
                            code_eleve=code_eleve,
                            defaults={
                                'nom': row.get('nom'),
                                'prenom': row.get('prenom'),
                                'classe': row.get('classe'),
                                'date_naissance': date_naissance_obj,
                                # Ajoutez d'autres champs ici
                            }
                        )
                        rows_imported += 1
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Créé : {eleve.nom} {eleve.prenom} ({eleve.code_eleve})"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Mis à jour : {eleve.nom} {eleve.prenom} ({eleve.code_eleve})"))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erreur lors de l'enregistrement de l'élève {code_eleve}: {e}"))
                        rows_skipped += 1

            self.stdout.write(self.style.SUCCESS(f"\n--- IMPORTATION TERMINÉE ---"))
            self.stdout.write(self.style.SUCCESS(f"{rows_imported} élèves importés ou mis à jour."))
            if rows_skipped > 0:
                self.stdout.write(self.style.WARNING(f"{rows_skipped} lignes ignorées à cause d'erreurs."))

        except Exception as e:
            raise CommandError(f"Une erreur inattendue est survenue : {e}")