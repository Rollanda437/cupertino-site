import csv
import io
import requests
from django.core.exceptions import ObjectDoesNotExist

# METS TON VRAI ID ICI (ex: 1vOaB2y5G9tY8eXz7kL3mQ9wR4tY6uI8oP9aS1dF3gH4)
SHEET_ID = "1iaegOAee9aA-nNyozgDnROwQPS3EJw9qoYhpeKd0TAM"

def _get_sheet_csv():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    r = requests.get(url)
    r.raise_for_status()
    return r.content.decode('utf-8')

class EleveSheet:
    DoesNotExist = ObjectDoesNotExist
    def __init__(self, row):
        self.code_eleve = str(row.get("code_eleve", "")).strip().upper()
        self.prenom = row.get("prenom", "").strip().title()
        self.nom = row.get("nom", "").strip().upper()
        self.classe = row.get("classe", "").strip()

def get_eleve_by_code(code):
    csv_data = _get_sheet_csv()
    reader = csv.DictReader(io.StringIO(csv_data))
    code = code.strip().upper()
    for row in reader:
        if str(row.get("code_eleve", "")).strip().upper() == code:
            return EleveSheet(row)
    raise EleveSheet.DoesNotExist()

def get_notes_for_bulletin(eleve, semestre="S1"):
    csv_data = _get_sheet_csv()
    reader = csv.DictReader(io.StringIO(csv_data))
    for row in reader:
        if str(row.get("code_eleve", "")).strip().upper() == eleve.code_eleve:
            notes = []
            for key, value in row.items():
                if semestre in key and any(x in key.lower() for x in ["inter", "devoir"]):
                    matiere = key.split(f" {semestre}")[0]
                    note = type('obj', (), {})()
                    note.matiere = matiere
                    note.inter1 = _to_float(row.get(f"{matiere} {semestre} Inter1"))
                    note.inter2 = _to_float(row.get(f"{matiere} {semestre} Inter2"))
                    note.inter3 = _to_float(row.get(f"{matiere} {semestre} Inter3"))
                    note.inter4 = _to_float(row.get(f"{matiere} {semestre} Inter4"))
                    note.devoir1 = _to_float(row.get(f"{matiere} {semestre} Devoir1"))
                    note.devoir2 = _to_float(row.get(f"{matiere} {semestre} Devoir2"))
                    notes.append(note)
            return notes
    return []

def _to_float(val):
    try: return float(val) if val and val.strip() else None
    except: return None