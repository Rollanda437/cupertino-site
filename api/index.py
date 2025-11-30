import os
from django.core.wsgi import get_wsgi_application

# Ajout des lignes de migration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
application = get_wsgi_application()

# --- BLOC D'EXÉCUTION DE MIGRATION ---
from django.core.management import call_command
from django.db.utils import OperationalError

try:
    print("Tentative d'exécution des migrations sur le démarrage...")
    call_command('migrate', interactive=False)
    print("Migrations terminées avec succès.")
except OperationalError as e:
    # Ceci peut arriver si la base de données n'est pas encore accessible
    print(f"Erreur lors de l'exécution des migrations : {e}")
# ------------------------------------

# Vercel exige exactement cette variable
app = application

# Optionnel : pour forcer le collectstatic au build (facultatif mais propre)
def __vercel_build():
    from django.core.management import call_command
    call_command('collectstatic', '--noinput')