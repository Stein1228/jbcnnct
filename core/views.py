from django.shortcuts import render
from usuarios.models import CustomUser, CustomUserManager, Trabajo  # Asegúrate de importar los modelos correctamente
from django.db.models import Sum
# Vista para la página de inicio
def home(request):
    # Obtener el número total de usuarios registrados
    usuarios_registrados = CustomUser.objects.count()

    # Obtener el número de usuarios administradores registrados
    usuarios_admin_registrados = CustomUser.objects.filter(is_superuser=True).count()

    # Obtener el número total de trabajos postulados
    trabajos_postulados = Trabajo.objects.count()

    # Obtener el número total de trabajos realizados
    trabajos_realizados = CustomUser.objects.aggregate(total=Sum('trabajos_realizados'))['total'] or 0

    # Pasar estos datos al contexto para que estén disponibles en el template
    context = {
        'usuarios_registrados': usuarios_registrados,
        'usuarios_admin_registrados': usuarios_admin_registrados,
        'trabajos_postulados': trabajos_postulados,
        'trabajos_realizados': trabajos_realizados
    }
    # Renderiza la plantilla 'home.html' ubicada en la carpeta 'core'
    return render(request, 'core/home.html', context)

# Vista para la página 'Nosotros'
def nosotros(request):
    # Renderiza la plantilla 'nosotros.html' ubicada en la carpeta 'core'
    return render(request, 'core/nosotros.html')

# Vista para la página de la 'Guía de uso'
def guia_de_uso(request):
    # Renderiza la plantilla 'soporte.html' ubicada en la carpeta 'core'
    return render(request, 'core/soporte.html')

# Vista para la página de 'Preguntas Frecuentes'
def preguntas_frecuentes(request):
    # Renderiza la plantilla 'preguntas_frecuentes.html' ubicada en la carpeta 'core'
    return render(request, 'core/preguntas_frecuentes.html')