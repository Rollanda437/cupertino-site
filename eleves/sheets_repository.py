# eleves/sheets_repository.py

from sheets_api import get_data_from_sheet # Assurez-vous que le chemin est correct

# --- 1. Classes de Simulation (Simule les objets de modèle Django) ---

class EleveSheet:
    """Simule l'objet Eleves de Django."""
    def __init__(self, data):
        # Assurez-vous que les clés correspondent aux colonnes de Eleves_DB
        self.code_eleve = data.get('code_eleve', '')
        self.nom = data.get('nom', '')
        self.prenom = data.get('prenom', '')
        self.classe = data.get('classe', '')

class MatiereSheet:
    """Simule l'objet Matiere de Django."""
    def __init__(self, nom):
        self.nom = nom # La matière est stockée comme une chaîne dans Notes_DB

class SemestreSheet:
    """Simule l'objet Semestre de Django."""
    def __init__(self, nom):
        self.nom = nom

class NoteSheet:
    """Simule l'objet Note de Django."""
    def __init__(self, data, eleve, semestre):
        # ⚠️ Clé Étrangère simulée
        self.eleve = eleve
        self.semestre = semestre 
        
        # Simule la relation select_related('matiere')
        self.matiere = MatiereSheet(data.get('matiere', '')) 
        
        # Conversion des notes en float (important pour les calculs de votre vue)
        try:
            self.inter1 = float(data.get('inter1', 0)) if data.get('inter1') else None
            self.inter2 = float(data.get('inter2', 0)) if data.get('inter2') else None
            self.inter3 = float(data.get('inter3', 0)) if data.get('inter3') else None
            self.inter4 = float(data.get('inter4', 0)) if data.get('inter4') else None
            self.devoir1 = float(data.get('devoir1', 0)) if data.get('devoir1') else None
            self.devoir2 = float(data.get('devoir2', 0)) if data.get('devoir2') else None
        except ValueError:
            # Gérer le cas où Sheets renvoie du texte non numérique
            self.inter1, self.inter2, self.inter3, self.inter4 = None, None, None, None
            self.devoir1, self.devoir2 = None, None
            
        # Les champs 'moyenne_interrogations', 'moyenne_devoirs', 'moyenne_semestre'
        # seront ajoutés par la vue 'bulletin' elle-même, comme avant !


# --- 2. Fonctions de Remplacement des Requêtes ORM ---

def get_eleve_by_code(code_eleve):
    """Remplace Eleves.objects.get(code_eleve=code)."""
    eleves_all = get_data_from_sheet("Eleves_DB")
    
    data = next(
        (e for e in eleves_all if str(e.get('code_eleve', '')).upper() == code_eleve), 
        None
    )
    
    if data:
        return EleveSheet(data)
    raise EleveSheet.DoesNotExist # Simuler l'exception Django

# Ajouter une classe pour simuler l'exception (pour que votre code ne plante pas)
class DoesNotExist(Exception):
    pass
EleveSheet.DoesNotExist = DoesNotExist


def get_notes_for_bulletin(eleve_obj, semestre_nom):
    """Simule Note.objects.filter(eleve=eleve, semestre=semestre).select_related('matiere')."""
    notes_all = get_data_from_sheet("Notes_DB")
    
    # Simuler l'objet Semestre requis par votre vue
    semestre_obj = SemestreSheet(semestre_nom)

    # Filtrer les notes pour l'élève et le semestre donné
    notes_filtrees = [
        n for n in notes_all 
        if str(n.get('code_eleve', '')).upper() == eleve_obj.code_eleve.upper() 
        and n.get('semestre') == semestre_nom
    ]
    
    # Convertir chaque dictionnaire de note filtrée en objet NoteSheet
    note_objects = [NoteSheet(data, eleve_obj, semestre_obj) for data in notes_filtrees]

    return note_objects