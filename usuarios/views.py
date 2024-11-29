# Importaciones
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, DeleteView, UpdateView
from django.contrib.auth.forms import AuthenticationForm

# Modelos y formularios
from .models import CustomUser, Habilidades, Region, Reseña, ImagenReseña, Comuna
from .forms import UserEditForm, CustomUserCreationForm, ReseñaForm

User = get_user_model()

# -------------------------
# Vistas de Usuarios
# -------------------------

@login_required
def salir_cuenta(request):
    """Cerrar sesión del usuario."""
    logout(request)
    return redirect('home')

@login_required
def perfil(request):
    """Vista del perfil del usuario."""
    user = request.user
    reseñas = Reseña.objects.filter(usuario_revisado=user)

    # Calcula la calificación promedio
    calificacion_promedio = reseñas.aggregate(Avg('calificacion'))['calificacion__avg'] if reseñas.exists() else 0.0
    calificacion_promedio = round(calificacion_promedio, 1) if calificacion_promedio else 0.0

    # Calcula la edad del usuario usando la función del modelo
    edad = user.calcular_edad()

    return render(request, 'usuarios/perfil.html', {
        'user': user,
        'reseñas': reseñas,
        'calificacion_promedio': calificacion_promedio,
        'edad': edad,
    })

class FiltrarComunasView(View):
    def get(self, request, region_id):
        
        try:
            region = Region.objects.get(id=region_id)
        except Region.DoesNotExist:
            return JsonResponse([], safe=False)  # Retorna una lista vacía si no existe la región
        
        comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
        comunas_data = [{'id': comuna.id, 'nombre': comuna.nombre} for comuna in comunas]
        return JsonResponse(comunas_data, safe=False)
    
class EditarPerfilView(LoginRequiredMixin, View):
    """Vista para editar el perfil del usuario, o de otros usuarios si es administrador."""
    
    def get(self, request, usuario_id=None):
        # Si es administrador y se pasa un usuario_id, obtener el perfil del otro usuario
        if request.user.is_staff and usuario_id:
            usuario = get_object_or_404(CustomUser, pk=usuario_id)
        else:
            usuario = request.user  # El usuario solo puede editar su propio perfil
        
        form = UserEditForm(instance=usuario)
        return render(request, 'usuarios/editar_perfil.html', {'form': form, 'usuario': usuario})

    def post(self, request, usuario_id=None):
        # Si es administrador y se pasa un usuario_id, obtener el perfil del otro usuario
        if request.user.is_staff and usuario_id:
            usuario = get_object_or_404(CustomUser, pk=usuario_id)
        else:
            usuario = request.user  # El usuario solo puede editar su propio perfil

        form = UserEditForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado exitosamente.")
            # Si el usuario está editando el perfil de otro usuario, redirigir al perfil público
            if request.user.is_staff and usuario_id:
                return redirect('perfil_publico', usuario_id=usuario.id)
            # Si no, redirigir al perfil del usuario editado
            return redirect('perfil')  
        
        # Si el formulario no es válido, volver a mostrar la página con los errores
        messages.error(request, "Por favor, corrige los errores en el formulario.")
        return render(request, 'usuarios/editar_perfil.html', {'form': form, 'usuario': usuario})

class EliminarPerfilView(LoginRequiredMixin, View):
    """Vista para eliminar el perfil de un usuario (solo administradores)."""

    def post(self, request, usuario_id):
        # Verificar si el usuario tiene permisos de staff
        if not request.user.is_staff:
            return HttpResponseForbidden("No tienes permiso para eliminar este perfil.")

        # Obtener el usuario a eliminar
        usuario = get_object_or_404(CustomUser, pk=usuario_id)

        # Eliminar el usuario
        usuario.delete()

        messages.success(request, "El perfil ha sido eliminado exitosamente.")
        return redirect('lista_usuarios')  # Redirigir a la página principal o la que prefieras
        
@login_required    
def listar_usuarios(request):
    """Lista de usuarios con opciones de filtro y paginación."""
    query = request.GET.get('query', '')
    habilidades_seleccionadas = request.GET.getlist('habilidades')
    calificacion_minima = request.GET.get('calificacion_minima')
    orden = request.GET.get('orden', 'desc')
    region_seleccionada = request.GET.get('region', '')  # Filtro por región
    comuna_seleccionada = request.GET.get('comuna', '')  # Filtro por comuna
    
    # Filtra solo habilidades válidas (evita errores si está vacío o no es numérico)
    habilidades_seleccionadas = [int(hab) for hab in habilidades_seleccionadas if hab.isdigit()]
    
    # Excluye al usuario logueado
    usuarios = CustomUser.objects.exclude(id=request.user.id)
    
    # Filtrar por nombre
    if query:
        usuarios = usuarios.filter(first_name__icontains=query) | usuarios.filter(last_name__icontains=query)
        
    # Filtrar por habilidades
    if habilidades_seleccionadas:
        usuarios = usuarios.filter(habilidades__id__in=habilidades_seleccionadas).distinct()

    # Filtrar por región si no es None
    if region_seleccionada and region_seleccionada != 'None':
        usuarios = usuarios.filter(region__id=region_seleccionada)

    # Filtrar por comuna si no es None
    if comuna_seleccionada and comuna_seleccionada != 'None':
        usuarios = usuarios.filter(comuna__id=comuna_seleccionada)

    # Anotar calificación promedio, tratando con usuarios sin reseñas
    usuarios = usuarios.annotate(
        calificacion_promedio=Coalesce(Avg('reseñas_recibidas__calificacion', output_field=FloatField()), Value(0.0))
    )

    # Filtrar por calificación mínima
    if calificacion_minima and calificacion_minima != 'None':
        usuarios = usuarios.filter(calificacion_promedio__gte=float(calificacion_minima))
    
    # Ordenar por calificación
    usuarios = usuarios.order_by('-calificacion_promedio' if orden == 'desc' else 'calificacion_promedio')
    
     # Paginación
    paginator = Paginator(usuarios, 9)  # Muestra 10 usuarios por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la consulta
    usuarios_paginated = paginator.get_page(page_number)
    
    habilidades = Habilidades.objects.all()
    regiones = Region.objects.all()  # Obtén todas las regiones
    
    comunas = Comuna.objects.filter(region_id=region_seleccionada) if region_seleccionada else Comuna.objects.none()# Obtén todas las comunas

    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios_paginated,
        'query': query,
        'habilidades': habilidades,
        'habilidades_seleccionadas': habilidades_seleccionadas,
        'calificacion_minima': calificacion_minima,
        'orden': orden,
        'regiones': regiones,  # Enviar regiones al template
        'comunas': comunas,    # Enviar comunas al template
        'region_seleccionada': region_seleccionada,  # Para mantener la selección
        'comuna_seleccionada': comuna_seleccionada,  # Para mantener la selección
    })

def register(request):
    """Vista para registrar un nuevo usuario."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir a la página de inicio de sesión
        else:
            messages.error(request, "Hubo un error en el registro. Por favor, revisa los campos.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'usuarios/register.html', {'form': form, 'post_data': request.POST})

# -------------------------
# Vistas de Perfiles Públicos
# -------------------------

class PerfilPublicoView(DetailView):
    """Vista para mostrar el perfil público de un usuario."""
    model = CustomUser
    template_name = 'usuarios/perfil_publico.html'
    context_object_name = 'usuario'
    
    def get_object(self, queryset=None):
        """Obtiene el usuario por su ID."""
        usuario_id = self.kwargs.get('usuario_id')
        return get_object_or_404(CustomUser, id=usuario_id)

    def get_context_data(self, **kwargs): 
        """Añade las reseñas del usuario al contexto."""
        context = super().get_context_data(**kwargs)
        usuario = self.get_object()
        context['reseñas'] = Reseña.objects.filter(usuario_revisado=usuario)
        context['edad'] = usuario.calcular_edad()
        
        # Verificar si el usuario actual es staff
        if self.request.user.is_staff:
            context['is_staff'] = True
        else:
            context['is_staff'] = False

        return context

# -------------------------
# Vistas de Reseñas
# -------------------------

class ModificarReseñaView(UpdateView):
    """Vista para modificar una reseña existente."""
    model = Reseña
    template_name = 'usuarios/modificar_reseña.html'  # Cambia esto al nombre de tu template
    form_class = ReseñaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imagenes'] = ImagenReseña.objects.filter(reseña=self.object)  # Carga las imágenes actuales
        context['usuario_revisor'] = self.object.usuario_revisor  # Revisor
        context['usuario_revisado'] = self.object.usuario_revisado  # Revisado
        context['rating_range'] = range(1, 6)  # Rango de calificaciones (1 a 5)
        return context

    def form_valid(self, form):
        self.object = form.save()
        
        # Eliminar imágenes seleccionadas para eliminar
        delete_images = self.request.POST.getlist('delete_images')
        ImagenReseña.objects.filter(id__in=delete_images).delete()  # Elimina las imágenes seleccionadas

        # Procesar el formulario para nuevas imágenes
        new_images = self.request.FILES.getlist('new_imagen')
        for new_image in new_images:
            ImagenReseña.objects.create(reseña=self.object, imagen=new_image)

        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirigir a la vista del perfil del usuario revisado
        return reverse('perfil_publico', args=[self.object.usuario_revisado.id])

@login_required
def eliminar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)

    # Verifica si el usuario es el autor de la reseña o un administrador
    if reseña.usuario_revisor == request.user or request.user.is_staff:
        reseña.delete()
        messages.success(request, "La reseña ha sido eliminada.")
    else:
        messages.error(request, "No tienes permiso para eliminar esta reseña.")

    # Redirigir usando el ID del usuario cuya reseña fue eliminada
    return redirect('perfil_publico', usuario_id=reseña.usuario_revisado.id)

class DejarReseñaView(View):
    """Vista para dejar una reseña a otro usuario."""

    def get(self, request, usuario_id):
        """Muestra el formulario para dejar una reseña."""
        usuario = get_object_or_404(CustomUser, id=usuario_id)
        form = ReseñaForm()
        return render(request, 'usuarios/dejar_resena.html', {'form': form, 'usuario': usuario})

    def post(self, request, usuario_id):
        """Guarda la reseña del usuario."""
        usuario = get_object_or_404(CustomUser, id=usuario_id)
        form = ReseñaForm(request.POST)

        # Manejo de imágenes
        imagenes = request.FILES.getlist('imagen')  # Captura varias imágenes

        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.usuario_revisor = request.user
            reseña.usuario_revisado = usuario
            reseña.save()
            self.guardar_imagenes(reseña, imagenes)
            return redirect('perfil_publico', usuario_id=usuario_id)  # Redirige a la página del usuario reseñado
        
        # Si el formulario no es válido, se muestran los errores específicos
        return render(request, 'usuarios/dejar_resena.html', {'form': form, 'usuario': usuario})

    def guardar_imagenes(self, reseña, imagenes):
        """Guarda las imágenes asociadas a la reseña."""
        for imagen in imagenes:
            ImagenReseña.objects.create(reseña=reseña, imagen=imagen)



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Aquí gestionas la lógica de login (redirigir, etc.)
            return redirect('nombre_de_la_url_a_redirigir')
        else:
            messages.error(request, "Credenciales incorrectas. Por favor, inténtalo de nuevo.")
    
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


# views.py




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Region, Comuna, Habilidades
from .forms import RegionForm, ComunaForm, HabilidadesForm

@login_required
def gestionar_entidades(request):
    # Crear o editar una región
    if request.method == 'POST':
        # Región
        if 'crear_region' in request.POST:
            region_form = RegionForm(request.POST)
            if region_form.is_valid():
                region_form.save()
        elif 'editar_region' in request.POST:
            region_id = request.POST.get('region_id')
            region = get_object_or_404(Region, pk=region_id)
            region_form = RegionForm(request.POST, instance=region)
            if region_form.is_valid():
                region_form.save()
        elif 'eliminar_region' in request.POST:
            region_id = request.POST.get('region_id')
            region = get_object_or_404(Region, pk=region_id)
            region.delete()

        # Comuna
        elif 'crear_comuna' in request.POST:
            comuna_form = ComunaForm(request.POST)
            if comuna_form.is_valid():
                comuna_form.save()
        elif 'editar_comuna' in request.POST:
            comuna_id = request.POST.get('comuna_id')
            comuna = get_object_or_404(Comuna, pk=comuna_id)
            comuna_form = ComunaForm(request.POST, instance=comuna)
            if comuna_form.is_valid():
                comuna_form.save()
        elif 'eliminar_comuna' in request.POST:
            comuna_id = request.POST.get('comuna_id')
            comuna = get_object_or_404(Comuna, pk=comuna_id)
            comuna.delete()

        # Habilidad
        elif 'crear_habilidad' in request.POST:
            habilidad_form = HabilidadesForm(request.POST)
            if habilidad_form.is_valid():
                habilidad_form.save()
        elif 'editar_habilidad' in request.POST:
            habilidad_id = request.POST.get('habilidad_id')
            habilidad = get_object_or_404(Habilidades, pk=habilidad_id)
            habilidad_form = HabilidadesForm(request.POST, instance=habilidad)
            if habilidad_form.is_valid():
                habilidad_form.save()
        elif 'eliminar_habilidad' in request.POST:
            habilidad_id = request.POST.get('habilidad_id')
            habilidad = get_object_or_404(Habilidades, pk=habilidad_id)
            habilidad.delete()

    # Inicializar los formularios vacíos
    region_form = RegionForm()
    comuna_form = ComunaForm()
    habilidad_form = HabilidadesForm()

    # Obtener las entidades existentes
    regions = Region.objects.all()
    comunas = Comuna.objects.all()
    habilidades = Habilidades.objects.all()

    context = {
        'region_form': region_form,
        'comuna_form': comuna_form,
        'habilidad_form': habilidad_form,
        'regions': regions,
        'comunas': comunas,
        'habilidades': habilidades,
    }

    return render(request, 'usuarios/gestionar_entidades.html', context)


