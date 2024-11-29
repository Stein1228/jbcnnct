from django.urls import path
from . import views

urlpatterns = [
    # Ruta para cerrar sesión
    path('logout/', views.salir_cuenta, name='exit'),

    # Ruta para registrar un nuevo usuario
    path('registro/', views.register, name='register'),

    # Ruta para mostrar el perfil del usuario autenticado
    path('perfil/', views.perfil, name='perfil'),

    # Ruta para editar el perfil del usuario
    path('perfil/editar_perfil/', views.EditarPerfilView.as_view(), name='editar_perfil'),

    # Ruta para listar otros usuarios
    path('usuarios/lista/', views.listar_usuarios, name='lista_usuarios'),

    # Ruta para mostrar el perfil público de un usuario específico
    path('usuario/<int:usuario_id>/', views.PerfilPublicoView.as_view(), name='perfil_publico'),

    # Ruta para dejar una reseña para un usuario específico
    path('usuario/<int:usuario_id>/dejar_resena/', views.DejarReseñaView.as_view(), name='dejar_reseña'),
    
    path('reseña/modificar/<int:pk>/', views.ModificarReseñaView.as_view(), name='modificar_reseña'),
    
    path('reseñas/eliminar/<int:reseña_id>/', views.eliminar_reseña, name='eliminar_reseña'),
    
    path('filtrar-comunas/<int:region_id>/', views.FiltrarComunasView.as_view(), name='filtrar_comunas'),
    
    path('eliminar_perfil/<int:usuario_id>/', views.EliminarPerfilView.as_view(), name='eliminar_perfil'),
     
    path('editar_perfil/<int:usuario_id>/', views.EditarPerfilView.as_view(), name='editar_perfil_admin'),

    path('gestionar/', views.gestionar_entidades, name='gestionar_entidades'),
]