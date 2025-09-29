import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = "usuario.Usuario"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q(2tc^ov3%a++i8a2z01&+&(i7-yz3!)usfnbq8)u8wp8$(!2u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "13.43.246.242",
    "localhost",
    "127.0.0.1",
    "www.ourbiz.ao",
    "ourbiz.ao",
    "api.v1.ourbiz.ao",
]

# Configuração CORS (se estiver usando django-cors-headers)
CORS_ALLOWED_ORIGINS = [
    "https://13.43.246.242",
    "https://www.ourbiz.ao",
    "https://ourbiz.ao",
    "https://api.v1.ourbiz.ao",
    "https://127.0.0.1",
    "https://localhost",
    "http://localhost:5173"
]

# Domínios confiáveis para CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://13.43.246.242",
    "https://www.ourbiz.ao",
    "https://ourbiz.ao",
    "https://api.v1.ourbiz.ao",
    "https://127.0.0.1",
    "https://localhost",
    "http://localhost:5173"

]

# Segurança
SECURE_SSL_REDIRECT = False  # True se usar HTTPS obrigatório
CSRF_COOKIE_SECURE = False   # True se só aceitar cookie via HTTPS
SESSION_COOKIE_SECURE = False
USE_X_FORWARDED_HOST = True  # Necessário se estiver atrás de proxy/load balancer

# CSRF via sessão
CSRF_USE_SESSIONS = True  # Alternativa para evitar falhas no CSRF
CSRF_COOKIE_HTTPONLY = True  # Impede que JavaScript acesse o cookie CSRF
CSRF_COOKIE_SAMESITE = 'Lax'  # Permite CSRF apenas para o mesmo site

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'jazzmin',
    #'django_nvd3',
    #'django_admin_charts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja',
    'ap_solicitar',
    'usuario',
    'cliente',
    'funcionario',
    'servico',
    'notificacoes',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
#AUTH_USER_MODEL = "usuario.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "Africa/Luanda"  # ou outro fuso horário
USE_I18N = True
USE_L10N = True
USE_TZ = True
 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]
# Default primary key field type  
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Servidor SMTP do Gmail
EMAIL_PORT = 587  # Porta SMTP padrão para TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "adelinoemilianoa@gmail.com"  # Substitua pelo seu e-mail
EMAIL_HOST_PASSWORD = "sbfl ucob pajy tklq"  # Substitua pela senha ou use "App Password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Configuração do Redis como backend do Celery
CELERY_BROKER_URL = "sqla+sqlite:///celerydb.sqlite3"
CELERY_RESULT_BACKEND = "db+sqlite:///celery_results.sqlite3"

# Formato das tarefas
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Tentar reconectar ao iniciar
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

"""# Configuração do Celery
EMAIL_HOST = "mail.ourbiz.ao"  # Servidor SMTP do seu e-mail empresarial
#EMAIL_HOST = "smtp.gmail.com"  # Servidor SMTP do Gmail
EMAIL_PORT = 587  # Use 465 para SSL ou 587 para TLS
EMAIL_USE_TLS = True  # Se usar a porta 465, mude para EMAIL_USE_SSL = True
EMAIL_USE_SSL = False  # Se usar SSL (porta 465), defina como True
EMAIL_HOST_USER = "comercial@ourbiz.ao"  # Seu e-mail empresarial
EMAIL_HOST_PASSWORD = "#M936059607D*"  # Substitua pela senha correta#X


CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_BROKER_CONNECTIONe_RETRY_ON_STARTUP = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Servidor SMTP do Gmail
EMAIL_PORT = 587  # Porta SMTP padrão para TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "adelinoemilianoa@gmail.com"  # Substitua pelo seu e-mail
EMAIL_HOST_PASSWORD = "sbfl ucob pajy tklq"  # Substitua pela senha ou use "App Password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
"""

# Configurações do JWT
SECRET_KEY = "sua_chave_screta"  # Substitua por uma chave forte
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 60


# settings.py

JAZZMIN_SETTINGS = {
    "site_title": "OurBiz - Administração",
    "site_header": "OurBiz Admin",
    "site_brand": "OurBiz",
    "welcome_sign": "👋 Bem-vindo! Aqui podes gerir usuários, empresas e solicitações. Dica: usa o menu lateral para navegar.",
    "site_logo": "admin/img/lateral branca 2.png",   # caminho relativo dentro de STATICFILES
    "site_icon": "admin/img/favicon.ico",
    "show_sidebar": True,
    "navigation_expanded": True,
        # ... outras configurações ...
    "theme": "flatly",  # ou outro tema base
    "custom_theme": {
        "sidebar-bg": "#ad7f00",         # fundo da sidebar
        "sidebar-hover-bg": "#060707",   # fundo quando passar o mouse
        "sidebar-active-bg": "#0C0C0C",  # fundo do menu ativo
        "sidebar-color": "#080808",      # cor do texto do menu
        "sidebar-brand-color": "#ffffff",# cor do texto do branding/logo na sidebar
    },
    "topmenu_links": [
        {"name": "Website", "url": "/ourbiz.ao", "new_window": True},
        {"name": "Documentação", "url": "https://docs.djangoproject.com/", "new_window": True},
    ],
    "icons": {
        "auth": "fas fa-users",
        "usuario": "fas fa-user",
        "empresa": "fas fa-building",
        "servico": "fas fa-concierge-bell",
    },
    "order_with_respect_to": ["auth", "usuario", "empresa", "servico"],
    # inclui CSS/JS custom (arquivos em STATICFILES)
    "custom_css": "admin/css/custom_admin.css",
    "custom_js": "admin/js/custom_admin.js",
}
