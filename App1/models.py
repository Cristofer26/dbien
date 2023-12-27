from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    nombre = models.CharField(max_length=50)
    detalles = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rut = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name() if self.user else  "Persona sin nombre"

class Habitacion(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    orientacion = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"Habitación {self.numero}"
    
    def esta_disponible(self):
        # Buscar en RegistroAlojamiento si esta habitación está siendo utilizada
        # en algún servicio cuyo checkout es None
        ocupaciones = RegistroAlojamiento.objects.filter(
            habitacion=self,
            servicio__checkOut=None
        )

        # Si hay alguna ocupación, la habitación no está disponible
        return not ocupaciones.exists()

    @property
    def disponibilidad(self):
        return "Disponible" if self.esta_disponible() else "Ocupada"

class Pasajero(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.persona.user.get_full_name() if self.persona and self.persona.user else "Pasajero desconocido"
    
    def delete(self, *args, **kwargs):
        super(Pasajero, self).delete(*args, **kwargs)
        self.persona.delete()
        self.persona.user.delete()

class Servicio(models.Model):
    checkIn = models.DateTimeField(auto_now_add=True)
    checkOut = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    es_responsable = models.ForeignKey(Pasajero, on_delete=models.SET_NULL, null=True, related_name='servicios_responsables')
    def __str__(self):
        return f"Servicio {self.id} - Estado: {'En uso' if not self.checkOut else 'Terminado'}"
    
    @property
    def estado(self):
        return 'En uso' if not self.checkOut else 'Terminado'

    def finalizar_servicio(self):
        self.checkOut = timezone.now()
        self.total = self.calcular_total()
        self.save()

    def calcular_total(self):
        if self.checkOut and self.checkIn:
            duracion = self.checkOut - self.checkIn
            dias = duracion.days
            if duracion.seconds > 0:
                dias += 1  # Agregar un día extra si hay fracción de día

            total = sum(registro.habitacion.precio for registro in self.registros.all()) * dias
            return total
        return 0


    
class Reserva(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    cantidad_dias = models.PositiveIntegerField()
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name='reservas', default="", null=True, blank=True)

    def __str__(self):
        return f"Reserva - Habitación {self.habitacion.numero} - {self.fecha_reserva} ({self.cantidad_dias} días)"

class Empleado(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.persona and self.persona.user:
            return self.persona.user.get_full_name() if self.persona and self.persona.user else "Empleado desconocido"
        
    def delete(self, *args, **kwargs):
        super(Empleado, self).delete(*args, **kwargs)
        self.persona.delete()
        self.persona.user.delete()


class RegistroAlojamiento(models.Model):
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, related_name='registros', on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['servicio', 'pasajero']

    def __str__(self):
        return f"Pasajero en Servicio {self.servicio.id}: {self.pasajero}"
 
