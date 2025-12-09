from django.core.management.base import BaseCommand
from eleves.models import Eleves, Semestre, Matiere, Note
# Note : Assurez-vous que les champs nb_absence et nb_retard existent dans eleves.models.Eleves

class Command(BaseCommand):
    help = 'Saisie interactive des notes, absences et retards des élèves directement dans la base de données.'

    def _get_float_input(self, prompt):
        """Fonction utilitaire pour gérer la saisie de notes (flottants, 0-20)."""
        while True:
            note_str = input(prompt).strip().replace(',', '.')
            if not note_str:
                return None
            if note_str.upper() == 'Q':
                raise KeyboardInterrupt
            try:
                float_value = float(note_str)
                if 0 <= float_value <= 20:
                    return float_value
                else:
                    self.stdout.write(self.style.ERROR("La note doit être comprise entre 0 et 20."))
            except ValueError:
                self.stdout.write(self.style.ERROR("Erreur : La valeur doit être un nombre."))

    def _get_int_input(self, prompt, current_value=0):
        """Fonction utilitaire pour gérer la saisie d'entiers (Absences/Retards)."""
        while True:
            # Affiche la valeur actuelle dans le prompt pour faciliter la modification
            input_prompt = f"{prompt} (Actuel: {current_value}) : "
            count_str = input(input_prompt).strip()
            
            if not count_str:
                return current_value # Si vide, on garde la valeur actuelle
            if count_str.upper() == 'Q':
                raise KeyboardInterrupt
            try:
                int_value = int(count_str)
                if int_value >= 0:
                    return int_value
                else:
                    self.stdout.write(self.style.ERROR("La valeur doit être un entier positif ou zéro."))
            except ValueError:
                self.stdout.write(self.style.ERROR("Erreur : La valeur doit être un nombre entier."))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Mode de Saisie Interactive ---"))
        self.stdout.write("Tapez 'q' ou laissez vide et tapez Entrée pour quitter la saisie à tout moment.")
        self.stdout.write("-" * 50)
        
        while True:
            try:
                # 1. SAISIE ET VÉRIFICATION DE L'ÉLÈVE
                code_eleve = input("Code de l'élève : ").strip().upper()
                if not code_eleve or code_eleve == 'Q': break
                
                eleve = Eleves.objects.get(code_eleve=code_eleve)
                self.stdout.write(f"-> Élève trouvé : {eleve.prenom} {eleve.nom} ({eleve.classe.nom})")
            
                # 2. SAISIE DES ABSENCES ET RETARDS
                self.stdout.write(self.style.NOTICE("\nSaisie des Absences/Retards (Laissez vide pour conserver la valeur actuelle) :"))
                
                # Récupère les valeurs actuelles avant de demander la saisie
                new_absence = self._get_int_input("  Nombre d'absences", current_value=eleve.nb_absence)
                new_retard = self._get_int_input("  Nombre de retards", current_value=eleve.nb_retard)
                
                # Mise à jour de l'objet Eleves
                if new_absence != eleve.nb_absence or new_retard != eleve.nb_retard:
                    Eleves.objects.filter(pk=eleve.pk).update(
                        nb_absence=new_absence,
                        nb_retard=new_retard
                    )
                    self.stdout.write(self.style.SUCCESS("✅ Succès : Absences/Retards mis à jour."))
                
                self.stdout.write(self.style.NOTICE("-" * 20))
                
                # 3. SAISIE ET VÉRIFICATION DU SEMESTRE/MATIÈRE (POUR LES NOTES)
                semestre_nom = input("Nom du semestre (ex: S1) : ").strip()
                if not semestre_nom or semestre_nom.upper() == 'Q': break
                semestre = Semestre.objects.get(nom=semestre_nom)
                
                matiere_nom = input("Nom de la matière (ex: MATH) : ").strip()
                if not matiere_nom or matiere_nom.upper() == 'Q': break
                matiere, _ = Matiere.objects.get_or_create(nom=matiere_nom)
                
                # 4. SAISIE DES NOTES
                self.stdout.write(self.style.NOTICE("\nSaisie des Notes (entrez 'q' pour annuler) :"))
                
                notes_data = {}
                # Le reste de la saisie des notes reste inchangé
                notes_data['inter1'] = self._get_float_input("  Note inter1 : ")
                notes_data['inter2'] = self._get_float_input("  Note inter2 : ")
                notes_data['inter3'] = self._get_float_input("  Note inter3 : ")
                notes_data['inter4'] = self._get_float_input("  Note inter4 : ")
                notes_data['devoir1'] = self._get_float_input("  Note devoir1 : ")
                notes_data['devoir2'] = self._get_float_input("  Note devoir2 : ")
                notes_data['appreciation'] = input("  Appréciation (Optionnel) : ").strip()
                
                # 5. ENREGISTREMENT/MISE À JOUR DES NOTES
                note, created = Note.objects.update_or_create(
                    eleve=eleve,
                    semestre=semestre,
                    matiere=matiere,
                    defaults={
                        'inter1': notes_data['inter1'],
                        'inter2': notes_data['inter2'],
                        'inter3': notes_data['inter3'],
                        'inter4': notes_data['inter4'],
                        'devoir1': notes_data['devoir1'],
                        'devoir2': notes_data['devoir2'],
                        'appreciation': notes_data['appreciation'],
                    }
                )

                action = "Créée" if created else "Mise à jour"
                self.stdout.write(self.style.SUCCESS(f"✅ Succès : Note ({action}) pour {eleve.code_eleve} en {matiere_nom} ({semestre_nom})."))

            except Eleves.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Erreur : Élève avec le code '{code_eleve}' non trouvé."))
            except Semestre.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Erreur : Semestre '{semestre_nom}' non trouvé."))
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Erreur inattendue : {e}"))
                
            self.stdout.write("-" * 50)
        
        self.stdout.write(self.style.NOTICE("Fin de la saisie interactive. Au revoir."))