from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pasajero, Habitacion, Reserva, Servicio, RegistroAlojamiento, Empleado, Perfil, Persona

# Personalización de la administración del modelo Persona
class PasajeroAdmin(admin.ModelAdmin):
    readonly_fields = ('id',) 

class HabitacionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  

class ReservaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',) 

class ServicioAdmin(admin.ModelAdmin):
    readonly_fields = ('id',) 

class RegistroAlojamientoAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  

class EmpleadoAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  

class PerfilAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  


class PersonaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  

# Registro de los modelos con las configuraciones personalizadas
admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Pasajero)
admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Servicio)
admin.site.register(RegistroAlojamiento)
admin.site.register(Empleado)
admin.site.register(Perfil)
admin.site.register(Persona)