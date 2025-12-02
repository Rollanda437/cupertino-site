import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
django.setup()

from django.contrib.auth.models import User

# Supprime tous les anciens au cas où
User.objects.filter(is_superuser=True).delete()

# Crée le nouveau
User.objects.create_superuser('admin', 'admin@sjcj.com', 'sjcj2026')
print("Superuser 'admin' / 'sjcj2026' créé en prod !")