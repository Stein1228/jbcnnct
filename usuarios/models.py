from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth import get_user_model
from django.db.models import Avg


def validar_fecha_nacimiento(value):
    """Valida que la fecha de nacimiento no sea futura y que el usuario tenga al menos 18 años."""
    hoy = date.today()
    
    # Verifica que la fecha no sea futura
    if value > hoy:
        raise ValidationError('La fecha de nacimiento no puede ser futura.')

    # Calcula la edad
    edad = hoy.year - value.year - ((hoy.month, hoy.day) < (value.month, value.day))
    
    # Verifica que la edad sea al menos 18 años
    if edad < 18:
        raise ValidationError('Debes tener al menos 18 años para registrarte.')


class CustomUserManager(BaseUserManager):
    """Manejador personalizado para el modelo de usuario."""
    
    def create_user(self, email, rut, first_name, last_name, fecha_nacimiento, 
                    numero_telefono, genero, nacionalidad, password=None, **extra_fields):
        """Crea y devuelve un usuario con un correo electrónico y una contraseña."""
        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')
        
        # Normaliza el correo electrónico
        email = self.normalize_email(email)
        
        # Crea el usuario
        user = self.model(
            email=email,
            rut=rut,
            first_name=first_name,
            last_name=last_name,
            fecha_nacimiento=fecha_nacimiento,
            numero_telefono=numero_telefono,
            genero=genero,
            nacionalidad=nacionalidad,
            **extra_fields
        )
        
        # Establece la contraseña y guarda el usuario
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, rut, first_name, last_name, fecha_nacimiento, 
                         numero_telefono, genero, nacionalidad, password=None, **extra_fields):
        """Crea y devuelve un superusuario con un correo electrónico y una contraseña."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            email=email,
            rut=rut,
            first_name=first_name,
            last_name=last_name,
            fecha_nacimiento=fecha_nacimiento,
            numero_telefono=numero_telefono,
            genero=genero,
            nacionalidad=nacionalidad,
            password=password,
            **extra_fields
        )

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='comunas')

    def __str__(self):
        return self.nombre
        
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado que extiende AbstractBaseUser y PermissionsMixin."""
    
    # Opciones de nacionalidad
    NATIONALITY_CHOICES = [
        ('CL', 'Chilena'),
        ('AR', 'Argentina'),
        ('BR', 'Brasileña'),
        ('VE', 'Venezolana'),
        ('PE', 'Peruana'),
        ('CO', 'Colombiana'),
        # Agregar otros países según sea necesario
    ]

    GENERO_CHOICES = [
        ('M', 'Masculino'), 
        ('F', 'Femenino'), 
        ('O', 'Otro')
    ]

    # Información básica del usuario
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12)  
    first_name = models.CharField(max_length=30)
    s_nombre = models.CharField(max_length=30, blank=True, null=True) 
    last_name = models.CharField(max_length=30)
    s_apellido = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField(validators=[validar_fecha_nacimiento])
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True) 
    
    numero_telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="El número debe estar en el formato: +999999999")]
    )
    
    # Datos extra del usuario
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    nacionalidad = models.CharField(max_length=15, choices=NATIONALITY_CHOICES)
    instagram = models.URLField(max_length=150, blank=True, null=True)
    facebook = models.URLField(max_length=150, blank=True, null=True)
    trabajos_realizados = models.PositiveIntegerField(default=0)
    trabajos_solicitados = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Relación ManyToMany con habilidades
    habilidades = models.ManyToManyField('Habilidades', blank=True)

    # Configuración de campos requeridos
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rut', 'first_name', 'last_name', 'fecha_nacimiento', 'numero_telefono', 'genero', 'nacionalidad']

    # Manejador de usuario personalizado
    objects = CustomUserManager()

    # Configuración de grupos y permisos para evitar conflictos
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True)

    def calificacion_promedio(self):
        """Calcula la calificación promedio del usuario."""
        calificacion_promedio = self.reseñas_recibidas.aggregate(Avg('calificacion'))['calificacion__avg']
        
        # Devuelve 0 si no hay calificaciones (calificacion_promedio es None)
        if calificacion_promedio is None:
            return 0  # Devuelve 0 si no hay reseñas
        else:
            return round(calificacion_promedio, 1)  # Redondea a 1 decimal
        
    def get_full_name(self):
        """Devuelve el nombre completo del usuario."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name
    
    def calcular_edad(self):
        """Calcula la edad del usuario."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return edad

    def __str__(self):
        """Representación en cadena del modelo CustomUser."""
        return f"{self.first_name} {self.last_name}"


class Habilidades(models.Model):
    """Modelo para representar las habilidades de los usuarios."""
    
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """Representación en cadena del modelo Habilidades."""
        return self.nombre
    
class Reseña(models.Model):
    """Modelo para representar las reseñas entre usuarios."""
    
    Usuario = get_user_model()
    usuario_revisor = models.ForeignKey(Usuario, related_name='reseñas_realizadas', on_delete=models.CASCADE)
    usuario_revisado = models.ForeignKey(Usuario, related_name='reseñas_recibidas', on_delete=models.CASCADE)
    contenido = models.TextField(max_length=500)
    calificacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Representación en cadena del modelo Reseña."""
        return f'Reseña de {self.usuario_revisor.get_full_name()} para {self.usuario_revisado.get_full_name()}'


class ImagenReseña(models.Model):
    """Modelo para representar imágenes asociadas a reseñas."""
    
    reseña = models.ForeignKey(Reseña, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='reseñas/', null=True, blank=True)

    def __str__(self):
        """Representación en cadena del modelo ImagenReseña."""
        return f"Imagen para la reseña de {self.reseña.usuario_revisor.get_full_name()}"


#MODELO TRABAJOS

class Trabajo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    presupuesto_minimo = models.IntegerField()
    presupuesto_maximo = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    usuario_creador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='trabajos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    is_disponible = models.BooleanField(default=True)  
    trabajador_seleccionado = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL,related_name="trabajos_seleccionados")
    is_completado = models.BooleanField(default=False)
    habilidades = models.ManyToManyField('Habilidades', blank=True)
    forma_pago = models.CharField(max_length=50, null=True, blank=True) 
    pago_final = models.IntegerField(null=True, blank=True)
    
    def str(self):
        return self.titulo

class Postulacion(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='postulaciones')
    usuario_postulante = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='postulaciones')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(blank=True, null=True)

    def str(self):
        return f'{self.usuario_postulante.username} - {self.trabajo.titulo}'