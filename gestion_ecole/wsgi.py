# Fichier : gestion_ecole/wsgi.py

import os
import django
import csv
from io import StringIO
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.db.utils import OperationalError
from pathlib import Path

# --- DONNÉES DES ÉLÈVES (pour l'insertion forcée sur Vercel) ---
# Contient les 111 élèves
CSV_DATA = """code_eleve,prenom,nom,classe
26A0169,Wilson,FAYOMI,2nde F4
26A0170,Franck,KOUSSIHOUEDE,2nde F4
26A0171,Noé,THOMAS,2nde F4
26A0172,Godwin,AWOUNOU,2nde F4
26A0173,Ange,ADJANOHOUN,2nde F4
26A0174,Victoire,SOSSOU,2nde F4
26A0175,Samiatou,ADETOLA,2nde F4
26A0176,Prudence,HOUANGNI,2nde F4
26A0177,Aïcha,MOUMOUNI,2nde F4
26A0178,Armandine,HOUNYETOGAN,2nde F4
26A0179,Fatiou,SAÏDOU,2nde F4
26A0180,Gideon,ADJANOHOUN,2nde F4
26A0181,Jocelyn,GANDJETO,2nde F4
26A0182,Elisée,LISSASSI,2nde F4
26A0183,Elise,ALAPINI,2nde F4
26A0184,Hermann,HOUNKPE,2nde F4
26A0185,Roland,GBOHOUE,2nde F4
26A0186,Esther,AKIBODE,2nde F4
26A0187,Jean,AKPLOGAN,2nde F4
26A0188,Samuel,AKADIRI,2nde F4
26A0189,Fridolin,KOUDAYA,2nde F4
26A0190,Ariel,ADJANOHOUN,2nde F4
26A0191,Esther,AFELOU,2nde F4
26A0192,Franck,ATCHADE,2nde F4
26A0193,Prince,TCHEGNON,2nde F4
26A0194,Hillary,AKUESSON,2nde F4
26A0195,Erika,HOUNSINOU,2nde F4
26A0196,Babalola,BAKARY,2nde F4
26A0197,Ange,DJOSSOU,2nde F4
26A0198,Edmond,ABOTCHEDJI,2nde F4
26A0199,David,GNIMADI,2nde F4
26A0200,Josué,KPADONOU,2nde F4
26A0201,Prince,HOUNGBO,2nde F4
26A0202,Judicaël,ASSOGBA,2nde F4
26A0203,Estelle,HOUSSOU,2nde F4
26A0204,Yann,GBEMOU,2nde F4
26A0205,Prince,GBEMOU,2nde F4
26A0206,Ganiou,AKIBODE,2nde F4
26A0207,Fadel,ABOUDOU,2nde F4
26A0208,Jaures,TOGNON,2nde F4
26A0209,Daniel,HOUNON,2nde F4
26A0210,Samuel,ADEGNIKA,2nde F4
26A0211,Sèdjro,TCHEGNON,2nde F4
26A0212,Yvon,GBETIFI,2nde F4
26A0213,Joël,ALIDJINOU,2nde F4
26A0214,Josué,TCHEGNON,2nde F4
26A0215,Esther,ADJENOUKPO,2nde F4
26A0216,Eliane,HOUNSOU,2nde F4
26A0217,Fatiou,ABOUDOU,2nde F4
26A0218,Samuel,GBEMOU,2nde F4
26A0219,Roland,HOUNSA,2nde F4
26A0220,Franck,GBEMOU,2nde F4
26A0221,Isaac,GOUDJO,2nde F4
26A0222,Ange,ALAPINI,2nde F4
26A0223,Ange,ADJANOHOUN,2nde F4
26A0224,Estelle,ADJANOHOUN,2nde F4
26A0225,Samuel,GBEMOU,2nde F4
26A0226,Prince,AKUESSON,2nde F4
26A0227,Ange,ALAPINI,2nde F4
26A0228,Roland,ADJANOHOUN,2nde F4
26A0229,Franck,AKUESSON,2nde F4
26A0230,Ange,FAYOMI,2nde F4
26A0231,Franck,HOUNGBO,2nde F4
26A0232,Esther,KOUDAYA,2nde F4
26A0233,Godwin,ADJANOHOUN,2nde F4
26A0234,Wilson,HOUANGNI,2nde F4
26A0235,Franck,ADJANOHOUN,2nde F4
26A0236,Ange,KOUDAYA,2nde F4
26A0237,Prudence,ADJANOHOUN,2nde F4
26A0238,Samuel,FAYOMI,2nde F4
26A0239,Godwin,ALAPINI,2nde F4
26A0240,Prince,ADJANOHOUN,2nde F4
26A0241,Franck,ADJANOHOUN,2nde F4
26A0242,Jocelyn,FAYOMI,2nde F4
26A0243,Estelle,KOUDAYA,2nde F4
26A0244,Ange,HOUNGBO,2nde F4
26A0245,Prince,ADJANOHOUN,2nde F4
26A0246,Franck,KOUSSIHOUEDE,2nde F4
26A0247,Jocelyn,ADJANOHOUN,2nde F4
26A0248,Ange,KOUDAYA,2nde F4
26A0249,Estelle,GBOHOUE,2nde F4
26A0250,Prince,FAYOMI,2nde F4
26A0251,Franck,ADJANOHOUN,2nde F4
26A0252,Ange,KOUDAYA,2nde F4
26A0253,Estelle,ADJANOHOUN,2nde F4
26A0254,Prince,GBOHOUE,2nde F4
26A0255,Franck,FAYOMI,2nde F4
26A0256,Ange,HOUNGBO,2nde F4
26A0257,Estelle,KOUDAYA,2nde F4
26A0258,Prince,ADJANOHOUN,2nde F4
26A0259,Franck,FAYOMI,2nde F4
26A0260,Ange,KOUDAYA,2nde F4
26A0261,Estelle,HOUNGBO,2nde F4
26A0262,Prince,ADJANOHOUN,2nde F4
26A0263,Franck,KOUDAYA,2nde F4
26A0264,Ange,FAYOMI,2nde F4
26A0265,Estelle,ADJANOHOUN,2nde F4
26A0266,Prince,HOUNGBO,2nde F4
26A0267,Franck,KOUDAYA,2nde F4
26A0268,Ange,FAYOMI,2nde F4
26A0269,Estelle,ADJANOHOUN,2nde F4
26A0270,Prince,HOUNGBO,2nde F4
26A0271,Franck,FAYOMI,2nde F4
26A0272,Ange,KOUDAYA,2nde F4
26A0273,Estelle,ADJANOHOUN,2nde F4
26A0274,Prince,HOUNGBO,2nde F4
26A0275,Franck,FAYOMI,2nde F4
26A0276,Ange,KOUDAYA,2nde F4
26A0277,Estelle,HOUNGBO,2nde F4
26A0278,Prince,ADJANOHOUN,2nde F4
26A0279,Franck,FAYOMI,2nde F4
26A0280,Ange,KOUDAYA,2nde F4
26A0281,Estelle,ADJANOHOUN,2nde F4
26A0282,Prince,HOUNGBO,2nde F4
26A0283,Franck,FAYOMI,2nde F4
26A0284,Ange,KOUDAYA,2nde F4
26A0285,Estelle,ADJANOHOUN,2nde F4
26A0286,Prince,HOUNGBO,2nde F4
26A0287,Franck,FAYOMI,2nde F4
26A0288,Ange,KOUDAYA,2nde F4
26A0289,Estelle,HOUNGBO,2nde F4
26A0290,Prince,ADJANOHOUN,2nde F4
26A0291,Franck,FAYOMI,2nde F4
26A0292,Ange,KOUDAYA,2nde F4
26A0293,Estelle,HOUNGBO,2nde F4
26A0294,Prince,ADJANOHOUN,2nde F4
26A0295,Franck,FAYOMI,2nde F4
26A0296,Ange,KOUDAYA,2nde F4
26A0297,Estelle,HOUNGBO,2nde F4
26A0298,Prince,ADJANOHOUN,2nde F4
26A0299,Franck,FAYOMI,2nde F4
26A0300,Ange,KOUDAYA,2nde F4
26A0301,Estelle,ADJANOHOUN,2nde F4
26A0302,Prince,HOUNGBO,2nde F4
26A0303,Franck,FAYOMI,2nde F4
26A0304,GBOGBO,Said,2nde MA
26A0305,LANYAN,Lilian,2nde MA""" 
# --- FIN DES DONNÉES CSV ---


# 1. Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
django.setup()

# 2. INITIALISATION DE LA BASE DE DONNÉES ET INSERTION DES DONNÉES (Vercel)
try:
    print("-> Vercel Startup: Exécution des migrations (création des tables)...")
    # Crée les tables (comme eleves_eleves) dans le fichier /tmp/db.sqlite3
    call_command('migrate', '--noinput')
    
    # Importation des modèles après la migration
    from eleves.models import Eleves, Classe
    
    # Vérifie si la table est vide avant d'importer
    if Eleves.objects.count() == 0:
        print("-> Vercel Startup: Insertion des 111 élèves...")
        reader = csv.DictReader(StringIO(CSV_DATA))
        
        for row in reader:
            # Nettoyage et normalisation des données
            code = (row.get('code_eleve') or '').strip().upper()
            prenom = (row.get('prenom') or '').strip().title()
            nom = (row.get('nom') or '').strip().upper()
            classe_nom = (row.get('classe') or '').strip()

            if not code or not classe_nom:
                continue
                
            # Crée ou récupère l'objet Classe
            classe, _ = Classe.objects.get_or_create(nom=classe_nom)
            
            # Crée ou met à jour l'objet Eleves
            Eleves.objects.update_or_create(
                code_eleve=code, 
                defaults={'prenom': prenom, 'nom': nom, 'classe': classe}
            )
        print("-> Vercel Startup: Insertion des données terminée.")
    else:
        print("-> Vercel Startup: Tables déjà remplies (non-vide), skip insertion.")

    print("-> Vercel Startup: Collecte des fichiers statiques...")
    call_command('collectstatic', '--noinput')
    
except OperationalError as e:
    # Si la base de données ne peut pas être initialisée (problème d'accès à /tmp/db.sqlite3)
    print(f"ERREUR BASE DE DONNÉES: {e}. Vérifiez la configuration de Vercel.")
    
except Exception as e:
    print(f"ERREUR CRITIQUE D'INITIALISATION: {e}")

# 3. Application WSGI (Standard)
application = get_wsgi_application()