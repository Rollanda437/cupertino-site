# 1. Crée le fichier repository qui lit TOUT depuis Google Sheets

import pandas as pd
import requests
from django.core.exceptions import ObjectDoesNotExist

# METS TON VRAI LIEN ICI (après avoir fait "Partager > Toute personne avec le lien peut voir")
SHEET_ID = "1iaegOAee9aA-nNyozgDnROwQPS3EJw9qoYhpeKd0TAM"  # ← Remplace par ton Google Sheet

def _get_df():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    return pd.read_csv(url).fillna("")

class EleveSheet:
    DoesNotExist = ObjectDoesNotExist
    
    def __init__(self, row):
        self.code_eleve = str(row.get("code_eleve", "")).strip().upper()
        self.prenom = row.get("prenom", "").strip().title()
        self.nom = row.get("nom", "").strip().upper()
        self.classe = row.get("classe", "").strip()

def get_eleve_by_code(code):
    df = _get_df()
    code = str(code).strip().upper()
    row = df[df['code_eleve'].astype(str).str.upper() == code]
    if row.empty:
        raise EleveSheet.DoesNotExist()
    return EleveSheet(row.iloc[0])

def get_notes_for_bulletin(eleve, semestre="S1"):
    df = _get_df()
    mask = df['code_eleve'].astype(str).str.upper() == eleve.code_eleve
    row = df[mask]
    if row.empty:
        return []
    
    notes = []
    cols = df.columns.tolist()
    matieres_cols = [c for c in cols if c not in ["code_eleve","prenom","nom","classe"]]
    
    for col in matieres_cols:
        if semestre not in col and any(x in col.lower() for x in ["inter","devoir","note"]):
            continue
        note = type('NoteSheet', (), {})()
        note.matiere = col.split(f" {semestre}")[0] if f" {semestre}" in col else col
        note.inter1 = pd.to_numeric(row.get(f"{note.matiere} {semestre} Inter1", ""), errors='coerce').iloc[0]
        note.inter2 = pd.to_numeric(row.get(f"{note.matiere} {semestre} Inter2", ""), errors='coerce').iloc[0]
        note.inter3 = pd.to_numeric(row.get(f"{note.matiere} {semestre} Inter3", ""), errors='coerce').iloc[0]
        note.inter4 = pd.to_numeric(row.get(f"{note.matiere} {semestre} Inter4", ""), errors='coerce').iloc[0]
        note.devoir1 = pd.to_numeric(row.get(f"{note.matiere} {semestre} Devoir1", ""), errors='coerce').iloc[0]
        note.devoir2 = pd.to_numeric(row.get(f"{note.matiere} {semestre} Devoir2", ""), errors='coerce').iloc[0]
        notes.append(note)
    return notes