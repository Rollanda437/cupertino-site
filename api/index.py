
    # api/index.py → CONFIGURATION OFFICIELLE VERCEL + DJANGO 2025
import os
from django.core.wsgi import get_wsgi_application

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
application = get_wsgi_application()

# Vercel exige exactement cette variable
app = application

# Optionnel : pour forcer le collectstatic au build (facultatif mais propre)
def __vercel_build():
    from django.core.management import call_command
    call_command('collectstatic', '--noinput')