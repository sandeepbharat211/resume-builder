"""
Django settings for the ResumePro project.

WHY THIS FILE LOOKS THE WAY IT DOES
------------------------------------
Secrets (Gemini API key, DB password, Django SECRET_KEY) are now read from
environment variables instead of being hardcoded. Hardcoding real API keys
or DB passwords directly in settings.py is a security risk -- anyone who
gets a copy of the project (via git, zip, screen-share, etc.) instantly
gets access to your keys and database.

HOW TO CONFIGURE
-----------------
1. Copy `.env.example` to a new file named `.env` in the project root
   (same folder as manage.py).
2. Fill in your real values (DB password, Gemini API key, etc.) in `.env`.
3. `.env` is only read locally -- never commit it to git / never zip it
   when sharing the project with someone else.
"""

from pathlib import Path
import os

# python-dotenv loads key=value pairs from a `.env` file into the process
# environment. This keeps secrets *out* of the source code.
from dotenv import load_dotenv

# BASE_DIR points at the project root (the folder containing manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from a .env file if one exists. If it doesn't exist,
# this simply does nothing (no crash) so the project still runs with
# sensible fallback values below.
load_dotenv(BASE_DIR / ".env")

# ─── Core Security Settings ────────────────────────────────────────────────

# SECRET_KEY is used by Django for signing sessions, cookies, CSRF tokens etc.
# It is read from the environment; a random dev-only fallback is provided so
# the project still boots the first time before you've created a .env file.
# IMPORTANT: generate a real, unique key for production
# (e.g. https://djecrety.ir) and put it in your .env file.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-fallback-key-change-me",
)

# DEBUG should be False in production. Controlled via env var so you can
# flip it without touching code. Defaults to True for local development.
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Comma separated list of allowed hosts, e.g. "example.com,www.example.com"
# Defaults to "*" (any host) which is fine for local dev but should be
# tightened for production deployments.
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'resume',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'resume.middleware.VisitorTrackingMiddleware',  # Custom visitor tracking (see resume/middleware.py)
]

ROOT_URLCONF = 'resume_builder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        # NOTE: 'APP_DIRS' is intentionally NOT set here (Django doesn't allow
        # it together with an explicit 'loaders' list -- see below).
        'OPTIONS': {
            # Explicit, always-uncached loaders. By default, when DEBUG=False
            # Django silently wraps the loaders below in a caching loader,
            # which keeps old compiled templates in memory until the server
            # process is fully restarted -- editing a .html file then appears
            # to "do nothing" even after a hard browser refresh. Listing the
            # loaders explicitly (without cached.Loader) guarantees templates
            # are always re-read from disk on every request, in every
            # environment, which is what you want during development.
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'resume_builder.wsgi.application'

# ─── Database (MySQL) ──────────────────────────────────────────────────────
# Install: pip install mysqlclient
# Create DB: CREATE DATABASE resume_builder_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
#
# All connection details come from environment variables (see .env.example)
# so real credentials never live in source control.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Prefer SQLite for a quick local test drive (no MySQL server needed)?
# Set USE_SQLITE=True in your .env file and this block takes over instead.
if os.environ.get("USE_SQLITE", "False") == "True":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ─── Static & Media Files ──────────────────────────────────────────────────

STATIC_URL = '/static/'

# STATICFILES_DIRS tells Django's staticfiles app-finder where to look for
# *project level* static files (i.e. files not inside a specific app's own
# static/ folder). Without this, files in the root-level `static/` folder
# (static/css/style.css, static/js/script.js) are silently ignored by
# `collectstatic` and can even 404 in DEBUG mode. This was missing before.
STATICFILES_DIRS = [BASE_DIR / "static"]

# STATIC_ROOT is where `collectstatic` copies everything for production.
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Gemini AI ──────────────────────────────────────────────────────────────
# Get a free key: https://aistudio.google.com/app/apikey
# Read from the environment -- put your real key in `.env` as GEMINI_API_KEY=...
# We use the Gemini 2.5 Flash model everywhere in this project (see
# resume/views.py) for fast, low-cost AI text generation.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Which Gemini model to use for all AI features. Centralized here so the
# whole project uses the exact same model consistently.
GEMINI_MODEL_NAME = "gemini-2.5-flash"
