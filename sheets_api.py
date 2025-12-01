# sheets_api.py
import gspread

# Le nom du fichier que vous avez téléchargé et renommé à l'Étape 2
CLIENT_SECRET_FILE = 'client_secret.json' 
# Le titre exact de votre feuille Google Sheets (ex: "Mon Projet Scolaire SJCJ")
GOOGLE_SHEET_TITLE = 'gestion_cupertino' 

def authenticate():
    """Authentifie gspread en utilisant le fichier client_secret.json."""
    try:
        # Utilise ServiceAccountCredentials pour lire le fichier JSON
        gc = gspread.service_account(filename=CLIENT_SECRET_FILE)
        return gc
    except Exception as e:
        print(f"Erreur d'authentification GSpread : {e}")
        return None

def get_data_from_sheet(worksheet_name):
    """Récupère toutes les données d'une feuille de travail spécifique."""
    gc = authenticate()
    if not gc:
        return []

    try:
        # Ouvrir la feuille par son titre
        sh = gc.open("gestion_cupertino")

        # Sélectionner la feuille de travail (worksheet) par son nom
        worksheet = sh.worksheet(worksheet_name)
        
        # Récupère toutes les lignes sous forme de liste de dictionnaires
        return worksheet.get_all_records()
    except gspread.exceptions.WorksheetNotFound:
        print(f"Erreur : La feuille de travail '{worksheet_name}' est introuvable.")
        return []
    except Exception as e:
        print(f"Erreur lors de la lecture des données : {e}")
        return []