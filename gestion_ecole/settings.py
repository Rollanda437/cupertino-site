import os
import shutil
from pathlib import Path, PosixPath

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-me-2025'  # À changer plus tard
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eleves',
    'avis',
    'calendrier',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestion_ecole.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestion_ecole.wsgi.application'

# BASE DE DONNÉES – VERSION QUI MARCHE À TOUS LES COUPS SUR VERCEL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Localement, la base est ici (dans le répertoire du projet)
        'NAME': PosixPath('/var/task/db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
# LOGIQUE DE COPIE DB POUR VERCEL
# Le chemin temporaire de Vercel doit être /tmp, pas la racine /
LOCAL_DB_PATH = BASE_DIR / 'db.sqlite3'
TMP_DB_PATH = Path('/tmp/db.sqlite3') # 💡 CORRECTION: utilisation de /tmp

# Nous n'exécutons la copie que si nous ne sommes PAS en mode DEBUG (c'est-à-dire en Production)
# Cette vérification est souvent utilisée dans les environnements sans serveur (Lambda/Vercel)
if not DEBUG and LOCAL_DB_PATH.exists() and not TMP_DB_PATH.exists():
    try:
        # Copie la base de données intégrée dans le paquet Vercel vers le répertoire temporaire (/tmp)
        shutil.copy(str(LOCAL_DB_PATH), str(TMP_DB_PATH))
        # Définir les droits d'écriture sur le fichier copié
        os.chmod(str(TMP_DB_PATH), 0o666)
    except Exception as e:
        print(f"Copie DB échouée (seulement un problème si c'est la première exécution sur Vercel) : {e}")


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AJOUTE ÇA À LA FIN DU FICHIER (juste avant la dernière ligne)
import os
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
# Nettoie le cache Vercel à chaque déploiement
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'