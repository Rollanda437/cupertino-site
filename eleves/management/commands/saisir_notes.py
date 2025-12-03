from django.core.management.base import BaseCommand
from eleves.models import Eleves, Semestre, Matiere, Note 

class Command(BaseCommand):
    help = 'Saisie interactive des notes des élèves directement dans la base de données.'

    def _get_float_input(self, prompt):
        """Fonction utilitaire pour gérer la saisie de nombres (virgule ou point)."""
        while True:
            note_str = input(prompt).strip().replace(',', '.')
            if not note_str:
                return None
            if note_str.upper() == 'Q':
                raise KeyboardInterrupt # Permet de sortir de la boucle principale
            try:
                float_value = float(note_str)
                if 0 <= float_value <= 20:
                    return float_value
                else:
                    self.stdout.write(self.style.ERROR("La note doit être comprise entre 0 et 20."))
            except ValueError:
                self.stdout.write(self.style.ERROR("Erreur : La valeur doit être un nombre."))

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Mode de Saisie Interactive des Notes ---"))
        self.stdout.write("Tapez 'q' ou laissez vide et tapez Entrée pour quitter la saisie à tout moment.")
        self.stdout.write("-" * 50)
        
        while True:
            try:
                # 1. SAISIE ET VÉRIFICATION DE L'ÉLÈVE
                code_eleve = input("Code de l'élève : ").strip().upper()
                if not code_eleve or code_eleve == 'Q': break
                
                eleve = Eleves.objects.get(code_eleve=code_eleve)
                self.stdout.write(f"-> Élève trouvé : {eleve.prenom} {eleve.nom} ({eleve.classe.nom})")
            
                # 2. SAISIE ET VÉRIFICATION DU SEMESTRE/MATIÈRE
                semestre_nom = input("Nom du semestre (ex: S1) : ").strip()
                if not semestre_nom or semestre_nom.upper() == 'Q': break
                semestre = Semestre.objects.get(nom=semestre_nom)
                
                matiere_nom = input("Nom de la matière (ex: MATH) : ").strip()
                if not matiere_nom or matiere_nom.upper() == 'Q': break
                matiere, _ = Matiere.objects.get_or_create(nom=matiere_nom)
                
                # 3. SAISIE DES NOTES
                self.stdout.write(self.style.NOTICE("Saisie des notes (entrez 'q' pour annuler) :"))
                
                notes_data = {}
                notes_data['inter1'] = self._get_float_input("  Note inter1 : ")
                notes_data['inter2'] = self._get_float_input("  Note inter2 : ")
                notes_data['inter3'] = self._get_float_input("  Note inter3 : ")
                notes_data['inter4'] = self._get_float_input("  Note inter4 : ")
                notes_data['devoir1'] = self._get_float_input("  Note devoir1 : ")
                notes_data['devoir2'] = self._get_float_input("  Note devoir2 : ")
                notes_data['appreciation'] = input("  Appréciation (Optionnel) : ").strip()
                
                # 4. ENREGISTREMENT/MISE À JOUR
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