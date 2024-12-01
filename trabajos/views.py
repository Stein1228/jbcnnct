from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse

from usuarios.models import Trabajo, Postulacion, Habilidades, Region, Comuna
from .forms import TrabajoForm, PostulacionForm

User = get_user_model()

# Función para enviar correos
def enviar_correo(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
    )

# Función para actualizar los contadores de trabajos realizados y solicitados
def actualizar_contadores(trabajo):
    trabajo.usuario_creador.trabajos_solicitados += 1
    trabajo.trabajador_seleccionado.trabajos_realizados += 1
    trabajo.usuario_creador.save()
    trabajo.trabajador_seleccionado.save()

# Vista para mostrar trabajos disponibles
@login_required
def trabajos(request):
    trabajos = Trabajo.objects.filter(is_disponible=True).exclude(usuario_creador=request.user)
    habilidades = Habilidades.objects.all()
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()

    habilidades_filter = request.GET.getlist('habilidades')
    if habilidades_filter:
        trabajos = trabajos.filter(habilidades__id__in=habilidades_filter).distinct()

    region_filter = request.GET.get('region')
    if region_filter:
        trabajos = trabajos.filter(region__id=region_filter)

    comuna_filter = request.GET.get('comuna')
    if comuna_filter:
        trabajos = trabajos.filter(comuna__id=comuna_filter)

    search_query = request.GET.get('search', '')
    if search_query:
        trabajos = trabajos.filter(
            Q(titulo__icontains=search_query) | 
            Q(descripcion__icontains=search_query) | 
            Q(comuna__nombre__icontains=search_query) |
            Q(region__nombre__icontains=search_query) |
            Q(habilidades__nombre__icontains=search_query)
        ).distinct()

    paginator = Paginator(trabajos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Verificar si el usuario ya ha postulado a algún trabajo
    postulaciones = Postulacion.objects.filter(usuario_postulante=request.user)
    postulaciones_trabajos = postulaciones.values_list('trabajo', flat=True)

    return render(request, 'trabajos/trabajos.html', {
        'trabajos': page_obj,
        'search_query': search_query,
        'habilidades': habilidades,
        'regiones': regiones,
        'comunas': comunas,
        'postulaciones_trabajos': postulaciones_trabajos, # Pasamos la lista de postulaciones al template
    })


# Vista para crear un nuevo trabajo
@login_required
def crear_trabajo(request):
    if request.method == 'POST':
        form = TrabajoForm(request.POST)
        if form.is_valid():
            trabajo = form.save(commit=False)
            trabajo.usuario_creador = request.user
            trabajo.save()
            form.save_m2m()

            habilidades_trabajo = trabajo.habilidades.all()
            usuarios_afines = User.objects.filter(habilidades__in=habilidades_trabajo).distinct()
            trabajo_url = request.build_absolute_uri(reverse('detalle_trabajo', args=[trabajo.id]))

            for usuario in usuarios_afines:
                enviar_correo(
                    subject="Nuevo Trabajo Relacionado a tus Habilidades",
                    message = f"""
                        Hola {usuario.get_full_name()}, 

                        ¡Buenas noticias! Se ha publicado un nuevo trabajo que creemos que puede ser de tu interés. Este trabajo coincide con las habilidades que has demostrado en nuestra plataforma y creemos que podrías ser una excelente opción para este proyecto.

                        El trabajo titulado "{trabajo.titulo}" está ahora disponible, y podrías ser el candidato ideal para llevarlo a cabo. Te invitamos a revisar los detalles y postularte si estás interesado. Aquí tienes la información clave sobre el trabajo:

                        - Título del trabajo: {trabajo.titulo}
                        - Ubicación: {trabajo.comuna}, {trabajo.region}

                        Para obtener más detalles sobre este trabajo y postularte, simplemente haz clic en el siguiente enlace:  
                        {trabajo_url}

                        Te animamos a que actúes rápidamente, ya que los trabajos populares tienden a recibir muchas postulaciones. Si tienes alguna pregunta o necesitas más información sobre el trabajo, no dudes en ponerte en contacto con nosotros. Estamos aquí para ayudarte.

                        ¡Esperamos que esta oportunidad sea perfecta para ti!

                        Saludos cordiales,  
                        Jobconnect
                        """,
                    recipient_email=usuario.email
                )
            # Agregar un mensaje de éxito
            messages.success(request, "El trabajo se ha creado exitosamente.")
            return redirect('ver_trabajos')
    else:
        form = TrabajoForm()
    return render(request, 'trabajos/crear_trabajo.html', {'form': form})

# Vista para editar un trabajo
@login_required
def editar_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    if request.method == 'POST':
        form = TrabajoForm(request.POST, instance=trabajo)
        if form.is_valid():
            trabajo = form.save(commit=False)
            trabajo.save()
            form.save_m2m()
            messages.success(request, "Trabajo editado con éxito!")  # Mensaje de éxito
            if request.user.is_staff:
                return redirect('trabajos')
            else:
                return redirect('ver_trabajos')
    else:
        form = TrabajoForm(instance=trabajo)
    return render(request, 'trabajos/editar_trabajo.html', {'form': form, 'trabajo': trabajo})

# Vista para eliminar un trabajo
@login_required
def eliminar_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    if request.method == 'POST':
        trabajo.delete()
        return redirect('trabajos')
    return render(request, 'trabajos/eliminar_trabajo.html', {'trabajo': trabajo})

# Vista para postular a un trabajo
@login_required
def postular_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)

    if request.method == 'POST':
        form = PostulacionForm(request.POST)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.trabajo = trabajo
            postulacion.usuario_postulante = request.user
            postulacion.save()

            empleador = trabajo.usuario_creador
            postulante = request.user
            
            # Crear el mensaje de correo en texto plano
            subject = f'Nuevo postulante para el trabajo: {trabajo.titulo}'
            message = f"""
            Hola {empleador.get_full_name()},\n\n

            El usuario {postulante.get_full_name()} ha postulado al trabajo: {trabajo.titulo}.\n
            Puedes ver su perfil haciendo clic en el siguiente enlace:\n
            {request.build_absolute_uri(f'/usuarios/usuario/{postulante.id}')}\n\n

            Gracias por usar JobConnect.
            """

            # Enviar el correo utilizando la función personalizada
            enviar_correo(subject, message, empleador.email)
            
            messages.success(request, f'Has postulado al trabajo: {trabajo.titulo} correctamente!.')
            messages.info(request, f'El usuario {request.user.get_full_name()} ha postulado al trabajo: {trabajo.titulo}.')
            return redirect('trabajos')
    else:
        form = PostulacionForm()

    return render(request, 'trabajos/postular_trabajo.html', {'form': form, 'trabajo': trabajo})

# Vista para ver las postulaciones de un trabajo
@login_required
def ver_postulaciones(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    postulaciones = trabajo.postulaciones.all()
    return render(request, 'trabajos/ver_postulaciones.html', {'trabajo': trabajo, 'postulaciones': postulaciones})

# Vista para mostrar los trabajos creados por el usuario
@login_required
def ver_trabajos(request):
    # Obtener el valor del filtro 'completado' desde la URL. Si no está presente, se asume que es False.
    completado = request.GET.get('completado', 'False') == 'True'
    
    # Filtrar trabajos según el usuario y el estado de completado
    trabajos = Trabajo.objects.filter(usuario_creador=request.user, is_completado=completado)

    # Calcular el valor opuesto de completado para usar en el enlace de la plantilla
    completado_opuesto = not completado

    if request.method == 'POST':
        trabajo_id = request.POST.get('trabajo_id')
        trabajo = get_object_or_404(Trabajo, id=trabajo_id)
        trabajo.delete()
        messages.success(request, f'Trabajo "{trabajo.titulo}" eliminado correctamente.', extra_tags=f"trabajo-eliminado-{trabajo.id}")
        return redirect('ver_trabajos')
    
    return render(request, 'trabajos/ver_trabajos.html', {
        'trabajos': trabajos,
        'completado': completado,  # Pasar el valor del filtro a la plantilla
        'completado_opuesto': completado_opuesto  # Pasar el valor opuesto a la plantilla
    })

# Vista para seleccionar al trabajador para un trabajo
def seleccionar_trabajador(request, trabajo_id, postulante_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    postulante = get_object_or_404(Postulacion, id=postulante_id, trabajo=trabajo)

    if not trabajo.is_disponible:
        messages.error(request, "Este trabajo ya no está disponible.")
        return redirect('match', trabajo_id=trabajo.id)

    trabajo.is_disponible = False
    trabajo.trabajador_seleccionado = postulante.usuario_postulante
    trabajo.save()

    Postulacion.objects.filter(trabajo=trabajo).exclude(id=postulante.id).delete()

    enviar_correo(
        subject='Has sido seleccionado para un trabajo',
        message = f'''
            Hola {trabajo.trabajador_seleccionado.get_full_name()}, 

            ¡Felicitaciones! Has sido seleccionado para el trabajo "{trabajo.titulo}". 
            Por favor, comunícate con el empleador para coordinar los siguientes pasos.

            Detalles de contacto del empleador:
            Nombre: {trabajo.usuario_creador.get_full_name()}
            Correo electrónico: {trabajo.usuario_creador.email}
            Número de contacto: {trabajo.usuario_creador.numero_telefono if trabajo.usuario_creador.numero_telefono else 'No disponible'}

            Saludos,
            JobConnect
            ''',
        recipient_email=trabajo.trabajador_seleccionado.email
    )

    messages.success(request, "Has seleccionado al trabajador.")
    return redirect('match', trabajo_id=trabajo.id)

# Vista de detalles de un trabajo
def detalle_trabajo(request, trabajo_id):
    # Obtener el trabajo
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    
    # Obtener las postulaciones del usuario
    postulaciones = Postulacion.objects.filter(usuario_postulante=request.user)
    postulaciones_trabajos = postulaciones.values_list('trabajo', flat=True)
    
    # Verificar si el trabajo ya fue postulado por el usuario
    if trabajo.id in postulaciones_trabajos:
        trabajo_postulado = True
    else:
        trabajo_postulado = False
    
    # Verificar si el trabajo no está disponible
    if not trabajo.is_disponible:
        messages.info(request, "Este trabajo ya ha sido asignado a un trabajador y no está disponible.")
    
    return render(request, 'trabajos/detalle_trabajo.html', {
        'trabajo': trabajo,
        'trabajo_postulado': trabajo_postulado,  # Pasar la variable que indica si ya se postuló
    })
    
# Vista para ver el resumen del match entre empleador y trabajador
@login_required
def resumen_match(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)

    if not trabajo.trabajador_seleccionado:
        messages.error(request, "Este trabajo no tiene un trabajador asignado.")
        return redirect('trabajos')

    empleador = trabajo.usuario_creador
    trabajador = trabajo.trabajador_seleccionado

    contexto = {
        'trabajo': trabajo,
        'empleador': empleador,
        'trabajador': trabajador,
        'empleador_calificacion': empleador.calificacion_promedio(),
        'trabajador_calificacion': trabajador.calificacion_promedio(),
        'empleador_edad': empleador.calcular_edad(),
        'trabajador_edad': trabajador.calcular_edad()
    }

    return render(request, 'trabajos/resumen.html', contexto)
    
# Vista para seleccionar la forma de pago (efectivo, transferencia, débito/crédito)
@login_required
def seleccionar_forma_pago(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)

    # Verificar que el trabajo tiene un trabajador seleccionado
    if not trabajo.trabajador_seleccionado:
        messages.error(request, "Este trabajo no tiene un trabajador asignado.")
        return redirect('trabajos')

    if request.method == 'POST':
        forma_pago = request.POST.get('forma_pago')
        pago_final = request.POST.get('pago_final') 

        # Validación de la forma de pago
        if forma_pago not in ['efectivo', 'transferencia', 'debito_credito']:
            messages.error(request, "Forma de pago no válida.")
            return redirect('seleccionar_forma_pago', trabajo_id=trabajo.id)

        # Validación del monto final
        if not pago_final or Decimal(pago_final) <= 0:
            messages.error(request, "El monto final debe ser un valor válido y mayor que 0.")
            return redirect('seleccionar_forma_pago', trabajo_id=trabajo.id)

        # Actualizamos el trabajo con la forma de pago y el monto final
        trabajo.forma_pago = forma_pago
        trabajo.pago_final = Decimal(pago_final)  # Guardamos el monto final
        trabajo.is_completado = True  # Marcar el trabajo como completado
        trabajo.save()

        # Actualizamos los contadores de trabajos realizados y solicitados
        actualizar_contadores(trabajo)

        # Enviar correo al trabajador seleccionado
        enviar_correo(
            subject='Forma de pago seleccionada para tu trabajo',
            message=f"""
                Hola {trabajo.trabajador_seleccionado.get_full_name()},
                
                ¡Felicidades! El trabajo "{trabajo.titulo}" ha sido marcado como completado, y se ha seleccionado la forma de pago: {forma_pago}.
                
                El monto final acordado para el pago es: {pago_final} CLP.
                
                Ahora que el trabajo está completo y la forma de pago ha sido acordada, te recomendamos que coordines con el empleador para cerrar todos los detalles finales y proceder con el pago.
                
                Si tienes preguntas, por favor no dudes en ponerte en contacto con nosotros.
                
                ¡Gracias por ser parte de nuestra plataforma!
                
                Saludos,
                El equipo de JobConnect.
            """,
            recipient_email=trabajo.trabajador_seleccionado.email
        )

        messages.success(request, f'La forma de pago y el monto final han sido seleccionados correctamente.')
        return redirect('ver_trabajos')

    return render(request, 'trabajos/seleccionar_forma_pago.html', {'trabajo': trabajo})


@login_required
def trabajos_asignados(request):
    # Obtener el valor del filtro 'completado' desde la URL. Si no está presente, se asume que es False.
    completado = request.GET.get('completado', 'False') == 'True'
    
    # Filtrar los trabajos asignados según el estado de completado
    trabajos = Trabajo.objects.filter(trabajador_seleccionado=request.user, is_completado=completado)

    # Calcular el valor opuesto de completado para usar en el enlace de la plantilla
    completado_opuesto = not completado

    return render(request, 'trabajos/trabajos_asignados.html', {
        'trabajos': trabajos,
        'completado': completado,  # Pasar el valor del filtro a la plantilla
        'completado_opuesto': completado_opuesto  # Pasar el valor opuesto a la plantilla
    })