import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Méthode 1 : Variable d’environnement (pour Vercel)
if os.getenv('FIREBASE_SERVICE_ACCOUNT'):
    service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
    cred = credentials.Certificate(service_account_info)
else:
    # Méthode 2 : Fichier local (pour ton PC)
    cred = credentials.Certificate('sjcj-firebase.json')

# Initialise seulement si pas déjà fait
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Base de données Firestore
db = firestore.client()

print("Firebase connecté avec succès !")