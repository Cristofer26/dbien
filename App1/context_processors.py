from .models import Pasajero, Empleado

def es_pasajero(user):
    return Pasajero.objects.filter(persona__user=user).exists()

def es_empleado(user):
    return Empleado.objects.filter(persona__user=user).exists()

def tiene_perfil(user, nombre_perfil):
    return Empleado.objects.filter(persona__user=user, perfil__nombre=nombre_perfil).exists()

def es_administrador(user):
    return tiene_perfil(user, 'Administrador')

def es_encargado(user):
    return tiene_perfil(user, 'Encargado')

def user_status(request):
    return {
        'es_pasajero': es_pasajero(request.user) if request.user.is_authenticated else False,
        'es_empleado': es_empleado(request.user) if request.user.is_authenticated else False,
        'es_administrador': es_administrador(request.user) if request.user.is_authenticated else False,
        'es_encargado': es_encargado(request.user) if request.user.is_authenticated else False,
    }