from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Comuna, CustomUser, Habilidades, Region, Reseña, ImagenReseña, Trabajo # Asegúrate de importar el modelo de usuario y el de habilidades

# Obtiene el modelo de usuario personalizado
User = get_user_model()

class UserEditForm(forms.ModelForm):
    """Formulario para editar los detalles del usuario."""

    habilidades = forms.ModelMultipleChoiceField(
        queryset=Habilidades.objects.all(),  # Obtiene todas las habilidades disponibles
        widget=forms.CheckboxSelectMultiple,  # Usa un widget de selección múltiple
        required=False
    )
    
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        empty_label="Selecciona una región"  # Opción predeterminada
    )

    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),  # Inicialmente vacío
        required=True,
        empty_label="Selecciona una comuna"  # Opción predeterminada
    )

    class Meta:
        model = CustomUser  # Especifica el modelo a utilizar en el formulario
        fields = [
            'email',
            'first_name',
            's_nombre',
            'last_name',
            's_apellido',
            'region',
            'comuna',
            'bio',
            'foto_perfil',
            'numero_telefono',
            'genero',
            'instagram',
            'facebook',
            'habilidades',
        ]

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:  
            if self.instance.region:
                self.fields['comuna'].queryset = self.instance.region.comunas.order_by('nombre')
                self.fields['comuna'].initial = self.instance.comuna  

    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get('region')
        comuna = cleaned_data.get('comuna')

        # Validar que se haya seleccionado una comuna
        if region and comuna:
            if comuna.region != region:
                raise forms.ValidationError("Debes selecionar una region y una comuna")
        
        return cleaned_data
                
class CustomUserCreationForm(forms.ModelForm):
    """Formulario para crear un nuevo usuario."""
    
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'rut',
            'first_name',
            'last_name',
            'fecha_nacimiento',
            'numero_telefono',
            'genero',
            'nacionalidad',
            'password',  # Asegúrate de incluir el campo de contraseña
        ]
    
    def __init__(self, *args, **kwargs):
        """Inicializa el formulario y establece etiquetas vacías para géneros y nacionalidades."""
        super().__init__(*args, **kwargs)
        self.fields['genero'].empty_label = "Seleccione un género"
        self.fields['nacionalidad'].empty_label = "Seleccione una nacionalidad"

    def clean(self):
        """Valida que las contraseñas coincidan y que el email, RUT y número de teléfono sean únicos."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        email = cleaned_data.get("email")
        rut = cleaned_data.get("rut")
        numero_telefono = cleaned_data.get("numero_telefono")

        # Verifica que el email sea único
        if email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")

        # Verifica que el RUT sea único
        if rut and CustomUser.objects.filter(rut=rut).exists():
            raise ValidationError("Este RUT ya está en uso.")

        # Verifica que el número de teléfono sea único
        if numero_telefono and CustomUser.objects.filter(numero_telefono=numero_telefono).exists():
            raise ValidationError("Este número de teléfono ya está en uso.")

        return cleaned_data

    
    def clean_email(self):
        """Verifica si el correo electrónico ya está en uso."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email
    
    def save(self, commit=True):
        """Guarda el usuario con la contraseña encriptada."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ReseñaForm(forms.ModelForm):
    """Formulario para crear una reseña."""
    
    class Meta:
        model = Reseña
        fields = ['contenido', 'calificacion']
        widgets = {
            'calificacion': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),  # Calificaciones de 1 a 5
        }
        
class ImagenReseñaForm(forms.ModelForm):
    """Formulario para subir imágenes de una reseña."""
    
    class Meta:
        model = ImagenReseña
        fields = ['imagen']


#MODELO TRABAJOS
class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ['titulo', 'descripcion', 'presupuesto_minimo', 'presupuesto_maximo', 'region', 'comuna']


# forms.py
from django import forms
from .models import Region, Comuna, Habilidades

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['nombre']  # Solo el campo 'nombre' es necesario
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la Región'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

class ComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ['nombre', 'region']  # Necesitamos el campo 'nombre' y el campo 'region'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la Comuna'}),
            'region': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['region'].widget.attrs.update({'class': 'form-control'})

class HabilidadesForm(forms.ModelForm):
    class Meta:
        model = Habilidades
        fields = ['nombre']  # Solo el campo 'nombre' es necesario
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la Habilidad'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
