from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Definimos las rutas principales del proyecto
urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),

    # Ruta principal que incluye las URLs definidas en la app 'core'
    path('', include('core.urls')),

    # Ruta para la gestión de usuarios, vinculada a las URLs de la app 'usuarios'
    path('usuarios/', include('usuarios.urls')),

    # Ruta para la autenticación de Django (login, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Ruta para la app 'trabajos', que gestiona las ofertas o búsquedas de empleo
    path('trabajos/', include('trabajos.urls')),
]

# Solo en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)