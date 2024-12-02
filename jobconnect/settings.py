import os
from pathlib import Path

# Construir rutas dentro del proyecto como esta: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de inicio rápido - no apta para producción
# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta utilizada en producción en secreto.
SECRET_KEY = 'django-insecure-d=c3m++#@fa#cj%fws%m$@qr8g1yc3w*1m)tnyttsf!c3(46uv'  # Clave secreta para el proyecto

# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción.
DEBUG = False  # Cambiar a False en producción

ALLOWED_HOSTS = ['*']  # Hosts que están permitidos para servir esta aplicación, deben especificarse en producción.

# Definición de aplicaciones
INSTALLED_APPS = [
    # Aplicaciones principales de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicaciones personalizadas
    'core',  # Aplicación principal
    'usuarios',  # Aplicación de gestión de usuarios
    'trabajos', # Aplicación de gestión de trabajos
]

# Middleware que gestiona varias capas de procesamiento de peticiones/respuestas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
ROOT_URLCONF = 'jobconnect.urls'  # Archivo principal de rutas del proyecto

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Directorios para plantillas personalizadas (vacío por defecto)
        'APP_DIRS': True,  # Habilita la búsqueda de plantillas en las apps instaladas
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

WSGI_APPLICATION = 'jobconnect.wsgi.application'  # Aplicación WSGI para la implementación del proyecto

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Uso de base de datos SQLite (cambiar a PostgreSQL, MySQL, etc. en producción)
        'NAME': BASE_DIR / 'db.sqlite3',  # Ubicación del archivo de base de datos
    }
}

# Validación de contraseñas para mayor seguridad
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

# Configuración de internacionalización
LANGUAGE_CODE = 'es-cl'  # Idioma predeterminado (Español)
TIME_ZONE = 'America/Santiago'  # Zona horaria (puedes cambiarla según la ubicación geográfica)
USE_I18N = True  # Habilitar internacionalización
USE_TZ = True  # Habilitar soporte de zonas horarias
USE_L10N = True  # Asegúrate de que la localización esté habilitada

# Archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = 'static/'  # URL para los archivos estáticos

# Directorios adicionales donde se almacenarán los archivos estáticos en desarrollo
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Directorio donde se recopilarán los archivos estáticos (por ejemplo, para producción)
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Archivos multimedia (imágenes, videos subidos por los usuarios)
MEDIA_URL = '/media/'  # URL para servir archivos multimedia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directorio donde se almacenarán los archivos subidos

# Tipo de campo de clave primaria predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Variables de redirección para el inicio de sesión y cierre de sesión
LOGIN_REDIRECT_URL = 'home'  # Redirige a 'home' después de iniciar sesión
LOGOUT_REDIRECT_URL = 'home'  # Redirige a 'home' después de cerrar sesión

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'usuarios.CustomUser'  # Especifica el modelo de usuario personalizado (CustomUser)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jbcnnct@gmail.com'
EMAIL_HOST_PASSWORD = 'osez yxar drcs dzeh'