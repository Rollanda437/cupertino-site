import os
import shutil
from pathlib import Path

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
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Copie automatique de la base (si elle existe à la racine) VERS /data
LOCAL_DB_PATH = BASE_DIR / 'db.sqlite3'
TMP_DB_PATH = Path('/db.sqlite3')

if LOCAL_DB_PATH.exists() and not TMP_DB_PATH.exists():
    try:
        shutil.copy(str(LOCAL_DB_PATH), str(TMP_DB_PATH))
        os.chmod(str(TMP_DB_PATH), 0o666)  # droits d'écriture
    except Exception as e:
        print("Copie DB échouée, on continue sans :", e)

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
