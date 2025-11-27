import os
from pathlib import Path
import shutil
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Répertoire temporaire où Vercel permet d’écrire
WRITABLE_DIR = os.environ.get('VERCEL_TMP', '/tmp')
if not os.path.exists(WRITABLE_DIR):
    WRITABLE_DIR = '/tmp'
    os.makedirs(WRITABLE_DIR, exist_ok=True)

# Chemin final de la base
DB_PATH = os.path.join(WRITABLE_DIR, 'db.sqlite3')

# Copie depuis la racine si elle existe et que /tmp est vide
LOCAL_DB = os.path.join(BASE_DIR, 'db.sqlite3')
if os.path.exists(LOCAL_DB) and not os.path.exists(DB_PATH):
    try:
        shutil.copy(LOCAL_DB, DB_PATH)
        # On donne les droits d'écriture (parfois nécessaire)
        os.chmod(DB_PATH, 0o666)
    except Exception as e:
        pass  # Si ça échoue, on continue quand même

SECRET_KEY = 'django-insecure-change-me'  # Change ça plus tard

DEBUG = True

ALLOWED_HOSTS = ['*']  # Temporaire pour Vercel, on nettoie après

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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',           # LE SEUL ENDROIT OÙ ON PEUT ÉCRIRE
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# On copie la base du projet vers /tmp au démarrage si elle n’existe pas
if not os.path.exists('/tmp/db.sqlite3'):
    import shutil
    shutil.copy('db.sqlite3', '/tmp/db.sqlite3')
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'