# Fichier : gestion_ecole/wsgi.py

import os
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

# 1. Configuration de l'environnement (Standard)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
django.setup()

# 2. TÂCHES DE DÉMARRAGE SUR L'ENVIRONNEMENT SANS SERVEUR (Vercel)
# Nous devons nous assurer que les tables existent et que les statiques sont collectés.
try:
    print("-> Vercel Startup: Exécution des migrations...")
    # Crée les tables (comme eleves_eleves) dans le fichier /tmp/db.sqlite3
    call_command('migrate', '--noinput')
    
    print("-> Vercel Startup: Collecte des fichiers statiques...")
    # Collecte les fichiers statiques (pour corriger les erreurs 404 sur SJCJ.png)
    call_command('collectstatic', '--noinput')
    
except Exception as e:
    # C'est normal que cette étape soit lente au premier démarrage.
    print(f"Erreur lors de l'initialisation de la DB/Statiques: {e}")

# 3. Application WSGI (Standard)
application = get_wsgi_application()

