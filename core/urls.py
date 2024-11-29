from django.urls import path
from . import views  # Importamos las vistas del archivo views.py en el mismo módulo

# Definimos las rutas (URL patterns)
urlpatterns = [
    # Ruta para la página de inicio
    path('', views.home, name='home'),

    # Ruta para la página 'Nosotros'
    path('nosotros/', views.nosotros, name='nosotros'),

    # Ruta para la página de la 'Guía de uso'
    path('soporte/', views.guia_de_uso, name='soporte'),

    # Ruta para la página de 'Preguntas Frecuentes'
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
]
