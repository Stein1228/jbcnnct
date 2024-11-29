from django.urls import path
from . import views  # Importamos las vistas desde el archivo views.py

# Definimos las rutas de la aplicación 'trabajos'
urlpatterns = [
    # Ruta para la vista 'productos', accesible en '/trabajos/'
    path('trabajos/', views.trabajos, name='trabajos'),
    path('trabajos/crear/', views.crear_trabajo, name='crear_trabajo'),
    path('trabajos/editar/<int:trabajo_id>/', views.editar_trabajo, name='editar_trabajo'),
    path('trabajos/eliminar/<int:trabajo_id>/', views.eliminar_trabajo, name='eliminar_trabajo'),
    path('postular/<int:trabajo_id>/', views.postular_trabajo, name='postular_trabajo'),
    path('ver_postulaciones/<int:trabajo_id>/', views.ver_postulaciones, name='ver_postulaciones'),
    path('ver_trabajos/', views.ver_trabajos, name='ver_trabajos'),
    path('trabajo/<int:trabajo_id>/seleccionar/<int:postulante_id>/', views.seleccionar_trabajador, name='seleccionar_trabajador'),
    path('trabajo/<int:trabajo_id>/', views.detalle_trabajo, name='detalle_trabajo'),
    path('trabajo/<int:trabajo_id>/resumen/', views.resumen_match, name='match'),
    path('trabajo/<int:trabajo_id>/forma_pago/', views.seleccionar_forma_pago, name='seleccionar_forma_pago'),
    path('trabajos/asignados/', views.trabajos_asignados, name='trabajos_asignados'),
]
