from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Habilidades, Reseña, ImagenReseña, Region, Comuna

class CustomUserCreationForm(forms.ModelForm):
    """Formulario para crear un nuevo usuario."""
    
    class Meta:
        model = CustomUser
        fields = (
            'email', 'rut', 'first_name', 's_nombre', 
            'last_name', 's_apellido', 'fecha_nacimiento', 
            'numero_telefono', 'password', 'genero', 
            'nacionalidad', 'region', 'comuna', 'bio', 
            'foto_perfil', 'instagram', 'facebook',
            'trabajos_realizados', 'trabajos_solicitados', 
            'habilidades', 'is_active', 'is_staff'  # Campos incluidos
        )

    def save(self, commit=True):
        """Guarda el usuario asegurando que la contraseña se establece correctamente."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Asegura que la contraseña se guarde correctamente
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """Formulario para editar un usuario existente."""
    
    class Meta:
        model = CustomUser
        fields = '__all__'  # Permite editar todos los campos


class CustomUserAdmin(UserAdmin):
    """Configuración del panel de administración para el modelo CustomUser."""
    
    add_form = CustomUserCreationForm  # Formulario para añadir un nuevo usuario
    form = CustomUserChangeForm  # Formulario para editar un usuario existente

    list_display = (
        'email', 'rut', 'first_name', 'last_name', 
        'fecha_nacimiento', 'numero_telefono', 
        'genero', 'nacionalidad', 'region', 'comuna', 
        'bio', 'trabajos_realizados', 'trabajos_solicitados',
        'is_active', 'is_staff'  # Campos visibles en la lista
    )
    
    ordering = ('email',)  # Ordena los usuarios por email

    list_filter = (
        'nacionalidad',  # Filtros disponibles en el panel de administración
        'is_active',     # Filtro por estado activo
        'is_staff'       # Filtro por estado de personal
    )

    fieldsets = (
        (None, {'fields': (
            'email', 'rut', 'first_name', 's_nombre', 
            'last_name', 's_apellido', 'fecha_nacimiento', 
            'numero_telefono', 'password', 'genero', 
            'nacionalidad', 'region', 'comuna', 'bio', 
            'foto_perfil', 'instagram', 'facebook', 
            'trabajos_realizados', 'trabajos_solicitados', 
            'habilidades', 'is_active', 'is_staff'  # Campos incluidos en el formulario
        )}),
    )

    def get_fieldsets(self, request, obj=None):
        """Evita que la contraseña se muestre en la lista de campos."""
        if obj:
            return super().get_fieldsets(request, obj)
        return self.fieldsets


@admin.register(ImagenReseña)
class ImagenReseñaAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo ImagenReseña."""

    list_display = ('reseña', 'imagen')  # Campos a mostrar en la lista
    list_filter = ('reseña',)  # Filtros para la lista
    search_fields = ('reseña__contenido',)  # Campo para buscar en el contenido de la reseña
    readonly_fields = ('reseña',)  # Campo no editable, si así lo deseas

    fieldsets = (
        (None, {
            'fields': ('reseña', 'imagen')
        }),
    )
    
@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo Reseña."""

    list_display = ('usuario_revisor', 'usuario_revisado', 'calificacion', 'fecha_creacion', 'mostrar_imagenes')  # Añade 'mostrar_imagenes' a la lista
    list_filter = ('usuario_revisor', 'usuario_revisado', 'calificacion')  # Filtros para la lista
    search_fields = ('contenido',)  # Campo para buscar
    ordering = ('-fecha_creacion',)  # Ordenar por fecha, más reciente primero
    readonly_fields = ('fecha_creacion',)  # Campo no editable

    fieldsets = (
        (None, {
            'fields': ('usuario_revisor', 'usuario_revisado', 'calificacion', 'contenido')
        }),
        ('Fecha', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',),  # Hace que el campo de fecha se colapse
        }),
    )

    def mostrar_imagenes(self, obj):
        """Muestra las imágenes relacionadas en el admin."""
        return ", ".join([str(imagen.imagen) for imagen in obj.imagenes.all()])  # Personaliza la representación de las imágenes

    mostrar_imagenes.short_description = 'Imágenes'  # Título de la columna

# Registra los modelos en el panel de administración
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Habilidades)
admin.site.register(Region)
admin.site.register(Comuna)