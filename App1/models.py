from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    nombre = models.CharField(max_length=50)
    detalles = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rut = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.user.first_name if self.user else "Usuario sin nombre"

class Habitacion(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    orientacion = models.CharField(max_length=20)

    def __str__(self):
        return f"Habitación {self.numero}"

class Reserva(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    cantidad_dias = models.PositiveIntegerField()

    def __str__(self):
        return f"Reserva - Habitación {self.habitacion.numero} - {self.fecha_reserva} ({self.cantidad_dias} días)"

class Pasajero(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True, blank=True)
    reservas = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True, blank=True)
    responsable = models.BooleanField(default=False)

    def __str__(self):
        return self.persona.user.username if self.persona and self.persona.user else "Pasajero desconocido"
    
class Empleado(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.persona and self.persona.user:
            return f"{self.persona.user.first_name} {self.persona.user.last_name}"
        return "Empleado sin nombre"

class Servicio(models.Model):
    responsable = models.ForeignKey(Pasajero, on_delete=models.CASCADE, null=True)
    checkIn = models.DateTimeField()
    checkOut = models.DateTimeField(null=True, blank=True)
    enUso = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Servicio - {self.responsable.persona.user.first_name if self.responsable and self.responsable.persona and self.responsable.persona.user else 'Sin responsable'}"

class RegistroAlojamiento(models.Model):
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, null=True)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True)

    def __str__(self):
        nombre_pasajero = self.pasajero.persona.user.first_name if self.pasajero and self.pasajero.persona and self.pasajero.persona.user else "Pasajero desconocido"
        return f"Registro - {nombre_pasajero} en Habitación {self.habitacion.numero if self.habitacion else 'N/A'}"


